"""
===================
Plot AllFlavor Flux
===================

Demonstrate AllFlavorFlux
"""

# Author: Moritz Lotze <mlotze@km3net.de>
# License: BSD-3

from km3flux.flux import AllFlavorFlux

##############################################
# use a single function call for mixed flavors
flavor = ["nu_mu", "anu_mu", "anu_mu"]
ene = [10, 20, 30]
zen = [1, 1.5, 2]

flux = AllFlavorFlux()
print(flux(ene, zen, flavor))
