import zipfile as zip_f
import peegy.io.xml_tools as x_tools
from os import path
import numpy as np
import json


def get_measurement_info_from_zip(zip_file_name):
    with zip_f.ZipFile(zip_file_name, 'r') as my_zip:
        files = my_zip.infolist()
        m_file = my_zip.open(files[0].filename, 'r')
        content = m_file.readlines()
        _, _extension = path.splitext(files[0].filename)
        if _extension == '.xml':
            measurement_info = x_tools.xml_string_to_dict(''.join(content))
        if _extension == '.json':
            measurement_info = json.loads(str.replace(content[0].decode("utf-8"), 'Inf', '''100000'''))
        return measurement_info


def get_extsys_parameters(parameter_files=['']):
    parameters = []
    for i, _file_name in enumerate(parameter_files):
        parameters.append(get_measurement_info_from_zip(_file_name))
    dates = [par['Measurement']['MeasurementModule']['Date'] for x, par in enumerate(parameters)]
    idx_par = [i[0] for i in sorted(enumerate(dates), key=lambda xx: xx[1])]
    sorted_parameters = np.array(parameters)[idx_par]
    sorted_parameter_files = np.array(parameter_files)[idx_par]
    return sorted_parameters, sorted_parameter_files, dates, idx_par


def freeze(d):
    if isinstance(d, dict):
        return frozenset((key, freeze(value)) for key, value in list(d.items()))
    elif isinstance(d, list):
        return tuple(freeze(value) for value in d)
    return d


def merge_parameters_by_condition(parameters=[{}], **kwargs):
    merge_conditions_by = kwargs.get('merge_conditions_by', [''])
    merge_stimulus_index = kwargs.get('merge_stimulus_index', 0)

    for _p in parameters:
        assert merge_stimulus_index < len(_p['Measurement']['StimuliModule']['Stimulus'])
        _par = _p['Measurement']['StimuliModule']['Stimulus'][merge_stimulus_index]['Parameters']

    _m_items = []
    for i_p, _p in enumerate(parameters):
        _par = _p['Measurement']['StimuliModule']['Stimulus'][merge_stimulus_index]['Parameters']
        _temp = []
        for _cond in merge_conditions_by:
            _temp.append(_par[_cond])
        _m_items.append(_temp)

    (conditions, index, inverse, counts) = np.unique(_m_items,
                                                     axis=0,
                                                     return_counts=True,
                                                     return_inverse=True,
                                                     return_index=True)
    sorted_parameters = parameters[index]
    return sorted_parameters, index, inverse
