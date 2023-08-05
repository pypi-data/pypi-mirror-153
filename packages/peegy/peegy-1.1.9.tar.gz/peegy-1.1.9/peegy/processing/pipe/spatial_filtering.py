from peegy.processing.pipe.definitions import InputOutputProcess
from peegy.processing.tools.epochs_processing_tools import et_get_spatial_filtering, et_apply_spatial_filtering
from peegy.processing.tools.eeg_epoch_operators import et_unfold
from peegy.definitions.channel_definitions import Domain, ChannelItem
from peegy.processing.tools.epochs_processing_tools import et_ica_epochs
from peegy.processing.tools.eeg_epoch_operators import et_fold
from peegy.processing.pipe.epochs import AverageEpochs, AverageEpochsFrequencyDomain
from peegy.processing.pipe.plot import PlotWaveforms, PlotTopographicMap
import numpy as np
import os
import copy
import astropy.units as u
from peegy.tools.units.unit_tools import set_default_unit
from PyQt5.QtCore import QLibraryInfo
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(QLibraryInfo.PluginsPath)


class SpatialFilter(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 sf_join_frequencies: np.array = None,
                 demean_data: bool = True,
                 weight_data: bool = True,
                 keep0: int = None,
                 keep1: float = 1e-9,
                 perc0: float = .99,
                 perc1: float = None,
                 block_size: int = 10,
                 delta_frequency: u.Quantity = 5 * u.Hz,
                 **kwargs):
        """
        This class will create a spatial filter based on the data. If sf_join_frequencies are passed, the spatial
        filter will use a biased function based on the covariance of those frequencies only.
        :param input_process:  InputOutputProcess Class
        :param sf_join_frequencies: numpy array indicating the biased frequencies (useful for steady-state responses)
        :param demean_data: if true, data will be demeaned prior filter estimation
        :param weight_data: if true, dss filter will be estimated using weights
        :param keep0: integer controlling  whitening of unbiased components in DSS. This integer value represent the
        number of components to keep.
        :param keep1: float controlling  whitening of unbiased components in DSS. This value will remove components
        below keep1 which is relative to the maximum eigen value.
        :param perc0: float (between 0 and 1) controlling whitening of unbiased components in DSS.
        This value will preserve components that explain the percentage of variance.
        :param perc1: float (between 0 and 1) controlling the number of biased components kept in DSS.
        This value will preserve the components of the biased PCA analysis that explain the percentage of variance.
        :param block_size: integer indicating the number of trials that would be use to estimate the weights
        :param delta_frequency: frequency size around each sf_join_frequency to estimate noise
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(SpatialFilter, self).__init__(input_process=input_process, **kwargs)
        self.sf_join_frequencies = set_default_unit(sf_join_frequencies, u.Hz)
        self.demean_data = demean_data
        self.weight_data = weight_data
        self.pwr0 = None
        self.pwr1 = None
        self.cov = None
        self.keep0 = keep0
        self.keep1 = keep1
        self.perc0 = perc0
        self.perc1 = perc1
        self.block_size = block_size
        self.delta_frequency = delta_frequency

    def transform_data(self):
        # compute spatial filter
        z, pwr0, pwr1, cov,  _ = et_get_spatial_filtering(epochs=self.input_node.data,
                                                          fs=self.input_node.fs,
                                                          sf_join_frequencies=self.sf_join_frequencies,
                                                          demean_data=self.demean_data,
                                                          weight_data=self.weight_data,
                                                          weights=self.input_node.w,
                                                          keep0=self.keep0,
                                                          keep1=self.keep1,
                                                          perc0=self.perc0,
                                                          perc1=self.perc1,
                                                          block_size=self.block_size,
                                                          delta_frequency=self.delta_frequency)
        self.output_node.data = z * u.dimensionless_unscaled
        self.pwr0 = pwr0
        self.pwr1 = pwr1
        self.cov = cov


class ApplySpatialFilter(InputOutputProcess):
    def __init__(self,
                 input_process: SpatialFilter = None,
                 sf_components: np.array = np.array([]),
                 sf_thr: float = 0.8,
                 **kwargs):
        """
        This class will apply an SpatialFilter to the data. If sf_components are paased, only those will be used to
        filter the data
        :param input_process: an SpatialFilter InputOutputProcess Class
        :param sf_components: numpy array of integers with indexes of components to be kept
        :param sf_thr: float indicating the percentage of explained variance by components to be kept (this is used when
        sf_components is empty)
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(ApplySpatialFilter, self).__init__(input_process=input_process, **kwargs)
        self.sf_components = sf_components
        self.sf_thr = sf_thr

    def transform_data(self):
        filtered_data, _ = et_apply_spatial_filtering(z=self.input_node.data,
                                                      pwr0=self.input_process.pwr0,
                                                      pwr1=self.input_process.pwr1,
                                                      cov_1=self.input_process.cov,
                                                      sf_components=self.sf_components,
                                                      sf_thr=self.sf_thr)
        self.output_node.data = filtered_data


class CreateAndApplySpatialFilter(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 sf_join_frequencies: np.array = None,
                 sf_components=np.array([]),
                 sf_thr: float = 0.8,
                 keep0: int = None,
                 keep1: float = 1e-9,
                 perc0: float = .99,
                 perc1: float = None,
                 delta_frequency: u.Quantity = 5 * u.Hz,
                 block_size: int = 10,
                 demean_data: bool = True,
                 weight_data: bool = True,
                 projection_domain: Domain = Domain.time,
                 components_to_plot: np.array = np.arange(0, 10),
                 plot_projections: bool = True,
                 plot_x_lim: [float, float] = None,
                 plot_y_lim: [float, float] = None,
                 user_naming_rule: str = '',
                 fig_format: str = '.png',
                 return_figures: bool = False,
                 save_to_file: bool = True,
                 **kwargs):
        """
        This class will create and apply an spatial filter to the data.
        :param input_process: an InputOutputProcess Class
        :param sf_join_frequencies: numpy array indicating the biased frequencies (useful for steady-state responses)
        :param sf_components: numpy array of integers with indexes of components to be kept
        :param sf_thr: float indicating the percentage of explained variance by components to be kept (this is used when
        sf_components is empty)
        :param keep1: float controlling  whitening of unbiased components in DSS. This value will remove components
        below keep1 which is relative to the maximum eigen value.
        :param perc0: float (between 0 and 1) controlling whitening of unbiased components in DSS.
        This value will preserve components that explain the percentage of variance.
        :param perc1: float (between 0 and 1) controlling the number of biased components kept in DSS.
        This value will preserve the components of the biased PCA analysis that explain the percentage of variance.
        :param delta_frequency: frequency size around each sf_join_frequency to estimate noise
        :param demean_data: If true, filter will be created with demeaned data
        :param weight_data: if true, weighted average will be use to create the filter
        :param projection_domain: indicate the domain in which component will be projected in plots
        :param components_to_plot: numpy array indicating which components will be plotted.
        :param plot_projections: if true, components will be projected to the original space and plots will be generated
        :param plot_x_lim: list with minimum and maximum horizontal range of x axis
        :param plot_y_lim: list with minimum and maximum vertical range of y axis
        :param user_naming_rule: string indicating a user naming to be included in the figure file name
        :param fig_format: string indicating the format of the output figure (e.g. '.png' or '.pdf')
        :param return_figures: bool indicating if figure handle should be returned in self.figures
        :param save_to_file: bool indicating whether figure should be saved to file
        :param block_size: number of trials that will be stack together to estimate the residual noise
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(CreateAndApplySpatialFilter, self).__init__(input_process=input_process, **kwargs)
        self.sf_join_frequencies = set_default_unit(sf_join_frequencies, u.Hz)
        self.sf_components = sf_components
        self.sf_thr = sf_thr
        self.keep0 = keep0
        self.keep1 = keep1
        self.perc0 = perc0
        self.perc1 = perc1
        self.delta_frequency = delta_frequency
        self.block_size = block_size
        self.components_to_plot = components_to_plot
        self.plot_projections = plot_projections
        self.projection_domain = projection_domain
        self.demean_data = demean_data
        self.weight_data = weight_data
        self.plot_x_lim = plot_x_lim
        self.plot_y_lim = plot_y_lim
        self.user_naming_rule = user_naming_rule
        self.fig_format = fig_format
        self.return_figures = return_figures
        self.save_to_file = save_to_file
        self.__kwargs = kwargs

    def transform_data(self):
        figures = None
        if self.return_figures:
            figures = []
        spatial_filter = SpatialFilter(input_process=self.input_process,
                                       sf_join_frequencies=self.sf_join_frequencies,
                                       demean_data=self.demean_data,
                                       weight_data=self.weight_data,
                                       keep0=self.keep0,
                                       keep1=self.keep1,
                                       perc0=self.perc0,
                                       perc1=self.perc1,
                                       block_size=self.block_size,
                                       delta_frequency=self.delta_frequency
                                       )
        spatial_filter.run()
        filtered_data = ApplySpatialFilter(input_process=spatial_filter,
                                           sf_components=self.sf_components,
                                           sf_thr=self.sf_thr,
                                           **self.__kwargs)
        filtered_data.run()
        self.output_node = filtered_data.output_node
        if self.components_to_plot is not None:
            plotter_1 = PlotSpatialFilterComponents(spatial_filter,
                                                    plot_x_lim=self.plot_x_lim,
                                                    plot_y_lim=self.plot_y_lim,
                                                    user_naming_rule=self.user_naming_rule,
                                                    fig_format=self.fig_format,
                                                    components_to_plot=self.components_to_plot,
                                                    domain=self.projection_domain,
                                                    return_figures=self.return_figures,
                                                    save_to_file=self.save_to_file
                                                    )
            plotter_1.run()
            if self.return_figures:
                figures.append(plotter_1.figures)
            if self.plot_projections and self.save_to_file:
                plotter_2 = ProjectSpatialComponents(spatial_filter,
                                                     user_naming_rule=self.user_naming_rule,
                                                     plot_x_lim=self.plot_x_lim,
                                                     plot_y_lim=self.plot_y_lim,
                                                     components_to_plot=self.components_to_plot,
                                                     domain=self.projection_domain,
                                                     return_figures=self.return_figures
                                                     )
                plotter_2.run()
                if self.return_figures:
                    figures += plotter_2.figures
        self.figures = figures


class PlotSpatialFilterComponents(InputOutputProcess):
    def __init__(self, input_process=SpatialFilter,
                 components_to_plot: np.array = np.arange(0, 10),
                 domain: Domain = Domain.time,
                 user_naming_rule: str = 'components',
                 plot_x_lim: [float, float] = None,
                 plot_y_lim: [float, float] = None,
                 fig_format: str = '.png',
                 return_figures: bool = False,
                 save_to_file: bool = True,
                 **kwargs):
        """
        This class plots the components waveforms (from an SpatialFilter)
        :param input_process: anInputOutputProcess Class
        :param components_to_plot: numpy array indicating which components will be plotted.
        :param domain: indicate the domain in which component will be projected
        :param user_naming_rule: string indicating a user naming to be included in the figure file name
        :param plot_x_lim: list with minimum and maximum horizontal range of x axis
        :param plot_y_lim: list with minimum and maximum vertical range of y axis
        :param fig_format: string indicating the format of the output figure (e.g. '.png' or '.pdf')
        :param return_figures: bool indicating if figure should be returned in self.figures
        :param save_to_file: bool indicating whether figure should be saved to file
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(PlotSpatialFilterComponents, self).__init__(input_process=input_process, **kwargs)
        self.components_to_plot = components_to_plot
        self.domain = domain
        self.user_naming_rule = user_naming_rule
        self.plot_x_lim = plot_x_lim
        self.plot_y_lim = plot_y_lim
        self.fig_format = fig_format
        self.return_figures = return_figures
        self.save_to_file = save_to_file
        self.__kwargs = kwargs

    def transform_data(self):
        if self.components_to_plot is not None:
            # we copy the input process to overwrite the layout without affecting other pipe processes
            _input_process = copy.deepcopy(self.input_process)

            # _input_process.output_node.y_units = u.def_unit('A.U.')
            # generate a generic layout
            _input_process.output_node.layout = np.array([ChannelItem()
                                                          for _ in range(_input_process.output_node.data.shape[1])])
            for _i, _lay in enumerate(_input_process.output_node.layout):
                _lay.label = str(_i)

            if self.domain == Domain.time:
                average = AverageEpochs(_input_process)

            if self.domain == Domain.frequency:
                average = AverageEpochsFrequencyDomain(_input_process,
                                                       test_frequencies=self.input_process.sf_join_frequencies,
                                                       delta_frequency=self.input_process.delta_frequency,
                                                       weight_frequencies=self.input_process.sf_join_frequencies
                                                       )
            average.name = 'AveragedSpatialComponents'
            average.run()
            plotter = PlotWaveforms(average,
                                    user_naming_rule='{:}_{:}_components'.format(
                                        self.user_naming_rule,
                                        average.output_node.data.shape[1]),
                                    ch_to_plot=self.components_to_plot,
                                    plot_x_lim=self.plot_x_lim,
                                    plot_y_lim=None,
                                    fig_format=self.fig_format,
                                    return_figures=self.return_figures,
                                    save_to_file=self.save_to_file)
            plotter.run()
            self.figures = plotter.figures


class ProjectSpatialComponents(InputOutputProcess):
    def __init__(self, input_process=SpatialFilter,
                 components_to_plot: np.array = np.arange(0, 10),
                 user_naming_rule: str = '',
                 plot_x_lim: [float, float] = None,
                 plot_y_lim: [float, float] = None,
                 domain: Domain = Domain.time,
                 return_figures: bool = False,
                 **kwargs):
        """
        This class will project back to the sensor space each component and plot them in a topographic map.
        :param input_process: an SpatialFilter InputOutputProcess Class
        :param components_to_plot: numpy array indicating which components will be plotted.
        :param user_naming_rule: string indicating a user naming to be included in the figure file name
        :param plot_x_lim: list with minimum and maximum horizontal range of x axis
        :param plot_y_lim: list with minimum and maximum vertical range of y axis
        :param domain: indicate the domain in which component will be projected
        :param return_figures: if true, figures will be returned in self.figures
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(ProjectSpatialComponents, self).__init__(input_process=input_process, **kwargs)
        self.components_to_plot = components_to_plot
        self.user_naming_rule = user_naming_rule
        self.plot_x_lim = plot_x_lim
        self.plot_y_lim = plot_y_lim
        self.domain = domain
        self.return_figures = return_figures
        self.__kwargs = kwargs

    def transform_data(self):
        figures = []
        for _component in self.components_to_plot:
            if _component > self.input_process.output_node.data.shape[1] - 1:
                continue
            if isinstance(self.input_process, SpatialFilter):
                projected_component = ApplySpatialFilter(input_process=self.input_process,
                                                         sf_components=np.array([_component]))
            if isinstance(self.input_process, SpatialFilterICA):
                projected_component = ApplySpatialFilterICA(input_process=self.input_process,
                                                            sf_components=np.array([_component]))
            projected_component.run()
            if self.domain == Domain.time:
                average = AverageEpochs(projected_component)
            if self.domain == Domain.frequency:
                average = AverageEpochsFrequencyDomain(projected_component,
                                                       test_frequencies=self.input_process.sf_join_frequencies,
                                                       weight_frequencies=self.input_process.sf_join_frequencies,
                                                       delta_frequency=self.input_process.delta_frequency)
            average.run()
            times = None
            if self.domain == Domain.time:
                max_chan = np.argmax(np.std(average.output_node.data, axis=0))
                cha_max_pow_label = average.output_node.layout[max_chan].label
                # find max and min within plot_x_lim
                if self.plot_x_lim is not None:
                    self.plot_x_lim = set_default_unit(self.plot_x_lim, average.output_node.x.unit)
                    _samples = average.output_node.x_to_samples(self.plot_x_lim)
                    _max = np.argmax(average.output_node.data[_samples[0]: _samples[-1], max_chan]) + _samples[0]
                    _min = np.argmin(average.output_node.data[_samples[0]: _samples[-1], max_chan]) + _samples[0]
                else:
                    _max = np.argmax(average.output_node.data[:, max_chan])
                    _min = np.argmin(average.output_node.data[:, max_chan])
                times = np.sort(average.output_node.x[np.array([_max, _min])])
            if self.domain == Domain.frequency:
                if self.input_process.sf_join_frequencies is not None:
                    _idx_f = average.output_node.x_to_samples(self.input_process.sf_join_frequencies)
                    max_chan = np.argmax(np.max(np.abs(average.output_node.data[_idx_f, :]), axis=0))
                    cha_max_pow_label = average.output_node.layout[max_chan].label

            # plot time potential fields for average channel
            _sep = '_' if self.user_naming_rule is not None else ''
            plotter = PlotTopographicMap(average,
                                         user_naming_rule=self.user_naming_rule + _sep + 'component_{:}'.format(
                                             _component),
                                         topographic_channels=np.array([cha_max_pow_label]),
                                         plot_x_lim=self.plot_x_lim,
                                         plot_y_lim=self.plot_y_lim,
                                         return_figures=self.return_figures,
                                         title='Component {:}'.format(_component),
                                         times=times)
            plotter.run()
            if self.return_figures and plotter.figures is not None:
                figures += plotter.figures
        self.figures = figures


class CreateAndApplyICAFilter(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 sf_components=np.array([]),
                 sf_thr=0.8,
                 components_to_plot: np.array = np.arange(0, 10),
                 plot_x_lim: [float, float] = None,
                 plot_y_lim: [float, float] = None,
                 n_tracked_points=256,
                 block_size=5,
                 weight_data=True,
                 user_naming_rule: str = '',
                 fig_format: str = '.png',
                 return_figures: bool = False,
                 **kwargs):
        """
        This class will create and apply an ICA filter to the data.
        :param input_process: an InputOutputProcess Class
        :param sf_components: numpy array of integers with indexes of components to be kept
        :param sf_thr: float indicating the percentage of explained variance by components to be kept (this is used when
        sf_components is empty)
        :param components_to_plot: numpy array indicating which components will be plotted.
        :param plot_x_lim: list with minimum and maximum horizontal range of x axis
        :param plot_y_lim: list with minimum and maximum vertical range of y axis
        :param user_naming_rule: string indicating a user naming to be included in the figure file name
        :param fig_format: string indicating the format of the output figure (e.g. '.png' or '.pdf')
        :param return_figures: if True, figures handles will be returnted on self.figures
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(CreateAndApplyICAFilter, self).__init__(input_process=input_process, **kwargs)
        self.sf_components = sf_components
        self.sf_thr = sf_thr
        self.components_to_plot = components_to_plot
        self.plot_x_lim = plot_x_lim
        self.plot_y_lim = plot_y_lim
        self.user_naming_rule = user_naming_rule
        self.fig_format = fig_format
        self.return_figures = return_figures
        self.n_tracked_points = n_tracked_points
        self.block_size = block_size
        self.weight_data = weight_data
        self._unmixing = None
        self._mixing: np.array = None
        self._pwr: np.array = None
        self._components: np.array = None
        self._whitening_m: np.array = None
        self.__kwargs = kwargs

    def transform_data(self):
        spatial_filter = SpatialFilterICA(input_process=self.input_process)
        spatial_filter.run()
        print('applying ICA filter')
        filtered_data = ApplySpatialFilterICA(input_process=spatial_filter,
                                              sf_components=self.sf_components,
                                              sf_thr=self.sf_thr,
                                              **self.__kwargs)
        filtered_data.run()
        self.output_node = filtered_data.output_node

        if self.components_to_plot is not None:
            plotter = PlotSpatialFilterComponents(spatial_filter,
                                                  plot_x_lim=self.plot_x_lim,
                                                  plot_y_lim=self.plot_y_lim,
                                                  user_naming_rule=self.user_naming_rule,
                                                  fig_format=self.fig_format,
                                                  components_to_plot=self.components_to_plot
                                                  )
            plotter.run()

            plotter = ProjectSpatialComponents(spatial_filter,
                                               user_naming_rule=self.user_naming_rule,
                                               plot_x_lim=self.plot_x_lim,
                                               plot_y_lim=self.plot_y_lim,
                                               components_to_plot=self.components_to_plot
                                               )
            plotter.run()


class SpatialFilterICA(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess,
                 **kwargs):
        """
        This class will create an spatial filter based on the data.
        :param input_process:  InputOutputProcess Class
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(SpatialFilterICA, self).__init__(input_process=input_process, **kwargs)
        self.mixing = None
        self.unmixing = None
        self.pwr = None
        self.whitening_m = None
        self.epoch_size = None

    def transform_data(self):
        # compute spatial filter
        _data = self.input_node.data
        self.epoch_size = _data.shape[0]
        if self.input_node.data.ndim == 3:
            _data = et_unfold(self.input_node.data)
        components, unmixing, mixing, pwr, whitening_m = et_ica_epochs(data=_data,
                                                                       tol=1e-4,
                                                                       iterations=10)
        self.mixing = mixing
        self.unmixing = unmixing
        self.pwr = pwr
        self.whitening_m = whitening_m
        self.output_node.data = et_fold(components, epoch_size=self.epoch_size)


class ApplySpatialFilterICA(InputOutputProcess):
    def __init__(self, input_process: SpatialFilterICA = None,
                 sf_components: np.array = np.array([]),
                 sf_thr: float = 0.8,
                 **kwargs):
        """
        This class will apply an SpatialFilter to the data. If sf_components are paased, only those will be used to
        filter the data
        :param input_process: an SpatialFilter InputOutputProcess Class
        :param sf_components: numpy array of integers with indexes of components to be kept
        :param sf_thr: float indicating the percentage of explained variance by components to be kept (this is used when
        sf_components is empty)
        :param kwargs: extra parameters to be passed to the superclass
        """
        super(ApplySpatialFilterICA, self).__init__(input_process=input_process, **kwargs)
        self.sf_components = sf_components
        self.sf_thr = sf_thr

    def transform_data(self):
        print('applying spatial filter')
        if self.sf_components is None or not self.sf_components.size:
            cumpower = np.cumsum(self.input_process.pwr) / np.sum(self.input_process.pwr)
            n_idxs = np.argwhere(cumpower <= self.sf_thr)
            n_components = np.arange(n_idxs.size)
        else:
            n_components = self.sf_components

        clean_epochs = self.mix_components(components_idx=n_components)
        if self.input_process.epoch_size is not None:
            clean_epochs = et_fold(clean_epochs, epoch_size=self.input_process.epoch_size)
        self.output_node.data = clean_epochs

    def mix_components(self,
                       components_idx: np.array = None):
        w_c = np.zeros(self.input_process.mixing.shape)
        w_c[:, components_idx] = 1
        s_clean = self.input_process.mixing * w_c
        _components = et_unfold(self.input_process.output_node.data)
        clean_data = s_clean.dot(_components.T).T
        return clean_data
