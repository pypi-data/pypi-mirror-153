#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import setuptools

import mirmag


setuptools.setup(
    name="miRMag",
    version=mirmag.__version__,
    author="Pavel Vorozheykin",
    author_email="pavel.vorozheykin@gmail.com",
    description="Tools to process miRNA sequences, to predict them and to explore their features.",
    long_description=open(os.path.join(os.path.dirname(__file__), "README.rst")).read(),
    long_description_content_type="text/x-rst",
    url="https://github.com/Repoxitory/miRMag",
    packages=setuptools.find_packages(),
    install_requires=["anytree", "biopython", "matplotlib", "networkx", "numpy"],
    include_package_data=True
)
