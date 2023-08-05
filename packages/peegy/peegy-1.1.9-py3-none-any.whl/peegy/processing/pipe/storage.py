import pandas as pd
from peegy.processing.pipe.definitions import InputOutputProcess
from peegy.io.storage.data_storage_tools import store_data, MeasurementInformation, SubjectInformation, PandasDataTable
from peegy.processing.statistics.definitions import TestType
import time


class SaveToDatabase(InputOutputProcess):
    def __init__(self,
                 database_path: str = None,
                 subject_information: SubjectInformation = None,
                 measurement_information: MeasurementInformation = None,
                 recording_information: dict = None,
                 stimuli_information: dict = None,
                 processes_list: [InputOutputProcess] = None,
                 include_waveforms: bool = False,
                 names_prefixes: [str] = None,
                 check_duplicates: bool = True):
        """
        This InputOutputProcess class saves the required data into a sqlite database that can be used to perform large
        analysis, for example, reading the database in R.
        :param database_path: full path and name where database will be created and saved (e.g. /home/user/data.sqlite)
        :param subject_information: class filled with the required subject information
        :param measurement_information: : class filled with the required measurement information
        :param recording_information: standard dictionary containing keys and values with useful information of
        recording device (e.g. {'sampling_rate': 16384, 'device': 'biosemi'})
        :param stimuli_information: standard dictionary containing keys and values with useful information of
        stimulus used for current data (e.g. {'amplitude': 0.5, 'stimulus': 'sinusoidal', 'carrier_frequency': 500})
        :param processes_list: a list of InputOutputProcess from which statistical tables, amplitudes and peaks will
        be extracted and saved.
        :param include_waveforms: boolean or list of boolean indicating if waveforms from each InputOutputProcess should
        be saved in the database. If a boolean variable is passed, that value will apply to all processes.
        If a list is passed, it must be the same size as process_list. Only the waveforms of the process_list item
        corresponding to the same index of include_waveform element == True will be saved.
        :param names_prefixes: either None or a list of strings of the same length as processes_list. When empty,
        tables created will have as prefix the name of the InputOutputProcess. If passes, tables will have the prefix
        passed in this list.
        :param check_duplicates: If true, entries from statistical tables contained by the process passed in the
        processes_list will be checked and replaced if a match exists.
        If false, repeated entries will be allowed. This may be useful to speedup saving data on a new database where
        no duplicate checks are necessary, but not recommendable when adding data into an existing database.

        """

        super(SaveToDatabase, self).__init__()
        self.database_path = database_path
        self.subject_information = subject_information
        self.measurement_information = measurement_information
        self.recording_information = recording_information
        self.stimuli_information = stimuli_information
        self.processes_list = processes_list
        if isinstance(include_waveforms, list):
            assert(len(include_waveforms) == len(processes_list))
        self.include_waveforms = include_waveforms
        self.names_prefixes = names_prefixes
        self.input_process = processes_list
        self.check_duplicates = check_duplicates

    def run(self):
        start_time = time.time()
        _data_tables = []
        _all_statistical_methods = TestType().get_available_methods()
        statistical_methods = {}
        peak_times = pd.DataFrame()
        peak_frequency = pd.DataFrame()
        peak_to_peak_amplitudes = pd.DataFrame()
        waveforms = pd.DataFrame()

        if self.names_prefixes is None:
            self.names_prefixes = [_process.name for _process in self.processes_list]
        assert len(self.names_prefixes) == len(self.processes_list)

        _include_waveforms = self.include_waveforms
        if isinstance(self.include_waveforms, bool):
            _include_waveforms = [self.include_waveforms] * len(self.processes_list)

        for _prefix, _process, _iwf in zip(self.names_prefixes, self.processes_list, _include_waveforms):
            for _test, _stats in _process.output_node.statistical_tests.items():
                _all_statistical_methods = statistical_methods.keys()
                if _test in _all_statistical_methods:
                    _stats['data_source'] = _prefix
                    statistical_methods[_test] = pd.concat([statistical_methods[_test], _stats])
                else:
                    _stats['data_source'] = _prefix
                    statistical_methods[_test] = _stats
            if _process.output_node.peak_times is not None:
                _peak_times = _process.output_node.peak_times
                _peak_times['data_source'] = _prefix
                peak_times = pd.concat([peak_times, _peak_times])

            if _process.output_node.peak_frequency is not None:
                _peak_frequency = _process.output_node.peak_frequency
                _peak_frequency['data_source'] = _prefix
                peak_frequency = pd.concat([peak_frequency, _peak_frequency])

            if _process.output_node.peak_to_peak_amplitudes is not None:
                _peak_to_peak_amplitudes = _process.output_node.peak_to_peak_amplitudes
                _peak_to_peak_amplitudes['data_source'] = _prefix
                peak_to_peak_amplitudes = pd.concat([peak_to_peak_amplitudes, _peak_to_peak_amplitudes])

            if _iwf:
                _wave_forms = _process.output_node.data_to_pandas()
                _wave_forms['data_source'] = _prefix
                waveforms = pd.concat([waveforms, _wave_forms])

        for _test, _data in statistical_methods.items():
            _data_tables.append(PandasDataTable(table_name=_test,
                                                pandas_df=_data))
        _data_tables.append(PandasDataTable(table_name='peaks_time',
                                            pandas_df=peak_times))
        _data_tables.append(PandasDataTable(table_name='peaks_frequency',
                                            pandas_df=peak_frequency))
        _data_tables.append(PandasDataTable(table_name='amplitudes',
                                            pandas_df=peak_to_peak_amplitudes))
        _data_tables.append(PandasDataTable(table_name='waveforms',
                                            pandas_df=waveforms))

        store_data(data_base_path=self.database_path,
                   subject_info=self.subject_information,
                   measurement_info=self.measurement_information,
                   recording_info=self.recording_information,
                   stimuli_info=self.stimuli_information,
                   check_duplicates=self.check_duplicates,
                   pandas_df=_data_tables)
        print("Saving took --- %s seconds ---" % (time.time() - start_time))
