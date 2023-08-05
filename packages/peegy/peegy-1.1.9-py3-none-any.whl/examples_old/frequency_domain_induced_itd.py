from peegy.processing.pipe.pype_line_definitions import *
from peegy.processing.pipe.definitions import ReadInputData
from peegy.io.external_tools.aep_gui.dataReadingTools import get_files_and_meta_data
import numpy as np


def my_pipe(data_links=None):
    test_frequencies = np.array([
        data_links.measurement_parameters['Measurement']['StimuliModule']['Stimulus'][0]['Parameters']['ITMRate'] / 2,
        data_links.measurement_parameters['Measurement']['StimuliModule']['Stimulus'][0]['Parameters']['ITMRate'],
        data_links.measurement_parameters['Measurement']['StimuliModule']['Stimulus'][0]['Parameters']['ModulationFrequency'],
        data_links.measurement_parameters['Measurement']['StimuliModule']['Stimulus'][0]['Parameters']['Rate']])
    pipe_line = PipePool()
    pipe_line.append(ReadInputData(file_path=_data_links.data_file, ini_time=_data_links.ini_time,
                                   end_time=_data_links.end_time, layout_file_name='biosemi64_2_EXT.lay'))
    pipe_line.append(ReferenceData(pipe_line[-1].process, reference_channels=['Cz'], invert_polarity=True))
    pipe_line.append(AutoRemoveBadChannels(pipe_line[-1].process))
    pipe_line.append(ReSampling(pipe_line[-1].process, new_sampling_rate=1000.))
    pipe_line.append(FilterData(pipe_line[-1].process, high_pass=1.0, low_pass=200.0))
    pipe_line.append(EpochData(pipe_line[-1].process, event_code=1.0))
    pipe_line.append(
        AverageEpochsFrequencyDomain(pipe_line.get_process('EpochData'), test_frequencies=test_frequencies))
    pipe_line.append(PlotTopographicMap(pipe_line.get_process('AverageEpochsFrequencyDomain'), plot_x_lim=[0, 85]))
    pipe_line.append(AverageEpochs(pipe_line.get_process('EpochData')))
    pipe_line.append(AverageFrequencyPower(pipe_line.get_process('EpochData'), plot_y_lim=[0, 85]))
    pipe_line.append(AverageTimeFrequencyResponse(pipe_line.get_process('EpochData'), time_window=1.024,
                                                  sample_interval=0.004),
                     name='overall_power')
    pipe_line.append(AverageTimeFrequencyResponse(pipe_line.get_process('EpochData'), time_window=1.024,
                                                  sample_interval=0.004,
                                                  average_mode='complex'),
                     name='evoked')
    pipe_line.append(
        PlotTimeFrequencyData(pipe_line.get_process('overall_power'), plot_y_lim=[0, 20], user_naming_rule='magnitude'))
    pipe_line.append(
        PlotTimeFrequencyData(pipe_line.get_process('evoked'), plot_y_lim=[0, 20], user_naming_rule='evoked'))

    pipe_line.run()


folder_name = '/run/media/jundurraga/Elements/Measurements/filtered-clicks/PILOTS/ITD_magnitude/MB/ITMRate_5Hz/'
to_process = get_files_and_meta_data(folder_name, split_trigger_code=16.0)

for _data_links in to_process:
    my_pipe(_data_links)


