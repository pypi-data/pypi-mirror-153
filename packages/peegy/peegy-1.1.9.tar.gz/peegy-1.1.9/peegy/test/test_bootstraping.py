import matplotlib.pyplot as plt
from peegy.processing.tools.epochs_processing_tools import bootstrap
import numpy as np
__author__ = 'jundurraga-ucl'

# create synthetic data
fs = 44100.0
nsamples = int(np.round(1 * fs))
nchans = 16
ntrials = 100
noise_dim = 36  # dimensionality of noise
f1 = 40
source = np.expand_dims(np.sin(2 * np.pi * f1 * np.arange(nsamples) / fs), axis=1)
coeff = np.arange(nchans/2) * 0.5 / (nchans / 2)
coeff = np.expand_dims(np.hstack((coeff, -coeff)), 0)

s = source * coeff
s = np.tile(np.expand_dims(s, axis=2), (1, 1, ntrials))
SNR = 6
noise = np.random.normal(0, 0.1, size=(nsamples, nchans, ntrials))
n_source = SNR * s / np.std(s)
data = noise / np.std(noise) + n_source

mean, ci_low, ci_high = bootstrap(data=data, num_samples=1000)

ax = plt.subplot(111)
ax.plot(np.mean(n_source, axis=2)[:, 10])
ax = plt.subplot(111)
ax.plot(np.mean(data, axis=2)[:, 10])
ax = plt.subplot(111)
ax.plot(mean[:, 10])
ax.fill_between(x=np.arange(0, mean.shape[0]), y1=mean[:, 10], y2=ci_high[:, 10])
ax.fill_between(x=np.arange(0, mean.shape[0]), y1=ci_low[:, 10], y2=mean[:, 10])

plt.show()
