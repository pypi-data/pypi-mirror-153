import unittest
import numpy as np
import peegy.processing.tools.eeg_epoch_operators as et


class DSSTests(unittest.TestCase):
    def test_et_demean(self):
        x = np.ones((100, 20, 30)) * np.arange(20)[:, None]
        dm_x = et.et_demean(x)
        self.assertAlmostEqual(np.sum(np.mean(dm_x, axis=0)), 0, delta=1e-12, msg="Should be 0")

    def test_et_demean_weights_1(self):
        x = np.random.randn(100, 20, 300) * np.arange(20)[:, None]
        w = np.ones((100, 1, 300))
        dm_x = et.et_demean(x, w)
        self.assertAlmostEqual(np.sum(np.mean(dm_x, axis=0)), 0, delta=1e-12, msg="Should be 0")

    def test_et_demean_weights_2(self):
        x = np.ones((100, 20, 300)) * np.arange(20)[:, None]
        w = 2 * np.ones((100, 20, 300))
        dm_x = et.et_demean(x, w)
        self.assertAlmostEqual(np.sum(np.mean(dm_x, axis=0)), 0, delta=1e-12, msg="Should be 0")

    def test_et_demean_weights_3(self):
        x = np.ones((100, 20, 300))
        w = np.arange(20)
        dm_x = et.et_demean(x, w)
        self.assertAlmostEqual(np.sum(np.mean(dm_x, axis=0)), 0, delta=1e-12, msg="Should be 0")

    def test_et_weighted_cov_1(self):
        x = np.ones((100, 20, 30)) * np.arange(20)[:, None]
        c1, t1 = et.et_weighted_covariance(x)
        c2, t2 = et.et_covariance(x)
        self.assertTrue(np.all(c1 == c2), msg="Should be True")

        w = np.ones(x.shape) * 2
        c1, t1 = et.et_weighted_covariance(x, w)
        c2, t2 = et.et_covariance(x)
        self.assertTrue(np.all(c1 / t1 == c2/t2), msg="Should be True")

    def test_et_weighted_cov_2(self):
        x = np.ones((100, 20, 30)) * np.arange(20)[:, None]
        w = np.ones(x.shape)
        w = w * np.arange(1, x.shape[2] + 1)
        c1, t1 = et.et_weighted_covariance(x, w)
        c2, t2 = et.et_covariance(x)
        self.assertTrue(np.all(c1 / t1 == c2/t2), msg="Should be True")


if __name__ == '__main__':
    unittest.main()
