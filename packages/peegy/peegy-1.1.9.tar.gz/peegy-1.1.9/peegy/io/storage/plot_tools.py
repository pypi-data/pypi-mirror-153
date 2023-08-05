import copy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.gridspec as gridspec
from peegy.layouts.layouts import Layout
from peegy.plot import eeg_plot_tools as eegpt
from matplotlib import ticker

__author__ = 'jundurraga'


def plot_time_frequency_responses(dataframe: pd.DataFrame = None,
                                  rows_by: str = None,
                                  cols_by: str = None,
                                  sub_average_time_buffer_size: int = None,
                                  time_xlim: [float, float] = None,
                                  time_ylim: [float, float] = None,
                                  freq_xlim: [float, float] = None,
                                  freq_ylim: [float, float] = None,
                                  time_vmarkers: np.array = None,
                                  freq_vmarkers: np.array = None,
                                  title_by: str = 'row',
                                  title_v_offset: float = 0.0
                                  ) -> plt.figure:
    """
    This function will plot the waveforms contained in a pandas dataframe read using the sqlite_waveforms_to_pandas
    function of pEEGy.
    The rows and columns of the output plot are specified by the factors of the dataframe.
    The output will show the data for each of those factors (both individual and average data).
    :param dataframe: a pandas dataframe returned by sqlite_waveforms_to_pandas function of pEEGy.
    :param rows_by: name of the factor in the dataframe for which the rows in the plot will be split.
    :param cols_by: name of the factor in the dataframe for which the columns in the plot will be split.
    :param sub_average_time_buffer_size: This is a parameter used to sub_average time_domain data. For example, if each
    of your data have 10000 points, and you want to show the average having a length of 1000 samples, you could specify
    sub_average_time_buffer_size = 1000. This will averaged the 10000 points by splitting the data into blocks of 1000
    sampels.
    :param time_xlim: x axis limis for the time-domain panels
    :param time_ylim: y axis limis for the time-domain panels
    :param freq_xlim: x axis limis for the frequency-domain panels
    :param freq_ylim: y axis limis for the frequency-domain panels
    :param time_vmarkers: array with x values to add a vertical marker in the time-domain panels
    :param freq_vmarkers: array with x values to add a vertical marker in the frequency-domain panels
    :param title_by: string specifying from which factor you want to show the titles in each panel. This can be: "row",
    "col", or "both"
    :param title_v_offset: float specifying the vertical offset of the title
    :return:
    """
    df = copy.copy(dataframe)
    _rows_and_cols = []
    n_rows = 1
    n_cols = 1
    row_conditions = np.array([1])
    col_conditions = np.array([1])
    if rows_by is not None:
        _rows_and_cols.append(rows_by)
        row_conditions = df[rows_by].astype("category").cat.categories
        n_rows = row_conditions.size
    else:
        df.loc[:, 'dummy_row'] = 1
        _rows_and_cols.append('dummy_row')
        n_rows = 1
    idx_rows = np.arange(row_conditions.size)

    if cols_by is not None:
        _rows_and_cols.append(cols_by)
        col_conditions = df[cols_by].astype("category").cat.categories
        n_cols = col_conditions.size
    else:
        df.loc[:, 'dummy_col'] = 1
        _rows_and_cols.append('dummy_col')
        n_cols = 1
    idx_cols = np.arange(col_conditions.size)

    groups = df.groupby(_rows_and_cols)
    fig_out, ax = plt.subplots(n_rows, n_cols)
    gs = gridspec.GridSpec(n_rows, n_cols)
    for _id, ((_current_row_group, _current_col_group), _group) in enumerate(groups):
        _idx_row = idx_rows[_current_row_group == row_conditions].squeeze()
        _idx_col = idx_cols[_current_col_group == col_conditions].squeeze()
        for _i, (_, _row) in enumerate(_group.iterrows()):
            y = _row['y']
            x = _row['x']
            fs = _row['x_fs']
            _domain = _row['domain']
            if y.ndim == 1:
                y = y.reshape([-1, 1])
            y_single_responses = y

            if _domain == 'time' and sub_average_time_buffer_size is not None:
                fs = 1 / np.mean(np.diff(x))
                used_samples = int(np.floor(y.shape[0] // sub_average_time_buffer_size) * sub_average_time_buffer_size)
                y_f = y[0: used_samples, :]
                y_f = np.transpose(np.reshape(y_f, (sub_average_time_buffer_size, -1, y_f.shape[1]), order='F'),
                                   [0, 2, 1])
                y_f = np.mean(y_f, axis=2)
                x = np.arange(0, sub_average_time_buffer_size) / fs
                y_single_responses = y_f

            ax = plt.subplot(gs[_idx_row, _idx_col])
            if title_by == 'row':
                title = '{:}'.format(_current_row_group)
            if title_by == 'col':
                title = '{:}'.format(_current_col_group)

            if title_by == 'both':
                title = '{:} / {:}'.format(_current_row_group, _current_col_group)

            ax.set_title(title, y=1 + title_v_offset, size=6)
            if _domain == 'time':
                y_mean = np.mean(y_single_responses, axis=1)
                ax.plot(x, y_single_responses,  linewidth=1.0, alpha=0.2, color='gray')
            if _domain == 'frequency':
                y_mean = np.mean(np.abs(y_single_responses), axis=1)
                ax.plot(x, np.abs(y_single_responses), linewidth=1.0, alpha=0.1, color='gray')

            ax.plot(x, y_mean, color='m', linewidth=1.5)
            if _idx_row == row_conditions.size // 2 and _idx_col == 0:
                ax.set_ylabel('Amplitude [{:}]'.format(_row['y_unit']))
            if _domain == 'time':
                ax.set_xlabel('Time [{:}]'.format(_row['x_unit']))
                if time_xlim is not None:
                    ax.set_xlim(time_xlim)
                if time_ylim is not None:
                    ax.set_ylim(time_ylim)
                if time_vmarkers is not None:
                    [ax.axvline(_t, color='k', linestyle=':', linewidth=0.5) for _t in time_vmarkers]
            if _domain == 'frequency':
                if freq_xlim is not None:
                    ax.set_xlim(freq_xlim)
                if freq_ylim is not None:
                    ax.set_ylim(freq_ylim)
                ax.set_xlabel('Frequency [{:}]'.format(_row['x_unit']))
                if freq_vmarkers is not None:
                    [ax.axvline(_f, color='k', linestyle=':', linewidth=0.5) for _f in freq_vmarkers]

    all_axes = fig_out.get_axes()
    for ax in all_axes:
        ax.spines['top'].set_visible(False)
        if not ax.is_last_row():
            ax.set_xticklabels([])
            ax.set_xlabel('')
        ax.spines['left'].set_visible(True)
        ax.spines['right'].set_visible(False)
    inch = 2.54
    fig_out.set_size_inches(12.0/inch, 2.25 * len(row_conditions)/inch)
    fig_out.subplots_adjust(top=0.98, bottom=0.08, hspace=0.0, left=0.15, right=0.95)
    return fig_out


def plot_topographic_maps(dataframe: pd.DataFrame = None,
                          rows_by: str = None,
                          cols_by: str = None,
                          subject_id_column: str = 'subject_id',
                          channels_column: str = 'channel',
                          title: str = '',
                          topographic_value: float = None,
                          layout: str = None,
                          title_by: str = 'row',
                          title_v_offset: float = 0.0,
                          grid_size: np.complex = 600j,
                          color_map_label: str = None,
                          normalize: bool = False,
                          ) -> plt.figure:
    """
    This function will plot the waveforms contained in a pandas dataframe read using the sqlite_waveforms_to_pandas
    function of pEEGy.
    The rows and columns of the output plot are specified by the factors of the dataframe.
    The output will show the data for each of those factors (both individual and average data).
    :param dataframe: a pandas dataframe returned by sqlite_waveforms_to_pandas function of pEEGy.
    :param rows_by: name of the factor in the dataframe for which the rows in the plot will be split.
    :param cols_by: name of the factor in the dataframe for which the columns in the plot will be split.
    :param subject_id_column: string indicating the column name with subject ids
    :param channels_column: name of column containing channel labels
    :param title: title of the figure
    :param topographic_value: name of column containing the value to be shown by the topographic map
    :param layout: path or name of the layout to be used
    :param title_by: string specifying from which factor you want to show the titles in each panel. This can be: "row",
    "col", or "both"
    :param title_v_offset: float specifying the vertical offset of the title
    :param grid_size: complex number indicating the size of the grid,
    :param color_map_label: string with the label that would be use of the colourmap. If empty, the default value will
    be the topographic_value
    :param normalize: if True, topographic maps will be normalized within subject
    :return:
    """
    df = copy.copy(dataframe)
    _rows_and_cols = []
    row_conditions = np.array([1])
    col_conditions = np.array([1])
    if rows_by is not None:
        _rows_and_cols.append(rows_by)
        row_conditions = df[rows_by].astype("category").cat.categories
        n_rows = row_conditions.size
    else:
        df.loc[:, 'dummy_row'] = 1
        _rows_and_cols.append('dummy_row')
        n_rows = 1
    idx_rows = np.arange(row_conditions.size)

    if cols_by is not None:
        _rows_and_cols.append(cols_by)
        col_conditions = df[cols_by].astype("category").cat.categories
        n_cols = col_conditions.size
    else:
        df.loc[:, 'dummy_col'] = 1
        _rows_and_cols.append('dummy_col')
        n_cols = 1
    idx_cols = np.arange(col_conditions.size)

    df['topo_value'] = df[topographic_value]
    if normalize:
        df = df.assign(
            topo_value=df.groupby(
                [subject_id_column])[topographic_value].transform(lambda x: x / np.max(x)))
    if len(_rows_and_cols):
        sub_groups = df.groupby(_rows_and_cols).apply(
            lambda x: get_topographic_maps(x,
                                           subject_id_column=subject_id_column,
                                           layout=layout,
                                           channels_column=channels_column,
                                           topographic_value='topo_value',
                                           grid_size=grid_size))
    else:
        _potentials = get_topographic_maps(df,
                                           subject_id_column=subject_id_column,
                                           layout=layout,
                                           channels_column=channels_column,
                                           topographic_value='topo_value',
                                           grid_size=grid_size)
        df['potentials'] = _potentials
        df['dummy_row'] = 1
        df['dummy_col'] = 1
        _rows_and_cols = ['dummy_row', 'dummy_col']
        sub_groups = df
    if color_map_label is None:
        color_map_label = topographic_value

    groups = sub_groups.groupby(_rows_and_cols)
    fig_out = plt.figure(constrained_layout=True)
    widths = [1.0] * n_cols
    heights = [1.0] * n_rows
    heights.append(0.1)
    gs = fig_out.add_gridspec(ncols=n_cols, nrows=n_rows + 1,
                              width_ratios=widths,
                              height_ratios=heights)
    max_sub = sub_groups.potentials.apply(lambda x: np.ma.mean(x, axis=2)).apply(np.max).max()
    max_distance = sub_groups.max_distance.max()

    for _id, ((_current_row_group, _current_col_group), _group) in enumerate(groups):
        _idx_row = idx_rows[_current_row_group == row_conditions].squeeze()
        _idx_col = idx_cols[_current_col_group == col_conditions].squeeze()
        ax = plt.subplot(gs[_idx_row, _idx_col])
        if title_by == 'row':
            panel_title = '{:}'.format(_current_row_group)
        if title_by == 'col':
            panel_title = '{:}'.format(_current_col_group)

        if title_by == 'both':
            panel_title = '{:} / {:}'.format(_current_row_group, _current_col_group)

        ax.set_title(panel_title, y=1 + title_v_offset, size=6)
        std_average = np.ma.mean(_group.potentials.values[0], axis=2)
        ax_im = ax.imshow(std_average.T, origin='lower',
                          extent=(-max_distance, max_distance, -max_distance, max_distance),
                          vmin=0,
                          vmax=max_sub,
                          aspect=1.0)
        ax_im.set_cmap('nipy_spectral')

        levels = np.arange(0, max_sub, max_sub / 5.0)
        ax.contour(std_average.T,
                   levels,
                   origin='lower',
                   extent=(-max_distance, max_distance, -max_distance, max_distance),
                   linewidths=1.0,
                   colors='k')
        ax.autoscale(enable=False)
        # plot color bar

        if _id == 0:
            c_bar_ax = plt.subplot(gs[-1, :])
            c_bar = fig_out.colorbar(ax_im, cax=c_bar_ax, orientation='horizontal', format='%.1f')
            c_bar.set_label(color_map_label, fontsize=10)
            tick_locator = ticker.MaxNLocator(nbins=3)
            c_bar.locator = tick_locator
            c_bar.update_ticks()
            c_bar.ax.tick_params(labelsize=8)
        channels = _group.channels.values[0]
        channel_labels = [ch['label'] for ch in channels]
        ax.plot(0, max_distance * 1.0, '|', markersize=8, color='k')
        _lay = Layout()
        _layout = _lay.get_layout(file_name=layout)
        _layout = np.array([_l for _l in _layout if _l.label not in ['COMNT', 'SCALE']])
        for i, lay in enumerate(_layout):
            if lay.label in channel_labels:
                ax.plot(lay.x, lay.y, 'o', color='b', markersize=0.2)
            else:
                ax.plot(lay.x, lay.y, 'o', color='b', markersize=0.2)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis('off')

    all_axes = fig_out.get_axes()
    for ax in all_axes:
        ax.spines['top'].set_visible(False)
        if not ax.is_last_row():
            ax.set_xticklabels([])
            ax.set_xlabel('')
        ax.spines['left'].set_visible(True)
        ax.spines['right'].set_visible(False)
    inch = 2.54
    fig_out.suptitle(title)
    fig_out.set_size_inches(3.2 * len(col_conditions)/inch, h=3.2 * len(row_conditions)/inch)
    return fig_out


def get_topographic_maps(df,
                         subject_id_column: str = 'subject_id',
                         channels_column: str = 'channel',
                         topographic_value: str = None,
                         layout: str = None,
                         grid_size: np.complex = 600j):
    _lay = Layout()
    _layout = _lay.get_layout(file_name=layout)
    _layout = np.array([_l for _l in _layout if _l.label not in ['COMNT', 'SCALE']])
    _single_responses = np.array([])

    _subject_groups = df.groupby([subject_id_column])
    for _, (_id_sub, _sub_group) in enumerate(_subject_groups):
        x = []
        y = []
        z = []
        channels = []
        max_potential = -np.inf
        for _i, (_, _row) in enumerate(_sub_group.iterrows()):
            ch = _row[channels_column]
            amp = _row[topographic_value]
            for _l in _layout:
                if _l.label == ch:
                    x.append(_l.x)
                    y.append(_l.y)
                    z.append(amp)
            channels.append({'label': ch})

        _potentials, max_distance = eegpt.interpolate_potential_fields(x=np.array(x).reshape(-1, 1),
                                                                       y=np.array(y).reshape(-1, 1),
                                                                       z=np.array(z).reshape(-1, 1),
                                                                       grid=grid_size)
        max_potential
        if not _single_responses.size:
            _single_responses = _potentials[:, :, None]
        else:
            _single_responses = np.ma.dstack((_single_responses, _potentials))
    out = pd.Series(data={'potentials': _single_responses,
                          'max_distance': max_distance,
                          'channels': channels})
    return out
