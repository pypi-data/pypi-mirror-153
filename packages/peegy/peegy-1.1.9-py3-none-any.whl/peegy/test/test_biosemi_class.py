from peegy.definitions import edf_bdf_reader as br
import numpy as np
import matplotlib.pyplot as plt
import bids.layout
import os
import gc
__author__ = 'jundurraga'

test_frequencies = np.array([6.8, 20.4, 40.9])
_path = os.path.abspath(os.path.dirname(__file__))
folder_name = os.path.join(_path, "../test_data/set_1/")
layout = bids.layout.BIDSLayout(folder_name)
f_name = layout.get(type='eeg', extensions='bdf')[0].filename
reader = br.EdfBdfDataReader(file_name=f_name, channels_to_process=list(range(2)), layout_setup='biosemi64_2_EXT.lay',
                             delete_all=True)
triggers = reader.get_triggers(trigger_codes=[])
w_triggers = reader.merge_triggers(triggers, trigger_code=int('00100000', 2))
n_triggers = reader.merge_triggers(triggers, trigger_code=int('01000000', 2))
c_triggers = reader.merge_triggers(triggers, trigger_code=int('00000010', 2))
print(len(w_triggers['idx']), len(n_triggers['idx']), len(c_triggers['idx']))
reader.set_epochs_raw(triggers=triggers)
reader.set_epochs_raw_ave()

fig = plt.figure(num=1, dpi=100, facecolor='w', edgecolor='w')
fig.set_size_inches(10, 7)
ax = fig.add_subplot(111)
for i in range(30):
    ax.plot(reader.epochs_raw_ave.average)

plt.close(fig)
del reader
gc.collect()
