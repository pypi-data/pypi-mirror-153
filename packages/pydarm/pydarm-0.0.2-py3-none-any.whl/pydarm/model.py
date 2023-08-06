# Copyright (C) Ethan Payne (2020)
#               Evan Goetz (2021)
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

import os
import configparser
import numpy as np
from scipy.signal import dfreqresp

from .analog import analog_aa_or_ai_filter_response
from .digital import iopdownsamplingfilters


# set up basic functions to check the type
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


class Model(object):
    """pyDARM Model class

    Represents a transfer function.

    """
    def __init__(self, config, measurement=None):
        """Initialize Model object

        Parameters
        ----------
        config : file path or string
            INI config
        measurement : string
            measurement type, corresponding to section in the config INI

        """
        self._config = None
        self.measurement = measurement
        self._load_configuration(config)

    def _load_configuration(self, config):
        """Reads configuration and load parameters

        Config can be either file path or configuration string.
        Config interface is stored in `self._config` attribute.

        Parameters
        ----------
        config : file path or string
            INI config

        """
        if self._config is None:
            self._config = configparser.ConfigParser(
                comment_prefixes=('#',), inline_comment_prefixes=('#',))

        if type(config) is dict:
            self._config.read_dict(config)
        elif os.path.exists(config):
            with open(config) as f:
                self._config.read_file(f)
        else:
            self._config.read_string(config)

        if self.measurement:
            for key, value in self._config[self.measurement].items():
                self._set_attribute(key, value)

        if 'metadata' in self._config:
            for key, value in self._config['metadata'].items():
                self._set_attribute(key, value)

        if 'interferometer' in self._config:
            for key, value in self._config['interferometer'].items():
                self._set_attribute(key, value)

    def _set_attribute(self, key, value):
        """Set Model attribute from config key/value

        """
        # Special case for module arrays
        # Sometimes (not always) keys that have the string '_modules' in their
        # name need to have a list of lists. To indicate this we use ':' in
        # the value to represent the separation of these lists
        # So, for _modules, the possibilities are:
        # - a list of 1 empty list
        # - a list of lists, where ':' separates each list
        # - a list of 1 list with values and no ':' was given in the value
        if '_modules' in key:
            if len(value) == 0:
                array = [[]]
            elif ':' in value:
                array = value.split(':')
                for index, inner_array in enumerate(array):
                    inner_array = \
                        [int(arr_entry) for arr_entry in
                         inner_array.split(',')]
                    array[index] = inner_array
            else:
                array = [[int(value_entry) for value_entry in value.split(',')]]

            value = array

        # Special case for compact measured zeros and poles of the OMC paths
        # This is like the module list of lists except instead of integers, we
        # want floats
        # - OMC paths measured zeros and poles
        elif 'omc_meas_' in key:
            if len(value) == 0:
                array = [[]]
            elif ':' in value:
                array = value.split(':')
                for index, inner_array in enumerate(array):
                    inner_array = [float(arr_entry) for arr_entry in
                                   inner_array.split(',')]
                    array[index] = inner_array
            else:
                array = [[float(value_entry) for value_entry in
                          value.split(',')]]

            value = array

        # Special case for arrays of strings that are separated by ','
        # - OMC path names
        # - OMC path analog whitening mode names
        # - sensing function anti-aliasing file names
        # - OMC compensation filter bank
        # - digital filter bank names
        elif (key == 'omc_path_names' or
                key == 'whitening_mode_names' or
                (self.measurement == 'sensing' and
                 key == 'analog_anti_aliasing_file') or
                ('omc_' in key and '_bank' in key) or
                key == 'digital_filter_bank'):
            value = value.strip(',')
            array = [str(value_entry).strip() for value_entry in
                     value.split(',')]

            value = array

        # special case if the _meas_z or _meas_p values are empty
        # Aside from the OMC paths measured zeros and poles, if any other
        # measured zeros and poles are empty, then assign an empty list
        # because we don't want an empty string
        elif (('_meas_z' in key and value == '') or
              ('_meas_p' in key and value == '')):
            value = []

        # special case for array of gain values (floats) separated by ','
        # where the gains need to be in a list, even if just one element
        # - sensing OMC path digital gains
        # - sensing OMC path gain ratios
        # - sensing balance matrix values
        # - sensing ADC gain values
        # - digital filter bank gain
        # - sensing OMC analog electronics apparent delay from high freq poles
        elif (('omc_' in key and '_gain' in key) or
              'gain_ratio' in key or 'balance_matrix' in key or
              key == 'adc_gain' or key == 'digital_filter_gain' or
              key == 'super_high_frequency_poles_apparent_delay'):
            value = [float(value_entry) for value_entry in value.split(',')]

        # Special case for True or False as values, convert string to python
        # bool
        elif 'True' in value:
            value = True
        elif 'False' in value:
            value = False

        # Check if the value is a float
        elif isfloat(value):
            value = float(value)

        # check if the configuration entry is a 2D array
        # this is more basic than the special cases above
        elif ':' in value:
            array = value.split(':')
            for index, inner_array in enumerate(array):
                inner_array = \
                    [float(arr_entry) for arr_entry in inner_array.split(',')]
                array[index] = inner_array

            value = array

        # Check if it is a 1D array
        # this is more basic than the special cases above
        elif ',' in value:
            value = value.strip(',')
            # Check if X or Y is in the string or make floats or integers
            if ('ON' in value or 'OFF' in value or 'DARM' in value or
                ('sensing' in self.measurement and
                 'analog_anti_aliasing_file' in key)):
                array = [str(value_entry).strip()
                         for value_entry in value.split(',')]
            elif '.' in value:
                array = [float(value_entry)
                         for value_entry in value.split(',')]
            else:
                array = [int(value_entry) for value_entry in value.split(',')]

            value = array

        setattr(self, key, value)

    def dpath(self, *args):
        """Return path to data file

        Path should be relative to the directory specified in the
        `cal_data_root` configuration variable, which may be
        overridden with the CAL_DATA_ROOT environment variable.  If
        not specified, paths will be assumed to be relative to the
        current working directory.

        """
        root = os.getenv('CAL_DATA_ROOT', getattr(self, 'cal_data_root', ''))
        return os.path.join(root, *args)

    def config_to_dict(self):
        """
        Return a nested dict of the model configuration. Sections are dict
        in of themselves

        Parameters
        ----------

        Returns
        -------
        out : dict
            dictionary of the model parameters
        """
        out = {}

        # loop over each of the sections
        for idx, val in enumerate(self._config.sections()):
            this_sect = {}

            # loop over each item in the section
            for idx2, val2 in enumerate(self._config.items(f'{val}')):
                this_sect[f'{val2[0]}'] = f'{val2[1]}'

            # add this section to the output
            out[f'{val}'] = this_sect

        return out

    def analog_aa_or_ai_filter_response(self, frequencies, idx=None):
        """
        Compute the analog anti-aliasing or anti-imaging filter response

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response
        idx : `int`, optional
            if multiple files provided, use an index like 0, 1, or 2 to access
            the appropriate file

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the analog AA or AI filter
        """
        if hasattr(self, 'analog_anti_aliasing_file') and idx is None:
            path = self.analog_anti_aliasing_file
        elif hasattr(self, 'analog_anti_aliasing_file'):
            path = self.analog_anti_aliasing_file[idx]
        else:
            path = self.analog_anti_imaging_file

        return analog_aa_or_ai_filter_response(self.dpath(path), frequencies)

    def digital_aa_or_ai_filter_response(self, frequencies):
        """
        Compute the digital anti-aliasing or -imaging filter response

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the digital filter
        """
        if hasattr(self, 'anti_aliasing_rate_string'):
            rate_string = self.anti_aliasing_rate_string
            method = self.anti_aliasing_method
        else:
            rate_string = self.anti_imaging_rate_string
            method = self.anti_imaging_method

        filt_ss = iopdownsamplingfilters(rate_string, method, rcg_ver=3)
        filt_zpk = filt_ss.to_zpk()

        return dfreqresp(filt_zpk, 2.0*np.pi*frequencies/2**16)[1]
