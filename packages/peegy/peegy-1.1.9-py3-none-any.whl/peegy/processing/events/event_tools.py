import numpy as np
from peegy.definitions.events import SingleEvent, Events
import astropy.units as u


def detect_events(event_channel: np.array = None, fs: float = None):
    start_points = np.hstack((0, np.where(np.diff(event_channel, axis=0) != 0)[0] + 1))
    stop_points = np.hstack(
        (np.where(np.diff(event_channel, axis=0) != 0)[0] + 1, len(event_channel) - 1))
    trigger_duration = (stop_points - start_points) / fs
    events = np.array([])
    for _s, _d in zip(start_points, trigger_duration):
        events = np.append(events, SingleEvent(code=float(event_channel[round(_s)]),
                                               time_pos=_s / fs,
                                               dur=_d))
    return events


def join_trigger_events(all_events=np.array([])):
    code = np.array([])
    idx = np.array([])
    dur = np.array([])
    dur_samples = np.array([])
    event_table = {}
    for events in all_events:
        for _code, _idx, _dur, _dur_samples in zip(events['code'], events['idx'], events['dur'], events['dur_samples']):
            code = np.append(code, _code)
            idx = np.append(idx, _idx)
            dur = np.append(dur, _dur)
            dur_samples = np.append(dur_samples, _dur_samples)
        event_table = {'code': code,
                       'idx': idx,
                       'dur': dur,
                       'dur_samples': dur_samples}
    return event_table


def join_triggers(all_triggers=np.array([])):
    """
    this function join two or more sets of triggers passed in a numpy array
    :param all_triggers: all_triggers: array of triggers
    :return: a new trigger with joined elements
    """
    code = np.array([], dtype=np.int)
    idx = np.array([], dtype=np.int)
    dur = np.array([])
    dur_samples = np.array([], dtype=np.int)
    min_distance = np.array([], dtype=np.int)
    max_distance = np.array([], dtype=np.int)
    position = np.array([], dtype=np.int)

    for events in all_triggers:
        code = np.append(events['code'], code)
        idx = np.append(events['idx'], idx)
        dur = np.append(events['dur'], dur)
        dur_samples = np.append(events['dur_samples'], dur_samples)
        min_distance = np.append(events['min_distance'], min_distance)
        max_distance = np.append(events['max_distance'], max_distance)
        position = np.append(events['position'], position)

    s_idx = np.argsort(idx)
    triggers = {'code': code[s_idx],
                'idx': idx[s_idx],
                'dur': dur[s_idx],
                'dur_samples': dur_samples[s_idx],
                'min_distance': min_distance[s_idx],
                'max_distance': max_distance[s_idx],
                'position': position[s_idx],
                'triggers': []
                }
    return triggers


def get_event_times(event_channel: np.array = None, fs: u.Quantity = None):
    _events = detect_events(event_channel=event_channel, fs=fs)
    _new_events = Events(events=np.array(_events))
    print(_new_events.summary().to_string(index=False))
    return _new_events
