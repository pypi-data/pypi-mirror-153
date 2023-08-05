import matplotlib.pyplot as plt
import numpy as np
import peegy.processing.tools.filters.spatial_filtering as sf
import peegy.processing.tools.eeg_epoch_operators as eo
__author__ = 'jundurraga-ucl'
# create synthetic data
fs = 44100.0
nsamples = int(np.round(1 * fs))
nchans = 36
ntrials = 100
noise_dim = 36  # dimensionality of noise
f1 = 40
source = np.expand_dims(np.sin(2 * np.pi * f1 * np.arange(nsamples) / fs + 3*np.pi/2), axis=1)
coeff = np.arange(nchans/2) * 0.5 / (nchans / 2)
coeff = np.expand_dims(np.hstack((coeff, -coeff)), 0)

# s = source * np.random.normal(0, 0.1, size=(1, nchans))
s = source * coeff
s = np.tile(np.expand_dims(s, axis=2), (1, 1, ntrials))
SNR = 10
noise = np.random.normal(0, 0.1, size=(nsamples, nchans, ntrials))
n_source = SNR * s / np.std(s)
data = noise / np.std(noise) + n_source

c0, c1 = sf.nt_bias_fft(data, np.array([f1]) / fs)

todss, pwr0, pwr1 = sf.nt_dss0(c0, c1)
z = eo.et_mmat(data, todss)
n_components = np.arange(1)
cov_1 = eo.et_x_covariance(z, data)
data_clean = eo.et_mmat(z[:, n_components, :], cov_1[n_components, :])

ax = plt.subplot(131)
ax.plot(np.mean(n_source, axis=2))
ax = plt.subplot(132)
ax.plot(np.mean(data, axis=2))
ax = plt.subplot(133)
ax.plot(np.mean(data_clean, axis=2))
plt.show()
