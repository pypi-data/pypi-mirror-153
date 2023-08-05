#!/usr/bin/env python
# Filename: setup.py
"""
The km3flux setup script.

"""
import os
from setuptools import setup


def read_requirements(kind):
    """Return a list of stripped lines from a file"""
    with open(os.path.join("requirements", kind + ".txt")) as fobj:
        return [l.strip() for l in fobj.readlines()]


try:
    with open("README.rst") as fh:
        long_description = fh.read()
except UnicodeDecodeError:
    long_description = "Neutrino fluxes"

setup(
    name="km3flux",
    url="http://git.km3net.de/km3py/km3flux",
    description="Neutrino fluxes",
    long_description=long_description,
    author="Moritz Lotze",
    author_email="mlotze@km3net.de",
    packages=["km3flux"],
    include_package_data=True,
    platforms="any",
    setup_requires=["setuptools_scm"],
    use_scm_version=True,
    install_requires=read_requirements("install"),
    extras_require={kind: read_requirements(kind) for kind in ["dev"]},
    python_requires=">=3.6",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
    ],
)

__author__ = "Moritz Lotze"
