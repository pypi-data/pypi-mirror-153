#!/usr/bin/env python
"""Utilities for effective Area computation.

All energies in GeV.
"""
from __future__ import division, absolute_import, print_function

import numpy as np


class Can(object):
    z_min = -117.2
    z_max = 139.5
    r_max = 205.402

    gen_vol = np.pi * (z_max - z_min) * np.square(r_max)

    @classmethod
    def contains(self, pos_r, pos_z):
        return (pos_r < self.r_max) & (self.z_min < pos_z) & (pos_z < self.z_max)


def gen_events():
    from glob import glob

    infiles = glob("muon-CC_3-100*")
    n_files_with_muon_cc_3_100 = len(infiles)
    normalization = {  # noqa
        "muon-CC_3-100": 600 / n_files_with_muon_cc_3_100,
    }
    muon_cc_3_100_hist = []
    can = Can()  # noqa

    for fname in infiles:
        norm = 600  # muon-cc_3-100
        for evt in fname:
            nu = evt.mc_trks[0]
            pos_r = np.sqrt(np.square(nu.pos_x) + np.square(nu.pos_y))
            if Can.contains(pos_r, nu.pos_z):
                muon_cc_3_100_hist.fill(nu.E, nu.dir_z, wgt=1 / norm)


def effective_area(self, flux, w2, ene, n_gen_total, angle_elem=4 * np.pi):
    seconds_in_a_year = 365.25 * 24 * 60 * 60
    n_gen_total = 1e6
    aeff = flux * w2 / (n_gen_total * angle_elem * seconds_in_a_year)
    return aeff
