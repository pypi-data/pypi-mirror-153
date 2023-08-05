import numpy as np
import peegy.processing.tools.filters.eegFiltering as eegf
import scipy.signal as signal
import time
import matplotlib.pyplot as plt
fs = 44100.0
f1 = 30.0
f2 = 200.0
low_pass = 50.0
high_pass = 100.0
low = 2 * low_pass / fs
high = 2 * high_pass / fs
t = np.arange(0, 7000000) / fs
s = np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)
data = np.tile(s, [24, 1]).T

_b_l, _a_l = signal.butter(N=2, Wn=low, btype='lowpass', analog=False)
filtered_data = eegf.filt_filt_multithread(input_data=data, b=_b_l, a=_a_l)
plt.plot(t, data[:, 0])
plt.plot(t, filtered_data[:, 0])
plt.show()

_b_l, _a_l = signal.butter(N=2, Wn=high, btype='highpass', analog=False)
filtered_data = eegf.filt_filt_multithread(input_data=data, b=_b_l, a=_a_l)
plt.plot(t, data[:, 0])
plt.plot(t, filtered_data[:, 0])
plt.show()

time1 = time.time()
filtered_signal_l2 = signal.filtfilt(_b_l, _a_l, data, axis=0)
time2 = time.time()
print(('standard filter took %f [ms]' % ((time2-time1) * 1000.0)))
