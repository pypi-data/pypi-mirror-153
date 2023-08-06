# Pysimmods

This projects contains a collection of (python) simulation models for a variety of energy generation and consumption units. Most of the models were originally developed in the context of the research project iHEM (intelligent Home Energy Management) or other projects at OFFIS. Other models were developed during a student project group at the University of Oldenburg. The models are intended to be used with the co-simulation framework mosaik (https://mosaik.offis.de), but are also usable without mosaik.

Version: 0.7.4

License: LGPL

## Installation

Pysimmods requires Python >= 3.6 and is available on https://pypi.org. 
It can be installed, preferably into a virtualenv,  with 

    >>> pip install pysimmods

Alternatively, you can clone this repository with

    >>> git clone https://gitlab.com/midas-mosaik/pysimmods.git

then switch into the pysimmods folder and type

    >>> pip install -e .

## Documentation

A more comprehensive documentation is growing in the docs folder.
To build the docu, sphinx (*pip install sphinx*) is required. Simply navigate
into the docs folder and type

    >>> make html

Afterwards, navigate inside the docs/_build/html folder and double-click on the
index.html file.
