import numpy as np
import pandas as pd
from pandas.io import sql
import sqlite3
from sqlalchemy import create_engine
import astropy.units as u
from numpy.core.records import fromarrays
from scipy.io import savemat
__author__ = 'jundurraga-ucl'


class SubjectInformation(object):
    def __init__(self, subject_id: str = '',
                 gender: str = '',
                 age: float = None,
                 date_of_birth: str = '',
                 handedness: str = '',
                 comments: str = ''):
        self.subject_id = subject_id
        self.gender = gender
        self.age = age
        self.date_of_birth = date_of_birth
        self.handedness = handedness
        self.comments = comments


class MeasurementInformation(object):
    def __init__(self, experiment: str = '', condition: str = '', date: str = '', comments: str = ''):
        self.experiment = experiment
        self.condition = condition
        self.date = date
        self.comments = comments


class PandasDataTable(object):
    def __init__(self, table_name: str = '', pandas_df: pd.DataFrame = None):
        self.table_name = table_name
        self.pandas_df = pandas_df


def pandas_with_units_to_sql_compatible(data_frame: pd.DataFrame = None):
    """
    Convert pandas data frame with astropy units to pandas compatible with sql
    :param data_frame:
    :return: data frame with columns where quantities and units are in separate columns
    """
    for column in data_frame:
        _condition_1 = np.any(np.array([isinstance(_v, u.quantity.Quantity)
                                        for _v in data_frame[column].to_numpy()]))
        _condition_2 = False
        if np.any(_condition_1):
            _condition_2 = np.any(np.array([_v.unit != u.dimensionless_unscaled
                                            for _v in data_frame[column].to_numpy()
                                            if isinstance(_v, u.Quantity)]))
        if _condition_2:
            unit_column = column + '_unit'
            data_frame[unit_column] = None
            for _i, _v in enumerate(data_frame[column].to_numpy()):
                if isinstance(_v, u.Quantity):
                    data_frame.iloc[_i, data_frame.columns.get_loc(unit_column)] = _v.unit.to_string()
                else:
                    data_frame.iloc[_i, data_frame.columns.get_loc(unit_column)] = u.dimensionless_unscaled.to_string()
        if _condition_1:
            for _i, _v in enumerate(data_frame[column].to_numpy()):
                if isinstance(_v, u.Quantity):
                    data_frame.iloc[_i, data_frame.columns.get_loc(column)] = _v.value
                else:
                    data_frame.iloc[_i, data_frame.columns.get_loc(column)] = _v

    return data_frame


def store_data(data_base_path='',
               subject_info: SubjectInformation = None,
               measurement_info: MeasurementInformation = MeasurementInformation(),
               stimuli_info: dict = None,
               recording_info: dict = None,
               pandas_df: [PandasDataTable] = None,
               check_duplicates: bool = True
               ):
    # connect and add items to data base
    # db = sqlite3.connect(data_base_path)
    engine = create_engine("sqlite:///" + data_base_path)
    cnn = engine.connect()
    # cursor = db.cursor()
    statement = "SELECT name FROM sqlite_master WHERE type='table';"
    print('Storing data in %s' % data_base_path)
    all_tables = cnn.execute(statement).fetchall()
    if ('subjects',) in all_tables:
        cursor = engine.execute('select id from subjects ;')
        _index = len(cursor.fetchall()) + 1
    else:
        _index = 1
    _new_df = dict({'anonymous_name': 'S' + str(_index)}, **subject_info.__dict__)

    _id_subject = upsert_db(table_name='subjects', new_df=pd.DataFrame([_new_df]), db=engine,
                            column_names=['subject_id'], replace=False)

    # add measurement info
    _row_measurement_info = dict({'id_subject': _id_subject},
                                 **measurement_info.__dict__)
    _row_measurement_info = pandas_with_units_to_sql_compatible(pd.DataFrame([_row_measurement_info]))
    _id_measurement = upsert_db(table_name='measurement_info', new_df=_row_measurement_info,
                                db=engine,
                                column_names=list(_row_measurement_info.keys()), replace=False)

    # convert lists to string to be compatible with sqlite
    [stimuli_info.update({_key: str(_value)}) for _key, _value in stimuli_info.items() if isinstance(_value, list)]
    # add stimuli to table
    _row_stimuli = dict({'id_subject': _id_subject, 'id_measurement': _id_measurement}, **stimuli_info)
    # check no dict is passed
    [_row_stimuli.pop(_key) for _key in list(_row_stimuli.keys()) if isinstance(_row_stimuli[_key], dict)]
    _row_stimuli = pandas_with_units_to_sql_compatible(pd.DataFrame([_row_stimuli]))
    _id_stimuli = upsert_db(table_name='stimuli', new_df=_row_stimuli, db=engine,
                            column_names=list(_row_stimuli.keys()), replace=False)

    # add recording processing to table
    _row_recording = dict({'id_stimuli': _id_stimuli, 'id_subject': _id_subject, 'id_measurement': _id_measurement},
                          **recording_info)
    _row_recording = pandas_with_units_to_sql_compatible(pd.DataFrame([_row_recording]))
    _id_recording = upsert_db(table_name='recording', new_df=_row_recording, db=engine,
                              column_names=list(_row_recording.keys()), replace=False)

    for _df in pandas_df:
        _df.pandas_df = pandas_with_units_to_sql_compatible(_df.pandas_df)
        _df.pandas_df['id_subject'] = _id_subject
        _df.pandas_df['id_measurement'] = _id_measurement
        _df.pandas_df['id_stimuli'] = _id_stimuli
        _df.pandas_df['id_recording'] = _id_recording
        upsert_db(table_name=_df.table_name, new_df=_df.pandas_df, db=engine,
                  column_names=['id_subject', 'id_measurement', 'id_stimuli', 'id_recording'],
                  replace=check_duplicates,
                  check_duplicates=check_duplicates)
    cnn.close()
    engine.dispose()


def write_set(filename, processname, pipe_line, event_code, ref_el):
    """Export OutputNodedata to EEGLAB .set file.
    Exports either continuous EEG data or epoched EEG data from the pipe line named 'pipe_line' and the
    pipe line step named 'processname' to a .set file named 'filename'. Also exports the known reference electrode
    'ref_el', and events coded with 'event_code'.
    Export functionality was assessed by loading the exported data into eeglab2021.1.
    Code ported from MNE-Lab, https://github.com/cbrnr/mnelab/blob/main/mnelab/io/writers.py
    Caveat: EEG layout parameters are currently not converted, only the channel names are used! Also it is assumed,
    that the pipeline has been called with the run() method before saving the data up to the requested process.
    Some of the following code parts are creating "dummy" variables, to match specific variables needed in EEGlab,
    see https://eeglab.org/tutorials/ConceptsGuide/Data_Structures.html for EEGlab datastructure documentation.

    Input parameters:
    filename: full filepath + Name of file to save, e.g. /home/user/eeg/mydata.set
    processname: name of output node processing step you want to save
    pipe_line: pipe object
    event_code: event code associated with the eeg data. Events needs to have a code, time and duration in order to get
    exported. Duration of trigger for now is fixed to 5ms. Currently only tested with one single event code.
    ref_el: reference electrode

    Output parameters:
    None, will print a line to STDOUT if export successful, containing processname and filename.

    Example call:
    .....
    ref_el = 'Cz'
    eventcode = 241 #Trigger event code
    pipe_line.append(AutoRemoveBadChannels(pipe_line.get_process('referenced'),
                                            keep_input_node=False),
                      name='channel_cleaned')

    pipe_line.run()
    write_set('/channel_cleaned.set', 'channel_cleaned', pipe_line, eventcode, ref_el)
    """
    processed_data = pipe_line.get_process(processname)
    fs = processed_data.output_node.fs.value
    data = processed_data.output_node.get_data().value.astype('float64')
    times = processed_data.output_node.x.value
    if len(data.shape) == 3:  # for epoched data
        data = np.transpose(data, (1, 0, 2))  # EEGlab data format is channel x amplitude x epoch
        epochs = data.shape[2]
        epoch_metadata = fromarrays([
                                    np.arange(1, epochs+1),
                                    np.tile('square', epochs),
                                    np.arange(1, epochs+1),
                                    np.tile(0.005, epochs),
                                    np.tile(0.0, epochs)],
                                    names=["event", "eventtype", "eventposition", "eventduration", "eventlatency"])
        # create dummy event data for EEGlab/brainstorms events structures
        events = fromarrays([np.tile(event_code, epochs),
                             # calculates epoch start latency in samples
                             [max(times)-min(times) * i * fs for i in np.arange(1, epochs+1)],
                             np.tile((0.005 * fs), epochs),  # assume 5ms duration of epoch trigger
                             np.arange(1, epochs+1).astype('float64')],
                            names=["type", "latency", "duration", "epoch"])
    elif len(data.shape) == 2:  # for continuous data
        data = np.transpose(data, (1, 0))  # EEGlab data format is channel x amplitude
        epochs = 1
        epoch_metadata = 0
        events = fromarrays([np.squeeze(processed_data.output_node.events.get_events_code(event_code)),
                             processed_data.output_node.events.get_events_time(event_code).value * fs + 1.0,
                             # event time starting points are stored as sample index in EEGlab events structure
                             processed_data.output_node.events.get_events_duration(event_code)],
                            names=["type", "latency", "duration"])
    else:
        raise Exception('Data needs to have at least two dimensions (channel x amplitude)')

    ch_names = [i.label for i in processed_data.output_node.layout]
    chanlocs = fromarrays([ch_names], names=["labels"])

    savemat(filename, dict(EEG=dict(data=data,
                                    setname=filename,
                                    nbchan=data.shape[0],
                                    pnts=float(data.shape[1]),
                                    trials=epochs,
                                    srate=fs,
                                    ref=ref_el,
                                    xmin=times[0],
                                    xmax=times[-1],
                                    chanlocs=chanlocs,
                                    epoch=epoch_metadata,
                                    event=events,
                                    icawinv=[],
                                    icasphere=[],
                                    icaweights=[])),
            appendmat=False)
    print("Successfully saved " + processname + " to " + filename)


def find_item_in_table(table_name='', new_df=pd.DataFrame, db=sqlite3.Connection):
    cursor = db.cursor()
    statement = "SELECT name FROM sqlite_master WHERE type='table';"
    all_tables = cursor.execute(statement).fetchall()
    if (table_name,) in all_tables:
        table = sql.read_sql('select * from ' + table_name, db)
        _found = table[new_df.columns].isin(new_df)
    return _found


def upsert_db(table_name='',
              new_df=pd.DataFrame,
              column_names: [str] = None,
              db=sqlite3.Connection,
              replace=True,
              check_duplicates=True
              ):
    """
   This function will upsert data to database therefore preventing duplicated rows.
   :param table_name: Name of the table where we want to add new data
   :param new_df: pandas data frame containing data to be appended
   :param column_names: list of columns in the database that should not be duplicated
   :param db: database connection
   :param replace: if true, it will always replace an existing entry, if false and a data entry exists then the index
   of this entry will be returned.
   :param check_duplicates: if true, it will check whether a similar row exits, it will find it and return the index.
   If false, it will always add a new row, regardless of whether a similar row exists.
   :return: indexes of new appended data
    """

    if not new_df.size:
        return None
    statement = "SELECT name FROM sqlite_master WHERE type='table';"
    all_tables = db.execute(statement).fetchall()
    connection = db.raw_connection()
    cursor = connection.cursor()
    add_new_rows = not check_duplicates
    if (table_name,) in all_tables:
        if check_duplicates:
            # find which rows already exists
            _condition = ''
            for _idx_col, _col in enumerate(column_names):
                sqlist = df_values_to_sqlist(new_df, _col)
                sep_and = '' if _idx_col == len(column_names) - 1 else ' and '
                _operator = 'is' if sqlist == '(NULL)' else 'in'
                _condition = _condition + '{:s} {:} {:} {:} '.format(''.join(_col), _operator, sqlist, sep_and)
            _table = cursor.execute('select id from ' + table_name + ' where ' + _condition + ' ;')
            _index = np.array(_table.fetchall())
            add_new_rows = _index.size == 0
            if _index.size and replace:
                # delete those rows that we are going to "upsert"
                _to_delete = array_values_to_sqlist(_index)
                _table = cursor.execute('delete from ' + table_name + ' where id in {:};'.format(_to_delete))
                connection.commit()
        # add data new data ensuring new indexes
        if add_new_rows or replace:
            _table = cursor.execute('select id from ' + table_name + ' ;')
            _all_ids = _table.fetchall()
            idx_off_set = np.max(_all_ids) + 1 if _all_ids else 0
            _index = new_df.index.values + idx_off_set
            new_df['id'] = _index
            new_df.to_sql(table_name, db, if_exists='append', index=False, chunksize=1000, method='multi')
    else:
        new_df.to_sql(table_name, db, if_exists='append', index=True, index_label='id', chunksize=1000, method='multi')
        # get new index from DB
        _id = sql.read_sql('select id from ' + table_name, db)
        _index = _id.values
    # delete temp table
    connection.commit()
    cursor.close()
    return int(_index) if _index.size == 1 else _index


def df_values_to_sqlist(new_df: pd.DataFrame = None,
                        column_name: str = None):
    new_df_values = new_df[column_name].values
    sql_list_values = ''
    for idx_v, _v in enumerate(new_df_values):
        sep = '' if idx_v == len(new_df_values) - 1 else ','
        if isinstance(_v, str):
            sql_list_values = sql_list_values + '"{:}"{:}'.format(_v, sep)
        elif isinstance(_v, np.ndarray):
            if _v.size:
                sql_list_values = sql_list_values + '"{:}"{:}'.format(_v, sep)
            else:
                sql_list_values = sql_list_values + '{:}{:}'.format('NULL', sep)
        elif _v is None:
            sql_list_values = sql_list_values + '{:}{:}'.format('NULL', sep)
        elif _v == np.inf:
            sql_list_values = sql_list_values + '{:}{:}'.format('+Infinity', sep)
        elif _v == -np.inf:
            sql_list_values = sql_list_values + '{:}{:}'.format('-Infinity', sep)
        else:
            sql_list_values = sql_list_values + '{:}{:}'.format(_v, sep)
    sql_list_values = '({:})'.format(sql_list_values)
    return sql_list_values


def array_values_to_sqlist(values: np.array = None):
    sql_list_values = ''
    for idx_v, _v in enumerate(values.squeeze()):
        sep = '' if idx_v == len(values) - 1 else ','
        if isinstance(_v, str):
            sql_list_values = sql_list_values + '"{:}"{:}'.format(_v, sep)
        elif _v is None:
            sql_list_values = sql_list_values + '{:}{:}'.format('NULL', sep)
        elif _v == np.inf:
            sql_list_values = sql_list_values + '{:}{:}'.format('+Infinity', sep)
        elif _v == -np.inf:
            sql_list_values = sql_list_values + '{:}{:}'.format('-Infinity', sep)
        else:
            sql_list_values = sql_list_values + '{:}{:}'.format(_v, sep)
    sql_list_values = '({:})'.format(sql_list_values)
    return sql_list_values
