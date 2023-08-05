from peegy.processing.pipe.pype_line_definitions import *
from peegy.processing.pipe.definitions import ReadInputData
from peegy.io.external_tools.aep_gui.dataReadingTools import get_files_and_meta_data
from peegy.io.storage.data_storage_tools import *
import os
folder_name = 'C:/Users/45064008/Desktop/JP_data_august/ACC/Asleep_conditions'
data_base_path = 'C:/Users/45064008/Desktop/JP_data_august/DataJPdataACC.sqlite'
to_process = get_files_and_meta_data(folder_name, split_trigger_code=16.0)

for _data_links in to_process:
    test_frequencies = np.array([
        _data_links.measurement_parameters['Measurement']['StimuliModule']['Stimulus'][0]['Parameters']['IPMRate'],
        _data_links.measurement_parameters['Measurement']['StimuliModule']['Stimulus'][0]['Parameters']['ModulationFrequency']
        # _parameters['Measurement']['StimuliModule']['Stimulus'][0]['Parameters']['ModulationFrequency']
    ])
    folder_naming = os.path.splitext(os.path.basename(_data_links.parameters_file))[0]
    pipe_line = PipePool()
    reader = ReadInputData(file_path=_data_links.data_file, ini_time=_data_links.ini_time, end_time=_data_links.end_time, layout_file_name='biosemi64_2_EXT.lay')
    reader.input_node.paths.subset_identifier = folder_naming
    pipe_line.append(reader)
    pipe_line.append(ReferenceData(pipe_line[-1].process, reference_channels=['Cz'], invert_polarity=True))
    pipe_line.append(AutoRemoveBadChannels(pipe_line[-1].process))
    pipe_line.append(ReSampling(pipe_line[-1].process, new_sampling_rate=1000.))
    pipe_line.append(FilterData(pipe_line[-1].process, high_pass=2.0, low_pass=60))
    pipe_line.append(EpochData(pipe_line[-1].process, event_code=1.0))
    pipe_line.append(CreateAndApplySpatialFilter(pipe_line[-1].process, sf_join_frequencies=test_frequencies))
    # pipe_line.append(AverageEpochs(pipe_line[-1].process))
    pipe_line.append(AverageEpochsFrequencyDomain(pipe_line[-1].process, test_frequencies=test_frequencies, ))
    pipe_line.append(PlotTopographicMap(pipe_line[-1].process, plot_x_lim=[0, 60], plot_y_lim=[0, 1.5]))
    # pipe_line.append(PlotTopographicMap(pipe_line[-1].process, plot_x_lim=[0, 0.5], plot_y_lim=[-2.0, 2.0]))

    pipe_line.run()

    # now we save our data to a database
    subject_info = SubjectInformation(
        subject_id=_data_links.measurement_parameters['Measurement']['MeasurementModule']['Subject'])
    measurement_info = MeasurementInformation(
        date=_data_links.measurement_parameters['Measurement']['MeasurementModule']['Date'],
        experiment='IPM-FR')
    freq_process = pipe_line.get_process('AverageEpochsFrequencyDomain')
    hotelling_table = PandasDataTable(table_name='hotelling_test',
                                      pandas_df=freq_process.output_node.statistical_tests)
    waveform_table = PandasDataTable(table_name='frequency_average_data',
                                     pandas_df=freq_process.output_node.data_to_pandas())

    store_data(data_base_path=data_base_path,
               subject_info=subject_info,
               measurement_info=measurement_info,
               stimuli_info=_data_links.measurement_parameters['Measurement']['StimuliModule']['Stimulus'][0]['Parameters'],
               recording_info=_data_links.measurement_parameters['Measurement']['RecordingModule'],
               pandas_df=[hotelling_table, waveform_table]
               )

