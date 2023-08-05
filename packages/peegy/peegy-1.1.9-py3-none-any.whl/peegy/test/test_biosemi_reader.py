import peegy.io.edf_bdf_reader as br
import matplotlib.pyplot as plt
import numpy as np
import bids.layout
import os
__author__ = 'jundurraga'

test_frequencies = np.array([6.8, 20.4, 40.9])
_path = os.path.abspath(os.path.dirname(__file__))
folder_name = os.path.join(_path, "../test_data/set_1/")
layout = bids.layout.BIDSLayout(folder_name)
f_name = layout.get(type='eeg', extensions='bdf')[0].filename
header = br.read_edf_bdf_header(file_name=f_name)
ch = []
[ch.append(header['channels'][x]) for x in [0]]
data = br.get_data(header=header, channels=ch, ini_time=0, end_time=None)
plt.plot(data)
plt.show()
