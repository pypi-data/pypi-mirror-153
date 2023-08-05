from peegy.processing.pipe.definitions import InputOutputProcess
from peegy.processing.tools.epochs_processing_tools import et_mean, et_frequency_mean2, et_snr_in_rois
from peegy.processing.tools.detection.definitions import TimeROI
from peegy.definitions.eeg_definitions import EegPeak
from peegy.definitions.channel_definitions import Domain
from peegy.definitions.events import SingleEvent, Events
from peegy.processing.statistics.definitions import FpmTest, StatisticalTests, TestType
from peegy.processing.statistics.eeg_statistic_tools import hotelling_t_square_test, f_test
from peegy.processing.tools.eeg_epoch_operators import w_mean, effective_sampling_size
import numpy as np
import pandas as pd
import os
import astropy.units as u
from tqdm import tqdm
from peegy.tools.units.unit_tools import set_default_unit
from PyQt5.QtCore import QLibraryInfo
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(QLibraryInfo.PluginsPath)


class EpochData(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 pre_stimulus_interval: u.quantity.Quantity = None,
                 post_stimulus_interval: u.quantity.Quantity = None,
                 event_code: float = None,
                 base_line_correction: bool = False,
                 demean: bool = True,
                 events_mask: int = None,
                 **kwargs):
        """
        This class will take a n*m matrix into a k*m*p, where p (number of trials) is determined by the number of
        triggers used to split the data
        :param input_process: InputOutputProcess Class
        :param pre_stimulus_interval: the length (in sec) of the data to be read before the trigger
        :param post_stimulus_interval: the length (in sec) of the data to be read after the trigger
        :param event_code: integer indicating the event code to be used to epoch the data
        :param base_line_correction: whether to perform beaseline correction or not, the timespan to calculate the mean
        for baseline correction from, can be defined by setting pre_stimulus_interval, e.g. 200 would perform
        the baseline correction from -200 to 0 seconds before trigger onset.
        :param demean: whether to remove the mean from each epoch
        :param events_mask: integer value used to masker triggers codes. This is useful to ignore triggers inputs avove
        a particular value. For example, if only the first 8 trigger inputs were used (max decimal value is 255), in a
        system with 16 trigger inputs, then the masker could be set to 255 to ignore any trigger from trigger inputs 9
        to 16.
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(EpochData, self).__init__(input_process=input_process, **kwargs)
        self.pre_stimulus_interval = set_default_unit(pre_stimulus_interval, u.s)
        self.post_stimulus_interval = set_default_unit(post_stimulus_interval, u.s)
        self.event_code = event_code
        self.base_line_correction = base_line_correction
        self.demean = demean
        self.events_mask = events_mask

    def transform_data(self):
        if self.event_code is None:
            print('no event code was provided')
            return
        data = self.input_node.data
        pre_stimulus_interval = 0.0 * u.s if self.pre_stimulus_interval is None else self.pre_stimulus_interval
        self.input_node.events.mask = self.events_mask
        events_index = self.input_node.events.get_events_index(code=self.event_code,
                                                               fs=self.input_node.fs)
        post_stimulus_interval = self.post_stimulus_interval
        if self.post_stimulus_interval is None:
            post_stimulus_interval = np.percentile(np.diff(events_index), 90) / self.input_node.fs
        buffer_size = np.int((post_stimulus_interval + pre_stimulus_interval) * self.input_node.fs)
        events_index = events_index - int((pre_stimulus_interval + self.input_node.x_offset) * self.input_node.fs)
        events_index = events_index[events_index >= 0]
        epochs = np.zeros((buffer_size, self.input_node.data.shape[1], events_index.size), dtype=np.float32)
        print('There are {:} events with code {:}'.format(events_index.shape[0], self.event_code))
        for i, _event in enumerate(tqdm(events_index, desc='Epoching data')):
            # ensure that blocks match buffer size
            if _event + buffer_size > self.input_node.data.shape[0]:
                epochs = epochs[:, :, list(range(i))]
                print("{:} events ignored as data length won't fit epoch length".format(
                    events_index.shape[0] - i))
                break
            epochs[:, :, i] = data[_event:_event + buffer_size, :]
        epochs = epochs * data.unit
        print('A total of {:} epochs were obtained using event code {:}, each with a duration of {:.3f}'.format(
            epochs.shape[2],
            self.event_code,
            (buffer_size / self.input_node.fs).to(u.s)))
        if self.demean:
            epochs = epochs - np.mean(epochs, axis=0)
        if self.base_line_correction:
            _ini_sample = 0
            _end_sample = max(1, int(pre_stimulus_interval * self.input_node.fs))
            epochs = epochs - np.mean(epochs[_ini_sample:_end_sample, :, :], axis=0)
        self.output_node.data = epochs
        self.output_node.x_offset = pre_stimulus_interval
        self.output_node.events = None


class RejectEpochs(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 std_threshold: float = 0.0,
                 rejection_percentage: float = 0.0,
                 rejection_threshold: u.quantity.Quantity = 100.0 * u.uV,
                 max_percentage_epochs_above_threshold: float = 1.0,
                 **kwargs):
        """
        This class will epochs where a given threshold have been exceeded. If any channel exceed the threshold at a
        given trial, that particular epoch will be removed from all channels. This is done to keep the data in a single
        matrix.
        :param input_process: InputOutputProcess Class
        :param std_threshold: float indicating the threshold in terms of standard deviations to remove epochs
        :param max_percentage_epochs_above_threshold: if a single channel has more than max_epochs_above_threshold
        (percentage) epochs, the channel will be removed.
        :param rejection_percentage indicates the percentage of epochs to remove.
        above the threshold, the channel will be removed.
        :param rejection_threshold: indicates level above which epochs will be rejected
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(RejectEpochs, self).__init__(input_process=input_process, **kwargs)
        self.std_threshold = set_default_unit(std_threshold, u.dimensionless_unscaled)
        self.rejection_threshold = set_default_unit(rejection_threshold, u.uV)
        self.max_percentage_epochs_above_threshold = max_percentage_epochs_above_threshold
        self.rejection_percentage = rejection_percentage

    def transform_data(self):
        _data = self.input_node.data
        _idx_to_keep = np.ones((_data.shape[2], ), dtype=bool)
        # first we check if a channel needs to be removed  based on max_percentage_epochs_above_threshold
        if self.max_percentage_epochs_above_threshold < 1.0:
            _max_amp = np.max(np.abs(_data), axis=0)
            _epoch_limit = int(self.max_percentage_epochs_above_threshold * _data.shape[2])
            _n_noisy_epochs_per_channel = np.sum(_max_amp > self.rejection_threshold, axis=1)
            _ch_to_remove = np.argwhere(_n_noisy_epochs_per_channel > _epoch_limit).flatten()
            print('Removing a total of {:} channels with more than {:} epochs above the threshold {:}'.format(
                np.sum(_ch_to_remove.size), _epoch_limit, self.rejection_threshold))
            # we assign data to output node to perform a clean delete of bad channels
            self.output_node.data = _data
            self.output_node.delete_channel_by_idx(_ch_to_remove)
            _data = self.output_node.data

        # now using the new data we find and remove the x % of ephocs with the highest peak
        if self.rejection_percentage > 0:
            _max_amp = np.max(np.abs(_data), axis=0)
            rejection_thr = np.quantile(np.max(_max_amp, axis=0), 1 - self.rejection_percentage)
            to_keep = np.max(_max_amp, axis=0, keepdims=True) < rejection_thr
            _idx_to_keep = np.logical_and(_idx_to_keep, np.all(to_keep, axis=0).flatten())

        if self.rejection_threshold > 0:
            # now we find epochs indexes across channels which are avove threshold
            _max_amp = np.max(np.abs(_data), axis=0)
            to_keep = _max_amp <= self.rejection_threshold
            _idx_to_keep = np.logical_and(_idx_to_keep, np.all(to_keep, axis=0).flatten())

        if self.std_threshold > 0:
            _epochs_std = np.std(_data, axis=0)
            _n_noisy_epochs_across_channels = np.sum(np.greater(_epochs_std,
                                                                (np.mean(_epochs_std, 1) +
                                                                 self.std_threshold * np.std(_epochs_std, 1)).reshape(
                                                                    -1, 1)),
                                                     axis=0,
                                                     keepdims=True)
            to_keep = _n_noisy_epochs_across_channels == 0
            _n_std_to_remove = np.sum(~to_keep)
            _std_percentage = 100 * _n_std_to_remove / _data.shape[2]
            _idx_to_keep = np.logical_and(_idx_to_keep, np.all(to_keep, axis=0).flatten())
            print('Rejecting a total of {:} epochs, corresponding to {:} % above {:} std'.format(
                np.sum(~_idx_to_keep), _std_percentage, self.std_threshold))
        # print some information and reject epochs
        _p_rejected = 100 * (1 - np.sum(_idx_to_keep) / _data.shape[2])
        print('Percentage of total epochs rejected {:}%'.format(_p_rejected))
        if _p_rejected == 100:
            raise Exception('All epochs were rejected!! check rejection level '
                            '(currently {:}) and run again'.format(self.rejection_percentage))

        self.output_node.data = _data[:, :, _idx_to_keep.flatten()]


class RemoveBadChannelsEpochsBased(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 threshold: float = 300.0,
                 max_epochs_above_threshold: float = 0.5,
                 **kwargs):
        """
        This class will remove a channel based on epochs data. If any channel has more than max_epochs_above_threshold
        percentage of epochs above a given threshold, this channel will be removed.
        :param input_process: InputOutputProcess Class
        :param threshold: the threshold to reject channels with too much noise
        :param max_epochs_above_threshold: if a single channel has more than max_epochs_above_threshold (percentage)
        epochs, the channel will be removed.
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(RemoveBadChannelsEpochsBased, self).__init__(input_process=input_process, **kwargs)
        self.threshold = threshold
        self.max_epoch_above_threshold = max_epochs_above_threshold

    def transform_data(self):
        _data = self.input_node.data
        _max_amp = np.max(np.abs(_data), axis=0)
        _epoch_limit = int(self.max_epoch_above_threshold * _data.shape[2])
        _n_noisy_epochs_per_channel = np.sum(_max_amp > self.threshold, axis=1)
        _ch_to_remove = np.argwhere(_n_noisy_epochs_per_channel > _epoch_limit).flatten()
        print('Removing a total of {:} channels with more than {:} epochs above the threshold {:}'.format(
            np.sum(_ch_to_remove.size), _epoch_limit, self.threshold))
        # we assign data to output node to perform a clean delete of bad channels
        self.output_node.data = _data
        self.output_node.delete_channel_by_idx(_ch_to_remove)


class SortEpochs(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 ascending=False,
                 sort_by: str = 'std',
                 **kwargs):
        """
        This class will sort epochs by maximum amplitude across all trials.
        :param input_process: InputOutputProcess Class
        :param sort_by: string indicating the method to sort ephocs, either 'std' for standard deviation or 'amp' to use
        maximum amplitude per epoch.
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(SortEpochs, self).__init__(input_process=input_process, **kwargs)
        self.ascending = ascending
        self.sort_by = sort_by

    def transform_data(self):
        _data = self.input_node.data
        if self.sort_by == 'amp':
            _measured_value = np.max(np.abs(_data), axis=0)
            _idx_sorted = np.argsort(_measured_value, axis=1)
        if self.sort_by == 'std':
            _measured_value = np.std(_data, axis=0)
            _idx_sorted = np.argsort(_measured_value, axis=1)
        sorted_data = np.zeros(_data.shape) * _data.unit
        if self.ascending:
            for _ch in range(_idx_sorted.shape[0]):
                sorted_data[:, _ch, :] = _data[:, _ch, _idx_sorted[_ch, :][::-1]]
        else:
            for _ch in range(_idx_sorted.shape[0]):
                sorted_data[:, _ch, :] = _data[:, _ch, _idx_sorted[_ch, :]]

        print('Sorting epochs by {:}'.format(self.sort_by))
        self.output_node.data = sorted_data


class AverageEpochs(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 weighted_average: bool = True,
                 n_tracked_points: int = None,
                 block_size: int = 5,
                 roi_windows: np.array([TimeROI]) = None,
                 **kwargs):
        """
        This InputOutputProcess average epochs
        :param input_process: InputOutputProcess Class
        :param weighted_average: if True, weighted average will be used
        :param n_tracked_points: number of equally spaced points over time used to estimate residual noise
        :param block_size: number of trials that will be stack together to estimate the residual noise
        :param roi_windows: time windows used to perform some measures (snr, rms)
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(AverageEpochs, self).__init__(input_process=input_process, **kwargs)
        self.weighted_average = weighted_average
        self.n_tracked_points = n_tracked_points
        self.block_size = block_size
        self.roi_windows = roi_windows

    def transform_data(self):
        block_size = max(self.block_size, 5)
        if self.n_tracked_points is None:
            self.n_tracked_points = self.input_node.data.shape[0]
        samples_distance = int(max(self.input_node.data.shape[0] // self.n_tracked_points, 1))
        w_ave, w, rn, cum_rn, w_fft, n, wb, nb = \
            et_mean(epochs=self.input_node.data,
                    block_size=block_size,
                    samples_distance=samples_distance,
                    weighted=self.weighted_average
                    )
        points_per_sweep = int(self.input_node.data.shape[0] / samples_distance)
        # compute noise degrees of freedom based on the effective degrees of freedoms
        dof = effective_sampling_size(w)[0, :]
        rn_dof = dof * points_per_sweep
        self.output_node.data = w_ave
        self.output_node.rn = rn
        self.output_node.cum_rn = cum_rn
        self.output_node.w = w
        self.output_node.n = n
        self.output_node.rn_df = rn_dof
        _stats = self.get_snr_table()
        self.output_node.statistical_tests = StatisticalTests({TestType.f_test_time: _stats})
        self.output_node.roi_windows = self.roi_windows

    def get_snr_table(self):
        roi_samples = self.get_roi_samples()
        final_snr, _ = et_snr_in_rois(data=self.output_node.data,
                                      roi_windows=roi_samples,
                                      rn=self.output_node.rn)
        tests = []
        for _iw in range(len(roi_samples)):
            _ini = roi_samples[_iw][0]
            _end = roi_samples[_iw][1]
            _label = None
            if self.roi_windows is not None:
                _label = self.roi_windows[_iw].label

            _data_chunk = self.output_node.data[_ini: _end, :]
            f_value, f_critic, df_num, df_den, p_value = f_test(samples=_data_chunk,
                                                                snr=final_snr[:, _iw],
                                                                df_noise=self.output_node.rn_df,
                                                                alpha=self.output_node.alpha
                                                                )
            for _idx_ch, _ch in enumerate(self.output_node.layout):
                df_den = self.output_node.rn_df
                tests.append(
                    FpmTest(df_1=df_num[_idx_ch],
                            df_2=df_den[_idx_ch],
                            f=f_value[_idx_ch],
                            f_critic=f_critic[_idx_ch],
                            p_value=p_value[_idx_ch],
                            rn=self.output_node.rn[_idx_ch],
                            snr=final_snr[_idx_ch, _iw],
                            time_ini=_ini / self.output_node.fs,
                            time_end=_end / self.output_node.fs,
                            n_epochs=self.output_node.n,
                            channel=_ch.label,
                            label=_label).__dict__
                )
        out = pd.DataFrame(tests)
        return out

    def get_roi_samples(self):
        if self.roi_windows is not None:
            roi_samples = [np.concatenate((self.input_node.x_to_samples([_roi.ini_time]),
                                           self.input_node.x_to_samples([_roi.end_time]))) for _roi in self.roi_windows]
        else:
            roi_samples = [np.array([0, self.output_node.data.shape[0]])]

        return roi_samples


class AverageEpochsFrequencyDomain(InputOutputProcess):
    def __init__(self,
                 input_process=InputOutputProcess,
                 n_tracked_points: int = 256,
                 block_size: int = 5,
                 test_frequencies: np.array = None,
                 n_fft: int = None,
                 weighted_average=True,
                 weight_frequencies: np.array = None,
                 delta_frequency: u.Quantity = 5. * u.Hz,
                 power_line_frequency: u.Quantity = 50 * u.Hz,
                 **kwargs):
        """
        This InputOutputProcess average epochs in the frequency domain
        :param input_process: InputOutputProcess Class
        :param n_tracked_points: number of equally spaced points over time used to estimate residual noise
        :param block_size: number of trials that will be stack together to estimate the residual noise
        :param test_frequencies: numpy array with frequencies that will be used to compute statistics (Hotelling test)
        :param weighted_average: bool indicating if weighted average is to be used, otherwise standard average is used
        :param weight_frequencies: numpy array with frequencies that will be used to estimate weights when
        weighted_average is activated
        :param delta_frequency: frequency size around each test_frequencies to estimate weights and noise
        :param power_line_frequency: frequency of local power line frequency. This will be used to prevent using
        this frequency or its multiples when performing frequency statistics
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(AverageEpochsFrequencyDomain, self).__init__(input_process=input_process, **kwargs)
        self.n_tracked_points = n_tracked_points
        self.block_size = block_size
        self.test_frequencies = set_default_unit(test_frequencies, u.Hz)
        self.weight_frequencies = set_default_unit(weight_frequencies, u.Hz)
        self.weighted_average = weighted_average
        self.delta_frequency = set_default_unit(delta_frequency, u.Hz)
        self.power_line_frequency = set_default_unit(power_line_frequency, u.Hz)

    def transform_data(self):
        # average processed data across epochs including frequency average
        if self.weight_frequencies is None:
            print('No specific frequency provided to estimate weights in the frequency-domain. Pooling across '
                  'test frequencies {:}. Results may be inaccurate if test frequencies contain no '
                  'relevant signal'.format(self.test_frequencies.to_string()))
            self.weight_frequencies = self.test_frequencies

        w_ave, snr, rn, by_freq_rn, by_freq_snr, w_fft, w, freq_samples, exact_frequencies = et_frequency_mean2(
            epochs=self.input_node.data,
            fs=self.input_node.fs,
            weighted_average=self.weighted_average,
            test_frequencies=self.weight_frequencies,
            delta_frequency=self.delta_frequency,
            block_size=self.block_size,
            power_line_frequency=self.power_line_frequency
        )

        hts = []
        for _idx, _f in enumerate(exact_frequencies):
            _freq_samples = freq_samples[_idx, :, :]
            h_samples = np.vstack((np.real(_freq_samples), np.imag(_freq_samples)))
            h_samples = h_samples.reshape((2, *freq_samples.shape[1::]))
            _spectral_amp = w_mean(epochs=_freq_samples.reshape((1, *freq_samples.shape[1::])),
                                   weights=w[0, :, :])
            _hts = hotelling_t_square_test(samples=h_samples, weights=w, channels=self.input_node.layout)
            for _idx_ch, _ht in enumerate(_hts):
                _ht.frequency_tested = _f.squeeze()
                _spectral_phase = np.angle(_spectral_amp[:, _idx_ch]).squeeze()
                _ht.mean_amplitude = np.abs(_spectral_amp[:, _idx_ch]).squeeze()
                _ht.mean_phase = _spectral_phase
            hts = hts + _hts
            # hotelling_t_square_test
        self.output_node.data = w_fft
        self.output_node.n_fft = self.input_node.data.shape[0]
        self.output_node.domain = Domain.frequency
        self.output_node.rn = rn
        self.output_node.snr = snr
        all_ht2 = [_h.__dict__ for _h in hts]
        _stats = pd.DataFrame(all_ht2)
        self.output_node.statistical_tests = StatisticalTests({TestType.hotelling_t2_freq: _stats})
        self.output_node.peak_frequency = self.get_frequency_peaks_as_pandas(pd.DataFrame(all_ht2))

    @staticmethod
    def get_frequency_peaks_as_pandas(hotelling_tests: pd.DataFrame = None):
        f_peaks = []
        for _i, _s_ht in hotelling_tests.iterrows():
            _f_peak = EegPeak(channel=_s_ht.channel,
                              x=_s_ht.frequency_tested,
                              rn=_s_ht.rn,
                              amp=_s_ht.mean_amplitude,
                              amp_snr=_s_ht.snr,
                              significant=bool(_s_ht.p_value < 0.05),
                              peak_label="{:10.1f}".format(_s_ht.frequency_tested),
                              show_label=True,
                              positive=True,
                              domain=Domain.frequency,
                              spectral_phase=_s_ht.mean_phase)
            f_peaks.append(_f_peak.__dict__)
        _data_pd = pd.DataFrame(f_peaks)
        return _data_pd


class DeEpoch(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess, de_mean=True, **kwargs):
        """
        This function will convert a n*m*p matrix into an (n*p) * m matrix
        :param input_process: InputOutputProcess Class
        :param de_mean: whether data should be demeaned before converting
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(DeEpoch, self).__init__(input_process=input_process, **kwargs)
        self.de_mean = de_mean

    def transform_data(self):
        _data = np.array(self.input_node.data.data)
        # if self.de_mean:
        #     _data -= np.mean(_data, axis=0)
        for _i in range(1, _data.shape[2]):
            _data[:, :, _i] = _data[:, :, _i] - (_data[0, :, _i] - _data[-1, :, _i - 1])

        self.output_node.data = np.reshape(np.transpose(_data, [0, 2, 1]), [-1, _data.shape[1]], order='F')
        events = []
        for _i in range(_data.shape[2]):
            events.append(SingleEvent(code=1,
                                      time_pos=_i * _data.shape[0] / self.input_node.fs,
                                      dur=0))
        events = Events(events=np.array(events))
        self.output_node.events = events
