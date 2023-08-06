#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from setuptools import setup, find_packages

import morphonet
 
setup(
 
    name='morphonet',
 
    version="2.1.6",
 
    packages=find_packages(),
 
    author="Emmanuel Faure",
 
    author_email="api@morphonet.org",
 
    description="Python API to interact with MorphoNet",
 
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    install_requires= [ "requests", "numpy","vtk","imageio","scikit-image","scipy","vtk","nibabel"] ,

    include_package_data=True, # MANIFEST.in
 
    url='https://gitlab.inria.fr/efaure/MorphoNet',
 
    # MetaData
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers.
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Visualization",
    ],

 
)