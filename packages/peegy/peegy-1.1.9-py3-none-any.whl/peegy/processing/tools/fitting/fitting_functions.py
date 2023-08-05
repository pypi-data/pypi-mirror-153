import numpy as np
__author__ = 'jundurraga'


def electrical_exponential_decay(t, a0, a1, a2):
    t0 = t[0]
    return a0 + a1 * np.exp(-a2 * (t - t0))
