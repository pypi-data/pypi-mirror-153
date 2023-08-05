# -*- coding: utf-8 -*-
"""
This module reads and process data from 24-bit Biosemi BDF files recorded with the ActiveTwo system together with
provided stimulation info.
@author:Jaime Undurraga
"""

from peegy.io import edf_bdf_reader as eb_reader
from peegy.layouts import layouts as lay
from peegy.definitions.eegReaderAbstractClasses import EEGData, EegChannel
import numpy as np
import peegy.processing.tools.filters.eegFiltering as eegf
from peegy.plot.eeg_ave_epochs_plot_tools import eeg_save_time_slice
from prettytable import PrettyTable
import logging
import astropy as u
from numpy import empty as _empty, float32
import os
import matplotlib.pyplot as plt

log = logging.getLogger()


def empty(*args, **kwargs):
    kwargs.update(dtype=float32)
    _empty(*args, **kwargs)


class EdfBdfDataReader(EEGData):
    def __init__(self, **kwargs):
        super(EdfBdfDataReader, self).__init__(**kwargs)
        self.layout_setup = kwargs.get('layout_setup', 'biosemi64.lay')
        self.channels_to_process = kwargs.get('channels_to_process', [])
        layout_replacement_list = kwargs.get('layout_replacement_list', None)
        self._data = []
        self._channelLabels = []
        _, file_extension = os.path.splitext(self.file_name)
        if file_extension == '.bdf':
            self.type = 'bdf'
        else:
            self.type = 'edf'
        self._header = eb_reader.read_edf_bdf_header(self.file_name)
        self.n_Channels = self._header['n_channels']
        self._fs = self._header['fs'][0]
        self._fs_raw = self._header['fs'][0]
        self._time_units = u.s
        self._amplitude_units = 0.0001 * u.V
        self._channels = []
        self._bad_channels = []
        self._oeg_channels = []
        self.layout = lay.Layout(file_name=self.layout_setup)

        self.data_processing['labels_to_replace'] = np.ndarray.tolist(layout_replacement_list) if \
            layout_replacement_list is not None else None

        if layout_replacement_list is not None:
            lay.change_layout_electrode(self.layout,
                                        labels_to_replace=layout_replacement_list,
                                        channel_mapping=self._header['channels'])

        self._channels = np.array([EegChannel(number=_ch) for _ch in self.channels_to_process])
        for _ch in self._channels:
            if _ch.number in self.layout.get_index():
                idx = int(np.argwhere(self.layout.get_index() == _ch.number))
                _item = self.layout.get_item(idx)
                _ch.x, _ch.y, _ch.h, _ch.label = (_item.x, _item.h, _item.y, _item.label)
            else:
                ch_nums = [_biosemi_ch['number'] for _biosemi_ch in self._header['channels']]
                idx = ch_nums.index(_ch.number)
                _ch.label = self._header['channels'][idx]['label']
                _ch.number = self._header['channels'][idx]['number']

        if len(self.ref_channels) == 1 and self.ref_channels[0].number is None:
            self.ref_channels = self._channels

    def get_all_channels(self):
        # TODO filter bad channels and oeg channels
        return self._channels

    all_channels = property(get_all_channels)

    def get_channel_by_label(self, channel_labels=['']):
        _channels = np.array([EegChannel(label=_ch) for _ch in channel_labels])
        for _ch in _channels:
            if _ch.label in self.layout['label']:
                idx = self.layout['label'].index(_ch.label)
                _ch.x, _ch.y, _ch.h, _ch.number = (self.layout['x'][idx], self.layout['y'][idx],
                                                   self.layout['h'][idx], self.layout['channel'][idx])
            else:
                ch_labels = [_biosemi_ch['label'] for _biosemi_ch in self._header['channels']]
                idx = ch_labels.index(_ch.label)
                _ch.number = self._header['channels'][idx]['number']
        return _channels

    def get_channel_idx(self, channel_labels=None):
        channels = [_ch for _ch in self._header['channels'] if _ch['label'] in channel_labels]
        return channels

    def get_triggers_events(self, **kwargs):
        trigger_channels = kwargs.get('trigger_channels', None)
        ideal_epoch_length = kwargs.get('ideal_epoch_length', None)
        if trigger_channels is not None:
            _channels = self.get_channel_idx(channel_labels=trigger_channels)
            trigger_data = eb_reader.get_data(header=self._header, channels=_channels)
            fig_file_name = self.paths.figure_basename_path + 'detected_triggers' + '.png'
            _events = self.find_triggers(data=trigger_data[:, 0],
                                         ideal_epoch_length=ideal_epoch_length,
                                         fig_file_name=fig_file_name)

        else:
            _, _events, _ = eb_reader.get_trigger_channel(header=self._header)

        # if requested we append new triggers
        _events = self.append_trigger_events(_events, **kwargs)
        return _events

    def append_trigger_events(self, events, **kwargs):
        target_event = kwargs.get('target_event', None)
        new_event_code = kwargs.get('new_event_code', None)
        new_event_time = kwargs.get('new_event_time', None)
        if target_event is None or new_event_code is None:
            return events
        code = np.array([])
        idx = np.array([])
        dur = np.array([])
        dur_samples = np.array([])
        for _code, _idx, _dur, _dur_samples in zip(events['code'], events['idx'], events['dur'], events['dur_samples']):
            code = np.append(code, _code)
            idx = np.append(idx, _idx)
            dur = np.append(dur, _dur)
            dur_samples = np.append(dur_samples, _dur_samples)
            if _code == target_event:
                code = np.append(code, new_event_code)
                idx = np.append(idx, np.round(new_event_time * self.fs).astype(np.int) + _idx)
                dur = np.append(dur, _dur)
                dur_samples = np.append(dur_samples, _dur_samples)

        event_table = {'code': code,

                       'idx': idx,
                       'dur': dur,
                       'dur_samples': dur_samples}
        return event_table

    def get_triggers(self, trigger_codes=[], **kwargs):
        _trigger_data = eb_reader.get_trigger_channel(header=self._header, **kwargs)
        return self.get_sub_triggers(trigger_data=_trigger_data, trigger_codes=trigger_codes)

    def get_sub_triggers(self, trigger_data=[], trigger_codes=[]):
        if not trigger_codes:
            sub_set_idx = np.arange(len(trigger_data['code'])).astype(int)
        else:
            sub_set_idx = np.where(trigger_data['code'] == trigger_codes[0])[0]
            if not sub_set_idx.size or not sub_set_idx.any():
                _triggers = {'idx': np.array([]),
                             'dur': np.array([]),
                             'code': np.array([]),
                             'dur_samples': np.array([]),
                             'min_distance': np.array([]),
                             'max_distance': np.array([]),
                             'position': np.array([]),
                             'triggers': []}
                return _triggers
        if len(trigger_data['idx'][sub_set_idx]) == 1:
            if len(trigger_data['idx']) > sub_set_idx + 1:
                min_distance = trigger_data['idx'][sub_set_idx + 1] - trigger_data['idx'][sub_set_idx]
                max_distance = min_distance
            elif sub_set_idx - 1 >= 0:
                min_distance = trigger_data['idx'][sub_set_idx] - trigger_data['idx'][sub_set_idx - 1]
                max_distance = min_distance
        else:
            min_distance = min(np.diff(trigger_data['idx'][sub_set_idx]))
            max_distance = max(np.diff(trigger_data['idx'][sub_set_idx]))

        _triggers = {'idx': trigger_data['idx'][sub_set_idx],
                     'dur': trigger_data['dur'][sub_set_idx],
                     'code': trigger_data['code'][sub_set_idx],
                     'dur_samples': trigger_data['dur_samples'][sub_set_idx],
                     'min_distance': [min_distance] * len(trigger_data['idx'][sub_set_idx]),
                     'max_distance': [max_distance] * len(trigger_data['idx'][sub_set_idx]),
                     'position': np.array(sub_set_idx),
                     'triggers': []}

        if len(trigger_codes[1:]) != 0:
            for i in range(len(_triggers['idx'])):
                ini_idx = _triggers['position'][i]
                if i == len(_triggers['idx']) - 1:
                    end_idx = -1
                else:
                    end_idx = _triggers['position'][i + 1] + 1
                _sub_triggers = {}
                for j, key_name in enumerate(trigger_data.keys()):
                    _sub_triggers[key_name] = trigger_data[key_name][ini_idx:end_idx]

                new_triggers = self.get_sub_triggers(trigger_data=_sub_triggers, trigger_codes=trigger_codes[1:])
                _triggers['triggers'].append(new_triggers)
        return _triggers

    @staticmethod
    def get_all_triggers(trigger_data=[], trigger_codes=[]):
        _triggers = {'idx': np.array([]),
                     'dur': np.array([]),
                     'code': np.array([]),
                     'dur_samples': np.array([]),
                     'min_distance': np.array([]),
                     'max_distance': np.array([]),
                     'position': np.array([]),
                     'triggers': []}
        for _code in trigger_codes:
            sub_set_idx = np.where(trigger_data['code'] == _code)[0]
            if not sub_set_idx.size or not sub_set_idx.any():
                continue
            if len(trigger_data['idx'][sub_set_idx]) == 1:
                if len(trigger_data['idx']) > sub_set_idx + 1:
                    min_distance = trigger_data['idx'][sub_set_idx + 1] - trigger_data['idx'][sub_set_idx]
                    max_distance = min_distance
                elif sub_set_idx - 1 >= 0:
                    min_distance = trigger_data['idx'][sub_set_idx] - trigger_data['idx'][sub_set_idx - 1]
                    max_distance = min_distance
            else:
                min_distance = min(np.diff(trigger_data['idx'][sub_set_idx]))
                max_distance = max(np.diff(trigger_data['idx'][sub_set_idx]))

            f_triggers = {'idx': trigger_data['idx'][sub_set_idx],
                          'dur': trigger_data['dur'][sub_set_idx],
                          'code': trigger_data['code'][sub_set_idx],
                          'dur_samples': trigger_data['dur_samples'][sub_set_idx],
                          'min_distance': [min_distance] * len(trigger_data['idx'][sub_set_idx]),
                          'max_distance': [max_distance] * len(trigger_data['idx'][sub_set_idx]),
                          'position': np.array(sub_set_idx),
                          'triggers': []}
            _triggers['triggers'].append(f_triggers)
        return _triggers

    def merge_triggers(self, triggers, trigger_code=[], new_code=None, tolerance=1):
        _new_triggers = []
        new_code = trigger_code if new_code is None else new_code

        for _idx, _code in enumerate(triggers['code'].astype(np.int)):
            if _code & trigger_code == trigger_code:
                if len(_new_triggers) == 0:
                    _new_triggers = {'idx': np.array([triggers['idx'][_idx]]),
                                     'dur': np.array([triggers['dur'][_idx]]),
                                     'code': np.array([new_code]),
                                     'dur_samples': np.array([triggers['dur_samples'][_idx]]),
                                     'min_distance': -1,
                                     'max_distance': -1,
                                     'position': np.array([triggers['position'][_idx]]),
                                     'triggers': []}
                elif triggers['idx'][_idx] - (_new_triggers['idx'][-1] + _new_triggers['dur_samples'][-1]) > tolerance:
                    _new_triggers['idx'] = np.append(_new_triggers['idx'], triggers['idx'][_idx])
                    _new_triggers['dur'] = np.append(_new_triggers['dur'], triggers['dur'][_idx])
                    _new_triggers['dur_samples'] = np.append(_new_triggers['dur_samples'],
                                                             triggers['dur_samples'][_idx])
                    _new_triggers['position'] = np.append(_new_triggers['position'], triggers['position'][_idx])
                    _new_triggers['code'] = np.append(_new_triggers['code'], new_code)
                else:
                    _new_triggers['dur'][-1] += triggers['dur'][_idx]
                    _new_triggers['dur_samples'][-1] += triggers['dur_samples'][_idx]
        min_distance = min(np.diff(_new_triggers['idx']))
        max_distance = max(np.diff(_new_triggers['idx']))
        _new_triggers['min_distance'] = min_distance
        _new_triggers['max_distance'] = max_distance

        new_unique_events = np.unique(_new_triggers['code'])
        new_event_counter = []
        for j, code in enumerate(new_unique_events):
            new_event_counter.append({'code': code, 'n': len(np.where(triggers['code'] == code)[0])})
        logging.info("\n".join([self.file_name, 'Merged Trigger events:', str(new_event_counter)]))
        return _new_triggers

    def split_triggers_by_std(self, triggers, epoch_code=None, std_thr=1.0):
        unique_events = np.unique(triggers['code'])
        # rank triggers
        _triggers_pos = triggers['idx'][triggers['code'] == epoch_code]
        _triggers_diff = np.diff(_triggers_pos)

        _positions_above_thr = np.where(_triggers_diff > std_thr * np.std(_triggers_diff) + np.mean(_triggers_diff))[0]

        if _positions_above_thr.size:
            _positions_above_thr += 1
            target_pos = np.unique(_triggers_pos[_positions_above_thr])
            # set new trigger code for found triggers
            new_code = unique_events[-1] + 1
            triggers['code'][0] = new_code
            # create an event before detected trigger sections
            for _t_pos in target_pos:
                _match_events = int(np.where(triggers['idx'] == _t_pos)[0])
                triggers = self.insert_trigger_event(triggers=triggers, idx=_match_events, code=new_code)

            new_triggers = self.get_sub_triggers(trigger_data=triggers, trigger_codes=[new_code, epoch_code])
            _message = 'there were %i triggers which deviated from the mean trigger duration of %f samples' % \
                       (len(target_pos), np.mean(_triggers_diff))

            logging.info(_message)
            print(_message)
        else:
            new_triggers = self.get_sub_triggers(trigger_data=triggers, trigger_codes=[epoch_code])

        event_counter = []
        for j, code in enumerate(unique_events):
            event_counter.append({'code': code, 'n': len(np.where(new_triggers['code'] == code)[0])})
        logging.info("\n".join([self.file_name, 'Trigger events:', str(event_counter)]))

        return new_triggers

    @staticmethod
    def insert_trigger_event(triggers={}, idx=None, code=None):
        # insert event before given idx
        aux_triggers = {}
        for _key in list(triggers.keys()):
            aux_triggers[_key] = triggers[_key][0:idx]
        aux_triggers['dur'] = np.append(aux_triggers['dur'], triggers['dur'][idx])
        aux_triggers['code'] = np.append(aux_triggers['code'], code)
        aux_triggers['idx'] = np.append(aux_triggers['idx'], triggers['idx'][idx] - triggers['dur_samples'][idx] - 1)
        aux_triggers['dur_samples'] = np.append(aux_triggers['dur_samples'], triggers['dur_samples'][idx])
        for _key in list(triggers.keys()):
            aux_triggers[_key] = np.concatenate((aux_triggers[_key], triggers[_key][idx:]))
        return aux_triggers

    def add_trigger_events(self,
                           triggers={},
                           master_triggers=np.array([]),
                           relative_time_positions=np.array([]),
                           new_code_events=np.array([])):
        # add triggers as desired
        assert new_code_events.ndim == 2, "new_code_events must be a 2D array"
        assert new_code_events.shape[0] == len(master_triggers), \
            "number of new_code_events rows must be same as number of master_triggers"
        assert new_code_events.shape[1] == relative_time_positions.size, \
            "The new_code event must have same length as relative_time_positions"
        _idx_rel_samples = self.time_to_samples(relative_time_positions)
        c_triggers = triggers
        for _mt_idx, m_t in enumerate(master_triggers):
            aux_triggers = {'code': [], 'idx': [], 'dur': [], 'dur_samples': []}
            for _i, (_code, _idx, _dur, _dur_samples) in enumerate(zip(c_triggers['code'],
                                                                       c_triggers['idx'],
                                                                       c_triggers['dur'],
                                                                       c_triggers['dur_samples'])):
                aux_triggers['code'] = np.append(aux_triggers['code'], _code)
                aux_triggers['idx'] = np.append(aux_triggers['idx'], _idx)
                aux_triggers['dur'] = np.append(aux_triggers['dur'], _dur)
                aux_triggers['dur_samples'] = np.append(aux_triggers['dur_samples'], _dur_samples)
                if _code == m_t:
                    aux_triggers['code'] = np.append(aux_triggers['code'], new_code_events[_mt_idx])
                    aux_triggers['idx'] = np.append(aux_triggers['idx'], _idx + _idx_rel_samples)
                    aux_triggers['dur'] = np.append(aux_triggers['dur'], _dur * np.ones(_idx_rel_samples.shape))
                    aux_triggers['dur_samples'] = np.append(aux_triggers['dur_samples'],
                                                            _dur_samples * np.ones(_idx_rel_samples.shape))
            c_triggers = aux_triggers
        new_epoch_codes = np.concatenate(new_code_events)
        return c_triggers, new_epoch_codes

    @staticmethod
    def clean_triggers(triggers={}, **kwargs):
        min_number_triggers = kwargs.get('min_number_triggers', 10)
        sub_n_triggers = [len(_sub_trigg['idx']) for _, _sub_trigg in enumerate(triggers['triggers'])]
        sub_codes = [np.unique(_sub_trigg['code']) for _, _sub_trigg in enumerate(triggers['triggers'])]
        to_remove = np.where(np.array(sub_n_triggers) < min_number_triggers)[0]
        t = PrettyTable()
        if triggers['code'].size:
            t.add_column(fieldname='Parent Trigger code', column=triggers['code'])
        if sub_codes:
            t.add_column(fieldname='Sub-trigger code', column=sub_codes)
        if sub_n_triggers:
            t.add_column(fieldname='Number of sub-triggers', column=sub_n_triggers)
            t.add_column(fieldname='Used', column=np.array(sub_n_triggers) >= min_number_triggers)
        print(t)
        logging.info(t)
        for _i, _idx_rem in enumerate(to_remove):
            triggers_to_remove = int(_idx_rem - _i)
            print('Removing trigger event %i with %i sub events,   check your data!' % (
                triggers['code'][triggers_to_remove], len(triggers['triggers'][triggers_to_remove]['idx'])))
            for _, _key in enumerate(triggers.keys()):
                triggers[_key] = np.delete(triggers[_key], triggers_to_remove)
        return triggers

    def get_data(self, channels=[{}], triggers={}, **kwargs):
        # auto_detect_reference = kwargs.get('auto_detect_reference', False)
        ini_time = kwargs.get('ini_time', np.floor(triggers['idx'][0] / self._fs_raw))
        end_time = kwargs.get('end_time', np.ceil(
            (triggers['idx'][-1] + triggers['min_distance'][0] - 1) / self._fs_raw))

        data = eb_reader.get_data(header=self._header,
                                  channels=[_ch.__dict__ for _ch in channels],
                                  ini_time=ini_time,
                                  end_time=end_time)
        relative_offset = np.floor(ini_time * self._fs_raw).astype(np.int)
        _channels_str = '_to_'.join(map(str, [_ch.label for _ch in [channels[0], channels[-1]]]))
        eeg_save_time_slice(data=data,
                            fs=self._fs_raw,
                            channels=self.channels,
                            title='raw data slice',
                            file_name=self.paths.figure_basename_path + _channels_str + 'raw_slice.png')

        t = PrettyTable()
        t.add_column(fieldname='File name', column=[self._file_name])
        t.add_column(fieldname='Trigger block', column=[str(triggers['idx'][0]) + ',' + str(triggers['idx'][-1])])
        log.info(t)
        print(t)
        return data, relative_offset

    def get_raw_data(self, channels=np.array([EegChannel()]), triggers={}, **kwargs):
        ref_channels = kwargs.get('ref_channels', np.array([EegChannel()]))
        resampling_fs = kwargs.get('resampling_fs', None)
        bad_channels = kwargs.get('bad_channels', [])
        remove_bad_channels = kwargs.get('remove_bad_channels', True)
        interpolation_rate = kwargs.get('interpolation_rate', None)
        interpolation_width = kwargs.get('interpolation_width', None)
        interpolation_offset = kwargs.get('interpolation_offset', 0)
        # add reference channels if buffer is not filled and if not included in all channels
        if not self._reference.size:
            for _r_ch in ref_channels:
                if not [_ch for _ch in channels if _ch.__dict__ == _r_ch.__dict__]:
                    channels.append(_r_ch)

        # remove from list bad known channels
        if remove_bad_channels:
            _known_bad_channels_pos = [i for i, _ch in enumerate(channels) if _ch.label in bad_channels]
            _bad_channels = [channels[i] for i in _known_bad_channels_pos]
            if _bad_channels:
                [channels.pop(idx) for bd in _bad_channels for idx, ch in enumerate(channels) if ch == bd]

        if resampling_fs:
            self.resampling_factor = resampling_fs / self._fs_raw

        _data = self.find_array(parameters=self.data_processing, descriptor='raw_data')
        if _data:
            data = _data['raw_data']
            relative_triggers = _data['relative_triggers']
            buffer_size = _data['buffer_size']
            self._fs = self._fs_raw * self.resampling_factor
        else:
            # get data slice
            data, relative_triggers,  buffer_size = \
                self.get_data_slice(channels=channels, triggers=triggers, **kwargs)

            if interpolation_rate is not None and interpolation_width is not None:
                _ini_points = np.array([], dtype=np.int64)
                # _length = np.mean(np.diff(relative_triggers))
                # int_vector = np.floor(np.arange(0, _length / self._fs_raw, 1. / interpolation_rate) * self._fs_raw)
                for _idx, _int_dur in enumerate(np.diff(relative_triggers)):
                    int_vector = np.floor(np.arange(0, _int_dur / self._fs_raw, 1. / interpolation_rate) * self._fs_raw)
                    _ini_points = np.concatenate((_ini_points, relative_triggers[_idx] + int_vector)).astype(np.int64)

                # after last trigger  data is interpolated as long as the mean interval duration
                int_vector = np.floor(
                    np.arange(0, np.mean(np.diff(relative_triggers)) / self._fs_raw, 1. / interpolation_rate) *
                    self._fs_raw)
                _ini_points = np.concatenate((_ini_points, relative_triggers[-1] + int_vector)).astype(np.int64)

                _end_points = _ini_points + np.ceil(interpolation_width * self._fs_raw).astype(int)
                offset = int(np.round(interpolation_offset * self._fs_raw))
                interpolation_data_points = {'ini': _ini_points + offset, 'end': _end_points + offset}
                self.interpolate_data(data, interpolation_data_points=interpolation_data_points)

            # resampling data
            data, _factor = eegf.eeg_resampling(x=data, factor=self.resampling_factor)
            if _factor != 1.0:
                self.resampling_factor = _factor
                self._fs = self._fs_raw * _factor
                buffer_size = int(buffer_size * _factor)
                relative_triggers = (relative_triggers * _factor).astype(np.int)

            self.save_array(parameters=self.data_processing, data_type='array',
                            data={'raw_data': data,
                                  'relative_triggers': relative_triggers,
                                  'buffer_size': np.array([buffer_size])},
                            descriptor='raw_data')

        t = PrettyTable()
        t.add_column(fieldname='File name', column=[self._file_name])
        t.add_column(fieldname='Trigger block', column=[str(triggers['idx'][0]) + ',' + str(triggers['idx'][-1])])
        t.add_column(fieldname='Removed channels', column=[bad_channels])
        t.add_column(fieldname='Resampling fs', column=[resampling_fs])
        log.info(t)
        return data, relative_triggers, buffer_size

    def get_data_slice(self, channels=[{}], triggers={}, epoch_length=None, **kwargs):
        fft_size = kwargs.get('fft_size', [])
        if not epoch_length:
            epoch_length = triggers['min_distance'][0] / self._fs_raw
        # epoch_length = np.minimum(epoch_length, triggers['min_distance'][0] / self._fs_raw)
        buffer_size = np.floor(epoch_length * self._fs_raw).astype(np.int)
        trigger_step = 1.0
        if fft_size:
            trigger_step = np.round(float(fft_size) / float(buffer_size))
            buffer_size = np.floor(epoch_length * trigger_step * self._fs_raw).astype(np.int)
        # check that trigger + buffer_size fit in the whole recording
        # we check against 2 times buffer_size to leave extra gap at the end
        used_trigger = triggers['idx'][self._header['duration'] * self._fs_raw -
                                       (triggers['idx'] + 2 * buffer_size) >= 0]
        used_trigger = used_trigger[np.arange(0, len(used_trigger), trigger_step).astype(np.int)]
        # get data. we read up to last trigger plus 2 times buffer_size to leave extra gap at the end
        data, relative_offset = self.get_data(channels=channels, triggers=triggers,
                                              end_time=np.ceil((used_trigger[-1] + 2 * buffer_size - 1) / self._fs_raw),
                                              **kwargs)
        t = PrettyTable()
        t.add_column(fieldname='File name', column=[self._file_name])
        t.add_column(fieldname='Trigger block', column=[str(used_trigger[0]) + ',' + str(used_trigger[-1])])
        t.add_column(fieldname='Number triggers', column=[len(used_trigger)])
        t.add_column(fieldname='Epoch length', column=[epoch_length * trigger_step])
        log.info(t)
        print(t)
        relative_triggers = used_trigger - relative_offset
        return data, relative_triggers, buffer_size

    def set_data(self, new_value):
        self._data = new_value

    data = property(get_data, set_data)

    def get_channel_labels(self):
        return [channel.label for channel in self._channels]

    def set_channel_labels(self, number, new_value):
        if len(number) == len(new_value):
            for i in number:
                self._channels[i].label = new_value[i]
        else:
            print('number of channels does not match number of labels')

    channelLabels = property(get_channel_labels)

    def get_biosemi_channels(self):
        return self._header['channels']

    def get_channels(self):
        return self._channels

    def set_channels(self, value):
        self._channels = value

    channels = property(get_channels, set_channels)

    def get_system(self):
        return 'Biosemi'

    system = property(get_system)

    def get_amplitude_units(self):
        return self._amplitude_units

    def set_amplitude_units(self, new_value):
        self._amplitude_units = new_value

    amplitude_units = property(get_amplitude_units, set_amplitude_units)

    def get_time_units(self):
        return self._amplitude_units

    def set_time_units(self, new_value):
        self._amplitude_units = new_value

    time_units = property(get_time_units, set_time_units)

    def get_paths(self):
        return self._paths

    paths = property(get_paths)

    def find_triggers(self, **kwargs):
        data = kwargs.get('data', None)
        positive = kwargs.get('positive', True)  # detect only positive
        ideal_epoch_length = kwargs.get('ideal_epoch_length', None)
        fig_file_name = kwargs.get('fig_file_name', None)
        data -= np.mean(data)
        if not positive:
            data *= -1
        data[data <= 0] = 0

        diff_trig = np.diff(np.insert(data, 0, 0))
        #  we will detect positive trantients only
        diff_trig[diff_trig < 0] = 0
        #  we find a detection threshold
        n_triggers = diff_trig.shape[0] / (self._fs * ideal_epoch_length)
        q = 100 - (n_triggers / diff_trig.shape[0]) * 100.0
        h_thr = np.percentile(diff_trig, q)
        _thr = h_thr / 2.0
        diff_trig[diff_trig < _thr] = 0
        # second derivative
        sec_diff = np.diff(np.insert(diff_trig, 0, 0))
        pos = np.where(np.diff(np.sign(sec_diff)))[0]

        # remove positions where second derivative is equal to zero
        pos = pos[sec_diff[pos] != 0]

        c_pos = self.clean_noisy_triggers(trigger_positions=pos,
                                          expected_n_samples=int(self._fs * ideal_epoch_length))
        event_table = {'code': np.ones(c_pos.shape),
                       'idx': c_pos,
                       'dur': np.zeros(c_pos.shape),
                       'dur_samples': np.zeros(c_pos.shape)}
        if fig_file_name is not None:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.plot(data)
            ax.plot(c_pos, np.zeros(c_pos.shape), 'o')
            fig.savefig(fig_file_name)
            print('detected triggers saved to {:s}'.format(fig_file_name))

        return event_table

    @staticmethod
    def clean_noisy_triggers(trigger_positions=[], expected_n_samples=None):
        samples_per_trigger = expected_n_samples * 0.9  # 90% tolerance
        cposIn = 0
        cposOut = 1
        triggerPosClean = np.array([])
        badtriggerPos = np.array([])
        while cposOut < len(trigger_positions):
            if trigger_positions[cposOut] - trigger_positions[cposIn] < samples_per_trigger:
                badtriggerPos = np.append(badtriggerPos, trigger_positions[cposOut])
                cposOut = cposOut + 1
            elif cposOut == len(trigger_positions) - 1:
                triggerPosClean = np.append(triggerPosClean, trigger_positions[cposIn], trigger_positions[cposOut])
                cposOut += 1
            else:
                triggerPosClean = np.append(triggerPosClean, trigger_positions[cposIn])
                cposIn = cposOut
                cposOut += 1
        return triggerPosClean.astype(np.int)
