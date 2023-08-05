#!/usr/bin/env python

import sys

import numpy as np
import tables as tb

from ppflux.flux import atmospheric_honda_sarcevic
from km3pipe.tools import pdg2name


def ahs(mct, ene, zen):
    return atmospheric_honda_sarcevic(
        mc_type=mct,
        energy=ene,
        zenith=zen,
    )


honda_fname = "/home/mlotze/pkg/km3flux/km3flux/data/honda2015_frejus_solarmin.h5"
with tb.open_file(honda_fname) as h5:
    ebins = h5.root.energy_binlims[:]
    czbins = h5.root.cos_zen_binlims[:]

flavors = {14, -14, 12, -12}  # noqa
flux = {}
for flavor in flavors:
    flux[flavor] = np.zeros((czbins.shape[0] - 1, ebins.shape[0] - 1), dtype=float)

for i in range(ebins.shape[0] - 1):
    ene = np.mean((ebins[i], ebins[i + 1]))
    for j in range(czbins.shape[0] - 1):
        cz = np.mean((czbins[j], czbins[j + 1]))
        zen = np.arccos(cz)
        for flavor in flavors:
            flux[flavor][j, i] = ahs(flavor, ene, zen)

with tb.open_file("honda_sarcevic.h5", "a") as h5:
    for mct, flux in flux.items():
        flav = pdg2name(mct)
        group = "/honda_sarcevic"
        h5.create_carray(group, flav, obj=flux, createparents=True)
