import copy
from tqdm import tqdm
from peegy.processing.pipe.definitions import InputOutputProcess
import matplotlib.pyplot as plt
from peegy.plot import eeg_ave_epochs_plot_tools as eegpt
from peegy.processing.tools.video.recording import Recorder
import numpy as np
import os
import astropy.units as u
from peegy.tools.units.unit_tools import set_default_unit
import gc
from PyQt5.QtCore import QLibraryInfo
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(QLibraryInfo.PluginsPath)


class PlotWaveforms(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 overlay: [InputOutputProcess] = None,
                 ch_to_plot: np.array = None,
                 title: str = '',
                 plot_x_lim: [float, float] = None,
                 plot_y_lim: [float, float] = None,
                 offset_step: u.quantity.Quantity = None,
                 return_figures: bool = False,
                 statistical_test: str = None,
                 show_following_stats: [str] = None,
                 fig_format: str = '.png',
                 fontsize: float = 12,
                 user_naming_rule: str = '',
                 save_to_file: bool = True,
                 show_peaks: bool = True,
                 show_labels: bool = True,
                 **kwargs):
        """
        This InputOutputProcess plots all channel waveforms in a single plot and saves them.
        :param input_process: an InputOutput process
        :param ch_to_plot: numpy array with index or labels of channels to plot
        :param overlay: list of InputOutputProcess to overlay
        :param title: title of the plot
        :param plot_x_lim: x limits of the plot
        :param plot_y_lim: y limits of the plot
        :param offset_step: offset between different channels
        :param return_figures: If true, handle to figure will be passed to self.figures
        :param statistical_test: name of statistical test to extract information.
        :param show_following_stats: list of string indicating which parameters found in statistical_tests are shown
        :param fig_format: string indicating the format of the output figure (e.g. '.png' or '.pdf')
        :param fontsize: size of fonts in plot
        :param idx_channels_to_plot: np.array indicating the index of the channels to plot
        :param user_naming_rule: string indicating a user naming to be included in the figure file name
        :param save_to_file: if True, figure will be saved
        :param show_peaks: if True, detected peaks will be shown
        :param show_labels: if True, peak labels will be shown
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(PlotWaveforms, self).__init__(input_process=input_process, **kwargs)
        self.ch_to_plot = ch_to_plot
        self.title = title
        self.plot_x_lim = plot_x_lim
        self.plot_y_lim = plot_y_lim
        self.offset_step = set_default_unit(offset_step, u.uV)
        self.fig_format = fig_format
        self.fontsize = fontsize
        self.user_naming_rule = user_naming_rule
        self.overlay = overlay
        self.statistical_test = statistical_test
        self.show_following_stats = show_following_stats
        self.return_figures = return_figures
        self.save_to_file = save_to_file
        self.show_peaks = show_peaks
        self.show_labels = show_labels

    def transform_data(self):
        figure_dir_path = self.input_node.paths.figures_current_dir
        _sep = '_' if self.user_naming_rule is not None else ''
        figure_basename = self.input_process.name + _sep + self.user_naming_rule
        to_plot = [self.input_node]
        if self.overlay is not None:
            to_plot += [_in.output_node for _in in self.overlay]

        figure = eegpt.plot_single_channels(ave_data=to_plot,
                                            channels=self.ch_to_plot,
                                            figure_dir_path=figure_dir_path,
                                            figure_basename=figure_basename,
                                            title=self.title,
                                            x_lim=self.plot_x_lim,
                                            y_lim=self.plot_y_lim,
                                            offset_step=self.offset_step,
                                            fig_format=self.fig_format,
                                            fontsize=self.fontsize,
                                            statistical_test=self.statistical_test,
                                            show_following_stats=self.show_following_stats,
                                            save_to_file=self.save_to_file,
                                            show_peaks=self.show_peaks,
                                            show_labels=self.show_labels
                                            )
        if self.return_figures:
            self.figures = figure
        else:
            plt.close(figure)
            gc.collect()


class PlotTopographicMap(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 topographic_channels: np.array([str]) = np.array([]),
                 title: str = '',
                 plot_x_lim: list = None,
                 plot_y_lim: list = None,
                 times: np.array = np.array([]),
                 save_to_file: bool = True,
                 fig_format: str = '.png',
                 fontsize: float = 12,
                 user_naming_rule: str = '',
                 return_figures: bool = False,
                 **kwargs
                 ):
        """
        Plot topographic maps of figures at desired times. If the input_process contains time or frequency peaks from
        PeakDetectionTimeDomain or tests such as FTest, AverageEpochsFrequencyDomain, or PhaseLockingValue,
        topographic maps for those peaks will be also shown
        :param input_process: an InputOutput process
        :param topographic_channels: a numpy array (integers index or string with channel labels) indicating channels to
        be plotted
        :param title: string with the desired figure title
        :param plot_x_lim: list with minimum and maximum horizontal range of x axis
        :param plot_y_lim: list with minimum and maximum vertical range of y axis
        :param times: numeric array with times to show topographic maps
        :param save_to_file: if True, figure will be saved
        :param fig_format: string indicating the format of the figure being saved
        :param fontsize: float indicating the size of the fonts
        :param user_naming_rule: string containing an extra text to be included in the name of the figure
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(PlotTopographicMap, self).__init__(input_process=input_process, **kwargs)
        self.topographic_channels = topographic_channels
        self.title = title
        self.plot_x_lim = plot_x_lim
        self.plot_y_lim = plot_y_lim
        self.fig_format = fig_format
        self.fontsize = fontsize
        self.user_naming_rule = user_naming_rule
        self.times = set_default_unit(times, u.s)
        self.return_figures = return_figures
        self.save_to_file = save_to_file

    def transform_data(self):
        _sep = '_' if self.user_naming_rule is not None else ''
        _figure_base_name = self.input_process.name + _sep + self.user_naming_rule
        figures = eegpt.plot_eeg_topographic_map(ave_data=self.input_node,
                                                 eeg_topographic_map_channels=self.topographic_channels,
                                                 figure_dir_path=self.input_node.paths.figures_current_dir,
                                                 figure_basename=_figure_base_name,
                                                 times=self.times,
                                                 domain=self.input_node.domain,
                                                 title=self.title,
                                                 x_lim=self.plot_x_lim,
                                                 y_lim=self.plot_y_lim,
                                                 fig_format=self.fig_format,
                                                 fontsize=self.fontsize,
                                                 return_figures=self.return_figures,
                                                 save_figures=self.save_to_file)
        if self.return_figures:
            self.figures = figures
        else:
            [plt.close(_fig) for _fig in figures]
            gc.collect()


class PlotSpectrogram(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 topographic_channels=np.array([]),
                 title='',
                 plot_x_lim=None,
                 plot_y_lim=None,
                 times=np.array([]),
                 fig_format='.png',
                 fontsize=12,
                 user_naming_rule='',
                 time_window=2.0,
                 sample_interval=0.004,
                 spec_thresh=4
                 ):
        super(PlotSpectrogram, self).__init__(input_process=input_process)
        self.topographic_channels = topographic_channels
        self.title = title
        self.plot_x_lim = plot_x_lim
        self.plot_y_lim = plot_y_lim
        self.fig_format = fig_format
        self.fontsize = fontsize
        self.user_naming_rule = user_naming_rule
        self.times = times
        self.time_window = time_window
        self.sample_interval = sample_interval
        self.spec_thresh = spec_thresh

    def transform_data(self):
        eegpt.plot_eeg_time_frequency_transformation(ave_data=self.input_node,
                                                     eeg_topographic_map_channels=self.topographic_channels,
                                                     figure_dir_path=self.input_node.paths.figure_basename_path,
                                                     figure_basename='{:}{:}'.format(
                                                         self.input_process.name + '_',
                                                         self.user_naming_rule),
                                                     time_unit='s',
                                                     amplitude_unit='uV',
                                                     times=self.times,
                                                     domain=self.input_node.domain,
                                                     title=self.title,
                                                     x_lim=self.plot_x_lim,
                                                     y_lim=self.plot_y_lim,
                                                     fig_format=self.fig_format,
                                                     fontsize=self.fontsize,
                                                     time_window=self.time_window,
                                                     sample_interval=self.sample_interval,
                                                     spec_thresh=self.spec_thresh
                                                     )


class TopographicMapVideo(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 topographic_channels: np.array([str]) = np.array([]),
                 step_size: u.Quantity = None,
                 title: str = '',
                 plot_x_lim: list = None,
                 plot_y_lim: list = None,
                 fig_format: str = '.png',
                 fontsize: float = 12,
                 user_naming_rule: str = '',
                 **kwargs
                 ):
        """
        Generate a video with the topographic over time. If the input_process contains time or frequency peaks from
        PeakDetectionTimeDomain or tests such as FTest, AverageEpochsFrequencyDomain, or PhaseLockingValue,
        topographic maps for those peaks will be also shown
        :param input_process: an InputOutput process
        :param topographic_channels: a numpy array (integers index or string with channel labels) indicating channels to
        be plotted
        :param step_size: step size to generate video in same units as self.input_node.x
        :param title: string with the desired figure title
        :param plot_x_lim: list with minimum and maximum horizontal range of x axis
        :param plot_y_lim: list with minimum and maximum vertical range of y axis
        :param times: numeric array with times to show topographic maps
        :param fig_format: string indicating the format of the figure being saved
        :param fontsize: float indicating the size of the fonts
        :param user_naming_rule: string containing an extra text to be included in the name of the figure
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(TopographicMapVideo, self).__init__(input_process=input_process, **kwargs)
        self.topographic_channels = topographic_channels
        self.step_size = step_size
        self.title = title
        self.plot_x_lim = plot_x_lim
        self.plot_y_lim = plot_y_lim
        self.fig_format = fig_format
        self.fontsize = fontsize
        self.user_naming_rule = user_naming_rule

    def transform_data(self):
        self.step_size = set_default_unit(self.step_size, self.input_node.x.unit)
        self.plot_x_lim = set_default_unit(self.plot_x_lim, self.input_node.x.unit)
        self.plot_y_lim = set_default_unit(self.plot_y_lim, self.input_node.data.unit)

        data_node = copy.copy(self.input_node)
        data_node.peak_times = None
        data_node.peak_frequency = None
        # Generate a video showing the topographic map over time
        _x_values = self.input_node.x
        if self.step_size is not None:
            skip = round((self.step_size * self.input_node.fs).to_value(u.dimensionless_unscaled))
            _x_values = _x_values[0::skip]
        for _ch in self.topographic_channels:
            _video_path = self.input_node.paths.figures_current_dir
            _sep = '_' if self.user_naming_rule is not None else ''
            _video_base_name = self.input_process.name + _sep + self.user_naming_rule
            rec = Recorder(video_path=_video_path + _video_base_name + '_' + _ch + '.mp4')
            for _x in tqdm(_x_values, desc='Generating Video for channel {:}'.format(_ch)):
                plt.ioff()
                figures = eegpt.plot_eeg_topographic_map(ave_data=data_node,
                                                         eeg_topographic_map_channels=[_ch],
                                                         save_figures=False,
                                                         times=_x,
                                                         domain=self.input_node.domain,
                                                         title=self.title,
                                                         x_lim=self.plot_x_lim,
                                                         y_lim=self.plot_y_lim,
                                                         fig_format=self.fig_format,
                                                         fontsize=self.fontsize,
                                                         return_figures=True)
                if figures is not None:
                    rec.add_frame(figures[0])
                    for _fig in figures:
                        plt.close(_fig)
                    gc.collect()
                # print_progress_bar(iteration=_i, total=x.size, prefix='Generating Video for channel {:}'.format(_ch))
            rec.end_recording()
