#!/usr/bin/env python3
from pathlib import Path
import sys

if sys.version_info < (3, 9):
    import importlib_resources as resources
else:
    from importlib import resources


basepath = Path(resources.files(__name__))


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
