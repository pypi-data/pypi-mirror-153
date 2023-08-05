"""
.. _tut-envelope extraction via deconvolution-sim:

##################################
Envelope extraction via deconvolution(Simulated)
##################################

In this example we estimate neural activity from the envelope by removing the transducer artifact
by means of impulse response estimation.
Here we estimate the impulse response from the entire signal, not from the epochs.

.. contents:: Page contents
   :local:
   :depth: 2
"""

# Enable below for interactive backend
import matplotlib
if 'Qt5Agg' in matplotlib.rcsetup.all_backends:
   matplotlib.use('Qt5Agg')

from peegy.processing.pipe.pipeline import PipePool
from peegy.processing.pipe.detection import PeakDetectionTimeDomain
from peegy.processing.tools.detection.definitions import TimePeakWindow, PeakToPeakMeasure, TimeROI
from peegy.processing.pipe.general import ReferenceData, FilterData, RegressOutEOG, ReSampling
from peegy.processing.pipe.epochs import AverageEpochs, EpochData, RejectEpochs
from peegy.processing.pipe.regression import RegressOutArtifactIR
from peegy.processing.pipe.plot import PlotWaveforms, PlotTopographicMap
from peegy.processing.pipe.spatial_filtering import CreateAndApplySpatialFilter
from peegy.processing.pipe.simulate import GenerateInputData
from peegy.processing.pipe.io import GenericInputData
from peegy.processing.pipe.storage import MeasurementInformation, SubjectInformation, SaveToDatabase
import os
import numpy as np
from peegy.processing.tools.template_generator.auditory_waveforms import artifact_and_brain_envelope
import astropy.units as u

# first we generate a test signal
fs = 2048.0 * 8 * u.Hz
epoch_length = 4.0 * u.s
epoch_length = np.ceil(epoch_length * fs) / fs  # fit to fs rate
alternating_polarity = False  # stimulus has fix polarity in every presentation

# first we generate a test signal
burst_duration = 1 * u.s
stim_delay = 0 * u.ms
brain_delay = 113 * u.ms  # brain response delay

brain_waveform, stimulus_waveform, leaked_stimulus = artifact_and_brain_envelope(
    fs=fs,
    stimulus_delay=stim_delay,
    brain_delay=brain_delay,
    duration=burst_duration,
    seed=0)
n_channels = 32
event_times = np.arange(0, 300, epoch_length.to(u.s).value) * u.s
pipeline = PipePool()

pipeline['reader'] = GenerateInputData(template_waveform=brain_waveform,
                                       stimulus_waveform=leaked_stimulus,
                                       alternating_polarity=alternating_polarity,
                                       fs=fs,
                                       n_channels=n_channels,
                                       snr=1,
                                       layout_file_name='biosemi32.lay',
                                       event_times=event_times,
                                       event_code=1.0,
                                       figures_subset_folder='artifact_subtraction_ir_1',
                                       noise_seed=10,
                                       line_noise_amplitude=0 * u.uV
                                       )
pipeline.run()


pipeline['referenced'] = ReferenceData(pipeline['reader'],
                                       reference_channels=['Cz'],
                                       invert_polarity=False)

# down-sample stimuli to match EEG data
rs_leak_stimulus = pipeline['reader'].simulated_artifact
rs_template_waveform = pipeline['reader'].template_waveform
rs_simulated_neural_response = pipeline['reader'].simulated_neural_response

pipeline['artifact_free'] = RegressOutArtifactIR(pipeline['reader'],
                                                 stimulus_waveform=stimulus_waveform,
                                                 ir_length=20 * u.ms)

pipeline['filtered_data'] = FilterData(pipeline['artifact_free'],
                                       high_pass=2.0 * u.Hz,
                                       low_pass=60.0 * u.Hz)
pipeline.run()

pipeline['time_epochs_free'] = EpochData(pipeline['filtered_data'],
                                         event_code=1.0,
                                         base_line_correction=False,
                                         post_stimulus_interval=2.0 * u.s)
pipeline.run()

pipeline['dss_time_epochs_free'] = CreateAndApplySpatialFilter(pipeline['time_epochs_free'])
pipeline.run()

pipeline['time_ave_free'] = AverageEpochs(pipeline['dss_time_epochs_free'])
pipeline.run()

# compute epochs using without dss
pipeline['topographic_map'] = PlotTopographicMap(pipeline['time_ave_free'],
                                                 plot_x_lim=[0, epoch_length.to(u.s).value],
                                                 user_naming_rule='time_domain_ave')

pipeline.run()

# we process data without removing the artifact on a second pipeline

pipeline['filtered_data_artefact'] = FilterData(pipeline['referenced'],
                                                high_pass=2.0 * u.Hz,
                                                low_pass=60.0 * u.Hz)

pipeline['time_epochs_artefact'] = EpochData(pipeline['filtered_data_artefact'],
                                             event_code=1.0,
                                             base_line_correction=False,
                                             post_stimulus_interval=2.0 * u.s)
pipeline.run()

pipeline['dss_time_epochs_artefact'] = CreateAndApplySpatialFilter(pipeline['time_epochs_artefact'])

pipeline.run()

pipeline['time_ave_artefact'] = AverageEpochs(pipeline['dss_time_epochs_artefact'])
pipeline.run()


pipeline['neural_raw'] = GenericInputData(data=pipeline['reader'].simulated_neural_response,
                                          fs=fs,
                                          event_times=event_times,
                                          event_code=1.0,
                                          figures_subset_folder='artifact_subtraction_ir_1')
pipeline.run()
pipeline['neural_raw'].output_node.layout = pipeline['reader'].output_node.layout
pipeline.run()
pipeline['filtered_data_neural'] = FilterData(pipeline['neural_raw'],
                                              high_pass=2.0 * u.Hz,
                                              low_pass=60.0 * u.Hz)
pipeline.run()

pipeline['time_epochs_neural'] = EpochData(pipeline['filtered_data_neural'],
                                           event_code=1.0,
                                           base_line_correction=False,
                                           post_stimulus_interval=2.0 * u.s)
pipeline.run()
pipeline['time_ave_neural'] = AverageEpochs(pipeline['time_epochs_neural'],
                                            weighted_average=False)
pipeline.run()
pipeline['plotter'] = PlotWaveforms(pipeline['time_ave_neural'],
                                    overlay=[pipeline['time_ave_free']],
                                    plot_x_lim=[0, epoch_length.to(u.s).value],
                                    user_naming_rule='time_domain_ave',
                                    return_figures=True)

pipeline.run()
#
# # we plot target response vs. recovered
# plt.plot(time_data_raw.output_node.data[:, -1], label='contaminated response')
# plt.plot(time_data_clean.output_node.data[:, -1], label='recovered response')
# plt.plot(rs_simulated_neural_response[0:int(epoch_length*new_fs), -1], label='target response')
# plt.legend()
# plt.show()
# # compute correlations between brain response and contaminated response artifact
# correlations_artifact = np.empty(time_data_clean.output_node.data.shape[1])
# for _idx in range(time_data_clean.output_node.data.shape[1]):
#     _size = np.minimum(time_data_raw.output_node.data.shape[0], rs_template_waveform.shape[0])
#     correlations_artifact[_idx] = np.corrcoef(
#         rs_template_waveform[0:_size, :].flatten(),
#         time_data_raw.output_node.data[0:_size, _idx])[0, 1]
# print('obtained correlation between and leaked artifact {:}'.format(correlations_artifact))
# 
# # compute correlations between brain response and recovered response artifact
# correlations_brain = np.empty(time_data_clean.output_node.data.shape[1])
# for _idx in range(time_data_clean.output_node.data.shape[1]):
#     _size = np.minimum(time_data_clean.output_node.data.shape[0], rs_template_waveform.shape[0])
#     correlations_brain[_idx] = np.corrcoef(
#         rs_template_waveform[0:_size, :].flatten(),
#         time_data_clean.output_node.data[0:_size, _idx])[0, 1]
# print('obtained correlation between response and simulated brain response {:}'.format(correlations_brain))
# 
# waveform_table_dss = PandasDataTable(table_name='time_waveform',
#                                      pandas_df=time_data_clean.output_node.data_to_pandas())
# 
# # now we save our data to a database
# subject_info = SubjectInformation(subject_id='Test_Subject')
# measurement_info = MeasurementInformation(
#     date='Today',
#     experiment='sim')
# 
# _parameters = {'Type': 'envelope_tracking'}
# data_base_path = reader.input_node.paths.file_directory + os.sep + 'envelope_tracking_ir_1.sqlite'
# store_data(data_base_path=data_base_path,
#            subject_info=subject_info,
#            measurement_info=measurement_info,
#            recording_info={'recording_device': 'dummy_device'},
#            stimuli_info=_parameters,
#            pandas_df=[waveform_table_dss])


