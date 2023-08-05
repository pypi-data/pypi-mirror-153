from peegy.processing.tools.epochs_processing_tools import et_subtract_correlated_ref, filt_data
from peegy.processing.tools.template_generator.auditory_waveforms import eog
import numpy as np
import matplotlib.pyplot as plt
import numpy.matlib

n_ch = 10
fs = 16384.0
recording_time = 16
eog_rate = 1 / 4
time = np.arange(0, 4, 1/fs)
n_trials = 10
# we generate a fake low frequency artefact signal and generate a mixing matrix
time = np.arange(0, recording_time, 1/fs)
n_samples = time.size
time_artefact = np.arange(0, 1/3, 1/fs)
n_events = int(recording_time // (1 / eog_rate))
# we generate a fake low frequency artefact signal and generate a mixing matrix
eog1_template, _ = eog(fs)
eog1mix = np.zeros((n_samples, n_ch, n_trials))
for _t in np.arange(n_trials):
    events = np.zeros(n_samples, )
    _intervals = 1 / eog_rate + 0.5 * np.random.randn(n_events, )
    event_times = np.cumsum(_intervals)
    event_times = event_times[event_times < recording_time]
    _idx = np.minimum(event_times * fs, n_samples - 1).astype(np.int)
    events[_idx] = 1 + 0.5 * np.random.rand(_idx.size)
    eog1 = filt_data(eog1_template.reshape(-1, 1), events.flatten(), mode='full').flatten()
    eog1 = eog1[0: n_samples]
    w1 = np.random.rand(1, n_ch)
    w1[0, -1] = 1
    eog1mix[:, :, _t] = np.matlib.repmat(eog1, n_ch, 1).T * w1

# generate EEG data at a higher frequency
ep = np.sin(2 * np.pi * 137.0 * time)
w3 = np.random.rand(1, n_ch)
epochs = np.matlib.repmat(ep, n_ch, 1).T * w3
epochs = np.expand_dims(epochs, axis=2) * np.ones((ep.size, n_ch, n_trials))
epochs[:, -1, :] = 0

# generate noise and mixing matrix
noise = 0.5 * np.random.randn(n_samples, n_ch, n_trials)
data = epochs + noise + eog1mix
orig = data.copy()
# remove artefacts
clean_data = et_subtract_correlated_ref(data=data, idx_ref=np.array([n_ch - 1]), fs=fs)

# get frequency responses
freq = np.arange(0, time.size) * fs / time.size
yfft_data = np.abs(np.fft.fft(orig, axis=0))
yfft_clean = np.abs(np.fft.fft(clean_data, axis=0))

fig = plt.figure()
ax = fig.add_subplot(221)
ax.plot(time, np.squeeze(orig[:, 0, :]), )
ax.set_title('contaminated')
ax = fig.add_subplot(222)
ax.plot(freq, np.squeeze(yfft_data[:, 0, :]))
ax.set_title('contaminated fft')
ax.set_xlim(0, 200)
ax = fig.add_subplot(223)
ax.plot(np.squeeze(clean_data[:, 0, :]))
ax.set_title('clean')
ax = fig.add_subplot(224)
ax.plot(freq, np.squeeze(yfft_clean[:, 0, :]))
ax.set_title('clean fft')
ax.set_xlim(0, 200)
fig.legend()
fig.show()
plt.show()
