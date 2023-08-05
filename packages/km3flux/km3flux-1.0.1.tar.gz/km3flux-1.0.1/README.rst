The km3flux Python package
==========================

.. image:: https://git.km3net.de/km3py/km3flux/badges/master/pipeline.svg
    :target: https://git.km3net.de/km3py/km3flux/pipelines

.. image:: https://git.km3net.de/km3py/km3flux/badges/master/coverage.svg
    :target: https://km3py.pages.km3net.de/km3flux/coverage

.. image:: https://api.codacy.com/project/badge/Grade/0660338483874475ba04f324de2123ec
    :target: https://www.codacy.com/manual/tamasgal/km3flux?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=KM3NeT/km3flux&amp;utm_campaign=Badge_Grade

.. image:: https://git.km3net.de/examples/km3badges/-/raw/master/docs-latest-brightgreen.svg
    :target: https://km3py.pages.km3net.de/km3flux

About
=====

KM3Flux is a collection of neutrino flux models + assorted utilities for
computing event weights.

Install
=======

This is developed on python 3.6. Lower versions (especially py2)
might or might not work.

Install the dependencies

- numpy 
- pandas
- h5py
- pytables 

In your python env, do::

    pip install km3flux

or just clone the git repository and install via ``pip install .``
