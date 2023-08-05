import numpy as np
import peegy.processing.tools.filters.eegFiltering as ept
import pyfftw
import multiprocessing
import copy
from peegy.definitions.channel_definitions import ElectrodeType
from peegy.processing.statistics.definitions import HotellingTSquareFrequencyTest
from peegy.processing.tools.detection.definitions import TimePeakWindow, EegPeak, PeakToPeakMeasure, TimeROI
__author__ = 'jundurraga'


class EegChannel(object):
    def __init__(self, **kwargs):
        self.number = kwargs.get('number', None)
        self.label = kwargs.get('label', str(self.number))
        self.x = kwargs.get('x', None)
        self.y = kwargs.get('y', None)
        self.h = kwargs.get('h', None)
        self.type = kwargs.get('type', ElectrodeType.scalp)
        self.valid = kwargs.get('valid', True)
        # if fixed_polarity is true the polarity of this channel will not be reversed when required
        # by class EegAverageEpochs
        self.fixed_polarity = kwargs.get('fixed_polarity', False)


class EegAverageEpochs(object):
    def __init__(self, **kwargs):
        self.invert_polarity = kwargs.get('invert_polarity', False)
        self.channels = kwargs.get('channels', None)
        self.rn = kwargs.get('rn', None)
        self.cum_rn = kwargs.get('cum_rn', None)
        self.snr = kwargs.get('snr', None)
        self.cum_snr = kwargs.get('cum_snr', None)
        self.n_samples_block = kwargs.get('n_samples_block', None)
        self.signal_variance = kwargs.get('signal_variance', None)
        self.amplitude_units = kwargs.get('amplitude_units', None)
        self.time_units = kwargs.get('time_units', None)
        self.frequency_bins = kwargs.get('frequency_bins', None)
        self.frequency_test = kwargs.get('frequency_test', [HotellingTSquareFrequencyTest])
        self.data_processing = kwargs.get('data_processing', {})
        self.peak_times = kwargs.get('time_peaks', [EegPeak()])
        self.peak_frequency = kwargs.get('peak_frequency', [EegPeak()])
        self.peak_amplitudes = kwargs.get('peak_amplitudes', [PeakToPeakMeasure()])
        self.peak_time_windows = kwargs.get('peak_time_windows', [TimePeakWindow()])
        self.resampling_factor = 1.0
        self.descriptor = kwargs.get('descriptor', '')
        self.roi_windows = kwargs.get('roi_windows', np.array([TimeROI()]))
        self._average = kwargs.get('average', np.array([]))
        self._fs = kwargs.get('fs', None)
        self._rfft_average = kwargs.get('rfft_average', np.array([]))

    def set_average(self, value=np.array([])):
        self._average = value

    def get_average(self):
        if self.channels is None:
            return np.array([])
        else:
            return self._average * (-1.0) ** (
                self.invert_polarity & ~np.array([_ch.fixed_polarity for _ch in self.channels])).astype(np.int)

    average = property(get_average, set_average)

    def set_rfft_average(self):
        fft = pyfftw.builders.rfft(self._average, overwrite_input=False, planner_effort='FFTW_ESTIMATE', axis=0,
                                   threads=multiprocessing.cpu_count())
        _fft = np.abs(fft())
        # scale data
        _fft /= _fft.shape[0]
        self._rfft_average = _fft

    def get_rfft_average(self):
        return self._rfft_average

    rfft_average = property(get_rfft_average)

    def get_fs(self):
        return self._fs

    def set_fs(self, new_value):
        self._fs = new_value

    fs = property(get_fs, set_fs)

    def get_time(self):
        return np.arange(self._average.shape[0]) / self._fs

    time = property(get_time)

    def get_frequency(self):
        return np.arange(self._rfft_average.shape[0]) * self._fs / self._average.shape[0]

    frequency = property(get_frequency)

    def time_to_samples(self, in_time):
        return np.rint(in_time * self._fs).astype(np.int64)

    def frequency_to_samples(self, in_freq):
        return np.rint(in_freq / (self._fs / 2.0) * self.frequency.size).astype(np.int64)

    def append_eeg_ave_channel(self, new_channel_data=np.array([]),
                               rn=None,
                               snr=None,
                               signal_variance=None,
                               label=None,
                               electrode_type=ElectrodeType.artificial,
                               **kwargs):
        self._average = np.hstack((self._average, new_channel_data))
        self.rn = np.append(self.rn, rn)
        for _i, _ in enumerate(self.snr):
            self.snr[_i] = np.append(self.snr[_i], snr[_i])
        for _i, _ in enumerate(self.signal_variance):
            self.signal_variance[_i] = np.append(self.signal_variance[_i], signal_variance[_i])
        new_channel = EegChannel(label=label, number=len(self.channels) + 1, type=type, **kwargs)
        self.channels = np.append(self.channels, new_channel)

    def resampling(self, new_fs=None):
        self._average, _factor = ept.eeg_resampling(x=self._average, factor=new_fs / self._fs)
        self.resampling_factor = _factor
        self._fs *= _factor
        self.set_rfft_average()
        # scale frequency tested to new sampling rate
        # if self.frequency_test is not None:
        #     for _h_t in self.frequency_test:
        #         _h_t.frequency_tested = self.frequency[_h_t.frequency_bin]

    def is_scalp_channel(self):
        return np.array([_ch.type == ElectrodeType.scalp for _ch in self.channels])

    def get_roi_measures(self, roi_windows=np.array([TimeROI()])):
        out = []
        for _roi in roi_windows:
            _samples = self.time_to_samples(_roi.interval)
            for _i, _channel in enumerate(self.channels):
                _roi.channel = _channel.label
                _data = self._average[_samples[0]: _samples[1], _i]

                if _roi.measure == 'snr':
                    s_var = np.var(_data)
                    if self.rn[_i] == 0:
                        snr = np.inf
                    else:
                        snr = s_var / self.rn[_i] ** 2.0 - 1.0
                    _roi.value = snr
                if _roi.measure == 'rms':
                    _roi.value = np.sqrt(np.mean(np.square(_data)))
                out.append(copy.copy(_roi))
        return out

    def get_unique_interval_rois(self, type='snr'):
        out = []
        if self.roi_windows.size:
            intervals = np.array([_roi.interval for _roi in self.roi_windows if _roi.label == type])
            b = np.ascontiguousarray(intervals).view(np.dtype((np.void, intervals.dtype.itemsize * intervals.shape[1])))
            _, idx = np.unique(b, return_index=True)
            out = self.roi_windows[idx]
        return out

    def get_rois_by_type(self, type='snr'):
        out = []
        if self.roi_windows is not None:
            out = np.array([_roi for _roi in self.roi_windows if _roi.measure == type])
        return out

    def roi_windows_in_samples(self):
        roi_samples = []
        for _i, _roi in enumerate(self.get_unique_interval_rois()):
            roi_samples.append(self.time_to_samples(_roi.interval))
        return roi_samples

    def get_roi_snr_and_rn(self):
        _roi_windows = self.get_rois_by_type(type='snr')
        _cum_snr = self.cum_snr
        _cum_rn = self.cum_rn
        _n_trials = np.cumsum(self.n_samples_block)
        _ch_idx = self.is_scalp_channel()
        _channels = self.channels[_ch_idx]
        out = []
        for _n, _roi_snrs in zip(_n_trials, _cum_snr):
            for _roi, _all_ch_snrs in zip(_roi_windows, _roi_snrs):
                for _ch, _snr in zip(_channels, _all_ch_snrs):
                    _roi = TimeROI(**{'interval': _roi.interval,
                                      'measure': 'snr',
                                      'condition': _n,
                                      'label': _roi.label,
                                      'channel': _ch.label,
                                      'value': _snr})
                    out.append(_roi)

        for channels_rn, _n in zip(_cum_rn, _n_trials):
            for _ch, _rn in zip(_channels, channels_rn):
                _roi = TimeROI(**{'interval': [],
                                  'measure': 'rn',
                                  'condition': _n,
                                  'label': 'rn',
                                  'channel': _ch.label,
                                  'value': _rn})
                out.append(_roi)
        return out

    def get_max_snr_per_channel(self):
        max_snr = np.nanmax(np.atleast_2d(self.snr), axis=0)
        return np.atleast_1d(np.squeeze(max_snr))

    def get_max_s_var_per_channel(self):
        max_var = np.nanmax(self.signal_variance, axis=0)
        return np.atleast_1d(np.squeeze(max_var))


def signal_information(**kwargs):
    # ensure there are this mandatory fields
    out = {'type': kwargs.pop('type', None),
           'condition': kwargs.pop('condition', None)}
    for _item, _val in kwargs.items():
        out[_item] = _val
    return out
