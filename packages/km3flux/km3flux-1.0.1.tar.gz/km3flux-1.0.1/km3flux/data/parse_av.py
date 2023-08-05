#!/usr/bin/env python
"""Parse the averaged tables."""

from __future__ import division, absolute_import, print_function
import six

import h5py
import numpy as np
import pandas as pd

prefix = "/home/mlotze/pkg/km3flux/km3flux/data"
fname = prefix + "/" + "all.csv"
df = pd.read_table(fname, header=0, delim_whitespace=True)
n_evts = len(df)

energy = np.unique(df["Enu"])
en_low_log = np.log10(energy) - 0.025
en_high_log = np.log10(energy) + 0.025
en_low = np.power(10, en_low_log)
en_high = np.power(10, en_high_log)
en_binlims = np.ones(energy.shape[0] + 1)
en_binlims[:-1] = en_low
en_binlims[-1] = en_high[-1]
df = df.set_index(["Enu"])

# (Energy, cos) matrices
numu = df["NuMu"].values
numubar = df["NuMubar"].values
nue = df["NuE"].values
nuebar = df["NuEbar"].values

h5 = h5py.File("data/honda2015_frejus_solarmin.h5")
h5.create_group("averaged")
# h5.create_dataset('energy', data=energy, compression="gzip", compression_opts=5)
# h5.create_dataset('energy_binlims', data=en_binlims, compression="gzip", compression_opts=5)
h5.create_dataset("averaged/nu_mu", data=numu, compression="gzip", compression_opts=5)
h5.create_dataset(
    "averaged/nu_mu_bar", data=numubar, compression="gzip", compression_opts=5
)
h5.create_dataset("averaged/nu_e", data=nue, compression="gzip", compression_opts=5)
h5.create_dataset(
    "averaged/nu_e_bar", data=nuebar, compression="gzip", compression_opts=5
)
h5.close()
