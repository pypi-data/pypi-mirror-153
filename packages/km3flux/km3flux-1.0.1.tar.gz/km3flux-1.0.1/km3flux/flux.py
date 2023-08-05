"""Assorted Fluxes, in  (m^2 sec sr GeV)^-1"""

import logging
from six import string_types

import h5py
import numpy as np
import pandas as pd
from scipy.integrate import romberg, simps
from scipy.interpolate import splrep, splev, RectBivariateSpline

from km3flux.data import (
    pdg2name,
    name2pdg,
    HONDAFILE,
    DM_GC_FLAVORS,
    DM_GC_CHANNELS,  # noqa
    DM_GC_MASSES,
    DM_GC_FILE,
    WIMPSIM_FILE,
    WIMPSIM_FLAVORS,
    WIMPSIM_INTERESTING_CHANNELS,
    WIMPSIM_MASSES,
    DM_SUN_CHAN_TRANS_INV,
    # dm_gc_spectrum, dm_sun_spectrum,
    # DM_SUN_FLAVORS, DM_SUN_CHANNELS, DM_SUN_MASSES
)

FLAVORS = ("nu_e", "anu_e", "nu_mu", "anu_mu")
MCTYPES = [name2pdg(name) for name in FLAVORS]

logger = logging.getLogger(__name__)


def bincenters(bins):
    """Bincenters, assuming they are all equally spaced."""
    bins = np.atleast_1d(bins)
    return 0.5 * (bins[1:] + bins[:-1])


def issorted(arr):
    """Check if array is sorted."""
    return np.all(np.diff(arr) >= 0)


class BaseFlux(object):
    """Base class for fluxes.

    Methods
    =======
    __call__(energy, zenith=None)
        Return the flux on energy, optionally on zenith.
    integrate(zenith=None, emin=1, emax=100, **integargs)
        Integrate the flux via romberg integration.
    integrate_samples(energy, zenith=None, emin=1, emax=100)
        Integrate the flux from given samples, via simpson integration.

    Example
    =======
    >>> zen = np.linspace(0, np.pi, 5)
    >>> ene = np.logspace(0, 2, 5)

    >>> from km3flux.flux import MyFlux
    >>> flux = MyFlux(flavor='nu_mu')

    >>> flux(ene)
    array([6.68440000e+01, 1.83370000e+01, 4.96390000e+00,
           1.61780000e+00, 5.05350000e-01,])
    >>> flux(ene, zen)
    array([2.29920000e-01, 2.34160000e-02, 2.99460000e-03,
           3.77690000e-04, 6.87310000e-05])
    """

    def __init__(self, **kwargs):
        pass

    def __call__(self, energy, zenith=None, interpolate=True):
        logger.debug("Interpolate? {}".format(interpolate))
        energy = np.atleast_1d(energy)
        logger.debug("Entering __call__...")
        if zenith is None:
            logger.debug("Zenith is none, using averaged table...")
            return self._averaged(energy, interpolate=interpolate)
        zenith = np.atleast_1d(zenith)
        if len(zenith) != len(energy):
            raise ValueError("Zenith and energy need to have the same length.")
        logger.debug("Zenith available, using angle-dependent table...")
        return self._with_zenith(energy=energy, zenith=zenith, interpolate=interpolate)

    def _averaged(self, energy, interpolate=True):
        logger.debug("Interpolate? {}".format(interpolate))
        raise NotImplementedError

    def _with_zenith(self, energy, zenith, interpolate=True):
        logger.debug("Interpolate? {}".format(interpolate))
        raise NotImplementedError

    def integrate(self, zenith=None, emin=1, emax=100, interpolate=True, **integargs):
        logger.debug("Interpolate? {}".format(interpolate))
        return romberg(self, emin, emax, vec_func=True, **integargs)

    def integrate_samples(
        self, energy, zenith=None, emin=1, emax=100, interpolate=True, **integargs
    ):
        logger.debug("Interpolate? {}".format(interpolate))
        energy = np.atleast_1d(energy)
        mask = (emin <= energy) & (energy <= emax)
        energy = energy[mask]
        if zenith:
            logger.debug("Zenith available, using angle-dependent table...")
            zenith = np.atleast_1d(zenith)
            zenith = zenith[mask]
        flux = self(energy, zenith=zenith, interpolate=interpolate)
        return simps(flux, energy, **integargs)


class PowerlawFlux(BaseFlux):
    """E^-gamma flux."""

    def __init__(self, gamma=2, scale=1e-4):
        self.gamma = gamma
        self.scale = scale

    def _averaged(self, energy, interpolate=True):
        return self.scale * np.power(energy, -1 * self.gamma)

    def integrate(self, zenith=None, emin=1, emax=100, **integargs):
        """Compute analytic integral instead of numeric one."""
        if np.around(self.gamma, decimals=1) == 1.0:
            return np.log(emax) - np.log(emin)
        num = np.power(emax, 1 - self.gamma) - np.power(emin, 1 - self.gamma)
        den = 1.0 - self.gamma
        return self.scale * (num / den)


class Honda2015(BaseFlux):
    """
    Get Honda 2015 atmospheric neutrino fluxes.

    Whitepaper at https://arxiv.org/abs/1502.03916.

    Flux table downloaded from http://www.icrr.u-tokyo.ac.jp/~mhonda/

    Flux at Frejus site, no mountain, solar minimum.

    Units are (1 / m^2 sec sr GeV)

    Methods
    =======
    __init__(flavor='nu_mu')
        Load flux table for the given neutrino flavor.
    __call__(energy, zenith=None)
        Return the flux on energy, optionally on zenith.
    integrate(zenith=None, emin=1, emax=100, **integargs)
        Integrate the flux via omberg integration.
    integrate_samples(energy, zenith=None, emin=1, emax=100)
        Integrate the flux from given samples, via simpson integration.
    """

    def __init__(self, flavor="nu_mu"):
        self.table = None
        self.avtable = None
        filename = HONDAFILE
        if flavor not in FLAVORS:
            raise ValueError("Unsupported flux '{}'".format(flavor))
        with h5py.File(filename, "r") as h5:
            self.energy_bins = h5["energy_binlims"][:]
            self.cos_zen_bins = h5["cos_zen_binlims"][:]
            self.table = h5[flavor][:]
            self.avtable = h5["averaged/" + flavor][:]
        # adjust upper bin for the case zenith==0
        self.cos_zen_bins[-1] += 0.00001
        self.energy_bincenters = bincenters(self.energy_bins)
        self.cos_zen_bincenters = bincenters(self.cos_zen_bins)
        assert issorted(self.cos_zen_bincenters)
        assert issorted(self.energy_bincenters)
        assert self.avtable.shape == self.energy_bincenters.shape
        assert self.table.shape[0] == self.cos_zen_bincenters.shape[0]
        assert self.table.shape[1] == self.energy_bincenters.shape[0]
        self.avinterpol = splrep(
            self.energy_bincenters,
            self.avtable,
        )
        self.interpol = RectBivariateSpline(
            self.cos_zen_bincenters, self.energy_bincenters, self.table
        )

    def _averaged(self, energy, interpolate=True):
        logger.debug("Interpolate? {}".format(interpolate))
        if not interpolate:
            fluxtable = self.avtable
            ene_bin = np.digitize(energy, self.energy_bins)
            ene_bin = ene_bin - 1
            return fluxtable[ene_bin]
        else:
            flux = splev(energy, self.avinterpol)
            return flux

    def _with_zenith(self, energy, zenith, interpolate=True):
        logger.debug("Interpolate? {}".format(interpolate))
        energy = np.atleast_1d(energy)
        zenith = np.atleast_1d(zenith)
        cos_zen = np.cos(zenith)
        if not interpolate:
            fluxtable = self.table
            ene_bin = np.digitize(energy, self.energy_bins)
            zen_bin = np.digitize(cos_zen, self.cos_zen_bins)
            ene_bin = ene_bin - 1
            zen_bin = zen_bin - 1
            return fluxtable[zen_bin, ene_bin]
        else:
            flux = self.interpol.ev(cos_zen, energy)
            return flux


class HondaSarcevic(BaseFlux):
    """
    Get Honda + Sarcevic atmospheric neutrino fluxes.
    """

    def __init__(self, flavor="nu_mu"):
        self.table = None
        self.avtable = None
        filename = HONDAFILE
        if flavor not in FLAVORS:
            raise ValueError("Unsupported flux '{}'".format(flavor))
        with h5py.File(filename, "r") as h5:
            self.energy_bins = h5["energy_binlims"][:]
            self.cos_zen_bins = h5["cos_zen_binlims"][:]
            self.table = h5["honda_sarcevic/" + flavor][:]
        # adjust upper bin for the case zenith==0
        self.cos_zen_bins[-1] += 0.00001

    def _averaged(self, energy, interpolate=True):
        raise NotImplementedError("Supports only zenith dependent flux!")

    def _with_zenith(self, energy, zenith, interpolate=True):
        fluxtable = self.table
        cos_zen = np.cos(zenith)
        ene_bin = np.digitize(energy, self.energy_bins)
        zen_bin = np.digitize(cos_zen, self.cos_zen_bins)
        ene_bin = ene_bin - 1
        zen_bin = zen_bin - 1
        return fluxtable[zen_bin, ene_bin]


class DarkMatterFlux(BaseFlux):
    """
    Get Dark Matter WimpWimp->foo->nu spectra.

    Units are ``d/d n_particles / cm^2 sec sr``.

    >>> from km3flux import DarkMatterFlux
    >>> flux = DarkMatterFlux('anu_mu')
    >>> flux(ene)
    array([  6.68440000e+01,   1.83370000e+01,   4.96390000e+00,
         1.61780000e+00,   5.05350000e-01,   2.29920000e-01,
         2.34160000e-02,   2.99460000e-03,   3.77690000e-04,
         6.87310000e-05,   1.42550000e-05])

    Methods
    =======
    __init__(source='gc', flavor='nu_mu', channel='w', mass=1000)
        Load flux table for the given neutrino flavor.
    __call__(energy, zenith=None, interpolate=True)
        Return the flux on energy, optionally on zenith.
    integrate(zenith=None, emin=1, emax=100, **integargs)
        Integrate the flux via romberg integration.
    integrate_samples(energy, zenith=None, emin=1, emax=100)
        Integrate the flux from given samples, via simpson integration.

    Example
    =======
    >>> from km3flux import DarkMatterFlux
    >>> print(DarkMatterFlux.flavors)
    >>> flux = DarkMatterFlux(flavor='anu_mu', channel='w', mass=1000)
    >>> ene = np.geomspace(1, 100, 11)
    >>> print(flux(ene, interpolate=True))
    """

    flavors = DM_GC_FLAVORS
    channels = DM_GC_CHANNELS
    masses = DM_GC_MASSES

    def __init__(self, source="gc", flavor="nu_mu", channel="w", mass=1000):
        """
        Parameters
        ==========
        source: string, optional [default: 'gc']
            Object where the WimpWimp annihilates. Currently only 'gc'
        flavor: string, optional [default: 'nu_mu']
            Neutrino flavor. See available flavors stored in
            ``DarkMatterFlux.flavors``
        channel: string, optional [default: 'w']
            WimpWimp annihilation channel (WimpWimp -> foofoo).
            See available channels stored in ``DarkMatterFlux.channels``
        mass: int, optional [default: 1000]
            WimpWimp parent mass.
            See available masses stored in ``DarkMatterFlux.masses``
        """
        if source == "gc":
            fname = DM_GC_FILE
        else:
            raise NotImplementedError("Only GC supported so far!")
        self.mass = mass
        self.channel = channel
        self.flavor = flavor

        tab = pd.read_hdf(fname, "data")
        tab = tab[(tab.flavor == flavor) & (tab.mass_dm == mass)]
        self.flux = tab[channel].values
        self.x_energy = tab["energy"]
        self.avinterpol = splrep(
            self.x_energy,
            self.flux,
        )

    @property
    def points(self):
        return self.x_energy, self.flux

    def _check_energy(self, ene, epsilon=0.0001):
        if np.any(ene > self.mass + epsilon):
            raise ValueError("Energies exceed parent mass!")
        return ene

    def __call__(self, energy, interpolate=True):
        energy = np.atleast_1d(energy)
        energy = self._check_energy(energy)
        flux = splev(energy, self.avinterpol)
        return flux

    def _averaged(self, *args, **kwargs):
        return self(*args, **kwargs)

    def _with_zenith(self, energy, zenith, interpolate=True):
        logger.debug("Interpolate? {}".format(interpolate))
        logging.warning(
            "No zenith dependent flux implemented! " "Falling back to averaged flux."
        )
        return self._averaged(self, energy)


class AllFlavorFlux:
    """Get mixed-flavor fluxes.

    Methods
    =======
    __init__(fluxclass='Honda2015')

    __call__(energy, zenith=None, interpolate=True)
        Return the flux on energy, optionally on zenith.
    """

    fluxmodels = {
        "Honda2015": Honda2015,
        "HondaSarcevic": HondaSarcevic,
    }

    def __init__(self, fluxclass="Honda2015"):
        if isinstance(fluxclass, string_types):
            fluxclass = self.fluxmodels[fluxclass]
        self.flux_flavors = {}
        for flav in FLAVORS:
            self.flux_flavors[flav] = fluxclass(flav)

    def __call__(self, energy, zenith=None, flavor=None, mctype=None, interpolate=True):
        """mctype is ignored if flavor is passed as arg."""
        if mctype is None and flavor is None:
            raise ValueError("Specify either mctype(int) or flavor(string)")
        if flavor is None:
            mctype = pd.Series(np.atleast_1d(mctype))
            flavor = mctype.apply(pdg2name)
        flavor = np.atleast_1d(flavor)
        energy = np.atleast_1d(energy)
        out = np.zeros_like(energy)
        if zenith is not None:
            zenith = np.atleast_1d(zenith)
        for flav in np.unique(flavor):
            where = flavor == flav
            if zenith is not None:
                loczen = zenith[where]
            flux = self.flux_flavors[flav](
                energy[where], loczen, interpolate=interpolate
            )
            out[where] = flux
        return out


class WimpSimFlux(BaseFlux):
    """WimpSim neutrino flux from Sun.

    http://wimpsim.astroparticle.se/data.html

    `z: nu mass / wimp mass`

    `theta: angle towards center of sun`

    `z=E_nu/m_WIMP`

    2d layout: `d^2N/dz dtheta`

    1d: `dN/dz`

    Neutrinos at detector (icecube), the units are `cm^-2 annihilation^-1`.

    we-res-jan2013-data.tar.gz

    All energies in GeV.
    """

    def __init__(self, filename=None):
        if filename is None:
            filename = WIMPSIM_FILE
        self.tab = pd.read_hdf(filename, "/flat")

    @property
    def points(self):
        return self.x_energy, self.dnde

    def _check_energy(self, ene, epsilon=0.0001):
        if np.any(ene > self.mass + epsilon):
            raise ValueError("Energies exceed parent mass!")
        return ene

    def __call__(
        self,
        energy,
        interpolate=True,
        flavor="nu_mu",
        mass=1000.0,
        channel="w",
    ):
        self.mass = mass
        chan_num = int(DM_SUN_CHAN_TRANS_INV[channel])
        tab = self.tab[
            (self.tab.chan_num == chan_num) & (np.isclose(self.tab.mass, mass))
        ]
        dnde = tab[flavor]
        self.x_energy = tab["energy"]
        self.avinterpol = splrep(
            self.x_energy,
            dnde,
        )
        energy = np.atleast_1d(energy)
        energy = self._check_energy(energy)
        dnde = splev(energy, self.avinterpol)
        return self.dnde2flux(dnde, self.mass)

    def _averaged(self, *args, **kwargs):
        return self(*args, **kwargs)

    def _with_zenith(self, energy, zenith, interpolate=True):
        raise NotImplementedError

    @staticmethod
    def dnde2flux(dnde, mass):
        """Expects Neutrinos at detector,

        Input units are `cm^-2 annihilation^-1`.

        Output is / (m^2 sec sr GeV)
        """
        # dN/dz comes out of WS
        # y = dN/dz = MDM * (dN/dE)
        # gamm = (1e14/sec) * (100GeV/m_dm)^2 * (4*pi*r_suntoearth)
        # -> [GeV m^2 sr s/yr]
        # geom fact in wimpsim = 1/(4pi * r_sun_to_earth)
        # -> geom fact already included (if using "yields at detector" table)
        # -> gamma = 1e14 * (100/m)^2
        # i don't get the 1e9 ???
        # bah whatever
        flux = (dnde / mass) * 1e14 * 1e9 * np.square(100 / mass)
        flux *= 1e4  # cm2 -> m2
        # gseagen:
        # pointsource, so the I_0 = 1 (no 1/sr)
        return flux


def add_honda(df):
    # assume all equal (e.g. inside `groupby(flavor)`)
    flav = df.flavor.iloc[0]
    # (m^2 sec sr GeV)^-1
    honda = Honda2015(flav)(energy=df.energy, zenith=df.zenith, interpolate=True)
    df["honda"] = honda
    return df


def add_wimp(df, mass=1000.0, channel="W+ W-"):
    # assume all equal (e.g. inside `groupby(flavor)`)
    flav = df.flavor.iloc[0]
    # (m^2 sec sr GeV)^-1
    wimp = WimpSimFlux()(
        flavor=flav, energy=df.energy, mass=mass, channel=channel, interpolate=True
    )
    df["wimpsim_{}_{}".format(channel, mass)] = wimp
    return df


def apply_honda(df):
    """Add Honda flux to a dataframe."""
    return df.groupby(df.flavor).apply(add_honda)


def apply_wimp(df, **kwargs):
    """Add WimpSim flux to a dataframe."""
    return df.groupby(df.flavor).apply(add_wimp, **kwargs)
