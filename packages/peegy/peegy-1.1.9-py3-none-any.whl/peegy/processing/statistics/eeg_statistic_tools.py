import numpy as np
from peegy.processing.statistics.definitions import HotellingTSquareTest
from peegy.definitions.channel_definitions import ChannelItem
from peegy.processing.tools.eeg_epoch_operators import w_mean, effective_sampling_size
from peegy.processing.tools.epochs_processing_tools import goertzel
from peegy.tools.units.unit_tools import set_default_unit
import astropy.units as u
import scipy.stats as st
from tqdm import tqdm


def hotelling_t_square_test(samples=np.array([]),
                            weights: np.array = None,
                            channels: np.array([ChannelItem]) = None,
                            **kwargs):
    """
    Compute Hotelling T2 test on samples
    :param samples: np.array with samples to perform the test (time x channels x trials)
    :param weights: if passed, statistics will be computed using weighted statistics
    :param channels: list of ChannelItems use to generate pandas data frame with the label of each channel
    :param kwargs:
    :return: pandas data frame with statistical tests
    """
    samples = set_default_unit(samples, u.uV)
    _test_data = []
    if not samples.size:
        return None
    if weights is None:
        weights = np.ones(samples.shape[1::]) * u.dimensionless_unscaled
    if weights.ndim == 3:
        # we assume that the same weight is use for each row
        weights = weights[0, :, :]

    mean_data = w_mean(samples, weights=weights)
    dof = effective_sampling_size(weights, axis=1)

    with np.errstate(divide='ignore', invalid='ignore'):
        for _ch in tqdm(range(samples.shape[1]), desc="Hotelling-T2"):
            data_ch = samples[:, _ch, :]
            mean_ch = mean_data[:, _ch]
            _cov_mat = np.cov(data_ch.value, aweights=weights[_ch, :].value) * data_ch.unit ** 2.0
            # if np.linalg.cond(_cov_mat) < 1 / sys.float_info.epsilon:
            try:
                _t_square = dof[_ch] * mean_ch.dot(np.linalg.inv(_cov_mat)).dot(mean_ch.T)
            except np.linalg.LinAlgError:
                try:
                    _t_square = dof[_ch] * mean_ch.dot(np.linalg.pinv(_cov_mat)).dot(mean_ch.T)
                    # _t_square = dof[_ch] * mean_ch.dot(np.linalg.inv(
                    #     _cov_mat +
                    #     np.eye(_cov_mat.shape[1]) * 10.e-10)).dot(mean_ch.T)
                except np.linalg.LinAlgError:
                    _t_square = np.inf * u.dimensionless_unscaled
                    print('could not found the inverse covariance matrix')

            n_p = data_ch.shape[0]
            n_n = dof[_ch]
            _f = (n_n - n_p) / (n_p * (n_n - 1.0)) * _t_square
            _d1 = n_p
            _d2 = n_n - n_p

            c = st.f.ppf(0.5, _d1, _d2)
            if _f > c:
                p = st.f.cdf(1.0 / _f, _d2, _d1)
            else:
                p = 1 - st.f.cdf(_f, _d1, _d2)
            _f_95 = st.f.ppf(0.95, _d1, _d2)
            # compute residual noise from circular variance
            _rn = np.sqrt(np.sum((data_ch - np.expand_dims(mean_ch, 1)) ** 2.0)) / (data_ch.shape[1] - 1)
            _snr = np.maximum(_f - 1, 0.0 * u.dimensionless_unscaled)
            if channels is not None:
                _channel = channels[_ch].label
            else:
                _channel = str(_ch)

            # _L = ((2 * (self.split_sweep_count[i] - 1) * D * F95)./(
            # self.split_sweep_count(i) * (self.split_sweep_count(i) - 2))) ** 2

            test = HotellingTSquareTest(t_square=_t_square,
                                        df_1=_d1,
                                        df_2=_d2,
                                        n_epochs=samples.shape[2],
                                        f=_f,
                                        p_value=p,
                                        # mean_amplitude=mean_ch,
                                        rn=_rn,
                                        snr=_snr,
                                        snr_db=10 * np.log10(_snr) if _snr > 0.0 else
                                        -np.Inf * u.dimensionless_unscaled,
                                        snr_critic_db=10 * np.log10(_f_95 - 1),
                                        snr_critic=_f_95 - 1,
                                        f_critic=_f_95,
                                        channel=_channel,
                                        **kwargs)
            _test_data.append(test)
    return _test_data


def f_test(samples=np.array([]),
           snr: np.array([]) = None,
           df_noise: np.array([]) = None,
           alpha: float = 0.05
           ) -> (float, float, float, float, float):
    """
    Compute F-Test for input samples.
    The degrees of freedom for signal are estimated from the frequency-domain.
    The assumption is similar to that used by effective_sampling_size with weighted average.
    A full white spectrum will have all degrees of freedoms which in the time-domain will correspond to the number of
    time points.
    When data are correlated (e.g., when data is filtered or because of un underlying signal), degrees of freedom will
    be reduced. This will be reflected by the relative energy in the spectrum. Thus, the estimation produces estimated
    degrees of freedom between zeros and the number of time x samples by weighting the spectral energy.
    Donelan, Mark, and Willard J. Pierson. 1983. “The Sampling Variability of Estimates of Spectra of Wind-Generated
    Gravity Waves.” Journal of Geophysical Research: Oceans 88 (C7): 4381–92. https://doi.org/10.1029/JC088iC07p04381.
    Medina, Josep R., José Aguilar, and J. Javier Diez. 1985. “Distortions Associated with Random Sea Simulators.”
    Journal of Waterway, Port, Coastal, and Ocean Engineering 111 (4): 603–28.
    https://doi.org/10.1061/(ASCE)0733-950X(1985)111:4(603).

    :param samples: numpy array with samples to perform the test (time x channels)
    :param df_noise: The estimated degrees of freedom of the noise used to estimate the input SNR
    :param snr: signal-to-noise ratio for each channel
    :param alpha: the statistical level for significance
    :return: pandas data frame with statistical tests
    """

    _fft_power = np.abs(np.fft.rfft(samples, axis=0)) ** 2
    df_signal = 2 * effective_sampling_size(_fft_power, axis=0) - 1
    df_num = df_signal
    df_den = df_noise
    f_value = snr + 1
    f_critic = st.f.ppf(1 - alpha, df_num, df_den)
    p_value = 1 - st.f.cdf(f_value, df_num, df_den)

    return f_value, f_critic, df_num, df_den, p_value


def phase_locking_value(
        data: np.array = None,
        alpha: float = 0.05,
        weights: np.array = None,
        eps: np.float = np.finfo(float).eps) -> np.array:
    """
    Compute phase-locking value (PLV) using Rayleigh test
    :param data: time x channels x trials numpy array in the time domain
    :param alpha: float indicating the alpha value for significance
    :param weights: trial by trial weights
    :param eps: machine numerical precision used to prevent dividing by zero
    :return: phase-locking value (frequency x channels), z-scores (frequency x channels), z_critic (float), p_values
    (frequency x channels), mean angles (frequency x channels in rads), degrees of freedom, residual_noise estimation
    """
    if weights is None:
        weights = np.ones(data.shape)
    _dof = effective_sampling_size(weights)
    # for the moment we assume that the same weight across time is applied so that it can be factor out from fft
    dof = np.min(_dof, axis=0, keepdims=False).squeeze()[None, :]
    _weights = np.min(weights, axis=0)[None, :, :]
    yfft = np.fft.rfft(data, axis=0)
    spectral_mean = w_mean(yfft, _weights)
    diff = yfft - spectral_mean[:, :, None]
    # compute weighted standard deviation
    noise = np.sqrt(w_mean(np.abs(diff) ** 2, _weights) / dof)
    # scale to match time domain amplitudes
    spectral_amp = 2 * np.abs(spectral_mean) / data.shape[0]
    residual_noise = 2 * np.abs(noise) / data.shape[0]
    # normalize using Tikhonov regularization
    yfft = yfft / np.sqrt(np.abs(yfft * np.conj(yfft) + eps))
    angles = np.angle(w_mean(yfft, _weights))
    plv = np.abs(w_mean(yfft, _weights))
    z = dof * plv ** 2

    # D.Wilkie. Rayleigh Test for Randomness of Circular Data".Applied Statistics.1983.
    tmp = np.ones(z.shape)
    _idx_tmp = (dof < 50).squeeze()

    if np.any(_idx_tmp):
        _tmp_coorection = 1.0 + (2.0 * z - z * z) / (4.0 * dof) - (
                24.0 * z - 132.0 * z ** 2.0 + 76.0 * z ** 3.0 - 9.0 * z ** 4.0) / (288.0 * dof * dof)
        tmp[:, _idx_tmp] = _tmp_coorection
    z_crit = -np.log(alpha) - (2 * np.log(alpha) + np.log(alpha) ** 2.0) / (4 * dof)
    p_values = np.exp(-z) * tmp

    return spectral_amp, plv, z, z_crit, p_values, angles, dof, residual_noise


def discrete_phase_locking_value(
        data: np.array = None,
        alpha: float = 0.05,
        fs: float = None,
        frequency: float = None,
        weights: np.array = None) -> np.array:
    """
    Compute spectral amplitude, phase, and  phase-locking value (PLV) using Rayleigh test for a single frequency
    component.
    :param data: time x channels x trials numpy array in the time domain
    :param alpha: float indicating the alpha value for significance
    :param fs: float indicating the sampling rate in Hz
    :param frequency: float indicating the frequency of interest
    :param weights: trial by trial weights
    :return: phase-locking value (frequency x channels), z-scores (frequency x channels), z_critic (float), p_values
    (frequency x channels), mean angles (frequency x channels in rads), degrees of freedom, residual_noise estimation
    """
    if weights is None:
        weights = np.ones((1, data.shape[1], data.shape[2]))
    _dof = effective_sampling_size(weights)
    # for the moment we assume that the same weight across time is applied so that it can be factor out from fft
    dof = np.min(_dof, axis=0, keepdims=False).squeeze()[None, :]

    yfft, exact_frequency = goertzel(data, fs, frequency)
    spectral_amp = np.abs(np.sum(yfft * weights, axis=2) / np.sum(weights, axis=2))
    diff = yfft - spectral_amp[:, :, None]
    noise = np.sqrt(np.var(diff, axis=2) / dof)
    # scale to match time domain amplitudes
    spectral_amp = 2 * spectral_amp / data.shape[0]
    residual_noise = 2 * noise / data.shape[0]
    yfft = yfft / np.abs(yfft)
    angles = np.angle(np.sum(yfft * weights, axis=2) / np.sum(weights, axis=2))
    plv = np.abs(np.sum(yfft * weights, axis=2) / np.sum(weights, axis=2))
    z = dof * plv ** 2
    # D.Wilkie. Rayleigh Test for Randomness of Circular Data".Applied Statistics.1983.
    tmp = np.ones(z.shape)
    _idx_tmp = (dof < 50).squeeze()

    if np.any(_idx_tmp):
        _tmp_coorection = 1.0 + (2.0 * z - z * z) / (4.0 * dof) - (24.0 * z - 132.0 * z ** 2.0 +
                                                                   76.0 * z ** 3.0 - 9.0 * z ** 4.0) / (
                                      288.0 * dof * dof)
        tmp[:, _idx_tmp] = _tmp_coorection
    z_crit = -np.log(alpha) - (2 * np.log(alpha) + np.log(alpha) ** 2.0) / (4 * dof)
    p_values = np.exp(-z) * tmp

    return spectral_amp, plv, z, z_crit, p_values, angles, dof, residual_noise


def get_discrete_frequency_value(
        data: np.array = None,
        fs: float = None,
        frequency: float = None,
        weights: np.array = None) -> np.array:
    """
    Compute spectral amplitude for a single frequency
    component.
    :param data: time x channels x trials numpy array in the time domain
    :param alpha: float indicating the alpha value for significance
    :param fs: float indicating the sampling rate in Hz
    :param frequency: float indicating the frequency of interest
    :param weights: trial by trial weights
    :return: frequency amplitudes
    """
    if weights is None:
        weights = np.ones((data.shape[1], data.shape[2]))
    _dof = effective_sampling_size(weights)
    # for the moment we assume that the same weight across time is applied so that it can be factor out from fft
    dof = np.min(_dof, axis=0, keepdims=False).squeeze()[None, :]

    yfft = goertzel(data, fs, frequency)

    spectral_amp = np.abs(np.sum(yfft * weights, axis=2) / np.sum(weights, axis=1))
    diff = yfft - spectral_amp[:, :, None]
    noise = np.sqrt(np.var(diff, axis=2) / dof)
    # scale to match time domain amplitudes
    spectral_amp = 2 * spectral_amp / data.shape[0]
    residual_noise = 2 * noise / data.shape[0]
    yfft = 2 * yfft / data.shape[0]
    return yfft, spectral_amp, residual_noise


def freq_bin_phase_locking_value(
        yfft: np.array = None,
        alpha: float = 0.05,
        weights: np.array = None) -> np.array:
    """
    Compute phase, and  phase-locking value (PLV) using Rayleigh test for an array of trials from a single frequency
    component.
    :param yfft: fft_bin (complex) x channels x trials numpy array in the time domain
    :param alpha: float indicating the alpha value for significance
    :param frequency: float indicating the frequency of interest
    :param weights: trial by trial weights
    :return: phase-locking value (frequency x channels), z-scores (frequency x channels), z_critic (float), p_values
    (frequency x channels), mean angles (frequency x channels in rads), degrees of freedom, residual_noise estimation
    """

    if weights is None:
        weights = np.ones((yfft.shape[1], yfft.shape[2]))
    _dof = effective_sampling_size(weights)
    # for the moment we assume that the same weight across time is applied so that it can be factor out from fft
    dof = np.min(_dof, axis=0, keepdims=False).squeeze()[None, :]

    spectral_amp = np.abs(np.sum(yfft * weights, axis=2) / np.sum(weights, axis=1))
    diff = yfft - spectral_amp[:, :, None]
    noise = np.sqrt(np.var(diff, axis=2) / dof)
    residual_noise = noise
    # scale to match time domain amplitudes
    yfft = yfft / np.abs(yfft)
    angles = np.angle(np.sum(yfft * weights, axis=2) / np.sum(weights, axis=1))
    plv = np.abs(np.sum(yfft * weights, axis=2) / np.sum(weights, axis=1))
    z = dof * plv ** 2

    # D.Wilkie. Rayleigh Test for Randomness of Circular Data".Applied Statistics.1983.
    tmp = 1.0
    if (dof < 50):
        tmp = 1.0 + (2.0 * z - z * z) / (4.0 * dof) - (24.0 * z - 132.0 * z ** 2.0 +
                                                       76.0 * z ** 3.0 - 9.0 * z ** 4.0) / (288.0 * dof * dof)
    z_crit = -np.log(alpha) - (2 * np.log(alpha) + np.log(alpha) ** 2.0) / (4 * dof)
    p_values = np.exp(-z) * tmp

    return spectral_amp, plv, z, z_crit, p_values, angles, dof, residual_noise
