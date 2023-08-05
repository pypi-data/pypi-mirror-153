from peegy.processing.pipe.definitions import InputOutputProcess
from peegy.processing.tools.epochs_processing_tools import et_mean
from sklearn.linear_model import LinearRegression
from peegy.processing.tools.detection.definitions import TimeROI, Marker
from peegy.definitions.eeg_definitions import EegPeak
from peegy.definitions.channel_definitions import Domain
from peegy.processing.statistics.definitions import PhaseLockingValueTest, HotellingTSquareFrequencyTest, \
    FrequencyFTest, StatisticalTests, TestType
from peegy.tools.units.unit_tools import set_default_unit
from peegy.processing.statistics.eeg_statistic_tools import hotelling_t_square_test, phase_locking_value
import pyfftw
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import multiprocessing
from scipy.stats import f
import os
import astropy.units as u
import gc
from PyQt5.QtCore import QLibraryInfo
from tqdm import tqdm
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(QLibraryInfo.PluginsPath)


class HotellingT2Test(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 block_time: u.quantity.Quantity = 0.040 * u.s,
                 detrend_data=False,
                 roi_windows: np.array(TimeROI) = None,
                 weight_data: bool = True,
                 block_size: int = 5,
                 **kwargs) -> InputOutputProcess:
        """
        This class computes the statistical significance of a region of interest in the  time-domain using a Hotelling
        T2 test.
        The time region where a response is expected is tested to assess whether the linear combination of data points
        within this region is significantly different of a random linear combination of points.

        :param input_process: InputOutputProcess Class
        :param block_time: the length (in secs) of each average window within a region of interest (roi). A ROI will be
        divided in several points of duration block_time. The average of each block_time will represent a sample passed
        for the statistical test
        :param detrend_data: whether to remove or not any linear component on each trial before performing the test
        :param roi_windows: a region of windows containing the response of interest
        :param weight_data: if True, estimations are based on weights from input node. If empty, weights are
        estimated from weighted average.
        :param block_size: number of epochs used to estimate weights when weight_data is True
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(HotellingT2Test, self).__init__(input_process=input_process, **kwargs)
        self.block_time = set_default_unit(block_time, u.s)
        self.detrend_data = detrend_data
        self.roi_windows = roi_windows
        self.weight_data = weight_data
        self.block_size = block_size

    def transform_data(self):
        block_size = int(self.block_time * self.input_node.fs)
        # by default we will use whatever weights are in the input_node
        weights = self.input_node.w
        # if no weights are passed, we compute them if required
        if self.weight_data and weights is None:
            # compute weighted average to extract weights
            _, weights, *_ = et_mean(epochs=self.input_node.data,
                                     block_size=self.block_size,
                                     samples_distance=int(max(self.input_node.data.shape[0] // 256, 10)),
                                     weighted=True)
        h_tests = []
        for _roi_idx, _roi in enumerate(self.roi_windows):
            _samples = np.concatenate((self.input_node.x_to_samples([_roi.ini_time]),
                                       self.input_node.x_to_samples([_roi.end_time])))
            data = self.input_node.data.copy()
            # remove linear trend
            _ini, _end = _samples
            if self.detrend_data:
                x = np.expand_dims(np.arange(0, data[_ini:_end].shape[0]), axis=1)
                for _idx in np.arange(data.shape[2]):
                    _ini_dt = np.maximum(0, _ini - int(self.fs * 0.1))
                    _end_dt = np.minimum(data.shape[0], _end + int(self.fs * 0.1))
                    _subset = data[_ini_dt:_end_dt, :, _idx].copy()
                    x_dt = np.expand_dims(np.arange(0, data[_ini_dt:_end_dt].shape[0]), axis=1)
                    regression = LinearRegression()
                    regression.fit(x_dt, _subset)
                    data[_ini:_end, :, _idx] -= regression.predict(x)
            # remove mean
            data[_ini:_end] = data[_ini:_end] - np.mean(data[_ini:_end], axis=0)
            block_size = max(0, min(block_size, _end - _ini))
            n_blocks = np.floor((_end - _ini) / block_size).astype(np.int)
            samples = np.array([np.mean(data[_ini + _i * block_size: _ini + (_i + 1) * block_size], axis=0)
                                for _i in range(n_blocks)]) * data.unit
            _roi_h_tests = hotelling_t_square_test(samples,
                                                   weights=weights,
                                                   channels=self.input_node.layout,
                                                   **_roi.__dict__)
            h_tests = h_tests + _roi_h_tests
            _stats = pd.DataFrame([_ht.__dict__ for _ht in h_tests])
        self.output_node.statistical_tests = StatisticalTests({TestType.hotelling_t2_time: _stats})


class FTest(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 delta_frequency: u.Quantity = 10. * u.Hz,
                 test_frequencies: np.array = None,
                 alpha: float = 0.05,
                 power_line_frequency: u.Quantity = 50 * u.Hz,
                 ignored_frequency_width: u.Quantity = 1 * u.Hz,
                 n_fft: int = None,
                 **kwargs) -> InputOutputProcess:
        """
        This class computes a FTest in the frequency domain of a signal.
        :param input_process: InputOutputProcess Class
        :param delta_frequency: the length in Hz around each target frequency to compute statistics
        :param test_frequencies: a numpy array with the frequencies that will be tested
        :param alpha: level to assess significance of the test
        :param power_line_frequency: frequency of local power line frequency. This will be used to prevent using
        this frequency or its multiples when performing the FTest
        :param ignored_frequency_width: width, in Hz, indicating the with around the target frequency that will be
        ignored when estimating the F-ratio. Neighbors frequencies within +- this value will not be considered for the
        F-test.
        :param n_fft: number of points to perform fft transformation
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(FTest, self).__init__(input_process=input_process, **kwargs)
        self.delta_frequency = set_default_unit(delta_frequency, u.Hz)
        self.ignored_frequency_width = set_default_unit(ignored_frequency_width, u.Hz)
        self.test_frequencies = set_default_unit(test_frequencies, u.Hz)
        self.fft_frequencies: np.array = None
        self.power_line_frequency = power_line_frequency
        self.alpha = alpha
        self.n_fft = n_fft

    def transform_data(self):
        if self.input_node.domain == Domain.time:
            if self.n_fft is None:
                self.n_fft = self.input_node.data.shape[0]
            fft = pyfftw.builders.rfft(self.input_node.data,
                                       overwrite_input=False,
                                       planner_effort='FFTW_ESTIMATE',
                                       axis=0,
                                       threads=multiprocessing.cpu_count(), n=self.n_fft)
            w_fft = fft() * self.input_node.data.unit
            w_fft /= self.input_node.data.shape[0] / 2
            self.fft_frequencies = np.arange(w_fft.shape[0]) * self.input_node.fs / self.n_fft
        else:
            self.n_fft = self.input_node.n_fft
            w_fft = self.input_node.data
            self.fft_frequencies = self.input_node.x

        results = [[]] * self.input_node.data.shape[1]
        all_makers = np.array([])
        for _freq in tqdm(self.test_frequencies, desc='F-Test'):
            _target_bin = self.freq_to_samples(_freq)
            # compute array of bins around target frequency
            _ini_bin = np.maximum(self.freq_to_samples(_freq - self.delta_frequency), 0)
            _end_bin = np.minimum(self.freq_to_samples(_freq + self.delta_frequency), w_fft.shape[0] - 1)
            _neighbours_idx_left = np.arange(_ini_bin, _target_bin)
            _neighbours_idx_right = np.arange(_target_bin + 1, _end_bin + 1)
            _neighbours_idx = np.concatenate((
                _neighbours_idx_left,
                _neighbours_idx_right))
            # compute array of bins around target frequency
            _ini_ignore = np.maximum(self.freq_to_samples(_freq - self.ignored_frequency_width), 0)
            _end_ignore = np.minimum(self.freq_to_samples(_freq + self.ignored_frequency_width), w_fft.shape[0] - 1)
            _neighbours_to_ignore_idx = np.concatenate((
                np.arange(_ini_ignore, _target_bin),
                np.arange(_target_bin + 1, _end_ignore + 1)))
            # compute power line frequencies
            _power_idx = np.array(
                [self.freq_to_samples(_power_freq) for _power_freq in
                 self.power_line_frequency * np.arange(1,
                                                       np.round(0.5 * self.input_node.fs / self.power_line_frequency))])
            # remove bins
            _neighbours_idx = np.setdiff1d(_neighbours_idx, _neighbours_to_ignore_idx)
            _neighbours_idx = np.setdiff1d(_neighbours_idx, _power_idx)

            _n = _neighbours_idx.size
            _f_critic = f.ppf(1 - self.alpha, 2, 2 * _n)
            _rns = np.sqrt(np.sum(np.abs(w_fft[_neighbours_idx, :]) ** 2, axis=0) / _n)
            _f_tests = np.abs(w_fft[_target_bin, :]) ** 2 / _rns ** 2.0

            for _ch, _f in enumerate(_f_tests):
                _d1 = 2
                _d2 = 2 * _n
                _p_values = 1 - f.cdf(_f, _d1, _d2)
                _snr = np.maximum(_f - 1, 0.0)
                _test_out = FrequencyFTest(frequency_tested=_freq,
                                           df_1=_d1,
                                           df_2=_d2,
                                           f=_f,
                                           p_value=_p_values,
                                           spectral_magnitude=np.abs(w_fft[_target_bin, _ch]),
                                           spectral_phase=np.angle(w_fft[_target_bin, _ch]),
                                           rn=_rns[_ch],
                                           snr=_snr,
                                           snr_db=10 * np.log10(_snr) if _snr > 0.0 else
                                           -np.Inf * u.dimensionless_unscaled,
                                           f_critic=_f_critic)
                results[_ch] = np.append(results[_ch], [_test_out])
            all_markers_l = [Marker(x_ini=self.fft_frequencies[np.min(_neighbours_idx_left)],
                                    x_end=self.fft_frequencies[np.max(_neighbours_idx_left)],
                                    channel=_ch.label) for _ch in self.input_node.layout]
            all_markers_r = [Marker(x_ini=self.fft_frequencies[np.min(_neighbours_idx_right)],
                                    x_end=self.fft_frequencies[np.max(_neighbours_idx_right)],
                                    channel=_ch.label) for _ch in self.input_node.layout]
            all_makers = np.concatenate((all_makers, all_markers_l, all_markers_r))

        # self.output_node.ht_tests = self.get_ht_tests_as_pandas(h_tests)
        self.output_node.data = w_fft
        self.output_node.n_fft = self.n_fft
        self.output_node.domain = Domain.frequency
        _stats = self.get_f_tests_as_pandas(results)
        self.output_node.statistical_tests = StatisticalTests({TestType.f_test_freq: _stats})
        self.output_node.peak_frequency = self.get_frequency_peaks_as_pandas(f_tests=results)

        self.output_node.markers = pd.DataFrame([_m.__dict__ for _m in all_makers])

    def get_frequency_peaks_as_pandas(self, f_tests: [np.array(FrequencyFTest)] = None):
        f_peaks = []
        for _i, (_f_ch, _ch) in enumerate(zip(f_tests, self.input_node.layout)):
            for _s_ft in _f_ch:
                _s_ft.label = _ch.label
                _f_peak = EegPeak(channel=_ch.label,
                                  x=_s_ft.frequency_tested,
                                  rn=_s_ft.rn,
                                  amp=_s_ft.spectral_magnitude,
                                  amp_snr=_s_ft.snr,
                                  significant=bool(_s_ft.p_value < 0.05),
                                  peak_label="{:10.1f}".format(_s_ft.frequency_tested),
                                  show_label=True,
                                  positive=True,
                                  domain=Domain.frequency,
                                  spectral_phase=_s_ft.spectral_phase)
                f_peaks.append(_f_peak.__dict__)
        _data_pd = pd.DataFrame(f_peaks)
        return _data_pd

    def freq_to_samples(self, value: np.array) -> np.array:
        if isinstance(value, float) or value.size == 1:
            value = [value]
        out = np.array([])
        for _v in value:
            out = np.append(out, np.argmin(np.abs(self.fft_frequencies - _v))).astype(np.int)
        return np.squeeze(out)

    def get_f_tests_as_pandas(self, f_tests: [np.array(HotellingTSquareFrequencyTest)] = None):
        f_peaks = []
        for _i, (_ht_ch, _ch) in enumerate(zip(f_tests, self.input_node.layout)):
            for _s_ht in _ht_ch:
                _s_ht.channel = _ch.label
                f_peaks.append(_s_ht.__dict__)
        _data_pd = pd.DataFrame(f_peaks)
        return _data_pd


class PhaseLockingValue(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 n_tracked_points: int = 256,
                 block_size: int = 5,
                 test_frequencies: np.array = None,
                 n_fft: int = None,
                 alpha=0.05,
                 weight_data: bool = True,
                 **kwargs):
        """
        This InputOutputProcess compute phase-locking value in the frequency domain
        :param input_process: InputOutputProcess Class
        :param n_tracked_points: number of equally spaced points over time used to estimate residual noise
        :param block_size: number of trials that will be stack together to estimate the residual noise
        :param test_frequencies: numpy array with frequencies that will be used to compute statistics (Hotelling test)
        :param n_fft: number of fft points
        :para, weight_data: If true, weights will be applied. If there are not weights, these will be calculated from
        weighted average.
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(PhaseLockingValue, self).__init__(input_process=input_process, **kwargs)
        self.n_tracked_points = n_tracked_points
        self.block_size = block_size
        self.test_frequencies = set_default_unit(np.unique(test_frequencies), u.Hz)
        self.n_fft = n_fft
        self.weight_data = weight_data
        self.alpha = alpha

    def transform_data(self):
        # average processed data across epochs including frequency average
        if self.n_fft is None:
            self.n_fft = self.input_node.data.shape[0]
        # we will use whatever weights are present in input_process
        weights = self.input_node.w

        # we compute weights if required
        if self.weight_data and weights is None:
            # run weighted average to provide weights
            _, weights, *_ = \
                et_mean(epochs=self.input_node.data,
                        block_size=max(self.block_size, 5),
                        samples_distance=int(max(self.input_node.data.shape[0] // self.n_tracked_points, 10)),
                        weighted=True
                        )

        amp, plv, z, z_critic, p_values, angles, dof, rn = phase_locking_value(
            self.input_node.data,
            weights=weights,
            alpha=self.alpha,
            eps=np.finfo(float).eps * self.input_node.data.unit ** 2.0)
        self.output_node.data = plv
        self.output_node.n_fft = self.n_fft
        self.output_node.domain = Domain.frequency
        _stats = self.get_plv_tests_as_pandas(
            plv=plv,
            angles=angles,
            z=z,
            z_critic=z_critic,
            p_values=p_values,
            dof=dof,
            rn=rn)
        self.output_node.statistical_tests = StatisticalTests({TestType.rayleigh_test: _stats})
        self.output_node.peak_frequency = self.get_plv_peaks_as_pandas(plv=plv,
                                                                       p_values=p_values,
                                                                       angles=angles)

    def get_plv_peaks_as_pandas(self, plv: np.array = None,
                                p_values: np.array = None,
                                angles: np.array = None):
        f_peaks = []
        freq_position = self.output_node.x_to_samples(self.test_frequencies)
        for _i, _ch in enumerate(self.input_node.layout):
            for _fpos, _f in zip(freq_position, self.test_frequencies):
                _f_peak = EegPeak(channel=_ch.label,
                                  x=_f,
                                  amp=plv[_fpos, _i],
                                  significant=bool(p_values[_fpos, _i] < self.alpha),
                                  peak_label="{:10.1f}".format(_f),
                                  show_label=True,
                                  positive=True,
                                  domain=Domain.frequency,
                                  spectral_phase=angles[_fpos, _i])
                f_peaks.append(_f_peak.__dict__)
        _data_pd = pd.DataFrame(f_peaks)
        return _data_pd

    def get_plv_tests_as_pandas(self, plv: np.array,
                                angles: np.array = None,
                                z: float = None,
                                z_critic: float = None,
                                p_values: np.array = None,
                                dof: float = None,
                                rn: float = None):
        r_tests = []
        freq_position = self.output_node.x_to_samples(self.test_frequencies)
        for _i, _ch in enumerate(self.input_node.layout):
            for _fpos, _f in zip(freq_position, self.test_frequencies):
                _test = PhaseLockingValueTest(p_value=p_values[_fpos, _i],
                                              mean_phase=angles[_fpos, _i],
                                              plv=plv[_fpos, _i],
                                              z_critic=z_critic[0, _i],
                                              z_value=z[_fpos, _i],
                                              df_1=dof[0, _i],
                                              channel=_ch.label,
                                              frequency_tested=_f,
                                              rn=rn[_fpos, _i])
                r_tests.append(_test.__dict__)
        _data_pd = pd.DataFrame(r_tests)
        return _data_pd


class Covariance(InputOutputProcess):
    def __init__(self, input_process: InputOutputProcess = None,
                 normalized=True,
                 return_figures: bool = False,
                 ini_time: u.Quantity = 0 * u.s,
                 end_time: u.Quantity = np.Inf * u.s,
                 fig_format: str = '.png',
                 fontsize: float = 12,
                 user_naming_rule: str = '',
                 save_to_file: bool = True,
                 **kwargs):
        """
        This class will apply compute the covariance matrix
        :param input_process: an SpatialFilter InputOutputProcess Class
        :param normalized: if true, covariance will be normalized (i.e. correlation)
        :param return_figures: If true, handle to figure will be passed to self.figures
        :param ini_time: float indicating the starting time to compute covariance
        :param end_time: float indicating the ending time to compute covariance
        :param fig_format: string indicating the format of the output figure (e.g. '.png' or '.pdf')
        :param fontsize: size of fonts in plot
        :param idx_channels_to_plot: np.array indicating the index of the channels to plot
        :param user_naming_rule: string indicating a user naming to be included in the figure file name
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(Covariance, self).__init__(input_process=input_process, **kwargs)
        self.normalized = normalized
        self.ini_time = set_default_unit(ini_time, u.s)
        self.end_time = set_default_unit(end_time, u.s)
        self.fig_format = fig_format
        self.fontsize = fontsize
        self.user_naming_rule = user_naming_rule
        self.return_figures = return_figures
        self.save_to_file = save_to_file
        self.figures = None

    def transform_data(self):
        data = self.input_node.data.value
        _ini_time = np.minimum(np.maximum(0,
                               self.input_node.x_to_samples(np.array([self.ini_time.to(u.s).value]) * u.s).squeeze()),
                               data.shape[0]).astype(int)
        _end_time = np.maximum(0,
                               np.minimum(
                                   data.shape[0],
                                   self.input_node.x_to_samples(np.array([self.end_time.to(u.s).value]) * u.s).squeeze()
                               )).astype(int)
        data = self.input_node.data.value[_ini_time: _end_time, :]
        if self.normalized:
            cov = np.corrcoef(data.T)
            v_min = -1 * u.dimensionless_unscaled
            v_max = 1 * u.dimensionless_unscaled
        else:
            cov = np.cov(data.T.value)
            v_min = np.min(cov)
            v_max = np.max(cov)

        self.output_node.data = cov
        # generate table
        table = pd.DataFrame()
        channels = [_ch.label for _ch in self.input_node.layout]
        for _i in range(cov.shape[0]):
            ch_i = channels[_i]
            for _j in range(cov.shape[1]):
                ch_j = channels[_j]
                table = pd.concat([table, pd.DataFrame([{'channel_x': ch_i,
                                                         'channel_y': ch_j,
                                                         'covariance': cov[_i, _j],
                                                         'normalized:': self.normalized}])],
                                  ignore_index=True)
        _stats = table
        self.output_node.statistical_tests = StatisticalTests({TestType.covariance: _stats})
        fig = plt.figure()
        ax = fig.add_subplot()
        maxis = ax.matshow(cov, vmin=v_min.value, vmax=v_max.value)
        ax.set_xticks(np.arange(0, len(channels)))
        ax.set_yticks(np.arange(0, len(channels)))
        ax.set_xticklabels(channels)
        ax.set_yticklabels(channels)
        plt.colorbar(maxis)
        mask = np.ones(cov.shape, dtype=bool)
        np.fill_diagonal(mask, 0)
        max_value = cov[mask].max()
        min_value = cov[mask].min()
        print('Maximum / Minimum covariance: {:} / {:}'.format(max_value, min_value))
        if self.save_to_file:
            figure_dir_path = self.input_node.paths.figures_current_dir
            _sep = '_' if self.user_naming_rule is not None else ''
            figure_basename = self.input_process.name + _sep + self.user_naming_rule
            fig.savefig(figure_dir_path + figure_basename + 'covariance' + self.fig_format)
        if self.return_figures:
            self.figures = fig
        else:
            plt.close(fig)
            gc.collect()
