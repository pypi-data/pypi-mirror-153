# -*- coding: utf-8 -*-
"""
This module defines abstracts classes for general purpose EEG processing
@author:Jaime Undurraga

"""
import abc
from prettytable import PrettyTable
import logging
from peegy.processing.tools.epochs_processing_tools import et_snr_weighted_mean, et_get_spatial_filtering, \
    et_apply_spatial_filtering, get_in_window_data
import os
from os import listdir
from os.path import isfile, join
import json
import datetime
from scipy.io import savemat, loadmat
import io
import pickle
from peegy.processing.tools import epochs_processing_tools as et
from peegy.processing.tools.eeg_epoch_operators import et_fold, et_unfold
from peegy.processing.tools.detection.time_domain_tools import detect_peaks_and_amplitudes
from peegy.processing.tools.filters.eegFiltering import eeg_notch_filter, filt_filt_multithread
from peegy.definitions.eeg_definitions import EegAverageEpochs
from peegy.processing.tools.detection.definitions import PeakToPeakMeasure, TimePeakWindow, EegPeak, TimeROI
from peegy.definitions.eeg_definitions import EegChannel, ElectrodeType
from peegy.definitions.channel_definitions import Domain
from peegy.processing.pipe.spatial_filtering import SpatialFilter
from peegy.directories.tools import DirectoryPaths
from peegy.plot import eeg_ave_epochs_plot_tools as eegpt
from peegy.processing.statistics.eeg_statistic_tools import hotelling_t_square_test
import pandas
import multiprocessing
import ctypes
import scipy.signal as signal
import matplotlib.pyplot as plt
from sklearn import linear_model
import astropy.units as u
import numpy as np
log = logging.getLogger()


class EEGData(object, metaclass=abc.ABCMeta):
    def __init__(self, file_name='', **kwargs):
        delete_all = kwargs.get('delete_all', False)
        delete_figures = kwargs.get('delete_figures', False)
        self._file_name = file_name
        self.data_processing = {}
        self.data_raw = np.array([])
        self.epochs_raw = np.array([])
        self.epochs_raw_ave = EegAverageEpochs()
        self.epochs_processed = np.array([])
        self.epochs_processed_ave = EegAverageEpochs()
        self.component_maps_ave = [EegAverageEpochs()]
        self.ref_channels = np.array([EegChannel()])
        self.roi_windows = np.array([TimeROI()])
        self._reference = np.array([])
        self.spatial_filter = SpatialFilter()
        self.invert_polarity = False
        self.resampling_factor = 1.0
        self.low_pass_freq = None
        self.high_pass_freq = None
        self.notch_frequencies = None
        self.average_domain = Domain.time
        self._fs = None
        self._fs_raw = None
        self._paths = DirectoryPaths(file_path=file_name, delete_all=delete_all, delete_figures=delete_figures)
        self._oeg_channels = np.array([EegChannel()])
        self._bad_channels = np.array([EegChannel()])
        self.x_offset = 0.0
        self.n_epochs_to_read = None
        self.ini_epoch_to_read = None

    def get_file_name(self):
        return self._file_name

    def set_file_name(self, new_value):
        self._file_name = new_value

    file_name = property(get_file_name, set_file_name)

    def get_data(self):
        return 'set_data not defined'

    def set_data(self, new_value):
        return 'get_data not defined'

    data = abc.abstractproperty(get_data, set_data)

    def get_channel_labels(self):
        return 'get_channelLabels not defined'

    def set_channel_labels(self, new_value):
        return 'set_channelLabels not defined'

    channelLabels = abc.abstractproperty(get_channel_labels, set_channel_labels)

    def get_channels(self):
        return 'get_channels not defined'

    def set_channels(self):
        return 'set_channels not defined'

    channels = abc.abstractproperty(get_channels)

    def get_all_channels(self):
        return 'get_channels not defined'

    all_channels = abc.abstractproperty(get_all_channels)

    def get_fs(self):
        return self._fs

    def set_fs(self, new_value):
        self._fs = new_value

    fs = property(get_fs, set_fs)

    def get_oeg_channels(self):
        return self._oeg_channels

    def set_oeg_channels(self, new_value=np.array([EegChannel()])):
        self._oeg_channels = new_value

    oeg_channels = property(get_oeg_channels, set_oeg_channels)

    def get_bad_channels(self):
        return self._oeg_channels

    def set_bad_channels(self, new_value=np.array([EegChannel()])):
        self._bad_channels += new_value

    bad_channels = property(get_bad_channels, set_bad_channels)

    def get_amplitude_units(self):
        return 'get_fs not defined'

    def set_amplitude_units(self, new_value):
        return 'set_fs not defined'

    amplitude_units = abc.abstractproperty(get_amplitude_units, set_amplitude_units)

    def get_time_units(self):
        return 'get_fs not defined'

    def set_time_units(self, new_value):
        return 'set_fs not defined'

    time_units = abc.abstractproperty(get_time_units, set_time_units)

    def get_paths(self):
        return 'get_file_paths not defined'

    paths = abc.abstractproperty(get_paths)

    def get_system(self):
        return 'get_system not defined'

    system = abc.abstractproperty(get_system)

    def time_to_samples(self, value):
        out = None
        if value is not None:
            out = np.round(value * self.fs).astype(np.int)
        return out

    @abc.abstractmethod
    def get_raw_data(self, win_length=0):
        print("get_raw_data not defined")
        return "get_raw_data not defined"

    @abc.abstractmethod
    def get_data(self, channels=[]):
        print("getData not defined")
        return "getData not defined"

    @abc.abstractmethod
    def get_triggers(self, triggerCodes=[]):
        print('getTriggers not defined')
        return

    @abc.abstractmethod
    def get_channel_by_label(self, channel_labels=[]):
        print('get_channel_by_label not defined')
        return

    def set_reference(self):
        # if auto_detect_reference:
        #     ref_channels = [channels[self.detect_ref_channel(epochs)]]
        print(('Referencing data to: %s' % ' '.join(map(str, [_ch.label for _ch in self.ref_channels]))))
        reference = np.zeros(self.epochs_raw.shape[0::2], dtype=np.float)
        count = 0.0
        for ref_ch in self.ref_channels:
            for i, ch in enumerate(self.channels):
                if ch.__dict__ == ref_ch.__dict__:
                    reference += self.epochs_raw[:, i, :]
                    count += 1.0
                    #  remove reference if only one is provided
                    if len(self.ref_channels) == 1:
                        self.remove_channels(channels_to_remove=[ch])
                        print('Channel %s was removed but used as reference' % ch.label)
                    break
        reference /= np.maximum(count, 1.0)
        self._reference = reference
        t = PrettyTable()
        t.add_column(fieldname='Reference Channel', column=[_ref.label for _ref in self.ref_channels])
        log.info(t)
        print(t)

    def reference_epochs(self, epochs=np.array):
        # if auto_detect_reference:
        #     ref_channels = [channels[self.detect_ref_channel(epochs)]]
        print(('Referencing data to: %s' % ' '.join(map(str, [_ch.label for _ch in self.ref_channels]))))
        epochs -= np.expand_dims(self._reference, 1)
        return epochs

    def find_array(self, parameters={}, descriptor=''):
        parameters_files = [join(self.paths.data_subset_path, f) for f in
                            listdir(self.paths.data_subset_path)
                            if isfile(join(self.paths.data_subset_path, f)) and f.endswith('.json')]
        data = {}
        path = None
        for _file in parameters_files:
            with io.open(_file) as f:
                _configuration = json.loads(f.read())
                _file_par = _configuration['parameters']
                _parameters = dict(parameters, **{'descriptor': descriptor})
            if np.alltrue(
                    [_parameters[_key] == _file_par[_key] for _key in list(_parameters.keys()) if _key in _file_par]):
                path = _configuration['file']
                break
        if path:
            if not os.path.isfile(path):
                print(('could not find associated file: ' + path))
            else:
                print(('reading data from %s: ' % path))
                if os.path.splitext(path)[1] == '.hdf':
                    my_data = pandas.HDFStore(path)
                    for index, row in my_data['data_shape'].iterrows():
                        if (row['shape'] is not None) and len(row['shape']) == 3:
                            _data = et_fold(my_data[row['label']].as_matrix(), row['shape'][0])
                        else:
                            _data = my_data[row['label']].as_matrix()
                        data[row['label']] = _data
                    my_data.close()
                if os.path.splitext(path)[1] == '.mat':
                    data = loadmat(path)
        return data

    def save_array(self, parameters={}, data_type='array', data={}, data_format='.hdf', descriptor=''):
        if data_format not in ['.hdf', '.mat']:
            print(('unknown output format:' + data_format))
            return
        _c_date = datetime.datetime.today().strftime('%d_%b_%Y_%H_%M_%S')
        _parameters_file = self.paths.data_basename_path + descriptor + _c_date + '.json'
        _data_file = self.paths.data_basename_path + descriptor + _c_date
        out_dict = {'file': _data_file + data_format,
                    'parameters': dict(parameters, **{'descriptor': descriptor})}
        print(('saving data to %s' % _data_file + data_format))
        with io.open(_parameters_file, 'w', encoding='utf-8') as f:
            f.write(str(json.dumps(out_dict, ensure_ascii=False)))
        if data_format == '.hdf':
            x = pandas.HDFStore(_data_file + '.hdf', mode='w')
            x['parameters'] = pandas.DataFrame({'parameters': parameters})
            x['data_type'] = pandas.DataFrame({'data_type': [data_type]})
            data_shape = pandas.DataFrame(columns=('label', 'shape'))
            for _idx, _label in enumerate(data.keys()):
                if isinstance(data[_label], np.ndarray):
                    data_shape.loc[_idx] = [_label, data[_label].shape]
                    if len(data[_label].shape) == 3:
                        x[_label] = pandas.DataFrame(et_unfold(data[_label]))
                    else:
                        x[_label] = pandas.DataFrame(data[_label])
                else:
                    data_shape.loc[_idx] = [_label, None]
                    x[_label] = pandas.DataFrame(data[_label])
            x['data_shape'] = data_shape
            x.close()
            # np.save(_data_file, data)
        if data_format == '.mat':
            savemat(_data_file, data=data)

    def save_object(self, parameters={}, new_object=object, descriptor=''):
        _c_date = datetime.datetime.today().strftime('%d_%b_%Y_%H_%M_%S')
        _parameters_file = self.paths.data_basename_path + descriptor + _c_date + '.json'
        _data_file = self.paths.data_basename_path + descriptor + _c_date + '.p'
        out_dict = {'file': _data_file,
                    'parameters': parameters}
        with io.open(_parameters_file, 'w', encoding='utf-8') as f:
            f.write(str(json.dumps(out_dict, ensure_ascii=False)))
        with io.open(_data_file, 'wb') as f:
            pickle.dump(new_object, f)

    def find_object(self, parameters={}):
        parameters_files = [join(self.paths.data_subset_path, f)
                            for f in listdir(self.paths.data_subset_path)
                            if isfile(join(self.paths.data_subset_path, f)) and f.endswith('.json')]
        data = None
        path = None
        for _file in parameters_files:
            with io.open(_file) as f:
                _configuration = json.loads(f.read())
            if parameters == _configuration['parameters']:
                path = _configuration['file']
                break
        if path:
            if not os.path.isfile(path):
                print(('could not find associated file: ' + path))
            print(('reading object from: ' + path))
            with open(path, 'rb') as f:
                data = pickle.load(f)
        return data

    def set_data_raw(self,
                     ref_channels=np.array([EegChannel()]),
                     triggers=np.array([]),
                     **kwargs):
        pad_zeros = kwargs.get('pad_zeros', None)
        self.data_processing['pad_zeros'] = pad_zeros

        raw_data, relative_triggers, buffer_size = self.get_raw_data(channels=self.channels,
                                                                     ref_channels=ref_channels,
                                                                     triggers=triggers,
                                                                     **kwargs)
        # pad zeros if requested
        if pad_zeros is not None:
            int_zero_points = {'ini': relative_triggers - 1,
                               'end': relative_triggers + int(pad_zeros * self.fs)}
            self.interpolate_data(data=raw_data, interpolation_data_points=int_zero_points)
        self.data_raw = raw_data

    def get_epochs(self, channels=np.array([EegChannel()]), triggers={}, low_pass_freq=None,
                   high_pass_freq=None, notch_frequencies=None, **kwargs):
        epoch_length = kwargs.get('epoch_length', None)
        pad_zeros = kwargs.get('pad_zeros', None)
        resampling_fs = kwargs.get('resampling_fs', self._fs_raw)
        bad_channels = kwargs.get('bad_channels', [])
        remove_bad_channels = kwargs.get('remove_bad_channels', True)
        thr = kwargs.get('thr', None)
        interval = kwargs.get('interval', None)
        amp_thr = kwargs.get('amp_thr', None)
        descriptor = kwargs.get('descriptor', 'raw_epochs')
        trigger_factor = kwargs.get('trigger_factor', None)  # if provided, will add or remove triggers using this value

        # creates dictionary containing processing information
        self.data_processing['notch_frequencies'] = notch_frequencies
        self.data_processing['epoch_length'] = epoch_length
        self.data_processing['high_pass_freq'] = high_pass_freq
        self.data_processing['low_pass_freq'] = low_pass_freq
        self.data_processing['pad_zeros'] = pad_zeros
        self.data_processing['subset_identifier'] = self.paths.subset_identifier
        self.data_processing['ref_channels'] = [_ch.label for _ch in self.ref_channels]
        self.data_processing['resampling_fs'] = resampling_fs
        # self.data_processing['bad_channels'] = np.array([_bc.__dict__ for _bc in bad_channels])
        self.data_processing['remove_bad_channels'] = remove_bad_channels
        self.data_processing['thr'] = thr
        self.data_processing['interval'] = interval
        self.data_processing['amp_thr'] = amp_thr
        self.data_processing['x_offset'] = self.x_offset
        self.data_processing['trigger_factor'] = trigger_factor
        if descriptor == 'oeg_epochs':
            self.data_processing['oeg_channels'] = [_ch.label for _ch in self.oeg_channels]

        # creates dictionary containing processing information

        _data = self.find_array(parameters=self.data_processing, descriptor=descriptor)
        if _data:
            epochs = _data['epochs']
            _d_bad_channels = np.array([EegChannel(**b_c[0]) for b_c in _data['auto_detected_bad_channels']])
            self._fs = resampling_fs if resampling_fs else self._fs_raw
        else:
            data_raw, relative_triggers, buffer_size = self.get_raw_data(channels=channels,
                                                                         triggers=triggers,
                                                                         ref_channels=self.ref_channels,
                                                                         **kwargs)
            # correct triggers to compensate for x_offset
            relative_triggers += np.round(self.x_offset * self.fs).astype(np.int)

            # pad zeros if requested
            if pad_zeros is not None:
                int_zero_points = {'ini': relative_triggers - 1,
                                   'end': relative_triggers + int(pad_zeros * self.fs)}
                self.interpolate_data(data=data_raw, interpolation_data_points=int_zero_points)
            # detect bad channels
            _d_bad_channels = self.detect_bad_channels(epochs=data_raw, channels=channels, **kwargs)
            # filter data
            data = self.filter_data(data=data_raw, low_pass=low_pass_freq, high_pass=high_pass_freq)
            if self.notch_frequencies:
                data = eeg_notch_filter(data, f=notch_frequencies, f_range=1.0, fs=self._fs)

            # interpolate triggers
            if trigger_factor:
                relative_triggers = self.interpolate_triggers2(triggers=relative_triggers, factor=trigger_factor)
                buffer_size = int(np.maximum(buffer_size, np.min(np.diff(relative_triggers))))
                _useful = relative_triggers + buffer_size <= data.shape[0]
                relative_triggers = relative_triggers[_useful]
                t = PrettyTable()
                t.add_column(fieldname='Adjusted epoch length [s]', column=[buffer_size / self._fs])
                log.info(t)

            epochs = np.zeros((buffer_size, len(channels), len(relative_triggers)), dtype=np.float32)
            for i, trigger_pos in enumerate(relative_triggers):
                # ensure that blocks match buffer size
                if trigger_pos + buffer_size > data.shape[0]:
                    epochs = epochs[:, :, list(range(i))]
                    break
                epochs[:, :, i] = data[trigger_pos:trigger_pos + buffer_size, :]
            self.save_array(parameters=self.data_processing, data_type='array',
                            data={'epochs': epochs,
                                  'bad_channels': np.array([_bc.__dict__ for _bc in bad_channels]),
                                  'auto_detected_bad_channels': np.array([_bc.__dict__ for _bc in _d_bad_channels])},
                            descriptor=descriptor)
        t = PrettyTable()
        t.add_column(fieldname='File name', column=[self._file_name])
        t.add_column(fieldname='High-pass Filter', column=[str(high_pass_freq)])
        t.add_column(fieldname='Low-pass Filter', column=[str(low_pass_freq)])
        t.add_column(fieldname='Notch Filter', column=[str(notch_frequencies)])
        log.info(t)

        self.data_processing['ini_epoch_to_read'] = self.ini_epoch_to_read
        self.data_processing['n_epochs_to_read'] = self.n_epochs_to_read
        n_epochs = epochs.shape[2]
        ini_epoch = 0
        end_epoch = n_epochs
        if self.ini_epoch_to_read is not None:
            ini_epoch = np.minimum(self.ini_epoch_to_read, n_epochs)
        if self.n_epochs_to_read is not None:
            end_epoch = np.minimum(self.n_epochs_to_read + ini_epoch, n_epochs)
        epochs = epochs[:, :, ini_epoch:end_epoch]
        t = PrettyTable(['reading epochs'])
        t.add_row(['Reading {:d} epochs'.format(end_epoch - ini_epoch)])
        t.add_row(['from {:d}'.format(ini_epoch)])
        t.add_row(['to {:d}'.format(end_epoch - 1)])
        log.info(t)
        print(t)

        return epochs, np.concatenate((bad_channels, _d_bad_channels))

    def set_epochs_raw(self,
                       triggers={},
                       **kwargs):
        epoch_length = kwargs.pop('epoch_length', None)
        resampling_fs = kwargs.pop('resampling_fs', self._fs_raw)
        # get scalp data
        self.data_processing['channels'] = [_ch.label for _ch in self.channels]
        self.data_processing['layout_channel_number'] = [_ch for _ch in self.layout['channel']]
        self.data_processing['layout_channel_label'] = [_lb for _lb in self.layout['label']]
        self.epochs_raw, auto_detected_bad_channels = self.get_epochs(channels=self.channels,
                                                                      data_raw=self.data_raw,
                                                                      triggers=triggers,
                                                                      low_pass_freq=self.low_pass_freq,
                                                                      high_pass_freq=self.high_pass_freq,
                                                                      notch_filter=self.notch_frequencies,
                                                                      epoch_length=epoch_length,
                                                                      resampling_fs=resampling_fs,
                                                                      bad_channels=self.bad_channels,
                                                                      **kwargs)

        # detect bad channels across epochs
        _d_bad_channels = self.detect_bad_channels(epochs=self.epochs_raw, channels=self.channels, **kwargs)
        return [_ch for _ch in list(set([_o for _o in np.concatenate((auto_detected_bad_channels, _d_bad_channels))]))]

    def remove_oeg_artifacts(self, triggers={}, epoch_length=None, **kwargs):
        if self.oeg_channels.size:
            # separate oog channels from scalp channels
            # get oeg data
            oeg_epochs, _bad_channels = self.get_epochs(channels=self.oeg_channels,
                                                        epoch_length=epoch_length,
                                                        triggers=triggers,
                                                        high_pass_freq=0.3,
                                                        low_pass_freq=0.7,
                                                        resampling_fs=self._fs,
                                                        descriptor='oeg_epochs',
                                                        **kwargs)
            oeg_epochs = self.reference_epochs(epochs=oeg_epochs)
            # remove oeg artifacts
            epochs_raw = et.eye_artifact_subtraction(epochs=self.epochs_raw, oeg_epochs=oeg_epochs)
            self.epochs_raw = epochs_raw
            if 'oeg_channels' in list(self.data_processing.keys()):
                self.data_processing['oeg_channels'] += [_oeg.label for _oeg in self.oeg_channels]
            else:
                self.data_processing['oeg_channels'] = [_oeg.label for _oeg in self.oeg_channels]
            t = PrettyTable(['oeg channels subtracted'])
            [t.add_row([_oeg.label]) for _oeg in self.oeg_channels]
            log.info(t)
            print(t)

    def set_epochs_raw_ave(self):
        w_ave, w, rn, cum_rn, snr, cum_snr, s_var, w_fft, nk = \
            et.et_weighted_mean(epochs=self.epochs_raw,
                                block_size=max(np.floor(self.epochs_raw.shape[2] / 100), 10),
                                samples_distance=max(np.floor(self.epochs_raw.shape[0] / 256).astype(int), 10),
                                roi_windows=self.roi_windows_in_samples()
                                )

        raw_average = EegAverageEpochs(average=w_ave,
                                       channels=self.channels,
                                       rn=rn,
                                       cum_rn=cum_rn,
                                       snr=snr,
                                       cum_snr=cum_snr,
                                       n_samples_block=nk,
                                       signal_variance=s_var,
                                       fs=self.fs,
                                       amplitude_units=self.amplitude_units,
                                       time_units=self.time_units,
                                       invert_polarity=self.invert_polarity,
                                       data_processing=self.data_processing,
                                       roi_windows=self.roi_windows)
        self.epochs_raw_ave = raw_average

    def roi_windows_in_samples(self):
        roi_samples = []
        for _i, _roi in enumerate(self.get_unique_interval_rois()):
            roi_samples.append(self.time_to_samples(_roi.interval))
        return roi_samples

    def apply_spatial_filtering(self, sf_join_frequencies=None, sf_components=np.array([]), **kwargs):
        self.data_processing['sf_filtering'] = True
        _data = self.find_array(parameters=self.data_processing, descriptor='spatial_filter')
        if _data:
            z = _data['z']
            pwr0 = _data['pwr0']
            pwr1 = _data['pwr1']
            cov = _data['cov']
        else:
            # compute spatial filter
            z, pwr0, pwr1, cov = et_get_spatial_filtering(epochs=self.epochs_raw,
                                                          fs=self.fs,
                                                          sf_join_frequencies=sf_join_frequencies)
            # save the filter
            self.save_array(parameters=self.data_processing,
                            data_type='spatial_filter',
                            data={'z': z,
                                  'pwr0': pwr0,
                                  'pwr1': pwr1,
                                  'cov': cov},
                            descriptor='spatial_filter')
        # compute average components and attach them to spatial_filter
        z_ave, z_w, z_rn, z_cum_rn, z_snr, z_cum_snr, z_s_var, z_w_fft, nk = \
            et.et_weighted_mean(epochs=z,
                                block_size=max(np.floor(z.shape[2] / 100), 10),
                                samples_distance=max(np.floor(z.shape[0] / 256).astype(int), 10),
                                roi_windows=self.roi_windows_in_samples()
                                )

        components_ave = EegAverageEpochs(average=z_ave,
                                          channels=np.array(
                                              [EegChannel(number=_n) for _n in np.arange(z_ave.shape[1])]),
                                          rn=z_rn,
                                          cum_rn=z_cum_rn,
                                          snr=z_snr,
                                          cum_snr=z_cum_snr,
                                          n_samples_block=nk,
                                          signal_variance=z_s_var,
                                          fs=self.fs,
                                          invert_polarity=self.invert_polarity,
                                          amplitude_units=1,
                                          time_units=self.time_units,
                                          roi_windows=self.roi_windows)
        # apply spatial filter
        self.epochs_processed, sf_components = et_apply_spatial_filtering(z=z, pwr0=pwr0, pwr1=pwr1, cov_1=cov,
                                                                          sf_components=sf_components, **kwargs)
        self.spatial_filter.z = z
        self.spatial_filter.pwr0 = pwr0
        self.spatial_filter.pwr1 = pwr1
        self.spatial_filter.cov = cov
        self.spatial_filter.components_ave = components_ave
        self.spatial_filter.component_indexes = sf_components

        t = PrettyTable()
        t.add_column(fieldname='spatial filtering retained components',
                     column=sf_components)
        log.info(t)
        print(t)

    def set_epochs_processed_ave(self, test_frequencies=None):
        w_fft = np.array([])
        freq_tests = []
        f_peaks = []
        cum_rn = []
        cum_snr = []
        nk = None
        if self.average_domain == Domain.time:
            # average de-noised data across epochs
            w_ave, w, rn, cum_rn, snr, cum_snr, s_var, w_fft, nk = \
                et.et_weighted_mean(epochs=self.epochs_processed,
                                    block_size=max(np.floor(self.epochs_processed.shape[2] / 100), 10),
                                    samples_distance=max(
                                        np.floor(self.epochs_processed.shape[0] / 256).astype(int), 10),
                                    roi_windows=self.roi_windows_in_samples()
                                    )

        if self.average_domain == Domain.frequency:
            # average processed data across epochs including frequency average
            w_ave, rn, snr, w_fft, _ht_tests, s_var = \
                et.et_frequency_mean(epochs=self.epochs_processed,
                                     fs=self.fs,
                                     test_frequencies=test_frequencies,
                                     block_size=max(np.floor(self.epochs_processed.shape[2] / 100), 10),
                                     samples_distance=max(
                                         np.floor(self.epochs_processed.shape[0] / 256).astype(int), 10))

            # restructure frequency tests and channel label to them
            f_peaks, freq_tests = self.set_frequency_peaks(hotelling_tests=_ht_tests,
                                                           channels=self.channels,
                                                           s_var=s_var)
        # attach data to class
        self.epochs_processed_ave = EegAverageEpochs(average=w_ave,
                                                     rfft_average=np.abs(w_fft),
                                                     channels=self.channels,
                                                     rn=rn,
                                                     snr=snr,
                                                     cum_rn=cum_rn,
                                                     cum_snr=cum_snr,
                                                     n_samples_block=nk,
                                                     signal_variance=s_var,
                                                     fs=self.fs,
                                                     frequency_test=freq_tests,
                                                     peak_frequency=f_peaks,
                                                     invert_polarity=self.invert_polarity,
                                                     amplitude_units=self.amplitude_units,
                                                     time_units=self.time_units,
                                                     roi_windows=self.roi_windows)

    @staticmethod
    def set_frequency_peaks(hotelling_tests=None, channels=None, s_var=None):
        f_peaks = []
        freq_tests = []
        for _i, (_ht_ch, _ch) in enumerate(zip(hotelling_tests, channels)):
            for _s_ht in _ht_ch:
                _s_ht.label = _ch.label
                freq_tests.append(_s_ht)
                _f_peak = {'channel': _ch.label,
                           'x': _s_ht.frequency_tested,
                           'rn': _s_ht.rn,
                           'snr': _s_ht.snr,
                           'amp': _s_ht.spectral_magnitude,
                           'amp_snr': _s_ht.snr,
                           'significant': bool(_s_ht.p_value < 0.05),
                           'label_peak': "{:10.1f}".format(_s_ht.frequency_tested),
                           'show_label': True,
                           'positive': True,
                           'domain': Domain.frequency,
                           'spectral_phase': _s_ht.spectral_phase}

                f_peaks.append(EegPeak(**_f_peak))
        return f_peaks, freq_tests

    def get_unique_interval_rois(self):
        out = []
        if self.roi_windows is not None and len(self.roi_windows):
            intervals = np.array([_roi.interval for _roi in self.roi_windows])
            b = np.ascontiguousarray(intervals).view(np.dtype((np.void, intervals.dtype.itemsize * intervals.shape[1])))
            _, idx = np.unique(b, return_index=True)
            out = self.roi_windows[idx]
        return out

    def hotelling_t2_test(self, block_time=0.040, **kwargs):
        ht2_de_trend_data = kwargs.get('ht2_de_trend_data', True)
        block_size = int(block_time * self.fs)
        tests = np.array([])
        for _roi_idx, _roi in enumerate(self.get_unique_interval_rois()):
            _samples = self.time_to_samples(_roi.interval)
            data = self.epochs_processed.copy()
            # remove linear trend
            _ini = _samples[0]
            _end = _samples[1]
            if ht2_de_trend_data:
                x = np.expand_dims(np.arange(0, data[_ini:_end, :, :].shape[0]), axis=1)
                for _idx in np.arange(data.shape[2]):
                    _ini_dt = np.maximum(0, _ini - int(self.fs*0.1))
                    _end_dt = np.minimum(data.shape[0], _end + int(self.fs * 0.1))
                    _subset = data[_ini_dt:_end_dt, :, _idx].copy()
                    x_dt = np.expand_dims(np.arange(0, data[_ini_dt:_end_dt, :, :].shape[0]), axis=1)
                    regression = linear_model.LinearRegression()
                    regression.fit(x_dt, _subset)
                    data[_ini:_end, :, _idx] -= regression.predict(x)
            # remove mean
            data[_ini:_end, :, :] -= np.mean(data[_ini:_end, :, :], axis=0)
            block_size = max(0, min(block_size, _samples[1] - _samples[0]))
            n_blocks = np.floor((_samples[1] - _samples[0]) / block_size).astype(np.int)
            samples = np.array([np.mean(data[_ini + _i * block_size: _ini + (_i + 1) * block_size, :, :], 0)
                                for _i in range(n_blocks)])
            if self.epochs_processed_ave.cum_rn is not None:
                epoch_block_size = np.cumsum(self.epochs_processed_ave.n_samples_block)
                for _n, _rn in zip(epoch_block_size, self.epochs_processed_ave.cum_rn):
                    tests = np.append(tests, hotelling_t_square_test(samples[:, :, 0:_n],
                                                                     interval=_roi.interval,
                                                                     channels=self.channelLabels
                                                                     )
                                      )

            else:
                tests = np.append(tests, hotelling_t_square_test(samples))
        if tests is not []:
            for _test in tests:
                _test.detrend = ht2_de_trend_data
        return tests

    def set_individuals_components_maps(self, n_components=11, test_frequencies=None):
        components_maps = []
        n_components = min(n_components, self.spatial_filter.z.shape[1])
        for _component in np.arange(n_components):
            _filtered_data, _ = et_apply_spatial_filtering(z=self.spatial_filter.z, pwr0=self.spatial_filter.pwr0,
                                                           pwr1=self.spatial_filter.pwr1, cov_1=self.spatial_filter.cov,
                                                           sf_components=np.array([_component]))
            freq_tests = []
            w_fft = np.array([])
            f_peaks = []
            cum_rn = None
            cum_snr = None
            nk = None
            if self.average_domain == Domain.time:
                # average de-noised data across epochs
                w_ave, w, rn, cum_rn, snr, cum_snr, s_var, w_fft, nk = \
                    et.et_weighted_mean(epochs=_filtered_data,
                                        block_size=max(np.floor(_filtered_data.shape[2] / 100), 10),
                                        samples_distance=max(np.floor(_filtered_data.shape[0] / 256).astype(int), 10),
                                        roi_windows=self.roi_windows_in_samples()
                                        )
            if self.average_domain == Domain.frequency:
                # average processed data across epochs including frequency average
                w_ave, rn, snr, w_fft, _ht_tests, s_var = \
                    et.et_frequency_mean(epochs=_filtered_data,
                                         fs=self.fs,
                                         test_frequencies=test_frequencies,
                                         block_size=max(np.floor(_filtered_data.shape[2] / 100), 10),
                                         samples_distance=max(np.floor(_filtered_data.shape[0] / 256).astype(int), 10))
                # restructure frequency tests and channel label to them
                f_peaks, freq_tests = self.set_frequency_peaks(hotelling_tests=_ht_tests,
                                                               channels=self.channels,
                                                               s_var=s_var)

            comp_ave = EegAverageEpochs(average=w_ave,
                                        rfft_average=np.abs(w_fft),
                                        channels=self.channels[0:w_ave.shape[1]],
                                        rn=rn,
                                        cum_rn=cum_rn,
                                        snr=snr,
                                        cum_snr=cum_snr,
                                        n_samples_block=nk,
                                        signal_variance=s_var,
                                        fs=self.fs,
                                        frequency_test=freq_tests,
                                        peak_frequency=f_peaks,
                                        invert_polarity=self.invert_polarity,
                                        amplitude_units=self.amplitude_units,
                                        time_units=self.time_units,
                                        descriptor='component_{:d}'.format(_component),
                                        roi_windows=self.roi_windows
                                        )
            components_maps.append(comp_ave)
        self.component_maps_ave = components_maps

    def plot_individuals_components(self,
                                    eeg_topographic_map_channels=np.array([]),
                                    peak_time_windows=[TimePeakWindow()],
                                    component_maps=[EegAverageEpochs],
                                    x_lim_time=None,
                                    y_lim_time=None,
                                    x_lim_freq=None,
                                    y_lim_freq=None,
                                    domain=Domain.time,
                                    **kwargs):
        amplitude_unit = kwargs.get('amplitude_unit', 'microvolt')
        time_unit = kwargs.get('time_unit', 'second')
        fig_format = kwargs.get('fig_format', 'second')
        fontsize = kwargs.get('fontsize', 8.0)

        for _component, comp_ave in enumerate(component_maps):

            self.set_peaks_and_amplitudes(averaged_epochs=comp_ave,
                                          peak_time_windows=peak_time_windows,
                                          amp_sigma_thr=0.0)

            max_chan = np.argmax(np.std(comp_ave.average, axis=0))
            cha_max_pow_label = self.channels[max_chan].label
            # plot time potential fields for average channel
            if domain == Domain.time:
                eegpt.plot_eeg_topographic_map(ave_data=comp_ave,
                                               eeg_topographic_map_channels=[cha_max_pow_label],
                                               figure_dir_path=self.paths.figure_basename_path,
                                               figure_basename='component_time_' + str(_component),
                                               time_unit=time_unit,
                                               amplitude_unit=amplitude_unit,
                                               domain=Domain.time,
                                               title='Single component time domain projection: ' + str(_component),
                                               x_lim=x_lim_time,
                                               y_lim=y_lim_time,
                                               fig_format=fig_format,
                                               fontsize=fontsize)

            # plot frequency potential fields for average channel
            if domain == Domain.frequency:
                eegpt.plot_eeg_topographic_map(ave_data=comp_ave,
                                               eeg_topographic_map_channels=[cha_max_pow_label],
                                               figure_dir_path=self.paths.figure_basename_path,
                                               figure_basename='component_freq_' + str(_component),
                                               time_unit=time_unit,
                                               amplitude_unit=amplitude_unit,
                                               domain=Domain.frequency,
                                               title='Single component frequency domain projection: ' + str(_component),
                                               x_lim=x_lim_freq,
                                               y_lim=y_lim_freq,
                                               fig_format=fig_format,
                                               fontsize=fontsize)

    def append_average_channel(self, averaged_epochs=EegAverageEpochs(), channel_labels=np.array([])):
        across_channels_ave_r, total_rn_r, total_snr_r, s_var = \
            eeg_across_channel_snr_weighted_mean(ave_epochs=averaged_epochs,
                                                 channel_labels=channel_labels,
                                                 roi_windows=self.roi_windows_in_samples()
                                                 )
        # get polarity to add average channel with proper polarity
        pol = (-1.0) ** averaged_epochs.invert_polarity
        # append across channels average to data as another eeg channel

        label = '_'.join(channel_labels) if channel_labels.size else 'ave'

        averaged_epochs.append_eeg_ave_channel(new_channel_data=across_channels_ave_r * pol,
                                               rn=total_rn_r,
                                               snr=total_snr_r,
                                               signal_variance=s_var,
                                               label=label,
                                               electrode_type=ElectrodeType.artificial)

    def append_gfp_channel(self, averaged_epochs=EegAverageEpochs()):
        gfp_data, gfp_var, snr = self.eeg_gfp()
        averaged_epochs.append_eeg_ave_channel(new_channel_data=gfp_data,
                                               rn=0,
                                               snr=snr,
                                               signal_variance=gfp_var,
                                               label='gfp',
                                               electrode_type=ElectrodeType.artificial,
                                               fixed_polarity=True,
                                               roi_windows=self.roi_windows)

    @staticmethod
    def set_peaks_and_amplitudes(averaged_epochs=EegAverageEpochs(),
                                 peak_time_windows=[TimePeakWindow()],
                                 peak_to_peak_measures=[PeakToPeakMeasure()],
                                 **kwargs):
        peaks, amplitudes, new_time_windows = detect_peaks_and_amplitudes(
            epochs_ave=averaged_epochs,
            time_peak_windows=peak_time_windows,
            eeg_peak_to_peak_measures=peak_to_peak_measures,
            **kwargs)
        averaged_epochs.peak_times = peaks
        averaged_epochs.peak_amplitudes = amplitudes
        averaged_epochs.peak_time_windows = new_time_windows
        return new_time_windows

    def interpolate_data(self, data=np.array, **kwargs):
        interpolation_data_points = kwargs.get('interpolation_data_points', {})
        save_plots = kwargs.get('save_plots', True)
        if interpolation_data_points:
            print('interpolating data')
            idx_delete = np.concatenate((np.where(interpolation_data_points['ini'] > data.shape[0])[0],
                                         np.where(interpolation_data_points['end'] > data.shape[0])[0]))

            if np.any(idx_delete):
                interpolation_data_points['end'] = np.delete(interpolation_data_points['end'], idx_delete)
                interpolation_data_points['ini'] = np.delete(interpolation_data_points['ini'], idx_delete)

            if save_plots:
                fig, ax = plt.subplots(1, 1)
                ax.plot(data[:, 0])
            for _ini, _end in zip(interpolation_data_points['ini'], interpolation_data_points['end']):
                new_x = np.linspace(_ini, _end, num=_end - _ini + 1).astype(np.int)
                new_x_ar = np.tile(np.atleast_2d(new_x).T, (1, data.shape[1]))
                data[new_x, :] = (new_x_ar - _ini) * (data[_end, :] - data[_ini, :]) / (_end - _ini) + data[_ini, :]
            if save_plots:
                ax.plot(data[:, 0])
                m_point = len(interpolation_data_points['ini']) // 2
                for _i in range(10):
                    _fig_path = self.paths.figure_basename_path + '_interpolation_{:d}.png'.format(_i)
                    _ini = max(0, m_point - 2 * 2**_i)
                    _end = min(len(interpolation_data_points['ini']), m_point + 2 * 2**_i)
                    ax.set_xlim(interpolation_data_points['ini'][_ini], interpolation_data_points['ini'][_end])
                    ax.autoscale_view()
                    fig.savefig(_fig_path)
                plt.close(fig)

    @staticmethod
    def detect_bad_channels(epochs=np.array([]), channels=np.array([EegChannel()]), **kwargs):
        thr_sd_bad_channels = kwargs.get('thr_sd_bad_channels', 2)
        interval = kwargs.get('interval', 10)
        amp_thr = kwargs.get('amp_thr', 50000)
        if len(epochs.shape) == 3:
            data = et_unfold(epochs)
        else:
            data = epochs
        sub_data = data[np.arange(0, data.shape[0], interval), :]
        a_max = np.max(np.abs(sub_data), axis=0)
        bad_channels = np.where(np.abs(a_max) > amp_thr)[0]
        t = PrettyTable()
        t.add_column(fieldname='automatic bad channels detection',
                     column=['%s exceeds amplitude threshold of %s' %
                             (channels[_idx].label, amp_thr) for _idx in bad_channels])
        log.info(t)
        print(t)
        _others_idx = np.array([idx for idx in np.arange(sub_data.shape[1]) if idx not in bad_channels])
        a_std = np.std(sub_data[:, _others_idx], axis=0)
        thr_ci = thr_sd_bad_channels * np.std(a_std) + np.mean(a_std)
        n_ch_idx = np.where(a_std > thr_ci)[0]
        bad_idx = _others_idx[n_ch_idx] if n_ch_idx.size else np.array([], dtype=np.int)
        t = PrettyTable()
        t.add_column(fieldname='automatic bad channels detection',
                     column=['%s considered an outlier, across channels std = %f, channel std (%f) > %f * std (%f)' %
                             (channels[_c_idx].label, np.std(a_std), a_std[_c_n_ch] - np.mean(a_std),
                              thr_sd_bad_channels,
                              thr_ci - np.mean(a_std))
                             for _c_idx, _c_n_ch in zip(bad_idx, n_ch_idx)])
        log.info(t)
        print(t)
        bad_channels = np.concatenate((bad_channels, bad_idx))
        _bad_channels_index = np.unique(bad_channels)
        bad_channel_list = [channels[_idx] for _idx in _bad_channels_index]
        return bad_channel_list

    def remove_channels(self, channels_to_remove=np.array([EegChannel()]), keep=np.array([EegChannel()])):
        if (isinstance(keep, list) and len(keep) == 0) or keep is None:
            keep = np.array([EegChannel()])

        channels_to_remove = [_b_ch for _b_ch in channels_to_remove for _k in keep if _k.__dict__ != _b_ch.__dict__]
        t = PrettyTable(['Removed Channels'])
        for _in_ch in channels_to_remove:
            for _idx, _ch in enumerate(self.channels):
                if _ch.label == _in_ch.label:
                    self.channels = np.delete(self.channels, _idx)
                    self.epochs_raw = np.delete(self.epochs_raw, _idx, 1)
                    t.add_row([_ch.label])
                    if 'removed_bad_channels' in list(self.data_processing.keys()):
                        self.data_processing['removed_bad_channels'] += [_ch.label]
                    else:
                        self.data_processing['removed_bad_channels'] = [_ch.label]
                    break
        log.info(t)
        print(t)

    @staticmethod
    def swap_channels(data=np.array([]),
                      channels=np.array([EegChannel()]),
                      channel_labels=[('label_from', 'label_to')]):
        for _left, _right in channel_labels:
            [(ch_left, pos_from)] = [(_ch, _pos) for _pos, _ch in enumerate(channels) if _ch.label == _left]
            [(ch_right, pos_to)] = [(_ch, _pos) for _pos, _ch in enumerate(channels) if _ch.label == _right]
            if not (ch_left and ch_right):
                print("could not find %s and %s pair of channel to perform swap" % (_left, _right))
                continue
            ch_left.label = _right
            ch_right.label = _left
            if data.ndim == 2:
                data[:, [pos_from, pos_to]] = data[:, [pos_to, pos_from]]
            if data.ndim == 3:
                data[:, [pos_from, pos_to], :] = data[:, [pos_to, pos_from], :]

    @staticmethod
    def remove_channels_from_channel_list(channels_to_remove=np.array([EegChannel()]),
                                          channels=np.array([EegChannel()])):
        _str_list = ' '.join(map(str, [_ch.label for _ch in channels]))
        for _in_ch in channels_to_remove:
            for _idx, _ch in enumerate(channels):
                if _ch.label == _in_ch.label:
                    channels.pop(_idx)
                    print('%s channel was removed from a list of channels: %s' % (_ch.label, _str_list))
                    break

    @staticmethod
    def detect_ref_channel(data, interval=10):
        # find best reference electrode
        rank = []
        for i in range(data.shape[1]):
            _var = []
            a = data[np.arange(0, data.shape[0], interval), :] - \
                np.expand_dims(data[np.arange(0, data.shape[0], interval), i], 1)
            for j in np.arange(a.shape[1]):
                _var.append(np.var(a[:, j], axis=0))
            rank.append(np.std(_var))
        return np.argmin(rank)

    def filter_data(self, data=np.array([]), blocks=None, low_pass=None, high_pass=None, plot_filter_response=False):
        if not low_pass and not high_pass:
            return data
        mp_arr = multiprocessing.Array(ctypes.c_double, data.size, lock=False)
        arr = np.frombuffer(mp_arr)
        filtered_signal = arr.reshape(data.shape)
        np.copyto(filtered_signal, data)

        _b_l = None
        _a_l = None

        if low_pass is not None:
            low = 2 * low_pass / self._fs
            _b_l, _a_l = signal.butter(N=3, Wn=low, btype='lowpass', analog=False)
            filt_filt_multithread(filtered_data=filtered_signal, data=data, b=_b_l, a=_a_l)
        if high_pass is not None:
            high = 2 * high_pass / self._fs
            _b_h, _a_h = signal.butter(N=3, Wn=high, btype='highpass', analog=False)
            filt_filt_multithread(filtered_data=filtered_signal, data=filtered_signal, b=_b_h, a=_a_h)

        if plot_filter_response and (low_pass or high_pass is not None):
            w, h = signal.freqz(_b_l, _a_l, 4096)
            plt.plot(self._fs / 2.0 * w / np.pi, 20 * np.log10(abs(h)))
            plt.xscale('log')
            plt.xlabel('Frequency [Hz]')
            plt.ylabel('Amplitude [dB]')
            plt.margins(0, 0.1)
            plt.grid(which='both', axis='both')
            plt.show()
            w, h = signal.freqz(_b_h, _a_h, 4096)
            plt.plot(self._fs / 2.0 * w / np.pi, 20 * np.log10(abs(h)))
            plt.xscale('log')
            plt.xlabel('Frequency [Hz]')
            plt.ylabel('Amplitude [dB]')
            plt.margins(0, 0.1)
            plt.grid(which='both', axis='both')
            plt.show()

            plt.plot(np.hstack((filtered_signal, data)))
            plt.show()
            plt.plot(np.arange(data.shape[0]) * self._fs / data.shape[0],
                     np.abs(np.fft.fft(np.hstack((data, filtered_signal)), axis=0)))
            plt.show()

        return filtered_signal

    @staticmethod
    def interpolate_triggers2(triggers=np.array([]), factor=2):
        idx = np.array([], dtype=np.int)
        if factor > 1:
            for _i, (_ini, _end) in enumerate(zip(triggers[0:-1], triggers[1:])):
                _samples = np.linspace(_ini, _ini + (_end - _ini) / factor, factor).astype(np.int)
                idx = np.append(idx, _samples)
            #  append last items
            mean_trigger_diff = np.round(np.mean(np.diff(triggers, axis=0)))
            _samples = np.linspace(triggers[-1], triggers[-1] + mean_trigger_diff / factor, factor).astype(np.int)
            idx = np.append(idx, _samples)
        else:
            for _i, _c_idx in enumerate(triggers[0:-1: int(1 / factor)]):
                idx = np.append(idx, _c_idx)
        t = PrettyTable()
        t.add_column(fieldname='Initial number of triggers', column=[len(triggers)])
        t.add_column(fieldname='Final number of triggers (interpolated)', column=[len(idx)])
        log.info(t)
        print(t)
        return idx

    @staticmethod
    def interpolate_triggers(triggers={}, factor=2):
        code = np.array([], dtype=np.int)
        idx = np.array([], dtype=np.int)
        dur = np.array([])
        dur_samples = np.array([], dtype=np.int)
        max_distance = np.array([], dtype=np.int)
        min_distance = np.array([], dtype=np.int)
        position = np.array([])
        if factor > 1:
            for _i, (_ini, _end) in enumerate(zip(triggers['idx'][0:-1], triggers['idx'][1:])):
                _samples = np.linspace(_ini, _ini + (_end - _ini) / factor, factor).astype(np.int)
                idx = np.append(idx, _samples)
                dur = np.append(dur, [triggers['idx'][_i]]*len(_samples))
                dur_samples = np.append(dur_samples, [triggers['dur_samples'][_i]]*len(_samples))
                code = np.append(code, [triggers['code'][_i]] * len(_samples))
                position = np.append(position, [triggers['position'][_i]] * len(_samples))
        else:
            for _i, _c_idx in enumerate(triggers['idx'][0:-1: int(1/factor)]):
                idx = np.append(idx, _c_idx)
                dur = np.append(dur, [triggers['idx'][_i]])
                dur_samples = np.append(dur_samples, [triggers['dur_samples'][_i]])
                code = np.append(code, [triggers['code'][_i]])
                position = np.append(position, [triggers['position'][_i]])

        max_distance = [np.max(np.diff(idx))] * len(idx)
        min_distance = [np.min(np.diff(idx))] * len(idx)
        out = {'idx': idx,
               'dur': dur,
               'dur_samples': dur_samples,
               'max_distance': max_distance,
               'min_distance': min_distance,
               'code': code,
               'position': position,
               'triggers': triggers['triggers']}
        return out

    def eeg_gfp(self):
        gfp = np.std(self.epochs_processed_ave.average, axis=1).reshape((-1, 1))
        roi_samples = self.roi_windows_in_samples()
        _data_rois = get_in_window_data(data=gfp, roi_windows=roi_samples)
        s_var = []
        snr = []
        for _data in _data_rois:
            s_var.append(np.var(_data, axis=0))
            snr.append(np.Inf * u.dimensionless_unscaled)
        return gfp, s_var, snr


def eeg_across_channel_snr_weighted_mean(ave_epochs=EegAverageEpochs(), channel_labels=[],
                                         roi_windows=np.array([])):
    channel_labels = np.array(channel_labels)
    is_scalp_ch = ave_epochs.is_scalp_channel()

    if channel_labels.size:
        _idx_channels = np.array([_i_ch for _label in channel_labels for _i_ch, _ch in
                                  enumerate(ave_epochs.channels) if _label == _ch.label and is_scalp_ch[_i_ch]])
    else:
        _idx_channels = np.array([_i_ch for _i_ch, _ch in enumerate(ave_epochs.channels) if is_scalp_ch[_i_ch]])

    across_channels_ave_r, total_rn_r, total_snr_r, s_var = \
        et_snr_weighted_mean(averaged_epochs=ave_epochs.average,
                             fs=ave_epochs.fs,
                             rn=ave_epochs.rn,
                             snr=ave_epochs.get_max_snr_per_channel(),
                             channel_idx=_idx_channels,
                             roi_windows=roi_windows)
    return across_channels_ave_r, total_rn_r, total_snr_r, s_var
