"""
Many of the functions here defined are originally published by Alain de Cheveigné
http://audition.ens.fr/adc/NoiseTools/
"""
import numpy as np
import pyfftw
import multiprocessing
from tqdm import tqdm
import astropy.units as u
from peegy.tools.units.unit_tools import set_default_unit
__author__ = 'jaime undurraga'


def et_covariance(x: np.array = np.array([]),
                  shifts: np.array(int) = np.array([0]),
                  w: np.array = np.array([])) -> (np.array, float):
    """
    Compute covariance matrix

    :param x: numpy array with data
    :param shifts: integer array specifying shifts
    :param w: numpy array with weights
    :return c: numpy array with covariance matrix
    :return tw: weights norm
    """
    c = np.zeros((x.shape[1], x.shape[1]))
    if x.ndim == 2:
        x = x[:, :, None]
    if w.size == 0:
        for i in np.arange(x.shape[2]):
            xx = et_multi_shift(x[:, :, i], shifts)
            xx = xx.squeeze()
            c = c + xx.T.dot(xx)
        tw = xx.shape[0] * x.shape[2]
    else:
        tw = 0
        for i in np.arange(x.shape[2]):
            xx = x[:, :, i]
            xx = et_multi_shift(xx, shifts)
            ww = w[:, :, i]
            ww = et_multi_shift(ww, shifts)
            xx = xx * ww
            xx = xx.squeeze()
            c = c + xx.T.dot(xx)
            tw = tw + ww.T.dot(ww)
        # tw = np.sum(w[:])
        tw = xx.shape[0] * x.shape[2]
        # tw = np.sum(w[:, 0, :])
    return c, tw


def et_time_shifted_xcovariance(x: np.array = np.array([]),
                                y: np.array = np.array([]),
                                shifts: np.array(int) = np.array([0]),
                                wx: np.array = np.array([]),
                                wy: np.array = np.array([])) -> (np.array, float):
    """
        Compute covariance matrix between x and y

        :param x: numpy array with data
        :param y: numpy array with data
        :param shifts: integer array specifying shifts
        :param wx: numpy array with weights for x
        :param wy: numpy array with weights for y
        :return c: numpy array with covariance matrix
        :return tw: weights norm
        """

    n_shifts = shifts.size
    c = np.zeros((x.shape[1], y.shape[1] * n_shifts))
    if x.ndim == 2:
        x = x[:, :, None]
    if y.ndim == 2:
        y = y[:, :, None]
    if not wx.size:
        wx = np.ones(x.shape)
    if not wy.size:
        wy = np.ones(y.shape)
    # w_x = w_x / np.sum(w_x, axis=2, keepdims=True)
    # w_y = w_y / np.sum(w_y, axis=2, keepdims=True)
    tw = 0
    for i in np.arange(x.shape[2]):
        yy = et_multi_shift(y[:, :, i], shifts)
        wwy = et_multi_shift(wy[:, :, i], shifts)
        xx = x[0: yy.shape[0], :, i]
        wxx = wx[0: yy.shape[0], :, i]
        c = c + (xx * wxx).T.dot(yy * wwy)
        w_total = wxx.T.dot(wwy)
        tw = tw + w_total

    # for i in np.arange(x.shape[2]):
    #     yy = et_multi_shift(y[:, :, i], shifts)
    #     wwy = wy[:, :, i]
    #     xx = x[0: yy.shape[0], :, i]
    #     # wwx = wx[0: yy.shape[0], :, i]
    #
    #     c = c + xx * wwx.T.dot(yy * wwy)
    #
    # if not wy.size:
    #     tw = xx.shape[0] * y.shape[1] * yy.shape[0]
    # else:
    #     wy = wy[0: yy.shape[0], :, :]
    #     tw = np.sum(wy[:])
    return c, tw


def et_freq_shifted_xcovariance(x: np.array = np.array([]),
                                y: np.array = np.array([]),
                                shifts: np.array(int) = np.array([0]),
                                wx: np.array = np.array([]),
                                wy: np.array = np.array([]),
                                normalized_frequencies: np.array = np.array([])) -> (np.array, float):
    """
        Compute covariance matrix between x and y in the frequency domain
        :param x: numpy array with data
        :param y: numpy array with data
        :param shifts: integer array specifying shifts
        :param wx: numpy array with weights to be applied to x
        :param wy: numpy array with weights to be applied to y
        :param normalized_frequencies: normalized freqs to compute covariance
        :return c: numpy array with covariance matrix
        :return tw: weights norm
        """

    n_shifts = shifts.size
    c = np.zeros((x.shape[1], y.shape[1] * n_shifts))
    if x.ndim == 2:
        x = x[:, :, None]
    if y.ndim == 2:
        y = y[:, :, None]
    if not wx.size:
        wx = np.ones(x.shape)
    if not wy.size:
        wy = np.ones(y.shape)

    if x.ndim == 2:
        x = x[:, :, None]
    if np.mod(x.shape[0], 2) == 0:
        fft_size = int((x.shape[0] / 2) + 1)
    else:
        fft_size = int((x.shape[0] + 1) / 2)

    freq = np.arange(fft_size) / float(x.shape[0])
    freq_filt = np.zeros(shape=(fft_size, 1), dtype=np.float)
    for f_bin in et_find_freq_bin(freq, normalized_frequencies):
        freq_filt[f_bin] = 1.0

    c = 0
    tw = 0
    for i in np.arange(x.shape[2]):
        yy = et_multi_shift(y[:, :, i], shifts)
        wyy = et_multi_shift(wy[:, :, i], shifts)
        xx = x[0: yy.shape[0], :, i]
        wxx = wx[0: yy.shape[0], :, i]
        xx = xx * wxx
        fftx = pyfftw.builders.rfft(xx, overwrite_input=False, planner_effort='FFTW_ESTIMATE', axis=0,
                                    threads=multiprocessing.cpu_count())
        yy = y[:, :, i] * wyy
        ffty = pyfftw.builders.rfft(yy, overwrite_input=False, planner_effort='FFTW_ESTIMATE', axis=0,
                                    threads=multiprocessing.cpu_count())
        xfft = fftx()
        yfft = ffty()
        zx = xfft * freq_filt
        zy = yfft * freq_filt
        c = c + 2 * np.real(zx.T.conj().dot(zy))
        tw = tw + wxx.T.dot(wyy)

    return c, tw


def et_unfold(x, ortogonal=False):
    # unfold to improve machine performance during multiplications
    if ortogonal:
        return np.reshape(np.transpose(x, [0, 2, 1]), [-1, x.shape[1]], order='F')
    else:
        return np.reshape(np.transpose(x, [0, 2, 1]), [-1, x.shape[1]])


def et_fold(x, epoch_size):
    #  fold back to normal
    return np.transpose(np.reshape(x, [epoch_size, -1, x.shape[1]]), [0, 2, 1])


def et_mmat(x, m):
    return et_fold(et_unfold(x).dot(m), x.shape[0])


def et_x_covariance(x, y):
    c = np.zeros((x.shape[1], y.shape[1]))
    for i in np.arange(x.shape[2]):
        c += x[:, :, i].T.dot(y[:, :, i])
    return c


def et_weighted_covariance(
        x: np.array = np.array([]),
        w: np.array([]) = np.array([])) -> (np.array, np.array):
    """
    Compute the weighted covariance of x
    :param x: numpy array with data to compute weights
    :param w: numpy array with weights to be used
    :return: covariance matrix and the total weights
    """

    #
    #  X can be 1D, 2D or 3D.
    #  W can be 1D (if X is 1D or 2D) or 2D (if X is 3D). The same weight is
    #  applied to each column.
    if w.size == 0:
        w = np.ones(x.shape)
    assert x.shape[0] == w.shape[0], "x and w must have the same number of samples"

    if w.shape[1] == 1:
        w = np.tile(w, [1, x.shape[1]])
    assert w.shape[1] == x.shape[1], "x and w must have the same number of columns"
    if x.ndim == 2:
        x = x[:, :, None]
    if w.ndim == 2:
        w = w[:, :, None]
    # x = et_unfold(x)
    # w = et_unfold(w)
    #  weights
    tw = 0
    c = 0
    for i in np.arange(x.shape[2]):
        ww = w[:, :, i]
        xx = x[:, :, i] * ww
        w_total = ww.T.dot(ww)
        tw = tw + w_total
        c = c + xx.T.dot(xx)
    return c, tw


def et_x_join_covariance(x, y):
    # compute the covariance combining all epochs
    return et_unfold(x).T.dot(et_unfold(y))


def et_find_freq_bin(freq_vector: np.array = np.array([]),
                     freq_to_find: np.array = np.array([])):
    f_bins = []
    for f in freq_to_find:
        f_pos = np.argmin(np.abs(freq_vector - f))
        f_bins.append(f_pos)
    return f_bins


# def et_w_covariance(epochs: np.array = np.array([])):
#     c = np.zeros((epochs.shape[1], epochs.shape[1]))
    # w_mean, w = et_weighted_mean(epochs)
    # for i in np.arange(x.shape[2]):
    #     c = c + x[:, :, i].T.dot(x[:, :, i])
    # return cfol

def et_multi_shift(x: np.array = None,
                   shifts: np.array(int) = np.array([0])):
    """
    :param  x: matrix to shift
    :param shifts: array of shifts (must be nonnegative)
    :return z: shifted matrix
    """
    z = x
    if shifts.size > 0 and np.any(shifts > 0):
        assert x.shape[0] > np.max(shifts), 'shifts should be no larger than nrows'
        assert np.min(shifts) >= 0, 'shifts should be nonnegative'
        n_shifts = shifts.shape[0]
        n = x.shape[0] - np.max(shifts)
        shift_array = (np.ones((n, n_shifts)) * shifts + np.arange(0, n).reshape(-1, 1)).astype(int)
        if x.ndim == 2:
            x = x[:, :, None]
        n_s, n_ch, n_trials = x.shape
        n_trials = np.maximum(n_trials, 1)
        z = np.zeros((n, n_ch * n_shifts, n_trials))
        for k in np.arange(n_trials):
            for j in np.arange(0, n_ch):
                y = x[:, j, k]
                pos = np.arange(j * n_shifts, j * n_shifts + n_shifts).astype(int)
                z[:, pos, k] = y[shift_array]
    z = z.squeeze()
    return z


def et_freq_weighted_cov(x: np.array = np.array([]),
                         normalized_frequencies: np.array = np.array([]),
                         w: np.array = np.array([])):
    if x.ndim == 2:
        x = x[:, :, None]
    if np.mod(x.shape[0], 2) == 0:
        fft_size = int((x.shape[0] / 2) + 1)
    else:
        fft_size = int((x.shape[0] + 1) / 2)

    freq = np.arange(fft_size) / (float(x.shape[0]))
    freq_filt = np.zeros(shape=(fft_size, 1), dtype=np.float)
    for f_bin in et_find_freq_bin(freq, normalized_frequencies):
        freq_filt[f_bin] = 1.0
    if w.size == 0:
        w = np.ones(x.shape)
        # w = w / np.sum(w, axis=2, keepdims=True)
    # normalize weights
    # w = w / np.sum(w ** 2, axis=2, keepdims=True)
    c = 0
    tw = 0
    for i in tqdm(np.arange(x.shape[2]), desc='Spatial filter covariance estimation'):
        ww = w[:, :, i]
        xx = x[:, :, i] * ww
        fft = pyfftw.builders.rfft(xx, overwrite_input=False, planner_effort='FFTW_ESTIMATE', axis=0,
                                   threads=multiprocessing.cpu_count())
        xfft = fft()
        z = xfft * freq_filt
        c = c + 2 * np.real(z.T.conj().dot(z))
        tw = tw + ww.T.dot(ww)
    return c, tw


# def et_tsr(x: np.array = np.array([]),
#            ref: np.array = np.array([]),
#            shifts: np.array(int) = np.array([0]),
#            wx: np.array(int) = np.array([0]),
#            wref: np.array = np.array([]),
#            keep: np.array = np.array([]),
#            thresh: float = 1e-20) -> np.array:
#     """
#         Compute covariance matrix between x and y
#         :param x: numpy array with data
#         :param y: numpy array with data
#         :param shifts: integer array specifying shifts
#         :param wx: numpy array with weights
#         :param wy: numpy array with weights
#         :return c: numpy array with covariance matrix
#         :return tw: weights norm
#         """
#     # We need to adjust x and ref to ensure that shifts are non-negative.
#     # If some values of shifts are negative, we increment shifts and truncate x.
#     # adjust x to make shifts non-negative
#     offset1 = np.maximum(0, -shifts.min())
#     idx = np.arange(offset1, x.shape[0])
#     x = x[idx, :, :]  # truncate x
#     if wx.size > 0:
#         wx = wx[idx, :, :]  # truncate wx
#     shifts = shifts + offset1  # shifts are now positive
#     # adjust size of x
#     offset2 = np.maximum(0, shifts.max())
#     idx = np.arange(0, ref.shape[0] - offset2)
#     x = x[idx, :, :]  # part of x that overlaps with time-shifted refs
#     if wx.size > 0:
#         wx = wx[idx, :, :]  # truncate wx
#     [mx,nx,ox] = x.shape
#     [mref, nref, oref] = ref.shape
#     # consolidate weights into single weight matrix
#     w = np.zeros([mx, 1, oref])
#     if wx.size == 0 and wref.size == 0:
#         w[0: mx, :, :] = 1
#     elif wref.size == 0:
#         w[:, :, :] = wx[:, :, :]
#     elif wx.size == 0:
#         for k in range(ox):
#             wr = wref[:, :, k]
#             wr = ts_multishift(wr, shifts)
#             wr=np.min(wr, axis = 1)
#             w[:, :, k] = wr
#     else:
#         for k in range(ox):
#             wr = wref[:, :, k]
#             wr = nt_multishift(wr, shifts)
#             wr = np.min(wr, axis=1)
#             wr = np.min(wr, wx[0: wr.shape[0], :, k])
#             w[:, :, k] = wr
#     wx = w
#     wref = np.zeros(mref, 1, oref)
#     wref[idx, :, :] = w
#     # remove weighted means
#     x0 = x
#     x = et_demean(x, wx)
#     mn1 = x - x0
#     ref = et_demean(ref,wref)
#     # equalize power of ref chans, then equalize power of ref PCs
#     ref = nt_normcol(ref,wref)
#     ref = nt_pca(ref, 0, [], 1e-6)
#     ref = nt_normcol(ref, wref)
#     # covariances and cross covariance with time-shifted refs
#     [cref,twcref] = nt_cov(ref, shifts, wref)
#     [cxref,twcxref] = nt_xcov(x, ref, shifts, wx)
#     # regression matrix of x on time-shifted refs
#     r = nt_regcov(cxref/twcxref,cref/twcref,keep,thresh)
#     #  r=r*0.765;
#     #  TSPCA: clean x by removing regression on time-shifted refs
#     y = np.zeros[mx, nx, ox]
#     for k in range(ox):
#         z = nt_multishift(ref[:, :, k], shifts) * r
#         y[:, :, k] = x[0:z.shape[0], : , k] - z
#     y0 = y
#     y = et_demean(y, wx)    # multishift(ref) is not necessarily 0 mean
#     mn2 = y - y0
#     idx = np.arange(offset1, y.shape[0] + offset1)
#     mn = mn1 + mn2
#     w = wref
#     return y
#
# def nt_tsregress(x: np.array = np.array([]),
#                  y: np.array = np.array([]),
#                  shifts: np.array(int) = np.array([0]),
#                  wx: np.array(int) = np.array([0]),
#                  wy: np.array(int) = np.array([0]),
#                  keep: np.array = np.array([]),
#                  threshold: float = 1e-20) -> np.array:
#
#     #  z: part of x modeled by time-shifted y
#     #  idx: x(idx) maps to z
#
#     #  x: data to model
#     #  y: regressor
#     #  shifts: array of shifts to apply (default: [0])
#     #  xw: weights to apply to x
#     #  yw: weights to apply to y
#     #  keep: number of components of shifted regressor PCs to keep (default: all)
#     #  threshold: discard PCs with eigenvalues below this
#
#     # Data X are regressed on time-shifted versions of Y. X and Y are initially
#     # time-aligned, but because of the shifts, Z is shorter than X.  Z is
#     # time-aligned with X(IDX).
#
#     assert x.shape[0] == y.shape[0], "x and y must have same number of samples"
#
#     # shifts must be non-negative
#     mn = shifts.min()
#     if mn < 0:
#         shifts = shifts - mn
#         x = x[-mn::, :, :]
#         y = y[-mn::, :, :]
#
#     nshifts = shifts.size
#
#     #  #  flag outliers in x and y
#     #  if ~isempty(toobig1) || ~isempty(toobig2)
#     #      xw=nt_find_outliers(x,toobig1,toobig2);
#     #      yw=nt_find_outliers(y,toobig1,toobig2);
#     #  else
#     #      xw=[];yw=[];
#     #      # xw=ones(size(x)); yw=ones(size(y));
#     #  end
#
#     #  subtract weighted means
#
#     if x.ndim == 3:
#         [Mx, Nx, Ox] = x.shape
#         [My, Ny, Oy] = y.shape
#         x=et_unfold(x)
#         y=et_unfold(y)
#         [x, xmn] = et_demean(x, wx)
#         [y, ymn] = et_demean(y, wy)
#         x = et_fold(x, Mx)
#         y = et_fold(y, My)
#     else:
#         [x, xmn] = et_demean(x, wx)
#         [y, ymn] = et_demean(y, wy)
#
#     #  covariance of y
#     cyy, totalweight = et_covariance(y, shifts.T, wy)
#     cyy = cyy / totalweight
#
#     #  cross-covariance of x and y
#     [cxy, totalweight] = nt_cov2(x, y, shifts.T, wx, wy)
#     #disp('!!!!!!!!!   WARNING: calling obsolete code  !!!!!!!!!!!!!!!!');
#     # [cxy, totalweight]=nt_xcov(x,y,shifts',xw,yw);
#     cxy= cxy / totalweight
#
#     #  regression matrix
#     r = nt_regcov(cxy, cyy, keep, threshold)
#
#     #  regression
#     if x.ndim == 3:
#         x = et_unfold(x)
#         y = et_unfold(y)
#         [m, n, l] = x.shape
#         mm = m - shifts.max()
#         z = np.zeros(x.shape)
#         for k in range(nshifts):
#             kk = shifts(k)
#             idx1 = np.arange(kk, kk + mm)
#             idx2 = k + np.arange(0, y.shape[1] - 1) * nshifts
#             z[0: mm, :] = z[0: mm, :] + y[idx1, :] * r[idx2, :]
#
#         z=et_fold(z, Mx)
#         z = z[0:-shifts.max(), :, :]
#     else:
#         [m, n] = x.shape
#         z = np.zeros(m - shifts.max(), n)
#         for k in range(nshifts):
#             kk = shifts[k]
#             idx1 = np.arange(kk, kk + z.shape[0])
#             idx2 = k + np.arange(0, y.shape[1] - 1) * nshifts
#             z = z + y[idx1, :] * r[idx2, :]
#
#     #  idx allows x to be aligned with z
#     offset = np.maximum(0, -mn)
#     idx=np.arange(offset, offset + z.shape[0])
#
#
#
def et_demean(x: np.array = np.array([]),
              w: np.array = np.array([]),
              eps: float = np.finfo(float).eps):

    if w.size and w.size < x.shape[0]:
        w = w[:]
        # interpret w as array of indices to set to 1
        assert ~(np.min(w) < 0 or np.max(w) > x.shape[0]), 'w interpreted as indices but values are out of range'
        ww = np.zeros((x.shape[0], 1, 1))
        ww[w] = 1
        w = ww

    if w.ndim == 3 and w.shape[2] != x.shape[2]:
        if w.shape[2] == 1 and x.shape[2] != 1:
            w = np.tile(w, [1, 1, x.shape[2]])
        else:
            raise Exception('W should have same number of trials as X, or else 1')

    [m, n, o] = x.shape
    # xx = et_unfold(x)
    # ww = et_unfold(w)
    # mm = xx * ww / np.sum(ww, axis=0)
    # xx = xx - mm
    # x = et_fold(xx, x.shape[0])

    if w.size == 0:
        mn = np.mean(x, axis=0)
        x = x - mn
    else:
        # w = et_unfold(w)
        if w.shape[0] != x.shape[0]:
            raise Exception('X and W should have same number of rows')
        if w.shape[1] == 1:
            mn = np.sum(x * w, axis=0) / (np.sum(w, axis=0) + eps)
        elif w.shape[1] == n:
            mn = np.sum(x * w, axis=0) / (np.sum(w, axis=0) + eps)
        else:
            raise Exception('W should have same number of columns as X, or else 1')
        x = x - mn
    return x


def w_mean(epochs: np.array = np.array([]),
           weights: np.array = np.array([]),
           keepdims=False,
           axis=2):
    """
    Computes weighted mean using provided weights
    :param epochs: samples x channels x trials numpy array
    :param weights: samples x channels x trials numpy array or channels x trials numpy (assumed same weights across
    samples). If samples == 1, then same weight is use across samples
    :param keepdims: if True, dimension of original input is kept
    :param axis: direction in which to average
    :return: weighted average
    """
    if weights.size == 0:
        weights = np.ones(epochs.shape)
    if weights.ndim == 2 and epochs.ndim == 3:
        assert epochs.shape[1::] == weights.shape, "number of channels and trials must agree between epochs and weights"
    if weights.ndim == 3:
        if weights.shape[0] != 1:
            assert epochs.shape == weights.shape, "number samples, trials, and channels must agree between epochs and" \
                                                  " weights"
    if weights.ndim == 2:
        weights = np.tile(weights, (epochs.shape[0], 1, 1))
    # normalize weights across trials
    weights = weights / np.expand_dims(np.sum(weights, axis=axis), axis=axis)
    return np.sum(epochs * weights, axis=axis, keepdims=keepdims)


def effective_sampling_size(weights: np.array, axis=2):
    """
    compute the effective sample size resulting from the use of weights
    Kish, Leslie(1965). "Survey Sampling".New York: John  Wiley & Sons, Inc.ISBN 0 - 471 - 10949 - 5.
    "Design Effects and Effective Sample Size".
    https://docs.displayr.com/wiki/Design_Effects_and_Effective_Sample_Size

    :param weights: array of weights
    :param axis: direction indicating how weights are summed
    :return:
    """
    weights = set_default_unit(weights, u.dimensionless_unscaled)
    epsilon = np.finfo(float).eps * weights.unit ** 2.0
    ess = np.sum(weights, axis=axis) ** 2.0 / (np.sum(weights ** 2.0, axis=axis) + epsilon)
    return ess
