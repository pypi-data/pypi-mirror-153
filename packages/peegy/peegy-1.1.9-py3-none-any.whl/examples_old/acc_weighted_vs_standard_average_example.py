from peegy.processing.pipe.pipeline import PipePool
from peegy.processing.pipe.simulate import GenerateInputData
from peegy.processing.tools.detection.definitions import TimePeakWindow, PeakToPeakMeasure, TimeROI
from peegy.processing.tools.template_generator.auditory_waveforms import aep
from peegy.processing.pipe.general import FilterData, ReSampling, AutoRemoveBadChannels, ReferenceData, RegressOutEOG
from peegy.processing.pipe.epochs import EpochData, AverageEpochs
from peegy.processing.pipe.spatial_filtering import CreateAndApplySpatialFilter
from peegy.processing.pipe.statistics import HotellingT2Test
from peegy.processing.pipe.detection import PeakDetectionTimeDomain
from peegy.processing.pipe.plot import PlotTopographicMap
from peegy.io.storage.data_storage_tools import store_data, MeasurementInformation, SubjectInformation, PandasDataTable
import os
import numpy as np


def my_pipe():
    tw = np.array([TimePeakWindow(ini_time=50e-3, end_ref='N1', label='P1', positive_peak=True),
                   TimePeakWindow(ini_time=100e-3, end_ref=200e-3, label='N1', positive_peak=False),
                   TimePeakWindow(ini_ref='N1', end_time=300e-3, label='P2', positive_peak=True)]
                  )
    pm = np.array([PeakToPeakMeasure(ini_peak='N1', end_peak='P2')])
    roi_windows = np.array([TimeROI(ini_time=100.0e-3, end_time=250.0e-3, measure="snr", label="itd_snr")])
    fs = 16384.0
    template_waveform, _ = aep(fs=fs)
    event_times = np.arange(0, 100.0, 1.0)
    reader = GenerateInputData(template_waveform=template_waveform,
                               fs=fs,
                               n_channels=32,
                               layout_file_name='biosemi32.lay',
                               snr=0.08,
                               include_non_stationary_noise_events=True,
                               noise_events_interval=20.0,
                               noise_events_duration=15.0,
                               noise_events_power_delta_db=25.0,
                               noise_seed=0,
                               event_times=event_times,
                               event_code=1.0,
                               figures_subset_folder='acc_standard_vs_weighted_test')
    reader.run()
    pipe_line = PipePool()
    pipe_line.append(ReferenceData(reader, reference_channels=['Cz'], invert_polarity=True),
                     name='referenced')
    pipe_line.append(AutoRemoveBadChannels(pipe_line.get_process('referenced')), name='channel_cleaned')
    pipe_line.append(ReSampling(pipe_line.get_process('channel_cleaned'), new_sampling_rate=1000.), name='down_sampled')
    # pipe_line.append(RegressOutEOG(pipe_line.get_process('down_sampled'), ref_channel_labels=['EXG3', 'EXG4']),
    #                  name='eog_removed')

    pipe_line.append(FilterData(pipe_line.get_process('down_sampled'), high_pass=2.0, low_pass=30.0),
                     name='time_filtered_data')
    pipe_line.append(EpochData(pipe_line.get_process('time_filtered_data'), event_code=1.0), name='time_epochs')
    pipe_line.append(CreateAndApplySpatialFilter(pipe_line.get_process('time_epochs')), name='dss_time_epochs')

    # compute everything using weighted averaging
    pipe_line.append(HotellingT2Test(pipe_line.get_process('dss_time_epochs'), roi_windows=roi_windows,
                                     weight_data=True),
                     name='ht2_weighted_average')
    pipe_line.append(AverageEpochs(pipe_line.get_process('dss_time_epochs'), roi_windows=roi_windows,
                                   weight_data=True),
                     name='weighted_time_average')

    pipe_line.append(PeakDetectionTimeDomain(pipe_line.get_process('weighted_time_average'),
                                             time_peak_windows=tw,
                                             peak_to_peak_measures=pm),
                     name='peak_detection_weighted_ave')

    pipe_line.append(PlotTopographicMap(pipe_line.get_process('peak_detection_weighted_ave'),
                                        plot_x_lim=[0, 0.8], plot_y_lim=[-3, 3],
                                        user_naming_rule='_weighted_time_average'))

    # compute everything using standard averaging
    pipe_line.append(HotellingT2Test(pipe_line.get_process('dss_time_epochs'), roi_windows=roi_windows,
                                     weight_data=False),
                     name='ht2_standard_average')
    pipe_line.append(AverageEpochs(pipe_line.get_process('dss_time_epochs'), roi_windows=roi_windows,
                                   weight_data=False),
                     name='standard_time_average')

    pipe_line.append(PeakDetectionTimeDomain(pipe_line.get_process('standard_time_average'),
                                             time_peak_windows=tw,
                                             peak_to_peak_measures=pm),
                     name='peak_detection_standard_ave')

    pipe_line.append(PlotTopographicMap(pipe_line.get_process('peak_detection_standard_ave'),
                                        plot_x_lim=[0, 0.8], plot_y_lim=[-3, 3],
                                        user_naming_rule='_standard_time_average'))

    # run the pipe line
    pipe_line.run()
    # extract peaks, waveforms for standard average
    time_measures_standard = pipe_line.get_process('peak_detection_standard_ave')
    time_table_standard = PandasDataTable(table_name='time_peaks_standard_average',
                                          pandas_df=time_measures_standard.output_node.peak_times)
    amps_table_standard = PandasDataTable(table_name='amplitudes_standard_average',
                                          pandas_df=time_measures_standard.output_node.peak_to_peak_amplitudes)

    time_waveforms_standard = pipe_line.get_process('standard_time_average')
    waveform_table_standard = PandasDataTable(table_name='time_waveforms_standard',
                                              pandas_df=time_waveforms_standard.output_node.data_to_pandas())

    ht2_tests_standard = pipe_line.get_process('ht2_standard_average')
    h_test_table_standard = PandasDataTable(table_name='h_t2_test_standard',
                                            pandas_df=ht2_tests_standard.output_node.statistical_tests)

    # extract peaks, waveforms for weighted average
    time_measures_weighted = pipe_line.get_process('peak_detection_weighted_ave')
    time_table_weighted = PandasDataTable(table_name='time_peaks_weighted_average',
                                          pandas_df=time_measures_weighted.output_node.peak_times)
    amps_table_weighted = PandasDataTable(table_name='amplitudes_weighted_average',
                                          pandas_df=time_measures_weighted.output_node.peak_to_peak_amplitudes)

    time_waveforms_weighted = pipe_line.get_process('weighted_time_average')
    waveform_table_weighted = PandasDataTable(table_name='time_waveforms_weighted',
                                              pandas_df=time_waveforms_weighted.output_node.data_to_pandas())

    ht2_tests_weighted = pipe_line.get_process('ht2_weighted_average')
    h_test_table_weighted = PandasDataTable(table_name='h_t2_test_weighted',
                                            pandas_df=ht2_tests_weighted.output_node.statistical_tests)

    # now we save our data to a database
    subject_info = SubjectInformation(subject_id='Test_Subject')
    measurement_info = MeasurementInformation(
        date='Today',
        experiment='sim')

    _parameters = {'Type': 'ACC'}
    data_base_path = reader.input_node.paths.file_directory + os.sep + 'acc_standard_vs_weighted_test_data.sqlite'
    store_data(data_base_path=data_base_path,
               subject_info=subject_info,
               measurement_info=measurement_info,
               recording_info={'recording_device': 'dummy_device'},
               stimuli_info=_parameters,
               pandas_df=[time_table_standard, amps_table_standard, waveform_table_standard, h_test_table_standard,
                          time_table_weighted, amps_table_weighted, waveform_table_weighted, h_test_table_weighted

                          ])


if __name__ == "__main__":
    my_pipe()
