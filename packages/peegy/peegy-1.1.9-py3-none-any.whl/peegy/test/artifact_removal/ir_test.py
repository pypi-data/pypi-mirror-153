"""
This example uses an estimation of the impulse response in order to estimate and subtract the stimulus artifact.
Here we use a noise as the stimulus and its envelope plus a delay as the brain response.
"""
import numpy as np
import matplotlib.pyplot as plt
from peegy.processing.tools.epochs_processing_tools import et_impulse_response_artifact_subtraction
from peegy.processing.tools.filters.eegFiltering import bandpass_fir_win, ols_filt_filt
from peegy.processing.tools.template_generator.auditory_waveforms import artifact_and_brain_envelope

# first we generate a test signal
fs = 16384.0
burst_duration = 1  # seconds

# here we define desired parameters for brain and artifact
stim_delay = 0.001  # neural delay in secs
brain_delay = 0.113  # brain response delay

template_waveform, stimulus_waveform, leaked_stimulus = artifact_and_brain_envelope(
    fs=fs,
    stimulus_delay=stim_delay,
    brain_delay=brain_delay,
    duration=burst_duration,
    seed=0)

# generate recorded data including brain, leaked artifact and noise
snr = -10  # dB
np.random.seed(2)
noise = 10 ** (-snr/20) * np.random.randn(template_waveform.size, 1) * np.std(template_waveform)

recorded_waveform = template_waveform + leaked_stimulus + noise

# plot stimuli, brain and leaked artifact
plt.plot(stimulus_waveform, label='input waveform')
plt.plot(recorded_waveform, label='recorded data')
plt.plot(leaked_stimulus, label='leaked artifact')
plt.plot(template_waveform, label='brain response')
plt.legend()
plt.show()

# remove artifacts
_recovered_response, _recovered_artifact = et_impulse_response_artifact_subtraction(
    data=np.atleast_3d(recorded_waveform),
    stimulus_waveform=stimulus_waveform,
    ir_length=int(0.01*fs),
    ir_max_lag=int(0.005*fs),
    regularization_factor=1,
    plot_results=True)

# apply filter to extract neural bandwidth
_b_brain = bandpass_fir_win(high_pass=2, low_pass=80.0, fs=fs)
_recovered_response = ols_filt_filt(b=_b_brain, x=_recovered_response)

# apply filter to extract neural response without removing artifact
_contaminated_response = ols_filt_filt(b=_b_brain, x=recorded_waveform)

# apply filter to extract neural response without removing artifact
_filtered_artifact = ols_filt_filt(b=_b_brain, x=leaked_stimulus)


# plot artifact
plt.figure()
plt.plot(leaked_stimulus, label='target artifact')
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
