# Copyright (C) Evan Goetz (2021-2022)
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

import numpy as np
import matplotlib.pyplot as plt
import configparser
import os
from copy import deepcopy
from scipy import signal
import h5py
from gwpy.timeseries import TimeSeriesDict as tsd
from .darm import DARMModel
from .utils import (read_chain_from_hdf5, read_gpr_from_hdf5)
from .model import isfloat


class DARMUncertainty(object):

    def __init__(self, config):
        """
        Parameters
        ----------
        Returns
        -------
        """

        # Load configuration and set attributes of DARMUncertainty object
        self._config = None
        self._load_configuration(config)

        # Initialize and compute derived data products from configuration
        self.darm = DARMModel(self.model)

        # Set the sensing mcmc chain or None
        if hasattr(self, 'sensing_mcmc_file') and self.sensing_mcmc_file != '':
            self.sensing_mcmc_chain = read_chain_from_hdf5(self.sensing_mcmc_file)
        else:
            self.sensing_mcmc_chain = None

        # Set the sensing gpr or None
        if hasattr(self, 'sensing_gpr_file') and self.sensing_gpr_file != '':
            self.sensing_gpr = read_gpr_from_hdf5(self.sensing_gpr_file, 'sensing')
        else:
            self.sensing_gpr = None

        # Set the actuation mcmc list elements, which could be None
        self.actuation_mcmc_dict = {'xarm': {}, 'yarm': {}}
        for idx, arm in enumerate(self.actuation_mcmc_files_dict):
            for n, stage in enumerate(self.actuation_mcmc_files_dict[arm]):
                if self.actuation_mcmc_files_dict[arm][stage] != '':
                    self.actuation_mcmc_dict[arm][stage] = read_chain_from_hdf5(
                        self.actuation_mcmc_files_dict[arm][stage])
                else:
                    self.actuation_mcmc_dict[arm][stage] = None

        # Set the actuation gpr list elements which could be None
        self.actuation_gpr_dict = {'xarm': {}, 'yarm': {}}
        for idx, arm in enumerate(self.actuation_gpr_files_dict):
            for n, stage in enumerate(self.actuation_gpr_files_dict[arm]):
                if self.actuation_gpr_files_dict[arm][stage] != '':
                    meas = f'actuation_{arm[0]}_arm'
                    self.actuation_gpr_dict[arm][stage] = read_gpr_from_hdf5(
                        self.actuation_gpr_files_dict[arm][stage], meas)
                else:
                    self.actuation_gpr_dict[arm][stage] = None

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

        if os.path.exists(config):
            with open(config) as f:
                self._config.read_file(f)
        else:
            self._config.read_string(config)

        mcmc_files_dict = {'xarm': {}, 'yarm': {}}
        gpr_files_dict = {'xarm': {}, 'yarm': {}}
        act_delay_sample_dict = {'xarm': {}, 'yarm': {}}
        cal_line_dict = {'xarm': {}, 'yarm': {}}
        tdcf_channels_dict = {'sensing': {}, 'xarm': {}, 'yarm': {}}

        for idx, sec in enumerate(self._config):
            if sec == 'reference-model':
                setattr(self, 'model', self._config[sec]['model'])

            elif sec == 'sensing-measurement':
                setattr(self, 'sensing_mcmc_file', self._config[sec]['mcmc'])
                setattr(self, 'sensing_gpr_file', self._config[sec]['gpr'])

            # Actuation measurement files
            elif 'arm-measurement' in sec:
                arm = ''.join(sec.split('-')[0:2])
                for n, (key, value) in enumerate(self._config[sec].items()):
                    stage = key.split('_')[0].upper()
                    if 'mcmc' in key:
                        mcmc_files_dict[arm][stage] = value
                    elif 'gpr' in key:
                        gpr_files_dict[arm][stage] = value
                    else:
                        act_delay_sample_dict[arm][stage] = value

            # Calibration lines
            elif 'cal-lines' in sec:
                arm = ''.join(sec.split('-')[0:2])
                for n, (key, value) in enumerate(self._config[sec].items()):
                    cal_line_dict[arm][key] = float(value)

            # TDCF channels
            elif sec == 'sensing-tdcf' or sec == 'x-arm-tdcf' or sec == 'y-arm-tdcf':
                if 'arm' not in sec:
                    sys = 'sensing'
                else:
                    sys = ''.join(sec.split('-')[0:2])
                for n, (key, value) in enumerate(self._config[sec].items()):
                    if isfloat(value):
                        tdcf_channels_dict[sys][key] = float(value)
                    else:
                        tdcf_channels_dict[sys][key] = value

            # TDCF data type and duration
            elif sec == 'tdcf-data':
                setattr(self, 'frametype', self._config[sec]['frametype'])
                setattr(self, 'duration', float(self._config[sec]['duration']))

            elif sec == 'hoft-tdcf-data-application':
                tdcf_data_application = {}
                for n, (key, value) in enumerate(self._config[sec].items()):
                    tdcf_data_application[key] = \
                        bool(value.lower() in ('yes', 'y', 'true', 't', '1'))
                setattr(self, 'hoft_tdcf_application', tdcf_data_application)

            elif sec == 'sample-tdcf':
                sample_tdcf = {}
                for n, (key, value) in enumerate(self._config[sec].items()):
                    sample_tdcf[key] = \
                        bool(value.lower() in ('yes', 'y', 'true', 't', '1'))
                setattr(self, 'sample_tdcf', sample_tdcf)

            elif sec == 'pcal':
                pcal = {}
                for n, (key, value) in enumerate(self._config[sec].items()):
                    if (key == 'sys_err' or key == 'sys_unc') and value != '':
                        pcal[key] = float(value)
                    elif key == 'sys_err' and value == '':
                        pcal[key] = 1
                    elif key == 'sys_unc' and value == '':
                        pcal[key] = 0
                    elif key == 'sample':
                        pcal[key] = \
                            bool(value.lower() in ('yes', 'y', 'true', 't', '1'))
                setattr(self, 'pcal', pcal)

        setattr(self, 'actuation_mcmc_files_dict', mcmc_files_dict)
        setattr(self, 'actuation_gpr_files_dict', gpr_files_dict)
        setattr(self, 'act_delay_sample_dict', act_delay_sample_dict)
        setattr(self, 'cal_line_dict', cal_line_dict)
        setattr(self, 'tdcf_channels_dict', tdcf_channels_dict)

    def _channel_list_from_dict(self):
        """
        This method creates a list from the TDCF channels dict

        Parameters
        ----------
        Returns
        -------
        channels : `list`
            Channels of the TDCFs
        """
        channels = []
        for idx, (subsys, val) in enumerate(self.tdcf_channels_dict.items()):
            for idx2, (par, ch) in enumerate(self.tdcf_channels_dict[subsys].items()):
                if not isfloat(ch) and par != 'pcal_arm':
                    channels.append(ch)

        return channels

    def _query_data(self, gpstime, data=None):
        """
        Get the data from either a gwpy.timeseries.TimeSeriesDict object
        or by querying for the data

        Parameters
        ----------
        gpstime : int
            GPS time at the point of interest. queried data will be
            [gpstime-self.duration/2, gpstime+self.duration/2)
        data : `gwpy.timeseries.TimeSeriesDict` object, optional
            This is the time series data of the TDCF channels (nominal values
            and uncertainty) computed either in the CAL-CS, GDS, or DCS
            pipeline. If this is not provided, or it does not match the GPS
            time and duration, then it will be queried. A LIGO.ORG credential
            will be required

        Returns
        -------
        TimeSeriesDict
            gwpy object containing the data
        """

        # Full channel list
        chans = self._channel_list_from_dict()
        chans_copy = chans.copy()
        for idx, ch in enumerate(chans):
            chans_copy[idx] = f'{self.darm.name}:{ch}'

        # Query for data unless data is passed
        if (data is not None and
                data.span[0] == gpstime - self.duration/2 and
                data.span[1] == gpstime + self.duration/2 and
                set(chans_copy) <= set(list(data.keys()))):
            pass
        else:
            if data is not None:
                print('WARNING:')
                print('Data object passed does not match the timespan or channel list required')
            data = self._get_gwpy_data(gpstime, channels=chans,
                                       duration=self.duration,
                                       frametype=self.frametype)

        return data

    def _get_gwpy_data(self, gpstime, duration=130,
                       channels=['CAL-CS_TDEP_KAPPA_C_OUTPUT',
                                 'CAL-CS_TDEP_F_C_OUTPUT',
                                 'CAL-CS_TDEP_KAPPA_UIM_REAL_OUTPUT',
                                 'CAL-CS_TDEP_KAPPA_PUM_REAL_OUTPUT',
                                 'CAL-CS_TDEP_KAPPA_TST_REAL_OUTPUT',
                                 'CAL-CS_TDEP_PCAL_LINE1_UNCERTAINTY',
                                 'CAL-CS_TDEP_PCAL_LINE2_UNCERTAINTY',
                                 'CAL-CS_TDEP_SUS_LINE1_UNCERTAINTY',
                                 'CAL-CS_TDEP_SUS_LINE2_UNCERTAINTY',
                                 'CAL-CS_TDEP_SUS_LINE3_UNCERTAINTY'],
                       frametype='R'):
        """
        Get the data using gwpy

        Parameters
        ----------
        gpstime : int
            GPS time at the point of interest. queried data will be
            [gpstime-duration/2, gpstime+duration/2)
        duration : `int`, optional
            duration of data to query in seconds
        channels : str `list`, optional
            list of channel names without the '<IFO>:' part
        frametype : str
            frametype without the '<IFO>_' part

        Returns
        -------
        TimeSeriesDict
            gwpy object containing the data
        """

        channels_copy = channels.copy()
        for idx, ch in enumerate(channels):
            channels_copy[idx] = f'{self.darm.name}:{ch}'

        frametype = f'{self.darm.name}_{frametype}'
        gpsStart = gpstime - self.duration / 2
        gpsEnd = gpstime + self.duration / 2

        return tsd.get(channels_copy, gpsStart, gpsEnd, frametype=frametype)

    def tdcf_mean_values(self, gpstime, data=None):
        """
        Compute the mean values of the TDCF channels

        Parameters
        ----------
        gpstime : int
            GPS time at the point of interest. queried data will be
            [gpstime-duration/2, gpstime+duration/2)
        data : `gwpy.timeseries.TimeSeriesDict` object, optional
            This is the time series data of the TDCF channels (nominal values
            and uncertainty) computed either in the CAL-CS, GDS, or DCS
            pipeline. If this is not provided, or it does not match the GPS
            time and duration, then it will be queried. A LIGO.ORG credential
            will be required

        Returns
        -------
        sensing : `float`, array-like
            kappa_c and f_cc in that order; zero if no channel provided
        actuation_x_arm : `float`, array-like
            kappa_uim, kappa_pum, kappa_tst in that order; zero if no channel provided
        actuation_y_arm : `float`, array-like
            kappa_uim, kappa_pum, kappa_tst in that order; zero if no channel provided
        """
        # Query for data
        data = self._query_data(gpstime, data=data)

        sensing = np.zeros(2)
        actuation_x_arm = np.zeros(3)
        actuation_y_arm = np.zeros(3)

        # Estimated TDCF values
        for idx, (subsys, val) in enumerate(self.tdcf_channels_dict.items()):
            for idx2, (par, ch) in enumerate(self.tdcf_channels_dict[subsys].items()):
                if par == 'pcal_arm':
                    continue
                elif isfloat(ch):
                    tdcf_mean = ch
                else:
                    tdcf_mean = np.mean(data[f'{self.darm.name}:{ch}'].value)
                if subsys == 'sensing':
                    if par == 'kappa_c':
                        sensing[0] = tdcf_mean
                    elif par == 'f_cc':
                        sensing[1] = tdcf_mean
                if subsys == 'xarm':
                    if par == 'kappa_uim':
                        actuation_x_arm[0] = tdcf_mean
                    elif par == 'kappa_pum':
                        actuation_x_arm[1] = tdcf_mean
                    elif par == 'kappa_tst':
                        actuation_x_arm[2] = tdcf_mean
                if subsys == 'yarm':
                    if par == 'kappa_uim':
                        actuation_y_arm[0] = tdcf_mean
                    elif par == 'kappa_pum':
                        actuation_y_arm[1] = tdcf_mean
                    elif par == 'kappa_tst':
                        actuation_y_arm[2] = tdcf_mean

        return sensing, actuation_x_arm, actuation_y_arm

    def sample_line_uncertainty(self, gpstime, data=None):
        """
        Sample the calibration line uncertainty

        Parameters
        ----------
        gpstime : int
            GPS time at the point of interest. queried data will be
            [gpstime-duration/2, gpstime+duration/2)
        data : `gwpy.timeseries.TimeSeriesDict` object, optional
            This is the time series data of the TDCF channels (nominal values
            and uncertainty) computed either in the CAL-CS, GDS, or DCS
            pipeline. If this is not provided, or it does not match the GPS
            time and duration, then it will be queried. A LIGO.ORG credential
            will be required

        Returns
        -------
        this_cal_sensing : float
        this_cal_sus_x : `float`, array-like
        this_cal_sus_y : `float`, array-like
        """
        # Query for data
        data = self._query_data(gpstime, data=data)

        # Estimated uncertainties of lines
        for idx, (subsys, val) in enumerate(self.tdcf_channels_dict.items()):
            for idx2, (par, ch) in enumerate(self.tdcf_channels_dict[subsys].items()):
                if par == 'pcal_arm':
                    continue
                elif isfloat(ch):
                    unc_mean = ch
                else:
                    unc_mean = np.mean(data[f'{self.darm.name}:{ch}'].value)
                if subsys == 'sensing':
                    if par == 'pcal2_unc':
                        pcal2_unc = unc_mean
                        this_cal_line_pcal_2 = np.random.normal(1, pcal2_unc)
                if subsys == 'xarm':
                    if par == 'uim_unc':
                        kappa_uim_unc_x = unc_mean
                        this_cal_line_u_x = np.random.normal(1, kappa_uim_unc_x)
                    elif par == 'pum_unc':
                        kappa_pum_unc_x = unc_mean
                        this_cal_line_p_x = np.random.normal(1, kappa_pum_unc_x)
                    elif par == 'tst_unc':
                        kappa_tst_unc_x = unc_mean
                        this_cal_line_t_x = np.random.normal(1, kappa_tst_unc_x)
                    elif par == 'pcal1_unc':
                        pcal1_unc_x = unc_mean
                        this_cal_line_pcal_1_x = np.random.normal(1, pcal1_unc_x)
                if subsys == 'yarm':
                    if par == 'uim_unc':
                        kappa_uim_unc_y = unc_mean
                        this_cal_line_u_y = np.random.normal(1, kappa_uim_unc_y)
                    elif par == 'pum_unc':
                        kappa_pum_unc_y = unc_mean
                        this_cal_line_p_y = np.random.normal(1, kappa_pum_unc_y)
                    elif par == 'tst_unc':
                        kappa_tst_unc_y = unc_mean
                        this_cal_line_t_y = np.random.normal(1, kappa_tst_unc_y)
                    elif par == 'pcal1_unc':
                        pcal1_unc_y = unc_mean
                        this_cal_line_pcal_1_y = np.random.normal(1, pcal1_unc_y)

        # If no CAL line uncertainty channel was given, set scaling to be = 1
        # TODO: probably cleaner way to do this
        if 'this_cal_line_pcal_1_x' not in locals():
            this_cal_line_pcal_1_x = 1.0
        if 'this_cal_line_pcal_1_y' not in locals():
            this_cal_line_pcal_1_y = 1.0
        if 'this_cal_line_pcal_2' not in locals():
            this_cal_line_pcal_2 = 1.0
        if 'this_cal_line_u_x' not in locals():
            this_cal_line_u_x = 1.0
        if 'this_cal_line_p_x' not in locals():
            this_cal_line_p_x = 1.0
        if 'this_cal_line_t_x' not in locals():
            this_cal_line_t_x = 1.0
        if 'this_cal_line_u_y' not in locals():
            this_cal_line_u_y = 1.0
        if 'this_cal_line_p_y' not in locals():
            this_cal_line_p_y = 1.0
        if 'this_cal_line_t_y' not in locals():
            this_cal_line_t_y = 1.0

        this_cal_sensing = this_cal_line_pcal_2

        this_cal_sus_x = np.array([
            this_cal_line_u_x, this_cal_line_p_x, this_cal_line_t_x,
            this_cal_line_pcal_1_x])

        this_cal_sus_y = np.array([
            this_cal_line_u_y, this_cal_line_p_y, this_cal_line_t_y,
            this_cal_line_pcal_1_y])

        return this_cal_sensing, this_cal_sus_x, this_cal_sus_y

    @staticmethod
    def sample_pcal_unc(err=1, unc=0.005):
        """
        Sample PCAL uncertainty

        Parameters
        ----------
        err : `float`, optional
        unc : `float`, optional

        Returns
        -------
        `float`
        """
        return np.random.normal(err, unc)

    @staticmethod
    def get_model_pars(model):
        """
        Extract the main fitted parameters from MCMCs into structures

        Parameters
        ----------
        model : pydarm.darm.DARMModel object

        Returns
        -------
        sensing_pars : dict
            dictionary of the sensing parameters that the MCMC posteriors would
            impact
        act_pars : dict
            dictionary of the actuation parameters that the MCMC posteriors
            would impact
        """
        sensing_pars = {'gain': model.sensing.coupled_cavity_optical_gain,
                        'f_cc': model.sensing.coupled_cavity_pole_frequency,
                        'f_s': model.sensing.detuned_spring_frequency,
                        'Q': model.sensing.detuned_spring_q,
                        'single_pole_delay_corr':
                            model.sensing.single_pole_approximation_delay_correction}

        act_pars = {'xarm': {}, 'yarm': {}}
        if model.actuation.xarm is not None and model.actuation.xarm.uim_npa != '':
            act_pars['xarm']['UIM'] = [model.actuation.xarm.uim_npa]
            if model.actuation.xarm.uim_delay != '':
                act_pars['xarm']['UIM'].append(model.actuation.xarm.uim_delay)
        if model.actuation.xarm is not None and model.actuation.xarm.pum_npa != '':
            act_pars['xarm']['PUM'] = [model.actuation.xarm.pum_npa]
            if model.actuation.xarm.pum_delay != '':
                act_pars['xarm']['PUM'].append(model.actuation.xarm.pum_delay)
        if model.actuation.xarm is not None and model.actuation.xarm.tst_npv2 != '':
            act_pars['xarm']['TST'] = [model.actuation.xarm.tst_npv2]
            if model.actuation.xarm.tst_delay != '':
                act_pars['xarm']['TST'].append(model.actuation.xarm.tst_delay)
        if model.actuation.yarm is not None and model.actuation.yarm.uim_npa != '':
            act_pars['yarm']['UIM'] = [model.actuation.yarm.uim_npa]
            if model.actuation.yarm.uim_delay != '':
                act_pars['yarm']['UIM'].append(model.actuation.yarm.uim_delay)
        if model.actuation.yarm is not None and model.actuation.yarm.pum_npa != '':
            act_pars['yarm']['PUM'] = [model.actuation.yarm.pum_npa]
            if model.actuation.yarm.pum_delay != '':
                act_pars['yarm']['PUM'].append(model.actuation.yarm.pum_delay)
        if model.actuation.yarm is not None and model.actuation.yarm.tst_npv2 != '':
            act_pars['yarm']['TST'] = [model.actuation.yarm.tst_npv2]
            if model.actuation.yarm.tst_delay != '':
                act_pars['yarm']['TST'].append(model.actuation.yarm.tst_delay)

        return sensing_pars, act_pars

    @staticmethod
    def sample_gpr(gpr, frequencies):
        """
        Sample from the GPR instance where there are 4 parameters:
        - model configuration string (str)
        - best fit curve of the data (complex, array-like)
        - covariance matrix (float, array-like)
        - frequencies (float, array-like)

        Parameters
        ----------
        gpr : list
            GPR list instance as described above
        frequencies : `float`, array-like
            list of frequencies to sample the GPR; if this is different than
            what the GPR was computed on, then this method will interpolate
            to the new values using linear interpolation

        Returns
        -------
        this_gpr : `complex`, array-like
            sampled GPR function
        """

        rng_state = np.random.get_state()
        this_gpr_mag = np.random.multivariate_normal(np.abs(gpr[1]), gpr[2]).T
        np.random.set_state(rng_state)
        this_gpr_pha = np.random.multivariate_normal(np.angle(gpr[1]),
                                                     gpr[2]).T
        this_gpr = (this_gpr_mag * np.exp(1j * this_gpr_pha))

        # interpolate to given frequencies
        this_gpr = np.interp(frequencies, gpr[3], this_gpr)

        return this_gpr

    def sample_response(self, gpstime, frequencies, data=None):
        """
        This method samples the response function at a specific GPS time one
        at a time. Call this method multiple times in order to get an estimate
        of the overall error and uncertainty

        Parameters
        ----------
        gpstime : int
            GPS time
        frequencies : `float`, array-like
            array of frequencies to compute the response
        data : `gwpy.timeseries.TimeSeriesDict` object, optional
            This is the time series data of the TDCF channels (nominal values
            and uncertainty) computed either in the CAL-CS, GDS, or DCS
            pipeline. If this is not provided, or it does not match the GPS
            time and duration, then it will be queried. A LIGO.ORG credential
            will be required

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the sensing function
        data : `gwpy.timeseries.TimeSeriesDict` object
            object containing the queried channel data
        sensing_pars : dict
            dictionary of sesing parameters for this sample (gain, f_cc, f_s,
            Q, and tau_c (the residual delay)
        act_pars : dict
            dictionary of actuation parameters for this sample. Each entry
            for an arm and stage is a list of: gain, tau_i (the residual delay)
        this_sensing_syserr : `complex128`, array-like
            sample for this sensing function GPR
        act_syserr_dict : dict
            dictionary of samples for this arm and stage for actuation GPR
        """

        # Check that the frequencies in the GPR files are the same as what is
        # requested. If not print a warning that interpolation will be used
        if self.sensing_gpr is not None:
            if not np.array_equal(frequencies, self.sensing_gpr[3]):
                print('NOTE: chosen frequencies are not commensurate with sensing GPR. '
                      'Interpolation is used')
        for idx, arm in enumerate(self.actuation_gpr_dict):
            for n, stage in enumerate(self.actuation_gpr_dict[arm]):
                if self.actuation_gpr_dict[arm][stage] is not None:
                    if not np.array_equal(frequencies, self.actuation_gpr_dict[arm][stage][3]):
                        print(f'NOTE: chosen frequencies are not commensurate with {arm} {stage} '
                              'GPR. Interpolation is used')

        # Make copy of darm because we don't want to edit the original
        darm_copy = deepcopy(self.darm)

        # Sample sensing MCMC here; we'll be sampling the actuation MCMC later
        if self.sensing_mcmc_chain is not None:
            sensing_mcmc_idx = np.random.randint(low=0, high=len(self.sensing_mcmc_chain[4]))
            this_sensing = self.sensing_mcmc_chain[4][sensing_mcmc_idx]
        else:
            this_sensing = [darm_copy.sensing.coupled_cavity_optical_gain,
                            darm_copy.sensing.coupled_cavity_pole_frequency,
                            darm_copy.sensing.detuned_spring_frequency,
                            1/darm_copy.sensing.detuned_spring_q,
                            0]

        # Sample sensing GPR; we'll be sampling the actuation GPR later
        if self.sensing_gpr is not None:
            this_sensing_syserr = self.sample_gpr(self.sensing_gpr,
                                                  frequencies)
        else:
            this_sensing_syserr = np.ones(len(frequencies), dtype='complex128')

        # Query for data unless data is passed
        data = self._query_data(gpstime, data=data)

        # Estimated TDCF values and uncertainties of lines
        sensing_tdcf, sus_x_tdcf, sus_y_tdcf = \
            self.tdcf_mean_values(gpstime, data=data)
        this_cal_sensing, this_cal_sus_x, this_cal_sus_y = \
            self.sample_line_uncertainty(gpstime, data=data)

        # Sampled actuator TDCF values.
        # This part just scales the reference value by the sampled uncertainty
        # of the calibration lines (if requested) and the mean of the TDCF.
        # Later, we will bring in the MCMC sampling by dividing out the
        # reference value and multiply in the MCMC sample (again, if requested)
        act_pars = {'xarm': {}, 'yarm': {}}
        if self.sample_tdcf['kappa_uim']:
            if darm_copy.actuation.xarm is not None and darm_copy.actuation.xarm.uim_npa != '':
                darm_copy.actuation.xarm.uim_npa *= (this_cal_sus_x[0] *
                                                     this_cal_sus_x[3] *
                                                     sus_x_tdcf[0])
            if darm_copy.actuation.yarm is not None and darm_copy.actuation.yarm.uim_npa != '':
                darm_copy.actuation.yarm.uim_npa *= (this_cal_sus_y[0] *
                                                     this_cal_sus_y[3] *
                                                     sus_y_tdcf[0])
        else:
            if darm_copy.actuation.xarm is not None and darm_copy.actuation.xarm.uim_npa != '':
                darm_copy.actuation.xarm.uim_npa *= sus_x_tdcf[0]
            if darm_copy.actuation.yarm is not None and darm_copy.actuation.yarm.uim_npa != '':
                darm_copy.actuation.yarm.uim_npa *= sus_y_tdcf[0]
        if self.sample_tdcf['kappa_pum']:
            if darm_copy.actuation.xarm is not None and darm_copy.actuation.xarm.pum_npa != '':
                darm_copy.actuation.xarm.pum_npa *= (this_cal_sus_x[1] *
                                                     this_cal_sus_x[3] *
                                                     sus_x_tdcf[1])
            if darm_copy.actuation.yarm is not None and darm_copy.actuation.yarm.pum_npa != '':
                darm_copy.actuation.yarm.pum_npa *= (this_cal_sus_y[1] *
                                                     this_cal_sus_y[3] *
                                                     sus_y_tdcf[1])
        else:
            if darm_copy.actuation.xarm is not None and darm_copy.actuation.xarm.pum_npa != '':
                darm_copy.actuation.xarm.pum_npa *= sus_x_tdcf[1]
            if darm_copy.actuation.yarm is not None and darm_copy.actuation.yarm.pum_npa != '':
                darm_copy.actuation.yarm.pum_npa *= sus_y_tdcf[1]
        if self.sample_tdcf['kappa_tst']:
            if darm_copy.actuation.xarm is not None and darm_copy.actuation.xarm.tst_npv2 != '':
                darm_copy.actuation.xarm.tst_npv2 *= (this_cal_sus_x[2] *
                                                      this_cal_sus_x[3] *
                                                      sus_x_tdcf[2])
            if darm_copy.actuation.yarm is not None and darm_copy.actuation.yarm.tst_npv2 != '':
                darm_copy.actuation.yarm.tst_npv2 *= (this_cal_sus_y[2] *
                                                      this_cal_sus_y[3] *
                                                      sus_y_tdcf[2])
        else:
            if darm_copy.actuation.xarm is not None and darm_copy.actuation.xarm.tst_npv2 != '':
                darm_copy.actuation.xarm.tst_npv2 *= sus_x_tdcf[2]
            if darm_copy.actuation.yarm is not None and darm_copy.actuation.yarm.tst_npv2 != '':
                darm_copy.actuation.yarm.tst_npv2 *= sus_y_tdcf[2]

        # kappa_C and f_cc estimated to compute normalized to reference optical
        # response
        sensing_line_freq = self.cal_line_dict[
            f"{self.tdcf_channels_dict['sensing']['pcal_arm'].lower()}arm"
            ]['sensing']
        opt_zpk = darm_copy.sensing.optical_response(
            sensing_tdcf[1], darm_copy.sensing.detuned_spring_frequency,
            darm_copy.sensing.detuned_spring_q,
            darm_copy.sensing.is_pro_spring)
        opt = signal.freqresp(opt_zpk, 2*np.pi*sensing_line_freq)[1]

        C_CalLineP2 = darm_copy.sensing.compute_sensing(
            np.asarray([sensing_line_freq]))[0]
        EP4 = C_CalLineP2 / opt[0]

        opt *= sensing_tdcf[0]

        # TODO: need a way to confirm the EPICS records used to compute the TDCFs
        #       are the same is what is computed here
        EP5 = darm_copy.digital.compute_response(
            np.asarray([sensing_line_freq]))[0]
        # This is nominally EP6 + EP7 + EP8 since we've already multiplied in
        # the actuator TDCFs above
        A_CalLineP2 = darm_copy.actuation.compute_actuation(
            np.asarray([sensing_line_freq]))[0]
        EP9 = (darm_copy.pcal.compute_pcal_correction(
            np.asarray([sensing_line_freq]))[0] *
            np.exp(-2*np.pi*1j*sensing_line_freq/16384))
        # Compute "(d_err/x_pc)**(-1)" from reference model EPICS records and
        # mean TDCF values
        kappaC_FC_CalLineP2 = (1.0/C_CalLineP2 + EP5 * A_CalLineP2) / EP9
        # Compute "S" for this sample, T1700106-v10 eq 46
        this_S = 1.0/(EP4 * EP9 * kappaC_FC_CalLineP2*this_cal_sensing -
                      EP4 * EP5 * A_CalLineP2)

        # Sampled sensing TDCF values
        if self.sample_tdcf['kappa_c']:
            this_kappa_c = np.abs(this_S)**2/np.real(this_S)
        else:
            this_kappa_c = sensing_tdcf[0]
        if self.sample_tdcf['f_cc']:
            this_f_cc = -np.real(this_S)/np.imag(this_S)*sensing_line_freq
        else:
            this_f_cc = sensing_tdcf[1]

        # Scale sensing
        # TODO: interestingly, the f_cc value is not sampled from the MCMC,
        #       just the uncertainty of the TDCFs. Consider revisiting this
        darm_copy.sensing.coupled_cavity_optical_gain = this_kappa_c * this_sensing[0]
        darm_copy.sensing.coupled_cavity_pole_frequency = this_f_cc
        darm_copy.sensing.detuned_spring_frequency = this_sensing[2]
        darm_copy.sensing.detuned_spring_q = 1/this_sensing[3]
        darm_copy.sensing.single_pole_approximation_delay_correction += \
            this_sensing[4]

        # Sample and scale actuation from the MCMC; build syserr dict
        act_syserr_dict = {'xarm': {}, 'yarm': {}}
        arms = list(act_syserr_dict.keys())
        kappa_a_label = ['TOP', 'UIM', 'PUM', 'TST']
        output_matrix = darm_copy.actuation.darm_output_matrix_values()
        for n in range(len(output_matrix[:, 0])):
            for m in range(len(output_matrix[0, :])):
                if output_matrix[n, m] != 0:
                    arm = arms[n]
                    stage = kappa_a_label[m]

                    # Sample MCMC if a file was given
                    if self.actuation_mcmc_dict[arm][stage] is not None:
                        # get random integer from 0 to length of the MCMC chain - 1
                        actuation_mcmc_idx = np.random.randint(
                            low=0, high=len(self.actuation_mcmc_dict[arm][stage][4]))
                        mcmc_sample_gain = \
                            self.actuation_mcmc_dict[arm][stage][4][actuation_mcmc_idx][0]
                        mcmc_sample_delay = 0

                        # if sampling the residual MCMC delay
                        if self.act_delay_sample_dict[arm][stage] != '':
                            delay_stage = self.act_delay_sample_dict[arm][stage]
                            mcmc_sample_delay = \
                                self.actuation_mcmc_dict[arm][stage][4][actuation_mcmc_idx][1]
                            if (delay_stage != stage):
                                idx = np.random.randint(
                                    low=0,
                                    high=len(self.actuation_mcmc_dict[arm][delay_stage][4]))
                                mcmc_sample_delay = \
                                    self.actuation_mcmc_dict[arm][delay_stage][4][idx][1]

                        # Assignments to darm_copy object
                        if n == 0 and m == 1:
                            darm_copy.actuation.xarm.uim_npa *= (
                                mcmc_sample_gain / self.model.actuation.xarm.uim_npa)
                            darm_copy.actuation.xarm.uim_delay += mcmc_sample_delay
                        elif n == 0 and m == 2:
                            darm_copy.actuation.xarm.pum_npa *= (
                                mcmc_sample_gain / self.model.actuation.xarm.pum_npa)
                            darm_copy.actuation.xarm.pum_delay += mcmc_sample_delay
                        elif n == 0 and m == 3:
                            darm_copy.actuation.xarm.tst_npv2 *= (
                                mcmc_sample_gain / self.model.actuation.xarm.tst_npv2)
                            darm_copy.actuation.xarm.tst_delay += mcmc_sample_delay
                        elif n == 1 and m == 1:
                            darm_copy.actuation.yarm.uim_npa *= (
                                mcmc_sample_gain / self.model.actuation.yarm.uim_npa)
                            darm_copy.actuation.yarm.uim_delay += mcmc_sample_delay
                        elif n == 1 and m == 2:
                            darm_copy.actuation.yarm.pum_npa *= (
                                mcmc_sample_gain / self.model.actuation.yarm.pum_npa)
                            darm_copy.actuation.yarm.pum_delay += mcmc_sample_delay
                        elif n == 1 and m == 3:
                            darm_copy.actuation.yarm.tst_npv2 *= (
                                mcmc_sample_gain / self.model.actuation.yarm.tst_npv2)
                            darm_copy.actuation.yarm.tst_delay += mcmc_sample_delay

                    # Sample gpr if a file was given
                    if self.actuation_gpr_dict[arm][stage] is not None:
                        this_actuation_syserr = self.sample_gpr(
                            self.actuation_gpr_dict[arm][stage],
                            frequencies)
                    else:
                        this_actuation_syserr = np.ones(len(frequencies), dtype='complex128')

                    act_syserr_dict[arm][stage] = this_actuation_syserr

        # Recall this samples' parameters
        sensing_pars, act_pars = self.get_model_pars(darm_copy)

        # Since the residual sensing delay from the MCMC was included in the
        # single pole approximation delay correction (adding to it), we should
        # subtract the reference model delay correction so that we have the
        # sampled tau_c
        this_sensing_single_pole_corr = sensing_pars.pop('single_pole_delay_corr')
        sensing_pars['tau_c'] = (
            this_sensing_single_pole_corr -
            self.darm.sensing.single_pole_approximation_delay_correction)

        # Compute response
        tf = darm_copy.compute_response_function(
            frequencies, this_sensing_syserr, act_syserr_dict)

        # Pcal uncertainty
        if self.pcal['sample']:
            pcal_unc = self.sample_pcal_unc(self.pcal['sys_err'], self.pcal['sys_unc'])
        else:
            pcal_unc = self.pcal['sys_err']

        tf /= pcal_unc

        return tf, data, sensing_pars, act_pars, this_sensing_syserr, act_syserr_dict

    def nominal_response(self, gpstime, frequencies, data=None):
        """
        This method computes the response function of a model at a specified
        GPS time, and, depending on whether the time-dependent correction
        factors were applied at the time, applies those TDCFs to the model so
        that the response function is corrected for those changes at a specific
        GPS time

        Parameters
        ----------
        gpstime : int
            GPS time
        frequencies : `float`, array-like
            array of frequencies to compute the response
        data : `gwpy.timeseries.TimeSeriesDict` object, optional
            This is the time series data of the TDCF channels (nominal values
            and uncertainty) computed either in the CAL-CS, GDS, or DCS
            pipeline. If this is not provided, or it does not match the GPS
            time and duration, then it will be queried. A LIGO.ORG credential
            will be required

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the sensing function
        data : `gwpy.timeseries.TimeSeriesDict` object
            object containing the queried channel data
        """

        # Make copy of darm because we don't want to edit the original
        darm_copy = deepcopy(self.darm)

        # Query for data unless data is passed
        data = self._query_data(gpstime, data=data)

        # Estimated TDCF values
        # A reminder that the optical gain and gains of actuators are scaled by
        # a multiplicative factor whereas the cavity pole is simply modified to
        # a new value
        for idx, (subsys, val) in enumerate(self.tdcf_channels_dict.items()):
            for idx2, (par, ch) in enumerate(self.tdcf_channels_dict[subsys].items()):
                if (par in self.hoft_tdcf_application and
                        self.hoft_tdcf_application[par]):
                    if isfloat(ch):
                        tdcf_mean = ch
                    else:
                        tdcf_mean = np.mean(data[f'{darm_copy.name}:{ch}'].value)
                    if par == 'f_cc':
                        darm_copy.sensing.coupled_cavity_pole_frequency = tdcf_mean
                    elif par == 'kappa_c':
                        darm_copy.sensing.coupled_cavity_optical_gain *= tdcf_mean
                    elif par == 'kappa_uim':
                        if subsys == 'xarm':
                            darm_copy.actuation.xarm.uim_npa *= tdcf_mean
                        elif subsys == 'yarm':
                            darm_copy.actuation.yarm.uim_npa *= tdcf_mean
                    elif par == 'kappa_pum':
                        if subsys == 'xarm':
                            darm_copy.actuation.xarm.pum_npa *= tdcf_mean
                        elif subsys == 'yarm':
                            darm_copy.actuation.yarm.pum_npa *= tdcf_mean
                    elif par == 'kappa_tst':
                        if subsys == 'xarm':
                            darm_copy.actuation.xarm.tst_npv2 *= tdcf_mean
                        elif subsys == 'yarm':
                            darm_copy.actuation.yarm.tst_npv2 *= tdcf_mean

        tf = darm_copy.compute_response_function(frequencies)

        if ('pcal_sys_err' in self.hoft_tdcf_application and
                self.hoft_tdcf_application['pcal_sys_err']):
            tf /= self.pcal['sys_err']

        return tf, data

    def compute_response_uncertainty(self, gpstime, frequencies, trials=1000,
                                     data=None, save_to_file=None):
        """
        This method samples the response function uncertainty a number of times
        in order to obtain an estimate of the systematic error and associated
        uncertainty. This is often referred to as the "error budget"

        The values are R_sample / R_nominal, meaning they are a multiplicative
        correction factor to the calibrated data in order to obtain the "true"
        response

        Parameters
        ----------
        gpstime : int
            GPS time
        frequencies : `float`, array-like
            array of frequencies to compute the response
        trials : `int`, optional
            number of times to sample the response
        data : `gwpy.timeseries.TimeSeriesDict` object, optional
            This is the time series data of the TDCF channels (nominal values
            and uncertainty) computed either in the CAL-CS, GDS, or DCS
            pipeline. If this is not provided, or it does not match the GPS
            time and duration, then it will be queried. A LIGO.ORG credential
            will be required

        Returns
        -------
        response_samples : list of `complex128`, array-like
            list of response transfer function samples
        """

        nominal_response, data = self.nominal_response(gpstime, frequencies,
                                                       data)

        # Store data for each of the samples so that it can be saved to an
        # HDF5 file
        response_samples = np.zeros((trials, len(frequencies)), dtype='complex128')
        sensing_syserr_samples = np.zeros((trials, len(frequencies)), dtype='complex128')
        act_pars_samples = {'xarm': {}, 'yarm': {}}
        act_syserr_samples = {'xarm': {}, 'yarm': {}}
        for i, arm in enumerate(self.actuation_mcmc_dict.keys()):
            for j, stage in enumerate(self.actuation_mcmc_dict[arm].keys()):
                act_pars_samples[arm][stage] = np.zeros((trials, 2))
        for i, arm in enumerate(self.actuation_gpr_dict.keys()):
            for j, stage in enumerate(self.actuation_gpr_dict[arm].keys()):
                act_syserr_samples[arm][stage] = np.zeros((trials, len(frequencies)),
                                                          dtype='complex128')

        # Loop over the number of trials
        for n in range(trials):
            (response, data, sens_pars, act_pars, sensing_syserr_samples[n, :],
             act_syserr_dict) = self.sample_response(
                 gpstime, frequencies, data=data)

            response_samples[n, :] = response / nominal_response

            if n == 0:
                sensing_pars_samples = np.zeros((trials, len(sens_pars)))

            sensing_pars_samples[n, :] = list(sens_pars.values())

            for i, arm in enumerate(act_pars.keys()):
                for j, stage in enumerate(act_pars[arm].keys()):
                    act_pars_samples[arm][stage][n, :] = act_pars[arm][stage]
            for i, arm in enumerate(act_syserr_dict.keys()):
                for j, stage in enumerate(act_syserr_dict[arm].keys()):
                    act_syserr_samples[arm][stage][n, :] = act_syserr_dict[arm][stage]

        # Save the draws to a file if requested
        # TODO: do we need to use astropy.table.Table in HDF5? The O3 version used it
        # TODO: what else is required to be saved into these files? The O3
        #       version had a lot but it wasn't clear if everything was needed
        if save_to_file is not None:
            if (os.path.splitext(save_to_file) == '.h5' or
                    os.path.splitext(save_to_file) == '.hdf5'):
                with h5py.File(save_to_file, 'r') as f:
                    f.create_dataset('config', data=self._config)
                    f.create_dataset('deltaR/freq', data=frequencies)
                    f.create_dataset('deltaR/draws', data=response_samples)
                    f.create_dataset('CalParams/sensing', data=sensing_pars_samples)
                    f.create_dataset('GPR/sensing', data=sensing_syserr_samples)
                    for i, arm in enumerate(act_pars_samples.keys()):
                        for j, stage in enumerate(act_pars_samples[arm].keys()):
                            f.create_dataset(f'CalParams/{arm}/{stage}',
                                             data=act_pars_samples[arm][stage])
                    for i, arm in enumerate(act_syserr_samples.keys()):
                        for j, stage in enumerate(act_syserr_samples[arm].keys()):
                            f.create_dataset(f'GPR/{arm}/{stage}',
                                             data=act_syserr_samples[arm][stage])
            elif (os.path.splitext(save_to_file) == '.txt'):
                response_mag_quant, response_pha_quant = \
                    self.response_quantiles(response_samples)
                save_txt_response = np.vstack((
                    frequencies,
                    response_mag_quant[1, :], response_pha_quant[1, :],
                    response_mag_quant[0, :], response_pha_quant[0, :],
                    response_mag_quant[2, :], response_pha_quant[2, :])).T
                header = "{:12} {:21} {:21} {:21} {:21} {:21} {:21}".format(
                    'Frequency', 'Median mag', 'Phase (Rad)',
                    '16th percentile mag', '16th percentile phase',
                    '84th percentile mag', '84th percentile phase')
                np.savetxt(save_to_file, save_txt_response, fmt='%+1.7e', header=header)

        return response_samples

    @staticmethod
    def response_quantiles(response_samples, quantiles=[16, 50, 84]):
        """
        Calculate the quantiles of response uncertainty samples

        Parameters
        ----------
        response_samples : `complex128`, list
            list of arrays of ration of sampled responses to nominal response
        quantiles : `float`, list, optional
            list of quantiles desired to be computed

        Returns
        -------
        response_mag_quant : `float`, array-like
            2-d array of length(quantiles) x length(resposne_samples) giving
            magnitude quantiles
        response_pha_quant : `float`, array-like
            2-d array of length(quantiles) x length(resposne_samples) giving
            phase quantiles in radians
        """
        # Set up arrays
        response_mag_quant = np.zeros((len(quantiles), len(response_samples[0])))
        response_pha_quant = np.zeros((len(quantiles), len(response_samples[0])))

        # Calculate the quantiles requested
        for i in range(len(quantiles)):
            response_mag_quant[i, :] = np.percentile(
                np.abs(response_samples), quantiles[i], axis=0)
            response_pha_quant[i, :] = np.percentile(
                np.angle(response_samples), quantiles[i], axis=0)

        return response_mag_quant, response_pha_quant

    @staticmethod
    def plot_response_samples(frequencies, RRMag, RRPha,
                              response_mag_quant, response_pha_quant,
                              filename=None):
        """
        Placeholder plotting for response function samples

        TODO: replace this with standard pyDARM plotting

        Parameters
        ----------
        frequencies : `float`, array-like
        RRMag : `float`, list of arrays
        RRPha : `float`, list of arrays
        response_mag_quant : `float`, array-like
        response_pha_quant : `float`, array-like

        Returns
        -------
        """

        h = plt.figure(figsize=(20, 15))
        f1 = h.add_subplot(211)
        f2 = h.add_subplot(212)
        legendLabel = '50 p/m 68/2 %'
        for i in range(len(RRMag)):
            f1.semilogx(frequencies, 100 * (RRMag[i, :]-1.0))
            f2.semilogx(frequencies, 180 / np.pi * (RRPha[i, :]))
        for j in range(len(response_mag_quant)):
            f1.semilogx(frequencies, 100 * (response_mag_quant[j, :]-1.0), label=legendLabel)
            f2.semilogx(frequencies, 180 / np.pi * (response_pha_quant[j, :]), label=legendLabel)
        f1.set_xlabel('Frequency [Hz]')
        f2.set_xlabel('Frequency [Hz]')
        f1.set_ylabel('Magnitude')
        f2.set_ylabel('Phase [deg.]')
        if filename is not None:
            plt.savefig(filename)
