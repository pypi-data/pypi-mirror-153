import os
from os.path import sep
import shutil


class DirectoryPaths(object):
    def __init__(self, file_path='', delete_all=False, delete_figures=False, figures_subset_folder=''):
        file_path = os.path.expanduser(file_path)
        self.file_path = file_path
        self.file_directory = os.path.dirname(os.path.abspath(file_path))
        self.file_basename_path = os.path.abspath(os.path.splitext(file_path)[0])
        self.delete_all = delete_all
        self.delete_figures = delete_figures
        figures_dir = os.path.join(self.file_directory, 'figures')
        if (self.delete_all or self.delete_figures) and os.path.exists(figures_dir):
            try:
                shutil.rmtree(figures_dir)
            except OSError:
                print((OSError.message))
        if not os.path.exists(figures_dir):
            os.makedirs(figures_dir)
        self.figures_dir = figures_dir

        data_directory = os.path.join(self.file_directory, '.data')
        if self.delete_all and os.path.exists(data_directory):
            try:
                shutil.rmtree(data_directory)
            except OSError:
                print((OSError.message))
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)
        self.data_dir = data_directory
        self.subset_identifier = figures_subset_folder

    def get_figure_basename_path(self):
        return os.path.join(self.figure_subset_path, os.path.basename(self.file_path).split('.')[0])

    figure_basename_path = property(get_figure_basename_path)

    def get_data_basename_path(self):
        return os.path.join(self.data_subset_path, os.path.basename(self.file_path).split('.')[0])

    data_basename_path = property(get_data_basename_path)

    def get_figure_subset_path(self):
        _path = os.path.join(self.figures_dir, self.subset_identifier) + sep
        if not os.path.exists(_path):
            os.makedirs(_path)
        return _path

    figure_subset_path = property(get_figure_subset_path)

    def get_data_subset_path(self):
        _path = os.path.join(self.data_dir, self.subset_identifier)
        if not os.path.exists(_path):
            os.makedirs(_path)
        return _path

    data_path = property(get_data_subset_path)
    figures_current_dir = property(get_figure_subset_path)
