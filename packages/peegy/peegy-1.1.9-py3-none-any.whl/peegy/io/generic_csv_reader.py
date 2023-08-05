import pandas as pd
import numpy as np
import astropy.units as u
from peegy.definitions.channel_definitions import ChannelItem
import os.path
import datetime
from peegy.tools.units.unit_tools import set_default_unit


def read_header(file_path: str = None,
                gain_col_name: str = None,
                fs_col_name: str = None,
                fs_unit: u.quantity.Quantity = u.Hz,
                gain_unit: u.quantity.Quantity = u.uV,
                gain_inverted: bool = False
                ) -> (dict, np.array):
    """
    Read header from cvs file. This is assumed to be the header indicating the parameters of the data.
    For the moment we assume one data channel, each row being an epoch.
    :param file_path: path to text file
    :param gain_col_name: string indicating the name of the column where data scaling factor should be obtained
    :param fs_col_name: string indicating the name of the column where data sampling rate should be obtained
    :param fs_unit: unit of sampling rate
    :param gain_unit: units of data
    :param gain_inverted: if True, gain will first be inverted and then multiplied
    :return: header information
    """
    header = pd.read_csv(file_path, sep="\t", header=0, nrows=1)
    # add extra information to make compatible with peegy-python
    header = header.to_dict('records')[0]
    header['n_channels'] = 1
    header['fs'] = (1.0 if fs_col_name is None else header[fs_col_name]) * fs_unit
    # header['gain'] = header['Volt/bit(nV)']
    header['gain'] = (1.0 if gain_col_name is None else header[gain_col_name]) * gain_unit
    if gain_inverted:
        header['gain'] = 1 / header['gain']
        gain_unit = 1 / gain_unit
    header['channels'] = np.array([ChannelItem(label='CH_0', idx=0)])
    header['file_name'] = file_path
    _start_date_format = "%d.%m.%y"
    _start_time_format = "%H.%M.%S"
    struct_data_time = datetime.datetime.strptime(
        datetime.datetime.fromtimestamp(os.path.getctime(file_path)).strftime(_start_date_format + _start_time_format),
        _start_date_format + _start_time_format)
    header['start_date'] = struct_data_time.strftime(_start_date_format)
    header['start_time'] = struct_data_time.strftime(_start_time_format)
    return header


def read_channel(header: dict = None,
                 channels_idx: np.array = np.array([]),
                 ini_time: float = 0,
                 end_time: float = None,
                 from_row: int = 2,
                 ) -> np.array:
    """
    Read data from csv files. For now we assumed single channel data, one row per epoch.
    :param header: dictionary containing the header of the file
    :param channels_idx: indexes of channels to be read
    :param ini_time: time (in seconds) to read from
    :param end_time: time (in seconds) to read up to
    :param from_row: integer indicating in which row data start.
    :return: raw data
    """
    ini_time = set_default_unit(ini_time, u.s)
    end_time = set_default_unit(end_time, u.s)
    data = pd.read_csv(header['file_name'], sep="\t", skiprows=from_row,  header=None)
    data = data.iloc[:, 1::].to_numpy()
    gain = header['gain']
    data = data * gain
    events = np.zeros(data.shape)
    events[:, 0] = 1
    data = data.reshape(-1, 1)
    events = events.reshape(-1, 1)
    _ini_pos = np.minimum(np.maximum(0, ini_time * header['fs']), data.shape[0]).astype(int)
    if end_time is None:
        _end_pos = data.shape[0]
    else:
        _end_pos = np.minimum(np.maximum(0, end_time * header['fs']), data.shape[0]).astype(int)
    if not channels_idx.size:
        channels_idx = np.arange(data.shape[1])
    data = data[_ini_pos: _end_pos, channels_idx]
    events = events[_ini_pos: _end_pos, :]
    return data, events, data.unit


def read_file(file_path: str = None) -> (pd.DataFrame, np.array):
    """
    Read data from cvs file
    :param file_path: path to text file
    :return: header information and raw data
    """
    header = pd.read_csv(file_path, sep="\t", header=0, nrows=1)
    data = pd.read_csv(file_path, sep="\t", skiprows=2,  header=None)
    data = data.iloc[:, 1::].to_numpy()
    data = data.T[:, None, :]
    return header, data


def merge_files(files_path: [str]):
    data = None
    headers = pd.DataFrame()
    for _file in files_path:
        _header, _data = read_file(file_path=_file)
        headers = pd.concat([headers, _header], ignore_index=True)
        if data is None:
            data = _data
        else:
            data = np.dstack((data, _data))
    if not np.all(headers.all()):
        RuntimeError('Files must have same header to be merged')
    header = headers.iloc[0, :]
    return header, data
