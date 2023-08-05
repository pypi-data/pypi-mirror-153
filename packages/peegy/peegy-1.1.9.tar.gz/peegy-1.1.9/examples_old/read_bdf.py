from peegy.processing.pipe.pype_line_definitions import *
from peegy.processing.pipe.definitions import ReadInputData
import pyqtgraph as pg
from peegy.processing.tools.detection.time_domain_tools import TimePeakWindow, PeakToPeakMeasure

f_name = '../test_data/set_1/sub-01/ses-test/eeg/sub-01_ses-test_task-ipmfr90_ieeg.bdf'
test_frequencies = np.array([6.8, 20.4, 40.9])
pipe_line = list()
pipe_line.append(ReadInputData(file_path=f_name, ini_time=0.0, end_time=None, layout_file_name='biosemi64_2_EXT.lay',
                               channels_idx=np.arange(0, 66)))

interpolation = PeriodicInterpolation(pipe_line[-1])
interpolation.interpolation_rate = 826.71957671
interpolation.interpolation_width = 0.0011
interpolation.interpolation_offset = 0.0015
# pipe_line.append(interpolation)
pipe_line.append(ReferenceData(pipe_line[-1], reference_channels=['Cz'], invert_polarity=True))
pipe_line.append(AutoRemoveBadChannels(pipe_line[-1]))
# pipe_line.append(ReSampling(pipe_line[-1], new_sampling_rate=1000., keep_input_node=False))
pipe_line.append(FilterData(pipe_line[-1], high_pass=3.0, low_pass=45))
pipe_line.append(EpochData(pipe_line[-1], pre_stimulus_interval=0.2, post_stimulus_interval=1.0, event_code=253.0))
# pipe_line.append(CreateAndApplySpatialFilter(pipe_line[-1]))
pipe_line.append(AverageEpochs(pipe_line[-1]))
pipe_line.append(AverageEpochsFrequencyDomain(pipe_line[-2], test_frequencies=test_frequencies))

tw = np.array([TimePeakWindow(ini_time=0.0, end_time=0.10, positive_peak=False, label='N1'),
               TimePeakWindow(ini_time=0.2, end_time=0.40, positive_peak=True, label='P1'),
               TimePeakWindow(ini_time=0.4, end_time=0.8, positive_peak=True, label='P2'),
               TimePeakWindow(ini_time=0.15, label='fix_peak')]
              )
pm = np.array([PeakToPeakMeasure(ini_peak='N1', end_peak='P2')])
pipe_line.append(PeakDetectionTimeDomain(pipe_line[-2], time_peak_windows=tw, peak_to_peak_measures=pm))
pipe_line.append(PlotTopographicMap(pipe_line[-1], plot_y_lim=None, plot_x_lim=[0, 1.2]))
pipe_line.append(PlotTopographicMap(pipe_line[-3], plot_y_lim=None, plot_x_lim=[0, 60.]))

pipe_line.run()

plotWidget = pg.plot(title="Three plot curves")



