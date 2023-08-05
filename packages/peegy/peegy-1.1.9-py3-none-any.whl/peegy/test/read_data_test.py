# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 10:46:23 2014

@author: jundurraga-ucl
"""
import numpy as np
import matplotlib.pyplot as plt
from peegy.io.eeg.reader import eeg_reader
import os
import bids

_path = os.path.abspath(os.path.dirname(__file__))
folder_name = os.path.join(_path, "../test_data/set_1/")
layout = bids.layout.BIDSLayout(folder_name)
f_name = layout.get(type='eeg', extensions='bdf')[0].filename
data1 = eeg_reader(file_name=f_name)

triggers = data1.get_triggers()

# retrieve sampling rates (list of sampling rate of each channel)
print("**********************")
print("The sampling rate of, ", f_name, "is", data1.fs, "Hz")
print("--------------\n")

data = data1.get_data()

fig1 = plt.figure(figsize=(7, 6), dpi=100)
ax = fig1.add_subplot(1, 1, 1)
ax.plot(data[:, 0] - np.mean(data[:, 0]))
ax.plot(triggers)
plt.show()
