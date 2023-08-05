"""
This example uses an estimation of the impulse response in order to estimate and subtract the stimulus artifact.
Here we use a noise as the stimulus and its envelope plus a delay as the brain response.
"""
import numpy as np
import matplotlib.pyplot as plt
from peegy.processing.tools.epochs_processing_tools import et_xcorr_subtraction
from peegy.processing.tools.filters.eegFiltering import bandpass_fir_win, ols_filt_filt

fs = 16384.0
epoch_length = 1.0
epoch_length = np.ceil(epoch_length * fs) / fs  # fit to fs rate
burst_duration = 0.375
ffr_frequencies = np.array([120, 240, 360, 480, 600.0])
ffr_frequencies = np.ceil(burst_duration * ffr_frequencies) / burst_duration  # fit to burst_duration length
alternating_polarity = False  # stimulus is alternating in polarity every presentation
# here we pick some random frequencies to test statistical detection
random_frequencies = np.unique(np.random.randint(100, 400, 3))
stim_delay = 0.001  # neural delay in secs
brain_delay = 0.0237
time = np.arange(0, burst_duration, 1 / fs).reshape(-1, 1)
# stimulation waveform
_original_stimulus_waveform = np.sum(
    3 * np.sin(2 * np.pi * ffr_frequencies * time),
    axis=1).reshape(-1, 1) * 1.0  # generates ffr artifacts with 1 uV amplitude
stimulus_waveform = np.pad(_original_stimulus_waveform, ((0, int(fs * brain_delay) + int(fs * stim_delay)),
                                                         (0, 0)), 'constant', constant_values=(0, 0))

# apply delay to leaked stimulus (assuming system delay)
_leak_stimulus = np.pad(_original_stimulus_waveform, ((int(fs * stim_delay), int(fs * brain_delay)),
                                                      (0, 0)), 'constant', constant_values=(0, 0))
# brain response
template_waveform = np.pad(_original_stimulus_waveform, ((int(fs * stim_delay) + int(fs * brain_delay), 0), (0, 0)),
                           'constant', constant_values=(0, 0))
_b_brain = bandpass_fir_win(high_pass=60, low_pass=800, fs=fs)
template_waveform = ols_filt_filt(b=_b_brain, x=template_waveform)
template_waveform *= 0.2  # 0.2 uV amplitude and a delay
template_waveform[template_waveform < 0] = 0  # rectify

# leaked artifact
_b = bandpass_fir_win(0.1, 1000, fs=fs)
_leak_stimulus = ols_filt_filt(b=_b, x=_leak_stimulus)

# scale respective signals
template_waveform *= 0.2
_leak_stimulus *= 1.0

# generate recorded data including brain, leaked artifact and noise
snr = 0  # dB
np.random.seed(2)
noise = 10 ** (-snr/20) * np.random.randn(template_waveform.size, 1) * np.std(template_waveform)

recorded_waveform = template_waveform + _leak_stimulus + noise

# # zero padding
stimulus_waveform = np.pad(stimulus_waveform, ((0, 0*stimulus_waveform.shape[0]),
                                               (0, 0)), 'constant', constant_values=(0, 0))
recorded_waveform = np.pad(recorded_waveform, ((0, 0*recorded_waveform.shape[0]),
                                               (0, 0)), 'constant', constant_values=(0, 0))

# plot stimuli, brain and leaked artifact
plt.plot(stimulus_waveform, label='input waveform')
plt.plot(recorded_waveform, label='recorded data')
plt.plot(_leak_stimulus, label='leaked artifact')
plt.plot(template_waveform, label='brain response')
plt.legend()
plt.show()

# remove artifacts
_recovered_response, _recovered_artifact = et_xcorr_subtraction(
    data=np.atleast_3d(recorded_waveform),
    stimulus_waveform=stimulus_waveform,
    max_lag=50,
    max_length=200,
    plot_results=False)

# apply filter to extract neural bandwidth
_recovered_response = ols_filt_filt(b=_b_brain, x=_recovered_response)

# apply filter to extract neural response without removing artifact
_contaminated_response = ols_filt_filt(b=_b_brain, x=recorded_waveform)

# apply filter to extract neural response without removing artifact
_filtered_artifact = ols_filt_filt(b=_b_brain, x=_leak_stimulus)


# plot artifact
plt.figure()
plt.plot(_leak_stimulus, label='target artifact')
plt.plot(_recovered_artifact.flatten(), label='recovered artifact')
plt.legend()
plt.show()

# plot response
plt.figure()
plt.plot(_contaminated_response, label='contaminated response Corr: {:}'.format(
    np.corrcoef(template_waveform.flatten(),
                _contaminated_response[0:template_waveform.shape[0]].flatten())[-1, 0]))

plt.plot(_filtered_artifact, label='leaked artifact response Corr: {:}'.format(
    np.corrcoef(template_waveform.flatten(),
                _filtered_artifact[0:template_waveform.shape[0]].flatten())[-1, 0]))

plt.plot(template_waveform, label='target response')

plt.plot(_recovered_response.flatten(), label='recovered response. Corr: {:}'.format(
    np.corrcoef(template_waveform.flatten(),
                _recovered_response[0:template_waveform.shape[0]].flatten())[-1, 0]))
plt.legend()
plt.show()
