import psutil as psu
import numpy as np


def enough_memory(data: np.array = None):
    """
    This function returns true, when there is enough memory in the system to allocate an array of same dimensions as
    data
    :param data: array from which memory will be estimated
    :return:
    """
    _virtual_memory = psu.virtual_memory()
    memory_fraction = _virtual_memory.available / data.nbytes
    return memory_fraction > 1
