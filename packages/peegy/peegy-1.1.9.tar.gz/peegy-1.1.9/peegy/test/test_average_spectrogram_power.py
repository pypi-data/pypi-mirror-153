from peegy.processing.tools.epochs_processing_tools import et_average_time_frequency_transformation
import matplotlib.pyplot as plt
import numpy as np
__author__ = 'jaime.undurraga@gmail.com'

# create synthetic data
fs = 44100.0
nsamples = int(np.round(4 * fs))
nchans = 36
ntrials = 100
noise_dim = 36  # dimensionality of noise
f1 = 40
source = np.expand_dims(np.sin(2 * np.pi * f1 * np.arange(nsamples) / fs), axis=1)
coeff = np.arange(nchans/2) * 0.5 / (nchans / 2)
coeff = np.expand_dims(np.hstack((coeff, -coeff)), 0)

s = source * coeff
s = np.tile(np.expand_dims(s, axis=2), (1, 1, ntrials))
# apply jitter
temp_jitter = 1 / f1
for _i in range(s.shape[2]):
    _jitter = int(fs * temp_jitter * (np.random.rand() - 0.5) / 0.5)
    s[:, :, _i] = np.roll(s[:, :, _i], shift=_jitter, axis=0)
SNR = 0.5
noise = np.random.normal(0, 0.1, size=(nsamples, nchans, ntrials))
# noise[1000:12000, :, 30:70] = 20.0 * noise[1000:12000, :, 30:70]
n_source = SNR * s / np.std(s)
data = noise / np.std(noise) + n_source

power_1, time, freqs = et_average_time_frequency_transformation(epochs=data,
                                                                fs=fs,
                                                                time_window=0.5*nsamples/fs,
                                                                sample_interval=0.5*nsamples/fs,
                                                                ave_mode='magnitude'
                                                                )

power_2, time, freqs = et_average_time_frequency_transformation(epochs=data,
                                                                fs=fs,
                                                                time_window=0.5*nsamples/fs,
                                                                sample_interval=0.5*nsamples/fs,
                                                                ave_mode='complex'
                                                                )

thr = 35
_ch = 10
ax = plt.subplot(121)
power_1 = np.abs(power_1)
ref = power_1.max()
power_1 /= ref
p1 = 10*np.log10(power_1)
p1[p1 < -thr] = -thr
cax = ax.pcolormesh(time, freqs, np.squeeze(p1[:, _ch]), cmap=plt.get_cmap('viridis'))
ax.set_xlabel('Time [s]')
ax.set_ylim([0, 60])
ax.set_ylabel('Frequency [Hz]')
ax.set_xlabel('Time [s]')
ax.set_ylim([0, 60])
ax.set_ylabel('Frequency [Hz]')
plt.colorbar(cax)

ax = plt.subplot(122)
power_2 = np.abs(power_2)
power_2 /= ref
p2 = 10*np.log10(power_2)
p2[p2 < -thr] = -thr
cax = ax.pcolormesh(time, freqs, np.squeeze(p2[:, _ch]), cmap=plt.get_cmap('viridis'))
ax.set_xlabel('Time [s]')
ax.set_ylim([0, 60])
ax.set_ylabel('Frequency [Hz]')
plt.colorbar(cax)

plt.show()
