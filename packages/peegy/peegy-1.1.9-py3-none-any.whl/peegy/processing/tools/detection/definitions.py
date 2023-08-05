from peegy.definitions.channel_definitions import Domain
from peegy.tools.units.unit_tools import set_default_unit
import pandas as pd
import astropy.units as u


class EegPeak(object):
    def __init__(self,
                 channel: str = None,
                 x: float = None,
                 rn: float = None,
                 amp: float = None,
                 amp_snr: float = None,
                 significant: bool = False,
                 peak_label: str = None,
                 show_label: bool = True,
                 show_peak: bool = True,
                 positive: bool = True,
                 domain: Domain = Domain.time,
                 spectral_phase: float = None):
        self.channel = channel
        self.x = x
        self.rn = rn
        self.amp = amp
        self.amp_snr = amp_snr
        self.significant = significant
        self.peak_label = peak_label
        self.show_label = show_label
        self.show_peak = show_peak
        self.positive = positive
        self.domain = domain
        self.spectral_phase = spectral_phase


class TimePeakWindow(object):
    def __init__(self,
                 label: str = None,
                 ini_time: u.quantity.Quantity = None,
                 end_time: u.quantity.Quantity = None,
                 ini_ref: str = None,
                 end_ref: str = None,
                 require_ini_ref: bool = False,
                 require_end_ref: bool = False,
                 global_ref: str = None,
                 require_global_ref: bool = False,
                 ini_global_ref: str = None,
                 end_global_ref: str = None,
                 positive_peak: bool = False,
                 show_label: bool = True,
                 show_peak: bool = True,
                 force_search: bool = True,
                 channel: str = None,
                 target_channels: [str] = None,
                 exclude_channels: [str] = None):
        self._label = label
        self._ini_time = set_default_unit(ini_time, u.s)
        self._end_time = set_default_unit(end_time, u.s)
        self.ini_ref = ini_ref
        self.end_ref = end_ref
        self.require_ini_ref = require_ini_ref
        self.require_end_ref = require_end_ref
        self.global_ref = global_ref
        self.require_global_ref = require_global_ref
        self.ini_global_ref = ini_global_ref
        self.end_global_ref = end_global_ref
        self.positive_peak = positive_peak
        self.show_label = show_label
        self.show_peak = show_peak
        self.force_search = force_search
        self.channel = channel
        self.target_channels = target_channels
        self.exclude_channels = exclude_channels

    def get_ini_time(self):
        return self._ini_time

    def set_ini_time(self, value):
        self._ini_time = value

    ini_time = property(get_ini_time, set_ini_time)

    def get_end_time(self):
        _end_time = self._end_time
        if self._end_time is None:
            _end_time = self._ini_time
        return _end_time

    def set_end_time(self, value):
        self._end_time = value
    end_time = property(get_end_time, set_end_time)

    def set_label(self, value):
        self._label = value

    def get_label(self):
        _label = self._label
        if self._label is None:
            _label = '{:.2e}'.format(self.ini_time)
        return _label
    label = property(get_label, set_label)


class PeaksContainer:
    def __init__(self, channel_label: str = None):
        self.channel_label = channel_label
        self._peaks = []

    def get_peaks(self):
        return self._peaks

    def append(self, value: EegPeak = None):
        self._peaks.append(value)

    peaks = property(get_peaks)

    def to_pandas(self):
        _data_pd = pd.DataFrame([_peak.__dict__ for _peak in self._peaks])
        return _data_pd


class PeakToPeakMeasure(object):
    def __init__(self,
                 ini_peak: str = None,
                 end_peak: str = None):
        """
        Class container. This class defines the peaks labels that will be used to measure peak-to-peak amplitudes.
        :param ini_peak: the label of the initial peak
        :param end_peak: the label of the end peak
        """
        self.ini_peak = ini_peak
        self.end_peak = end_peak


class PeakToPeakQuantity(object):
    def __init__(self,
                 channel: str = None,
                 ini_time: u.Quantity = None,
                 end_time: u.Quantity = None,
                 max_time: u.Quantity = None,
                 min_time: u.Quantity = None,
                 amp: u.Quantity = None,
                 rn: u.Quantity = None,
                 amp_snr: u.Quantity = None,
                 amp_label: str = None
                 ):
        """
        Class container. This class defines the parameters that will be used to store peak-to-peak measurements.
        :param channel:
        :param ini_time: time of initial peak in a peak-to-peak measurement
        :param end_time: time of end peak in a peak-to-peak measurement
        :param max_time: time of the maximum peak
        :param min_time: time of the minimum peak
        :param amp: peak-to-peak amplitude
        :param rn: estimated residual noise in peak-to-peak measurement
        :param amp_snr: estimated peak-to-peak amplitude signal-to-noise ratio
        :param amp_label: label to identify this measurement
        """
        self.channel = channel
        self.ini_time = ini_time
        self.max_time = max_time
        self.min_time = min_time
        self.amp = amp
        self.rn = rn
        self.amp_snr = amp_snr
        self.amp_label = amp_label


class PeakToPeakAmplitudeContainer:
    def __init__(self,
                 channel_label: str = None):
        self.channel_label = channel_label
        self._peaks = []

    def get_peaks(self):
        return self._peaks

    def append(self, value: PeakToPeakQuantity = None):
        self._peaks.append(value)

    peaks = property(get_peaks)

    def to_pandas(self):
        _data_pd = pd.DataFrame([_peak.__dict__ for _peak in self._peaks])
        return _data_pd


class TimeROI(object):
    """
    Object used to define the timepoints in a region of interest (ROI), for time-window based analysis. The required
    parameters  are the beginning (initial) and ending timepoints in seconds. To distinguish different ROI windows,
    each objects can  be linked to a measure (string), a label (string), a condition (string), an (EEG) channel (str),
    or a value (float). This class will return a  numpy array. The TimeROI object is used by classes like AverageEpochs
    or HotellingT2Test.
    Example to define a ROI window for SNR estimation starting at 150 ms and ending at 350 ms:
    roi_windows = np.array([TimeROI(ini_time=150.0e-3, end_time=350.0e-3, measure="snr", label="itd_snr")])
    """
    def __init__(self,
                 ini_time: u.quantity.Quantity = None,
                 end_time: u.quantity.Quantity = None,
                 measure: str = None,
                 label: str = None,
                 condition: str = None,
                 value: u.quantity.Quantity = None,
                 show_window: bool = True,
                 show_label: bool = False,
                 ):
        """

        :param ini_time: initial time of the window (in seconds)
        :param end_time: end time of the window (in seconds)
        :param measure: str measure to be performed e.g. "snr", "rms" (this key value can be used to trigger a given
        action within a function requiring a ROI window
        :param label: str defining a desired label for this ROI
        :param condition: str defining a desired condition
        :param value: output value to store the output  of a given measure
        :param show_window: boolean use when plotting data. If true, time interval will be shown in plots
        :param show_label: boolean use when plotting data. If true, label will be shown in plots
        """
        self.ini_time = set_default_unit(ini_time, u.s)
        self.end_time = set_default_unit(end_time, u.s)
        self.measure = measure
        self.label = label
        self.condition = condition
        self.value = value
        self.show_window = show_window
        self.show_label = show_label


class Marker(object):
    def __init__(self,
                 x_ini: u.Quantity = 0,
                 x_end: u.Quantity = 0,
                 y_ini: u.Quantity = 0,
                 y_end: u.Quantity = 0,
                 label: str = None,
                 channel: str = None):
        self.x_ini = x_ini
        self.x_end = x_end
        self.y_ini = y_ini
        self.y_end = y_end
        self.channel = channel
        self.label = label
