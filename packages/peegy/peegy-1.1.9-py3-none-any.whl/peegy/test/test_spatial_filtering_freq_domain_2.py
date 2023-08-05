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
import peegy.processing.tools.filters.spatial_filtering as sf
from peegy.processing.tools.eeg_epoch_operators import et_mmat, et_freq_shifted_xcovariance, \
    et_freq_weighted_cov
from peegy.processing.tools.epochs_processing_tools import et_mean, et_frequency_mean2
import numpy as np
import matplotlib.gridspec as gridspec
from scipy.stats import norm
__author__ = 'jundurraga'


def plot_covariances(covariances: [np.array] = None,
                     normalized=True):
    gs = gridspec.GridSpec(1, len(covariances))
    fig = plt.figure()
    for _i, _cov in enumerate(covariances):
        if normalized:
            _cxy = _cov[np.diag_indices_from(_cov)][None, :] ** 0.5
            _norm_cxy = _cxy.T.dot(_cxy)
            _cov = _cov / _norm_cxy
        ax = plt.subplot(gs[0, _i])
        maxis = ax.matshow(_cov)
        plt.colorbar(maxis)
    return fig


def plot_data_results(data_list: [np.array] = None, titles: [str] = None):
    gs = gridspec.GridSpec(1, len(data_list))
    fig = plt.figure()
    for _i, (_data, _title) in enumerate(zip(data_list, titles)):
        ax = plt.subplot(gs[0, _i])
        ax.plot(_data)
        ax.set_title(_title)
    return fig


# create synthetic data
nsamples = 500 * 3
nchans = 30
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

scaled_source = SNR * s / np.std(s)
scaled_noise = noise / np.std(noise)

# generate non-stationary noise
for i in np.arange(1, 4):
    _ini = i*20
    _end = _ini + 10
    scaled_noise[:, :, _ini: _end] += 1e4 * i * scaled_noise[:, :, _ini: _end]

# mix data
data = scaled_noise + scaled_source
frequencies = freq * (1 + np.arange(1))
# standard averaging of the data
s_ave, s_snr, s_rn, s_rn_fre, s_snr_freq, s_fft, s_w, _, _ = et_frequency_mean2(data,
                                                                                fs=fs,
                                                                                block_size=10,
                                                                                weighted_average=False,
                                                                                test_frequencies=frequencies)
# weighted averaging of the data
w_ave, w_snr, w_rn, w_rn_freq, w_snr_freq, w_fft, w_w, _, _ = et_frequency_mean2(data,
                                                                                 fs=fs,
                                                                                 block_size=10,
                                                                                 weighted_average=True,
                                                                                 test_frequencies=frequencies)

n_components = np.arange(1)

# clean data using weighted dss
n_freq = frequencies / fs
cref, tref = et_freq_weighted_cov(data, normalized_frequencies=n_freq, w=w_w)
c1, t1 = et_freq_weighted_cov(w_ave, normalized_frequencies=n_freq)
cref = cref / tref
c1 = c1 / t1
todss, pwr0, pwr1 = sf.nt_dss0(cref, c1, keep1=1e-5)
z0 = et_mmat(data, todss)
cov_1, tw_cov = et_freq_shifted_xcovariance(z0, data, wy=w_w, normalized_frequencies=n_freq)
cov_1 = cov_1 / tw_cov
data_clean0 = et_mmat(z0[:, n_components, :], cov_1[n_components, :])

# clean data using dss with standard average
cref, tref = et_freq_weighted_cov(data, normalized_frequencies=n_freq, w=s_w)
c1, t1 = et_freq_weighted_cov(s_ave, normalized_frequencies=n_freq)
cref = cref / tref
c1 = c1 / t1
todss, pwr0, pwr1 = sf.nt_dss0(cref, c1)
z1 = et_mmat(data, todss)
cov_1, tw_cov = et_freq_shifted_xcovariance(z1, data, wy=s_w, normalized_frequencies=n_freq)
cov_1 = cov_1 / tw_cov
data_clean1 = et_mmat(z1[:, n_components, :], cov_1[n_components, :])


# clean data using dss only on weighted average
cref, tref = et_freq_weighted_cov(data, normalized_frequencies=n_freq, w=s_w)
c1, t1 = et_freq_weighted_cov(w_ave, normalized_frequencies=n_freq)
cref = cref / tref
c1 = c1 / t1
todss, pwr0, pwr1 = sf.nt_dss0(cref, c1, keep1=1e-5)
z2 = et_mmat(data, todss)
cov_1, tw_cov = et_freq_shifted_xcovariance(z2, data, normalized_frequencies=n_freq, wy=s_w)
cov_1 = cov_1 / tw_cov
data_clean2 = et_mmat(z2[:, n_components, :], cov_1[n_components, :])

# plot the results

w_ave_0, *_ = et_mean(data_clean0, block_size=5, weighted=True)
w_ave_1, *_ = et_mean(data_clean1, block_size=5, weighted=True)
w_ave_2, *_ = et_mean(data_clean2, block_size=5, weighted=True)
w_ave_z0, *_ = et_mean(z0[:, 0:3, :], block_size=5, weighted=True)
w_ave_z1, *_ = et_mean(z1[:, 0:3, :], block_size=5, weighted=True)
w_ave_z2, *_ = et_mean(z2[:, 0:3, :], block_size=5, weighted=True)
w_ave_z0 = np.abs(np.fft.rfft(w_ave_0, axis=0))
w_ave_z1 = np.abs(np.fft.rfft(w_ave_1, axis=0))
w_ave_z2 = np.abs(np.fft.rfft(w_ave_2, axis=0))
plot_data_results([np.mean(scaled_source, axis=2),
                   s_ave,
                   w_ave,
                   w_ave_0,
                   w_ave_1,
                   w_ave_2,
                   w_ave_z0,
                   w_ave_z1,
                   w_ave_z2],
                  ['Target source',
                   'standard average',
                   'weighted average',
                   'w_cov & w_ave',
                   's_cov & s_ave',
                   's_cov & w_ave',
                   'components data_clean0',
                   'components data_clean1',
                   'components data_clean2',
                   ]
                  )
plt.show()
# plot weights and noise
plt.figure()
noise_sample = scaled_noise[0, 0, :]
plt.plot(noise_sample / np.abs(noise_sample).max())
w_w_sample = w_w[0, 0, :]
plt.plot(w_w_sample / np.max(w_w_sample))
plt.show()

# plot noise
plt.figure()
plt.plot(s_rn)
plt.plot(w_rn)
plt.show()

# plot snr
plt.figure()
plt.plot(s_snr)
plt.plot(w_snr)
plt.show()
