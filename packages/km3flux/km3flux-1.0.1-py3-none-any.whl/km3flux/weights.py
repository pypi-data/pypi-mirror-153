"""Utilities to compute event weights.

Most important is the make_weights function, to compute weights for mixed
flavors (e.g. neutrinos + mupage).
"""
from __future__ import division, absolute_import, print_function

import numpy as np

from km3flux.flux import e2flux
from km3flux.data import pdg2name


def nu_wgt(w2, n_gen, adjust_orca_overlap=False, energy=None):
    """Get neutrino weight, optionally adjust for ORCA energy overlap.

    Aka crazy Joao hack:

        // If energy in overlap region, divide by 2
        if(nu.E>3 && nu.E<5) weight /= 2;
    """
    wgt = w2 / n_gen
    if adjust_orca_overlap and (energy is None):
        raise ValueError(
            "When correcting for orca overlap, you need " "to specify the energy."
        )
    if adjust_orca_overlap and (energy is not None):
        overlap_mask = (3 <= energy) & (energy <= 5)
        wgt[overlap_mask] /= 2
    return wgt


def atmu_wgt(livetime_sec, fill_blank=False, fill=60.0):
    """Compute mupage weight."""
    if fill_blank:
        livetime_sec = np.full_like(livetime_sec, fill)
    out = 1 / livetime_sec
    return out


def make_weights(
    w2,
    n_gen,
    livetime_sec,
    is_neutrino,
    adjust_orca_overlap=False,
    energy=None,
    fix_atmu=False,
):
    """Generate weights for events of mixed flavor.

    This assumes that all arrays have the same length. If you have mixed
    neutrino + atmu events, just pad the unused fields (e.g. livetime for
    neutrinos, w2 for atmu) with anything, they will be ignored.

    Of course, if your data has only neutrinos/mupage, use the dedicated
    methods for them instead: `nu_wgt` and `atmu_wgt`.

    Parameters
    ==========
    w2: array-like
    n_gen: scalar or array-like
        number ov generated events *in the entire production*
        for gSeaGen, this is already n_gen.
        For GenHen, this is `n_gen * n_files`
    livetime_sec: scalar or array-like
        livetime *in seconds*
    is_neutrino: boolean array
    adjust_orca_overlap: bool, default=False
        Some Orca productions (2016) have energy overlap, between 3-5 GeV.
        If set True, you need to pass in an energy.
    energy: array, default=None
        If `adjust_orca_overlap` is set, you need to pass this.
    """
    wgt = np.ones(len(w2))
    wgt[is_neutrino] = nu_wgt(
        w2[is_neutrino],
        n_gen[is_neutrino],
        adjust_orca_overlap=adjust_orca_overlap,
        energy=energy,
    )
    wgt[~is_neutrino] = atmu_wgt(livetime_sec[~is_neutrino], fill_blank=fix_atmu)
    return wgt


def strange_flavor_to_mupage(flav, fill="mu+"):
    mask = (flav == "N/A") | (flav == "n")
    flav[mask] = fill
    return flav


def add_flavor(df, fix_strange_flavor=True):
    def t2f(row):
        return pdg2name(row["type"])

    flavor = df.apply(t2f, axis=1).astype("str")
    if fix_strange_flavor:
        flavor = strange_flavor_to_mupage(flavor)
    return flavor


def add_weights_and_fluxes(df, **kwargs):
    """Add weights + common fluxes."""
    for k in ["weight_w2", "n_events_gen", "livetime_sec", "is_neutrino", "energy"]:
        assert k in df.columns
    df["flavor"] = add_flavor(df)
    df["wgt"] = make_weights(
        df.weight_w2,
        df.n_events_gen,
        df.livetime_sec,
        df.is_neutrino,
        adjust_orca_overlap=True,
        energy=df.energy,
        **kwargs
    )
    df["e2flux"] = e2flux(df.energy)
    df = make_atmo_weight(df)
    return df


def make_atmo_weight(df_):
    df_["wgt_atmo"] = df_.wgt.copy()
    hon = df_.honda[df_.flavor != "mu+"]
    df_.loc[df_.flavor != "mu+", "wgt_atmo"] *= hon
    return df_
