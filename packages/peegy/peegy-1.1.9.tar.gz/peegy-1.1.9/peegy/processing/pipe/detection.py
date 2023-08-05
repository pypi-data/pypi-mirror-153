from peegy.processing.pipe.definitions import InputOutputProcess
from peegy.processing.tools.detection.time_domain_tools import detect_peaks_and_amplitudes, TimePeakWindow, \
    PeakToPeakMeasure
import numpy as np
import pandas as pd
import os
from PyQt5.QtCore import QLibraryInfo
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(QLibraryInfo.PluginsPath)


class PeakDetectionTimeDomain(InputOutputProcess):
    def __init__(self, input_process=InputOutputProcess, time_peak_windows=np.array([TimePeakWindow]),
                 peak_to_peak_measures=np.array([PeakToPeakMeasure]), **kwargs):
        super(PeakDetectionTimeDomain, self).__init__(input_process=input_process, **kwargs)
        self.time_peak_windows = time_peak_windows
        self.peak_to_peak_measures = peak_to_peak_measures

    def transform_data(self):
        peak_containers, amplitudes = detect_peaks_and_amplitudes(
            data_node=self.input_node,
            time_peak_windows=self.time_peak_windows,
            eeg_peak_to_peak_measures=self.peak_to_peak_measures)

        _data_pd = pd.concat([_peaks.to_pandas() for _peaks in peak_containers], ignore_index=True)
        _amps_pd = pd.concat([_amp.to_pandas() for _amp in amplitudes], ignore_index=True)
        self.output_node.data = self.input_node.data
        self.output_node.peak_times = _data_pd
        self.output_node.peak_to_peak_amplitudes = _amps_pd
