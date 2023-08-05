from peegy.processing.pipe.definitions import InputOutputProcess
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.ticker import FormatStrFormatter
from PyQt5.QtCore import QLibraryInfo
from peegy.tools.units.unit_tools import set_default_unit
import astropy.units as u
from matplotlib.ticker import AutoMinorLocator

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(QLibraryInfo.PluginsPath)


class InterpolateData(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 ini_end_points: np.array = np.array([[], []]),
                 save_plots: bool = True,
                 n_plots: int = 9,
                 fig_format: str = '.png',
                 fontsize: float = 8,
                 idx_channels_to_plot: np.array = np.array([0]),
                 user_naming_rule: str = 'interpolation',
                 **kwargs):
        """
        This class will interpolate data on each channel at a between two points passed in ini_end_points
        :param input_process: an InputOutput process
        :param ini_end_points: a Nx2 numpy array with the interpolation points
        :param save_plots: bool, if true, figures will be generated and saved showing a zoomed progression of the interp
        :param n_plots: int: number of plots (with different zoom scales) to be generated
        :param fig_format: string indicating the format of the output figure (e.g. '.png' or '.pdf')
        :param fontsize: size of fonts in plot
        :param idx_channels_to_plot: np.array indicating the index of the channels to plot
        :param user_naming_rule: string indicating a user naming to be included in the figure file name
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(InterpolateData, self).__init__(input_process=input_process, **kwargs)
        self.ini_end_points = ini_end_points
        self.save_plots = save_plots
        self.n_plots = n_plots
        self.fig_format = fig_format
        self.fontsize = fontsize
        self.idx_channels_to_plot = idx_channels_to_plot
        self.user_naming_rule = user_naming_rule
        self.fontsize = fontsize

    def transform_data(self):
        if self.ini_end_points.size:
            print('Interpolating data')
            idx_delete = np.concatenate((np.where(self.ini_end_points[:, 0] >
                                                  self.input_node.data.shape[0] - 1)[0],
                                         np.where(self.ini_end_points[:, 1] >
                                                  self.input_node.data.shape[0] - 1)[0]))

            if np.any(idx_delete):
                self.ini_end_points = np.delete(self.ini_end_points, idx_delete, 0)
            self.output_node.data = self.input_node.data.copy()
            for _i in range(self.ini_end_points.shape[0]):
                _ini = self.ini_end_points[_i, 0]
                _end = self.ini_end_points[_i, 1]
                new_x = np.linspace(_ini, _end, num=_end - _ini + 1).astype(np.int)
                new_x_ar = np.tile(np.atleast_2d(new_x).T, (1, self.input_node.data.shape[1]))
                self.output_node.data[new_x, :] = ((new_x_ar - _ini) * (self.output_node.data[_end, :] -
                                                                        self.output_node.data[_ini, :]) /
                                                   (_end - _ini) + self.output_node.data[_ini, :])
            if self.save_plots:
                for _idx_channel in self.idx_channels_to_plot:
                    fig, ax = plt.subplots(1, 1)
                    ax.plot(self.input_node.x, self.input_node.data[:, _idx_channel])
                    ax.plot(self.input_node.x, self.output_node.data[:, _idx_channel])
                    ax.plot(self.input_node.x[self.ini_end_points[:, 0]],
                            self.output_node.data[self.ini_end_points[:, 0], _idx_channel],
                            'o', color='k', markersize=2)
                    ax.plot(self.input_node.x[self.ini_end_points[:, 1]],
                            self.output_node.data[self.ini_end_points[:, 1], _idx_channel],
                            'o', color='r', markersize=2)
                    m_point = self.ini_end_points.shape[0] // 2
                    figure_dir_path = self.input_node.paths.figures_current_dir
                    _sep = '_' if self.user_naming_rule is not None else ''
                    figure_basename = self.name + _sep + self.user_naming_rule
                    for _i in range(self.n_plots):
                        _label = self.input_node.layout[_idx_channel].label
                        _fig_path = figure_dir_path + os.path.sep + _label + '_' + figure_basename + '_{:}{:}'.format(
                            _i, self.fig_format)
                        _ini = max(0, m_point - 2 * 2 ** _i)
                        _end = min(self.ini_end_points.shape[0], m_point + 2 * 2 ** _i)
                        ax.set_xlim(self.input_node.x[self.ini_end_points[_ini, 0]],
                                    self.input_node.x[self.ini_end_points[_end, 0]])
                        ax.autoscale_view()
                        ax.set_xlabel('Time [{:}]'.format(self.input_node.x.unit), fontsize=self.fontsize)
                        ax.set_ylabel('Amplitude [{:}]'.format(self.input_node.data.unit), fontsize=self.fontsize)
                        ax.xaxis.set_major_formatter(FormatStrFormatter('%.3f'))
                        ax.xaxis.set_minor_locator(AutoMinorLocator())
                        fig.tight_layout()
                        fig.savefig(_fig_path)
                        print('saving interpolated figures in {:}'.format(_fig_path))
                    plt.close(fig)


class PeriodicInterpolation(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 interpolation_rate=None,
                 interpolation_width=0.0,
                 interpolation_offset=0.0,
                 event_code=0.0,
                 user_naming_rule='',
                 **kwargs):
        """
        This class will interpolate data on each channel at a given rate using as a reference time the position of
        trigger events
        :param input_process: InputOutputProcess Class
        :param interpolation_rate: rate (in Hz) to interpolate data points
        :param interpolation_width: the width (in sec) of the interpolation region
        :param interpolation_offset: an offset (in sec) in reference to trigger events
        :param event_code: the event code that will be use as reference to start interpolating
        :param user_naming_rule: string indicating a user naming to be included in the figure file name
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(PeriodicInterpolation, self).__init__(input_process=input_process, **kwargs)
        self.interpolation_rate = set_default_unit(interpolation_rate, u.Hz)
        self.interpolation_width = set_default_unit(interpolation_width, u.s)
        self.interpolation_offset = set_default_unit(interpolation_offset, u.s)
        self.event_code = event_code
        self.user_naming_rule = user_naming_rule

    def transform_data(self):
        _events = self.input_node.events.get_events(self.event_code)
        _event_times = [_e.time_pos for _e in _events]

        _ini_points = np.array([])
        for _start, _end in zip(_event_times[:-1], _event_times[1::]):
            if self.interpolation_rate is not None:
                _ini_points = np.concatenate((_ini_points, np.arange(_start.to(u.s).value,
                                                                     _end.to(u.s).value,
                                                                     1. / self.interpolation_rate.to(u.Hz).value)))
            else:
                _ini_points = np.append(_ini_points, _start)

        if self.interpolation_rate is not None:
            _ini_points = np.concatenate((_ini_points,
                                          np.arange(_event_times[-1].to(u.s).value,
                                                    self.input_node.data.shape[0] / self.input_node.fs.to(u.Hz).value,
                                                    1. / self.interpolation_rate.to(u.Hz).value))) * u.s
        _ini_points = _ini_points - self.interpolation_offset
        _end_points = _ini_points + self.interpolation_width
        ini_end_points = (np.array([_ini_points, _end_points]).T * self.input_node.fs.to(u.Hz).value).astype(np.int)
        interp_data = InterpolateData(input_process=self.input_process,
                                      ini_end_points=ini_end_points,
                                      user_naming_rule=self.user_naming_rule)
        interp_data.run()
        self.output_node = interp_data.output_node
