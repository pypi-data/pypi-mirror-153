"""
Created on Tue Dec 16 10:55:37 2014

@author: jundurraga-ucl
"""
from peegy.processing.tools.template_generator.auditory_waveforms import abr
from peegy.tools.signal_generator.noise_functions import generate_modulated_noise
import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
# Enable below for interactive backend
import matplotlib
if 'Qt5Agg' in matplotlib.rcsetup.all_backends:
    matplotlib.use('Qt5Agg')

# create synthetic data
fs = 20000.0 * u.Hz
duration = 1000 * u.ms
n_channels = 1
source, _ = abr(fs=fs, time_length=duration)

white_noise = generate_modulated_noise(fs=fs.value,
                                       duration=duration.to(u.s).value,
                                       f_noise_low=100,
                                       f_noise_high=10000,
                                       attenuation=0,
                                       n_channels=n_channels)

pink_noise = generate_modulated_noise(fs=fs.value,
                                      duration=duration.to(u.s).value,
                                      f_noise_low=100,
                                      f_noise_high=10000,
                                      attenuation=3,
                                      n_channels=n_channels)

brown_noise = generate_modulated_noise(fs=fs.value,
                                       duration=duration.to(u.s).value,
                                       f_noise_low=100,
                                       f_noise_high=10000,
                                       attenuation=6,
                                       n_channels=n_channels)

psd_pink_noise = np.abs(np.fft.rfft(pink_noise, axis=0)) ** 2.0
psd_brown_noise = np.abs(np.fft.rfft(brown_noise, axis=0)) ** 2.0
psd_white_noise = np.abs(np.fft.rfft(white_noise, axis=0)) ** 2.0
freqs = np.fft.rfftfreq(pink_noise.shape[0], 1 / fs)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(freqs, 10 * np.log10(psd_pink_noise / psd_pink_noise.max()), color='pink', label='Pink')
ax.plot(freqs, 10 * np.log10(psd_brown_noise / psd_brown_noise.max()), color='brown', label='Brown')
ax.plot(freqs, 10 * np.log10(psd_white_noise / psd_white_noise.max()), color='black', label='White')
ax.set_xscale('log')
ax.set_ylabel("PSD")
ax.set_xlabel("Frequency")
ax.grid(True)
ax.legend()
ax.set_xlim(100, 10000)
ax.set_ylim(-50, 2)
plt.show()
