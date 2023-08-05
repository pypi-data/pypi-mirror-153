import numpy as np
from peegy.processing.tools.filters import eegFiltering as eegf
import scipy.signal as signal
import time
import matplotlib.pyplot as plt

fs = 1000.0
f1 = 10.0
f2 = 43.0
low_pass = 50.0
high_pass = 40.0
low = 2 * low_pass / fs
high = 2 * high_pass / fs
t = np.arange(0, 7000000) / fs
s = np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)
data = np.tile(s, [12, 1]).T

# _b_l = eegf.bandpass_fir_win(fs=fs, low_pass=low_pass)
# w, h = signal.freqz(_b_l, worN=8000)
# plt.plot((w/np.pi)*fs*0.5, np.abs(h), linewidth=2)
# plt.xlabel('Frequency (Hz)')

# _b_l = eegf.bandpass_fir_win(fs=fs, high_pass=high_pass)
# w, h = signal.freqz(_b_l, worN=8000)
# plt.plot((w/np.pi)*fs*0.5, np.abs(h), linewidth=2)
# plt.xlabel('Frequency (Hz)')

_b_l = eegf.bandpass_fir_win(fs=fs, high_pass=high_pass, low_pass=low_pass)
w, h = signal.freqz(_b_l, worN=8000)
plt.plot((w/np.pi)*fs*0.5, np.abs(h), linewidth=2)
plt.xlabel('Frequency (Hz)')


_ori_data = data.copy()
filtered_data = eegf.filt_filt_worker_ovs(filtered_data=_ori_data.copy(), pos_ini=0, pos_end=None, b=_b_l)
filtered_data2 = eegf.filt_worker_ovs(filtered_data=_ori_data.copy(), pos_ini=0, pos_end=None, b=_b_l)
time1 = time.time()
filtered_signal_standard = signal.filtfilt(_b_l, 1, data, axis=0)
time2 = time.time()
print(('standard filter took %f [ms]' % ((time2-time1) * 1000.0)))
plt.figure()
plt.plot(t, _ori_data[:, 0], label='original')
plt.plot(t, filtered_data[:, 0], label='ovs_filt_filt')
plt.plot(t, filtered_signal_standard[:, 0], label='scipy_filt_filt')
plt.plot(t, filtered_data2[:, 0], label='ols_filt')
plt.legend()
plt.show()
