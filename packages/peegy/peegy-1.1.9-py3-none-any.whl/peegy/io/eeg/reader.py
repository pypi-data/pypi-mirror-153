import peegy.io.edf_bdf_reader as ebr
import peegy.io.generic_csv_reader as cvsr
import os
import abc
import numpy as np
import astropy.units as u


class EEGData(object, metaclass=abc.ABCMeta):
    def __init__(self, file_name=''):
        self.file_name = file_name
        self.fs = None
        self.n_channels = None
        self.default_layout = None
        self.event_channel_label = None

    def get_data(self, channels: np.array = np.array([]), ini_time=0, end_time: float = None):
        print('need to define')

    def get_events(self):
        print('need to define')


class _BDFEDFDataReader(EEGData):
    def __init__(self, file_name='',
                 event_channel_label: ebr.DeviceEventChannel = ebr.DeviceEventChannel.auto):
        """
        This class handles reading of edf and bdf files.
        :param file_name: path to file to be read
        :param event_channel_label: string indicating the label of the channel containing all events.
        This is usually the 'Status' channel for bdf files and 'EDF Annotations' for EDF files, however, some
        devices provide other labels, e.g. 'BDF Annotations', therefore we leve this open
        """
        super(_BDFEDFDataReader, self).__init__(file_name=file_name)
        self._header = ebr.read_edf_bdf_header(self.file_name)
        self.n_channels = self._header['n_channels']
        self.fs = self._header['fs'][0]
        self.default_layout = None
        _, file_extension = os.path.splitext(file_name)
        if file_extension == '.bdf':
            if event_channel_label == ebr.DeviceEventChannel.auto or event_channel_label is None:
                for ch in self._header['channels']:
                    if ch.label == ebr.DeviceEventChannel.bdf_event_channel:
                        self.event_channel_label = ebr.DeviceEventChannel.bdf_event_channel
                        break
                    if ch.label == ebr.DeviceEventChannel.bdf_event_annotations:
                        self.event_channel_label = ebr.DeviceEventChannel.bdf_event_annotations
        if file_extension == '.edf':
            self.event_channel_label = ebr.DeviceEventChannel.edf_event_channel
        # we override the default event_channel_label if another is provided by user
        if event_channel_label is not None and event_channel_label != ebr.DeviceEventChannel.auto:
            self.event_channel_label = event_channel_label

    def get_data(self, channels_idx: np.array = np.array([]),
                 ini_time: u.quantity.Quantity = 0 * u.s,
                 end_time: u.quantity.Quantity = None):
        data, events, units, annotations = ebr.get_data(header=self._header,
                                                        channels_idx=channels_idx,
                                                        ini_time=ini_time,
                                                        end_time=end_time,
                                                        event_channel_label=self.event_channel_label)
        if channels_idx.size:
            self.default_layout = self._header['channels'][channels_idx]
        else:
            self.default_layout = self._header['channels']

        # here the event channel is removed from the layout
        _status_idx = [_i for _i, _ch in enumerate(self.default_layout) if
                       self.default_layout[_i].label == self.event_channel_label]
        if _status_idx:
            self.default_layout = np.delete(self.default_layout, _status_idx)
        return data, events, units, annotations

    def get_events(self):
        _events, _ = ebr.get_event_channel(header=self._header,
                                           event_channel_label=self.event_channel_label)
        return _events


class _CSVDataReader(EEGData):
    def __init__(self, file_name='',
                 fs_col_name: str = None,
                 gain_col_name: str = None,
                 fs_unit: u.quantity.Quantity = u.Hz,
                 gain_unit: u.quantity.Quantity = u.uV,
                 gain_inverted: bool = False
                 ):
        super(_CSVDataReader, self).__init__(file_name=file_name)
        self._header = cvsr.read_header(self.file_name,
                                        fs_col_name=fs_col_name,
                                        gain_col_name=gain_col_name,
                                        fs_unit=fs_unit,
                                        gain_unit=gain_unit,
                                        gain_inverted=gain_inverted
                                        )
        self.n_channels = self._header['n_channels']
        self.fs = self._header['fs']
        self.default_layout = None
        _, file_extension = os.path.splitext(file_name)
        if file_extension == '.txt':
            self.event_channel_label = "Events"

    def get_data(self, channels_idx: np.array = np.array([]), ini_time=0, end_time: float = None) -> (np.array,
                                                                                                      np.array,
                                                                                                      u,
                                                                                                      tuple):
        annotations = ()
        data, events, units = cvsr.read_channel(
            header=self._header,
            channels_idx=channels_idx,
            ini_time=ini_time,
            end_time=end_time)
        if channels_idx.size:
            self.default_layout = self._header['channels'][channels_idx]
        else:
            self.default_layout = self._header['channels']

        # here the status channel is removed from the layout
        _status_idx = [_i for _i, _ch in enumerate(self.default_layout) if
                       self.default_layout[_i].label == self.event_channel_label]
        if _status_idx:
            self.default_layout = np.delete(self.default_layout, _status_idx)
        return data, events, units, annotations

    def get_events(self):
        _, events, _ = cvsr.read_channel(
            header=self._header)
        return events


def eeg_reader(file_name='',
               fs_col_name: str = None,
               gain_col_name: str = None,
               fs_unit: u.quantity.Quantity = u.Hz,
               gain_unit: u.quantity.Quantity = u.uV,
               gain_inverted: bool = False,
               event_channel_label: str = None
               ):
    _, file_extension = os.path.splitext(file_name)
    if file_extension in ['.bdf', '.edf']:
        return _BDFEDFDataReader(file_name=file_name,
                                 event_channel_label=event_channel_label)
    if file_extension in ['.txt', '.cvs']:
        return _CSVDataReader(file_name=file_name,
                              fs_col_name=fs_col_name,
                              gain_col_name=gain_col_name,
                              fs_unit=fs_unit,
                              gain_unit=gain_unit,
                              gain_inverted=gain_inverted)
