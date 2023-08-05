import os
from os.path import sep
import logging
import numpy as np
from peegy.definitions.channel_definitions import ChannelItem
import matplotlib.pyplot as plt
__author__ = 'jundurraga'
log = logging.getLogger()


class Layout(object):
    def __init__(self, file_name='biosemi64.lay'):
        self.layout = self.get_layout(file_name=file_name)

    def get_layout(self, file_name='biosemi64.lay'):
        """
        Reads in a .lay Layout file, as specified by the variable file_name.
        The function will recognize all layouts inside of the "Layouts" subdirectory of peegy-Python.
        To ease working with subject specific Layout files, it is also possible to include the full path in the
        filename.
        :file_name: string containing the Layout file name (can contain a full path).
        """
        _path, file_name = os.path.split(file_name)
        if not _path:
            _path = os.path.dirname(os.path.realpath(__file__))
        return self.read_layout(_path + sep + file_name)

    @staticmethod
    def read_layout(file_path=None):
        out = np.array([])
        if file_path is not None:
            with open(file_path, 'r') as f:
                while True:
                    _data = f.readline()
                    if not _data:
                        break
                    lay = _data.rstrip().split('\t')
                    out = np.append(out,
                                    ChannelItem(idx=int(lay[0]) - 1,
                                                x=float(lay[1]),
                                                y=float(lay[2]),
                                                w=float(lay[3]),
                                                h=float(lay[4]),
                                                label=lay[5]))
        return out

    def get_labels(self):
        return np.array([_ch.label for _ch in self.layout])

    def get_index(self):
        return np.array([_ch.idx for _ch in self.layout])

    def get_item(self, idx=None):
        _idx = max(0, min(idx, self.layout.size))
        return self.layout[_idx]

    @staticmethod
    def change_layout_idem(layout={}, labels_to_replace=[['from', 'to']], channel_mapping=[]):
        for _pair in labels_to_replace:
            _l_from = _pair[0]
            _l_to = _pair[1]
            _pos_ch_from = [(_pos, layout['channel'][_pos]) for _pos, _ch in enumerate(layout['label']) if
                            _ch == _l_from]
            _pos_ch_to = [(_pos, layout['channel'][_pos]) for _pos, _ch in enumerate(layout['label']) if
                          _ch == _l_to]

            if _pos_ch_from:
                number_in_map_from = [(_pos, _ch['number']) for _pos, _ch in enumerate(channel_mapping) if
                                      _ch['number'] == _pos_ch_from[0][1]]
            else:
                number_in_map_from = [(_pos, _ch['number']) for _pos, _ch in enumerate(channel_mapping) if
                                      _ch['label'] == _l_from]

            if _pos_ch_to:
                number_in_map_to = [(_pos, _ch['number']) for _pos, _ch in enumerate(channel_mapping) if
                                    _ch['number'] == _pos_ch_to[0][1]]
            else:
                number_in_map_to = [(_pos, _ch['number']) for _pos, _ch in enumerate(channel_mapping) if
                                    _ch['label'] == _l_to]

            if number_in_map_from and number_in_map_to:
                ini_channel = number_in_map_from[0][1]
                end_channel = number_in_map_to[0][1]
                if _pos_ch_from:
                    _pos_from = _pos_ch_from[0][0]
                    layout['channel'][_pos_from] = end_channel
                else:
                    channel_mapping[number_in_map_from[0][0]]['number'] = end_channel

                text = 'remapping channel {:s} to {:s}'.format(_l_from, _l_to)
                logging.info('\n' + ''.join(text))
                print(text)

                if _pos_ch_to:
                    _pos_to = _pos_ch_to[0][0]
                    layout['channel'][_pos_to] = ini_channel
                else:
                    channel_mapping[number_in_map_to[0][0]]['number'] = ini_channel

                text = 'remapping channel {:s} to {:s}'.format(_l_to, _l_from)
                logging.info('\n' + ''.join(text))
                print(text)
            else:
                text = 'could not remap channel {:s} by {:s}, ' \
                       'one of the electrode pairs is not in the map'.format(_l_to, _l_from)
                logging.info('\n' + ''.join(text))
                print(text)

    def plot_layout(self):
        fig_out = plt.figure(constrained_layout=True)
        widths = [1.0]
        heights = [1.0]
        gs = fig_out.add_gridspec(ncols=1, nrows=1, width_ratios=widths,
                                  height_ratios=heights)
        inch = 2.54
        fig_out.subplots_adjust(wspace=0.0, hspace=0.0)
        fig_out.set_size_inches(20.0 / inch, 20.0 / inch)
        ax = plt.subplot(gs[0, 0])
        for i, lay in enumerate(self.layout):
            ax.plot(lay.x, lay.y, 'o', color='b', markersize=1)
            ax.text(lay.x, lay.y, lay.label)
        return fig_out
