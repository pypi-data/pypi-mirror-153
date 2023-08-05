import pandas as pd
from peegy.io.eeg import reader
from os import listdir, walk
from os.path import isfile, isdir, join, basename
import numpy as np
from prettytable import PrettyTable
import logging
import datetime
from peegy.io.external_tools.aep_gui import extsys_tools as et
from peegy.processing.events import event_tools as tt
from peegy.io.external_tools.file_tools import DataLinks
from peegy.io.external_tools.file_tools import match_keywords, flatten_dictionary
from itertools import chain
import os
import glob
import json
__author__ = 'jaime undurraga'


def find_bdf_directories(root_path, f_type='.bdf'):
    out = []
    # search on root path
    root_data_files = [join(root_path, f) for f in listdir(root_path) if
                       isfile(join(root_path, f)) and f.endswith(f_type)]
    if root_data_files:
        out.append(root_path)
    # search in subdirectories
    _directories = [join(root_path, d) for d in listdir(root_path) if isdir(join(root_path, d))]
    for _dir in _directories:
        _out = find_bdf_directories(_dir)
        if _out:
            [out.append(_path) for _path in _out]
        data_files = [join(_dir, f) for f in listdir(_dir) if isfile(join(_dir, f)) and f.endswith(f_type)]
        if data_files:
            out.append(_dir)

    return set(out)


def events_summary(events: np.array([tt.SingleEvent]) = None):
    _codes = np.array([_e.code for _e in events])
    unique_events = np.unique(_codes)
    event_counter = []
    for i, code in enumerate(unique_events):
        event_counter.append({'code': code, 'n': len(np.where(_codes == code)[0])})
    logging.info("\n".join(['Trigger events:', str(event_counter)]))
    print("\n".join(['Trigger events:', str(event_counter)]))


def get_files_and_meta_data(measurement_path: str = '',
                            split_trigger_code: float = None,
                            filter_key_words_in_path: [str] = None,
                            exclude_key_words_in_path: [str] = None,
                            filter_key_words_in_file: [str] = None,
                            exclude_key_words_in_file: [str] = None,
                            deep_match_in_filter_path: bool = True,
                            deep_match_in_filter_file: bool = True,
                            deep_match_in_exclude_path: bool = True,
                            deep_match_in_exclude_file: bool = True,
                            meta_data_file_extension: [str] = ['.json'],
                            meta_data_reference_extension: str = '.extsys'
                            ) -> pd.DataFrame:
    """
    This function search for .bdf or .edf  and .extsys files recursively and try to pair them according to their date.
    The result is a list of DataLinks object, containing the information that links both files.
    :param measurement_path: the root path to search for pairs of files
    :param split_trigger_code: if provided, each .extsys file will be matched to the same bdf file, the ini_time and
    end_time of the DataLinks files will be determined by the trigger_code passed.
    :param filter_key_words_in_path: if provided, the return list will only contain DataLinks object whose paths does
    include
    the exclude_key_words_in_path. This is useful to process entire folders with different conditions
    :param exclude_key_words_in_path: if provided, the return list will only contain DataLinks object whose paths does
    not include
    the exclude_key_words_in_path. This is useful to process entire folders with different conditions
    :param filter_key_words_in_file: if provided, the return list will only contain DataLinks object whose file name
     does include
    the filter_key_words_in_file. This is useful to process entire folders with different conditions
    :param exclude_key_words_in_file: if provided, the return list will only contain DataLinks object whose file name
    does not include
    the exclude_key_words_in_path. This is useful to process entire folders with different conditions
    :param deep_match_in_filter_path: if True, all keywords in deep_match_in_filter_path must be present to return True
    :param deep_match_in_filter_file: if True, all keywords in filter_key_words_in_file must be present to return True
    :param deep_match_in_exclude_path: if True, all keywords in exclude_key_words_in_path must be present to return True
    :param deep_match_in_exclude_file: if True, all keywords in exclude_key_words_in_file must be present to return True
    :param meta_data_file_extension: list indicating the extension of associated meta_data files, e.g. ['.csv', .'json']
    :param meta_data_reference_extension: string indicating the file extension used as a reference to match meta_data
    file
    :return: pandas dataframe with columns extracted from .extsys files. The column DataLinks objects contain the object
     linking .bdf or .edf
    """
    par_out = pd.DataFrame()
    _all_directories = [x[0] for x in walk(measurement_path)]
    for _current_directory in _all_directories:
        if filter_key_words_in_path is not None and not match_keywords(
                filter_key_words_in_path, _current_directory,
                deep_match=deep_match_in_filter_path):
            continue
        if exclude_key_words_in_path is not None and match_keywords(
                exclude_key_words_in_path, _current_directory,
                deep_match=deep_match_in_exclude_path):
            continue

        data_files = [join(_current_directory, f) for f in listdir(_current_directory)
                      if isfile(join(_current_directory, f)) and (f.endswith('.bdf') or f.endswith('.edf'))]
        parameter_files = [join(_current_directory, f) for f in listdir(_current_directory)
                           if isfile(join(_current_directory, f)) and f.endswith('.extsys')]

        if not len(data_files):
            continue
        # get and sort parameters dates
        parameters = []
        for i, _file_name in enumerate(parameter_files):
            parameters.append(et.get_measurement_info_from_zip(_file_name))
        dates = [par['Measurement']['MeasurementModule']['Date'] for x, par in enumerate(parameters)]
        idx_par = [_i[0] for _i in sorted(enumerate([datetime.datetime.strptime(_date, '%m-%d-%y-%H-%M-%S-%f')
                                                     for _date in dates]), key=lambda x: x[1])]
        # get and sort bdf files dates
        _data = []
        for i, _file_name in enumerate(data_files):
            _eeg_reader = reader.eeg_reader(_file_name)
            _data.append(_eeg_reader)
        file_dates = [_c_data._header['start_date'] + '.' + _c_data._header['start_time']
                      for x, _c_data in enumerate(_data)]
        idx_bdf = [_i[0] for _i in sorted(enumerate([datetime.datetime.strptime(_date, '%d.%m.%y.%H.%M.%S')
                                                     for _date in file_dates]), key=lambda x: x[1])]
        # initialize ini and end time to read raw data
        ini_time, end_time = [0] * len(idx_par), [None] * len(idx_bdf)
        if len(idx_bdf) == 1 and split_trigger_code is not None:
            # ensure each parameter file and data file have are paired
            idx_bdf = idx_bdf * len(idx_par)
            raw_events = _data[0].get_events()
            events = tt.detect_events(event_channel=raw_events, fs=_data[0].fs)
            events_summary(events)
            _split_events = np.array([_e for _e in events if _e.code == split_trigger_code])
            assert _split_events.size == len(idx_par), "number of triggers to split conditions does not match" \
                                                       " the number of" \
                                                       " condition files. {:}".format(_data[0].file_name)
            ini_time = [_e.time_pos for _e in _split_events]
            end_time = [_e.time_pos for _e in _split_events[1:]]
            end_time.append(None)

        for i_p, i_b, _ini_time, _end_time in zip(idx_par, idx_bdf, ini_time, end_time):
            _data_file_name, _data_extension = os.path.splitext(_data[i_b].file_name)
            _param_file_name, _param_extension = os.path.splitext(parameter_files[i_p])
            if filter_key_words_in_file is not None and \
                    not (match_keywords(filter_key_words_in_file, _data_file_name,
                                        deep_match=deep_match_in_filter_file) and
                         match_keywords(filter_key_words_in_file, _param_file_name,
                                        deep_match=deep_match_in_filter_file)):
                continue
            if exclude_key_words_in_file is not None and \
                    (match_keywords(exclude_key_words_in_file, _data_file_name,
                                    deep_match=deep_match_in_exclude_file) or
                     match_keywords(exclude_key_words_in_file, _param_file_name,
                                    deep_match=deep_match_in_exclude_file)):
                continue
            if match_keywords(['_bad_'], _param_file_name):
                continue

            # first we check if any file is associated to parameter data file
            if meta_data_reference_extension == _param_extension:
                meta_files = list(chain(*[glob.glob(_param_file_name + '*{:}'.format(_extension))
                                          for _extension in meta_data_file_extension]))
            # if none, we look of any file is associated to data file
            if meta_data_reference_extension == _data_extension:
                meta_files = list(chain(*[glob.glob(_data_file_name + '*{:}'.format(_extension))
                                          for _extension in meta_data_file_extension]))

            meta_data = []
            for _meta_file in meta_files:
                _, file_extension = os.path.splitext(_meta_file)
                if file_extension == '.json':
                    with open(_meta_file, 'r') as f:
                        meta_data.append(json.load(f))

            data_links = DataLinks(parameters=parameters[i_p],
                                   parameters_file=parameter_files[i_p],
                                   parameters_date=dates[i_p],
                                   data_file=_data[i_b].file_name,
                                   data_date=file_dates[i_b],
                                   ini_time=_ini_time,
                                   end_time=_end_time,
                                   meta_data=meta_data
                                   )
            _tmp_pd = pd.DataFrame(parameters[i_p])
            _tmp_pd['Measurement']['data_links'] = data_links
            par_out = pd.concat([par_out, pd.DataFrame.from_dict(
                [flatten_dictionary(dict({k: [v] for k, v in parameters[i_p].items()},
                                         **{'data_links': [data_links]}))])],
                                ignore_index=True)
    if par_out.size:
        _aux = par_out.data_links.values.astype(np.ndarray)
        t = PrettyTable()
        t.add_column(fieldname='File name', column=[basename(x.parameters_file) for x in _aux])
        t.add_column(fieldname='File date', column=[basename(x.parameters_date) for x in _aux])
        t.add_column(fieldname='bdf file name', column=[basename(x.data_file) for x in _aux])
        t.add_column(fieldname='bdf file date', column=[x.data_date for x in _aux])
        logging.info(t)
        print(t)
    return par_out
