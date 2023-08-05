Changelog
=========

Unreleased Changes
------------------

1.0.1 (2022-05-31)
------------------
* last minor release before the next breaking release

1.0 (2020-04-17)
----------------
* version jump to 1.0 to clean up the versioning mess, starting over...
* km3pipe dependency removed
* fix bug in wimpsimflux choosing the wrong mass/channel

0.3 (2018-03-19)
----------------
* add wimpsim fluxes
* add convenience functions for adding fluxes to dataframes

0.2.1 (2017-11-29)
------------------

* replaces bugged (pre-histogrammed) cirelli tables with the tables
  taken directly from http://www.marcocirelli.net/PPPC4DMID.html
  (including EW corrections)

0.2.1
-----
* all fluxes now interpolated by default
* adapt DMflux to new baseclass API

0.2.1
-----
* add allflavor flux (single function call for mixed flavors)
* fix up docs, CI, packaging etc

0.2
---
* fluxes are not interpolated with cubic splines

0.12
----
* add usage example
* fix pandas handling bugs

0.11
----
* add dark matter fluxes
* cleanup file naming logic

0.10.3
------
* fix dependencies + docs

0.10.2 / 2017-03-18
-------------------
* initial versioned release
* cleanup naming logic of fluxes (e.g. HondaFlux -> Honda2015)
* add weight/aeff utils
