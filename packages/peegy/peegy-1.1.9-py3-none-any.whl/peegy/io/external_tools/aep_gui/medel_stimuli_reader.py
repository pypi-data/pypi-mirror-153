__author__ = 'jundurraga'

import numpy as np


def get_medel_am_alt_phase_biphasic_pulse_positions(stimulus_parameters={}, **kwargs):
    triggers = kwargs.get('triggers', np.array([]))
    trigger_to_first_pulse_delay = kwargs.get('trigger_to_first_pulse_delay', 8.333e-6)
    trigger_offset_correction = kwargs.get('trigger_offset_correction', True)
    fs = kwargs.get('fs', 16384.0)
    """

    :type trigger_positions: numpy array
    """
    _inter_pulse_interval = 1 / stimulus_parameters['CarrierRate']
    phase_alt_period = 1 / stimulus_parameters['AltPhaseRate']
    _comp_slope = 1.0
    _triggers_pos = triggers['idx']
    n_epochs = len(_triggers_pos)
    expected_samples_per_trigger = 0.0

    if trigger_offset_correction:
        expected_samples_per_trigger = stimulus_parameters['Duration']
        _trigger_distance = np.mean(np.diff(_triggers_pos)) / fs
        _comp_slope = _trigger_distance / expected_samples_per_trigger

    _n_pulses_per_epoch = np.round(stimulus_parameters['Duration'] * stimulus_parameters['CarrierRate'])
    _switch_count = 0
    _pulse_positions = np.array([])
    _temp_switch_distance = 0.0
    n_sequences = 1
    for i in np.arange(n_sequences):
        for j in np.arange(_n_pulses_per_epoch):
            _time = j * _inter_pulse_interval
            if j == 0:
                # set the starting phase for starting sequence
                _temp_switch_distance = _inter_pulse_interval * (stimulus_parameters['CarrierPhase'] / (2 * np.pi))
                if i > 0:
                    _temp_switch_distance = _inter_pulse_interval * (
                            stimulus_parameters['CarrierPhase'] - stimulus_parameters['CarrierAltPhase']) / (2 * np.pi)

            else:
                if np.round(_time * 1.0e6) >= np.round(phase_alt_period / 2 * (_switch_count + 1) * 1.0e6):
                    _switch = True
                    _switch_count += 1
                else:
                    _switch = False

                if _switch:
                    if np.mod(_switch_count, 2) == 1:
                        _switch_phase = _inter_pulse_interval * (stimulus_parameters['CarrierAltPhase'] -
                                                                 stimulus_parameters['CarrierPhase']) / (2 * np.pi)
                    else:
                        _switch_phase = _inter_pulse_interval * (stimulus_parameters['CarrierPhase'] -
                                                                 stimulus_parameters['CarrierAltPhase']) / (2 * np.pi)

                    _temp_switch_distance += _switch_phase

            _pulse_positions = np.append(_pulse_positions, j * _inter_pulse_interval + _temp_switch_distance)
            # compensate drift
            _pulse_positions[-1] = _comp_slope * (_pulse_positions[-1] - expected_samples_per_trigger / fs)

        # start sequence
        _sequence = np.ceil((trigger_to_first_pulse_delay + _pulse_positions) * fs)
        pulse_positions = _triggers_pos[0] + _sequence
    for i in np.arange(1, stimulus_parameters['NRepetitions'] * n_epochs):
        if i > len(_triggers_pos):
            break
        pulse_positions = np.append(pulse_positions, _sequence + _triggers_pos[i])
    assert isinstance(pulse_positions, np.ndarray)
    return pulse_positions


def get_medel_am_biphasic_pulse_positions(stimulus_parameters={}, **kwargs):
    triggers = kwargs.get('triggers', np.array([]))
    trigger_to_first_pulse_delay = kwargs.get('trigger_to_first_pulse_delay', 8.333e-6)
    trigger_offset_correction = kwargs.get('trigger_offset_correction', True)
    fs = kwargs.get('fs', 16384.0)
    """

    :type trigger_positions: numpy array
    """
    _inter_pulse_interval = 1 / stimulus_parameters['CarrierRate']
    _comp_slope = 1.0
    _triggers_pos = triggers['idx']
    n_epochs = len(_triggers_pos)
    expected_samples_per_trigger = 0.0

    if trigger_offset_correction:
        expected_samples_per_trigger = stimulus_parameters['Duration']
        _trigger_distance = np.mean(np.diff(_triggers_pos)) / fs
        _comp_slope = _trigger_distance / expected_samples_per_trigger

    _n_pulses_per_epoch = np.round(stimulus_parameters['Duration'] * stimulus_parameters['CarrierRate'])
    _pulse_positions = np.array([])
    _temp_switch_distance = 0.0
    for j in np.arange(_n_pulses_per_epoch):
        if j == 0:
            # set the starting phase for starting sequence
            _temp_switch_distance = _inter_pulse_interval * (stimulus_parameters['CarrierPhase'] / (2 * np.pi))
        _pulse_positions = np.append(_pulse_positions, j * _inter_pulse_interval + _temp_switch_distance)
        # compensate drift
        _pulse_positions[-1] = _comp_slope * (_pulse_positions[-1] - expected_samples_per_trigger / fs)

    _sequence = np.ceil((trigger_to_first_pulse_delay + _pulse_positions) * fs)
    pulse_positions = _triggers_pos[0] + _sequence
    for i in np.arange(1, stimulus_parameters['NRepetitions'] * n_epochs):
        if i > len(_triggers_pos):
            break
        pulse_positions = np.append(pulse_positions, _sequence + _triggers_pos[i])
    assert isinstance(pulse_positions, np.ndarray)
    return pulse_positions
