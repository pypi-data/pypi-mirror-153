import peegy.io.edf_bdf_reader as br
import matplotlib.pyplot as plt
import numpy as np
import pyedflib
__author__ = 'jundurraga'

f_name = '/run/media/jundurraga/Elements/Measurements/P300/Data/1_cijfers.edf'
header = br.read_edf_bdf_header(file_name=f_name)
ch = np.array([0, 1])
event_table = br.get_event_channel(header=header, ini_time=0, end_time=None,
                                   event_channel_label='EDF Annotations')
data, _events, _units, annotations = br.get_data(header=header, channels_idx=ch, ini_time=0, end_time=None)
fs = header['fs'][0]
x = np.arange(0, data.shape[0]) / fs
fig = plt.figure()
plt.plot(x, data - np.mean(data, axis=0))
plt.plot(x[_events.squeeze() > 0], _events[_events > 0], 'ro')

f = pyedflib.EdfReader(f_name)
f.readAnnotations()
n = f.signals_in_file
signal_labels = f.getSignalLabels()
sigbufs = np.zeros((f.getNSamples()[0], n))
for i in np.arange(n):
    sigbufs[:, i] = f.readSignal(i)
xx = np.arange(0, sigbufs.shape[0])/f.getSampleFrequency(0)
plt.figure()
plt.plot(xx, sigbufs[:, 0:n])
plt.show()
plt.show()

plt.figure()
f = np.arange(data.shape[0]) * fs / data.shape[0]
plt.plot(f, np.abs(np.fft.fft(data, axis=0)) * 2 / data.shape[0])
plt.xlim(0, 60)
plt.show()
