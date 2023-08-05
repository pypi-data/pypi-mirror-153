# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 10:55:37 2014

@author: jundurraga-ucl
"""
from peegy.processing.tools import epochs_processing_tools as ept
import numpy as np
import matplotlib.pyplot as plt

# create synthetic data
fs = 4000.0
nsamples = np.round(1 * fs).astype(np.int)
nchans = 36
ntrials = 130
noise_dim = 36  # dimensionality of noise
f1 = 40
f2 = 8
t = np.arange(nsamples) / fs
source = np.expand_dims(np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t), axis=1)
coeff = np.ones(nchans//2) * 0.5 / (nchans / 2)
coeff = np.expand_dims(np.hstack((coeff, coeff)), 0)

s = source * coeff
s_std = np.std(s, axis=0)
s = np.tile(np.expand_dims(s, axis=2), (1, 1, ntrials))

desired_snr = 5.0
ini_std = 10.0 ** (-desired_snr / 20.0) * s_std * ntrials ** 0.5
theoretical_rn = ini_std / ntrials ** 0.5

# noise = np.random.normal(0, ini_std[0], size=(nsamples, nchans, ntrials))
noise = np.random.power(0.5, size=(nsamples, nchans, ntrials))
s[:, 0] = s[:, 0] * 0.5
data = noise + s


w_ave, w, rn, cumulative_rn, snr, cumulative_snr, s_var, w_fft, nk = ept.et_weighted_mean(epochs=data,
                                                                                          block_size=10,
                                                                                          samples_distance=10
                                                                                          )
across_channels_ave, total_rn, total_snr, t_s_var = \
    ept.et_snr_weighted_mean(averaged_epochs=w_ave, fs=fs, rn=rn, snr=np.max(snr, axis=0))

# fig = plt.figure()
# ax = fig.add_subplot(131)
# ax.plot(np.mean(s, axis=2))
# ax = fig.add_subplot(132)
# ax.plot(w_ave)
# ax = fig.add_subplot(133)
# ax.plot(across_channels_ave)
# plt.show()

freq = np.arange(0, w_fft.shape[0]) * fs / w_ave.shape[0]
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.plot(freq, np.abs(w_fft))
# plt.show()

# moving averaging

data2 = data.transpose(2, 0, 1).reshape(-1, data.shape[1])
Nw = int(4 * 1. / f2 * fs)
k = data.shape[0] // Nw
new_epoch_number = k * data.shape[2] - k
new_epochs = np.zeros((data.shape[0], data.shape[1], new_epoch_number))
for _i in range(new_epoch_number):
    _ini_pos = int(round(_i * Nw))
    _end_pos = _ini_pos + data.shape[0]
    if _end_pos >= data2.shape[0]:
        break
    new_epochs[:, :, _i] = data2[_ini_pos:_end_pos, :]


w_ave_2, w_2, rn_2, cumulative_rn_2, snr_2, cumulative_snr_2, s_var_2, w_fft_2, nk_2 = \
    ept.et_weighted_mean(epochs=new_epochs,
                         block_size=10,
                         samples_distance=10)

fig = plt.figure()
ax = fig.add_subplot(131)
ax.plot(np.mean(s, axis=2))
ax = fig.add_subplot(132)
ax.plot(w_ave)
ax = fig.add_subplot(133)
ax.plot(w_ave_2)
plt.show()

# [f, px] = welch(data2, fs=fs, window='blackman', nperseg=4000., noverlap=1000., nfft=4000., detrend='constant',
#                 return_onesided=True, scaling='spectrum', axis=0)

freq = np.arange(0, w_fft.shape[0]) * fs / w_ave.shape[0]
fig = plt.figure()
ax = fig.add_subplot(121)
ax.plot(freq, np.abs(w_fft[:, 0]))
ax.plot(freq, np.abs(w_fft_2[:, 0]))
# ax.plot(f, px[:, 0]**0.5)
ax.plot(freq, 2*np.abs(np.fft.fft(s[:, 0, 1])[np.arange(0, w_fft.shape[0])])/s.shape[0])
plt.show()

fig = plt.figure()
ax = fig.add_subplot(121)
ax.plot(s[:, 0, 1])
ax.plot(w_ave[:, 0])
ax = fig.add_subplot(122)
ax.plot(s[:, 0, 1])
ax.plot(w_ave_2[:, 0])
plt.show()
