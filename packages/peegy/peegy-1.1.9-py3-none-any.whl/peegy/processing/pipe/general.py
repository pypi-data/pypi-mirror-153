from peegy.processing.pipe.definitions import InputOutputProcess
from peegy.processing.tools.epochs_processing_tools import et_subtract_oeg_template, et_subtract_correlated_ref, \
    filt_filt_data
import matplotlib.pyplot as plt
import peegy.processing.tools.filters.eegFiltering as eegf
from peegy.processing.tools.eeg_epoch_operators import et_unfold
import numpy as np
from sklearn.decomposition import FastICA
from sklearn.cross_decomposition import CCA
import itertools
import os
import astropy.units as u
from peegy.tools.units.unit_tools import set_default_unit
from PyQt5.QtCore import QLibraryInfo
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(QLibraryInfo.PluginsPath)


class ReSampling(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 new_sampling_rate: u.quantity.Quantity = None,
                 **kwargs):
        """
        This InputOutputProcess class will resample the data to the new_sampling_rate
        :param input_process: InputOutputProcess Class
        :param new_sampling_rate: float indicating the new sampling rate
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(ReSampling, self).__init__(input_process=input_process, **kwargs)
        self.new_sampling_rate = set_default_unit(new_sampling_rate, u.Hz)

    def transform_data(self):
        data, _factor = eegf.eeg_resampling(x=self.input_node.data,
                                            factor=self.new_sampling_rate / self.input_node.fs)
        self.output_node.data = data
        self.output_node.fs = self.input_node.fs * _factor
        self.output_node.process_history.append(self.process_parameters)


class ReferenceData(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 reference_channels: [str] = None,
                 remove_reference=True,
                 invert_polarity=False,
                 **kwargs):
        """
        This class will reference the data by subtracting the reference_channels (mean) from each individual channel
        :param input_process: InputOutputProcess Class
        :param reference_channels: list of string with the reference channels labels, if empty across channel average
        will be used
        :param remove_reference: boolean indicating whether to keep or remove the reference channel from the data
        :param invert_polarity: boolean indicating if channels polarity will be polarity inverted (data * -1)
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(ReferenceData, self).__init__(input_process=input_process, **kwargs)
        if reference_channels is None:
            reference_channels = ['']
        self.reference_channels = reference_channels
        self.remove_reference = remove_reference
        self.invert_polarity = invert_polarity

    def transform_data(self):
        _ch_idx = self.input_node.get_channel_idx_by_label(self.reference_channels)
        if not _ch_idx.size:
            self.remove_reference = False
            _ch_idx = np.arange(self.input_node.layout.size)
        print('Referencing data to: ' + ''.join(['{:s} '.format(_ch.label) for _ch in self.input_node.layout[_ch_idx]]))
        reference = np.mean(self.input_node.data[:, _ch_idx], axis=1, keepdims=True)
        self.output_node.data = (self.input_node.data - reference) * (-1.0) ** self.invert_polarity

        if self.remove_reference:
            self.output_node.delete_channel_by_idx(_ch_idx)


class FilterData(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 high_pass: u.quantity.Quantity = None,
                 low_pass: u.quantity.Quantity = None,
                 **kwargs):
        """
        Filter EEG data using a zero group-delay technique
        :param input_process: InputOutputProcess Class
        :param high_pass: Frequency (in Hz) of high-pass filter
        :param low_pass: Frequency (in Hz) of low-pass filter
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(FilterData, self).__init__(input_process=input_process, **kwargs)
        self.low_pass = set_default_unit(low_pass, u.Hz)
        self.high_pass = set_default_unit(high_pass, u.Hz)

    def transform_data(self):
        if self.low_pass is None and self.high_pass is None:
            self.output_node.data = self.input_node.data
            return
        filtered_signal = self.input_node.data.copy()
        _b = eegf.bandpass_fir_win(high_pass=self.high_pass, low_pass=self.low_pass, fs=self.input_node.fs)
        _b = _b * u.dimensionless_unscaled
        filtered_signal = filt_filt_data(input_data=filtered_signal, b=_b)
        self.output_node.data = filtered_signal


class RegressOutEOG(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 ref_channel_labels: [str] = None,
                 method: str = 'template',
                 high_pass: u.quantity.Quantity = 0.1 * u.Hz,
                 low_pass: u.quantity.Quantity = 20.0 * u.Hz,
                 peak_width: u.quantity.Quantity = 0.1 * u.s,
                 template_width: u.quantity.Quantity = 0.6 * u.s,
                 remove_eog_channels: bool = True,
                 save_figure: bool = True,  # save figure
                 fig_format: str = '.png',
                 user_naming_rule: str = '',
                 return_figures: bool = False,
                 **kwargs):
        """
        This class removes EOG artifacts using a template technique. Blinking artifacts are detected and averaged to
        generate a template. This template is scaled for each channel in order to maximize correlation between each
        individual blink and individual events on each channel
        The resulting template is removed from the data, reducing blinks artifacts.
        :param input_process: InputOutputProcess Class
        :param ref_channel_labels: a list with the channel labels that contain the EOG
        :param high_pass: Frequency (in Hz) of high-pass filter all data. This is necessary to generate the template
        :param low_pass: Frequency (in Hz) of low-pass filter only applied to EOG channels
        :param peak_width: default minimum width (in seconds) to detect peaks
        :param template_width: the duration (in seconds) of the time window to average and generate a template
        :param remove_eog_channels: if true EOG channels will be removed once data has been cleaned
        :param save_figure: whether to save or not figures showing the detection and removal of blinks
        :param fig_format: format of output figure
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(RegressOutEOG, self).__init__(input_process=input_process, **kwargs)
        self.ref_channel_labels = ref_channel_labels
        self.low_pass = low_pass
        self.high_pass = high_pass
        self.peak_width = peak_width
        self.template_width = template_width
        self.remove_eog_channels = remove_eog_channels
        self.save_figure = save_figure
        self.fig_format = fig_format
        self.method = method
        self.user_naming_rule = user_naming_rule
        self.return_figures = return_figures

    def transform_data(self):
        data = self.input_node.data.copy()
        _ref_idx = self.input_node.get_channel_idx_by_label(labels=self.ref_channel_labels)
        figure_dir_path = self.input_node.paths.figures_current_dir
        _sep = '_' if self.user_naming_rule is not None else ''
        figure_basename = self.name + _sep + self.user_naming_rule
        artefact_method = self.method
        if artefact_method is None:
            if data.ndim == 3:
                artefact_method = 'correlation'
            else:
                artefact_method = 'template'

        if _ref_idx.size:
            print('Using {:} to remove eog artifacts'.format(artefact_method))
            if artefact_method == 'template':
                data, fig = et_subtract_oeg_template(data=data,
                                                     idx_ref=np.array(_ref_idx),
                                                     high_pass=self.high_pass,
                                                     low_pass=self.low_pass,
                                                     fs=self.input_node.fs,
                                                     template_width=self.template_width,
                                                     plot_results=self.save_figure,
                                                     figure_path=figure_dir_path,
                                                     figure_basename=figure_basename)
            if artefact_method == 'correlation':
                data, fig = et_subtract_correlated_ref(data=data,
                                                       idx_ref=np.array(_ref_idx),
                                                       high_pass=self.high_pass,
                                                       low_pass=self.low_pass,
                                                       fs=self.input_node.fs,
                                                       plot_results=self.save_figure,
                                                       figure_path=figure_dir_path,
                                                       figure_basename=figure_basename)

            if self.return_figures:
                self.figures = fig
            else:
                plt.close(fig)
        else:
            print('Reference channels for eye artefact reduction are not valid! Will return data unaltered.')

        self.output_node.data = data
        if self.remove_eog_channels and _ref_idx.size:
            self.output_node.delete_channel_by_idx(_ref_idx)


class RegressOutICA(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 ref_channel_labels: [str] = None,
                 **kwargs):
        """
        This class uses independent component analysis to remove EOG activity. The removal is based on the correlation
        between the ICA and the reference channels (containing large EOG activity)
        :param input_process: InputOutputProcess Class
        :param ref_channel_labels: a list with the channel labels that contain the EOG
        :param kwargs:
        """
        super(RegressOutICA, self).__init__(input_process=input_process, **kwargs)
        self.ref_channel_labels = ref_channel_labels

    def transform_data(self):
        data = self.input_node.data.copy()
        _ref_idx = self.input_node.get_channel_idx_by_label(labels=self.ref_channel_labels)
        _cov = data[:, _ref_idx]
        _offset = int(data.shape[0] * 0.10)

        # Compute ICA
        print('Performing ICA analysis')
        ica = FastICA(n_components=data.shape[1], max_iter=1000)
        ica.fit(data)
        # decompose signal into components
        components = ica.fit_transform(data)
        corr_coefs = np.empty((components.shape[1], _cov.shape[1]))
        for _i_com, _i_cov in itertools.product(range(components.shape[1]), range(_cov.shape[1])):
            corr_coefs[_i_com, _i_cov] = \
                np.corrcoef(_cov[_offset:-_offset, _i_cov], components[_offset:-_offset, _i_com])[0, 1]
        _idx_to_remove = np.argmax(np.abs(corr_coefs), axis=0)
        print('Maximum correlations: {:}'.format(corr_coefs[np.argmax(np.abs(corr_coefs), axis=0), :]))
        print('Removing components: {:}'.format(_idx_to_remove))
        components[:, _idx_to_remove] = 0
        clean_data = ica.inverse_transform(components)
        self.output_node.data = clean_data


class RegressOutCCA(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess, ref_channel_labels: [str] = None, **kwargs):
        super(RegressOutCCA, self).__init__(input_process=input_process, **kwargs)
        self.channel_labels = ref_channel_labels

    def transform_data(self):
        data = self.input_node.data.copy()
        _ref_idx = self.input_node.get_channel_idx_by_label(labels=self.ref_channel_labels)
        _cov = data[:, _ref_idx]
        # Compute ICA
        print('Performing ICA analysis')

        cca = CCA(n_components=data.shape[1])
        cca.fit(data, _cov)
        # decompose signal into components
        X_c, Y_c = cca.transform(data, _cov)
        # corr_coefs = np.empty((components.shape[1], _cov.shape[1]))
        # for _i_com, _i_cov in itertools.product(range(components.shape[1]), range(_cov.shape[1])):
        #     corr_coefs[_i_com, _i_cov] = \
        #     np.corrcoef(_cov[_offset:-_offset, _i_cov], components[_offset:-_offset, _i_com])[0, 1]
        # _idx_to_remove = np.argmax(np.abs(corr_coefs), axis=0)
        # print('Maximum correlations: {:}'.format(corr_coefs[np.argmax(np.abs(corr_coefs), axis=0), :]))
        # print('Removing components: {:}'.format(_idx_to_remove))
        # components[:, _idx_to_remove] = 0
        # clean_data = ica.inverse_transform(components)

        # self.output_node.data = clean_data


class AutoRemoveBadChannels(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 thr_sd=5.0 * u.dimensionless_unscaled,
                 amp_thr=50000.0 * u.uV,
                 interval=0.001 * u.s,
                 **kwargs):
        """
        This function will try to detect bad channels by looking at the standard deviation across channels.
        It will remove any channels with and std largerd than thr_sd, which is computed across all channels.
        It also remove any channel which amplitude exceeds amp_thr.
        :param input_process: InputOutputProcess Class
        :param thr_sd: threshold standard deviation to remove channels. Channels with larger std will be removed
        :param amp_thr: threshold ampltitude. Channel exceeding this will be removed
        :param interval: time interval to subsample the data before estimating std (this is used to speed up the process
        in very long data files
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(AutoRemoveBadChannels, self).__init__(input_process=input_process, **kwargs)
        self.thr_sd = thr_sd
        self.amp_thr = set_default_unit(amp_thr, u.uV)
        self.interval = set_default_unit(interval, u.s)

    def transform_data(self):
        if self.input_node.data.ndim == 3:
            data = et_unfold(self.input_node.data)
        else:
            data = self.input_node.data
        step_size = np.maximum(int(self.interval * self.input_node.fs), 1)
        _samples = np.arange(0, self.input_node.data.shape[0], step_size).astype(np.int)
        sub_data = data[_samples, :]
        # compute dc component
        _dc_component = np.mean(np.abs(sub_data), axis=0)
        bad_channels = np.where(_dc_component > self.amp_thr)[0]
        _others_idx = np.array([idx for idx in np.arange(sub_data.shape[1]) if idx not in bad_channels], dtype=np.int)
        a_std = np.std(sub_data[:, _others_idx], axis=0)
        thr_ci = self.thr_sd * np.std(a_std) + np.mean(a_std)
        n_ch_idx = np.where(a_std > thr_ci)[0]
        bad_idx = _others_idx[n_ch_idx] if n_ch_idx.size else np.array([], dtype=np.int)
        bad_channels = np.concatenate((bad_channels, bad_idx))
        _bad_channels_index = np.unique(bad_channels)
        self.output_node.data = self.input_node.data.copy()
        self.output_node.delete_channel_by_idx(_bad_channels_index)


class RemoveBadChannels(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess, bad_channels: [str] = None, **kwargs):
        """
        This class will remove any channel passed in bad_channel
        :param input_process: InputOutputProcess Class
        :param bad_channels: list of strings with the label of the channels to be removed
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(RemoveBadChannels, self).__init__(input_process=input_process, **kwargs)
        if bad_channels is None:
            bad_channels = ['']
        self.bad_channels = bad_channels

    def transform_data(self):
        idx_bad_channels = [_i for _i, _item in enumerate(self.input_node.layout) if _item.label in self.bad_channels]
        _bad_channels_index = np.unique(idx_bad_channels)
        self.output_node.data = self.input_node.data.copy()
        if _bad_channels_index.size:
            self.output_node.delete_channel_by_idx(_bad_channels_index)


class BaselineCorrection(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 ini_time: u.quantity.Quantity = None,
                 end_time: u.quantity.Quantity = None,
                 **kwargs):
        """
        This class will remove the mean of the data on each row between the specified times (ini_time and end_time)
        :param input_process: InputOutputProcess Class
        :param ini_time: initial time (in sec) from which mean will be calculated
        :param end_time: end time (in sec) for which the mean will be calculated
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(BaselineCorrection, self).__init__(input_process=input_process, **kwargs)
        self.ini_time = set_default_unit(ini_time, u.s)
        self.end_time = set_default_unit(end_time, u.s)

    def transform_data(self):
        data = self.input_node.data
        ini_time = 0.0 * u.s if self.ini_time is None else self.ini_time
        end_time = np.inf * u.s if self.end_time is None else self.end_time
        _ini_sample = self.input_node.x_to_samples(np.array([ini_time.value]) * ini_time.unit)[0]
        _end_sample = self.input_node.x_to_samples(np.array([end_time.value]) * end_time.unit)[0]
        if np.isinf(_end_sample):
            _end_sample = data.shape[0]
        data = data - np.mean(data[_ini_sample:_end_sample], axis=0)
        self.output_node.data = data
