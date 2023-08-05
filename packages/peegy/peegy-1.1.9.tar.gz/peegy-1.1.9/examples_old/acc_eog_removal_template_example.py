# This example shows removal of the eye artefacts via a template subtraction method
# described in Valderrama et al, 2018. This script will output a figure, showing the
# estimated eye artefact, and the EEG signal before and after eye artefact removal.
# The algorithm performs three steps:
# 1) Blinks are detected in each channel using a (generic) eye artefact template.
# The template is iteratively adjusted after each newly detected eye blink, to more closely match
# the individual subject one.
# 2) A signal is generated, which used the individual template to represent all detected eyeblinks,
# depending on the amplitudes and timepoints of each individual eyeblink.
# 3) The signal from step two is subtracted from the raw EEG signal, thus leading to an enhanced
# EEG signal, where eyeblinks do not lead to dropping of the affected epochs.
# Literature:
# Valderrama, J. T., de la Torre, A., & Van Dun, B. (2018). An automatic algorithm for blink-artifact suppression based
# on iterative template matching: Application to single channel recording of cortical auditory evoked potentials.
# Journal of Neural Engineering, 15(1), 016008. https://doi.org/10.1088/1741-2552/aa8d95
from peegy.processing.pipe.pipeline import PipePool
from peegy.processing.pipe.simulate import GenerateInputData
from peegy.processing.tools.detection.definitions import TimePeakWindow, PeakToPeakMeasure, TimeROI
from peegy.processing.tools.template_generator.auditory_waveforms import aep
from peegy.processing.pipe.general import FilterData, ReSampling, AutoRemoveBadChannels, ReferenceData, RegressOutEOG
from peegy.processing.pipe.epochs import EpochData, AverageEpochs
from peegy.processing.pipe.spatial_filtering import CreateAndApplySpatialFilter
from peegy.processing.pipe.statistics import HotellingT2Test
from peegy.processing.pipe.detection import PeakDetectionTimeDomain
from peegy.processing.pipe.plot import PlotWaveforms, PlotTopographicMap
from peegy.processing.pipe.attach import AppendGFPChannel
from peegy.io.storage.data_storage_tools import store_data, MeasurementInformation, SubjectInformation, PandasDataTable
import os
import numpy as np


def my_pipe():
    tw = np.array([TimePeakWindow(ini_time=50e-3, end_ref='N1', label='P1', positive_peak=True,
                                  exclude_channels=['GFP']),
                   TimePeakWindow(ini_time=100e-3, end_ref=200e-3, label='N1', positive_peak=False,
                                  exclude_channels=['GFP']),
                   TimePeakWindow(ini_ref='N1', end_time=300e-3, label='P2', positive_peak=True,
                                  exclude_channels=['GFP']),
                   TimePeakWindow(ini_time=50e-3, end_time=150e-3, label='gfp1', positive_peak=True,
                                  target_channels=['GFP']),
                   TimePeakWindow(ini_time=150e-3, end_time=500e-3, label='gfp2', positive_peak=True,
                                  target_channels=['GFP'])])
    pm = np.array([PeakToPeakMeasure(ini_peak='N1', end_peak='P2')])
    roi_windows = np.array([TimeROI(ini_time=100.0e-3, end_time=250.0e-3, measure="snr", label="itd_snr")])
    fs = 16384.0
    template_waveform, _ = aep(fs=fs)
    event_times = np.arange(0, 100.0, 1.0)
    reader = GenerateInputData(template_waveform=template_waveform,
                               fs=fs,
                               n_channels=32,
                               layout_file_name='biosemi32.lay',
                               snr=0.1,
                               event_times=event_times,
                               event_code=1.0,
                               figures_subset_folder='acc_test_eog_template',
                               include_eog_events=True,
                               include_non_stationary_noise_events=True
                               )
    reader.run()
    pipe_line = PipePool()
    pipe_line.append(ReferenceData(reader, reference_channels=['Cz'],
                                   invert_polarity=True),
                     name='referenced')
    pipe_line.append(AutoRemoveBadChannels(pipe_line.get_process('referenced')),
                     name='channel_cleaned')
    pipe_line.append(ReSampling(pipe_line.get_process('channel_cleaned'),
                                new_sampling_rate=1024.),
                     name='down_sampled')

    pipe_line.append(RegressOutEOG(pipe_line.get_process('down_sampled'),
                                   ref_channel_labels=['EOG1'],
                                   method='template'),
                     name='eog_removed')
    pipe_line.append(FilterData(pipe_line.get_process('eog_removed'),
                                high_pass=2.0,
                                low_pass=30.0),
                     name='time_filtered_data')
    pipe_line.append(FilterData(pipe_line.get_process('down_sampled'),
                                high_pass=2.0,
                                low_pass=30.0),
                     name='time_filtered_data_with_eog_artefacts')

    pipe_line.append(EpochData(pipe_line.get_process('time_filtered_data'),
                               event_code=1.0),
                     name='time_epochs')
    pipe_line.append(EpochData(pipe_line.get_process('time_filtered_data_with_eog_artefacts'),
                               event_code=1.0),
                     name='time_epochs_with_eog_artefacts')

    pipe_line.append(CreateAndApplySpatialFilter(pipe_line.get_process('time_epochs_with_eog_artefacts')),
                     name='dss_time_epochs_with_eog_artefacts')

    pipe_line.append(AppendGFPChannel(pipe_line.get_process('time_epochs')),
                     name='time_epochs_gfp')
    pipe_line.append(AppendGFPChannel(pipe_line.get_process('time_epochs_with_eog_artefacts')),
                     name='time_epochs_gfp_with_eog_artefacts')
    pipe_line.append(HotellingT2Test(pipe_line.get_process('time_epochs_gfp'),
                                     roi_windows=roi_windows), name='ht2')
    pipe_line.append(HotellingT2Test(pipe_line.get_process('time_epochs_gfp_with_eog_artefacts'),
                                     roi_windows=roi_windows), name='ht2')
    pipe_line.append(AverageEpochs(pipe_line.get_process('time_epochs_gfp'), roi_windows=roi_windows,
                                   weight_data=False),
                     name='time_average')
    pipe_line.append(AverageEpochs(pipe_line.get_process('time_epochs_gfp_with_eog_artefacts'),
                                   roi_windows=roi_windows,
                                   weight_data=False),
                     name='time_average_with_eog_artefacts')

    pipe_line.append(AverageEpochs(pipe_line.get_process('time_epochs_gfp_with_eog_artefacts'),
                                   roi_windows=roi_windows,
                                   weight_data=True),
                     name='time_w_average_with_eog_artefacts_dss')

    pipe_line.append(AverageEpochs(pipe_line.get_process('dss_time_epochs_with_eog_artefacts'),
                                   roi_windows=roi_windows,
                                   weight_data=False),
                     name='time_average_with_eog_artefacts_dss')

    pipe_line.append(PeakDetectionTimeDomain(pipe_line.get_process('time_average'),
                                             time_peak_windows=tw,
                                             peak_to_peak_measures=pm),
                     name='data_with_peaks')
    pipe_line.append(PeakDetectionTimeDomain(pipe_line.get_process('time_average_with_eog_artefacts'),
                                             time_peak_windows=tw,
                                             peak_to_peak_measures=pm),
                     name='data_with_peaks_with_eog_artefacts')

    pipe_line.append(PeakDetectionTimeDomain(pipe_line.get_process('time_w_average_with_eog_artefacts_dss'),
                                             time_peak_windows=tw,
                                             peak_to_peak_measures=pm),
                     name='data_with_peaks_with_eog_artefacts_weighted_average')

    pipe_line.append(PeakDetectionTimeDomain(pipe_line.get_process('time_average_with_eog_artefacts_dss'),
                                             time_peak_windows=tw,
                                             peak_to_peak_measures=pm),
                     name='data_with_peaks_with_eog_artefacts_dss')

    pipe_line.append(PlotTopographicMap(pipe_line.get_process('data_with_peaks'),
                                        plot_x_lim=[0, 0.8],
                                        plot_y_lim=[-3, 3],
                                        user_naming_rule='_eog_free_'))

    pipe_line.append(PlotTopographicMap(pipe_line.get_process('data_with_peaks_with_eog_artefacts'),
                                        plot_x_lim=[0, 0.8],
                                        plot_y_lim=[-3, 3],
                                        user_naming_rule='_with_eog_'))
    pipe_line.append(PlotTopographicMap(pipe_line.get_process('data_with_peaks_with_eog_artefacts_weighted_average'),
                                        plot_x_lim=[0, 0.8],
                                        plot_y_lim=[-3, 3],
                                        user_naming_rule='_with_eog_weighted_average_'))

    pipe_line.append(PlotTopographicMap(pipe_line.get_process('data_with_peaks_with_eog_artefacts_dss'),
                                        plot_x_lim=[0, 0.8],
                                        plot_y_lim=[-3, 3],
                                        user_naming_rule='_with_eog_dss_'))

    pipe_line.append(PlotWaveforms(pipe_line.get_process('data_with_peaks'),
                                   ch_to_plot=np.array(['C4', 'CP2'])))

    pipe_line.run()

    time_measures = pipe_line.get_process('data_with_peaks')
    time_table = PandasDataTable(table_name='time_peaks',
                                 pandas_df=time_measures.output_node.peak_times)
    amps_table = PandasDataTable(table_name='amplitudes',
                                 pandas_df=time_measures.output_node.peak_to_peak_amplitudes)

    time_waveforms = pipe_line.get_process('time_average')
    waveform_table = PandasDataTable(table_name='time_waveforms',
                                     pandas_df=time_waveforms.output_node.data_to_pandas())

    ht2_tests = pipe_line.get_process('ht2')
    h_test_table = PandasDataTable(table_name='h_t2_test',
                                   pandas_df=ht2_tests.output_node.statistical_tests)

    # now we save our data to a database
    subject_info = SubjectInformation(subject_id='Test_Subject')
    measurement_info = MeasurementInformation(
        date='Today',
        experiment='sim')

    _parameters = {'Type': 'ACC'}
    data_base_path = reader.input_node.paths.file_directory + os.sep + 'acc_test_data_eog_template.sqlite'
    store_data(data_base_path=data_base_path,
               subject_info=subject_info,
               measurement_info=measurement_info,
               recording_info={'recording_device': 'dummy_device'},
               stimuli_info=_parameters,
               pandas_df=[time_table, amps_table, waveform_table, h_test_table])


if __name__ == "__main__":
    my_pipe()
