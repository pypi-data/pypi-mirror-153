from peegy.processing.pipe.pype_line_definitions import *
from peegy.processing.pipe.definitions import ReadInputData
import bidshandler as bh
import os
import numpy as np

test_frequencies = np.array([6.8, 20.4, 40.9])
_path = os.path.abspath(os.path.dirname(__file__))
folder_name = '..//test_data/'

data_base_path = os.path.join(_path, "..//test_data/data.sqlite")
layout = bh.BIDSTree(folder_name)
f_name = layout.scans[0].raw_file
pipe_line = PipePool()
pipe_line.append(ReadInputData(file_path=f_name, ini_time=0.0, end_time=None, layout_file_name='biosemi64_2_EXT.lay'))
pipe_line.append(ReferenceData(pipe_line[-1].process, reference_channels=['Cz'], invert_polarity=True))
pipe_line.append(AutoRemoveBadChannels(pipe_line[-1].process))
pipe_line.append(ReSampling(pipe_line[-1].process, new_sampling_rate=1000.))
pipe_line.append(FilterData(pipe_line[-1].process, high_pass=2.0, low_pass=44.0))
pipe_line.append(EpochData(pipe_line[-1].process, event_code=253.0))
pipe_line.append(AverageEpochsFrequencyDomain(pipe_line.get_process('EpochData'), test_frequencies=test_frequencies))
pipe_line.append(PlotTopographicMap(pipe_line.get_process('AverageEpochsFrequencyDomain'), plot_x_lim=[0, 60]))
pipe_line.append(AverageEpochs(pipe_line.get_process('EpochData')))
pipe_line.append(AverageFrequencyPower(pipe_line.get_process('EpochData'), plot_y_lim=[0, 60]))
pipe_line.append(AverageTimeFrequencyResponse(pipe_line.get_process('EpochData'), time_window=1.024,
                                              sample_interval=0.004),
                 name='overall_power')
pipe_line.append(AverageTimeFrequencyResponse(pipe_line.get_process('EpochData'), time_window=1.024,
                                              sample_interval=0.004,
                                              average_mode='complex'),
                 name='evoked')
pipe_line.append(PlotTimeFrequencyData(pipe_line.get_process('overall_power'), plot_y_lim=[0, 60], user_naming_rule='magnitude'))
pipe_line.append(PlotTimeFrequencyData(pipe_line.get_process('evoked'), plot_y_lim=[0, 60], user_naming_rule='evoked'))

pipe_line.run()



