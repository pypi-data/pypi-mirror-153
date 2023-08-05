from peegy.processing.pipe.pype_line_definitions import *
from peegy.processing.pipe.definitions import GenerateInputData
from peegy.processing.tools.template_generator.auditory_waveforms import aep
from peegy.io.storage.data_storage_tools import *
import os


def my_pipe():
    fs = 16384.0
    epoch_length = 4.0
    epoch_length = np.ceil(epoch_length * fs) / fs  # fit to fs rate
    assr_frequency = np.array([41.0])
    assr_frequency = np.ceil(epoch_length * assr_frequency) / epoch_length  # fit to epoch length
    # here we pick some random frequencies to test statistical detection
    random_frequencies = np.unique(np.random.rand(10)*30)
    template_waveform, _ = aep(fs=fs)
    n_channels = 32
    event_times = np.arange(0, 360.0, 1/assr_frequency)
    reader = GenerateInputData(template_waveform=template_waveform,
                               fs=fs,
                               n_channels=n_channels,
                               snr=0.05,
                               layout_file_name='biosemi32.lay',
                               event_times=event_times,
                               event_code=1.0,
                               figures_subset_folder='assr_ht2_test')
    reader.run()
    events = reader.output_node.events.get_events(code=1)
    # skip events to preserve only those at each epoch point
    _new_events = Events(events=events[0:-1:int(epoch_length * assr_frequency)])
    reader.output_node.events = _new_events
    pipe_line = PipePool()
    pipe_line.append(ReferenceData(reader, reference_channels=['Cz'], invert_polarity=True),
                     name='referenced')
    pipe_line.append(AutoRemoveBadChannels(pipe_line.get_process('referenced')), name='channel_cleaned')
    pipe_line.append(FilterData(pipe_line.get_process('channel_cleaned'), high_pass=2.0, low_pass=100.0),
                     name='time_filtered_data')
    pipe_line.append(EpochData(pipe_line.get_process('time_filtered_data'),
                               event_code=1.0,
                               base_line_correction=False),
                     name='time_epochs')
    pipe_line.append(CreateAndApplySpatialFilter(pipe_line.get_process('time_epochs'),
                                                 sf_join_frequencies=assr_frequency),
                     name='dss_time_epochs')

    pipe_line.append(AppendGFPChannel(pipe_line.get_process('dss_time_epochs')),
                     name='dss_time_epochs_with_gfp')
    pipe_line.append(AverageEpochsFrequencyDomain(pipe_line.get_process('dss_time_epochs_with_gfp'),
                                                  n_fft=int(epoch_length*fs),
                                                  test_frequencies=np.concatenate((
                                                      assr_frequency,
                                                      2 * assr_frequency,
                                                      random_frequencies))),
                     name='fft_ave')

    pipe_line.append(PlotTopographicMap(pipe_line.get_process('fft_ave'), plot_x_lim=[0, 90], plot_y_lim=[0, 1.5]))

    pipe_line.run()

    freq_process = pipe_line.get_process('fft_ave')
    hotelling_table = PandasDataTable(table_name='hotelling_test',
                                      pandas_df=freq_process.output_node.statistical_tests)
    waveform_table = PandasDataTable(table_name='frequency_average_data',
                                     pandas_df=freq_process.output_node.data_to_pandas())

    # now we save our data to a database
    subject_info = SubjectInformation(subject_id='Test_Subject')
    measurement_info = MeasurementInformation(
        date='Today',
        experiment='sim')

    _parameters = {'Type': 'ASSR'}
    data_base_path = reader.input_node.paths.file_directory + os.sep + 'assr_ht2_test.sqlite'
    store_data(data_base_path=data_base_path,
               subject_info=subject_info,
               measurement_info=measurement_info,
               recording_info={'recording_device': 'dummy_device'},
               stimuli_info=_parameters,
               pandas_df=[hotelling_table, waveform_table])


if __name__ == "__main__":
    my_pipe()
