"""
.. _tut-acc-sim:

Test spatial filtering with evoked response (Simulation)
==============================

This example simulates an evoked responses with non-stationary noise.
We illustrate how weighted averaging and DSS can lead to much better results in terms of recovering the data.
This example follows that by Alain de Cheveigné (http://audition.ens.fr/adc/NoiseTools/) but it has been extended
to include non-stationary noise and weighted average.
.. contents:: Page contents
   :local:
   :depth: 2
"""
import matplotlib.pyplot as plt
from peegy.processing.tools.eeg_epoch_operators import et_mmat
from peegy.processing.tools.epochs_processing_tools import et_mean, et_frequency_mean2
import numpy as np
from scipy.stats import norm
from astropy import units as u
# Enable below for interactive backend
import matplotlib
if 'Qt5Agg' in matplotlib.rcsetup.all_backends:
    matplotlib.use('Qt5Agg')
__author__ = 'jundurraga'

# create synthetic data
nsamples = 500 * 3
nchans = 10
ntrials = 300
noise_dim = 20  # dimensionality of noise
freq = 100
fs = 1000

source = np.concatenate((
    np.zeros((nsamples // 3, )),
    np.sin(2 * np.pi * np.arange(nsamples / 3) / fs * freq),
    np.zeros((nsamples // 3, ))))

# source = np.sin(2 * np.pi * np.arange(nsamples) / fs * freq)

np.random.seed(2)
mix_m = norm.ppf(np.random.rand(nchans, 1))
s = source * mix_m
s = np.tile(np.expand_dims(s.T, axis=2), (1, 1, ntrials))
SNR = 0.5

noise_unmixed = norm.ppf(np.random.rand(noise_dim * ntrials * nsamples))
noise_unmixed = np.reshape(noise_unmixed, [nsamples, noise_dim, ntrials], order='F')

noise_mix = norm.ppf(np.random.rand(nchans * noise_dim))
noise_mix = np.reshape(noise_mix, [noise_dim, nchans], order='F')
noise = et_mmat(noise_unmixed, noise_mix)

scaled_source = SNR * s * u.uV / np.std(s)
scaled_noise = noise * u.uV / np.std(noise)
block_size = 20
# generate non-stationary noise
for i in np.arange(1, 4):
    _ini = i*20
    _end = _ini + 10
    scaled_noise[:, :, _ini: _end] += 0.5e2 * i * scaled_noise[:, :, _ini: _end]

# mix data
data = scaled_noise + scaled_source
frequencies = freq * (1 + np.arange(1))

rn_w_vector = []
rn_s_vector = []
real_rn_w_vector = []
real_rn_s_vector = []
snr_w_vector = []
snr_s_vector = []
snr_w_dss_vector = []
real_snr_w_vector = []
real_snr_s_vector = []
ave_source, source_w, source_rn, _, source_fft, n, *_ = et_mean(scaled_source, block_size=block_size)
freq_axis = np.arange(0, ave_source.shape[0]) * fs / ave_source.shape[0]
scaling_factor = 2 / data.shape[0]
_idx_freq = np.argmin(np.abs(freq_axis - freq))
target_amp = np.abs(np.fft.fft(ave_source, axis=0))[_idx_freq, :] * scaling_factor
delta_freq = 3
for _n in np.arange(block_size, data.shape[2], block_size):
    subset = np.copy(data)[:, :, 0: _n]

    # standard averaging of the data
    s_ave, s_snr, s_rn, s_rn_fre, s_snr_freq, s_fft, w_s, _, _ = et_frequency_mean2(subset,
                                                                                    fs=fs,
                                                                                    block_size=block_size,
                                                                                    weighted_average=False,
                                                                                    test_frequencies=frequencies,
                                                                                    delta_frequency=delta_freq)
    # weighted averaging of the data
    w_ave, w_snr, w_rn, w_rn_freq, w_snr_freq, w_fft, w_w, _, _ = et_frequency_mean2(subset,
                                                                                     fs=fs,
                                                                                     block_size=block_size,
                                                                                     weighted_average=True,
                                                                                     test_frequencies=frequencies,
                                                                                     delta_frequency=delta_freq)

    # compute actual residual noise by subtracting the source signal
    real_noise_standard_ave = ave_source - s_ave
    real_noise_weighted_ave = ave_source - w_ave

    fft_noise_standard_ave = np.abs(np.fft.fft(real_noise_standard_ave, axis=0)) * scaling_factor
    fft_noise_weighted_ave = np.abs(np.fft.fft(real_noise_weighted_ave, axis=0)) * scaling_factor

    rn_s_vector.append(s_rn)
    rn_w_vector.append(w_rn)

    _real_noise_s_ave = fft_noise_standard_ave[_idx_freq, :]
    _real_noise_w_ave = fft_noise_weighted_ave[_idx_freq, :]

    real_rn_s_vector.append(_real_noise_s_ave)
    real_rn_w_vector.append(_real_noise_w_ave)

    snr_s_vector.append(s_snr)
    snr_w_vector.append(w_snr)

    real_snr_s_vector.append(target_amp ** 2 / _real_noise_s_ave ** 2)
    real_snr_w_vector.append(target_amp ** 2 / _real_noise_w_ave ** 2)

# plot noise
plt.figure()
plt.plot(real_rn_s_vector, 'k')
plt.plot(rn_s_vector, 'b')

plt.figure()
plt.plot(real_rn_w_vector, 'k')
plt.plot(rn_w_vector, 'b')


# plot snr
n_epochs = np.arange(block_size, data.shape[2], block_size)
plt.figure()
plt.plot(n_epochs, 10 * np.log10(real_snr_s_vector), 'k')
plt.plot(n_epochs, 10 * np.log10(snr_s_vector), 'b')

noise_sample = scaled_noise[0, 0, :]
plt.plot(noise_sample / np.abs(noise_sample).max())
w_sample = w_s[0, 0, :]
plt.plot(w_sample / np.max(w_sample), 'g')

plt.figure()
plt.plot(n_epochs, 10 * np.log10(real_snr_w_vector), 'k')
plt.plot(n_epochs, 10 * np.log10(snr_w_vector), 'b')
plt.plot(noise_sample / np.abs(noise_sample).max())
w_sample = w_w[0, 0, :]
plt.plot(w_sample / np.max(w_sample), 'g')

plt.show()
