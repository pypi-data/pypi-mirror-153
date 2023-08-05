import unittest
import peegy.processing.tools.detection.time_domain_tools as td
from peegy.processing.pipe.definitions import DataNode
import numpy as np

__author__ = 'bwilliges-uoc'


class TestPeakDetectionMethods(unittest.TestCase):

    def test_peak(self):
        # create simple peak data
        fs = 44100.0
        nsamples = int(np.round(1 * fs))
        data = np.zeros((nsamples, 1))
        p1peak = int(np.round(0.1 * fs))  # P1 peak at 100 ms
        n1peak = int(np.round(0.15 * fs))  # N1 peak at 150 ms
        p2peak = int(np.round(0.2 * fs))  # P2 peak at 200 ms
        data[p1peak] = 1  # P1 peak
        data[n1peak] = -1  # N1 peak
        data[p2peak] = 1  # P2 peak
        dataobject = DataNode(fs=fs, data=data, rn=np.zeros(1)+1, snr=np.zeros(1), s_var=np.zeros(1)+1)
        tw = np.array([td.TimePeakWindow(ini_time=50e-3, end_time=150e-3, label='P1', positive_peak=True),
                       td.TimePeakWindow(ini_time=100e-3, end_time=200e-3, label='N1', positive_peak=False),
                       td.TimePeakWindow(ini_time=110e-3, end_time=300e-3, label='P2', positive_peak=True)])
        pm = np.array([td.PeakToPeakMeasure(ini_peak='N1', end_peak='P2')])
        peak_containers, amplitudes = td.detect_peaks_and_amplitudes(dataobject,
                                                                     time_peak_windows=tw,
                                                                     peak_to_peak_measures=pm)
        a = peak_containers[0].get_peaks()
        self.assertEqual([a[0].idx, a[1].idx, a[2].idx], [p1peak, n1peak, p2peak])
        # self.assertEqual(amplitudes, 2)
        # later test case with reference window
        twref = np.array([td.TimePeakWindow(ini_time=50e-3, end_ref='N1', label='P1', positive_peak=True),
                          td.TimePeakWindow(ini_time=100e-3, end_time=200e-3, label='N1', positive_peak=False),
                          td.TimePeakWindow(ini_ref='N1', end_time=300e-3, label='P2', positive_peak=True)])
        pm = np.array([td.PeakToPeakMeasure(ini_peak='N1', end_peak='P2')])
        peak_containers, amplitudes = td.detect_peaks_and_amplitudes(dataobject, time_peak_windows=twref,
                                                                     peak_to_peak_measures=pm)
        a = peak_containers[0].get_peaks()
        self.assertEqual([a[1].idx, a[0].idx, a[2].idx], [p1peak, n1peak, p2peak])
        self.assertEqual([a[0].idx, a[1].idx, a[2].idx], [p1peak, n1peak, p2peak])
        # self.assertEqual(amplitudes, 2)


if __name__ == '__main__':
    unittest.main()
