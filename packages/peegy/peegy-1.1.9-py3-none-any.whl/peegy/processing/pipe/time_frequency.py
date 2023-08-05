from peegy.processing.pipe.definitions import InputOutputProcess
from peegy.processing.tools.epochs_processing_tools import et_mean, et_average_frequency_transformation,\
    et_average_time_frequency_transformation
import multiprocessing
from peegy.plot import eeg_ave_epochs_plot_tools as eegpt
from peegy.definitions.channel_definitions import Domain
import pyfftw
import numpy as np
import os
import astropy.units as u
from PyQt5.QtCore import QLibraryInfo
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(QLibraryInfo.PluginsPath)


class HilbertEnvelope(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess, high_pass=None, low_pass=None, **kwargs):
        """
        This process computes the  Hilbert Envelope of EEG data
        :param input_process: InputOutputProcess Class
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(HilbertEnvelope, self).__init__(input_process=input_process, **kwargs)

    def transform_data(self):
        data = self.input_node.data.copy()
        _fft = pyfftw.builders.fft(data, overwrite_input=False, planner_effort='FFTW_ESTIMATE', axis=0,
                                   threads=multiprocessing.cpu_count())
        fx = _fft()
        n = fx.shape[0]
        h = np.zeros(n)
        if n % 2 == 0:
            h[0] = h[n // 2] = 1
            h[1:n // 2] = 2
        else:
            h[0] = 1
            h[1:(n + 1) // 2] = 2
        _ifft = pyfftw.builders.ifft(fx * h.reshape(-1, 1), overwrite_input=False, planner_effort='FFTW_ESTIMATE',
                                     axis=0,
                                     threads=multiprocessing.cpu_count())
        hilbert_data = _ifft()
        self.output_node.data = np.abs(hilbert_data)


class InducedResponse(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 weighted_average=True,
                 n_tracked_points=256,
                 block_size=5,
                 roi_windows=None, **kwargs):
        super(InducedResponse, self).__init__(input_process=input_process, **kwargs)
        self.weighted_average = weighted_average
        self.n_tracked_points = n_tracked_points
        self.block_size = block_size
        self.roi_windows = roi_windows

    def transform_data(self):
        trials_abs_w_ave, w, rn, cum_rn, w_fft, *_ = \
            et_mean(epochs=np.abs(self.input_node.data),
                    block_size=max(self.block_size, 5),
                    samples_distance=int(max(self.input_node.data.shape[0] // self.n_tracked_points, 10)),
                    roi_windows=self.roi_windows,
                    weighted=self.weighted_average
                    )
        w_ave, w, rn, cum_rn, w_fft, *_ = \
            et_mean(epochs=self.input_node.data,
                    block_size=max(self.block_size, 5),
                    samples_distance=int(max(self.input_node.data.shape[0] // self.n_tracked_points, 10)),
                    roi_windows=self.roi_windows,
                    weighted=self.weighted_average
                    )
        self.output_node.data = trials_abs_w_ave - np.abs(w_ave)
        self.output_node.rn = rn
        self.output_node.cum_rn = cum_rn
        self.output_node.snr = None
        self.output_node.cum_snr = None
        self.output_node.s_var = None


class AverageTimeFrequencyResponse(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 time_window: u.Quantity = 0.3 * u.s,
                 sample_interval: u.Quantity = 0.004 * u.s,
                 topographic_channels=np.array([]),
                 title: str = '',
                 plot_x_lim=None,
                 plot_y_lim=None,
                 times=np.array([]),
                 fig_format='.png',
                 fontsize=12,
                 user_naming_rule: str = '',
                 spec_thresh=4,
                 average_mode='magnitude',
                 **kwargs):
        super(AverageTimeFrequencyResponse, self).__init__(input_process=input_process, **kwargs)
        self.time_window = time_window
        self.sample_interval = sample_interval
        self.frequency = None
        self.time = None
        self.topographic_channels = topographic_channels
        self.title = title
        self.plot_x_lim = plot_x_lim
        self.plot_y_lim = plot_y_lim
        self.fig_format = fig_format
        self.fontsize = fontsize
        self.user_naming_rule = user_naming_rule
        self.times = times
        self.time_window = time_window
        self.sample_interval = sample_interval
        self.spec_thresh = spec_thresh
        self.average_mode = average_mode

    def transform_data(self):
        power, time, freqs = et_average_time_frequency_transformation(epochs=self.input_node.data,
                                                                      fs=self.input_node.fs,
                                                                      time_window=self.time_window,
                                                                      sample_interval=self.sample_interval,
                                                                      average_mode=self.average_mode
                                                                      )
        self.output_node.data = power
        self.output_node.x = time
        self.output_node.y = freqs
        self.output_node.domain = Domain.time_frequency


class PlotTimeFrequencyData(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 topographic_channels=np.array([]),
                 title='',
                 plot_x_lim=None,
                 plot_y_lim=None,
                 times=np.array([]),
                 fig_format='.png',
                 fontsize=12,
                 user_naming_rule='',
                 spec_thresh=4,
                 **kwargs):
        super(PlotTimeFrequencyData, self).__init__(input_process=input_process, **kwargs)
        self.topographic_channels = topographic_channels
        self.title = title
        self.plot_x_lim = plot_x_lim
        self.plot_y_lim = plot_y_lim
        self.fig_format = fig_format
        self.fontsize = fontsize
        self.user_naming_rule = user_naming_rule
        self.times = times
        self.spec_thresh = spec_thresh

    def transform_data(self):
        assert self.input_node.domain == Domain.time_frequency, 'input should be a time-frequency transformed data'

        eegpt.plot_eeg_time_frequency_power(ave_data=self.input_node,
                                            time=self.input_node.x,
                                            frequency=self.input_node.y,
                                            eeg_topographic_map_channels=self.topographic_channels,
                                            figure_dir_path=self.input_node.paths.figures_current_dir,
                                            figure_basename='{:}{:}'.format(
                                                self.input_process.name + '_',
                                                self.user_naming_rule),
                                            time_unit='s',
                                            amplitude_unit='uV',
                                            times=self.times,
                                            title=self.title,
                                            x_lim=self.plot_x_lim,
                                            y_lim=self.plot_y_lim,
                                            fig_format=self.fig_format,
                                            fontsize=self.fontsize,
                                            spec_thresh=self.spec_thresh
                                            )


class AverageSpectrogram(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 topographic_channels=np.array([]),
                 title='',
                 plot_x_lim=None,
                 plot_y_lim=None,
                 times=np.array([]),
                 fig_format='.png',
                 fontsize=12,
                 user_naming_rule='',
                 time_window=2.0,
                 sample_interval=0.004,
                 spec_thresh=4
                 ):
        super(AverageSpectrogram, self).__init__(input_process=input_process)
        self.topographic_channels = topographic_channels
        self.title = title
        self.plot_x_lim = plot_x_lim
        self.plot_y_lim = plot_y_lim
        self.fig_format = fig_format
        self.fontsize = fontsize
        self.user_naming_rule = user_naming_rule
        self.times = times
        self.time_window = time_window
        self.sample_interval = sample_interval
        self.spec_thresh = spec_thresh

    def transform_data(self):
        power, freqs = et_average_frequency_transformation(epochs=self.input_node.data,
                                                           fs=self.input_node.fs,
                                                           ave_mode='magnitude'
                                                           )
        self.output_node.data = power


class AverageFrequencyPower(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 topographic_channels=np.array([]),
                 title='',
                 plot_x_lim=None,
                 plot_y_lim=None,
                 times=np.array([]),
                 fig_format='.png',
                 fontsize=12,
                 user_naming_rule='',
                 **kwargs):
        super(AverageFrequencyPower, self).__init__(input_process=input_process, **kwargs)
        self.frequency = None
        self.time = None
        self.topographic_channels = topographic_channels
        self.title = title
        self.plot_x_lim = plot_x_lim
        self.plot_y_lim = plot_y_lim
        self.fig_format = fig_format
        self.fontsize = fontsize
        self.user_naming_rule = user_naming_rule
        self.times = times

    def transform_data(self):
        power, freqs = et_average_frequency_transformation(epochs=self.input_node.data,
                                                           fs=self.input_node.fs,
                                                           ave_mode='magnitude'
                                                           )
        self.output_node.data = power
