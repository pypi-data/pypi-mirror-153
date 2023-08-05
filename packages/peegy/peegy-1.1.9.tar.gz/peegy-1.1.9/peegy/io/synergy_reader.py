import configparser
import re
import numpy as np
import peegy.definitions.eegReaderAbstractClasses as eegAbstract
__author__ = 'jundurraga'


class SynergyReader(eegAbstract.EEGData):
    def __init__(self, file_name=''):
        self.__file_name = file_name
        self.__data = np.array([])
        self.__channel_labels = []
        self.__channel_units = []
        self.__fs = []
        self.__gain = 1.0
        self.__time = np.array([])
        self.__channel_recording_parameters = []
        # initial parsing
        self.__parser = IniParser()
        self.__parser.read(file_name)
        self._file_data = self.__parser.as_dict()
        self.__parse_store_data()
        self.__time_offset = 0.0
        self.subject = dict(self._file_data['1 - Patient Details'], **self._file_data['1.1 - Visit'])

    def get_data(self):
        return self.__data / self.__gain

    def set_data(self, value):
        self.__data = value

    data = property(get_data, set_data)

    def get_gain(self):
        return self.__gain

    def set_gain(self, value):
        self.__gain = value

    gain = property(get_gain, set_gain)

    def set_channel_labels(self, value):
        self.__channel_labels = value

    def get_channel_labels(self):
        return self.__channel_labels

    channelLabels = property(get_channel_labels)

    def set_channel_units(self, value):
        self.__channel_units = value

    def get_channel_units(self):
        return self.__channel_units

    channel_units = property(get_channel_units, set_channel_units)

    def get_time(self):
        return np.arange(0, self.__data.shape[0]) / self.fs - self.__time_offset

    time = property(get_time)

    def set_time_offset(self, value):
        self.__time_offset = value

    def get_time_offset(self):
        return self.__time_offset

    time_offset = property(get_time_offset, set_time_offset)

    def get_channel_recording_parameters(self):
        return self.__channel_recording_parameters

    channel_recording_parameters = property(get_channel_recording_parameters)

    def time_to_samples(self, value):
        return np.where(self.time >= value)[0][0]

    def __parse_store_data(self):
        count = 0
        for _key_name in list(self._file_data.keys()):
            if re.search(r'(\s*)Store Data', _key_name):
                data_values_key = [_sub_key for _sub_key in self._file_data[_key_name] if re.search('averaged data',
                                                                                                    _sub_key)]
                _fs_key = [_sub_key for _sub_key in self._file_data[_key_name] if re.search('sampling frequency*',
                                                                                            _sub_key)][0]
                if not data_values_key:
                    continue
                data_unit = re.search(r'\([A-Za-z]*\)', data_values_key[0]).group()
                _data = np.expand_dims(
                    np.array(list(map(float, self._file_data[_key_name][data_values_key[0]].split(',')))),
                    axis=1)
                # self.__channel_labels.append(self._file_data[_key_name]['channel number'])
                self.__channel_labels.append(str(count))
                self.__channel_units.append(data_unit)
                self.__fs.append(float(self._file_data[_key_name][_fs_key]) * 1000.0)
                if not self.__data.any():
                    self.__data = np.append(self.__data, _data)
                else:
                    self.__data = np.hstack((self.__data, _data))
                if self.__data.ndim == 1:
                    self.__data = np.expand_dims(self.__data, axis=1)
                _temp_dict = self._file_data[_key_name].copy()
                _temp_dict.pop(data_values_key[0])
                self.__channel_recording_parameters.append(_temp_dict)
                count += 1

    def get_fs(self):
        return np.unique(self.__fs)

    def set_fs(self, new_value):
        self.__fs = new_value

    fs = property(get_fs, set_fs)

    def get_file_name(self):
        return self.__file_name

    def set_file_name(self, new_value):
        self.__file_name = new_value

    file_name = property(get_file_name, set_file_name)

    def get_epochs(self, win_length=0):
        return self.data

    def get_triggers(self, triggerCodes=[]):
        return []


class IniParser(configparser.ConfigParser):
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d
