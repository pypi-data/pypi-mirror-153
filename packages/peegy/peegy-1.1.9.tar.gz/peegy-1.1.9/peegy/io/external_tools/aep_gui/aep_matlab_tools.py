import numpy as np
import peegy.processing.tools.weightedAverage as averager
import peegy.io.external_tools.aep_gui.medel_stimuli_reader as medel_reader
from peegy.definitions.eeg_definitions import signal_information
__author__ = 'jundurraga-ucl'


def generate_frequency_dict(j_averager=averager.JAverager, channels=[{}]):
    out = []
    _j_h_test = j_averager.hotelling_t_square_test()
    for i, ch in enumerate(channels):
        for j, h_test in enumerate(_j_h_test[i]):
            out.append(dict(ch, **h_test))
    return out


def get_frequencies_of_interest(stimulus_parameters=[signal_information()]):
    # trigger_channel = parameters['Measurement']['MeasurementModule']['TriggerChannel']
    freq = np.array([], dtype=np.float64)
    for i, _parameters in enumerate(stimulus_parameters):
        if _parameters['type'] in ['generateSinusoidalNotchNoise', 'sinusoidal']:
            freq = np.append(freq, _parameters['ModulationFrequency'])
            freq = np.append(freq, _parameters['CarrierFrequency'])
        elif _parameters['type'] in ['sin_alt_phase', 'medelAM_Alt_Phase_BiphasicPulses', 'transposeToneAltPhase']:
            freq = np.append(freq, [_parameters['AltPhaseRate'] * 2.0 * i for i in np.arange(1, 4)])
        elif _parameters['type'] in ['generateNoiseAltDelaySignal']:
            if 'ITDModRate' in list(_parameters.keys()):
                s_rate = _parameters['ITDModRate']
            if 'NITDModulations' in list(_parameters.keys()):
                s_rate = _parameters['NITDModulations'] / _parameters['Duration']
            freq = np.append(freq, _parameters['ModulationFrequency'])
            freq = np.append(freq, [s_rate * i for i in np.arange(1, 4)])
        elif _parameters['type'] in ['sin_alt_burst']:
            s_rate = _parameters['AltLevelRate']
            freq = np.append(freq, _parameters['ModulationFrequency'])
            freq = np.append(freq, [s_rate * i for i in np.arange(1, 4)])
            freq = np.append(freq, _parameters['ModulationFrequency'] + s_rate)
            freq = np.append(freq, _parameters['ModulationFrequency'] - s_rate)
        elif _parameters['type'] in ['attentional_sin']:
            freq = np.append(freq, _parameters['ModulationFrequencyTa'])
            freq = np.append(freq, _parameters['ModulationFrequencyTb'])
            freq = np.append(freq, _parameters['ModulationFrequencyDa'])
            freq = np.append(freq, _parameters['ModulationFrequencyDb'])
            freq = np.append(freq, _parameters['CarrierFrequencyTa'])
            freq = np.append(freq, _parameters['CarrierFrequencyTb'])
            freq = np.append(freq, _parameters['CarrierFrequencyDa'])
            freq = np.append(freq, _parameters['CarrierFrequencyDb'])
        elif 'AltLevelRate' in _parameters:
            s_rate = _parameters['AltLevelRate']
            freq = np.append(freq, _parameters['ModulationFrequency'])
            freq = np.append(freq, [s_rate * i for i in np.arange(1, 4)])
            freq = np.append(freq, _parameters['ModulationFrequency'] + s_rate)
            freq = np.append(freq, _parameters['ModulationFrequency'] - s_rate)
        elif 'IPMRate' in _parameters:
            s_rate = _parameters['IPMRate']
            freq = np.append(freq, _parameters['ModulationFrequency'])
            freq = np.append(freq, [s_rate * i for i in np.arange(1, 4)])
            freq = np.append(freq, _parameters['ModulationFrequency'] + s_rate)
            freq = np.append(freq, _parameters['ModulationFrequency'] - s_rate)
        elif 'ITMRate' in _parameters:
            s_rate = _parameters['ITMRate']
            freq = np.append(freq, _parameters['ModulationFrequency'])
            freq = np.append(freq, [s_rate * i for i in np.arange(1, 4)])
            freq = np.append(freq, _parameters['ModulationFrequency'] + s_rate)
            freq = np.append(freq, _parameters['ModulationFrequency'] - s_rate)
            if 'Rate' in _parameters:
                freq = np.append(freq, _parameters['Rate'])
        elif 'AltRate' in _parameters and 'ModulationFrequency_1' in _parameters and\
                'ModulationFrequency_2' in _parameters:
            s_rate = _parameters['AltRate']
            freq = np.append(freq, [s_rate * i for i in np.arange(1, 4)])
            freq = np.append(freq, s_rate / 2.0)
            freq = np.append(freq, _parameters['ModulationFrequency_1'])
            freq = np.append(freq, _parameters['ModulationFrequency_2'])
        freq = np.delete(freq, np.where(freq == 0)[0])
    return np.unique(freq)


def get_stimulus_parameters(parameters={}):
    stimuli = []
    if isinstance(parameters, dict) and 'Measurement' in list(parameters.keys()):
        trigger_stimulus = parameters['Measurement']['MeasurementModule']['TriggerChannel']
        for i, stimulus in enumerate(parameters['Measurement']['StimuliModule']['Stimulus']):
            if not stimulus['Parameters']['SignalType'] in ['medelAM_Alt_Phase_BiphasicPulses',
                                                            'medelAMBiphasicPulsesElectChange',
                                                            'generateNoiseAltDelaySignal']:
                if stimulus['Parameters']['Channel'] == trigger_stimulus['Parameters']['Channel']:
                    continue
            _signal = signal_information(**{'type': stimulus['Parameters']['SignalType']})
            for _key in list(stimulus['Parameters'].keys()):
                _signal[_key] = stimulus['Parameters'][_key]
            stimuli.append(_signal)
    return stimuli


def get_interpolation_data_points(**kwargs):
    parameters = kwargs.get('parameters', {})
    width = kwargs.get('width', 1200.0e-6)
    fs = kwargs.get('width', 16384.0)
    _interpolation_points = np.array([])
    for i, stimulus in enumerate(parameters['Measurement']['StimuliModule']['Stimulus']):
        stimulus_parameters = stimulus['Parameters']
        if stimulus_parameters['SignalType'] in ['medelAM_Alt_Phase_BiphasicPulses']:
            _interpolation_points = np.concatenate((_interpolation_points,
                                                    medel_reader.get_medel_am_alt_phase_biphasic_pulse_positions(
                                                        stimulus_parameters, **kwargs)))
            _interpolation_points = np.unique(_interpolation_points)
        if stimulus_parameters['SignalType'] in ['medelAM_BiphasicPulses', 'medelAMBiphasicPulsesElectChange']:
            _interpolation_points = np.concatenate((_interpolation_points,
                                                    medel_reader.get_medel_am_biphasic_pulse_positions(
                                                        stimulus_parameters, **kwargs)))
        _interpolation_points = _interpolation_points.astype(np.int)
    interpolation_points = {'ini': _interpolation_points,
                            'end': _interpolation_points + np.round(width * fs).astype(np.int)}
    return interpolation_points


def cat_dictionary_list(dict_list=[{}]):
    out = {}
    for i, _dict in enumerate(dict_list):
        c_out = {}
        keys = _dict.keys()
        for j, _key in enumerate(keys):
            c_out[_key + '_{}'.format(i)] = _dict[_key]
        out = dict(out, **c_out)
    return out
