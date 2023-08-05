from peegy.definitions.channel_definitions import Domain, ChannelItem, ChannelType
from peegy.processing.statistics.definitions import StatisticalTests
from peegy.directories.tools import DirectoryPaths
from peegy.definitions.events import Events
from peegy.tools.units.unit_tools import set_default_unit
import inspect
import pandas as pd
import io
import gc
import astropy.units as u
import itertools
import abc
import matplotlib.pyplot as plt
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
pg.setConfigOption('leftButtonPan', False)


class DataNode(object):
    """
    Core data object used to keep data. During the creation, it requires the sampling rate and the actual data.
    Data is passed in a numpy array of n * m or n * m * t, where n represent samples, m channels, and t trials.
    Units are passed via unit kargs (default units is microVolts)
    """
    def __init__(self,
                 fs=None,
                 data: np.array = np.array([]),
                 domain=Domain.time,
                 x_offset=0.0 * u.s,
                 n_fft=None,
                 layout: np.array([ChannelItem]) = None,
                 process_history=[],
                 events: Events = None,
                 events_annotations: () = None,
                 paths: DirectoryPaths = None,
                 rn: np.array = None,
                 rn_df: np.array = None,
                 cum_rn: np.array = None,
                 snr: np.array = None,  # it may content snr for different ROIs
                 cum_snr: np.array = None,
                 s_var=None,
                 alpha=0.05,
                 n: int = None,
                 w: np.array = None,
                 statistical_tests: StatisticalTests = StatisticalTests(),
                 peak_times=None,
                 peak_frequency=None,
                 peak_to_peak_amplitudes=None,
                 peak_time_windows=None,
                 roi_windows=None,
                 markers=None
                 ):
        # n * m * t data array
        # if data represent time or frequency
        # time offset from origin
        # layout
        # list used to store processing history that resulted in the current data

        self.fs = fs
        self._data = data
        self.domain = domain
        self.x_offset = x_offset
        self.layout = layout
        self.events = events
        self.events_annotations = events_annotations
        self.process_history = process_history
        self.paths = paths
        # signal statistics
        self.rn = rn
        self.cum_rn = cum_rn
        self.snr = snr
        self.cum_snr = cum_snr
        self.s_var = s_var
        self.n = n
        self.rn_df = rn_df
        self.w = w
        self.alpha = alpha
        self.statistical_tests = statistical_tests
        # peak measures
        self.peak_times = peak_times
        self.peak_frequency = peak_frequency
        self.peak_to_peak_amplitudes = peak_to_peak_amplitudes
        self.peak_time_windows = peak_time_windows
        self.roi_windows = roi_windows
        self.markers = markers
        self.n_fft = n_fft
        if self.layout is None and data.size:
            self.layout = np.array([ChannelItem() for _ in range(self.data.shape[1])])  # default channel information
        self._x = None
        self._y = None

    def get_x(self):
        if self.domain == Domain.time:
            out = np.arange(self.data.shape[0]) / self.fs - self.x_offset
            out = out.to(u.s)
        if self.domain == Domain.frequency:
            out = np.arange(self.data.shape[0]) * self.fs / self.n_fft
            out = out.to(u.Hz)
        if self.domain == Domain.time_frequency:
            out = self._x
        return out

    def set_x(self, value):
        self._x = value
    x = property(get_x, set_x)

    def get_y(self):
        return self._y

    def set_y(self, value):
        self._y = value

    y = property(get_y, set_y)

    def apply_layout(self, layout=None):
        for _s_i in layout.layout:
            for _i, _l in enumerate(self.layout):
                if _l.idx == _s_i.idx:
                    self.layout[_i] = _s_i
                    break

    def delete_channel_by_idx(self, idx: np.array = np.array([])):
        labels = '/'.join([_ch.label for _ch in self.layout[idx]])
        self.data = np.delete(self.data, idx, 1)
        self.layout = np.delete(self.layout, idx)
        print('removed channels: ' + ''.join(labels))

    def delete_channel_by_label(self, label=''):
        _idx = np.array([_i for _i, _lay in enumerate(self.layout) if _lay.label == label])
        self.delete_channel_by_idx(idx=_idx)

    def get_channel_idx_by_label(self, labels: np.array([str]) = None):
        if labels is None:
            labels = np.array([_channel.label for _channel in self.layout])
        if isinstance(labels, list):
            labels = np.array(labels)
        # ensure unique labels and remove repeated in same order
        _, idx_labels = np.unique(labels, return_index=True)
        labels = labels[np.sort(idx_labels)]
        all_labels = np.array([_channel.label for _idx, _channel in enumerate(self.layout)])
        idx = []
        for _label in labels:
            _idx = np.argwhere(_label == all_labels)
            if _idx.size:
                idx.append(_idx.squeeze())
        idx = np.array(idx)
        return idx

    def get_channel_idx_by_type(self, channel_type=ChannelType.Event):
        all_idx = np.array([_idx for _idx, _channel in enumerate(self.layout) if _channel.type == channel_type])
        idx = np.unique(all_idx)
        return idx

    def get_channel_label_by_idx(self, idx: np.array = np.array([])) -> [str]:
        if idx.size == 0:
            idx = np.arange(self.layout.size)
        labels = [_ch.label for _ch in self.layout[idx]]
        return labels

    def set_data(self, value=np.array):
        self._data = value

    def get_data(self):
        return self._data
    data = property(get_data, set_data)

    def get_max_snr_per_channel(self):
        if self.snr is not None:
            max_snr = np.nanmax(np.atleast_2d(self.snr), axis=0)
        else:
            max_snr = np.array([None] * self._data.shape[1])
        return np.atleast_1d(np.squeeze(max_snr))

    def get_max_s_var_per_channel(self):
        max_var = np.nanmax(self.s_var, axis=0)
        return np.atleast_1d(np.squeeze(max_var))

    def x_to_samples(self, value: np.array) -> np.array:
        out = np.array([])
        for _v in value:
            _value = _v.to(self.x.unit).value
            if np.isinf(_value):
                out = np.append(out, _value)
            else:
                out = np.append(out, np.argmin(np.abs(self.x.value - np.array(_value)))).astype(np.int)
        return out

    def data_to_pandas(self):
        _row_test = []
        if self._data.size:
            for i in range(self._data.shape[1]):
                data_binary_x = io.BytesIO()
                np.save(data_binary_x, self.x.value)
                data_binary_y = io.BytesIO()
                np.save(data_binary_y, self.data[:, i].value)
                data_binary_x.seek(0)
                data_binary_y.seek(0)
                _row_time_data = {'domain': self.domain,
                                  'channel': self.layout[i].label,
                                  'x': data_binary_x.read(),
                                  'y': data_binary_y.read(),
                                  'x_unit': self.x.unit.to_string(),
                                  'y_unit': self.data[:, i].unit.to_string(),
                                  'snr': self.get_max_snr_per_channel()[i]}
                _row_test.append(_row_time_data)
        _data_pd = pd.DataFrame(_row_test)
        return _data_pd

    def append_new_channel(self, new_data: np.array = None, layout_label: str = ''):
        new_channel = ChannelItem(label=layout_label)
        self.layout = np.append(self.layout, new_channel)
        self.data = np.append(self.data.value, new_data.to_value(self.data.unit), axis=1) * self.data.unit
        self.rn = np.append(self.rn, np.nan)
        if self.snr is not None:
            self.snr = np.append(self.snr, np.nan)
        if self.s_var is not None:
            self.s_var = np.append(self.s_var, np.nan)

    def clip(self, ini_time: u.Quantity = 0 * u.s, end_time: u.Quantity = np.inf * u.s):
        ini_time = set_default_unit(ini_time, u.s)
        end_time = set_default_unit(end_time, u.s)
        if np.isinf(end_time):
            end_time = self.x[-1]
        samples = self.x_to_samples(np.array([ini_time.to(u.s).value,
                                              end_time.to(u.s).value]) * u.s)
        _extact_time_offset = self.x[samples[0]]
        self._data = self._data[samples[0]: samples[-1], ::]
        self.events.clip(ini_time=ini_time, end_time=end_time)
        # apply offset
        self.events.set_offset(time_offset=_extact_time_offset)


class InputOutputQtFigure(object):
    """
    This class is a wrapper to allow sphinx showing qt figures
    """
    def __init__(self, figure: pg.GraphicsWindow = None):
        self.figure = figure

    def _repr_html_(self):
        ex = pg.exporters.SVGExporter(self.figure.scene())
        out = ex.export(toBytes=True)
        html__figure_exporter = out.decode("utf-8")
        return html__figure_exporter


class InputOutputProcess(metaclass=abc.ABCMeta):
    """
    Core abstract input-output function. Each inherit class must provide an input data, a process function and and
    output data set
    """
    def __init__(self, input_process: object = None,
                 keep_input_node=True,
                 **kwargs):
        self.input_process: InputOutputProcess = input_process if input_process is not None else self  # Input data
        # must be InputOutputProcess class
        self.function_args: dict = kwargs
        self.input_node: DataNode = None
        self.output_node: DataNode = None
        self.process_parameters: dict = kwargs  # dict with all the parameters used in process function
        self.keep_input_node: bool = keep_input_node
        self.figures: [plt.Figure] = None
        self.name: str = None
        self.ready = False
        if self.name is None:
            self.name = self.__class__.__name__

    def transform_data(self):
        return 'core method to generate output data'

    def run(self):
        self.input_node = self.input_process.output_node
        callable_list = [_i for _i in dir(DataNode) if callable(getattr(DataNode, _i))]
        properties_list = [_i[0] for _i in inspect.getmembers(DataNode, lambda o: isinstance(o, property))]
        attributes = [a for a in dir(self.input_node) if not (a.startswith('__') or a.startswith('_')) and
                      a not in callable_list and a not in properties_list]
        pars = {_a: getattr(self.input_node, _a) for _a in attributes}
        self.output_node = DataNode(data=np.array([]),
                                    **pars
                                    )  # Output data must be DataNode class
        self.transform_data(**self.function_args)
        self.ready = True

        if not self.keep_input_node:
            if isinstance(self.input_node, DataNode):
                self.input_node.data = None
            self.input_node = None
            gc.collect()
        return

    def plot(self,
             plot_input: bool = False,
             plot_output: bool = True,
             ch_to_plot: [str] = None,
             interactive: bool = True):
        """
        This method will plot data in the input and/or the output node.
        :param plot_input: bool indicating if input_node data should be plotted
        :param plot_output: bool indicating if output_node data should be plotted
        :param ch_to_plot: list of strings indicating the labels of the channels to be shown. If empty, all channels
        will be shown.
        :param interactive: boolean indicating if plot should be interactive or not
        """
        win = plot_input_output_process(input_output_process=self,
                                        plot_input=plot_input,
                                        plot_output=plot_output,
                                        ch_to_plot=ch_to_plot
                                        )
        out = InputOutputQtFigure(figure=win)
        if interactive:
            QtGui.QApplication.instance().exec_()
        return out


def plot_input_output_process(input_output_process: InputOutputProcess = None,
                              plot_input: bool = False,
                              plot_output: bool = True,
                              ch_to_plot: [str] = None):
    """
    This method will plot data in the input and/or the output node.
    :param input_output_process: InputOutputProcess for which plot will be generated.
    :param plot_input: bool indicating if input_node data should be plotted
    :param plot_output: bool indicating if output_node data should be plotted
    :param ch_to_plot: list of strings indicating the labels of the channels to be shown. If empty, all channels
    will be shown.
    """
    if not plot_input and not plot_output:
        return
    symbols = itertools.cycle(
        ['o', 's', 't', 'd', '+', 't1', 't2', 't3', 'p', 'h', 'star', 'x', 'arrow_up', 'arrow_right',
         'arrow_down', 'arrow_left', 'crosshair'])
    data_in = input_output_process.input_node.data
    name_in = input_output_process.input_process.name
    name_out = input_output_process.name
    data_out = input_output_process.output_node.data
    if input_output_process.input_node.domain == Domain.frequency:
        data_in = np.abs(data_in)
    if input_output_process.output_node.domain == Domain.frequency:
        data_out = np.abs(data_out)

    if data_in is not None or data_out is not None:
        win = pg.GraphicsWindow(title=input_output_process.name + '/' +
                                input_output_process.name)
        ax = win.addPlot(row=1, col=1)
        ax.addLegend()
    else:
        return

    offset_in, offset_out = 0, 0
    channels_in, channels_out = [], []
    if data_in is not None and plot_input:
        offset_in = (np.max(np.abs(data_in.flatten() - np.mean(data_in.flatten()))) +
                     np.min(np.abs(data_in.flatten() - np.mean(data_in.flatten())))) / 2
        channels_in = [_l.label for _l in input_output_process.input_node.layout]
    if data_out is not None and plot_output:
        offset_out = (np.max(np.abs(data_out.flatten() - np.mean(data_out.flatten()))) +
                      np.min(np.abs(data_out.flatten() - np.mean(data_out.flatten())))) / 2
        channels_out = [_l.label for _l in input_output_process.output_node.layout]

    if ch_to_plot is not None:
        channels_in = list(set(ch_to_plot) & set(channels_in))
        channels_out = list(set(ch_to_plot) & set(channels_out))

    channels = np.unique(channels_in + channels_out)
    offset = np.maximum(offset_in, offset_out)
    if plot_input and data_in is not None:
        x_in = input_output_process.input_node.x
        ax.setDownsampling(auto=True, mode='peak')
        ax.showGrid(True, True)
        _color = (255, 0, 0)
        for _i, _label in enumerate(channels_in):
            _name = name_in if _i == 0 else None
            _pos = np.argwhere(channels == _label).squeeze()
            if not _pos.size:
                continue
            text_item = pg.TextItem(_label, anchor=(0.0, 0.0))
            text_item.setPos(0, offset.value * _pos)
            if data_in.ndim == 2:
                ax.plot(x_in, data_in[:, _i] - np.mean(data_in[:, _i]) +
                        offset * _pos, pen=_color, name=_name)

            if data_in.ndim == 3:
                for _t in range(data_in.shape[2]):
                    ax.plot(x_in, data_in[:, _i, _t] - np.mean(data_in[:, _i, _t]) +
                            offset * _pos, pen=_color, name=_name)
            ax.addItem(text_item)

            if input_output_process.input_node.events is not None:
                itertools.tee(symbols)
                _codes = np.unique(input_output_process.input_node.events.get_events_code())
                for _code in _codes:
                    _events = input_output_process.input_node.events.get_events_time(code=_code)
                    ax.plot(x=_events.to_value(_events.unit),
                            y=0.0 * _events.value + offset * _pos,
                            pen=None,
                            symbol=next(symbols),
                            symbolBrush=_color,
                            symbolSize=6)

        if input_output_process.input_node.domain == Domain.time:
            ax.setLabel('bottom', "Time [{:}]".format(input_output_process.input_node.x.unit))
            ax.setLabel('left', "Amplitude [{:}]".format(input_output_process.input_node.data.unit))
        if input_output_process.input_node.domain == Domain.frequency:
            ax.setLabel('bottom', "Time [{:}]".format(input_output_process.input_node.x.unit))
            ax.setLabel('left', "Frequency [{:}]".format(input_output_process.input_node.data.unit))

    if plot_output and data_out is not None:
        _color = (0, 0, 255)
        x_out = input_output_process.output_node.x
        ax.setDownsampling(ds=100.0, mode='peak')
        ax.showGrid(True, True)
        for _i, _label in enumerate(channels_out):
            _name = name_out if _i == 0 else None
            _pos = np.argwhere(channels == _label).squeeze()
            if not _pos.size:
                continue
            text_item = pg.TextItem(_label, anchor=(0.0, 0.0))
            text_item.setPos(0, offset.value * _pos)
            if data_out.ndim == 2:
                ax.plot(x_out, data_out[:, _i] - np.mean(data_out[:, _i]) +
                        offset * _pos, pen=_color, name=_name)
            if data_out.ndim == 3:
                for _t in range(data_out.shape[2]):
                    ax.plot(x_out, data_out[:, _i, _t] - np.mean(data_out[:, _i, _t]) +
                            offset * _pos, pen=_color, name=_name)
            ax.addItem(text_item)
            if input_output_process.output_node.events is not None:
                itertools.tee(symbols)
                _codes = np.unique(input_output_process.output_node.events.get_events_code())
                for _code in _codes:
                    _events = input_output_process.output_node.events.get_events_time(code=_code)
                    ax.plot(x=_events,
                            y=0.0 * _events.value + offset * _pos,
                            pen=None,
                            symbol=next(symbols),
                            symbolBrush=_color,
                            symbolSize=6)

        if input_output_process.output_node.domain == Domain.time:
            ax.setLabel('bottom', "Time [{:}]".format(input_output_process.output_node.x.unit))
            ax.setLabel('left', "Amplitude [{:}]".format(input_output_process.output_node.data.unit))
        if input_output_process.output_node.domain == Domain.frequency:
            ax.setLabel('bottom', "Time [{:}]".format(input_output_process.output_node.x.unit))
            ax.setLabel('left', "Frequency [{:}]".format(input_output_process.output_node.data.unit))
    pg.QtGui.QApplication.processEvents()
    return win
