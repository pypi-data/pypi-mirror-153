import numpy as np
import inspect
from peegy.definitions.channel_definitions import Domain
from peegy.definitions.eeg_definitions import EegPeak
from peegy.processing.tools.detection.definitions import PeakToPeakMeasure, PeakToPeakQuantity, TimePeakWindow, \
    PeaksContainer, PeakToPeakAmplitudeContainer
from peegy.processing.pipe.definitions import DataNode
import astropy.units as u


def get_peaks_2(time_vector=np.array([]), data_channels=np.array([]), rn=np.array([]), **kwargs):
    peak_windows = kwargs.get('peak_windows', np.array([]))
    channel_labels = kwargs.get('channel_labels', np.array([]))
    # classify all peaks
    peaks = detect_peaks(time_vector=time_vector,
                         data_channels=data_channels,
                         rn=rn,
                         peak_windows=peak_windows,
                         channel_labels=channel_labels)
    return peaks


def detect_peaks(peak_windows=np.array([TimePeakWindow]),
                 data_channels=np.array([]),
                 time_vector=np.array([]),
                 rn=np.array([]),
                 channel_labels=np.array([])):
    _detected_peaks = np.array([])
    if not channel_labels.size:
        channel_labels = np.arange(data_channels.size).astype(np.str)
    _peak_windows = sort_peak_windows(peak_windows)

    for i, _ch_label in zip(np.arange(data_channels.shape[1]), channel_labels):
        _peak_container = PeaksContainer(channel_label=_ch_label)
        for _t_w in _peak_windows:
            # apply time reference to current peal window (ini or end)
            if _t_w.target_channels is not None and _ch_label not in _t_w.target_channels:
                continue
            if _t_w.exclude_channels is not None and _ch_label in _t_w.exclude_channels:
                continue
            _t_w = update_time_window(peak_window=_t_w, peaks_container=_peak_container)
            _peak = find_time_peak(peak_time_window=_t_w,
                                   data=data_channels[:, i],
                                   rn=rn[i],
                                   time_vector=time_vector,
                                   channel_label=_ch_label
                                   )
            _peak_container.append(_peak)
        _detected_peaks = np.append(_detected_peaks, _peak_container)
    return _detected_peaks


def update_time_window(peak_window: TimePeakWindow, peaks_container: PeaksContainer = None):
    """
    This function search and apply reference time to passed windows. If a given ini_ref or end_ref was given to
    peak_window, we search the referential peak across all passed peaks within peaks_container.
    :param peak_window: TimePeakWindow class with searching parameters for a given peak
    :param peaks_container: PeaksContainer class with found peaks
    :return: updated version of peak_window (ini_time and/or end_time) to perform search
    """
    for _peak in peaks_container.get_peaks():
        if peak_window.ini_ref is not None and peak_window.ini_ref == _peak.peak_label:
            peak_window.ini_time = _peak.x
        if peak_window.end_ref is not None and peak_window.end_ref == _peak.peak_label:
            peak_window.end_time = _peak.x
    return peak_window


def label_peak(peak=EegPeak, time_window=TimePeakWindow):
    if peak is not None:
        peak.label_peak = time_window.label
        peak.show_label = time_window.show_label
        # make sure that there is not another peak having this label
        # for _p in all_peaks:
        #     if _p.label_peak == _detected_peak.label_peak and _detected_peak != _p:
        #         _p._detected_peak = None
        #         _p.show_label = False


def find_time_peak(peak_time_window: TimePeakWindow = None,
                   data=np.array([]),
                   time_vector=np.array([]),
                   rn: float = None,
                   channel_label=None,
                   ):
    _ini = np.searchsorted(time_vector, peak_time_window.ini_time)
    _end = np.searchsorted(time_vector, peak_time_window.end_time)
    _end = _end + 1 if _end == _ini else _end

    if peak_time_window.positive_peak:
        _idx = np.argmax(data[_ini:_end])
    else:
        _idx = np.argmin(data[_ini:_end])

    _idx += _ini
    _amp = data[_idx]
    _significant = np.abs(_amp) > 2.0 * rn
    snr = np.abs(_amp) / rn
    _val = {'x': time_vector[_idx],
            'rn': rn,
            'amp': _amp,
            'amp_snr': snr,
            'significant': _significant,
            'peak_label': peak_time_window.label,
            'show_label': peak_time_window.show_label,
            'show_peak': peak_time_window.show_peak,
            'positive': peak_time_window.positive_peak,
            'domain': Domain.time,
            'channel': channel_label}
    return EegPeak(**_val)


def measure_peak_to_peak_amplitudes(detected_peaks: np.array([PeaksContainer]) = None,
                                    peak_to_peak_amp_labels=np.array([PeakToPeakMeasure()])):
    if peak_to_peak_amp_labels is None:
        return
    amplitudes = np.array([])
    for peaks_container in detected_peaks:
        peak_to_peak_container = PeakToPeakAmplitudeContainer(channel_label=peaks_container.channel_label)
        for p_p_labels in peak_to_peak_amp_labels:
            ini_peak = [_peak for _peak in peaks_container.peaks if _peak.peak_label == p_p_labels.ini_peak]
            end_peak = [_peak for _peak in peaks_container.peaks if _peak.peak_label == p_p_labels.end_peak]
            _current_amp = {}
            if ini_peak and end_peak:
                amp = np.abs(ini_peak[0].amp - end_peak[0].amp)
                amp_sigma = (ini_peak[0].rn ** 2.0 + end_peak[0].rn ** 2.0) ** 0.5
                if ini_peak[0].amp >= end_peak[0].amp:
                    max_time = ini_peak[0].x
                else:
                    max_time = end_peak[0].x

                if ini_peak[0].amp < end_peak[0].amp:
                    min_time = ini_peak[0].x
                else:
                    min_time = end_peak[0].x
                _current_amp = {'max_time': max_time,
                                'min_time': min_time,
                                'ini_time': ini_peak[0].x,
                                'end_time': end_peak[0].x,
                                'rn': amp_sigma,
                                'amp': amp,
                                'amp_snr': np.inf * u.dimensionless_unscaled if amp_sigma == 0 else
                                amp / amp_sigma,
                                'amp_label': ini_peak[0].peak_label + '-' + end_peak[0].peak_label,
                                'channel': peaks_container.channel_label
                                }
                peak_to_peak_container.append(PeakToPeakQuantity(**_current_amp))
        amplitudes = np.append(amplitudes, peak_to_peak_container)
    return amplitudes


def sort_peak_windows(peak_windows=np.array([TimePeakWindow()])):
    for _i, _w in enumerate(peak_windows):
        _w_dependency_labels = [_w.ini_ref, _w.end_ref, _w.global_ref]
        for _dep in _w_dependency_labels:
            if _dep is not None:
                _idx = [_ip for _ip, _p in enumerate(peak_windows) if _p.label == _dep]
                if _idx:
                    # when find dependency, move it so dependency is first
                    if _idx[0] > _i:
                        peak_windows[_idx[0]], peak_windows[_i] = peak_windows[_i], peak_windows[_idx[0]]
                        # print [_p.label for _p in  peak_windows]
    return peak_windows


def join_to_channel_dict(dict_to_join=[{}], channels=[{}]):
    out = []
    for i, _ch in enumerate(channels):
        for _items in dict_to_join[i]:
            if inspect.isclass(type(_items)):
                _to_join = _items.__dict__
            else:
                _to_join = _items
            out.append(dict(_ch, **_to_join))
    return out


def join_arr_dict_to_arr_dict(arr_1=[{}], arr_2=[{}]):
    out = []
    for i, (_ch, _ndi) in enumerate(zip(arr_1, arr_2)):
        out.append(dict(_ch, **_ndi))
    return out


def detect_peaks_and_amplitudes(data_node=DataNode(),
                                time_peak_windows=np.array([TimePeakWindow()]),
                                eeg_peak_to_peak_measures=np.array([PeakToPeakMeasure()]),
                                ):
    peaks = None
    amplitudes = None
    if time_peak_windows is not None:
        # find peaks for all channels
        peaks = detect_peaks(time_vector=data_node.x,
                             data_channels=data_node.data,
                             channel_labels=np.array([_ch.label for _ch in data_node.layout]),
                             rn=data_node.rn,
                             peak_windows=time_peak_windows)
        if eeg_peak_to_peak_measures is not None:
            amplitudes = measure_peak_to_peak_amplitudes(detected_peaks=peaks,
                                                         peak_to_peak_amp_labels=eeg_peak_to_peak_measures)

    return peaks, amplitudes


def get_channel_peaks_and_windows(eeg_peaks=np.array([EegPeak]), eeg_time_windows=np.array([TimePeakWindow()]),
                                  channel_label=None):
    sub_peaks = np.array([])
    sub_windows = np.array([])
    if eeg_peaks is not None and len(eeg_peaks) > 0:
        sub_peaks = eeg_peaks.loc[eeg_peaks['channel'] == channel_label]
        for _w in eeg_time_windows:
            if _w.channel == channel_label:
                sub_windows = np.append(sub_windows, _w)
    return sub_peaks, sub_windows
