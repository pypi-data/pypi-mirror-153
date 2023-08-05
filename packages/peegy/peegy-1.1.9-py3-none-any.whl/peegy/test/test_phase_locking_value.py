# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 10:55:37 2014

@author: jundurraga-ucl
"""
from peegy.processing.statistics import eeg_statistic_tools as espt
import numpy as np
import matplotlib.pyplot as plt
# Enable below for interactive backend
# import matplotlib
# if 'Qt5Agg' in matplotlib.rcsetup.all_backends:
#    matplotlib.use('Qt5Agg')

# create synthetic data
fs = 1000.0
nsamples = np.round(1 * fs).astype(np.int)
nchans = 36
ntrials = 49
noise_dim = 300  # dimensionality of noise
f1 = 40
source = np.expand_dims(np.sin(2 * np.pi * f1 * np.arange(nsamples) / fs), axis=1)
coeff = np.ones(nchans//2) * 0.5 / (nchans / 2)
coeff = np.expand_dims(np.hstack((coeff, coeff)), 0)

s = source * coeff
s_std = np.std(s, axis=0)
s = np.tile(np.expand_dims(s, axis=2), (1, 1, ntrials))

desired_snr = 5.0
ini_std = 10.0 ** (-desired_snr / 20.0) * s_std * ntrials ** 0.5
theoretical_rn = ini_std / ntrials ** 0.5

noise = np.random.normal(0, ini_std[0], size=(nsamples, nchans, ntrials))
# s[:, 0] = s[:, 0] * 0.5
data = noise + s
testg = espt.goertzel(data, fs, frequency=40)
amp, plv, z, z_crit, p_value, angles, dof, rn = espt.phase_locking_value(data, alpha=0.001)
amp_2, plv_2, z_2, z_crit_2, p_value_2, angles_2, dof_2, rn_2 = espt.discrete_phase_locking_value(data,
                                                                                                  alpha=0.001,
                                                                                                  fs=fs,
                                                                                                  frequency=40)
noise_amp, noise_plv, noise_z, noise_z_crit, noise_p_value, noise_angles, noise_dof, noise_rn = \
    espt.phase_locking_value(noise, alpha=0.001)

plt.figure()
plt.plot(plv[40])
plt.plot(plv_2.T)

plt.figure()
plt.plot(angles[40])
plt.plot(angles_2.T)

plt.figure()
plt.plot(amp[40])
plt.plot(amp_2.T)
plt.plot(rn[40])
plt.plot(noise_amp[40])


plt.plot(rn_2.T)
plt.show()

freq = np.arange(0, plv.shape[0]) * fs / data.shape[0]
fig = plt.figure()
ax = fig.add_subplot(141)
ax.plot(source)

ax = fig.add_subplot(142)
ax.plot(freq, plv)

ax = fig.add_subplot(143)
ax.plot(freq, z)
[ax.axhline(_z) for _z in z_crit.squeeze()]

ax = fig.add_subplot(144, projection='polar')
significant = z > z_crit
ax.plot(angles[significant] + np.pi/2, plv[significant], 'o')
ax.plot(angles[40, :] + np.pi/2, plv[40, :], 'o', 'red')
plt.show()
