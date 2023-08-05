import numpy as np
import astropy.units as u


def set_default_unit(value: np.array = None,
                     unit=u.Unit) -> u.quantity.Quantity:
    """
    This function will convert a numpy array into a Quantity using the default unit, only if the input does not have
    a unit
    :param value: array to set default units
    :param unit: the default unit to use
    :return: array with units
    """
    if value is None:
        return
    if isinstance(value, u.quantity.Quantity):
        out = value
    else:
        out = value * unit
        print('No metric unit set, assuming {:}'.format(unit))
    return out
