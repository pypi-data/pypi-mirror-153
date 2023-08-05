import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy import interpolate
import gc
# from pykCSD.pykCSD import KCSD

__author__ = 'jaime undurraga'


def interpolate_potential_fields(x, y, z, **kwargs):
    grid = kwargs.get('grid', 1000j)
    max_distance = np.max(np.linalg.norm((x, y), axis=0))
    grid_x, grid_y = np.mgrid[-max_distance:max_distance:grid, -max_distance:max_distance:grid]
    mask_int = np.array([])
    if x.size > 1 and y.size > 1 and z.size > 1:
        try:
            int_data = interpolate.griddata(points=np.hstack((x, y)), values=np.squeeze(z), xi=(grid_x, grid_y),
                                            method='cubic', rescale=True)
        except ValueError:
            int_data = interpolate.griddata(points=np.hstack((x, y)), values=np.squeeze(z), xi=(grid_x, grid_y),
                                            method='nearest', rescale=True)
        int_data = extrapolate_nans(grid_x, grid_y, int_data)

        radius = int_data.shape[0] / 2.0
        mask_int = mask_data(int_data, int_data.shape[0]/2, int_data.shape[1]/2, radius)

    return mask_int, np.maximum(grid_x.max(), grid_y.max())


def extrapolate_nans(x, y, v):
    '''
    Extrapolate the NaNs or masked values in a grid INPLACE using nearest
    value.

    .. warning:: Replaces the NaN or masked values of the original array!

    Parameters:

    * x, y : 1D arrays
        Arrays with the x and y coordinates of the data points.
    * v : 1D array
        Array with the scalar value assigned to the data points.

    Returns:

    * v : 1D array
        The array with NaNs or masked values extrapolated.
    '''

    if np.ma.is_masked(v):
        nans = v.mask
    else:
        nans = np.isnan(v)
    notnans = np.logical_not(nans)
    v[nans] = interpolate.griddata((x[notnans], y[notnans]), v[notnans],
                                   (x[nans], y[nans]), method='nearest').ravel()
    return v


def mask_data(data, center_x, center_y, radius):
    # mask data from center of the circle
    ny, nx = data.shape
    ix, iy = np.meshgrid(np.arange(nx), np.arange(ny))
    distance = np.sqrt((ix - center_x)**2 + (iy - center_y)**2)
# Mask portions of the data array outside of the circle
    data = np.ma.masked_where(distance > radius, data)
    return data


def plot_clipped(data, center_x, center_y, radius):
    """Plots the image clipped outside of a circle by using a clip path"""
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Make a circle
    circ = patches.Circle((center_x, center_y), radius, facecolor='none')
    ax.add_patch(circ)  # Plot the outline

    # Plot the clipped image
    ax.imshow(data, clip_path=circ, clip_on=True)
    ax.title('Clipped Array')
    plt.close(fig)
    gc.collect()


def get_3D_spherical_positions(x, y):
    r = np.max(np.concatenate((x, y)))
    pos = [(_x, _y, (r ** 2.0 - (_x ** 2.0 + _y ** 2.0)) ** 0.5) for _x, _y in zip(x, y)]
    return np.squeeze(np.array(pos))
