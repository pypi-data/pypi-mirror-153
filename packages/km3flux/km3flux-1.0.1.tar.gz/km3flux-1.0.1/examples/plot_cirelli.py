"""
======================
Plot DarkMatter Fluxes
======================

Plot some Fluxes from WimpWimp -> foo in the GC.
"""

# Author: Moritz Lotze <mlotze@km3net.de>
# License: BSD-3

import matplotlib.pyplot as plt
import numpy as np

from km3flux.flux import DarkMatterFlux

#############################################################################
# show available tables

print("flavors:  ", DarkMatterFlux.flavors)
print("channels: ", DarkMatterFlux.channels)
print("masses:   ", DarkMatterFlux.masses)

#############################################################################
# generate energies, logarithmically spaced, for which to compute fluxes

dm_mass = 3000
dm_channel = "w"

energy = np.geomspace(0.1, dm_mass, 201)
print(energy[:10])

#############################################################################
# load the flux table. flux is then interpolated to our energies.

dmflux = DarkMatterFlux(flavor="nu_mu", channel=dm_channel, mass=dm_mass)
print(dmflux(energy[:5]))

#############################################################################
# also grab the points from the table (used for the interpolation)
# but keep only the ones in the energy range of interest

x, y = dmflux.points
mask = x >= energy.min()
x = x[mask]
y = y[mask]

#############################################################################
# plot everything

plt.title(r"$\nu_\mu$ Flux from WimpWimp $\to$ {chan}{chan}".format(chan=dm_channel))
plt.plot(energy, dmflux(energy), label="Interpolated")
plt.plot(x, y, "s", label="From table", marker="x", markersize=2)
plt.xlabel("Energy / GeV")
plt.ylabel(r"$\frac{\mathrm{d}N}{\mathrm{d}}$ / cm$^2$ sec sr")
plt.yscale("log")
plt.xscale("log")
plt.legend()
