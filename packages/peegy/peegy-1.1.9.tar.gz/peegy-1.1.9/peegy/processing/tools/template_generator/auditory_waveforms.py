import numpy as np
from scipy import interpolate
from scipy.signal import hilbert
from peegy.processing.tools.filters.eegFiltering import bandpass_fir_win, ols_filt_filt
import astropy.units as u
from peegy.tools.units.unit_tools import set_default_unit


def aep(fs=16384.0 * u.Hz,
        time_length=1.0 * u.s):
    """
    This function generates a typical auditory cortex waveform (as shown in  Human Auditory Evoked Potentials
    Terence W. Picton
    :param fs: sampling rate of the generated waveform (samples per seconds)
    :param time_length: desired time of the output
    :return: waveform and time vector
    """
    fs = set_default_unit(fs, u.Hz)
    time_length = set_default_unit(time_length, u.s)
    time = np.arange(0, time_length * fs) / fs
    # Terrace Picton peaks latencies (in ms)
    _peak_times = np.array([0.0,
                            0.75,
                            1.5, 2.0,  # I
                            2.5, 3.0,  # II
                            3.5, 4.0,  # III
                            4.5, 5.0,  # IV
                            6.0, 7.0,  # V
                            7.5, 9.0,  # VI-N0
                            13.0, 18.0,  # P0-Na
                            30.0, 40.0,  # Pa-Nb
                            50., 100,  # P1-N1
                            180.0, 300.,   # P2-N2
                            600.0,
                            1000.0
                            ])*1e-3

    # Amplitudes in uV
    _peak_amplitudes = np.array([0.0,
                                 0.0,
                                 0.15, 0.0,  # I
                                 0.1, -0.02,  # II
                                 0.2, 0.03,  # III
                                 0.4, 0.35,  # IV
                                 0.5, 0.1,  # V
                                 0.15, -0.4,  # VI-N0
                                 0.1, -0.7,  # P0-Na
                                 0.8, -0.7,  # Pa-Nb
                                 0.9, -2.0,  # P1-N1
                                 2.5, -1.0,  # P2-N2
                                 -0.2,
                                 0
                                 ])
    f = interpolate.interp1d(_peak_times, _peak_amplitudes, kind='linear', fill_value="extrapolate")
    _x = np.logspace(np.log10(time[1].value), np.log10(time[-1].value), num=75, endpoint=False)
    _y = f(_x)
    f2 = interpolate.interp1d(_x, _y, kind='quadratic', fill_value="extrapolate")
    ynew = f2(time).reshape(-1, 1) * u.uV
    # plt.plot(_x, _y)
    # plt.plot(_peak_times, _peak_amplitudes, 'o')
    # plt.plot(time, ynew)
    # plt.show()
    # demean wafeform
    ynew = ynew - np.mean(ynew, axis=0)
    return ynew, time


def eog(fs=16384.0 * u.Hz,
        thau1: u.quantity.Quantity = 0.05 * u.s,
        thau2: u.quantity.Quantity = 0.01 * u.s,
        peak_amp: u.quantity.Quantity = 100 * u.uV,
        event_duration: u.quantity.Quantity = 1.0 * u.s):
    """
    This function generates a typical eye blink waveform with an amplitude of 300 uV
    :param fs: sampling rate of the generated waveform (samples per seconds)
    :return: waveform and time vector
    """
    fs = set_default_unit(fs, u.Hz)
    thau1 = set_default_unit(thau1, u.s)
    thau2 = set_default_unit(thau2, u.s)
    peak_amp = set_default_unit(peak_amp, u.uV)
    event_duration = set_default_unit(event_duration, u.s)
    event_time = np.arange(0, event_duration * fs) / fs
    # event = windows.flattop(event_time.size) + windows.general_gaussian(event_time.size, p=1.5, sig=5000)
    event = (np.exp(-event_time/thau1) - np.exp(-event_time/thau2))
    y_new = np.zeros(event_time.shape)
    y_new[0:event_time.size] = event
    # apply rise-fade window
    fade_in_out = np.ones(y_new.shape)
    fade_len = np.round(event_time.size // 20)
    fade_in_out[0: fade_len] = (np.sin(2 * np.pi * (1 / (4 * fade_len / fs)) *
                                       event_time[0: fade_len] * u.rad) ** 2)
    fade_in_out[-fade_len:] = (np.sin(2 * np.pi * (1 / (4 * fade_len / fs)) *
                                      event_time[0: fade_len] * u.rad + np.pi * u.rad / 2) ** 2)
    y_new = y_new * fade_in_out * u.uV
    y_new *= peak_amp / np.abs(y_new).max()

    return y_new.reshape(-1, 1), event_time


def fade_in_out_window(n_samples: int = None, fraction=0.1):
    """
    This function will generate a fade window with a fade_in and fade_out length as a propoertion of the number of
    samples
    :param n_samples: length of the window
    :param fraction: percentage of fade in and out length
    :return:
    """
    # apply rise-fade window
    fade_in_out = np.ones([n_samples, 1])
    fade_len = int(np.round(n_samples * fraction))
    fade_in_out[0: fade_len, 0] = (np.sin(2 * np.pi * (np.arange(fade_len) * u.rad / (4 * fade_len))) ** 2)
    fade_in_out[-fade_len:, 0] = (np.sin(2 * np.pi * (np.arange(fade_len) * u.rad / (4 * fade_len))
                                         + np.pi * u.rad / 2) ** 2)
    return fade_in_out


def artifact_and_brain_envelope(fs: u.Quantity = 16384.0 * u.Hz,  # sampling rate
                                stimulus_delay: u.Quantity = 0.0 * u.s,  # brainstem delay
                                brain_delay: u.Quantity = 113 * u.ms,  # brainstem delay
                                duration: u.Quantity = 1 * u.s,  # seconds
                                seed=None,  # random generator seed
                                leak_amplitude: u.Quantity = 20.0 * u.uV,
                                brain_amplitude: u.Quantity = 0.2 * u.uV
                                ):
    """
    This function will generate an envelope response (as it was from the brain) evoked by an external stimulus.
    :param fs: sampling rate
    :param stimulus_delay: physical delay between the presented waveform and the output of the device (this simulates
    a delay between the waveform and the transducer)
    :param brain_delay: delay of the envelope response being followed by the brain (this delay emulates a neural source
    responding later in time to the stimulus)
    :param duration: length of the envelope response
    :param seed: defines the seed for the noise generator (this allows to reproduce the same stimulus every time)
    :param leak_amplitude: the amplitude of the leaked waveform
    :param brain_amplitude: the amplitude of the brain response
    :return: brain_waveform (the target neural response),
    stimulus_waveform (the presented waveform),
    leaked_stimulus (the recorded artefact in an EEG system; this is, the stimulus_waveform with delay and filter
    applied)
    """
    fs = set_default_unit(fs, u.Hz)
    duration = set_default_unit(duration, u.s)
    stimulus_delay = set_default_unit(stimulus_delay, u.s)
    brain_delay = set_default_unit(brain_delay, u.s)
    leak_amplitude = set_default_unit(leak_amplitude, u.uV)
    brain_amplitude = set_default_unit(brain_amplitude, u.uV)

    time = np.arange(0, duration.to(u.s).value, 1 / fs.to(u.Hz).value).reshape(-1, 1) * u.s

    # define stimulation waveform
    if seed is not None:
        np.random.seed(seed)
    stimulus_waveform = np.random.randn(time.size, 1) * u.dimensionless_unscaled
    stimulus_waveform = stimulus_waveform / np.abs(stimulus_waveform).max()

    # apply rise-fade window
    fade_in_out = np.ones(stimulus_waveform.shape)
    fade_len = round(time.size // 20)
    fade_in_out[0: fade_len] = np.sin(2 * np.pi * u.rad * (1 / (4 * fade_len / fs)) * time[0: fade_len]) ** 2
    fade_in_out[-fade_len:] = np.sin(2 * np.pi * u.rad * (1 / (4 * fade_len / fs)) *
                                     time[0: fade_len] + np.pi * u.rad / 2) ** 2
    stimulus_waveform = stimulus_waveform * fade_in_out

    # brain response follows signal envelop with a delay
    template_waveform = np.abs(hilbert(stimulus_waveform)) * stimulus_waveform.unit
    _b_brain = bandpass_fir_win(high_pass=2 * u.Hz,
                                low_pass=80.0 * u.Hz,
                                fs=fs)
    # rectify  brain response
    template_waveform[template_waveform < 0] = 0

    # filter brain response
    template_waveform = ols_filt_filt(b=_b_brain, x=template_waveform)
    template_waveform = template_waveform * fade_in_out

    # pad zeros to add stimulus and neural delay
    template_waveform = np.pad(template_waveform, ((int(fs * stimulus_delay) + int(fs * brain_delay), 0), (0, 0)),
                               'constant', constant_values=(0, 0))
    template_waveform = template_waveform / np.abs(template_waveform).max()

    # apply delay to leaked stimulus (assuming system delay)
    leaked_stimulus = np.pad(stimulus_waveform, ((int(fs * stimulus_delay), int(fs * brain_delay)),
                                                 (0, 0)), 'constant', constant_values=(0, 0))
    # pad with zeros stimulus_waveform to output all data with same length
    stimulus_waveform = np.pad(stimulus_waveform, ((0, int(fs * stimulus_delay) + int(fs * brain_delay)),
                                                   (0, 0)), 'constant', constant_values=(0, 0))

    # leaked artifact
    _b = bandpass_fir_win(None, 1000 * u.Hz, fs=fs, ripple_db=60)
    leaked_stimulus = ols_filt_filt(b=_b, x=leaked_stimulus)

    # scale respective signals
    brain_waveform = template_waveform * brain_amplitude
    leaked_stimulus = leaked_stimulus * leak_amplitude
    return brain_waveform, stimulus_waveform, leaked_stimulus


def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


def abr(fs: u.quantity.Quantity = 16384.0 * u.Hz,
        time_length: u.quantity.Quantity = 1.0 * u.s,
        peaks_amplitudes: np.ndarray = np.array([0.1, 0.07, 0.2, 0.05, 0.5]) * u.uV):
    """
    This function generates a typical abr waveform
    :param fs: sampling rate of the generated waveform (samples per seconds)
    :param time_length: desired time of the output
    :param peaks_amplitudes: array with amplitudes for waves i, ii, iii, iv, and v
    :return: waveform and time vector
    """
    fs = set_default_unit(fs, u.Hz)
    time_length = set_default_unit(time_length, u.s)
    peaks_amplitudes = set_default_unit(peaks_amplitudes, u.uV)

    time = np.arange(0, time_length * fs) / fs
    _template_time = np.arange(0, 0.01 * u.s * fs) / fs
    wave_i = np.concatenate(([0], np.diff(gaussian(_template_time, 0.002 * u.s, 0.0001 * u.s)))) + 0.1 * gaussian(
        _template_time, 0.002 * u.s, 0.0001 * u.s)
    wave_ii = np.concatenate(([0], np.diff(gaussian(_template_time, 0.003 * u.s, 0.00015 * u.s)))) + 0.1 * gaussian(
        _template_time, 0.003 * u.s, 0.0001 * u.s)
    wave_iii = 2 * np.concatenate(([0], np.diff(gaussian(_template_time, 0.004 * u.s, 0.00015 * u.s)))) + 1 * gaussian(
        _template_time, 0.004 * u.s, 0.0001 * u.s)
    wave_iv = np.concatenate(([0], np.diff(gaussian(_template_time, 0.005 * u.s, 0.0001 * u.s)))) + gaussian(
        _template_time, 0.005 * u.s, 0.0001 * u.s)
    wave_v = 2 * np.concatenate(([0], np.diff(gaussian(_template_time, 0.006 * u.s, 0.001 * u.s)))) + .5 * gaussian(
        _template_time, 0.006 * u.s, 0.00038 * u.s)
    # normalize and scale peaks
    wave_i *= peaks_amplitudes[0] / wave_i.max()
    wave_ii *= peaks_amplitudes[1] / wave_ii.max()
    wave_iii *= peaks_amplitudes[2] / wave_iii.max()
    wave_iv *= peaks_amplitudes[3] / wave_iv.max()
    wave_v *= peaks_amplitudes[4] / wave_v.max()
    _abr = wave_i + wave_ii + wave_iii + wave_iv + wave_v
    f = interpolate.interp1d(_template_time, _abr, kind='linear', fill_value="extrapolate")
    ynew = f(time).reshape(-1, 1) * u.uV
    return ynew, time
