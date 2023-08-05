import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from peegy.processing.tools.detection.time_domain_tools import get_channel_peaks_and_windows
from peegy.definitions.eeg_definitions import EegChannel
from peegy.definitions.channel_definitions import Domain
import os
from peegy.plot.eeg_plot_tools import interpolate_potential_fields
import gc
import matplotlib.gridspec as gridspec
from scipy import signal
from operator import itemgetter
import pycwt as wavelet
import pywt as pw
from peegy.processing.pipe.definitions import DataNode
import astropy.units as u
from matplotlib.pyplot import cm
from astropy.visualization import quantity_support, time_support
from peegy.tools.units.unit_tools import set_default_unit
# from matplotlib.projections.polar import PolarAxes
# from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import warnings
warnings.filterwarnings("ignore", message="No contour levels were found within the data range.")
quantity_support()
time_support()


def get_potential_fields(epochs_ave: DataNode = DataNode(),
                         x_val: np.array = np.array([]),
                         domain: Domain = Domain.time,
                         **kwargs):
    x_val = np.atleast_1d(x_val)
    if domain == Domain.time:
        potentials = np.squeeze(epochs_ave.data[epochs_ave.x_to_samples(x_val), :])
    if domain == Domain.frequency:
        potentials = np.squeeze(np.abs(epochs_ave.data)[epochs_ave.x_to_samples(x_val), :])

    x = np.zeros((potentials.size, 1))
    y = np.zeros((potentials.size, 1))
    z = np.zeros((potentials.size, 1))
    for i, _ch in enumerate(epochs_ave.layout):
        if (_ch.x is not None and not np.isnan(_ch.x)) and (_ch.y is not None and not np.isnan(_ch.y)):
            x[i] = _ch.x
            y[i] = _ch.y
            z[i] = potentials[i]
    interpolated_potentials = None
    max_distance = None
    if x.any() and y.any() and z.any():
        interpolated_potentials, max_distance = interpolate_potential_fields(x, y, z, **kwargs)
    return interpolated_potentials, max_distance


def plot_single_channels(ave_data: [DataNode] = None,
                         channels: np.array([str]) = np.array([]),
                         figure_dir_path: str = None,
                         figure_basename: str = None,
                         fig_format: str = '.png',
                         statistical_test: str = None,
                         show_following_stats: [str] = None,
                         offset_step: u.quantity.Quantity = None,
                         save_to_file: bool = True,
                         title: str = '',
                         x_lim: [float, float] = None,
                         y_lim: [float, float] = None,
                         show_peaks: bool = True,
                         show_labels: bool = True,
                         fontsize=8):
    """
    :param ave_data: list of DataNode class containing data to plot
    :param figure_dir_path: directory path where figure will be saved
    :param figure_basename: output file name
    :param fig_format: output format of generated figure (.pdf, .png)
    :param statistical_test: name of the statistical test used to extract data
    :param show_following_stats: list of string indicating which parameters found in statistical_tests are shown
    :param channels: index or labels of channels to be plotted
    :param offset_step: constant to vertically separate each channel
    :param save_to_file: if True, figure will be saved into figure_dir_path
    :param title: desired figure title
    :param x_lim: plot x limits
    :param y_lim: plot x limits
    :param show_peaks: if True, detected peaks will be shown
    :param show_labels: if True, peak labels will be shown
    :param fontsize: fontsize of text in figures
    :return:
    """
    # plot individual channels
    font = {'size': 6}
    _fig_path = figure_dir_path + figure_basename + fig_format
    fig = plt.figure()
    inch = 2.54
    fig.set_size_inches(12 / inch, 8 / inch)
    plt.rc('font', **font)
    colors = cm.tab10.colors[0: len(ave_data)]
    # get list with all channels labels
    all_labels = np.array([_layout.label for _data in ave_data for _layout in _data.layout])
    _, _idx = np.unique(all_labels, return_index=True)
    all_labels = all_labels[np.sort(_idx)]
    if channels is not None:
        if isinstance(channels[0], str):
            all_labels = np.intersect1d(all_labels, channels)
            # ensure unique labels and remove repeated in same order
            _, idx_channels = np.unique(channels, return_index=True)
            channels = channels[np.sort(idx_channels)]
            idx = []
            for _label in channels:
                _idx = np.argwhere(_label == all_labels)
                if _idx.size:
                    idx.append(_idx.squeeze())
            idx = np.array(idx)
            all_labels = all_labels[idx]
        else:
            _aviable_channels = np.minimum(len(all_labels) - 1, channels)
            _, idx_channels = np.unique(_aviable_channels, return_index=True)
            _aviable_channels = _aviable_channels[np.sort(idx_channels)]
            all_labels = all_labels[_aviable_channels]
    n_ch_to_plot = len(all_labels)

    for _idx_data, (_ave_data, _color) in enumerate(zip(ave_data, colors)):
        my_stats_text = []
        my_color_text = []
        my_offset_text = []
        if channels is not None and channels.size and isinstance(channels[0], str):
            ch_idx = _ave_data.get_channel_idx_by_label(channels)
        else:
            ch_idx = channels if channels is not None else list(range(_ave_data.data.shape[1]))
            ch_idx = np.minimum(ch_idx, _ave_data.data.shape[1] - 1)
        _, idx = np.unique(ch_idx, return_index=True)
        ch_idx = ch_idx[np.sort(idx)]
        _channels = np.array([ch.label for ch in _ave_data.layout])[ch_idx]

        # initialize offset step based on first input and axis for polar plots
        if _idx_data == 0:
            if _ave_data.domain == Domain.frequency:
                gs = gridspec.GridSpec(n_ch_to_plot, 5)
                ax1 = plt.subplot(gs[::, 0:4])
                ax_in = [None] * n_ch_to_plot
                for _idx in range(n_ch_to_plot):
                    ax_in[_idx] = plt.subplot(gs[_idx, 4], projection='polar')
                    ax_in[_idx].tick_params(axis='x', which='both', bottom=False,
                                            top=False, labelbottom=False)
                    ax_in[_idx].tick_params(axis='y', which='both', right=False,
                                            left=False, labelleft=False)
                    # for pos in ['right', 'top', 'bottom', 'left']:
                    #     ax_in[_idx].spines[pos].set_visible(False)

            else:
                gs = gridspec.GridSpec(1, 1)
                ax1 = plt.subplot(gs[0])

            if offset_step is None:
                offset_step = np.max(np.max(np.abs(_ave_data.data[:, ch_idx]), axis=0))
        offset_vector = np.arange(n_ch_to_plot) * offset_step
        _offset_idx = np.argwhere(np.in1d(all_labels, _channels)).squeeze()
        all_peaks = None
        all_markers = _ave_data.markers
        rn_up, rn_down = None, None

        if _ave_data.domain == Domain.time:
            ave_w = _ave_data.data[:, ch_idx] - offset_vector[_offset_idx].reshape(1, -1)
            x_label = 'Time [{:}]'.format(_ave_data.x.unit)
            all_peaks = _ave_data.peak_times
            rn_up = _ave_data.rn[ch_idx] - offset_vector[_offset_idx].reshape(1, -1)
            rn_down = -_ave_data.rn[ch_idx] - offset_vector[_offset_idx].reshape(1, -1)
        if _ave_data.domain == Domain.frequency:
            ave_w = np.abs(_ave_data.data[:, ch_idx]) - offset_vector[_offset_idx].reshape(1, -1)
            x_label = 'Frequency [{:}]'.format(_ave_data.x.unit)
            all_peaks = _ave_data.peak_frequency

        if all_peaks is not None and all_peaks.shape[0]:
            _unique_peaks = all_peaks.peak_label.unique()
            peak_color = list(iter(cm.Set1(np.linspace(0, 1, _unique_peaks.size * (1 + len(ave_data))))))
        ax1.plot(_ave_data.x, ave_w, linewidth=0.5, color=_color)

        if rn_up is not None and rn_down is not None:
            [ax1.axhline(y=_rn, color=_color, linewidth=0.5) for _rn in rn_up.reshape(-1, 1)]
            [ax1.axhline(y=_rn, color=_color, linewidth=0.5) for _rn in rn_down.reshape(-1, 1)]

        # add detected peaks
        _max_peak_amp = -np.inf
        for i, _ch in enumerate(_channels):
            _current_offset = np.atleast_1d(offset_vector[_offset_idx])[i]
            if all_markers is not None:
                _subset = all_markers.query('channel == "{:}"'.format(_ch))
                for _idx, _m in _subset.iterrows():
                    ax1.add_patch(Rectangle((_m.x_ini, _m.y_ini - _current_offset),
                                            _m.x_end - _m.x_ini, _m.y_end - _m.y_ini,
                                            edgecolor='k'))
            if all_peaks is not None and all_peaks.shape[0] and \
                    not np.all(all_peaks.amp.apply(lambda x_value: np.isnan(x_value.value))):
                _idx_amps = all_peaks.amp.apply(lambda x_value: not np.isnan(x_value.value))
                all_peaks = all_peaks[_idx_amps]
                _max_peak_amp = np.maximum(all_peaks.amp, _max_peak_amp)
                _subset = all_peaks.query('channel == "{:}"'.format(_ch))
                for _idx, _peak in _subset.iterrows():
                    _peak_color = peak_color[np.argwhere(_unique_peaks == _peak.peak_label).squeeze() +
                                             _unique_peaks.size * _idx_data]
                    markerfacecolor = _peak_color if _peak.significant else 'white'
                    x = _peak.x
                    y = _peak.amp
                    if _peak.show_peak and show_peaks:
                        if _peak.positive:
                            ax1.plot(x, y - _current_offset, '^', markersize=3,
                                     markerfacecolor=markerfacecolor, color=_peak_color)
                        else:
                            ax1.plot(x, y - _current_offset, 'v', markersize=3,
                                     markerfacecolor=markerfacecolor, color=_peak_color)
                    if _peak.show_label and show_labels:
                        ax1.text(x, y * 1.1 - _current_offset, _peak.peak_label,
                                 horizontalalignment='center',
                                 verticalalignment='bottom')
                    if _ave_data.domain == Domain.frequency:
                        _pol_ax_idx = i
                        ax_in[_pol_ax_idx].plot(
                            _peak.spectral_phase,
                            y,
                            color=_peak_color,
                            marker='o',
                            linestyle=None,
                            markersize=2,
                            alpha=1,
                            label='')
                        _amp = _max_peak_amp.values[0]
                        ax_in[_pol_ax_idx].set_ylim(0 * _amp.unit, _amp * 1.1)
                        ax_in[_pol_ax_idx].set_yticklabels([])
                        ax_in[_pol_ax_idx].set_xticklabels([])
                        ax_in[_pol_ax_idx].grid(True)
                        ax_in[_pol_ax_idx].set_xlabel('')
                        ax_in[_pol_ax_idx].set_ylabel('')
                        ax_in[_pol_ax_idx].patch.set_alpha(1)

            if show_following_stats is not None:
                all_stats = None
                if statistical_test is not None:
                    if statistical_test in _ave_data.statistical_tests.keys():
                        all_stats = _ave_data.statistical_tests[statistical_test]
                    else:
                        print('Available statistical tests: {:}'.format(list(_ave_data.statistical_tests.keys())))
                        print('Could not find statistical test called {:}'.format(statistical_test))

                if all_stats is None:
                    continue
                columns_found = np.intersect1d(all_stats.columns, show_following_stats)
                if columns_found.size == 0:
                    print('Could not find columns: {:}'.format(show_following_stats))
                    continue
                # resort columns to keep input order
                _cols = []
                for _ss in show_following_stats:

                    if _ss in columns_found:
                        _cols.append(_ss)
                columns_found = _cols
                _subset = all_stats.query('channel == "{:}"'.format(_ch))
                _text_stats = ''
                for _idx, _test in _subset.iterrows():
                    for _col in columns_found:
                        _value = _test[_col]
                        if isinstance(_value, str):
                            _text_stats = _text_stats + '{:} '.format(_test[_col])
                        else:
                            _text_stats = _text_stats + '{:} = {:.3f} '.format(_col, _test[_col])
                    _text_stats = _text_stats + '\n'
                my_stats_text.append(_text_stats)
                my_color_text.append(_color)
                my_offset_text.append(_current_offset)
        if _ave_data.roi_windows is not None:
            for _roi in _ave_data.roi_windows:
                if _roi.show_window:
                    ax1.axvspan(_roi.ini_time, _roi.end_time, alpha=0.05, color=_color)
                if _roi.show_label:
                    _y_label = np.max(ax1.get_ylim())
                    ax1.text((_roi.end_time - _roi.ini_time) / 2,
                             _y_label, _roi.label,
                             horizontalalignment='center',
                             verticalalignment='bottom')
        if _idx_data == 0:
            if x_lim is None:
                x_lim = [0, _ave_data.x[-1].value]
            _x = np.min(x_lim)
            ax1.set_title(title, fontsize=fontsize)
            ax1.set_xlim(x_lim)
            if y_lim is not None:
                # ax1.set_ylim(-(n_ch_to_plot + 1) * offset_step, offset_step)
                # else:
                ax1.set_ylim(y_lim)
            y_unit = _ave_data.data.unit
            if y_unit == u.dimensionless_unscaled:
                y_unit = 'A.U.'
            ax1.set_xlabel(x_label,
                           fontsize=fontsize)
            ax1.set_ylabel('Amplitude [{:}]'.format(y_unit),
                           fontsize=fontsize)
            ax2 = ax1.twinx()
            ax2.set_ylim(ax1.get_ylim())
            ax2.set_yticks(-offset_vector)
            ax2.set_yticklabels([_ch for _ch in all_labels], fontsize=fontsize)
            ax2.spines["right"].set_position(("axes", - 0.25))

        text_width = 0

        for _t, _c, _o in zip(my_stats_text, my_color_text, my_offset_text):
            if my_stats_text != '':
                ax_text = ax1.text(_x, -_o, _t,
                                   horizontalalignment='left',
                                   verticalalignment='bottom',
                                   color=_c,
                                   fontsize=6)
                transf = ax1.transData.inverted()
                bb = ax_text.get_window_extent(renderer=fig.canvas.get_renderer())
                bb = bb.transformed(transf)
                text_width = np.maximum(text_width, (bb.xmax - bb.xmin) * 1.1)
        _x = _x + text_width

    fig.tight_layout()
    if save_to_file:
        fig.savefig(_fig_path)
        print('time plots saved figure: {:}'.format(_fig_path))
    return fig


def plot_time_peak_topographic_map(ave_data=DataNode(),
                                   file_name='',
                                   title='',
                                   channel_label=[],
                                   x_lim=None,
                                   y_lim=None,
                                   fontsize=8):
    if x_lim is None:
        x_lim = [ave_data.x[0], ave_data.x[-1]]
    grid_size = 500j
    peak_scalp_potentials = []

    _ch_idx = [_i for _i, _ch in enumerate(ave_data.layout) if _ch.x is not None and _ch.y is not None]
    assigned_channels = ave_data.layout[_ch_idx]

    if not channel_label:
        channel_label = assigned_channels[0].label

    dummy_var = np.array([_i for _i, _ch in enumerate(assigned_channels) if _ch.label == channel_label])
    if not len(dummy_var):
        return
    idx_ch = ave_data.get_channel_idx_by_label([channel_label])

    # check if channels has maximum snr to add in title
    max_snr_idx = np.argmax(ave_data.get_max_snr_per_channel()[_ch_idx])
    if idx_ch == max_snr_idx:
        title += ' best snr'
    # filter peaks for specific channel
    _peaks, _time_windows = get_channel_peaks_and_windows(eeg_peaks=ave_data.peak_times,
                                                          eeg_time_windows=ave_data.peak_time_windows,
                                                          channel_label=channel_label)
    sorted_peaks = None
    _y_max = None
    _y_min = None
    if _peaks:
        # sort peaks by time
        _s_p = itemgetter(*np.argsort([_p.x for _p in _peaks]))(_peaks)
        sorted_peaks = _s_p if isinstance(_s_p, tuple) else (_s_p,)

        max_amps = [_p.amp for _p in ave_data.peak_times if _p.peak_label]
        if max_amps:
            _y_max = np.max(max_amps)
            _y_min = np.min([_p.amp for _p in ave_data.peak_times if _p.peak_label])

        # compute topographic map
        for _peak in sorted_peaks:
            if _peak.peak_label:
                peak_potentials, max_distance = get_potential_fields(epochs_ave=ave_data,
                                                                     x_val=_peak.x,
                                                                     grid=grid_size,
                                                                     domain=_peak.domain)
                # print _peak.peak_label
                # get_CDF(epochs_ave=ave_data,
                #         x_val=_peak.x,
                #         grid=grid_size,
                #         domain=_peak.domain)
                peak_scalp_potentials.append({'potential': peak_potentials,
                                              'peak': _peak.peak_label})

    # plot topographic map
    inch = 2.54
    fig = plt.figure()
    fig.set_size_inches(18 / inch, 12 / inch)

    row_idx = 0
    gs = gridspec.GridSpec(2, len(peak_scalp_potentials)) if peak_scalp_potentials else gridspec.GridSpec(1, 1)
    if peak_scalp_potentials:
        row_idx += 1
        for _idx, peak_field in enumerate(peak_scalp_potentials):
            ax = plt.subplot(gs[0, _idx])
            ax_im = ax.imshow(peak_field['potential'].T, origin='lower',
                              extent=(-max_distance, max_distance, -max_distance, max_distance),
                              vmin=_y_min,
                              vmax=_y_max,
                              aspect=1.0)
            ax_im.set_cmap('nipy_spectral')
            levels = np.arange(_y_min, _y_max, (_y_max - _y_min) / 5.0)
            ax.contour(peak_field['potential'].T,
                       levels,
                       origin='lower',
                       extent=(-max_distance, max_distance, -max_distance, max_distance),
                       linewidths=1.0,
                       colors='k')
            ax.autoscale(enable=False)
            ax.plot(0, max_distance * 1.0, '|', markersize=5, color='k')
            for i, _ch in enumerate(ave_data.layout):
                if not (_ch.x is None or _ch.y is None):
                    ax.plot(_ch.x, _ch.y, 'o', color='b', markersize=0.2)
            ax.get_xaxis().set_ticks([])
            ax.get_yaxis().set_ticks([])
            ax.axis('off')
            ax.set_title(peak_field['peak'])

        c_bar_ax = fig.add_axes([0.05, 0.6, 0.01, 0.25])
        fig.colorbar(ax_im, cax=c_bar_ax, orientation='vertical', format='%.1f')
        c_bar_ax.yaxis.set_ticks_position('left')

    ax2 = plt.subplot(gs[row_idx, 0:])
    ax2.plot(ave_data.x, ave_data.data[:, idx_ch])
    ax2.axhline(y=ave_data.rn[idx_ch], color='k', linewidth=0.3)
    ax2.axhline(y=-ave_data.rn[idx_ch], color='k', linewidth=0.3)
    if sorted_peaks is not None:
        for _idx, _peak in enumerate(sorted_peaks):
            if _peak.peak_label and _peak.show_label:
                markerfacecolor = 'black' if _peak.significant else 'white'
                if _peak.positive:
                    ax2.plot(_peak.x, _peak.amp, '^', markersize=3, markerfacecolor=markerfacecolor)
                else:
                    ax2.plot(_peak.x, _peak.amp, 'v', markersize=3, markerfacecolor=markerfacecolor)
                ax2.text(_peak.x, _peak.amp * 1.1, _peak.peak_label, horizontalalignment='center',
                         verticalalignment='bottom')
    ax2.set_xlabel('Time [{:}]'.format(ave_data.x.unit), fontsize=fontsize)
    ax2.set_xlim(x_lim)
    ax2.set_ylabel('Amplitude [{:}]'.format(ave_data.data.unit), fontsize=fontsize)
    if _y_max and _y_min and y_lim is None:
        ax2.set_ylim([_y_min * 1.2, (_y_max + (_y_max - _y_min) / 10.0) * 1.2])
    elif y_lim is not None:
        ax2.set_ylim(y_lim)
    ax2.set_title(title, fontsize=fontsize)
    if _time_windows:
        [ax2.axvspan(_t_w.ini_time, _t_w.end_time, alpha=0.15, color='r')
         for _t_w in _time_windows if _t_w.positive_peak and _t_w.show_window]
        [ax2.axvspan(_t_w.ini_time, _t_w.end_time, alpha=0.15, color='b')
         for _t_w in _time_windows if not _t_w.positive_peak and _t_w.show_window]
    plt.tight_layout()
    fig.savefig(file_name)
    plt.close(fig)
    gc.collect()
    print(('figure saved: ' + file_name))


def plot_time_topographic_map(ave_data=DataNode(),
                              title: str = '',
                              times: u.Quantity = np.array([]),
                              channel_label: [str] = None,
                              x_lim: [float, float] = None,
                              y_lim: [float, float] = None,
                              fontsize: float = 8):
    if x_lim is None:
        x_lim = [ave_data.x[0], ave_data.x[-1]]
    grid_size = 500j
    peak_scalp_potentials = []
    times = set_default_unit(times, u.s)
    # _ch_idx = [_i for _i, _ch in enumerate(ave_data.layout) if _ch.x is not None and _ch.y is not None]
    # assigned_channels = ave_data.layout[_ch_idx]
    # if channel_label is None:
    #     channel_label = assigned_channels[0].label
    #
    # dummy_var = np.array([_i for _i, _ch in enumerate(assigned_channels) if _ch.label == channel_label])
    # if not len(dummy_var):
    #     return
    idx_ch = ave_data.get_channel_idx_by_label([channel_label])
    if not idx_ch.size:
        return

    # check if channels has maximum snr to add in title
    # max_snr_idx = np.argmax(ave_data.get_max_snr_per_channel()[_ch_idx])
    # if idx_ch == max_snr_idx:
    #     title += ' best snr'

    _y_max = None
    _y_min = None
    _time_labels = np.array([''] * times.size)
    _show_labels = np.array([True] * times.size)
    if ave_data.peak_times is not None and ave_data.peak_times.shape[0]:
        _subset = ave_data.peak_times.query('channel == "{:}"'.format(channel_label))
        _subset = _subset.reset_index(drop=True)
        if _subset.shape[0]:
            # sort peaks by time
            _time_points = ave_data.x_to_samples(_subset['x'])
            _original_idx = np.argsort(_time_points)
            _peak_labels = _subset['peak_label'][_original_idx]
            _show = _subset['show_label'][_original_idx]
            times = np.append(times, ave_data.x[_time_points[_original_idx]])
            _time_labels = np.append(_time_labels, _peak_labels)
            _show_labels = np.append(_show_labels, _show)

    if times.size:
        amps = ave_data.data[ave_data.x_to_samples(times), :]
        _y_max = np.nanmax(amps)
        _y_min = np.nanmin(amps)

        # compute topographic map
        max_distance = None
        for _idx_t, _t in enumerate(times):
            peak_potentials, max_distance = get_potential_fields(epochs_ave=ave_data,
                                                                 x_val=_t,
                                                                 grid=grid_size,
                                                                 domain=ave_data.domain)
            if peak_potentials is None or not peak_potentials.size:
                continue
            _label = _time_labels[_idx_t] if _show_labels[_idx_t] else ''
            peak_scalp_potentials.append({'potential': peak_potentials,
                                          'peak': '{:} {:.2e}'.format(_label, _t)}
                                         )

        if len(peak_scalp_potentials) == 0:
            return
        # plot topographic map
        inch = 2.54
        fig = plt.figure()
        fig.set_size_inches(18 / inch, 12 / inch)

        row_idx = 0
        gs = gridspec.GridSpec(2, len(peak_scalp_potentials)) if peak_scalp_potentials else gridspec.GridSpec(1, 1)
        if peak_scalp_potentials:
            row_idx += 1
            for _idx, peak_field in enumerate(peak_scalp_potentials):
                ax = plt.subplot(gs[0, _idx])
                ax_im = ax.imshow(peak_field['potential'].T, origin='lower',
                                  extent=(-max_distance, max_distance, -max_distance, max_distance),
                                  vmin=_y_min.value,
                                  vmax=_y_max.value,
                                  aspect=1.0)
                ax_im.set_cmap('nipy_spectral')
                levels = np.arange(_y_min.value, _y_max.value, (_y_max.value - _y_min.value) / 5.0)
                ax.contour(peak_field['potential'].T,
                           levels,
                           origin='lower',
                           extent=(-max_distance, max_distance, -max_distance, max_distance),
                           linewidths=1.0,
                           colors='k')
                ax.autoscale(enable=False)
                ax.plot(0, max_distance * 1.0, '|', markersize=5, color='k')
                for i, _ch in enumerate(ave_data.layout):
                    if not (_ch.x is None or _ch.y is None):
                        ax.plot(_ch.x, _ch.y, 'o', color='b', markersize=0.2)
                ax.get_xaxis().set_ticks([])
                ax.get_yaxis().set_ticks([])
                ax.axis('off')
                ax.set_title(peak_field['peak'])

            c_bar_ax = fig.add_axes([0.05, 0.6, 0.01, 0.25])
            fig.colorbar(ax_im, cax=c_bar_ax, orientation='vertical', format='%.1f')
            c_bar_ax.yaxis.set_ticks_position('left')

        ax2 = plt.subplot(gs[row_idx, 0:])
        ax2.plot(ave_data.x, ave_data.data[:, idx_ch])
        ax2.axhline(y=ave_data.rn[idx_ch].to_value(ave_data.data.unit), color='k', linewidth=0.3)
        ax2.axhline(y=-ave_data.rn[idx_ch].to_value(ave_data.data.unit), color='k', linewidth=0.3)
        for _t in times:
            ax2.axvline(_t)
        ax2.set_xlabel('Time [{:}]'.format(ave_data.x.unit), fontsize=fontsize)
        ax2.set_xlim(x_lim)
        ax2.set_xticks(np.linspace(0, max(x_lim), num=10))  # sets xticks
        _unit = ave_data.data.unit
        if _unit == u.dimensionless_unscaled:
            _unit = 'A.U.'
        ax2.set_ylabel('Amplitude [{:}]'.format(_unit), fontsize=fontsize)
        if _y_max is not None and _y_min is not None and y_lim is None:
            ax2.set_ylim([_y_min * 1.2, (_y_max + (_y_max - _y_min) / 10.0) * 1.2])
        elif y_lim is not None:
            ax2.set_ylim(y_lim)
        ax2.set_title(title, fontsize=fontsize)
        return fig


def plot_freq_topographic_map(ave_data=DataNode(),
                              title='',
                              channel_label: [str] = None,
                              x_lim=None,
                              y_lim=None,
                              fontsize=8.0):
    plt.ioff()
    if x_lim is None:
        x_lim = [0, ave_data.x[-1].value]
    grid_size = 150j
    peak_scalp_potentials = []

    idx_ch = ave_data.get_channel_idx_by_label([channel_label])
    if idx_ch.size == 0:
        return
    _peaks, _ = get_channel_peaks_and_windows(eeg_peaks=ave_data.peak_frequency, channel_label=channel_label)

    sorted_peaks = None
    _y_max = None
    max_distance = None
    if _peaks.size:
        # sort peaks by frequency
        sorted_peaks = _peaks.sort_values('x')

        _y_max = ave_data.peak_frequency['amp'].max()

        # compute topographic map
        for _, _peak in sorted_peaks.iterrows():
            if _peak.peak_label:
                peak_potentials, max_distance = get_potential_fields(epochs_ave=ave_data,
                                                                     x_val=_peak.x,
                                                                     grid=grid_size,
                                                                     domain=_peak.domain)
                if peak_potentials is not None:
                    peak_scalp_potentials.append({'potential': peak_potentials,
                                                  'peak': _peak.peak_label})

    # plot topographic map
    inch = 2.54
    fig = plt.figure()
    fig.set_size_inches(18 / inch, 12 / inch)
    row_idx = 0
    gs = gridspec.GridSpec(2, len(peak_scalp_potentials)) if peak_scalp_potentials else gridspec.GridSpec(1, 1)

    if peak_scalp_potentials:
        row_idx += 1
        for _idx, peak_field in enumerate(peak_scalp_potentials):
            ax = plt.subplot(gs[0, _idx])
            ax_im = ax.imshow(peak_field['potential'].T, origin='lower',
                              extent=(-max_distance, max_distance, -max_distance, max_distance),
                              vmin=0,
                              vmax=_y_max.value,
                              aspect=1.0)
            ax_im.set_cmap('nipy_spectral')
            levels = np.arange(0, 5) * _y_max / 4
            ax.contour(peak_field['potential'].T,
                       levels,
                       origin='lower',
                       extent=(-max_distance, max_distance, -max_distance, max_distance),
                       linewidths=1.0,
                       colors='k')
            ax.autoscale(enable=False)
            ax.plot(0, max_distance * 1.0, '|', markersize=5, color='k')
            for i, _ch in enumerate(ave_data.layout):
                if not (_ch.x is None or _ch.y is None):
                    ax.plot(_ch.x, _ch.y, 'o', color='b', markersize=0.2)
            ax.get_xaxis().set_ticks([])
            ax.get_yaxis().set_ticks([])
            ax.axis('off')
            ax.set_title(peak_field['peak'])

        c_bar_ax = fig.add_axes([0.05, 0.6, 0.01, 0.25])
        fig.colorbar(ax_im, cax=c_bar_ax, orientation='vertical', format='%.1f')
        c_bar_ax.yaxis.set_ticks_position('left')

    # plot waveform of channel used
    ax2 = plt.subplot(gs[row_idx, 0:])
    ax2.plot(ave_data.x, np.abs(ave_data.data[:, idx_ch]))
    ax2.set_xlim(x_lim)
    if sorted_peaks is not None:
        for _idx, _peak in sorted_peaks.iterrows():
            if _peak.show_label:
                markerfacecolor = 'black' if _peak.significant else 'white'
                if _peak.positive:
                    ax2.plot(_peak.x,
                             _peak.amp,
                             'v',
                             markersize=3,
                             markerfacecolor=markerfacecolor)
                else:
                    ax2.plot(_peak.x,
                             _peak.amp,
                             '^',
                             markersize=3,
                             markerfacecolor=markerfacecolor)
                if _peak.peak_label:
                    ax2.text(_peak.x,
                             _peak.amp + 0.1 * _peak.amp.unit,
                             _peak.peak_label,
                             horizontalalignment='center',
                             verticalalignment='bottom',
                             fontsize=fontsize)
    ax2.set_xlabel('Frequency [{:}]'.format(u.Hz),
                   fontsize=fontsize)
    _unit = ave_data.data.unit
    if _unit == u.dimensionless_unscaled:
        _unit = 'A.U.'
    ax2.set_ylabel('Amplitude [{:}]'.format(_unit), fontsize=fontsize)

    if _y_max is not None and y_lim is None:
        ax2.set_ylim([0 * _y_max.unit, _y_max * 1.2])
    elif y_lim is not None:
        ax2.set_ylim(y_lim)
    ax2.set_title(title, fontsize=fontsize)
    return fig


def plot_eeg_time_frequency_transformation(ave_data: DataNode = DataNode(),
                                           figure_dir_path='',
                                           figure_basename='',
                                           eeg_topographic_map_channels=np.array([]),
                                           title='',
                                           x_lim=None,
                                           y_lim=None,
                                           fig_format='.pdf',
                                           fontsize=8,
                                           **kwargs):
    if eeg_topographic_map_channels.size:
        topographic_map_channels = eeg_topographic_map_channels
    else:
        topographic_map_channels = [_ch.label for _ch in ave_data.layout]

    for _label in topographic_map_channels:
        _fig_path = figure_dir_path + '_' + _label + '_' + figure_basename + '_spectrogram_' + fig_format
        plot_time_frequency_transformation(ave_data=ave_data,
                                           channel_label=_label,
                                           file_name=_fig_path,
                                           title=_label + ' / ' + title,
                                           x_lim=x_lim,
                                           y_lim=y_lim,
                                           fontsize=fontsize,
                                           **kwargs)


def plot_time_frequency_transformation(ave_data: DataNode = DataNode(),
                                       file_name='',
                                       title='',
                                       channel_label: [str] = None,
                                       x_lim=None,
                                       y_lim=None,
                                       fontsize=8,
                                       **kwargs):
    method = kwargs.get('method', 'spectrogram')
    time_window = kwargs.get('time_window', 2.0)
    sample_interval = kwargs.get('sample_interval', 2.0)
    # nperseg = kwargs.get('nperseg', 256)
    # noverlap = kwargs.get('noverlap', 128)
    # nfft = nfft if nperseg < nfft else nperseg
    spec_thresh = kwargs.get('spec_thresh', 4)
    nfft = int(time_window * ave_data.fs)
    noverlap = max(nfft - int(sample_interval * ave_data.fs), 0)

    if x_lim is None:
        x_lim = [0, ave_data.x[-1]]

    _ch_idx = [_i for _i, _ch in enumerate(ave_data.layout) if _ch.x is not None and _ch.y is not None]
    assigned_channels = ave_data.layout[_ch_idx]

    if channel_label is None:
        channel_label = assigned_channels[0].label

    dummy_var = np.array([_i for _i, _ch in enumerate(assigned_channels) if _ch.label == channel_label])
    if not len(dummy_var):
        return
    idx_ch = ave_data.get_channel_idx_by_label([channel_label])

    if not len(idx_ch):
        return
    # check if channels has maximum snr to add in title
    # check if channels has maximum snr to add in title
    max_snr_idx = np.argmax(ave_data.get_max_snr_per_channel()[_ch_idx])
    if idx_ch == max_snr_idx:
        title += ' best snr'

    # plot topographic map
    inch = 2.54
    fig = plt.figure()
    fig.set_size_inches(1 / inch, 12 / inch)

    row_idx = 0
    gs = gridspec.GridSpec(1, 1)
    ax2 = plt.subplot(gs[row_idx, 0:])
    if method == 'spectrogram':
        freqs, time, power = signal.spectrogram(np.squeeze(ave_data.data[:, idx_ch]),
                                                window=signal.hamming(nfft),
                                                fs=ave_data.fs,
                                                nfft=nfft,
                                                noverlap=noverlap,
                                                mode='magnitude',
                                                scaling='spectrum')
        power /= power.max()
        power = 10 * np.log10(power)
        power[power < -spec_thresh] = -spec_thresh
    if method == 'wavelet':
        freq = np.arange(1, ave_data.data.shape[0] + 1) * ave_data.fs / ave_data.data.shape[0]
        # mother = wavelet.Morlet(f0=2 * np.pi)
        # s0 = 2 / ave_data.fs  # Starting scale
        # dj = 1 / 12.  # Twelve sub-octaves per octaves
        # J = 7 / dj  # Seven powers of two with dj sub-octaves
        [cfs, freqs] = pw.cwt(np.squeeze(ave_data.data[:, idx_ch]),
                              scales=np.arange(1, 128),
                              wavelet='cmor',
                              sampling_period=1 / ave_data.fs)

        w = pw.ContinuousWavelet('cmor')
        w.bandwidth_frequency = 1.5
        w.center_frequency = 1
        [cfs, freqs] = pw.cwt(np.squeeze(ave_data.data[:, idx_ch]),
                              scales=np.arange(1, ave_data.data.shape[0] / 2),
                              wavelet=w,
                              sampling_period=1 / ave_data.fs)
        wave, scales, freqs, coi, fft, fftfreqs = wavelet.cwt(np.squeeze(ave_data.data[:, idx_ch]),
                                                              dt=1 / ave_data.fs,
                                                              freqs=freq)
        # power = (np.abs(wave)) ** 2
        # fft_power = np.abs(fft) ** 2
        # period = 1 / freqs
        power = np.abs(cfs)
        time = np.arange(0, power.shape[1]) * 1 / ave_data.fs

    cax = ax2.pcolormesh(time, freqs, power, cmap=plt.get_cmap('viridis'))
    ax2.set_ylabel('Frequency [{:}]'.format(u.Hz))
    ax2.set_xlabel('Time [{:}]'.format(ave_data.x.unit), fontsize=fontsize)
    ax2.set_xlim(x_lim)
    if y_lim is not None:
        ax2.set_ylim(y_lim)
    ax2.set_title(title, fontsize=fontsize)
    a_pos = ax2.get_position()
    cbaxes = fig.add_axes([a_pos.x1 + 0.005, a_pos.y0, 0.005, a_pos.height])
    fig.colorbar(cax, cax=cbaxes)
    fig.savefig(file_name)
    plt.close(fig)
    gc.collect()
    print(('figure saved: ' + file_name))


def plot_eeg_time_frequency_power(ave_data: DataNode = DataNode(),
                                  figure_dir_path='',
                                  figure_basename='',
                                  eeg_topographic_map_channels=np.array([]),
                                  title='',
                                  x_lim=None,
                                  y_lim=None,
                                  fig_format='.pdf',
                                  fontsize=8,
                                  **kwargs):
    if eeg_topographic_map_channels.size:
        topographic_map_channels = eeg_topographic_map_channels
    else:
        topographic_map_channels = [_ch.label for _ch in ave_data.layout]

    for _label in topographic_map_channels:
        _fig_path = figure_dir_path + '_' + _label + '_' + figure_basename + '_power_spectrogram_.' + fig_format
        plot_time_frequency_power_transformation(ave_data=ave_data,
                                                 channel_label=_label,
                                                 file_name=_fig_path,
                                                 title=_label + ' / ' + title,
                                                 x_lim=x_lim,
                                                 y_lim=y_lim,
                                                 fontsize=fontsize,
                                                 **kwargs)


def plot_time_frequency_power_transformation(ave_data: DataNode = DataNode(),
                                             time: np.array = np.array([]),
                                             frequency: np.array = np.array([]),
                                             file_name='',
                                             title='',
                                             channel_label: [str] = None,
                                             x_lim=None,
                                             y_lim=None,
                                             fontsize=8,
                                             **kwargs):
    spec_thresh = kwargs.get('spec_thresh', 4)

    if x_lim is None:
        x_lim = [0, time[-1]]

    _ch_idx = [_i for _i, _ch in enumerate(ave_data.layout) if _ch.x is not None and _ch.y is not None]
    assigned_channels = ave_data.layout[_ch_idx]

    if channel_label is None:
        channel_label = assigned_channels[0].label

    dummy_var = np.array([_i for _i, _ch in enumerate(assigned_channels) if _ch.label == channel_label])
    if not len(dummy_var):
        return
    idx_ch = ave_data.get_channel_idx_by_label([channel_label])

    if not len(idx_ch):
        return

    # plot topographic map
    inch = 2.54
    fig = plt.figure()
    fig.set_size_inches(18 / inch, 12 / inch)

    row_idx = 0
    gs = gridspec.GridSpec(1, 1)
    ax2 = plt.subplot(gs[row_idx, 0:])

    power = np.squeeze(np.abs(ave_data.data[:, idx_ch, :]))
    power /= power.max()
    power = 10 * np.log10(power)
    power[power < -spec_thresh] = -spec_thresh
    cax = ax2.pcolormesh(time, frequency, power, cmap=plt.get_cmap('viridis'))
    ax2.set_ylabel('Frequency [{:}]'.format(u.Hz))
    ax2.set_xlabel('Time [{:}]'.format(ave_data.x.unit), fontsize=fontsize)
    ax2.set_xlim(x_lim)
    if y_lim is not None:
        ax2.set_ylim(y_lim)
    ax2.set_title(title, fontsize=fontsize)
    a_pos = ax2.get_position()
    cbaxes = fig.add_axes([a_pos.x1 + 0.005, a_pos.y0, 0.005, a_pos.height])
    fig.colorbar(cax, cax=cbaxes)

    # plt.tight_layout()
    fig.savefig(file_name)
    plt.close(fig)
    gc.collect()
    print(('figure saved: ' + file_name))


def plot_eeg_topographic_map(ave_data: DataNode = DataNode(),
                             figure_dir_path: str = '',
                             figure_basename: str = '',
                             return_figures: bool = False,
                             eeg_topographic_map_channels: np.array = np.array([]),
                             domain: Domain = Domain.time,
                             save_figures: bool = True,
                             times: np.array = None,
                             title: str = '',
                             x_lim: [] = None,
                             y_lim: [] = None,
                             fig_format: str = '.pdf',
                             fontsize: float = 8) -> [plt.figure]:
    """
    This function produces a matplotlib figure with the topographic map of the input DataNode.
    :param ave_data: DataNode containing the data to be plotted (times x channels)
    :param figure_dir_path: path where figures will be saved
    :param figure_basename: this is the base file name to save figures. Since the output will consist of several
    figures (one per channel), the channel label will be appended to the figure_basename
    :param return_figures: if True, the matplotlib figure will be returned
    :param eeg_topographic_map_channels: A list of strings with the labels of the channels to will be plotted. If left
    empty, all channels will be plotted.
    :param domain: the domain of the topographic map (Domain.time or Domain.frequency)
    :param save_figures: if True, figures will be saved on the figure_dir_path
    :param times: numpy array with times that will be used to generate the respective topographic maps.
    :param title: string with the title of the figure
    :param x_lim: numerical list with the range of the x-axis (min and max).
    :param y_lim: numerical list with the range of the y-axis (min and max).
    :param fig_format: the desired format of the saved figures (e.g. '.png', '.pdf')
    :param fontsize: float indicating the font size (in points) used to render text in the figure
    :return: list of figures
    """
    times = set_default_unit(times, u.s)
    if times is not None and times.ndim == 0:
        times = np.array([times.to_value()]) * times.unit
    eeg_topographic_map_channels = np.array(eeg_topographic_map_channels)
    figures = []
    if eeg_topographic_map_channels.size:
        topographic_map_channels = eeg_topographic_map_channels
    else:
        topographic_map_channels = [_ch.label for _ch in ave_data.layout]

    for _label in topographic_map_channels:
        _title = _label if title == '' else _label + ' / ' + title
        if domain == Domain.time:
            _fig_path = figure_dir_path + os.sep + _label + '_' + figure_basename + '_TMap' + fig_format
            fig = plot_time_topographic_map(ave_data=ave_data,
                                            channel_label=_label,
                                            times=times,
                                            title=_title,
                                            x_lim=x_lim,
                                            y_lim=y_lim,
                                            fontsize=fontsize)
            if fig is not None and save_figures:
                fig.savefig(_fig_path)
                print('figure saved: {:}'.format(_fig_path))
            if not return_figures:
                plt.close(fig)
                gc.collect()
            else:
                figures.append(fig)
        if domain == Domain.frequency:
            _fig_path = figure_dir_path + os.sep + _label + '_' + figure_basename + '_TMap_freq' + fig_format
            fig = plot_freq_topographic_map(ave_data=ave_data,
                                            channel_label=_label,
                                            title=_title,
                                            x_lim=x_lim,
                                            y_lim=y_lim,
                                            fontsize=fontsize)
            if fig is not None and save_figures:
                fig.savefig(_fig_path)
                print('figure saved: {:}'.format(_fig_path))
            if not return_figures:
                plt.close(fig)
                gc.collect()
            else:
                figures.append(fig)
    return figures


def eeg_save_time_slice(data: np.array = np.array([]),
                        fs: np.float = 0,
                        channels: np.array([EegChannel]) = np.array([EegChannel()]),
                        time_length: np.float = 4.0,
                        title: str = '',
                        file_name: str = ''):
    buffer_size = np.floor(np.minimum(time_length * fs, data.shape[0])).astype(np.int)
    fig, ax1 = plt.subplots()
    font = {'size': 6}
    plt.rc('font', **font)
    offset_vector = 10 * np.arange(data.shape[1])
    ax1.plot(np.arange(buffer_size) / fs, data[np.arange(buffer_size), :] - offset_vector,
             linewidth=0.5)
    # if interpolate_data:
    #     ax1.plot(interpolation_data_points['ini'],
    #              np.ones((interpolation_data_points['ini'].shape[0], data.shape[1]))
    #              + np.mean(data[np.arange(buffer_size), :], axis=0) - offset_vector,
    #              marker='v',
    #              linestyle='None',
    #              markerfacecolor='black',
    #              markersize=1.0)
    #
    #     ax1.plot(interpolation_data_points['end'],
    #              np.ones((interpolation_data_points['end'].shape[0], data.shape[1]))
    #              + np.mean(data[np.arange(buffer_size), :], axis=0) - offset_vector,
    #              marker='^',
    #              linestyle='None',
    #              markerfacecolor='black',
    #              markersize=1.0)
    ax1.set_title(title)
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Amplitude [' + r'$\mu$' + 'V]')
    ax2 = ax1.twinx()
    ax2.set_ylim(ax1.get_ylim())
    ax2.set_yticks(np.mean(data[np.arange(buffer_size), :] - offset_vector, axis=0))
    ax2.set_yticklabels([ch.label for i, ch in enumerate(channels)])
    ax2.spines["right"].set_position(("axes", - 0.1))
    fig.savefig(file_name)
    plt.close(fig)
    gc.collect()


def get_cdf(epochs_ave: DataNode = DataNode(),
            x_val: np.float = None,
            domain=Domain.time,
            **kwargs):
    idx_elec = np.where(np.array([ch.x for ch in epochs_ave.channels]))[0]
    # remove electrodes without a label
    if domain == Domain.time:
        potentials = epochs_ave.data[epochs_ave.time_to_samples(x_val), idx_elec]
    if domain == Domain.frequency:
        potentials = epochs_ave.rfft_average[epochs_ave.frequency_to_samples(x_val), idx_elec]

    x = np.zeros((potentials.size, 1))
    y = np.zeros((potentials.size, 1))
    z = np.zeros((potentials.size, 1))
    elec_pos = np.zeros((potentials.size, 2))
    _channels = np.array(epochs_ave.channels)[idx_elec]
    for i, _ch in enumerate(_channels):
        if _ch.x is not None and _ch.y is not None:
            x[i] = _ch.x
            y[i] = _ch.y
            z[i] = potentials[i]
            elec_pos[i] = np.array([_ch.x, _ch.y])
    # params = {'gdX': 0.05,
    #           'gdY': 0.05,
    #           'gdZ': 0.05,
    #           'n_sources': 64
    #           }
    # elec_pos = get_3D_spherical_positions(x, y)

    # params = {'gdX': 0.05,
    #           'gdY': 0.05,
    #           'n_sources': 64
    #           }

    # k = KCSD(elec_pos, z, params)
    #
    # k.estimate_pots()
    # k.estimate_csd()

    # k.plot_all()
    return interpolate_potential_fields(x, y, z, **kwargs)
