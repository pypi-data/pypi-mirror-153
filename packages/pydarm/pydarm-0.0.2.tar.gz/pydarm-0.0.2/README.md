# pyDARM

[![PyPI version](https://badge.fury.io/py/pydarm.svg)](https://badge.fury.io/py/pydarm)
[![Conda version](https://img.shields.io/conda/vn/conda-forge/pydarm.svg)](https://anaconda.org/conda-forge/pydarm/)
[![License](https://img.shields.io/pypi/l/pydarm.svg)](https://choosealicense.com/licenses/gpl-3.0/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pydarm.svg)

pyDARM is a python implementation of the LIGO DARM servo loop
model. It is used to calibrate the detector digital output into units
of differential arm length variations or spacetime strain.

If you need assistance, please review INSTALL.md and CONTRIBUTING.md
for detailed installation instructions and contribution guidelines,
respectively.

## Installation

For best results, please install from [conda-forge](https://conda-forge.org/):

```shell
conda install -c conda-forge pydarm
```

On Unix systems, you can also install directly from PyPI:

```shell
pip install pydarm
```

## Basic usage

See the [examples](examples) directory for examples of library
usage. You can use pyDARM either from `python`, `ipython`, or a
jupyter notebook, depending on your preferences.

### Command line interface

pyDARM will eventually include a command line interface to help guide through the
calibration process.  See the command help for more info:
```shell
$ python3 -m pydarm --help
```
