#!/usr/bin/env python

from km3flux.flux import DarkMatterFlux

f = DarkMatterFlux()

ene = [300, 400, 500]
print(f(ene))
