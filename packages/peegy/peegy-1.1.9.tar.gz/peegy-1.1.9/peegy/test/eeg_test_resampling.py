import numpy as np
import peegy.processing.tools.filters.eegFiltering as ep
import matplotlib.pyplot as plt
__author__ = 'jundurraga-ucl'


fs = 1000.0
f_s = 50.0
n_o = 700.0
t = np.arange(0, n_o) / fs
y1 = np.sin(2*np.pi*f_s*t)
y2 = np.sin(2*np.pi*4*f_s*t)
y = np.tile(np.array(y1 + y2) + 0.0*np.random.random(t.shape), (4, 1)).T
new_fs = fs/5

yf = np.fft.fft(y, axis=0)
freq = np.arange(len(yf)) * fs / len(yf)
yc, factor = ep.eeg_resampling(x=y, factor=new_fs / fs, blocks=8)
new_fs = fs * factor
new_time = np.arange(0, yc.shape[0]) / new_fs
if factor > 1.0:
    plt.plot(np.squeeze(new_time), np.squeeze(yc), 'rs')
    plt.plot(t, y)
    plt.plot(t, y1)
    plt.plot(t, y2)
    plt.plot(t, y, 'bo')
else:
    plt.plot(t, y)
    plt.plot(t, y1)
    plt.plot(t, y2)
    plt.plot(t, y, 'bo')
    plt.plot(np.squeeze(new_time), np.squeeze(yc), 'rv')
plt.show()
plt.show()
