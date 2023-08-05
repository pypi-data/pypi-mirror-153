from peegy.processing.pipe.pipeline import PipePool
from peegy.processing.pipe.io import ReadInputData
from peegy.processing.tools.detection.definitions import TimePeakWindow, PeakToPeakMeasure, TimeROI
from peegy.processing.pipe.general import FilterData, ReSampling, AutoRemoveBadChannels, ReferenceData, RegressOutEOG
from peegy.processing.pipe.epochs import EpochData, AverageEpochs
from peegy.processing.pipe.spatial_filtering import CreateAndApplySpatialFilter
from peegy.processing.pipe.statistics import HotellingT2Test
from peegy.processing.pipe.detection import PeakDetectionTimeDomain
from peegy.processing.pipe.plot import PlotTopographicMap
from peegy.processing.pipe.definitions import Events
from peegy.io.storage.data_storage_tools import store_data, MeasurementInformation, SubjectInformation, PandasDataTable
import os
import numpy as np
from peegy.io.external_tools.aep_gui.dataReadingTools import get_files_and_meta_data

folder_name = '/home/lvyper/Documents/Paediatric_IPMFR/Data/CYL/ACC/Asleep_conditions'
data_base_path = '/home/lvyper/Documents/Paediatric_IPMFR/Table/data.sql'
to_process = get_files_and_meta_data(folder_name, split_trigger_code=16.0)


def my_pipe(data_links=None, experiment=''):
    folder_naming = os.path.splitext(os.path.basename(data_links.parameters_file))[0]
    # below is the example when we want force peaks to be before and after a reference peak (e.g. N1)
    tw = np.array([TimePeakWindow(ini_time=50e-3, end_ref='N1', label='P1', positive_peak=True),
                   TimePeakWindow(ini_time=100e-3, end_time=200e-3, label='N1', positive_peak=False),
                   TimePeakWindow(ini_ref='N1', end_time=300e-3, label='P2', positive_peak=True)]
                  )
    pm = np.array([PeakToPeakMeasure(ini_peak='N1', end_peak='P2')])
    roi_windows = np.array([TimeROI(ini_time=100.0e-3, end_time=250.0e-3, measure="snr", label="itd_snr")])

    reader = ReadInputData(file_path=data_links.data_file, ini_time=data_links.ini_time,
                           end_time=data_links.end_time, layout_file_name='biosemi64_2_EXT.lay')
    reader.input_node.paths.subset_identifier = folder_naming
    reader.run()
    events = reader.output_node.events.get_events(code=1)
    _new_events = Events(events=events[0:-1:2])
    reader.output_node.events = _new_events
    pipe_line = PipePool()
    pipe_line.append(ReferenceData(reader, reference_channels=['Cz'], invert_polarity=True),
                     name='ref')
    pipe_line.append(AutoRemoveBadChannels(pipe_line.get_process('ref')), name='channel_cleaned')
    pipe_line.append(ReSampling(pipe_line.get_process('channel_cleaned'), new_sampling_rate=1000.), name='down_sampled')
    pipe_line.append(RegressOutEOG(pipe_line.get_process('down_sampled'), ref_channel_labels=['EXG3', 'EXG4']),
                     name='eog_removed')
    pipe_line.append(FilterData(pipe_line.get_process('eog_removed'), high_pass=2.0, low_pass=30.0),
                     name='time_filtered_data')
    pipe_line.append(EpochData(pipe_line.get_process('time_filtered_data'), event_code=1.0), name='time_epochs')
    pipe_line.append(CreateAndApplySpatialFilter(pipe_line.get_process('time_epochs')), name='dss_time_epochs')
    pipe_line.append(HotellingT2Test(pipe_line.get_process('dss_time_epochs'), roi_windows=roi_windows), name='ht2')
    pipe_line.append(AverageEpochs(pipe_line.get_process('dss_time_epochs'), roi_windows=roi_windows),
                     name='time_average')
    pipe_line.append(PeakDetectionTimeDomain(pipe_line.get_process('time_average'),
                                             time_peak_windows=tw,
                                             peak_to_peak_measures=pm))
    pipe_line.append(PlotTopographicMap(pipe_line[-1].process, plot_x_lim=[0, 0.8], plot_y_lim=[-3, 3]))

    pipe_line.run()

    time_measures = pipe_line.get_process('PeakDetectionTimeDomain')
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
    subject_info = SubjectInformation(
        subject_id=data_links.measurement_parameters['Measurement']['MeasurementModule']['Subject'])
    measurement_info = MeasurementInformation(
        date=data_links.measurement_parameters['Measurement']['MeasurementModule']['Date'],
        experiment=experiment)

    _parameters = data_links.measurement_parameters['Measurement']['StimuliModule']['Stimulus'][0]['Parameters']
    _recording = data_links.measurement_parameters['Measurement']['RecordingModule']
    store_data(data_base_path=data_base_path,
               subject_info=subject_info,
               measurement_info=measurement_info,
               stimuli_info=_parameters,
               recording_info=_recording,
               pandas_df=[time_table, amps_table, waveform_table, h_test_table]
               )


for _data_links in to_process:
    my_pipe(data_links=_data_links, experiment='acc-awake')
