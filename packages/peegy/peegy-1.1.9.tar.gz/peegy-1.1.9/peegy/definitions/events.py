import copy

import numpy as np
import astropy.units as u
import pandas as pd


class SingleEvent(object):
    def __init__(self,
                 code: float = None,
                 time_pos: u.quantity.Quantity = None,
                 dur: u.quantity.Quantity = None):
        """
        Class for a single (trigger) event, which is characterized by having a numerical identifier (code), an
        associated time point [s], and a duration [s].
        Parameters
        ----------
        code: Trigger event code (usually some number)
        time_pos: Time in seconds of trigger event
        dur: Duration of trigger event in seconds
        """
        self.code = code
        self.time_pos = time_pos
        self.dur = dur

    def __repr__(self):
        return(f'{self.__class__.__name__}('
               f'{self.code!r}, {self.time_pos!r}, {self.dur!r}')

    def __str__(self):
        return 'Single event at time {} s with code {} and duration {} s'.format(self.time_pos, self.code, self.dur)


class Events(object):
    def __init__(self, events: np.array([SingleEvent]) = None):
        """
        Defines event class
        :param events: raw events array
        """
        self._events = events
        self._mask = None

    @property
    def events(self):
        out = []
        if self.mask is not None:
            for _ev in self._events:
                new_event = copy.copy(_ev)
                new_event.code = float(int(new_event.code) & int(self.mask))
                out.append(new_event)
            out = np.array(out)
        else:
            out = self._events
        return out

    @property
    def mask(self):
        return self._mask

    @mask.setter
    def mask(self, value: float = None):
        self._mask = value
        print('Event mask {:} set'.format(self.mask))
        print(self.summary().to_string(index=False))

    def __repr__(self):
        return(f'{self.__class__.__name__}('
               f'{self.events.shape!r}')

    def __str__(self):
        return 'Event array of size {}'.format(self.events.shape)

    def get_events(self, code=None):
        if code is None:
            return np.array([_ev for _ev in self.events])
        else:
            return np.array([_ev for _ev in self.events if _ev.code == code])

    def get_events_index(self, code=None, fs=None):
        if code is None:
            return np.array([int(_ev.time_pos * fs) for _ev in self.events])
        else:
            return np.array([int(_ev.time_pos * fs) for _ev in self.events if _ev.code == code])

    def get_events_time(self, code=None):
        if code is None:
            return np.array([_ev.time_pos.to(u.s).value for _ev in self.events]) * u.s
        else:
            return np.array([_ev.time_pos.to(u.s).value for _ev in self.events if _ev.code == code]) * u.s

    def get_events_duration(self, code=None):
        if code is None:
            return np.array([_ev.dur.to(u.s).value for _ev in self.events]) * u.s
        else:
            return np.array([_ev.dur.to(u.s).value for _ev in self.events if _ev.code == code]) * u.s

    def get_events_code(self, code=None):
        if code is None:
            return np.array([_ev.code for _ev in self.events])
        else:
            return np.array([_ev.code for _ev in self.events if _ev.code == code])

    def interpolate_events(self, scaling_factor=1.0, code=None, events_mask=None):
        """
        This function interpolates time events between consecutive event. The time position of new events is defined
        by the scaling factor. For example, an scaling_factor of 2.0 will add a new trigger event exactly in the middle
        time between two events
        :param scaling_factor: a float that determine the number of new events that will be generated
        :param code: event code to be interpolated
        :param events_mask: integer value used to masker triggers codes. This is useful to ignore triggers inputs avove
        a particular value. For example, if only the first 8 trigger inputs were used (max decimal value is 255), in a
        system with 16 trigger inputs, then the masker could be set to 255 to ignore any trigger from trigger inputs 9
        to 16.
        :return: new an Events class containing the new interpolated events
        """
        self.mask = events_mask
        _times = self.get_events_time(code=code)
        _durations = self.get_events_duration(code=code)
        _codes = self.get_events_code(code=code)
        _times_intervals = np.diff(_times)
        _times_intervals = np.append(_times_intervals, np.mean(_times_intervals))
        _new_events = []
        for _ini_time, _length, _dur, _code in zip(_times, _times_intervals, _durations, _codes):
            _new_times = np.arange(_ini_time.to(u.s).value,
                                   (_ini_time + _length).to(u.s).value,
                                   (_length / scaling_factor).to(u.s).value) * u.s
            [_new_events.append(SingleEvent(time_pos=_t, dur=_dur, code=_code)) for _t in _new_times]
        return Events(events=np.array(_new_events))

    def summary(self):
        out = pd.DataFrame()
        for i, _code in enumerate(np.unique(self.get_events_code())):
            out = pd.concat([out,
                             pd.DataFrame.from_dict(
                                 {'event_code': [_code],
                                  'n_events': [self.get_events_code(code=_code).size]})],
                            ignore_index=True)
        return out

    def clip(self, ini_time: u.Quantity = 0 * u.s, end_time: u.Quantity = 0 * u.s):
        self.events = np.array([_ev for _ev in self.events if _ev.time_pos >= ini_time])
        self.events = np.array([_ev for _ev in self.events if _ev.time_pos <= end_time])

    def set_offset(self, time_offset: u.Quantity = 0 * u.s):
        self.events = np.array([
            SingleEvent(time_pos=_ev.time_pos - time_offset,
                        dur=_ev.dur,
                        code=_ev.code) for _ev in self.events])
