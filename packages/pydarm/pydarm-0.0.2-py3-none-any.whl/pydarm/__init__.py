# Copyright (C) Evan Goetz (2021)
#
# This file is part of pyDARM.
#
# pyDARM is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# pyDARM is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# pyDARM. If not, see <https://www.gnu.org/licenses/>.

from . import (sensing, actuation, utils, darm, pcal, measurement, uncertainty,
               plot, calcs)

try:
    from ._version import version as __version__
except ModuleNotFoundError:
    try:
        import setuptools_scm
        __version__ = setuptools_scm.get_version(fallback_version='?.?.?')
    except (ModuleNotFoundError, TypeError, LookupError):
        __version__ = '?.?.?'

__author__ = 'Evan Goetz <evan.goetz@ligo.org>'
__credits__ = 'Ethan Payne, Antonios Kontos, Jameson Rollins, ' \
  'Miftahul Maarif, Afif Ismail, Hsiang-Yu Huang'
