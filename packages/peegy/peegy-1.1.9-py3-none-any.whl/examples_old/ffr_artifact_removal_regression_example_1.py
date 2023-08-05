from peegy.processing.pipe.pype_line_definitions import *
from peegy.processing.pipe.definitions import GenerateInputData
from peegy.processing.tools.template_generator.auditory_waveforms import aep
from peegy.io.storage.data_storage_tools import *
import os
import peegy.processing.tools.filters.eegFiltering as eegf


def my_pipe():
    # first we generate a test signal
    fs = 16384.0
    epoch_length = 1.0
    epoch_length = np.ceil(epoch_length * fs) / fs  # fit to fs rate
    burst_duration = 0.375
    ffr_frequencies = np.array([120, 240, 360])
    ffr_frequencies = np.ceil(burst_duration * ffr_frequencies) / burst_duration  # fit to burst_duration length
    alternating_polarity = False  # stimulus is alternating in polarity every presentation
    # here we pick some random frequencies to test statistical detection
    random_frequencies = np.unique(np.random.randint(100, 400, 3))
    stim_delay = 0.001  # neural delay in secs
    brain_delay = 0.0237
    time = np.arange(0, burst_duration, 1 / fs).reshape(-1, 1)
    # stimulation waveform
    _original_stimulus_waveform = np.sum(
        3 * np.sin(2 * np.pi * ffr_frequencies * time),
        axis=1).reshape(-1, 1) * 1.0  # generates ffr artifacts with 1 uV amplitude
    stimulus_waveform = np.pad(_original_stimulus_waveform, ((int(fs * stim_delay), int(fs * brain_delay)),
                                                             (0, 0)), 'constant', constant_values=(0, 0))
    # brain response
    template_waveform = np.pad(_original_stimulus_waveform, ((int(fs * stim_delay) + int(fs * brain_delay), 0), (0, 0)),
                               'constant', constant_values=(0, 0))
    template_waveform *= 0.2  # 0.2 uV amplitude and a delay
    template_waveform[template_waveform < 0] = 0  # rectify

    n_channels = 32
    event_times = np.arange(0, 360.0, epoch_length)
    reader = GenerateInputData(template_waveform=template_waveform,
                               stimulus_waveform=stimulus_waveform,
                               alternating_polarity=alternating_polarity,
                               fs=fs,
                               n_channels=n_channels,
                               snr=3,
                               layout_file_name='biosemi32.lay',
                               event_times=event_times,
                               event_code=1.0,
                               figures_subset_folder='ffr_artifact_test',
                               noise_seed=0)
    reader.run()
    # define new sampling rate to make processing easier
    new_fs = fs // 1
    pipe_line = PipePool()
    pipe_line.append(ReferenceData(reader, reference_channels=['Cz'], invert_polarity=True),
                     name='referenced')
    pipe_line.append(AutoRemoveBadChannels(pipe_line.get_process('referenced')), name='channel_cleaned')
    pipe_line.append(ReSampling(pipe_line.get_process('channel_cleaned'),
                                new_sampling_rate=new_fs),
                     name='down_sampled')
    pipe_line.append(FilterData(pipe_line.get_process('down_sampled'), high_pass=2.0, low_pass=None),
                     name='time_filtered_data')

    rs_stimulus_waveform, _ = eegf.eeg_resampling(x=stimulus_waveform,
                                                  factor=new_fs / fs)

    pipe_line.append(RegressOutArtifact(pipe_line.get_process('time_filtered_data'),
                                        event_code=1.0,
                                        alternating_polarity=alternating_polarity,
                                        stimulus_waveform=rs_stimulus_waveform,
                                        method='xcorr'
                                        ),
                     name='artifact_free')

    pipe_line.append(EpochData(pipe_line.get_process('artifact_free'),
                               event_code=1.0,
                               base_line_correction=False,
                               post_stimulus_interval=burst_duration/1.0),
                     name='time_epochs')

    pipe_line.append(CreateAndApplySpatialFilter(pipe_line.get_process('time_epochs'),
                                                 sf_join_frequencies=ffr_frequencies),
                     name='dss_time_epochs')

    pipe_line.append(AverageEpochs(pipe_line.get_process('time_epochs')),
                     name='time_domain_ave')

    # compute epochs using without dss
    pipe_line.append(AverageEpochsFrequencyDomain(pipe_line.get_process('time_epochs'),
                                                  test_frequencies=np.concatenate((
                                                      ffr_frequencies, random_frequencies)),
                                                  n_fft=int(burst_duration * new_fs)  # here we make the nfft constant
                                                  ),
                     name='fft_ave_no_dss')

    pipe_line.append(PlotTopographicMap(pipe_line.get_process('fft_ave_no_dss'),
                                        plot_x_lim=[100, 400], plot_y_lim=[0, 0.5],
                                        user_naming_rule='_fft_ave_no_dss'))

    # compute epochs using dss
    pipe_line.append(AverageEpochsFrequencyDomain(pipe_line.get_process('dss_time_epochs'),
                                                  test_frequencies=np.concatenate((
                                                      ffr_frequencies, random_frequencies)),
                                                  n_fft=int(burst_duration * new_fs)  # here we make the nfft constant
                                                  ),
                     name='fft_ave_dss')
    pipe_line.append(PlotTopographicMap(pipe_line.get_process('fft_ave_dss'),
                                        plot_x_lim=[100, 400], plot_y_lim=[0, 0.5],
                                        user_naming_rule='_fft_ave_dss'))
    pipe_line.run()
    # create tables with results for data without dss
    freq_process_no_dss = pipe_line.get_process('fft_ave_no_dss')
    hotelling_table_no_dss = PandasDataTable(table_name='hotelling_test_no_dss',
                                             pandas_df=freq_process_no_dss.output_node.statistical_tests)
    waveform_table_no_dss = PandasDataTable(table_name='frequency_average_data_no_dss',
                                            pandas_df=freq_process_no_dss.output_node.data_to_pandas())

    # create tables with results for data using dss
    freq_process_dss = pipe_line.get_process('fft_ave_dss')
    hotelling_table_dss = PandasDataTable(table_name='hotelling_test_dss',
                                          pandas_df=freq_process_dss.output_node.statistical_tests)
    waveform_table_dss = PandasDataTable(table_name='frequency_average_data_dss',
                                         pandas_df=freq_process_dss.output_node.data_to_pandas())

    # now we save our data to a database
    subject_info = SubjectInformation(subject_id='Test_Subject')
    measurement_info = MeasurementInformation(
        date='Today',
        experiment='sim')

    _parameters = {'Type': 'test'}
    data_base_path = reader.input_node.paths.file_directory + os.sep + 'ffr_ht2_test.sqlite'
    store_data(data_base_path=data_base_path,
               subject_info=subject_info,
               measurement_info=measurement_info,
               recording_info={'recording_device': 'dummy_device'},
               stimuli_info=_parameters,
               pandas_df=[hotelling_table_no_dss, waveform_table_no_dss,
                          hotelling_table_dss, waveform_table_dss,
                          ])


if __name__ == "__main__":
    my_pipe()
