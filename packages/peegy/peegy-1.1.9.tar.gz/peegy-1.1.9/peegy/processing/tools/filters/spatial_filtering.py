import numpy as np
import peegy.processing.tools.eeg_epoch_operators as eo
import warnings

__author__ = 'jundurraga'


def nt_dss0(c0: np.array = np.array([]),
            c1: np.array = np.array([]),
            keep0: int = None,
            keep1: float = 1e-9,
            perc0: float = .99,
            perc1: float = None
            ):
    """
    Generate DSS matrix
    :param c0: average covariance matrix across all epochs
    :param c1: covariance matrix of average data
    :param keep0: number of components to keep. This parameter is useful to remove negligent components and to add
    numerical stability.
    :param keep1: float indicating the a threshold (relative to the maximum eigenvalue) to keep components and to add
    numerical stability.
    :param perc0: float indicating a percentage of explained variance that would be used as a threshold to keep
    components when whitening data.
    :param perc1: float indicating a percentage of explained variance that would be used as a threshold to keep
    components when generating dss rotation.
    :return: dss matrix, unbiased power, and biased power.
    """
    # whitening and selection of components for stability
    topcs_1, evs_1 = nt_pcarot(c0, keep0)
    evs_1 = np.abs(evs_1)

    if keep1 is not None:
        idx = np.where(evs_1 / np.max(evs_1) > keep1)[0]
        topcs_1 = topcs_1[:, idx]
        evs_1 = evs_1[idx]

    if perc0 is not None:
        n_evs_1 = evs_1 / np.sum(evs_1)
        _thr = np.argwhere(np.cumsum(n_evs_1) > perc0)
        _n = _thr[0] if _thr.size else evs_1.size - 1
        _idx_to_keep = np.arange(_n + 1)
        topcs_1 = topcs_1[:, _idx_to_keep]
        evs_1 = evs_1[_idx_to_keep]

    # apply PCA and whitening to the biased covariance and ensure that non-negative eigen values are produced
    n1 = np.diag(np.sqrt(1 / evs_1))
    c2 = n1.T.dot(topcs_1.T).dot(c1).dot(topcs_1).dot(n1)
    # matrix to convert PCA-whitened data to DSS
    topcs_2, evs_2 = nt_pcarot(c2, keep0)

    if perc1 is not None:
        n_evs_2 = evs_2 / np.sum(evs_2)
        _thr2 = np.argwhere(np.cumsum(n_evs_2) > perc1)
        _n2 = _thr2[0] if _thr2.size else evs_2.size - 1
        _idx_to_keep2 = np.arange(_n2 + 1)
        topcs_2 = topcs_2[:, _idx_to_keep2]
        # evs_2 = evs_2[_idx_to_keep2]

    # DSS matrix (raw data to normalized DSS)
    todss = topcs_1.dot(n1).dot(topcs_2)
    n2 = np.diagonal(todss.T.dot(c0).dot(todss))
    if np.any(n2 <= 0):
        warnings.warn("""
        Negative or zero normalization value in DSS filter.
        This is usually caused by numerical errors on very low eigenvalue components. Please check the whitening
        threshold. Usually increasing this threshold helps to overcome this issue.
        """)

    todss = todss.dot(np.diag(1 / np.sqrt(n2)))  # adjust so that components are normalized

    # power per DSS component
    pwr0 = np.sqrt(np.sum((c0.T.dot(todss) ** 2), axis=0))  # unbiased
    pwr1 = np.sqrt(np.sum((c1.T.dot(todss) ** 2), axis=0))  # biased
    return todss, pwr0, pwr1


def nt_pcarot(cov: np.array = np.array([]),
              n: int = 0):
    eigen_val, eigen_vec = np.linalg.eig(cov)
    eigen_vec = np.real(eigen_vec)
    eigen_val = np.real(eigen_val)
    idx = np.argsort(eigen_val)[::-1]
    if n:
        idx = idx[0: n]
    return eigen_vec[:, idx], eigen_val[idx]


def nt_bias_fft(x: np.array = np.array([]),
                normalized_frequencies: np.array = np.array([]),
                w: np.array = np.array([])):
    if w.size == 0:
        w = np.ones(x.shape)
    c0, _ = eo.et_covariance(x, w=w)
    c1, _ = eo.et_freq_weighted_cov(x, w=w, normalized_frequencies=normalized_frequencies)
    return c0, c1


def nt_bias_fft2(x: np.array = np.array([]),
                 normalized_frequencies: np.array = np.array([]),
                 w: np.array = np.array([])):
    if w.size == 0:
        w = np.ones(x.shape)
    w_ave = eo.w_mean(x, weights=w)
    c0, t0 = eo.et_freq_weighted_cov(x, normalized_frequencies=normalized_frequencies)
    c1, t1 = eo.et_freq_weighted_cov(w_ave, normalized_frequencies=normalized_frequencies)
    return c0, c1, t0, t1
