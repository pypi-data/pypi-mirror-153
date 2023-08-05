import numpy as np
from peegy.processing.tools import weightedAverage as averager, eeg_epoch_operators as eo
import peegy.processing.tools.filters.eegFiltering as eegf
from peegy.processing.tools.multiprocessing.multiprocessesing_filter import filt_data, filt_filt_data
from sklearn import linear_model
import matplotlib.pyplot as plt
import peegy.processing.tools.filters.spatial_filtering as sf
from peegy.processing.system.memory import enough_memory
import pyfftw
import multiprocessing
from scipy import signal
import pycwt as wavelet
import pywt as pw
from sklearn.linear_model import LinearRegression
from peegy.tools.units.unit_tools import set_default_unit
import astropy.units as u
from tqdm import tqdm

__author__ = 'jaime undurraga'


def et_get_epoch_weights_and_rn_weighted_average(epochs: np.array = np.array([]),
                                                 block_size: int = 5,
                                                 samples_distance: int = 10):
    """
    This function computes the weights and residual noise for weighted averaging.
    :param epochs: samples x channels x trials numpy array
    :param block_size: number of trials used to estimate noise and weights
    :param samples_distance: separation between samples to estimate noise and weights
    :return: weights, residual noise, cumulative residual noise over trials,
    array with number of sources per noise source

    """
    # compute weights for averaging an residual noise estimation
    block_size = np.minimum(epochs.shape[2], block_size)
    blocks = np.arange(0, epochs.shape[2] + 1, block_size).astype(np.int)
    _epochs = epochs[np.arange(0, epochs.shape[0], samples_distance), :, :]
    blocks[-1] = np.maximum(blocks[-1], _epochs.shape[2])
    unfolded_epochs = eo.et_unfold(np.transpose(_epochs, [0, 2, 1]), ortogonal=True)
    var = np.var(unfolded_epochs[:, blocks[0]: blocks[1]], axis=1)
    # var2 = np.expand_dims(np.mean(np.var(_epochs[:, :, blocks[0]: blocks[1]], axis=2), axis=0), axis=1)
    for i in range(1, len(blocks) - 1):
        var = np.vstack((var, np.var(unfolded_epochs[:, blocks[i]: blocks[i+1]], axis=1)))
    var = var[None, :]
    wb = 1.0 / np.mean(eo.et_fold(var.T, _epochs.shape[1]), axis=2)

    if np.all(wb == np.inf):
        wb[:] = 1
    nk = np.diff(blocks)
    w = np.ones((_epochs.shape[1], nk[0])) * np.expand_dims(wb[:, 0], 1)
    for i, n in enumerate(nk[1:]):
        w = np.concatenate((w, np.ones(n) * np.expand_dims(wb[:, i + 1], 1)), axis=1)
    rn = np.sqrt(1.0 / np.sum(w, axis=1))
    cumulative_rn = None
    for _i in range(wb.shape[1]):
        if _i == 0:
            cumulative_rn = np.sqrt(1.0 / np.sum(nk[0:_i + 1] * wb[:, 0:_i + 1], axis=1))
        else:
            cumulative_rn = np.vstack((cumulative_rn, np.sqrt(1.0 / np.sum(nk[0:_i+1] * wb[:, 0:_i + 1], axis=1))))
    n_total = np.sum(nk)
    return w, rn, cumulative_rn, n_total, wb, nk


def et_get_epoch_weights_and_rn_standard_average(epochs: np.array = np.array([]),
                                                 block_size: int = 5,
                                                 samples_distance: int = 10):
    """
    This function computes the weights and residual noise for standard averaging.
    :param epochs: samples x channels x trials numpy array
    :param block_size: number of trials used to estimate noise and weights
    :param samples_distance: separation between samples to estimate noise and weights
    :return: weights, residual noise, cumulative residual noise over trials,
    array with number of sources per noise source
    """
    # compute weights for averaging an residual noise estimation
    block_size = np.minimum(epochs.shape[2], block_size)
    blocks = np.arange(0, epochs.shape[2] + 1, block_size).astype(np.int)
    _epochs = epochs[np.arange(0, epochs.shape[0], samples_distance), :, :]
    blocks[-1] = np.maximum(blocks[-1], _epochs.shape[2])
    unfolded_epochs = eo.et_unfold(np.transpose(_epochs, [0, 2, 1]), ortogonal=True)
    var = np.var(unfolded_epochs[:, blocks[0]: blocks[1]], axis=1)[None, :]
    for i in range(1, len(blocks) - 1):
        var = np.vstack((var, np.var(unfolded_epochs[:, blocks[i]: blocks[i + 1]], axis=1)))
    nb_var = np.mean(eo.et_fold(var.T, _epochs.shape[1]), axis=2)
    wb = np.ones((_epochs.shape[1], var.shape[0]))
    nk = np.diff(blocks)
    w = np.ones((_epochs.shape[1], nk[0])) * np.expand_dims(wb[:, 0], 1) * u.dimensionless_unscaled
    for i, n in enumerate(nk[1:]):
        w = np.concatenate((w, np.ones(n) * np.expand_dims(wb[:, i + 1], 1)), axis=1)
    rn = np.sqrt(np.sum(nk * nb_var, axis=1) / (np.sum(nk) ** 2.0))
    cumulative_rn = None
    for _i in range(nb_var.shape[1]):
        _cum_rn = np.sqrt(np.sum(nk[0:_i + 1] * nb_var[:, 0:_i + 1], axis=1) / (np.sum(nk[0:_i + 1]) ** 2.0))
        if _i == 0:
            cumulative_rn = _cum_rn
        else:
            cumulative_rn = np.vstack((cumulative_rn, _cum_rn))
    n_epochs = np.sum(nk)
    return w, rn, cumulative_rn, n_epochs, wb, nk


def et_mean(epochs: np.array = np.array([]),
            block_size: int = 5,
            samples_distance: int = 10,
            weighted: bool = True,
            normalize_weights: bool = False):
    """
    Compute the mean of the input epochs
    :param epochs: samples x channels x trials numpy array
    :param block_size: number of trials used to estimate noise and weights
    :param samples_distance: separation between samples to estimate noise and weights
    :param weighted: boolean indicating if weighted average is used
    :param normalize_weights: if true weights will be normalized so that their sum across x is equal to 1
    :return: average data (standard or weighted), weights, residual noise, cumulative residual noise over trials,
    spectrum of final average scaled to time domain amplitudes, array with number of sources per noise source
    """

    if weighted:
        w, final_rn, cumulative_rn, n, wb, nb = et_get_epoch_weights_and_rn_weighted_average(epochs,
                                                                                             block_size,
                                                                                             samples_distance)
    else:
        w, final_rn, cumulative_rn, n, wb, nb = et_get_epoch_weights_and_rn_standard_average(epochs,
                                                                                             block_size,
                                                                                             samples_distance)
    # normalize weights to facilitate computations
    if normalize_weights:
        w = w / np.sum(w, axis=1)[:, None]
    w = np.tile(w, (epochs.shape[0], 1, 1))
    w_ave = eo.w_mean(epochs, w)
    fft = pyfftw.builders.rfft(w_ave, overwrite_input=False, planner_effort='FFTW_ESTIMATE', axis=0,
                               threads=multiprocessing.cpu_count())
    w_fft = fft()
    w_fft /= w_fft.shape[0]
    return w_ave, w, final_rn, cumulative_rn, w_fft, n, wb, nb


def et_snr_in_rois(data: np.array = None,
                   roi_windows: np.array = None,
                   rn: [np.array] = None):
    data_in_windows = get_in_window_data(data=data, roi_windows=roi_windows)
    if rn is None:
        rn = [np.array([])]
    final_snr = np.zeros((data.shape[1], len(data_in_windows)))
    final_s_var = np.zeros((data.shape[1], len(data_in_windows)))
    snr = np.zeros((data.shape[1]))

    for _i, _data in enumerate(data_in_windows):
        s_var = np.var(_data, axis=0).reshape(-1, )
        _noise_var = rn ** 2.0
        _idx_valid = _noise_var != 0
        snr[_idx_valid] = np.maximum(s_var[_idx_valid] / _noise_var[_idx_valid] - 1.0, 0)
        _idx_invalid = _noise_var == 0
        snr[_idx_invalid] = np.inf * u.dimensionless_unscaled
        final_snr[:, _i] = snr
        final_s_var[:, _i] = s_var
    return final_snr, final_s_var


def get_in_window_data(data: np.array = np.array([]),
                       roi_windows: [np.array] = None):
    if roi_windows is None:
        snr_sample_windows = [np.array([0, data.shape[0]])]
    else:
        snr_sample_windows = roi_windows
    data_snr = []
    samples = []
    data = np.atleast_3d(data)
    for _i, _roi in enumerate(snr_sample_windows):
        _ini = np.maximum(_roi[0], 0)
        _end = np.minimum(_roi[1], data.shape[0])
        data_snr.append(data[_ini:_end, :, :])
        samples.append(np.array([_ini, _end]))
    return data_snr


def et_snr_weighted_mean(averaged_epochs: np.array = np.array([]),
                         rn: np.array = np.array([]),
                         snr: np.array = np.array([]),
                         roi_windows: [np.array] = None,
                         n_ch: int = None,
                         channel_idx: np.array = np.array([])):
    if not channel_idx.size:
        if n_ch is None:
            _v = np.arange(averaged_epochs.shape[1])
        else:
            _v = np.argsort(snr)[::-1][0:n_ch]
    else:
        _v = channel_idx
    _snr = snr
    if not np.any(snr):
        _snr = np.ones(snr.shape)
    w_ave = np.sum(averaged_epochs[:, _v] * _snr[_v].T, axis=1) / sum(_snr[_v])
    total_noise_var = rn[_v] ** 2.0
    w_total_noise_var = 1.0 / sum(1./total_noise_var)
    total_rn = w_total_noise_var ** 0.5
    total_snr, _signal_var = et_snr_in_rois(data=np.expand_dims(w_ave, 1), roi_windows=roi_windows, rn=total_rn)
    return np.expand_dims(w_ave, axis=1), total_rn, total_snr, _signal_var


def et_frequency_mean(epochs=np.array([]), fs=None,
                      samples_distance=10,
                      n_fft=None,
                      snr_time_window=np.array([]),
                      block_size=5,
                      test_frequencies=None,
                      scale_frequency_data=True,
                      weighted_average=True):
    j_ave = averager.JAverager()
    j_ave.splits = epochs.shape[1]
    j_ave.fs = fs
    j_ave.t_p_snr = np.arange(0, epochs.shape[0], epochs.shape[0] / samples_distance) / fs
    j_ave.analysis_window = snr_time_window
    j_ave.time_offset = 0.0
    j_ave.alpha_level = 0.05
    j_ave.min_block_size = block_size
    j_ave.plot_sweeps = False
    j_ave.frequencies_to_analyze = test_frequencies
    j_ave.n_fft = n_fft

    _n_sweep = 0
    _total_sweeps = epochs.shape[1] * epochs.shape[2]
    for i in range(epochs.shape[2]):
        for j in range(epochs.shape[1]):
            j_ave.add_sweep(epochs[:, j, i])
            _n_sweep += 1
            print(('averaged %i out of %i sweeps' % (_n_sweep, _total_sweeps)))
    if weighted_average:
        w_ave = j_ave.w_average
        w_fft = j_ave.w_fft
        rn = j_ave.w_rn
        snr = j_ave.w_snr
        s_var = j_ave.w_signal_variance
    else:
        w_ave = j_ave.s_average
        w_fft = j_ave.s_fft
        rn = j_ave.s_rn
        snr = j_ave.s_snr
        s_var = j_ave.s_signal_variance

    _h_test = j_ave.hotelling_t_square_test()
    if scale_frequency_data:
        n_samples = epochs.shape[0]
        n_fft = n_samples if n_fft is None else n_fft
        factor = 2 / np.minimum(n_samples, n_fft)
        w_fft = w_fft * factor
        for ch_tests in _h_test:
            for _s_test in ch_tests:
                _s_test.spectral_magnitude *= factor
                _s_test.rn *= factor
    return w_ave, rn, [snr], w_fft, _h_test, [s_var]


def et_frequency_wights(epochs=np.array([]), fs=None,
                        samples_distance=10,
                        n_fft=None,
                        snr_time_window=np.array([]),
                        block_size=5,
                        test_frequencies=None,
                        scale_frequency_data=True,
                        weighted_average=True):
    j_ave = averager.JAverager()
    j_ave.splits = epochs.shape[1]
    j_ave.fs = fs
    j_ave.t_p_snr = np.arange(0, epochs.shape[0], epochs.shape[0] / samples_distance) / fs
    j_ave.analysis_window = snr_time_window
    j_ave.time_offset = 0.0
    j_ave.alpha_level = 0.05
    j_ave.min_block_size = block_size
    j_ave.plot_sweeps = False
    j_ave.frequencies_to_analyze = test_frequencies
    j_ave.n_fft = n_fft

    _n_sweep = 0
    _total_sweeps = epochs.shape[1] * epochs.shape[2]
    for i in range(epochs.shape[2]):
        for j in range(epochs.shape[1]):
            j_ave.add_sweep(epochs[:, j, i])
            _n_sweep += 1
            print(('averaged %i out of %i sweeps' % (_n_sweep, _total_sweeps)))
    if weighted_average:
        w_ave = j_ave.w_average
        w_fft = j_ave.w_fft
        rn = j_ave.w_rn
        snr = j_ave.w_snr
        s_var = j_ave.w_signal_variance
    else:
        w_ave = j_ave.s_average
        w_fft = j_ave.s_fft
        rn = j_ave.s_rn
        snr = j_ave.s_snr
        s_var = j_ave.s_signal_variance

    _h_test = j_ave.hotelling_t_square_test()
    if scale_frequency_data:
        n_samples = epochs.shape[0]
        n_fft = n_samples if n_fft is None else n_fft
        factor = 2 / np.minimum(n_samples, n_fft)
        w_fft = w_fft * factor
        for ch_tests in _h_test:
            for _s_test in ch_tests:
                _s_test.spectral_magnitude *= factor
                _s_test.rn *= factor
    return w_ave, rn, [snr], w_fft, _h_test, [s_var]


def et_frequency_mean2(epochs=np.array([]),
                       fs: u.Quantity = None,
                       block_size: int = 10,
                       test_frequencies: np.array = None,
                       scale_frequency_data: bool = True,
                       weighted_average: bool = True,
                       delta_frequency: u.Quantity = 2 * u.Hz,
                       power_line_frequency: u.Quantity = 50 * u.Hz):
    epochs = set_default_unit(epochs, u.uV)
    fs = set_default_unit(fs, u.Hz)
    delta_frequency = set_default_unit(delta_frequency, u.Hz)
    test_frequencies = set_default_unit(test_frequencies, u.Hz)

    weights, pooled_rn, pooled_snr, by_freq_rn, by_freq_snr, freq_samples, exact_frequencies = \
        get_pooled_frequency_weights(
            epochs=epochs,
            fs=fs,
            block_size=block_size,
            frequencies=test_frequencies,
            weighted_average=weighted_average,
            delta_frequency=delta_frequency,
            power_line_frequency=power_line_frequency,
        )

    w_ave = eo.w_mean(epochs=epochs,
                      weights=weights[0, :, :])

    fft = pyfftw.builders.rfft(w_ave, overwrite_input=False, planner_effort='FFTW_ESTIMATE', axis=0,
                               threads=multiprocessing.cpu_count())
    scaling_factor = 1.0
    if scale_frequency_data:
        scaling_factor = 2 / epochs.shape[0]

    w_fft = fft() * scaling_factor * w_ave.unit
    freq_samples = scaling_factor * freq_samples
    pooled_rn = scaling_factor * pooled_rn
    return w_ave, pooled_snr, pooled_rn, by_freq_snr, by_freq_snr, w_fft, weights, freq_samples, exact_frequencies


def et_subtract_correlated_ref(data: np.array = np.array([]),
                               idx_ref: np.array = np.array([]),
                               high_pass: float = 0.1,
                               low_pass: float = 20.0,
                               plot_results=False,
                               fs: float = 1.0,
                               figure_path: str = '',
                               figure_basename: str = ''):
    data = np.atleast_3d(data)
    origin_data = data.copy()
    fig = None
    # filter
    _b_h, _b_l = None, None
    if high_pass is not None:
        _b_h = eegf.bandpass_fir_win(high_pass=high_pass, low_pass=None, fs=fs)
    if low_pass is not None:
        _b_l = eegf.bandpass_fir_win(high_pass=None, low_pass=low_pass, fs=fs)
    for _trial in np.arange(data.shape[2]):
        reg = linear_model.LinearRegression()
        x = np.arange(0, data.shape[0])[:, None]
        reg.fit(x, data[:, :, _trial])
        data[:, :, _trial] = data[:, :, _trial] - reg.predict(x)
        temp_data = data[:, :, _trial]
        if high_pass is not None:
            temp_data = filt_filt_data(input_data=data[:, :, _trial], b=_b_h)
        if low_pass is not None:
            temp_data = filt_filt_data(input_data=temp_data, b=_b_l)
        ref = temp_data[:, idx_ref]
        for _idx in np.arange(ref.shape[1]):
            _current_ref = ref[:, _idx]
            transmission_index = temp_data.T.dot(_current_ref) / np.expand_dims(
                np.sum(np.square(_current_ref)), axis=0)
            data[:, :, _trial] -= _current_ref[:, None].dot(transmission_index[None, :])
            temp_data -= _current_ref[:, None].dot(transmission_index[None, :])
    if plot_results:
        time = np.arange(0, data.shape[0]) / fs
        fig = plt.figure()
        ax = fig.add_subplot(121)
        ax.plot(time, origin_data[:, 0, :].squeeze())
        ax.set_title('original')
        ax.legend(loc="upper right")
        ax = fig.add_subplot(122, sharey=ax)
        ax.plot(time, data[:, 0, :].squeeze())
        ax.set_title('eog removed')
        ax.legend(loc="upper right")
        fig.savefig(figure_path + figure_basename + '.png')
    return data, fig


def rms(x: np.array = None):
    return np.sqrt(np.mean(x ** 2.0))


def crest_factor(x: np.array = None):
    return 20.0 * np.log10(np.max(np.abs(x)) / rms(x))


def unitary_step(x: np.array = None):
    return (x > 0).astype(np.float)


def clean_peaks(peaks_amp: np.array = None,
                peaks_pos: np.array = None,
                minimum_width_samples: int = None):
    assert peaks_amp.size == peaks_pos.size
    _idx_diff, = np.where(np.append(0, np.diff(peaks_pos)) > minimum_width_samples)
    plt.plot(peaks_pos, peaks_amp)


def et_subtract_oeg_template(data: np.array = np.array([]),
                             fs: u.Quantity = None,
                             idx_ref: np.array = np.array([]),
                             high_pass: u.Quantity = 0.1 * u.Hz,
                             low_pass: u.Quantity = 20 * u.Hz,
                             template_width: u.Quantity = 0.5 * u.s,
                             crest_factor_threshold=10,
                             plot_results=False,
                             figure_path: str = '',
                             figure_basename: str = '',
                             minimum_interval_width: u.Quantity = 0.075 * u.s,
                             eog_peak_width: u.Quantity = 0.02 * u.s):
    # # removal of the eye artefacts via a template subtraction method
    # # described in Valderrama et al, 2018.The algorithm performs three steps:
    # # 1) Blinks are detected in each channel using a (generic) eye artefact template.
    # # The template is iteratively adjusted after each newly detected eye blink, to more closely match
    # # the individual subject one.
    # # 2) A signal is generated, which used the individual template to represent all detected eyeblinks,
    # # depending on the amplitudes and timepoints of each individual eyeblink.
    # # 3) The signal from step two is subtracted from the raw EEG signal, thus leading to an enhanced
    # # EEG signal, where eyeblinks do not lead to dropping of the affected epochs.
    # # Literature:
    # # Valderrama, J. T., de la Torre, A., & Van Dun, B. (2018). An automatic algorithm for blink-artifact suppression
    # # based on iterative template matching: Application to single channel recording of cortical auditory evoked
    # potentials. Journal of Neural Engineering, 15(1), 016008. https://doi.org/10.1088/1741-2552/aa8d95
    fig = None
    # demean data before filtering to minimize ringing of filter
    reg = linear_model.LinearRegression()
    x = np.arange(0, data.shape[0])[:, None]
    reg.fit(x, data)
    data = data - reg.predict(x) * data.unit
    # filter data
    if high_pass is not None:
        _b = eegf.bandpass_fir_win(high_pass=high_pass, low_pass=None, fs=fs)
        data = filt_filt_data(input_data=data, b=_b)

    # low pass eye artifacts
    ref = data[:, idx_ref]
    if low_pass is not None:
        _b = eegf.bandpass_fir_win(high_pass=None, low_pass=low_pass, fs=fs)
        ref = filt_filt_data(input_data=ref, b=_b)

    # find propagation coefficients and subtract artifacts
    for _idx_eog_ch in range(ref.shape[1]):
        _current_eog = ref[:, _idx_eog_ch].flatten()
        _rms = rms(_current_eog)
        # we check if positive or negative dominated waveform by looking the number of events with crest factors
        # larger than crest_factor_threshold in dB
        _amp_threshold = 10 ** (crest_factor_threshold / 20) * _rms
        positive_peaks, _ = signal.find_peaks(_current_eog * unitary_step(_current_eog - _amp_threshold),
                                              prominence=_amp_threshold.to_value(data.unit),
                                              distance=int(fs * minimum_interval_width),
                                              width=int(fs * eog_peak_width))
        negative_peaks, _ = signal.find_peaks(-_current_eog.value * unitary_step(-_current_eog - _amp_threshold),
                                              prominence=_amp_threshold.to_value(data.unit),
                                              distance=int(fs * minimum_interval_width),
                                              width=int(fs * eog_peak_width))
        _invert_waveform = False
        if positive_peaks.size and negative_peaks.size:
            _invert_waveform = positive_peaks.size < negative_peaks.size
        elif positive_peaks.size:
            _invert_waveform = False
        elif negative_peaks.size:
            _invert_waveform = True

        if _invert_waveform:
            _current_eog *= -1

        _idx_peak, _ = signal.find_peaks(_current_eog * unitary_step(_current_eog - _amp_threshold),
                                         distance=int(fs * minimum_interval_width),
                                         prominence=_amp_threshold.to_value(data.unit),
                                         width=int(eog_peak_width * fs))
        if _idx_peak.size:
            _peaks = _current_eog[_idx_peak]
            n_events = _peaks.size
            _sorted_amp_idx = np.argsort(_peaks)
            _event_weighs = np.array([1])
            # weights are updated only if more than one event is found
            if n_events > 1:
                _ranks = np.arange(0, n_events)
                _event_weighs = 0.54 - 0.46 * np.cos(4 * np.pi * (_ranks - 0.25 * n_events) / (n_events - 1))
                _event_weighs = _event_weighs * np.logical_and(_ranks > 0.25 * n_events, _ranks < 0.75 * n_events)
            # sort peaks
            _idx_peak = _idx_peak[_sorted_amp_idx]
            _peaks = _peaks[_sorted_amp_idx]
            template_samples = int(fs*template_width)
            template = np.zeros((template_samples, 1)) * data.unit
            reconstructed = np.zeros(data.shape) * data.unit
            if n_events > 0:
                for _i, _peak in enumerate(_idx_peak):
                    _ini = _peak - template_samples // 2
                    _end = _ini + template_samples
                    if _ini < 0:
                        template[-_ini::, 0] += _current_eog[0: _end] * _event_weighs[_i]
                    elif _end > data.shape[0]:
                        template[0:-(_end - data.shape[0]):, 0] += _current_eog[_ini::] * _event_weighs[_i]
                    else:
                        template[:, 0] += _current_eog[_ini: _end] * _event_weighs[_i]
                # normalize
                template = template * template.unit / np.abs(template).max()
                # apply window to have smooth onset and offset
                _window = np.ones((template.size, 1))
                nw = _window.size // 8
                _window[0: nw] = np.sin(np.pi / (2 * nw) * np.arange(0, nw)).reshape(-1, 1)
                _window[_window.size - nw::] = _window[0: nw][::-1]
                template *= _window
                # we recreate a peak template
                convolution_matrix = np.zeros(data.shape)
                for _i, _peak in enumerate(_idx_peak):
                    _current_template = template
                    _ini = _peak - template_samples // 2
                    _end = _ini + template_samples
                    if _ini < 0:
                        _current_template = template[-_ini::, :]
                    if _end > data.shape[0]:
                        _current_template = template[0:-(_end - data.shape[0]), :]
                    _ini = _peak - template_samples // 2
                    _end = _ini + template_samples
                    _ini = max(_ini, 0)
                    _end = min(_end, data.shape[0])

                    original = data[_ini: _end, :]
                    transmission_index = original.T.dot(_current_template) / np.expand_dims(
                        np.sum(np.square(_current_template)), axis=0)

                    # generate unitary dirac impulses
                    convolution_matrix[_ini, :] = transmission_index.reshape(-1, )

                # convolve source with dirac train to generate blinks signal
                for _ch_idx in tqdm(np.arange(0, convolution_matrix.shape[1]), desc='Reconstructing EOG artefacts'):
                    reconstructed[:, _ch_idx] = filt_data(
                        input_data=template,
                        b=convolution_matrix[:, _ch_idx].reshape(-1, 1).flatten(),
                        mode='full', onset_padding=False)[0: data.shape[0]].flatten()
            data -= reconstructed
            if plot_results:
                time = np.arange(0, data.shape[0]) / fs
                time_template = (np.arange(0, template.shape[0]) - template_samples / 2) / fs
                fig = plt.figure()
                # ax = fig.add_subplot(321)
                # ax.plot(_edges, _hist, label='histogram')
                # ax.plot(_edges, smoothed_kernel, label='smooth  histogram')
                # ax.plot(_edges[_idx_threshold], smoothed_kernel[_idx_threshold], 'o', label='threshold')
                # ax.legend(loc="upper right")
                ax = fig.add_subplot(221)
                ax.plot(time, _current_eog, label='reference eog')
                ax.plot(time[_idx_peak], _peaks, 'o', label='detected events')
                ax.legend(loc="upper right")
                ax = fig.add_subplot(222)
                ax.plot(time_template, template, label='fitted template')
                ax.legend(loc="upper right")
                ax = fig.add_subplot(223)
                ax.plot(time, _current_eog, label='reference eog')
                ax.plot(time, reconstructed[:, idx_ref[_idx_eog_ch]] * (-1) ** _invert_waveform,
                        label='reconstructed eog')
                ax.legend(loc="upper right")
                ax = fig.add_subplot(224)
                ax.plot(time, _current_eog, label='reference eog')
                ax.plot(time, data[:, idx_ref[_idx_eog_ch]] * (-1) ** _invert_waveform, label='eog removed')
                ax.legend(loc="upper right")
                fig.savefig(figure_path + figure_basename + 'eog_ref_{:}.png'.format(_idx_eog_ch))
    return data, fig


def et_get_spatial_filtering(epochs: np.array = np.array([]),
                             fs: u.Quantity = None,
                             sf_join_frequencies: np.array = None,
                             weight_data=True,
                             weights: np.array = None,
                             demean_data: bool = True,
                             keep0: int = None,
                             keep1: float = 1e-9,
                             perc0: float = .99,
                             perc1: float = None,
                             block_size: int = 10,
                             delta_frequency: u.Quantity = 5 * u.Hz
                             ):
    """

    :param epochs: m x n x l (samples, channels, epochs)
    :param fs: sampling rate
    :param sf_join_frequencies: numpy array with frequencies to bias the filter
    :param weight_data: if True, covariance and mean will be estimated using weights
    :param weights: array of weights to use when weighted_average is true. If none and weighted_average is true,
    these will be estimated.
    :param demean_data: if True, data will be demeaned prior weights estimation.
    :param keep0: integer controlling  whitening of unbiased components in DSS. This integer value represent the number
    of components to keep.
    :param keep1: float controlling  whitening of unbiased components in DSS. This value will remove components below
    keep1 which is relative to the maximum eigen value.
    :param perc0: float (between 0 and 1) controlling whitening of unbiased components in DSS.
    This value will preserve components that explain the percentage of variance.
    :param perc1: float (between 0 and 1) controlling the number of biased components kept in DSS.
    This value will preserve the components of the biased PCA analysis that explain the percentage of variance.
    :param block_size: integer indicating the number of trials that would be use to estimate the weights
    :param delta_frequency: frequency size around each sf_join_frequency to estimate noise
    :return: z, pwr0, pwr1, cov_1, weights: components, unbiased power, biased power, covariance rotation,
    estimated weights
    """
    print('computing spatial filter')

    # bias function uses weighted mean or standard mean
    if weight_data and weights is None:
        if sf_join_frequencies is None:
            _, weights, *_ = et_mean(epochs,
                                     weighted=weight_data,
                                     block_size=block_size)
        else:
            weights, *_ = get_pooled_frequency_weights(
                epochs=epochs,
                fs=fs,
                frequencies=sf_join_frequencies,
                weighted_average=weight_data,
                block_size=block_size,
                delta_frequency=delta_frequency,
            )

    if weights is None:
        weights = np.ones(epochs.shape) * u.dimensionless_unscaled
    if demean_data:
        epochs = eo.et_demean(epochs, w=weights, eps=np.finfo(float).eps * weights.unit)

    average = eo.w_mean(epochs, weights=weights)

    if sf_join_frequencies is not None:
        n_frequencies = sf_join_frequencies / fs
        c0, t0 = eo.et_freq_weighted_cov(epochs, normalized_frequencies=n_frequencies, w=weights)
        c1, t1 = eo.et_freq_weighted_cov(average, normalized_frequencies=n_frequencies)
        c0 = c0 / t0
        c1 = c1 / t1
        todss, pwr0, pwr1 = sf.nt_dss0(c0, c1, keep0=keep0, keep1=keep1, perc0=perc0, perc1=perc1)
        z = eo.et_mmat(epochs, todss)
        cov_1, tw_cov = eo.et_freq_shifted_xcovariance(z, epochs, normalized_frequencies=n_frequencies, wy=weights)
        cov_1 = cov_1 / tw_cov
    else:
        # clean data using dss with weighted average as bias. Data covariance weighted with same weights
        c0, tw0 = eo.et_weighted_covariance(epochs, w=weights)
        c1, tw1 = eo.et_weighted_covariance(average)
        c0 = c0 / tw0
        c1 = c1 / tw1
        todss, pwr0, pwr1 = sf.nt_dss0(c0, c1, keep0=keep0, keep1=keep1, perc0=perc0, perc1=perc1)
        z = eo.et_mmat(epochs, todss)
        cov_1, tw_cov = eo.et_time_shifted_xcovariance(z, epochs, wy=weights)
        cov_1 = cov_1 / tw_cov

    return z, pwr0, pwr1, cov_1, weights


def et_apply_spatial_filtering(z=np.array([]),
                               pwr0=np.array([]),
                               pwr1=np.array([]),
                               cov_1=np.array([]),
                               sf_components=np.array([]),
                               sf_thr=0.8):
    print('applying spatial filter')
    max_num_components = z.shape[1]
    if sf_components is None or not sf_components.size:
        p_ratio = pwr1 / pwr0
        pos = np.maximum(np.where(np.cumsum(p_ratio)/np.sum(p_ratio) >= sf_thr)[0][0], 1)
        n_components = np.arange(pos)
    else:
        n_components = sf_components
    n_components = n_components[n_components < max_num_components]
    cleaned_data = eo.et_mmat(z[:, n_components, :], cov_1[n_components, :])
    return cleaned_data, n_components


def estimate_rn_from_trace(data=np.array([]), rn_ini_sample=0, rn_end_sample=-1, plot_estimation=False):
    x = np.expand_dims(np.arange(0, data[rn_ini_sample:rn_end_sample, :].shape[0]), axis=1)
    _subset = data[rn_ini_sample:rn_end_sample, :]
    regression = linear_model.LinearRegression()
    regression.fit(x, _subset)
    rn = np.std(_subset - regression.predict(x), axis=0)
    if plot_estimation:
        plt.plot(x, _subset)
        plt.plot(x, regression.predict(x))
        plt.title('rn regression, rn:' + str(rn))
        plt.show()

    return rn


def estimate_srn_from_trace(data=np.array([]), snr_ini_sample=0, snr_end_sample=-1, **kwargs):
    rn = estimate_rn_from_trace(data=data, **kwargs)
    _subset = data[snr_ini_sample:snr_end_sample, :]
    snr = np.var(_subset, axis=0) / rn ** 2.0 - 1
    return snr, rn


def eye_artifact_subtraction(epochs: np.array = np.array([]),
                             oeg_epochs: np.array = np.array([])):
    # subtract eye artifacts
    print('removing oeg artifacts')
    clean_data = et_subtract_correlated_ref(epochs=epochs, ref=oeg_epochs)
    return clean_data


def et_average_time_frequency_transformation(epochs: np.array = np.array([]),
                                             method='spectrogram',
                                             time_window=2.0,
                                             sample_interval=2.0,
                                             fs=0.0,
                                             average_mode='magnitude'):

    nfft = int(time_window * fs)
    noverlap = max(nfft - int(sample_interval * fs), 0)
    power, freqs, ave = None, None, None
    data = epochs
    if average_mode == 'complex':
        data = np.mean(epochs, 2, keepdims=True)

    for _i in range(data.shape[2]):
        if method == 'spectrogram':
            freqs, time, power = signal.spectrogram(data[:, :, _i],
                                                    window=signal.hamming(nfft),
                                                    fs=fs,
                                                    nfft=nfft,
                                                    noverlap=noverlap,
                                                    mode='complex',
                                                    scaling='spectrum',
                                                    axis=0)
            if average_mode == 'magnitude':
                power = np.abs(power)
        if method == 'wavelet':
            freq = np.arange(1, data.shape[0] + 1) * fs / data.shape[0]
            # mother = wavelet.Morlet(f0=2 * np.pi)
            # s0 = 2 / fs  # Starting scale
            # dj = 1 / 12.  # Twelve sub-octaves per octaves
            # J = 7 / dj  # Seven powers of two with dj sub-octaves
            [cfs, freqs] = pw.cwt(data[:, :, _i],
                                  scales=np.arange(1, 128),
                                  wavelet='cmor',
                                  sampling_period=1 / fs,
                                  axis=0)

            w = pw.ContinuousWavelet('cmor')
            w.bandwidth_frequency = 1.5
            w.center_frequency = 1
            [cfs, freqs] = pw.cwt(data,
                                  scales=np.arange(1, data.shape[0] / 2),
                                  wavelet=w,
                                  sampling_period=1 / fs)
            wave, scales, freqs, coi, fft, fftfreqs = wavelet.cwt(data,
                                                                  dt=1 / fs,
                                                                  freqs=freq)
            # power = (np.abs(wave)) ** 2
            # fft_power = np.abs(fft) ** 2
            # period = 1 / freqs
            power = np.abs(cfs)

        if _i == 0:
            ave = power
        else:
            ave += power
        print('Computing spectrogram {:} out of {:}'. format(_i, data.shape[2]))
    ave /= data.shape[2]
    return ave, time, freqs


def et_average_frequency_transformation(epochs: np.array = np.array([]),
                                        fs=0.0,
                                        ave_mode='magnitude'):

    fft = pyfftw.builders.rfft(epochs, overwrite_input=False, planner_effort='FFTW_ESTIMATE', axis=0,
                               threads=multiprocessing.cpu_count())
    _fft = fft()

    if ave_mode == 'magnitude':
        _fft = np.abs(_fft)
    ave = np.abs(np.mean(_fft, axis=2))
    ave *= 2/epochs.shape[0]
    freqs = np.arange(0, _fft.shape[0]) * fs / epochs.shape[0]
    return ave, freqs


def bootstrap(data: np.array = np.array([]), statistic=np.mean, num_samples=1000, alpha=0.05):
    """
    This function bootstrap incoming data using passed statistic function
    :param data: numpy array
    :param statistic: function that will be bootstrapped
    :param num_samples: number of estimations that will be used
    :param alpha: probabilistic level to compute confidence intervals
    :param axis: axis where statistic will be applied
    :return: bootstrap estimate of 100.0*(1-alpha) CI for statistic.
    """
    n = data.shape[2]
    idx = np.random.randint(0, n, (int(num_samples), n))
    unfolded_epochs = eo.et_unfold(np.transpose(data, [0, 2, 1]), ortogonal=True)
    new_data = np.zeros((unfolded_epochs.shape[0], num_samples))
    for _set in range(num_samples):
        samples = unfolded_epochs[:, idx[_set]]
        new_data[:, _set] = statistic(samples, axis=1)

    stat = np.sort(new_data, axis=1)
    mean = np.mean(stat, axis=1)
    ci_low, ci_hi = (stat[:, int((alpha / 2.0) * num_samples)], stat[:, int((1 - alpha / 2.0) * num_samples)])
    out_mean = np.reshape(mean, (data.shape[0], data.shape[1]), order='F')
    out_ci_low = np.reshape(ci_low, (data.shape[0], data.shape[1]), order='F')
    out_ci_hi = np.reshape(ci_hi, (data.shape[0], data.shape[1]), order='F')
    return out_mean, out_ci_low, out_ci_hi


def et_impulse_response_artifact_subtraction(
        data: np.array = None,
        stimulus_waveform: np.array = None,
        ir_length: int = 100,
        ir_max_lag: int = 0,
        regularization_factor: float = 1,
        plot_results: bool = False,
) -> np.array:
    """
    This function will remove an artifact which has the shape of the input stimulus_waveform.
    Here, artifact is estimated from the impulse response. The latter is estimated by averaging individual
    impulse responses across epochs.
    :param data: data samples x channels x trials
    :param stimulus_waveform: single column numpy array with the target waveform artifact
    :param ir_length: estimated impulse response length in samples
    :param ir_max_lag: maximum lag or sydtem delay (from zero). Impulse response window will be centered around the max
    within the max_lag.
    :param regularization_factor: This value is used to regularize the deconvolution based on Tikhonov regularization
    allow to estimate the transfer function when the input signal is sparse in frequency components
    :param plot_results: if True, figures with results will be shown
    :return: data without artifacts
    """
    original_data_shape = data.shape
    # compute impulse response; data padded to next power of 2 to speed process
    n_fft = next_power_two(data.shape[0])

    data = np.atleast_3d(data)
    _stim_template = stimulus_waveform[0: data.shape[0]]
    data = np.pad(data, ((0, n_fft - data.shape[0]), (0, 0), (0, 0)), constant_values=(0, 0), mode='constant')
    _stim_template = np.pad(_stim_template, ((0, n_fft - _stim_template.shape[0]), (0, 0)),
                            constant_values=(0, 0), mode='constant')
    _fft = pyfftw.builders.rfft(_stim_template,
                                overwrite_input=False, planner_effort='FFTW_ESTIMATE', axis=0,
                                threads=multiprocessing.cpu_count())
    x_fft = _fft()
    _fft = pyfftw.builders.rfft(data,
                                overwrite_input=False, planner_effort='FFTW_ESTIMATE', axis=0,
                                threads=multiprocessing.cpu_count())
    y_fft = _fft()

    # estimate impulse response for each epoch via Tikhonov regularization
    x_fft = np.atleast_3d(x_fft)
    h_fft = y_fft * np.conjugate(x_fft) / (x_fft * np.conjugate(x_fft) + regularization_factor)

    _ifft = pyfftw.builders.irfft(h_fft,
                                  n=data.shape[0],
                                  overwrite_input=False, planner_effort='FFTW_ESTIMATE', axis=0,
                                  threads=multiprocessing.cpu_count())
    h = _ifft()
    h = np.mean(h, axis=2, keepdims=True)
    w = np.zeros(h.shape)
    ws = np.repeat(signal.windows.hanning(ir_length).reshape(-1, 1), h.shape[1], axis=1)
    w[0: ws.shape[0], :, :] = np.atleast_3d(ws)
    _max_ir = np.argmax(h[0: ir_max_lag + 1])
    w = np.roll(w, -ir_length // 2 + _max_ir, axis=0)
    h_ave_w = h * w
    # estimate artifact by convolution
    _fft = pyfftw.builders.rfft(h_ave_w,
                                overwrite_input=False, planner_effort='FFTW_ESTIMATE', axis=0,
                                threads=multiprocessing.cpu_count())
    h_ave_w_fft = _fft()
    # convolve
    fft_artifact = h_ave_w_fft * x_fft
    _ifft = pyfftw.builders.irfft(fft_artifact,
                                  n=data.shape[0],
                                  overwrite_input=False, planner_effort='FFTW_ESTIMATE', axis=0,
                                  threads=multiprocessing.cpu_count())
    _recovered_artifact = _ifft() * data.unit
    _clean_data = data - _recovered_artifact
    if plot_results:
        plt.figure()
        plt.plot(h.squeeze(), label='full IR')
        plt.plot(h_ave_w.squeeze(), label='windowed IR')
        plt.legend()
        plt.show()
    clean_data = np.resize(_clean_data, original_data_shape)
    recovered_artifact = np.resize(_recovered_artifact, original_data_shape)
    return clean_data, recovered_artifact


def next_power_two(n):
    # Returns next power of two following 'number'
    return int(2 ** np.ceil(np.log2(n)))


def et_regression_subtraction(
        data: np.array = None,
        stimulus_waveform: np.array = None,
        max_lag: int = 0,
        max_length: int = None,
        plot_results: bool = False
) -> np.array:
    """
    This function will remove an artifact which has the shape of the input stimulus_waveform.
    Here, artifact is estimated from the impulse response. The latter is estimated by averaging individual
    impulse responses across epochs.
    :param data: data samples x channels x trials
    :param stimulus_waveform: single column numpy array with the target waveform artifact
    :param max_lag: max expected delay between artifact and stimulus waveform. The maximum correlation will be searched
     within this  0 to max_lag
    :param max_length: determines the maxlegnth to search for correlation between stimulus artifact and data. This is
    useful if the desire response has a delay relative to the stimulus artifact. You could limit the correlation to look
    only on the region containing only the artifact,
    :param plot_results: if True, figures with results will be shown
    :return: data without artifacts
    """
    clean_data = np.zeros(data.shape)
    subset_idx = np.arange(0, data.shape[0])
    if max_length is not None:
        subset_idx = np.arange(0, np.minimum(max_length, data.shape[0]))
    sub_stimulus_waveform = stimulus_waveform[subset_idx]
    sub_data_set = data[subset_idx, :]
    _optimal_lag = 0
    # first we detect the lag to which regression fit is maximal across channels
    if max_lag > 0:
        score = np.zeros((max_lag, data.shape[1]))
        for _idx in np.arange(data.shape[1]):
            for _i_lag in range(max_lag):
                regression = LinearRegression()
                _delayed_sub_stimulus_waveform = np.pad(sub_stimulus_waveform,
                                                        ((_i_lag, 0),
                                                         (0, 0)), 'constant', constant_values=(0, 0))
                _delayed_sub_stimulus_waveform.resize(sub_stimulus_waveform.shape, refcheck=False)
                regression.fit(_delayed_sub_stimulus_waveform, sub_data_set[:, _idx])
                score[_i_lag, _idx] = regression.score(_delayed_sub_stimulus_waveform, sub_data_set[:, _idx])
        # we define the optimal lag as the average one across all channel
        _optimal_lag = np.round(np.mean(np.argmax(score, axis=0))).astype(np.int)

    # now we use optimal lag to subtract artifact
    for _idx in tqdm(np.arange(data.shape[1]), desc='Artefact regression'):
        regression = LinearRegression()
        _delayed_sub_stimulus_waveform = np.pad(sub_stimulus_waveform,
                                                ((_optimal_lag, 0),
                                                 (0, 0)), 'constant', constant_values=(0, 0))
        _delayed_sub_stimulus_waveform.resize(sub_stimulus_waveform.shape, refcheck=False)
        regression.fit(_delayed_sub_stimulus_waveform, sub_data_set[:, _idx])
        delayed_stimulus_waveform = np.pad(stimulus_waveform,
                                           ((_optimal_lag, 0),
                                            (0, 0)), 'constant', constant_values=(0, 0))
        delayed_stimulus_waveform.resize(stimulus_waveform.shape, refcheck=False)
        recovered_artifact = regression.predict(delayed_stimulus_waveform)
        clean_data[:, _idx] = data[:, _idx] - recovered_artifact

    if plot_results:
        plt.plot(data[:, -1], label="original data")
        plt.plot(recovered_artifact[:, -1], label="recovered artifact")
        plt.plot(clean_data[:, -1], label="clean data")
        plt.legend()
        plt.show()
    return clean_data, recovered_artifact


def et_xcorr_subtraction(
        data: np.array = None,
        stimulus_waveform: np.array = None,
        max_lag: int = 0,
        max_length: int = None,
        plot_results: bool = False,
) -> np.array:
    """
    This function will remove an artifact which has the shape of the input stimulus_waveform.
    Here, artifact is estimated from the impulse response. The latter is estimated by averaging individual
    impulse responses across epochs.
    :param data: data samples x channels x trials
    :param stimulus_waveform: single column numpy array with the target waveform artifact
    :param max_lag: max expected delay between artifact and stimulus waveform. The maximum correlation will be searched
     within this  0 to max_lag as we assume only a positive delay
    :param max_length: determines the maxlegnth to search for correlation between stimulus artifact and data. This is
    useful if the desire response has a delay relative to the stimulus artifact. You could limit the correlation to look
    only on the region containing only the artifact,
    :param plot_results: if True, figures with results will be shown
    :return: data without artifacts
    """
    original_shape = data.shape
    data = np.atleast_3d(data)
    clean_data = np.zeros(data.shape)
    subset_idx = np.arange(0, data.shape[0])
    if max_length is not None:
        subset_idx = np.arange(0, np.minimum(max_length, data.shape[0]))
    sub_stimulus_waveform = stimulus_waveform[subset_idx]
    sub_data_set = data[subset_idx, ::]
    _optimal_lag = 0
    if max_lag > 0:
        score = np.zeros((max_lag, data.shape[1]))
        for _i_lag in range(max_lag):
            _delayed_sub_stimulus_waveform = np.pad(sub_stimulus_waveform,
                                                    ((_i_lag, 0),
                                                     (0, 0)), 'constant', constant_values=(0, 0))
            _delayed_sub_stimulus_waveform.resize(sub_stimulus_waveform.shape, refcheck=False)
            ave_data = np.mean(sub_data_set, 2)
            transmission_index = ave_data.T.dot(_delayed_sub_stimulus_waveform) / np.expand_dims(
                np.sum(np.square(_delayed_sub_stimulus_waveform)), axis=0)
            recovered_artifact = np.tile(np.atleast_3d(stimulus_waveform * transmission_index.T), (1, 1, data.shape[2]))
            clean_data = data - recovered_artifact
            score[_i_lag, :] = np.mean(np.std(np.mean(data - recovered_artifact, axis=2), axis=0))
        # we define the optimal lag as the average one across all channel
        _optimal_lag = np.round(np.mean(np.argmax(score, axis=0))).astype(np.int)

    # remove artifact at optimal lag
    _delayed_sub_stimulus_waveform = np.pad(sub_stimulus_waveform,
                                            ((_optimal_lag, 0),
                                             (0, 0)), 'constant', constant_values=(0, 0))
    _delayed_sub_stimulus_waveform.resize(sub_stimulus_waveform.shape, refcheck=False)
    ave_data = np.mean(sub_data_set, 2)
    transmission_index = ave_data.T.dot(_delayed_sub_stimulus_waveform) / np.expand_dims(
        np.sum(np.square(_delayed_sub_stimulus_waveform)), axis=0)

    delayed_stimulus_waveform = np.pad(stimulus_waveform,
                                       ((_optimal_lag, 0),
                                        (0, 0)), 'constant', constant_values=(0, 0))
    delayed_stimulus_waveform.resize(stimulus_waveform.shape, refcheck=False)

    recovered_artifact = np.tile(np.atleast_3d(delayed_stimulus_waveform * transmission_index.T),
                                 (1, 1, data.shape[2]))
    clean_data = data - recovered_artifact

    if plot_results:
        plt.plot(data[:, -1], label="original data")
        plt.plot(recovered_artifact[:, -1], label="recovered artifact")
        plt.plot(clean_data[:, -1], label="clean data")
        plt.legend()
        plt.show()
    clean_data = clean_data.reshape(original_shape)
    return clean_data, recovered_artifact


# def et_hotelling_test_frequency(
#         data: np.array = None,
#         test_frequencies: np.array = None,
#         fs: float = None,
#         weights: np.array = None) -> np.array:
#         yfft = np.fft.rfft(data, axis=0)
#         freqs = np.arange(0, yfft.shape[0]) * fs / data.shape[0]
#         if weights is None:
#             weights = np.ones(data.shape[1], data.shape[2])
#
#         freq_pos = [np.argmin(np.diff(np.abs(_f - freqs))) for _f in test_frequencies]
#
#         for _f_pos in np.arange(freq_pos):
#             test_samples = yfft[_f_pos, :, :]
#             rx = np.real(test_samples)
#             ix = np.imag(test_samples)
#             # for standard averaging
#             # mean_rx = np.mean(rx)
#             # mean_ix = np.mean(ix)
#
#             # for weighted averaging
#             mean_rx = np.sum(weights * rx, axis=1) / np.sum(weights, axis=1)
#             mean_ix = np.sum(weights * ix, axis=1) / np.sum(weights, axis=1)
#             _t_square = np.array([np.inf])
#
#             # for standard averaging
#             # dof = self.split_sweep_count[i]
#
#             # for weighted averaging
#             dof = np.sum(weights, axis=1) ** 2.0 / np.sum(weights ** 2.0, axis=1)
#
#             with np.errstate(divide='ignore', invalid='ignore'):
#                 if np.linalg.cond(np.vstack((rx, ix))) < 1 / sys.float_info.epsilon:
#                     x = np.vstack((rx, ix))
#                     # for standard averaging
#                     # _cov_mat = np.cov(x)
#
#                     # for weighted averaging
#                     _cov_mat = np.cov(x, aweights=_weights)
#                     # _eigen_vals = np.linalg.eigvals(_cov_mat)
#                     if np.linalg.cond(_cov_mat) < 1 / sys.float_info.epsilon:
#                         ## get tsquare
#                         _t_square = np.dot(dof * np.array([mean_rx, mean_ix]),
#                                            np.dot(np.linalg.inv(_cov_mat), np.array([[mean_rx], [mean_ix]])))
#
#             _f = (dof - 2) / (2 * dof - 2) * _t_square
#             _d1 = 2
#             _d2 = dof - 2
#             # we calculate the half length and direction of the ellipse
#             _f_critic = f.ppf(1 - alpha, _d1, _d2)
#             # compute residual noise from circular variance
#             _rn = np.sqrt(np.sum((rx - mean_rx) ** 2.0 + (ix - mean_ix) ** 2.0)) / (dof - 1)
#             #_L = ((2 * (self.split_sweep_count[i] - 1) * D * F95)./(
#             self.split_sweep_count(i) * (self.split_sweep_count(i) - 2))) ** 2
#             _snr = np.maximum(_f - 1, 0.0)
#             test = HotellingTSquareFrequencyTest(frequency_tested=self._fft_frequencies[self._frequency_bin[j]],
#                                                  frequency_bin=self._frequency_bin[j],
#                                                  t_square=_t_square[0],
#                                                  df_1=_d1,
#                                                  df_2=_d2,
#                                                  f=_f[0],
#                                                  p_value=1 - f.cdf(_f, _d1, _d2)[0],
#                                                  spectral_magnitude=np.abs(_fft[self._frequency_bin[j], i]),
#                                                  spectral_phase=np.angle(_fft[self._frequency_bin[j], i]),
#                                                  rn=_rn,
#                                                  snr=_snr[0],
#                                                  snr_db=10 * np.log10(_snr)[0] if _snr[0] > 0.0 else -np.Inf,
#                                                  snr_critic_db=10 * np.log10(_f_critic - 1),
#                                                  snr_critic=_f_critic - 1,
#                                                  channel=str(i))
#             _split_data = np.append(_split_data, test)
#         value.append(_split_data)
def et_ica_epochs(
        data: np.array = np.array([]),
        tol: float = 1e-4,
        iterations: int = 200):
    """
    This function computes and sorts the components of an input matrix using ICA. The components are sorted by their
    power.
    :param data: np.array where components are obtained for each column
    :param tol: float indicating the tolerance for the difference between previous and updated weights to stop the
    iteration
    :param iterations: maximum number of iterations to estimate the components
    :return: components, unmixing matrix (used to obtain the components), mixing_matrix (used to project the components
    back to the original space, power of components, whitening matrix
    """

    no_chans = data.shape[1]
    whitened_ave, whitening_m = et_ica_whitening(data)

    # Implement ICA
    # Guess random initial value for W (inverse mixing matrix) and update until it is orthogonal
    # (ie. multiplied by transverse = 1)
    # Initialise array for w
    w = np.zeros((no_chans, no_chans))

    # Iterate through W matrix and update it - ie. calculate new value for w
    # Based on formula from https://towardsdatascience.com/independent-component-analysis-ica-in-python-a0ef0db0955e
    for i in range(no_chans):
        W = np.random.rand(no_chans)

        j = 0
        tol_lim = 1

        while (j < iterations) and (tol_lim > tol):
            u = np.dot(W, whitened_ave)
            g = np.tanh(u)
            g_dash = 1 - np.square(np.tanh(u))
            W_update = (whitened_ave * g).mean(axis=1) - (g_dash.mean() * W.squeeze())
            # Decorrelating w
            W_update = W_update - np.dot(np.dot(W_update, w[:i].T), w[:i])
            W_update = W_update / np.sqrt((W_update ** 2).sum())
            # Create a limit condition using the current value of w
            tol_lim = np.abs(np.abs((W_update * W).sum()) - 1)
            # Update original w with the new values
            W = W_update
            # Iterator counter
            j += 1
        w[i, :] = W.T

    # Unmix Signals
    components = np.dot(w, whitened_ave)
    components = components.T
    mixing = np.linalg.pinv(np.dot(w, whitening_m))

    # Sorting by power
    # Calculate and sort a power array (large to small)
    pwr = np.max(np.abs(mixing), axis=0)
    idx_pwr = np.argsort(-pwr)
    s_pwr = pwr[idx_pwr]

    # Sort mixing matrix and components by power
    unmixing = w.T
    s_unmixing = unmixing[:, idx_pwr].T
    s_mixing = mixing[:, idx_pwr]
    s_components = components[:, idx_pwr]

    # Projection back into cortical space
    # proj = (np.dot(mixing, components.T)).T

    return s_components, s_unmixing, s_mixing, s_pwr, whitening_m


def et_ica_whitening(data: np.array = None):
    # Preprocessing
    data = data.T

    # Centering - subtracting the mean from the observed data
    mean = np.mean(data, axis=1, keepdims=True)
    centered_data = data - mean

    # Whitening x - removing correlations between components
    # Calculate covariance matrix
    covar = (centered_data.dot(centered_data.T)) / (np.shape(centered_data)[1] - 1)

    # Use single value decomposition to describe the matrix using its constituents
    # Breaking it down into left singular vectors (U) or eigenvectors, the singular values or eigenvalues (K)
    # and right singular vectors (V)
    u, k, v = np.linalg.svd(covar)

    # Create a diagonal matrix of the eigenvalues (inverse square)
    d = np.diag(1 / np.sqrt(k))

    # Calculate the matrix which will whiten the weight averaged epochs
    whitening_m = np.dot(u, np.dot(d, u.T))

    # Whiten EEG averaged data using above whitening matrix
    whitened_ave = np.dot(whitening_m, data)

    return whitened_ave, whitening_m


def goertzel(data, fs, frequency):
    """
    Implementation of the Goertzel algorithm, to calculate individual frequency Fourier values.
    :param data: (time x channels) numpy arra
    :param fs: float indicating the sampling rate
    :param frequency: frequency to be estimated in Hz
    :return: np.array with Fourier frequency term for each channel (1 x channels)
    Frequency amplitude will match that of numpy.fft.fft, exact frequency bin tested
    """
    n = data.shape[0]
    freqs = np.arange(0, n) * fs / n
    k = np.argmin(np.abs(freqs - frequency))
    cr = np.cos(2.0 * np.pi * k / n)
    ci = np.sin(2.0 * np.pi * k / n)
    coeff = 2.0 * cr
    sprev = 0.0
    sprev2 = 0.0
    for _i in tqdm(np.arange(n).astype(int), desc='DFT estimation {:}'.format(frequency)):
        s = data[[_i], :] + coeff * sprev - sprev2
        sprev2 = sprev
        sprev = s
    real = sprev * cr - sprev2
    imag = sprev * ci
    exact_frequency = freqs[k]
    return real + 1j * imag, exact_frequency


def discrete_dft(data: np.array = None,
                 fs: float = None,
                 frequencies: float = None,
                 method: str = 'auto'):
    """
    Gets individual frequency Fourier values using either fast fft or Goertzel depending on available memory.
    :param data: (time x channels) numpy array
    :param fs: float indicating the sampling rate
    :param frequencies: frequencies to be estimated in Hz
    :param method: string specifying how to compute DFT
    :return: np.array with Fourier frequency term for each channel (1 x channels)
    """
    data = set_default_unit(data, u.uV)
    frequencies = set_default_unit(frequencies, u.Hz)
    n = data.shape[0]
    freqs = np.arange(0, n) * fs / n
    k = np.array([np.argmin(np.abs(freqs - _f)) for _f in frequencies])
    dft = np.zeros((k.size, data.shape[1], data.shape[2])) * data.unit
    exact_frequencies = np.zeros(k.size) * frequencies.unit
    _memory = enough_memory(data)
    if method == 'auto':
        _method = 'fft' if _memory else 'goertzel'

    if _method == 'fft':
        fft = pyfftw.builders.rfft(data, overwrite_input=False, planner_effort='FFTW_ESTIMATE', axis=0,
                                   threads=multiprocessing.cpu_count())
        _fft = fft()
        dft = _fft[k, :] * data.unit
        exact_frequencies = freqs[k]
    elif _method == 'goertzel':
        for _i, _f in enumerate(frequencies):
            _dft, _exact_frequency = goertzel(data, fs, _f)
            dft[_i] = _dft
            exact_frequencies[_i] = _exact_frequency
    else:
        raise 'no implemented method'

    return dft, exact_frequencies


def get_discrete_frequencies_weights(
        epochs: np.array = None,
        fs: float = None,
        frequencies: float = None,
        block_size: int = 5,
        weighted_average=True,
        regularization_factor: float = 0.005,) -> np.array:
    """
    Compute spectral amplitude for a given frequencies
    component.
    :param epochs: time x channels x trials numpy array in the time domain
    :param fs: float indicating the sampling rate in Hz
    :param frequencies: array with the frequencies of interest
    :param block_size: integer indicating the number of trials that would be use to estimate the weights
    :param weighted_average: if false, frequency bins will not be weighted to compute mean and std
    :param regularization_factor: This value is used to regularize the variance if too small (based on Tikhonov
     regularization)
    """
    epochs = set_default_unit(epochs, u.uV)
    fs = set_default_unit(fs, u.Hz)
    frequencies = set_default_unit(frequencies, u.Hz)

    y_fft, exact_frequencies = discrete_dft(epochs, fs, frequencies)

    block_size = np.minimum(epochs.shape[2], block_size)
    blocks = np.arange(0, epochs.shape[2] + 1, block_size).astype(np.int)
    blocks[-1] = np.maximum(blocks[-1], epochs.shape[2])
    n_blocks = np.maximum(len(blocks) - 1, 1)
    r = np.zeros((y_fft.shape[0], epochs.shape[1], n_blocks))
    norm_r = np.zeros((y_fft.shape[0], epochs.shape[1], n_blocks))
    total_var = np.zeros((y_fft.shape[0], epochs.shape[1], n_blocks)) * epochs.unit ** 2.0
    wb = np.ones(total_var.shape) * total_var.unit
    ini_block, end_block = blocks[:-1], np.cumsum(np.diff(blocks))[::1]
    for i, (_ini_trial, _end_trial) in enumerate(zip(ini_block, end_block)):
        mag = np.abs(y_fft[:, :, _ini_trial: _end_trial])
        ang = np.angle(y_fft[:, :, _ini_trial: _end_trial]).value
        if weighted_average:
            angular_weights = (mag + regularization_factor * mag.unit) ** 2.0
            angular_weights = angular_weights / np.sum(angular_weights, axis=2, keepdims=True)
        else:
            angular_weights = 1.0

        norm_r[:, :, i] = np.abs(np.sum((angular_weights * np.exp(1j * ang)), axis=2))
        mean_x = np.sum((mag * angular_weights * np.cos(ang)), axis=2, keepdims=True)
        mean_y = np.sum((mag * angular_weights * np.sin(ang)), axis=2, keepdims=True)
        r[:, :, i] = np.sqrt(mean_x ** 2.0 + mean_y ** 2)[:, :, 0]
        var_x = np.sum(angular_weights * (mag * np.cos(ang) - mean_x) ** 2.0, axis=2)
        var_y = np.sum(angular_weights * (mag * np.sin(ang) - mean_y) ** 2.0, axis=2)
        # we assumed that variance on x and y axis are independent from each other
        # this encapsulates the variance: sigma_r^2 <= variance <= sigma_r^2 + 4 * sum(w_angular*r_i*mean(r_i))
        total_var[:, :, i] = var_x + var_y + (regularization_factor * mag.unit) ** 2.0
        # purely radial
        # mean_r = np.sum(mag * angular_weights, axis=2, keepdims=True)
        # total_var[:, :, i] = np.sum(angular_weights * (mag - mean_r) ** 2.0, axis=2)

        # fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        # ax.plot(ang.T.squeeze(), mag.T.squeeze(), 'o')
        # ax.plot(np.angle(mean_x + 1j*mean_y).squeeze(), r[:, :, i].squeeze(), 'o', markersize=8, color='k')

    if weighted_average:
        wb = 1 / total_var
    if np.all(wb == np.inf):
        wb[:] = 1
    w = np.zeros(y_fft.shape) * wb.unit
    for i, (_ini_trial, _end_trial) in enumerate(zip(ini_block, end_block)):
        w[:, :, _ini_trial: _end_trial] = wb[:, :, [i]]
    if weighted_average:
        rn = np.sqrt(1.0 / np.sum(block_size / total_var, axis=2))
    else:
        rn = np.sqrt(np.sum(block_size * total_var, axis=2) / ((block_size * n_blocks) ** 2.0))
    spectral_magnitude = np.abs(eo.w_mean(y_fft, weights=w))
    sig_plus_noise_var = spectral_magnitude ** 2.0
    snr = sig_plus_noise_var / (rn ** 2) - 1
    return w, spectral_magnitude, sig_plus_noise_var, rn, snr, exact_frequencies, y_fft


def get_pooled_frequency_weights(
        epochs: np.array = None,
        fs: float = None,
        frequencies: float = None,
        block_size: int = 5,
        weighted_average=True,
        delta_frequency: u.Quantity = 5 * u.Hz,
        power_line_frequency: u.Quantity = 50 * u.Hz) -> np.array:
    """
    Compute spectral amplitude and pooled weights for set of frequencies.
    :param epochs: time x channels x trials numpy array in the time domain
    :param fs: float indicating the sampling rate in Hz
    :param frequencies: numpy array indicating the frequency of interest
    :param block_size: integer indicating the number of trials that would be use to estimate the weights
    :param weighted_average: if false, frequency bins will not be weighted to compute mean and std
    :param delta_frequency: frequency size around each frequency used to estimate the noise
    :param power_line_frequency: frequency of local power line frequency. This will be used to prevent using
        this frequency or its multiples when performing frequency statistics
    :return: weights, complex frequencies, exact tested frequencies, estimate of residual noise and snr at those
    frequencies
    """
    epochs = set_default_unit(epochs, u.uV)
    fs = set_default_unit(fs, u.Hz)
    frequencies = set_default_unit(frequencies, u.Hz)
    delta_frequency = set_default_unit(delta_frequency, u.Hz)
    freq_axis = np.fft.rfftfreq(epochs.shape[0], 1 / fs)
    power_line_frequencies = power_line_frequency * np.arange(1,
                                                              np.round(0.5 * fs / power_line_frequency))
    _power_idx = np.array([np.argmin(np.abs(freq_axis - _freq)) for _freq in power_line_frequencies])
    _target_idx = np.array([np.argmin(np.abs(freq_axis - _freq)) for _freq in frequencies])
    # we always keep the input frequencies, even if they are multiple of line_power
    _power_idx = np.setdiff1d(_power_idx, _target_idx).astype(int)
    # get all frequencies for the analysis
    _idx_to_include_all = np.array([])
    for _idx_t, _f in enumerate(frequencies):
        # _idx_target = np.argmin(np.abs(freq_axis - _f))
        # _f_target = freq_axis[_idx_target]
        _ini_bin = np.maximum(np.argmin(np.abs(freq_axis - (_f - delta_frequency))), 0)
        _end_bin = np.minimum(np.argmin(np.abs(freq_axis - (_f + delta_frequency))), freq_axis.size - 1)
        _idx_freq = np.arange(_ini_bin, _end_bin + 1)
        _idx_to_include_all = np.concatenate((_idx_to_include_all, _idx_freq))
    _idx_to_include_all = np.unique(_idx_to_include_all)
    # remove power line bins
    _idx_to_include = np.setdiff1d(_idx_to_include_all, _power_idx).astype(int)
    _idx_excluded = np.setdiff1d(_idx_to_include, _idx_to_include_all)
    if _idx_excluded.size > 0:
        print('Excluding {:} to avoid power line harmonics'.format(
            freq_axis[_idx_excluded]))
    # print('Test frequency {:}. Noise estimation between {:} and {:}'.format(_f_target,
    #                                                                         freq_axis[_ini_bin],
    #                                                                         freq_axis[_end_bin]))

    # get target and surrounding frequency bins first
    _w, _amp, _, _rn, _snr, _exact_frequencies, y_fft = get_discrete_frequencies_weights(
        epochs=epochs,
        fs=fs,
        block_size=block_size,
        frequencies=freq_axis[_idx_to_include],
        weighted_average=weighted_average
    )
    _signal_plus_noise_var = _amp ** 2.0
    # pool across frequencies
    _var_ave = 1 / _w
    total_variance = np.mean(_var_ave, axis=0, keepdims=True)
    weights = 1 / total_variance
    # ensure same size as input epochs. All time examples are weighted the same
    weights = np.ones(epochs.shape) * weights
    pooled_rn = np.sqrt(np.mean(_rn ** 2.0, axis=0))
    pooled_snr = np.mean(_signal_plus_noise_var, axis=0) / (pooled_rn ** 2) - 1
    _idx_targets = np.array([np.argmin(np.abs(_exact_frequencies - _f)) for _f in frequencies])
    by_freq_rn = _rn[_idx_targets]
    freq_samples = y_fft[_idx_targets]
    exact_frequencies = _exact_frequencies[_idx_targets]
    by_freq_snr = _snr[_idx_targets]

    print("Weights, noise, and snr estimated by pooling {:} individual measures, each estimated with a delta of "
          "{:} around each frequency.".format(frequencies, delta_frequency))
    return weights, pooled_rn, pooled_snr, by_freq_rn, by_freq_snr, freq_samples, exact_frequencies
