import os
import numpy as np
import re
from peegy.definitions.channel_definitions import ChannelItem, ChannelType
import logging
import astropy.units as u
from peegy.tools.units.unit_tools import set_default_unit
log = logging.getLogger()


class DeviceEventChannel:
    bdf_event_channel = 'Status'
    edf_event_channel = 'EDF Annotations'
    bdf_event_annotations = 'BDF Annotations'
    auto = 'auto'


def read_edf_bdf_header(file_name):
    with open(file_name, 'rb') as f:
        # read first 256 bytes
        # first byte is skipped as is not important for bdf or edf files
        f.seek(1, 1)
        header = {'file_name': file_name,
                  'file_size': os.path.getsize(file_name),
                  'version': f.read(7).strip().decode('ascii'),
                  'subject_id': f.read(80).strip().decode('ascii'),
                  'recording_id': f.read(80).strip().decode('ascii'),
                  'start_date': f.read(8).strip().decode('ascii'),
                  'start_time': f.read(8).strip().decode('ascii'),
                  'bytes_in_header': int(f.read(8)),
                  'data_format': f.read(44).strip().decode('ascii'),
                  'number_records': int(f.read(8)),
                  'duration_data_record': float(f.read(8)) * u.s,
                  'n_channels': int(f.read(4))}
        header['duration'] = header['number_records'] * header['duration_data_record']
        # read next N x 256 bytes
        ch = []
        [ch.append(ChannelItem(label=f.read(16).strip().decode('ascii'), idx=i)) for i in range(header['n_channels'])]
        header['channels'] = np.array(ch)
        ch = []
        [ch.append(f.read(80).strip().decode('ascii')) for i in range(header['n_channels'])]
        header['transducer'] = np.array(ch)
        ch = []
        [ch.append(f.read(8).strip().decode('ascii')) for i in range(header['n_channels'])]
        header['physical_dimension'] = np.array(ch)
        ch = []
        [ch.append(float(f.read(8))) for i in range(header['n_channels'])]
        header['physical_minimum'] = np.array(ch)
        ch = []
        [ch.append(float(f.read(8))) for i in range(header['n_channels'])]
        header['physical_maximum'] = np.array(ch)
        ch = []
        [ch.append(float(f.read(8))) for i in range(header['n_channels'])]
        header['digital_minimum'] = np.array(ch)
        ch = []
        [ch.append(float(f.read(8))) for i in range(header['n_channels'])]
        header['digital_maximum'] = np.array(ch)
        ch = []
        [ch.append((header['physical_maximum'][i] - header['physical_minimum'][i]) /
                   (header['digital_maximum'][i] - header['digital_minimum'][i]))
         for i in range(header['n_channels'])]
        header['gain'] = np.array(ch)
        ch = []
        [ch.append(f.read(80).strip().decode('ascii')) for i in range(header['n_channels'])]
        header['pre_filtering'] = np.array(ch)
        ch = []
        [ch.append(int(f.read(8))) for i in range(header['n_channels'])]
        header['number_samples_per_record'] = np.array(ch)
        ch = []
        [ch.append(f.read(32).strip().decode('ascii')) for i in range(header['n_channels'])]
        header['reserved'] = np.array(ch)
        ch = []
        [ch.append((header['number_samples_per_record'][i] / header['duration_data_record']).to(u.Hz).value)
         for i in range(header['n_channels'])]
        header['fs'] = np.array(ch) * u.Hz
        if header['number_records'] == -1:
            header_off_set = 256 * (1 + header['n_channels'])
            header['number_records'] = ((os.stat(header['file_name']).st_size -
                                         header_off_set) / header['n_channels'] / header['fs'][0].value / 3
                                        ).astype(np.int64)
            header['duration'] = header['number_records'] * header['duration_data_record']

    return header


def read_bdf_channel(header,
                     channels_idx: np.array = np.array([]),
                     ini_time: u.quantity.Quantity = 0 * u.s,
                     end_time: u.quantity.Quantity = None,
                     include_event_channel=True,
                     event_channel_label=DeviceEventChannel.bdf_event_channel):
    fs_data = set_default_unit(header['fs'][0], u.Hz)
    ini_time = set_default_unit(ini_time, u.s)
    end_time = set_default_unit(end_time, u.s)
    if end_time is None:
        end_time = np.floor(header['duration'])
    else:
        end_time = np.minimum(end_time, header['duration'])

    if not channels_idx.size:
        channels = header['channels']
    else:
        channels = header['channels'][channels_idx]

    annotated_event_channel = False
    fs_events = None
    if include_event_channel:
        if event_channel_label == DeviceEventChannel.bdf_event_annotations:
            annotated_event_channel = True

        # check if trigger channel is in channel list
        _idx_event = np.squeeze([_i for _i, _ch in enumerate(channels) if _ch.label == event_channel_label])
        if _idx_event.size == 0:
            _idx_event = [_i for _i, _ch in enumerate(header['channels']) if _ch.label == event_channel_label][0]
            channels = np.append(channels, header['channels'][_idx_event])
        fs_events = header['fs'][_idx_event]

    ini_time = np.round(ini_time / header['duration_data_record']) * header['duration_data_record']
    records_to_read = np.floor((end_time - ini_time) / header['duration_data_record']).astype(np.int64)
    # buffer_size = np.round(records_to_read * header['duration_data_record'] * fs_data).astype(np.int64)
    buffer_size_data = np.round(records_to_read * header['duration_data_record'] * fs_data).astype(np.int64)
    buffer_size_events = np.round(records_to_read * header['duration_data_record'] * fs_events).astype(np.int64)
    start_offset = (3 * ini_time.value * np.sum(header['number_samples_per_record'])).astype(np.int64)
    data_channel = np.zeros((buffer_size_data, len(channels) - 1), dtype=np.float32)
    event_channel = np.zeros((buffer_size_data, 1), dtype=np.float32)

    event_channel_annotations = None
    if annotated_event_channel:
        event_channel_annotations = np.zeros((buffer_size_events * 3, 1), dtype=np.uint8)
    # buffer to store events as additional channel
    sys_code_channel = np.zeros((buffer_size_data,), dtype=np.float)
    record_length = np.int64(np.sum(header['number_samples_per_record']) * 3)
    _time = ini_time
    with open(header['file_name'], 'rb') as f:
        # skip first 256 bytes + 256 * N channels
        header_off_set = 256 * (1 + header['n_channels'])
        ch_offsets = np.cumsum((np.concatenate(([0], header['number_samples_per_record']))))
        for nr in range(records_to_read):
            for i, ch in enumerate(channels):
                samples_per_record = np.int64(header['number_samples_per_record'][ch.idx])
                f.seek(header_off_set + start_offset + ch_offsets[ch.idx] * 3 + record_length * nr)
                data = np.fromfile(f, dtype=np.uint8, count=3 * samples_per_record)
                try:
                    if ch.label != event_channel_label or ch.label == DeviceEventChannel.bdf_event_channel:
                        data = data.reshape(-1, 3).astype(np.int32)
                except Exception:
                    print("Your data file seems to be INCOMPLETE, check it!")
                    break
                if not data.size:
                    break
                if ch.label != event_channel_label:
                    data = np.int32((data[:, 0] << 8) | (data[:, 1] << 16) | (data[:, 2] << 24)) >> 8
                    data_channel[nr * samples_per_record: (nr + 1) * samples_per_record, i] = data
                else:
                    if ch.label == DeviceEventChannel.bdf_event_channel:
                        sys_code_channel[nr * samples_per_record: (nr + 1) * samples_per_record] = data[:, 2]
                        # data = (data[:, 0] | (data[:, 1] << 8)) & 255
                        data = (np.int32((data[:, 0] << 8) | (data[:, 1] << 16) | (data[:, 2] << 24)) >> 8) & (
                                2 ** 16-1)
                        event_channel[nr * samples_per_record: (nr + 1) * samples_per_record, 0] = data
                        # set channel type to event
                        ch.type = ChannelType.Event
                    if ch.label == DeviceEventChannel.bdf_event_annotations:
                        event_channel_annotations[nr * samples_per_record * 3:
                                                  (nr + 1) * samples_per_record * 3, 0] = data
            _time = _time + header['duration_data_record']
            print('Processed time: {:.1f}'.format(_time))
    unique_events, unique_codes = None, None
    if annotated_event_channel:
        event_channel, unique_events, unique_codes = decode_annotated_events(
            data=event_channel_annotations,
            fs_data=fs_data,
            event_channel=event_channel,
            ini_time=ini_time
        )
    gain = np.array([header['gain'][ch.idx] for ch in channels])
    # convert all data channels to same unit (micro Volts)
    unit_scaling = np.array([u.Quantity(1, header['physical_dimension'][ch.idx]).to(u.uV).value
                             for ch in channels[0:-1]])
    return data_channel * gain[0:-1] * unit_scaling * u.uV, event_channel * gain[-1], (unique_events, unique_codes)


def read_edf_channel(header,
                     channels_idx: np.array = np.array([]),
                     ini_time: u.quantity.Quantity = 0 * u.s,
                     end_time: u.quantity.Quantity = None,
                     include_event_channel=True,
                     event_channel_label=DeviceEventChannel.edf_event_channel):
    fs_data = set_default_unit(header['fs'][0], u.Hz)
    ini_time = set_default_unit(ini_time, u.s)
    end_time = set_default_unit(end_time, u.s)
    if event_channel_label is None:
        event_channel_label = DeviceEventChannel.edf_event_channel
    if end_time is None:
        end_time = np.floor(header['duration'])
    else:
        end_time = np.minimum(end_time, header['duration'])
    if not channels_idx.size:
        channels = header['channels']
    else:
        channels = header['channels'][channels_idx]
    _idx_event = None
    if include_event_channel:
        # check if trigger channel is in channel list
        _idx_event = np.squeeze(np.array([_i for _i, _ch in enumerate(channels) if _ch.label == event_channel_label]))
        if _idx_event.size == 0:
            _idx_event = [_i for _i, _ch in enumerate(header['channels']) if _ch.label == event_channel_label][0]
            channels = np.append(channels, header['channels'][_idx_event])
        fs_events = header['fs'][_idx_event]
    # ensure that in_time is multiple of duration_data_record
    ini_time = np.round(ini_time / header['duration_data_record']) * header['duration_data_record']
    records_to_read = np.floor((end_time - ini_time) / header['duration_data_record']).astype(np.int64)
    header_off_set = 256 * (1 + header['n_channels'])
    ch_offsets = np.cumsum((np.concatenate(([0], header['number_samples_per_record']))))

    buffer_size_data = np.round(records_to_read * header['duration_data_record'] * fs_data).astype(np.int64)
    buffer_size_events = np.round(records_to_read * header['duration_data_record'] * fs_events).astype(np.int64)
    data_channel = np.zeros((buffer_size_data, len(channels) - 1), dtype=np.float32)
    event_channel = np.zeros((buffer_size_data, 1), dtype=np.float32)
    sys_code_channel = np.zeros((buffer_size_events,), dtype=np.int16)
    record_length = np.sum(header['number_samples_per_record']) * 2
    start_offset = (ini_time.value * record_length).astype(np.int64)
    _time = ini_time
    unique_events, unique_codes = [], []
    with open(header['file_name'], 'rb') as f:
        # skip first 256 bytes + 256 * N channels
        for nr in range(records_to_read):
            for i, ch in enumerate(channels):
                samples_per_record = header['number_samples_per_record'][ch.idx]
                f.seek(header_off_set + start_offset + ch_offsets[ch.idx] * 2 + record_length * nr)
                data = np.fromfile(f, dtype=np.int16, count=samples_per_record)
                _length = data.shape[0]
                _ini_pos = nr * samples_per_record
                _end_pos = _ini_pos + _length
                if ch.label != (event_channel_label or DeviceEventChannel.edf_event_channel):
                    data_channel[_ini_pos: _end_pos, i] = data
                if ch.label == (event_channel_label or DeviceEventChannel.edf_event_channel):
                    sys_code_channel[_ini_pos: _end_pos] = data
                    # set channel type to event
                    ch.type = ChannelType.Event
            _time = _time + header['duration_data_record']
            print('Processed time %f' % _time)

    if include_event_channel:
        if channels[-1].label == (event_channel_label or DeviceEventChannel.edf_event_channel):
            # fist we try getting annotated channel
            event_channel, unique_events, unique_codes = decode_annotated_events(
                data=sys_code_channel,
                fs_data=fs_data,
                event_channel=event_channel,
                ini_time=ini_time
            )
    gain = np.array([header['gain'][ch.idx] for ch in channels])
    # convert all data channels to same unit (micro Volts)
    unit_scaling = np.array([u.Quantity(1, header['physical_dimension'][ch.idx]).to(u.uV).value
                             for ch in channels[0:-1]])
    return data_channel * unit_scaling * u.V * gain[0:-1], event_channel, (unique_events, unique_codes)


def get_event_channel(header,
                      ini_time: u.quantity.Quantity = 0 * u.s,
                      end_time: u.quantity.Quantity = None,
                      event_channel_label=None):
    event_channel = None
    _, file_extension = os.path.splitext(header['file_name'])
    if event_channel_label is None:
        event_channel_label = DeviceEventChannel.bdf_event_channel if file_extension == '.bdf' \
            else DeviceEventChannel.edf_event_channel
    annotations = None
    _idx_event = np.array([_i for _i, _ch in enumerate(header['channels']) if _ch.label == event_channel_label])
    if file_extension == '.bdf':
        _, event_channel, annotations = read_bdf_channel(header=header,
                                                         ini_time=ini_time,
                                                         end_time=end_time,
                                                         channels_idx=_idx_event,
                                                         event_channel_label=event_channel_label)
    if file_extension == '.edf':
        _, event_channel, annotations = read_edf_channel(header=header,
                                                         ini_time=ini_time,
                                                         end_time=end_time,
                                                         channels_idx=_idx_event,
                                                         event_channel_label=event_channel_label)

    return event_channel, annotations


def get_data(header,
             channels_idx: np.array = None,
             ini_time: u.quantity.Quantity = 0 * u.s,
             end_time: u.quantity.Quantity = None,
             event_channel_label: str = None):
    data, events = None, None
    _, file_extension = os.path.splitext(header['file_name'])
    annotations = ()
    if file_extension == '.bdf':
        data, events, annotations = read_bdf_channel(header=header, channels_idx=channels_idx,
                                                     ini_time=ini_time, end_time=end_time,
                                                     event_channel_label=event_channel_label)
    if file_extension == '.edf':
        data, events, annotations = read_edf_channel(header=header,
                                                     channels_idx=channels_idx,
                                                     ini_time=ini_time,
                                                     end_time=end_time,
                                                     event_channel_label=event_channel_label)
    return data, events, data.unit, annotations


def decode_annotated_events(data: np.array = None,
                            fs_data: float = None,
                            ini_time: float = None,
                            event_channel: np.array = None):
    pattern = re.compile('([+-]\\d+\\.?\\d*)(\x15(\\d+\\.?\\d*))?(\x14.*?)\x14\x00')
    start_event = pattern.findall(data.tostring().decode('latin-1'))
    used_events = []
    for _ev in start_event:
        onset = float(_ev[0]) * u.s
        duration = float(_ev[2]) * u.s if _ev[2] else 0 * u.s
        for description in _ev[3].split('\x14')[1:]:
            if description:
                used_events.append([onset, duration, description])

    if len(used_events) > 0:
        event_pos = []
        event_dur = []
        event_label = []

        for _i_time, _dur, _code in used_events:
            event_pos.append(_i_time - ini_time)
            event_dur.append(0 if _dur == '' else _dur)
            event_label.append(_code.replace('\x14', ''))

        try:
            # if labels are integer, we use them as numeric code
            event_code = np.array(event_label).astype(np.int)
        except ValueError:
            # if labels are not, generate a numeric code
            unique_events = np.unique(event_label)
            unique_codes = np.arange(0, unique_events.size) + 1
            event_code = np.array([int(unique_codes[np.where(_l == unique_events)[0]]) for _l in event_label])

        for _ini, _dur, _code in zip(event_pos, event_dur, event_code):
            _ini_time = _ini
            _end_time = _ini_time + np.maximum(_dur, 1 / fs_data)
            # compute samples as this were recorded as a data channel
            _ini_sample = np.minimum((_ini_time * fs_data).astype(np.int64), event_channel.shape[0])
            _end_sample = np.minimum(np.maximum((_end_time * fs_data).astype(np.int64), _ini_sample + 1),
                                     event_channel.shape[0])

            event_channel[_ini_sample: _end_sample, 0] = _code
    else:
        # if none annotations are found we try to read channel  event as a data channel
        event_channel[:, 0] = data
    return event_channel, unique_events, unique_codes
