# -*- coding: utf-8 -*-
"""
Test various methods to denoise data
"""
# import initExample  ## Add path to library (just for examples; you do not need this)

from peegy.processing.tools.eeg_epoch_operators import et_multi_shift, et_covariance, et_time_shifted_xcovariance
import numpy as np

a = np.arange(0, 100.0).reshape(10, -1, 5, order='F')
b = et_multi_shift(a, np.array([0]))
print(b)

b = et_covariance(a, shifts=np.array([2]), w=np.ones(a.shape) * 2.0)
print(b)

c = et_time_shifted_xcovariance(a, a - 1, shifts=np.array([2]), w=np.ones(a.shape) * 2.0)
print(c)

c = et_time_shifted_xcovariance(a, a - 1, shifts=np.array([2, 3]), w=np.ones(a.shape) * 2.0)
print(c)
