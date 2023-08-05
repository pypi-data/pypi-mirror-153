import numpy as np
import multiprocessing
import pyfftw
import psutil as psu
import scipy.signal as signal
import time
import ctypes
import astropy.units as u
from tqdm import tqdm
__author__ = 'jundurraga-ucl'


def timeit(method):
    def timed(*args, **kw):
        time_start = time.time()
        result = method(*args, **kw)
        time_end = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((time_end - time_start) * 1000)
        else:
            print('{:s}: {:.2f} ms'.format(method.__name__, (time_end - time_start) * 1000))
        return result
    return timed


def find_freq(freq_vector=np.array, freq_to_find=np.array, f_range=0.0):
    f_bins = []
    for f in freq_to_find:
        f_pos = [np.where(freq_vector < f - f_range)[0][-1],
                 np.where(freq_vector > f + f_range)[0][0]]
        f_bins.append(f_pos)
    return f_bins


def eeg_notch_filter(x: np.array = np.array([]), f: list = [50.0], f_range=1.0, fs=16384.0, blocks=8) -> np.array:
    if np.mod(x.shape[0], 2) == 0:
        fft_size = (x.shape[0] / 2) + 1
    else:
        fft_size = (x.shape[0] + 1) / 2

    freq = np.arange(fft_size) * fs / x.shape[0]
    f_bins = find_freq(freq, f, f_range)
    blocks = np.minimum(x.shape[1], blocks)
    xfilt = np.zeros(x.shape)
    for b in np.arange((np.ceil(x.shape[1]) / blocks)):
        pos_ini = int(b * blocks)
        pos_end = int(np.minimum((b + 1) * blocks, x.shape[1]) + 1)
        fft = pyfftw.builders.rfft(x[:, pos_ini:pos_end], overwrite_input=False, planner_effort='FFTW_ESTIMATE', axis=0,
                                   threads=multiprocessing.cpu_count())
        spectrum = fft()
        for i, _f_pos in enumerate(f_bins):
            spectrum[_f_pos[0]:_f_pos[1] + 1, :] = 0.0

        ifft = pyfftw.builders.irfft(spectrum, overwrite_input=False, planner_effort='FFTW_ESTIMATE', axis=0,
                                     threads=multiprocessing.cpu_count())
        xfilt[:, pos_ini:pos_end] = ifft()
        print('fft notch filtered:', pos_end - 1)
        if pos_end == x.shape[1]:
            break
    return xfilt


def eeg_resampling(x: np.array = np.array([]), factor=1.0, blocks=8) -> np.array:
    if factor == 1.0:
        return x, factor
    nfft = x.shape[0]
    upnfft = np.round((nfft * factor)).astype(np.int)
    if factor < 1:
        new_nfft = int(np.ceil(1.0 / factor) * (nfft * factor))
        factor = float(upnfft) / float(new_nfft)
        x = np.pad(x, ((0, new_nfft - nfft), (0, 0)), 'constant', constant_values=(0, 0))
    else:
        new_nfft = np.round(nfft * factor).astype(np.int)
        factor = float(new_nfft) / float(nfft)

    # zero padding to match ensure correct decimation
    blocks = np.minimum(x.shape[1], blocks)
    xfilt = np.zeros((upnfft, x.shape[1]))

    for b in tqdm(np.arange((np.ceil(x.shape[1]) / blocks)), desc='Resampling'):
        pos_ini = int(b * blocks)
        pos_end = int(np.minimum((b + 1) * blocks, x.shape[1]) + 1)
        fft = pyfftw.builders.rfft(x[:, pos_ini:pos_end],
                                   overwrite_input=False,
                                   planner_effort='FFTW_ESTIMATE',
                                   axis=0,
                                   threads=multiprocessing.cpu_count())
        fft_data = fft()
        if factor < 1:
            f_end = 0.99 * np.pi * factor
            f_end_attenuation = 100  # dB
            f_c = 0.9 * f_end
            s_2 = 20 * np.log10(np.exp(1)) * (f_end - f_c) ** 2 / (2 * f_end_attenuation)
            f = np.arange(0, fft_data.shape[0]).reshape((-1, 1)) * np.pi / fft_data.shape[0]
            lpf = np.ones((fft_data.shape[0], 1))
            lpf[f >= f_c] *= np.exp(-(f[f >= f_c] - f_c) ** 2 / (2 * s_2))
            fft_data *= lpf

        ifft = pyfftw.builders.irfft(fft_data,
                                     n=upnfft,
                                     overwrite_input=False,
                                     planner_effort='FFTW_ESTIMATE',
                                     axis=0,
                                     threads=multiprocessing.cpu_count())
        sub_set = ifft()
        xfilt[:, pos_ini:pos_end] = sub_set
        # print('re-sampling channel %i to %i' % (pos_ini, pos_end - 1))
        if pos_end == x.shape[1]:
            break
    return xfilt * factor * x.unit, factor


@timeit
def filt_filt_multithread(input_data: np.array([]),
                          a=None,
                          b=None,
                          ch_per_block=None,
                          n_jobs=None) -> np.array:
    mp_arr = multiprocessing.Array(ctypes.c_double, input_data.size, lock=False)
    arr = np.frombuffer(mp_arr)
    filtered_data = arr.reshape(input_data.shape)
    np.copyto(filtered_data, input_data)

    if not n_jobs:
        n_jobs = np.maximum(multiprocessing.cpu_count(), 1)
    else:
        n_jobs = np.minimum(multiprocessing.cpu_count(), n_jobs)
    if not ch_per_block:
        _virtual_memory = psu.virtual_memory()
        ch_per_block = np.maximum(1, np.int(_virtual_memory.available /
                                            (filtered_data.nbytes / filtered_data.shape[1]) * 0.1))
    ch_per_block = np.minimum(filtered_data.shape[1], ch_per_block)
    print(('filtering ' + str(ch_per_block) + ' channels per block'))

    for _bl in np.arange((np.ceil(filtered_data.shape[1]) / ch_per_block)):
        p = []
        pos_ini = int(_bl * ch_per_block)
        pos_end = int(np.minimum((_bl + 1) * ch_per_block, filtered_data.shape[1]))
        _b_size = pos_end - pos_ini
        _ch_per_thread = int(np.ceil(float(_b_size) / n_jobs))
        _n_jobs = int(np.minimum(n_jobs, np.ceil(float(_b_size) / _ch_per_thread)))
        # q_out = multiprocessing.Queue(maxsize=_n_jobs)
        pool = multiprocessing.Pool(processes=_n_jobs)
        for _t in range(_n_jobs):
            sub_pos_ini = int(pos_ini + _ch_per_thread * _t)
            sub_pos_end = int(np.minimum(pos_end, pos_ini + _ch_per_thread * (_t + 1)))
            p.append(pool.Process(target=filter_worker,
                                  args=(filtered_data, sub_pos_ini,
                                        sub_pos_end, b, a)))
            print(('Thread %i filtering channels: %i to %i' % (_t, sub_pos_ini, sub_pos_end - 1)))
        [_p.start() for _p in p]
        [_p.join() for _p in p]
        pool.close()
        pool.join()
        print(('Filtered channels: %i to %i' % (pos_ini, pos_end - 1)))
    return filtered_data


def filter_worker(filtered_data, pos_ini, pos_end, b, a):
    """
    IIR/FIR filtering worker. This function filter part of input data. Filter coefficients can be either  FIR or IIR
    :param filtered_data: mxn matrix to be filtered
    :param pos_ini: initial column to begin filtering
    :param pos_end: end column to begin filtering
    :param b: filter coefficients numerator
    :param a: filter coefficients denominator
    :return: partially filtered data
    :return: filtered data
    """
    filtered_data[:, pos_ini:pos_end] = signal.filtfilt(b, a, filtered_data[:, pos_ini:pos_end], axis=0)


@timeit
def filt_filt_multithread_ovs(input_data: np.array([]),
                              b=None,
                              ch_per_block=None,
                              n_jobs=None,
                              onset_padding=True) -> np.array:
    """
    This function implements parallel filtering using overlap-saving FIR filtering
    :param input_data: numpy array with data to be filtered
    :param b: FIR filter coefficients
    :param ch_per_block: number of channels to be filter per job
    :param n_jobs: number of parallel jobs
    :param onset_padding: whether to pad samples or not at the beginning and end of the input data. This minimizes the
    ringing effects of the filter
    :return: filtered data
    """
    mp_arr = multiprocessing.Array(ctypes.c_double, input_data.size, lock=False)
    arr = np.frombuffer(mp_arr)
    pad_width = 0
    if onset_padding:
        pad_width = input_data.shape[0] // 8
        input_data = np.pad(input_data, ((pad_width, pad_width), (0, 0)), mode='edge')
    filtered_data = arr.reshape(input_data.shape)
    np.copyto(filtered_data, input_data)

    if not n_jobs:
        n_jobs = np.maximum(multiprocessing.cpu_count(), 1)
    else:
        n_jobs = np.minimum(multiprocessing.cpu_count(), n_jobs)
    if not ch_per_block:
        _virtual_memory = psu.virtual_memory()
        ch_per_block = np.maximum(1, np.int(_virtual_memory.available /
                                            (filtered_data.nbytes / filtered_data.shape[1]) * 0.1))
    ch_per_block = np.minimum(filtered_data.shape[1], ch_per_block)
    print(('filtering ' + str(ch_per_block) + ' channels per block'))

    for _bl in tqdm(np.arange((np.ceil(filtered_data.shape[1]) / ch_per_block)), desc='Filter'):
        p = []
        pos_ini = int(_bl * ch_per_block)
        pos_end = int(np.minimum((_bl + 1) * ch_per_block, filtered_data.shape[1]))
        _b_size = pos_end - pos_ini
        _ch_per_thread = int(np.ceil(float(_b_size) / n_jobs))
        _n_jobs = int(np.minimum(n_jobs, np.ceil(float(_b_size) / _ch_per_thread)))
        # q_out = multiprocessing.Queue(maxsize=_n_jobs)
        pool = multiprocessing.Pool(processes=_n_jobs)
        for _t in range(_n_jobs):
            sub_pos_ini = int(pos_ini + _ch_per_thread * _t)
            sub_pos_end = int(np.minimum(pos_end, pos_ini + _ch_per_thread * (_t + 1)))
            p.append(pool.Process(target=filt_worker_ovs,
                                  args=(filtered_data, sub_pos_ini,
                                        sub_pos_end, b)))
            # print(('Thread %i filtering channels: %i to %i' % (_t, sub_pos_ini, sub_pos_end - 1)))
        [_p.start() for _p in p]
        [_p.join() for _p in p]
        pool.close()
        pool.join()
        # print(('Filtered channels: %i to %i' % (pos_ini, pos_end - 1)))
    return filtered_data[pad_width: filtered_data.shape[0] - pad_width, :]


def filt_worker_ovs(filtered_data: np.array = None, pos_ini=0, pos_end=0, b: np.array = None):
    """
    Overlap saving filtering worker. This function filter part of input data. Filter coefficients are assumed to be
    from an FIR filter
    :param filtered_data: mxn matrix to be filtered
    :param pos_ini: initial column to begin filtering
    :param pos_end: end column to begin filtering
    :param b: filter coefficients
    :return: partially filtered data
    """
    if pos_end is None:
        pos_end = filtered_data.shape[1]
    s_1 = ols_filt(b=b, x=filtered_data[:, pos_ini:pos_end])
    filtered_data[:, pos_ini:pos_end] = s_1[0:filtered_data.shape[0], :]
    return filtered_data


def filt_filt_worker_ovs(filtered_data: np.array = None, pos_ini=0, pos_end=None, b: np.array = None):
    """
    Overlap saving filtering worker. This function filter part of input data. Filter coefficients are assumed to be
    from an FIR filter
    :param filtered_data: mxn matrix to be filtered
    :param pos_ini: initial column to begin filtering
    :param pos_end: end column to begin filtering
    :param b: filter coefficients
    :return: partially filtered data
    """
    if pos_end is None:
        pos_end = filtered_data.shape[1]
    filtered_data[:, pos_ini:pos_end] = ols_filt_filt(b=b, x=filtered_data[:, pos_ini:pos_end])
    return filtered_data


def ols_filt(b: np.array = None, x: np.array = None, axis=0):
    """
    Overlap-saving filtering.
    Filter a one-dimensional array with an FIR filter
    Filter a data array using a FIR filter given in `b`.
    Filtering uses the overlap-add method converting both `x` and `b`
    into frequency domain first.  The FFT size is determined as the
    next higher power of 2 of twice the length of `b`.

    :param b: one-dimensional numpy array. The impulse response of the filter
    :param x: numpy array to be filtered
    :param axis: dimension in which filtering is applied
    :return: filtered array
    """

    l_i = b.shape[0]
    # Find power of 2 larger that 2*l_i (from abarnert on Stackoverflow)
    l_f = 2 << (l_i-1).bit_length()
    l_s = l_f - l_i + 1
    l_sig = x.shape[0]
    offsets = range(0, l_sig, l_s)

    # handle complex or real input
    if np.iscomplexobj(b) or np.iscomplexobj(x):
        fft_func = np.fft.fft
        ifft_func = np.fft.ifft
        res = np.zeros((l_sig+l_f, *x.shape[1:]), dtype=np.complex128) * x.unit
    else:
        fft_func = np.fft.rfft
        ifft_func = np.fft.irfft
        res = np.zeros((l_sig+l_f, *x.shape[1:])) * x.unit

    FDir = np.atleast_2d(fft_func(b, n=l_f, axis=axis)).T
    if x.ndim == 3:
        FDir = np.atleast_3d(FDir)

    # overlap and add
    for n in offsets:
        res[n:n+l_f, :] += ifft_func(fft_func(x[n:n+l_s, :], n=l_f, axis=0)*FDir, axis=0)

    return res


def ols_filt_filt(b: np.array = None, x: np.array = None, axis=0):
    """
    Overlap-saving filt-filt. Filters input x twice (in both directions) to cancel out the group-delay introduced by the
    filter
    :param b: FIR filter coef
    :param x: numpy array to be filtered
    :param axis: dimension in which filtering is applied
    :return: filtered array
    """
    s_1 = ols_filt(b=b, x=x, axis=axis)
    _l_1 = s_1.shape[0] - x.shape[0]
    s_1 = ols_filt(b=b, x=np.flip(s_1, axis=axis), axis=axis)
    s_1 = np.flip(s_1, axis=axis)
    return s_1[_l_1:_l_1 + x.shape[0], :]


def bandpass_fir_win(high_pass: u.quantity.Quantity = None,
                     low_pass: u.quantity.Quantity = None,
                     fs: u.quantity.Quantity = 16884.0 * u.Hz,
                     ripple_db=60.0):
    """
    Generate FIR filter coefficients using a Kaiser filter
    :param high_pass: frequency (in Hz) of high-pass filter
    :param low_pass: frequency (in Hz) of low-pass filter
    :param fs: sampling frequency (in Hz)
    :param ripple_db: amount of ripple, in dB, in the pass-band region. The magnitude will variation will be below
    -ripple dB.
    :return: a numpy array with the filter coefficients
    """
    nyq = 0.5 * fs
    width = 1.0 * u.Hz / nyq
    taps = None
    if low_pass is not None and high_pass is None:
        width = min((nyq - low_pass) / nyq, width)
        n_taps, beta = signal.kaiserord(ripple_db, width)
        # ensure odd number of taps to prevent filter to crash
        n_taps = n_taps // 2 * 2 + 1

        taps = signal.firwin(n_taps,
                             low_pass.to(u.Hz).value,
                             nyq=nyq.to(u.Hz).value,
                             pass_zero='lowpass',
                             window=('kaiser', beta), scale=True)

    if low_pass is None and high_pass is not None:
        width = min(high_pass / nyq, width)
        n_taps, beta = signal.kaiserord(ripple_db, width)
        n_taps = n_taps // 2 * 2 + 1
        taps = signal.firwin(n_taps, high_pass.to(u.Hz).value,
                             nyq=nyq.to(u.Hz).value,
                             pass_zero='highpass',
                             window=('kaiser', beta), scale=True)
    if low_pass is not None and high_pass is not None:
        width_1 = min((nyq - low_pass) / nyq, width)
        width_2 = min(high_pass / nyq, width)
        width = min(width_1, width_2)
        n_taps, beta = signal.kaiserord(ripple_db, width)
        n_taps = n_taps // 2 * 2 + 1
        taps = signal.firwin(n_taps, [high_pass.to(u.Hz).value,
                                      low_pass.to(u.Hz).value],
                             nyq=nyq.to(u.Hz).value, pass_zero='bandpass',
                             window=('kaiser', beta), scale=True)

    print('FIR Kaiser filter ({:} taps) HP {:} - LP {:}, {:} dB ripple, {:} transition width.'.format(
        taps.size,
        high_pass,
        low_pass,
        ripple_db,
        width * nyq))

    return taps
