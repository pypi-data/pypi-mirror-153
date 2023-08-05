from peegy.processing.pipe.definitions import InputOutputProcess
from peegy.processing.tools.epochs_processing_tools import et_impulse_response_artifact_subtraction
from sklearn.linear_model import LinearRegression
import numpy as np
import os
from peegy.processing.tools.multiprocessing.multiprocessesing_filter import filt_data
import astropy.units as u
from peegy.tools.units.unit_tools import set_default_unit
from PyQt5.QtCore import QLibraryInfo
from tqdm import tqdm
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(QLibraryInfo.PluginsPath)


class RegressOutArtifact(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 event_code: float = None,
                 artifact_window: float = 0.01,
                 alternating_polarity: bool = False,
                 stimulus_waveform: np.array = None,
                 method: str = 'regression',
                 **kwargs):
        """
        This InputOutputProcess will remove an artifact which has the shape of the input stimulus_waveform
        :param input_process: InputOutputProcess Class
        :param event_code: event code where the stimulus waveform starts
        :param artifact_window: time from onset where we only expect artifacts (free of neural response)
        :param alternating_polarity: indicate whether the paradigm used an alternating polarity scheme. the
        stimulus_waveform will be alternating in polarity accord
        :param stimulus_waveform: single column numpy array with the target waveform artifact
        :param method: either 'regression' or 'xcorr'. A regression model or an scaled amplitude based on cross
        correlation will be used to estimate the amount of artifact
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(RegressOutArtifact, self).__init__(input_process=input_process, **kwargs)
        self.event_code = event_code
        self.artifact_window = set_default_unit(artifact_window, u.s)
        self.alternating_polarity = alternating_polarity
        self.stimulus_waveform = set_default_unit(stimulus_waveform, u.uV)
        self.method = method

    def transform_data(self):
        data = self.input_node.data.copy()
        # if event code is given, convolve source with dirac train to generate entire signal
        subset_idx = np.arange(0, int(self.input_node.fs * self.artifact_window))
        _events_index = None
        if self.event_code is not None:
            _events_index = self.input_node.events.get_events_index(code=self.event_code, fs=self.input_node.fs)
            events = np.zeros(data.shape[0])
            events[_events_index] = 1
            if self.alternating_polarity:
                events[_events_index[1: -1: 2]] = -1
            #  convolve source with triggers
            source = filt_data(input_data=self.stimulus_waveform, b=events.flatten(), mode='full', onset_padding=False)
            source = source[0: data.shape[0]]
        else:
            source = self.stimulus_waveform[0: data.shape[0]]

        if self.method == 'regression':
            for _idx in np.arange(data.shape[1]):
                regression = LinearRegression()
                regression.fit(source[subset_idx], data[subset_idx, _idx])
                data[:, _idx] -= regression.predict(source) * source.unit
        if self.method == 'xcorr':
            if data.ndim == 2:
                transmission_index = data[subset_idx, :].T.dot(source[subset_idx]) / np.expand_dims(
                    np.sum(np.square(source[subset_idx])), axis=0)
                data -= np.tile(np.atleast_2d(source), (1, data.shape[1])) * transmission_index.T
            if data.ndim == 3:
                ave_data = np.mean(data, 2)
                transmission_index = ave_data[subset_idx, :].T.dot(source[subset_idx]) / np.expand_dims(
                    np.sum(np.square(source[subset_idx])), axis=0)
                data -= np.tile(np.atleast_3d(source * transmission_index.T), (1, 1, data.shape[2]))
        if self.method == 'xcorr_by_event' and _events_index is not None:
            reconstructed = np.zeros(data.shape)
            # we recreate a peak template
            _template = self.stimulus_waveform
            for _idx in tqdm(_events_index, desc='Artefact reconstruction'):
                _current_template = _template
                _ini = _idx
                _end = _idx + _template.shape[0]
                if _end > data.shape[0]:
                    _current_template = _template[0:-(_end - data.shape[0]), :]
                original = data[_ini: _end, :]
                transmission_index = original[subset_idx, :].T.dot(_current_template[subset_idx]) / np.expand_dims(
                    np.sum(np.square(_current_template[subset_idx])), axis=0)
                reconstructed[_ini: _end, :] = np.repeat(
                    _current_template,
                    data.shape[1],
                    axis=1) * transmission_index.T
            data -= reconstructed

        self.output_node.data = data


class RegressOutArtifactIR(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 stimulus_waveform: np.array = None,
                 ir_length: float = 0.01,
                 regularization_factor: float = 1,
                 **kwargs):
        """
        This InputOutputProcess will remove an artifact which has the shape of the input stimulus_waveform.
        Here, artifact is estimated from the impulse response. The latter is estimated by averaging individual
        impulse responses across epochs.
        :param input_process: InputOutputProcess Class
        stimulus_waveform will be alternating in polarity accord
        :param stimulus_waveform: single column numpy array with the target waveform artifact
        :param ir_length: estimated length in seconds of impulse response
        :param regularization_factor: This value is used to regularize the deconvolution based on Tikhonov
        regularization allow to estimate the transfer function when the input signal is sparse in frequency components
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(RegressOutArtifactIR, self).__init__(input_process=input_process, **kwargs)
        self.stimulus_waveform = stimulus_waveform
        self.ir_length = ir_length
        self.regularization_factor = regularization_factor
        self.recovered_artifact = None

    def transform_data(self):
        data = self.input_node.data.copy()
        # compute impulse response
        clean_data, _recovered_artifact = et_impulse_response_artifact_subtraction(
            data=data,
            stimulus_waveform=self.stimulus_waveform,
            ir_length=int(self.ir_length * self.input_node.fs),
            regularization_factor=self.regularization_factor)
        self.recovered_artifact = _recovered_artifact
        self.output_node.data = clean_data
