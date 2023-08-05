# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 10:55:37 2014

@author: jundurraga-ucl
"""
from peegy.processing.tools import epochs_processing_tools as ept
from peegy.processing.tools.eeg_epoch_operators import w_mean
import numpy as np
import matplotlib.pyplot as plt
# create synthetic data
fs = 1000.0
nsamples = np.round(1 * fs).astype(int)
nchans = 36
ntrials = 130
noise_dim = 36  # dimensionality of noise
f1 = 40
source = np.expand_dims(np.sin(2 * np.pi * f1 * np.arange(nsamples) / fs - np.pi / 4), axis=1)
coeff = np.ones(nchans//2) * 0.5 / (nchans / 2)
coeff = np.expand_dims(np.hstack((coeff, coeff)), 0)

s = source * coeff
s_std = np.std(s, axis=0)
s = np.tile(np.expand_dims(s, axis=2), (1, 1, ntrials))

desired_snr = 1
ini_std = 10.0 ** (-desired_snr / 20.0) * s_std * ntrials ** 0.5
theoretical_rn = ini_std / ntrials ** 0.5

noise = np.random.normal(0, ini_std[0], size=(nsamples, nchans, ntrials))
data = noise + s * 1
w, y_fft, rn, snr = ept.get_discrete_frequency_weights(
    epochs=data,
    block_size=10,
    fs=fs,
    frequency=f1,
    weighted_average=True
)

time_wa = w_mean(data, weights=w)
freq_wa = np.abs(np.fft.rfft(time_wa, axis=0)) / time_wa.shape[0]
freq_source = np.abs(np.fft.rfft(np.mean(s, axis=2), axis=0)) / s.shape[0]
diff = (y_fft - np.atleast_3d(w_mean(y_fft, weights=w[0, :, :])))
noise = np.sqrt(np.abs(np.mean(diff ** 2.0, axis=2))) / (time_wa.shape[0] * np.sqrt(diff.shape[2]))
freq = np.arange(0, freq_wa.shape[0]) * fs / time_wa.shape[0]
fig = plt.figure()
ax = fig.add_subplot(131)
ax.plot(freq, freq_wa)
# ax.plot(freq, freq_source)
ax.plot(f1, np.abs(w_mean(y_fft, weights=w[0, :, :])) / time_wa.shape[0], 'o')
[ax.axhline(y=_n.value) for _n in rn.squeeze() / time_wa.shape[0]]
plt.show()
