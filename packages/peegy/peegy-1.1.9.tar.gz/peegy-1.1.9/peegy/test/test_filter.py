# __author__ = 'jundurraga-ucl'
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
n = 16384 * 1
fs = 16384.0
high_pass = 1.0
low_pass = 100.0

b, a = signal.iirfilter(4, rs=20, Wn=[2.0 * high_pass/fs],
                        ftype='cheby2', btype='highpass')
w, h = signal.freqz(b, a, 8000)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(fs / 2 * w / np.pi, 20 * np.log10(abs(h)))
ax.set_xscale('log')
ax.set_title('Chebyshev Type II bandpass frequency response')
ax.set_xlabel('Frequency [radians / second]')
ax.set_ylabel('Amplitude [dB]')
ax.grid(which='both', axis='both')
plt.axhline(y=-3)
plt.axhline(y=-6)
plt.show()
