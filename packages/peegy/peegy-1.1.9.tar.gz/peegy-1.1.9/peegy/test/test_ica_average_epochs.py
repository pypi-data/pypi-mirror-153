# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 10:55:37 2014

@author: jundurraga-ucl
"""
from peegy.processing.tools import epochs_processing_tools as ept
import matplotlib.pyplot as plt
from peegy.processing.tools.eeg_epoch_operators import et_unfold, et_fold
import numpy as np

# ICA in 3 dimensions ##################
# Synthesise data
fs = 44100.0
nsamples = int(np.round(1 * fs))
nchans = 36
ntrials = 100
noise_dim = 36  # dimensionality of noise
f1 = 40
source = np.expand_dims(np.sin(2 * np.pi * f1 * np.arange(nsamples) / fs + 3 * np.pi / 2), axis=1)
coeff = np.arange(nchans / 2) * 0.5 / (nchans / 2)
coeff = np.expand_dims(np.hstack((coeff, -coeff)), 0)

# s = source * np.random.normal(0, 0.1, size=(1, nchans))
s = source * coeff
s = np.tile(np.expand_dims(s, axis=2), (1, 1, ntrials))
SNR = 10
noise = np.random.normal(0, 0.1, size=(nsamples, nchans, ntrials))
n_source = SNR * s / np.std(s)
data = noise / np.std(noise) + n_source

unf_data = et_unfold(data)

s_components, s_unmixing, s_mixing, s_pwr, whitening_m = ept.et_ica_epochs(data=unf_data,
                                                                           tol=1e-4,
                                                                           iterations=10)

components = et_fold(s_components, data.shape[0])
scomps = np.mean(components, axis=2)
plt.plot(scomps + np.arange(0, scomps.shape[1]) * scomps.max())
plt.show()

plt.show()
