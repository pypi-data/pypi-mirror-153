import matplotlib.pyplot as plt
import os
import graphviz
import PIL as pil
import pydot
import tempfile
from PyQt5.QtCore import QLibraryInfo
from peegy.processing.pipe.definitions import InputOutputProcess
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(QLibraryInfo.PluginsPath)


class PipePool(dict):
    """This class manages InputOutputProcess appended to it.
    When InputOutputProcess are appended, to the PipePool, they can be called by calling the run function of the
    PipePool. If an element has been already run, this won't be called again.
    """

    def __init__(self):
        super(PipePool, self).__init__()

    def __del__(self):
        plt.close('all')

    def __setitem__(self, key, value):
        # optional processing here
        assert isinstance(value, InputOutputProcess)
        key = self.ensure_unique_name(label=key)
        super(PipePool, self).__setitem__(key, value)
        # we add the new item as class variable
        setattr(self, key, value)
        # set name of InoutOutputProcess
        value.name = key

    def append(self, item: object, name=None):
        if name is None:
            name = type(item).__name__
        self[name] = item

    def ensure_unique_name(self, label: str = None):
        all_names = [_key for _key in self.keys()]
        _label = label
        count = 0
        while _label in all_names:
            _label = label + '_' + str(count)
            count = count + 1
        if count > 0:
            print('PipePool item "{:}" already exists. Renamed to "{:}"'.format(label, _label))
        return _label

    def __getitem__(self, key):
        return super(PipePool, self).__getitem__(key)

    def run(self):
        for _item, _value in self.items():
            if _value.ready:
                continue
            _value.run()
            _value.ready = True

    def diagram(self,
                file_name: str = '',
                return_figure=False,
                dpi=300,
                ):
        """
        This function generates a flow diagram with the available connections in the pipeline
        :param file_name: string indicating the file name to save pipeline diagram
        :param return_figure: boolean indicating if figure should be returned
        :param dpi: resolution of output figure

        """
        _file, file_extension = os.path.splitext(file_name)
        _temp_file = tempfile.mkdtemp() + os.sep + 'diagram'
        gviz = graphviz.Digraph("Pipeline",
                                filename=_temp_file,
                                node_attr={'color': 'lightblue2', 'style': 'filled'},
                                format=file_extension.replace('.', ''))
        gviz.attr(rankdir='TB', size='7,14')
        items = list(self.items())
        for _idx_1 in list(range(len(self))):
            _current_list = []
            _assigned = False
            for _idx_2 in list(range(len(self))):
                if _idx_1 == _idx_2:
                    continue
                (_name_1, process_1) = items[_idx_1]
                (_name_2, process_2) = items[_idx_2]
                if process_1 is not None and process_2 is not None:
                    process_2_list = []
                    if isinstance(process_1, InputOutputProcess):
                        if isinstance(process_2.input_process, InputOutputProcess):
                            process_2_list = [process_2.input_process]
                        elif isinstance(process_2.input_process, list) and all(isinstance(x, InputOutputProcess)
                                                                               for x in process_2.input_process):
                            process_2_list = process_2.input_process
                        else:
                            raise ValueError('Either an InputOutputProcess or list of them should be used')
                    for _p2 in process_2_list:
                        if process_1 == _p2:
                            _current_list.append(_name_2)
                            gviz.edge(_name_1, _name_2)
                            _assigned = True
            if not _assigned:
                gviz.node(_name_1)
        gviz.render(_temp_file)
        # use numpy to construct an array from the bytes
        gviz.save(_temp_file)
        (graph,) = pydot.graph_from_dot_file(_temp_file)
        graph.write_png(_file + '.png', prog=['dot', '-Gdpi={:}'.format(dpi)])
        fig_out = None

        if return_figure:
            img = pil.Image.open(_file + '.png')
            fig_out = plt.figure()
            ax = fig_out.add_subplot(111)
            ax.imshow(img, aspect=1)
            ax.axis('off')
            fig_out.tight_layout()
        return fig_out
