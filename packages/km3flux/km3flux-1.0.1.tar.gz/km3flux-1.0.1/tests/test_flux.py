from unittest import TestCase

import numpy as np

from km3flux.flux import (
    BaseFlux,
    Honda2015,
    HondaSarcevic,
    DarkMatterFlux,
    AllFlavorFlux,
    WimpSimFlux,
)  # noqa

# from km3flux.data import dm_gc_spectrum


class TestBaseFlux(TestCase):
    def setUp(self):
        self.flux = BaseFlux()
        assert self.flux is not None

    def test_shape_exception(self):
        with self.assertRaises(ValueError):
            self.flux([1, 2, 3], zenith=[3, 4])

    def test_nonimplemented(self):
        with self.assertRaises(NotImplementedError):
            self.flux([1, 2, 3])

        with self.assertRaises(NotImplementedError):
            self.flux([1, 2, 3], zenith=[2, 3, 4])

    def test_integration(self):
        with self.assertRaises(NotImplementedError):
            self.flux.integrate()
        with self.assertRaises(NotImplementedError):
            self.flux.integrate_samples([1, 2, 3])
        with self.assertRaises(IndexError):
            self.flux.integrate_samples([1, 2, 3], [1, 2])


class TestHonda2015(TestCase):
    def setUp(self):
        self.flux = Honda2015()
        assert self.flux is not None

    def test_shape_exception(self):
        with self.assertRaises(ValueError):
            self.flux([1, 2, 3], zenith=[3, 4])

    def test_call(self):
        self.flux([10, 20, 30])
        self.flux([10, 20, 30], zenith=[0.2, 0.3, 0.4])

    def test_integration(self):
        self.flux.integrate()
        self.flux.integrate_samples([1, 2, 3])
        with self.assertRaises(IndexError):
            self.flux.integrate_samples([1, 2, 3], [1, 2])

    def test_scalar(self):
        self.flux(1)
        self.flux(1, zenith=2)


class TestHondaSarcevic(TestCase):
    def setUp(self):
        self.flux = HondaSarcevic()
        assert self.flux is not None

    def test_shape_exception(self):
        with self.assertRaises(ValueError):
            self.flux([1, 2, 3], zenith=[3, 4])

    def test_call(self):
        with self.assertRaises(NotImplementedError):
            self.flux([1, 2, 3])
        self.flux([2, 3, 4], zenith=[1, 2, 3])

    def test_integration(self):
        with self.assertRaises(NotImplementedError):
            self.flux.integrate()
        with self.assertRaises(NotImplementedError):
            self.flux.integrate_samples([1, 2, 3])
        with self.assertRaises(IndexError):
            self.flux.integrate_samples([1, 2, 3], [0.1, 0.2])


class TestDMFlux(TestCase):
    def test_init(self):
        dmf = DarkMatterFlux(flavor="nu_mu", channel="w", mass=90)
        assert dmf is not None

    def test_flux(self):
        dmf = DarkMatterFlux(flavor="nu_mu", channel="w", mass=90)
        dmf([3])
        dmf([20])
        with self.assertRaises(ValueError):
            dmf([99])
        dmf([18])
        energy = np.array([3, 20, 18, 2, 4, 50, 28])
        dmf(energy)
        risky_energy = np.array([3, 20, 18, 2, 4, 50, 28, 90])
        dmf(risky_energy)
        bad_energy = np.array([3, 20, 18, 2, 4, 50, 28, 99])
        with self.assertRaises(ValueError):
            dmf(bad_energy)


#  class TestDartMatterLoader(TestCase):
#      def test_cast(self):
#          x1, y1 = dm_gc_spectrum('nu_mu', 'b', '90')
#          x2, y2 = dm_gc_spectrum('nu_mu', 'b', 90)
#          assert np.array_equal(x1, x2)
#          assert np.array_equal(y1, y2)
#
#      def test_shape_normal(self):
#          x, y = dm_gc_spectrum('nu_mu', 'b', '90')
#          assert x.shape == y.shape
#
#      def test_shape_full(self):
#          x, y = dm_gc_spectrum('nu_mu', 'b', '90', full_lims=True)
#          assert x.shape[0] == y.shape[0] - 1
#
#      def test_avail(self):
#          with self.assertRaises(KeyError):
#              x, y = dm_gc_spectrum('bad', 'b', '90')
#          with self.assertRaises(KeyError):
#              x, y = dm_gc_spectrum('nu_mu', 'crazy', '90')
#          with self.assertRaises(KeyError):
#              x, y = dm_gc_spectrum('nu_mu', 'b', '90000000000')


class TestWimpSim(TestCase):
    def setUp(self):
        self.flux = WimpSimFlux()
        assert self.flux is not None

    def test_flux(self):
        dmf = self.flux
        dmf([3])
        dmf([20])
        with self.assertRaises(ValueError):
            dmf([9999])
        dmf([18])
        energy = np.array([3, 20, 18, 2, 4, 50, 28])
        dmf(energy)
        risky_energy = np.array([3, 20, 18, 2, 4, 50, 28, 90])
        dmf(risky_energy)
        bad_energy = np.array([3, 20, 18, 2, 4, 50, 28, 9999])
        with self.assertRaises(ValueError):
            dmf(bad_energy)


class TestAllFlavorFlux(TestCase):
    def setUp(self):
        self.flavor = ["nu_mu", "anu_mu", "anu_mu"]
        self.ene = [10, 20, 30]
        self.zen = [1, 1.5, 2]

    def test_call(self):
        flux = AllFlavorFlux()
        flux(self.ene, self.zen, self.flavor)
