from __future__ import division, absolute_import, print_function

import os.path

import numpy as np
import pandas as pd
import h5py

import km3flux


PDG2NAME = {
    12: "nu_e",
    -12: "anu_e",
    14: "nu_mu",
    -14: "anu_mu",
    16: "nu_tau",
    -16: "anu_tau",
}


NAME2PDG = {v: k for k, v in PDG2NAME.items()}


def pdg2name(pdgid):
    return PDG2NAME[pdgid]


def name2pdg(name):
    return NAME2PDG[name]


DATADIR = os.path.dirname(km3flux.__file__) + "/data"
HONDAFILE = DATADIR + "/honda2015_frejus_solarmin.h5"
WIMPSIM_FILE = DATADIR + "/wimpsim_1d.h5"
# DM_GC_FILE = DATADIR + '/gc_spectra.h5'
DM_GC_FILE = DATADIR + "/cirelli_gc.h5"
DM_GC_MASSES = {
    "100000",
    "260",
    "100",
    "5000",
    "360",
    "200",
    "10",
    "1000",
    "750",
    "30000",
    "2000",
    "50",
    "10000",
    "180",
    "500",
    "150",
    "3000",
    "25",
    "90",
    "1500",
}
DM_GC_FLAVORS = {"anu_mu", "nu_mu"}
DM_GC_CHANNELS = {"b", "mu", "tau", "w"}

DM_SUN_FILE = DATADIR + "/sun_spectra.h5"
DM_SUN_MASSES = {
    "1000",
    "100",
    "10",
    "1500",
    "176",
    "150",
    "2000",
    "200",
    "250",
    "25",
    "3000",
    "350",
    "5000",
    "500",
    "50",
    "750",
}
DM_SUN_FLAVORS = {"anu_mu", "nu_mu"}
DM_SUN_CHANNELS = {"11", "8", "5"}

DM_SUN_CHAN_TRANS = {"8": "w", "11": "tau", "5": "b"}
DM_SUN_CHAN_TRANS_INV = {v: k for k, v in DM_SUN_CHAN_TRANS.items()}
DM_SUN_CHAN_TRANS_INV.update(
    {
        "W+ W-": "8",
        "tau- tau+": "11",
        "b b-bar": "5",
    }
)

WIMPSIM_CHANNELS = {
    1: "d d-bar",
    2: "u u-bar",
    3: "s s-bar",
    4: "c c-bar",
    5: "b b-bar",
    6: "t t-bar",
    7: "glue glue",
    8: "W+ W-",
    9: "Z0 Z0",
    10: "mu- mu+",
    11: "tau- tau+",
    12: "nu_e nu_e-bar",
    13: "nu_mu nu_mu-bar",
    14: "nu_tau nu_tau-bar",
}
WIMPSIM_FLAVORS = ["nu_e", "anu_e", "nu_mu", "anu_mu", "nu_tau", "anu_tau"]
WIMPSIM_INTERESTING_CHANNELS = {8, 11, 5}
WIMPSIM_INTERESTING_CHANNELS.update(
    {WIMPSIM_CHANNELS[c] for c in WIMPSIM_INTERESTING_CHANNELS}
)
WIMPSIM_MASSES = [
    5.00e02,
    3.00e00,
    1.50e03,
    5.00e03,
    6.00e00,
    2.00e03,
    1.50e02,
    7.50e03,
    2.50e02,
    9.12e01,
    1.00e04,
    1.00e03,
    1.00e01,
    3.50e02,
    2.00e02,
    1.00e02,
    1.76e02,
    2.50e01,
    7.50e02,
    8.03e01,
    3.00e03,
    5.00e01,
]


def dm_gc_spectrum(flavor="nu_mu", channel="w", mass="100", full_lims=False):
    """Dark Matter spectra by M. Cirelli."""
    mass = str(mass)
    if mass not in DM_GC_MASSES:
        raise KeyError("Mass '{}' not available.".format(mass))
    if flavor not in DM_GC_FLAVORS:
        raise KeyError("Flavor '{}' not available.".format(flavor))
    if channel not in DM_GC_CHANNELS:
        raise KeyError("Channel '{}' not available.".format(channel))

    fname = DM_GC_FILE
    with h5py.File(fname, "r") as h5:
        gr = h5[flavor][channel][mass]
        counts = gr["entries"][:]
        bins = gr["binlims"][:]
    if not full_lims:
        bins = bins[:-1]
    return counts, bins


def dm_sun_spectrum(flavor="nu_mu", channel="w", mass="100", full_lims=False):
    """Dark Matter spectra by M. Cirelli."""
    chan_num = DM_SUN_CHAN_TRANS_INV[channel]
    mass = str(mass)
    if mass not in DM_SUN_MASSES:
        raise KeyError("Mass '{}' not available.".format(mass))
    if flavor not in DM_SUN_FLAVORS:
        raise KeyError("Flavor '{}' not available.".format(flavor))
    if chan_num not in DM_SUN_CHANNELS:
        raise KeyError("Channel '{}' not available.".format(channel))

    fname = DM_SUN_FILE
    with h5py.File(fname, "r") as h5:
        gr = h5[flavor][chan_num][mass]
        counts = gr["entries"][:]
        bins = gr["binlims"][:]
    if not full_lims:
        bins = bins[:-1]
    return counts, bins


# WIMPSIM
# n_lines_2d_per_flavor = 50
# n_z_bins_1d = 100
# z_bins_1d = np.linspace(0.005, 0.995, n_z_bins_1d)
# n_z_bins_2d = n_lines_2d_per_flavor
# z_bins_2d = np.linspace(0.01, 0.99, n_z_bins_2d)
#
# n_theta_bins = 91
# theta_first = np.linspace(0.1, 9.9, 50)
# theta_second = np.linspace(10.25, 29.75, 40)
# # last bin is >30
# theta_last = [30., ]
# theta_bins = np.concatenate([theta_first, theta_second, theta_last])
# theta_bins


def wimpsim_parse_fname(fname):
    """Parse wimpsim filename.

    Returns
    -------
    parent_mass, channel, n_dimensions
    """
    # example: './data/we-m10000-ch11-su-1D-diff-f1.dat'
    _, mass, chan, _, dim, _, _ = os.path.basename(fname).split("-")
    # 'm10000'
    mass = float(mass[1:])
    # 'ch11'
    chan = int(chan[2:])
    # '1D' / '2D'
    ndim = int(dim[0])
    return mass, chan, ndim


def wimpsim_read_file(fname):
    mass, chan, ndim = wimpsim_parse_fname(fname)
    if ndim == 1:
        df = wimpsim_read_1d(fname)
    else:
        raise NotImplementedError(
            "Only 1d tables supported, got ndim={}. Sorry!".format(ndim)
        )
    df["mass"] = mass
    df["energy"] = df["mass"] * df["z"]
    df["chan_num"] = chan
    # df['channel'] = CHANNELS[chan]
    return df


def wimpsim_read_1d(fname):
    n_z_bins_1d = 100
    z_bins_1d = np.linspace(0.005, 0.995, n_z_bins_1d)
    df = pd.read_csv(
        fname,
        delim_whitespace=True,
        comment="#",
        header=None,
    )
    df = df.T
    df.columns = WIMPSIM_FLAVORS
    df["z"] = z_bins_1d
    return df
