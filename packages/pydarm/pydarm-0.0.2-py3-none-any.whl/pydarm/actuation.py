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

import numpy as np
from scipy import signal, io

from .utils import digital_delay_filter
from .utils import compute_digital_filter_response, freqrespZPK
from .model import Model


class ActuationModel(Model):
    """
    An arm actuation model object

    This is a class to set up the model for the actuation function from a
    configuration file with all the information about where the data is stored

    Parameters
    ----------

    Returns
    -------


    """

    def __init__(self, config, measurement):
        super().__init__(config, measurement=measurement)

        # TODO need some way of validating the configuration file is
        # appropriate

    def analog_driver_response(self, frequencies):
        """
        The transfer function of the analog driver electronics. By default,
        the output will be a dictionary for UIM, PUM, and TST with
        dictionaries for each containing the quadrants UL, LL, UR, LR.
        Transfer functions are unity with zero phase unless the params
        file/string contains a <uim|pum|tst>_driver_meas_<z|p>_<ul|ll|ur|lr>
        for the particular quadrant and values

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        out : dict, `complex128`, array-like
            transfer function response of the uncompensated driver electronics
        """

        out = {'UIM': {'UL': np.ones(len(frequencies), dtype='complex128'),
                       'LL': np.ones(len(frequencies), dtype='complex128'),
                       'UR': np.ones(len(frequencies), dtype='complex128'),
                       'LR': np.ones(len(frequencies), dtype='complex128')},
               'PUM': {'UL': np.ones(len(frequencies), dtype='complex128'),
                       'LL': np.ones(len(frequencies), dtype='complex128'),
                       'UR': np.ones(len(frequencies), dtype='complex128'),
                       'LR': np.ones(len(frequencies), dtype='complex128')},
               'TST': {'UL': np.ones(len(frequencies), dtype='complex128'),
                       'LL': np.ones(len(frequencies), dtype='complex128'),
                       'UR': np.ones(len(frequencies), dtype='complex128'),
                       'LR': np.ones(len(frequencies), dtype='complex128')}}

        for i, stage in enumerate(out.keys()):
            for j, quadrant in enumerate(out[stage].keys()):
                if (hasattr(self, f'{stage.lower()}_driver_meas_z_{quadrant.lower()}') and
                        hasattr(self, f'{stage.lower()}_driver_meas_p_{quadrant.lower()}')):
                    zeros = np.asarray(
                        getattr(self, f'{stage.lower()}_driver_meas_z_{quadrant.lower()}'))
                    poles = np.asarray(
                        getattr(self, f'{stage.lower()}_driver_meas_p_{quadrant.lower()}'))
                    gain = np.prod(2.0*np.pi*poles) / np.prod(2.0*np.pi*zeros)
                    model = signal.ZerosPolesGain(
                        -2.0*np.pi*zeros,
                        -2.0*np.pi*poles,
                        gain)
                    tf = signal.freqresp(model, 2.0*np.pi*frequencies)[1]
                    out[stage][quadrant] = tf

        return out

    def uim_dc_gain_Apct(self):
        """
        This computes the UIM DC gain in units of amps / count
        """

        return 4 * 0.25 * self.dac_gain * self.uim_driver_dc_trans_apv

    def pum_dc_gain_Apct(self):
        """
        This computes the PUM DC gain in units of amps / count
        """

        return 4 * 0.25 * self.dac_gain * self.pum_driver_dc_trans_apv * \
            self.pum_coil_outf_signflip

    def tst_dc_gain_V2pct(self):
        """
        This computes the TST DC gain in units of volts**2 / count
        """

        return 4 * 0.25 * self.dac_gain * self.tst_driver_dc_gain_vpv_lv * \
            2 * self.tst_driver_dc_gain_vpv_hv * \
            self.actuation_esd_bias_voltage

    def uim_dc_gain_Npct(self):
        """
        This computes the UIM DC gain in units of Newtons / count
        """

        return self.uim_dc_gain_Apct() * self.uim_npa

    def pum_dc_gain_Npct(self):
        """
        This computes the PUM DC gain in units of Newtons / count
        """

        return self.pum_dc_gain_Apct() * self.pum_npa

    def tst_dc_gain_Npct(self):
        """
        This computes the TST DC gain in units of Newtons / count
        """

        return self.tst_dc_gain_V2pct() * self.tst_npv2

    def sus_digital_filters_response(self, frequencies):
        """
        The transfer function of the SUS digital filters

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        uim_digital_filter_response : `complex128`, array-like
            transfer function response of the digital filters in the UIM path
        pum_digital_filter_response : `complex128`, array-like
            transfer function response of the digital filters in the PUM path
        tst_digital_filter_response : `complex128`, array-like
            transfer function response of the digital filters in the TST path
        """

        # Start with TST stage filters
        tst_isc_inf_filter_response, pfilt = \
            compute_digital_filter_response(
                self.dpath(self.sus_filter_file),
                self.tst_isc_inf_bank, self.tst_isc_inf_modules[0],
                self.tst_isc_inf_gain, frequencies)
        tst_lock_filter_response = \
            compute_digital_filter_response(
                self.dpath(self.sus_filter_file),
                self.tst_lock_bank, self.tst_lock_modules[0],
                self.tst_lock_gain, frequencies, pfilt)[0]
        tst_drive_align_filter_response = \
            compute_digital_filter_response(
                self.dpath(self.sus_filter_file),
                self.tst_drive_align_bank, self.tst_drive_align_modules[0],
                self.tst_drive_align_gain, frequencies, pfilt)[0]
        tst_digital_filter_response = tst_isc_inf_filter_response * \
            tst_lock_filter_response * tst_drive_align_filter_response

        # The PUM stage feedback is to the same SUS as TST stage, so
        # we can reuse the pfilt variable from above
        pum_lock_filter_response = \
            compute_digital_filter_response(
                self.dpath(self.sus_filter_file),
                self.pum_lock_bank, self.pum_lock_modules[0],
                self.pum_lock_gain, frequencies, pfilt)[0]
        pum_drive_align_filter_response = \
            compute_digital_filter_response(
                self.dpath(self.sus_filter_file),
                self.pum_drive_align_bank, self.pum_drive_align_modules[0],
                self.pum_drive_align_gain, frequencies, pfilt)[0]
        pum_digital_filter_response = tst_isc_inf_filter_response * \
            tst_lock_filter_response * pum_lock_filter_response * \
            pum_drive_align_filter_response

        # The UIM stage feedback is to the same SUS as PUM stage, so
        # we can reuse the pfilt variable from above
        uim_lock_filter_response = \
            compute_digital_filter_response(
                self.dpath(self.sus_filter_file),
                self.uim_lock_bank, self.uim_lock_modules[0],
                self.uim_lock_gain, frequencies, pfilt)[0]
        uim_drive_align_filter_response = \
            compute_digital_filter_response(
                self.dpath(self.sus_filter_file),
                self.uim_drive_align_bank, self.uim_drive_align_modules[0],
                self.uim_drive_align_gain, frequencies, pfilt)[0]
        uim_digital_filter_response = tst_isc_inf_filter_response * \
            tst_lock_filter_response * pum_lock_filter_response * \
            uim_lock_filter_response * uim_drive_align_filter_response

        return uim_digital_filter_response, \
            pum_digital_filter_response, \
            tst_digital_filter_response

    def sus_digital_compensation_response(self, frequencies):
        """
        The transfer function of the SUS compensation filters for driver
        electronics. By default, the output will be a dictionary for UIM,
        PUM, and TST with dictionaries for each containing the quadrants
        UL, LL, UR, LR. Transfer functions are unity with zero phase unless
        the params file/string contains:
        <uim|pum|tst>_compensation_filter_bank_<ul|ll|ur|lr> with a name;
        <uim|pum|tst>_compensation_filter_modules_in_use_<ul|ll|ur|lr> with
        list of modules turned on; and
        <uim|pum|tst>_compensation_filter_gain_<ul|ll|ur|lr>

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        out : dict, `complex128`, array-like
            transfer function response of the digital compensation filters in
            each path and quadrant
        """

        out = {'UIM': {'UL': np.ones(len(frequencies), dtype='complex128'),
                       'LL': np.ones(len(frequencies), dtype='complex128'),
                       'UR': np.ones(len(frequencies), dtype='complex128'),
                       'LR': np.ones(len(frequencies), dtype='complex128')},
               'PUM': {'UL': np.ones(len(frequencies), dtype='complex128'),
                       'LL': np.ones(len(frequencies), dtype='complex128'),
                       'UR': np.ones(len(frequencies), dtype='complex128'),
                       'LR': np.ones(len(frequencies), dtype='complex128')},
               'TST': {'UL': np.ones(len(frequencies), dtype='complex128'),
                       'LL': np.ones(len(frequencies), dtype='complex128'),
                       'UR': np.ones(len(frequencies), dtype='complex128'),
                       'LR': np.ones(len(frequencies), dtype='complex128')}}

        pfilt = None
        for i, stage in enumerate(out.keys()):
            for j, quadrant in enumerate(out[stage].keys()):
                if hasattr(self, f'{stage.lower()}_compensation_filter_bank_{quadrant.lower()}'):
                    bank = getattr(self,
                                   f'{stage.lower()}_compensation_filter_bank_{quadrant.lower()}')
                if hasattr(
                        self,
                        f'{stage.lower()}_compensation_filter_modules_in_use_{quadrant.lower()}'):
                    modules = getattr(
                        self,
                        f'{stage.lower()}_compensation_filter_modules_in_use_{quadrant.lower()}')
                if hasattr(self, f'{stage.lower()}_compensation_filter_gain_{quadrant.lower()}'):
                    gain = getattr(
                        self, f'{stage.lower()}_compensation_filter_gain_{quadrant.lower()}')

                if ('bank' in locals() and len(bank) > 0 and
                        'modules' in locals() and 'gain' in locals()):
                    tf, pfilt = compute_digital_filter_response(
                        self.dpath(self.sus_filter_file),
                        bank, modules, gain, frequencies, pfilt)

                    out[stage][quadrant] *= tf
                    del bank, gain, modules

        return out

    def combine_sus_quadrants(self, frequencies):
        """
        Combine the digital and analog paths for the SUS quadrants on a
        per-stage and per-path basis. Meaning
        (0.25 x UIM UL digital x UIM UL analog +
        0.25 x UIM LL digital x UIM LL analog + ...) and so on for each
        stage

        Parameters
        ----------
        sus_dict_digital : dict, `complex`, array-like
            dictionary of digital compensation transfer function values
        sus_dict_analog : dict, `complex`, array-like
            dictionary of analog driver transfer function values

        Returns
        -------
        uim : dict, `complex128`, array-like
            transfer function response of the digital compensation filters in
            each path and quadrant for the UIM
        pum : dict, `complex128`, array-like
            transfer function response of the digital compensation filters in
            each path and quadrant for the PUM
        tst : dict, `complex128`, array-like
            transfer function response of the digital compensation filters in
            each path and quadrant for the TST
        """

        sus_dict_digital = self.sus_digital_compensation_response(frequencies)
        sus_dict_analog = self.analog_driver_response(frequencies)

        uim = 0.25 * (
            sus_dict_digital['UIM']['UL'] * sus_dict_analog['UIM']['UL'] +
            sus_dict_digital['UIM']['LL'] * sus_dict_analog['UIM']['LL'] +
            sus_dict_digital['UIM']['UR'] * sus_dict_analog['UIM']['UR'] +
            sus_dict_digital['UIM']['LR'] * sus_dict_analog['UIM']['LR'])
        pum = 0.25 * (
            sus_dict_digital['PUM']['UL'] * sus_dict_analog['PUM']['UL'] +
            sus_dict_digital['PUM']['LL'] * sus_dict_analog['PUM']['LL'] +
            sus_dict_digital['PUM']['UR'] * sus_dict_analog['PUM']['UR'] +
            sus_dict_digital['PUM']['LR'] * sus_dict_analog['PUM']['LR'])
        tst = 0.25 * (
            sus_dict_digital['TST']['UL'] * sus_dict_analog['TST']['UL'] +
            sus_dict_digital['TST']['LL'] * sus_dict_analog['TST']['LL'] +
            sus_dict_digital['TST']['UR'] * sus_dict_analog['TST']['UR'] +
            sus_dict_digital['TST']['LR'] * sus_dict_analog['TST']['LR'])

        return uim, pum, tst

    @staticmethod
    def matlab_force2length_response(suspension_file, frequencies):
        """
        Load the ZPK output from the matlab exported values and output a
        frequency response. This function expects variables in a .mat file to
        be UIMz, UIMp, UIMk, PUMz, PUMp, PUMk, TSTz, TSTp, and TSTk

        Parameters
        ----------
        suspension_file: `str`
            path and filename to .mat file that has the ZPK arrays
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        UIM_F2L_freqresp : `complex128`, array-like
            transfer function response of the UIM stage
        PUM_F2L_freqresp : `complex128`, array-like
            transfer function response of the PUM stage
        TST_F2L_freqresp : `complex128`, array-like
            transfer function response of the TST stage
        """

        mat = io.loadmat(suspension_file)
        UIM_F2L = signal.ZerosPolesGain(mat['UIMz'][:, 0], mat['UIMp'][:, 0],
                                        mat['UIMk'][0, 0])
        PUM_F2L = signal.ZerosPolesGain(mat['PUMz'][:, 0], mat['PUMp'][:, 0],
                                        mat['PUMk'][0, 0])
        TST_F2L = signal.ZerosPolesGain(mat['TSTz'][:, 0], mat['TSTp'][:, 0],
                                        mat['TSTk'][0, 0])
        UIM_F2L_freqresp = freqrespZPK(UIM_F2L, 2.0*np.pi*frequencies)
        PUM_F2L_freqresp = freqrespZPK(PUM_F2L, 2.0*np.pi*frequencies)
        TST_F2L_freqresp = freqrespZPK(TST_F2L, 2.0*np.pi*frequencies)

        return UIM_F2L_freqresp, PUM_F2L_freqresp, TST_F2L_freqresp

    def digital_out_to_displacement(self, frequencies):
        """
        This computes the transfer function from the output of the drive align
        filter bank of each stage to displacement of the test mass

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        uim_response : `complex128`, array-like
            transfer function response of the UIM stage
        pum_response : `complex128`, array-like
            transfer function response of the PUM stage
        tst_response : `complex128`, array-like
            transfer function response of the TST stage
        """

        # SUS to IOP and IOP to analog digital time delays (see G1601472)
        sus_to_iop_delay_response = signal.dfreqresp(
            digital_delay_filter(1, 16384), 2.0*np.pi*frequencies/16384)[1]
        iop_to_analog_delay_response = signal.dfreqresp(
            digital_delay_filter(4, 65536), 2.0*np.pi*frequencies/65536)[1]

        # digital anti-imaging filter
        digital_ai_filter_response = \
            self.digital_aa_or_ai_filter_response(frequencies)

        # analog anti-imaging filter response
        analog_ai_filter_response = \
            self.analog_aa_or_ai_filter_response(frequencies)

        # Combine analog driver electronics for each quadrant with the
        # digital compensation for each quadrant, and then take the mean
        # of the four quadrants for each stage
        uim_tf, pum_tf, tst_tf = self.combine_sus_quadrants(frequencies)

        # Analog force to length response for each stage from Matlab
        sus_file = self.dpath(self.suspension_file)
        [uim_f2l_response,
         pum_f2l_response,
         tst_f2l_response] = self.matlab_force2length_response(sus_file,
                                                               frequencies)

        # Unknown overall time delay
        unknown_actuation_delay = np.exp(-2.0*np.pi*1j *
                                         self.unknown_actuation_delay *
                                         frequencies)

        # Independent time delays
        if hasattr(self, 'uim_delay') and self.uim_delay != '':
            uim_delay_tf = np.exp(-2.0*np.pi*1j*self.uim_delay*frequencies)
        else:
            uim_delay_tf = 1
        if hasattr(self, 'pum_delay') and self.pum_delay != '':
            pum_delay_tf = np.exp(-2.0*np.pi*1j*self.pum_delay*frequencies)
        else:
            pum_delay_tf = 1
        if hasattr(self, 'tst_delay') and self.tst_delay != '':
            tst_delay_tf = np.exp(-2.0*np.pi*1j*self.tst_delay*frequencies)
        else:
            tst_delay_tf = 1

        # Everything together now!
        tst_response = (tst_tf *
                        sus_to_iop_delay_response *
                        iop_to_analog_delay_response *
                        digital_ai_filter_response *
                        analog_ai_filter_response *
                        self.tst_dc_gain_Npct() *
                        tst_f2l_response *
                        unknown_actuation_delay *
                        tst_delay_tf)
        pum_response = (pum_tf *
                        sus_to_iop_delay_response *
                        iop_to_analog_delay_response *
                        digital_ai_filter_response *
                        analog_ai_filter_response *
                        self.pum_dc_gain_Npct() *
                        pum_f2l_response *
                        unknown_actuation_delay *
                        pum_delay_tf)
        uim_response = (uim_tf *
                        sus_to_iop_delay_response *
                        iop_to_analog_delay_response *
                        digital_ai_filter_response *
                        analog_ai_filter_response *
                        self.uim_dc_gain_Npct() *
                        uim_f2l_response *
                        unknown_actuation_delay *
                        uim_delay_tf)

        return uim_response, pum_response, tst_response

    def drivealign_to_displacement(self, frequencies):
        """
        This computes the transfer function from the input of the drive align
        filter bank of each stage to displacement of the test mass.

        This is particularly useful for computing EPICS records

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        uim_response : `complex128`, array-like
            transfer function response of the UIM stage
        pum_response : `complex128`, array-like
            transfer function response of the PUM stage
        tst_response : `complex128`, array-like
            transfer function response of the TST stage
        """

        # Digital out to displacement of the TST stage by each of the
        # SUS stages
        [uim_response,
         pum_response,
         tst_response] = self.digital_out_to_displacement(frequencies)

        # Need to add in the DRIVEALIGN bank for each stage
        # Like before, we can reuse the pfilt variable if the preceeding
        # stage feedback goes to the same SUS
        tst_drive_align_filter_response, pfilt = \
            compute_digital_filter_response(
                self.dpath(self.sus_filter_file),
                self.tst_drive_align_bank, self.tst_drive_align_modules[0],
                self.tst_drive_align_gain, frequencies)
        pum_drive_align_filter_response = \
            compute_digital_filter_response(
                self.dpath(self.sus_filter_file),
                self.pum_drive_align_bank, self.pum_drive_align_modules[0],
                self.pum_drive_align_gain, frequencies, pfilt)[0]
        uim_drive_align_filter_response = \
            compute_digital_filter_response(
                self.dpath(self.sus_filter_file),
                self.uim_drive_align_bank, self.uim_drive_align_modules[0],
                self.uim_drive_align_gain, frequencies)[0]

        uim_response *= uim_drive_align_filter_response
        pum_response *= pum_drive_align_filter_response
        tst_response *= tst_drive_align_filter_response

        return uim_response, pum_response, tst_response

    def known_actuation_terms_for_measurement(self, frequencies):
        """
        This computes the transfer function from the input of the drive align
        filter bank of each stage to displacement of the test mass, everything
        but N/(drive unit); either amps or volts**2. This also includes the
        DARM feedback sign of the arm the measurement is taken on since we
        read out the measurment at DARM

        This is used for dividing out everything from measurements to establish
        the actuator gain in units of N/(drive unit)

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        uim_response : `complex128`, array-like
            transfer function response of the UIM stage, everything but N/ct
        pum_response : `complex128`, array-like
            transfer function response of the PUM stage, everything but N/ct
        tst_response : `complex128`, array-like
            transfer function response of the TST stage, everything but N/ct
        """

        [uim_response,
         pum_response,
         tst_response] = self.drivealign_to_displacement(frequencies)

        uim_response *= self.darm_feedback_sign * \
            (self.uim_dc_gain_Apct()/self.uim_dc_gain_Npct())
        pum_response *= self.darm_feedback_sign * \
            (self.pum_dc_gain_Apct()/self.pum_dc_gain_Npct())
        tst_response *= self.darm_feedback_sign * \
            (self.tst_dc_gain_V2pct()/self.tst_dc_gain_Npct())

        return uim_response, pum_response, tst_response

    def compute_actuation_single_stage(self, frequencies, stage='TST'):
        """
        Compute the actuation function transfer function for a single stage
        (see G1501518). This transfer function is from DARM_CTRL to meters
        sensed by the IFO. Note that the sign of the DARM_ERR signal is
        dependent upon which arm is under control.

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the actuation function
        """

        # Digital output to TST displacement
        # Note that no feedback or output matrix values are applied here
        [uim_response,
         pum_response,
         tst_response] = self.digital_out_to_displacement(frequencies)
        if stage == 'UIM' or stage == 'L1':
            sus_response = uim_response
        elif stage == 'PUM' or stage == 'L2':
            sus_response = pum_response
        elif stage == 'TST' or stage == 'L3':
            sus_response = tst_response
        else:
            raise ValueError('stage must be UIM, PUM, TST, L1, L2, or L3')

        # All SUS digital filters
        [uim_digital_filter_response,
         pum_digital_filter_response,
         tst_digital_filter_response] = self.sus_digital_filters_response(
             frequencies)
        if stage == 'UIM' or stage == 'L1':
            digital_filter_response = uim_digital_filter_response
        elif stage == 'PUM' or stage == 'L2':
            digital_filter_response = pum_digital_filter_response
        else:
            digital_filter_response = tst_digital_filter_response

        # OMC to SUS digital time delay (see G1601472)
        # Note that SUS to IOP, IOP to analog, and unknown delays already
        # applied
        omc_to_sus_delay_response = signal.dfreqresp(
            digital_delay_filter(1, 16384), 2.0*np.pi*frequencies/16384)[1]

        sus_response *= digital_filter_response*omc_to_sus_delay_response

        # The response on DARM will depend on which arm is being actuated
        # by the DARM feedback
        sus_response *= self.darm_feedback_sign

        # Everything *above* here is modelling the physical actuator that we
        # have. However, the calibration group's convention is that A in their
        # loop drawings is minus the physical actuator (which allows the
        # explicit writing of the minus sign in the loop drawing to indicate
        # negative feedback). Ideally we'd just put
        # A = -1 * (TOP + UIM + PUM + TST),
        # but the actuation products below (which are used for other things
        # downstream) are expecting to receive minus of each stage of the
        # physical actuator. So, we multiply every stage by -1, and then sum
        # them up, and the result will be that A is negative of the physical
        # actuator. JCD_26Mar2019
        # See more details in T1800456.
        sus_response *= -1

        return sus_response


class DARMActuationModel(Model):
    """
    An DARM actuation model object

    This is a class to set up the model for the DARM loop from a
    configuration file with all the information about where the data is stored

    Parameters
    ----------

    Returns
    -------


    """

    def __init__(self, config):
        super().__init__(config, measurement='actuation')
        self.xarm = self.yarm = None
        if 'actuation_x_arm' in self._config:
            self.xarm = ActuationModel(config, measurement='actuation_x_arm')
        if 'actuation_y_arm' in self._config:
            self.yarm = ActuationModel(config, measurement='actuation_y_arm')

    def darm_output_matrix_values(self):
        """
        Turns the output matrix values into an array for the QUAD SUS
        """

        output_matrix = np.zeros((2, 4))
        for n in range(len(output_matrix[:, 0])):
            for m in range(len(output_matrix[0, :])):
                if n == 0 and self.darm_feedback_x[m] == 'ON':
                    output_matrix[n, m] = self.darm_output_matrix[0]
                elif n == 1 and self.darm_feedback_y[m] == 'ON':
                    output_matrix[n, m] = self.darm_output_matrix[1]

        return output_matrix

    def compute_actuation(self, frequencies, syserr_dict=None):
        """
        Compute the entire actuation function transfer function (see G1501518).
        This transfer function is from DARM_CTRL to meters sensed by the IFO.
        Note that the sign of the DARM_ERR signal is dependent upon which arm
        is under control.

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response
        actuation_syserr_dict : `dict`, optional
            dict of multiplicative values, ex.:
            {'xarm': {'UIM': `complex`, array-like}}

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the actuation function
        """

        output_matrix = self.darm_output_matrix_values()

        darm_actuation = np.zeros(len(frequencies), dtype='complex128')
        for arm in range(len(output_matrix[:, 0])):
            for stage in range(len(output_matrix[0, :])):
                if output_matrix[arm, stage] != 0.0:
                    if stage == 0:
                        stage_label = 'TOP'
                    elif stage == 1:
                        stage_label = 'UIM'
                    elif stage == 2:
                        stage_label = 'PUM'
                    else:
                        stage_label = 'TST'
                    if arm == 0:
                        if self.xarm is None:
                            raise ValueError(
                                'Must provide an xarm ActuationModel object')
                        this_arm = self.xarm
                    else:
                        if self.yarm is None:
                            raise ValueError(
                                'Must provide a yarm ActuationModel object')
                        this_arm = self.yarm
                    single_stage = this_arm.compute_actuation_single_stage(
                        frequencies, stage=stage_label)

                    if (syserr_dict is not None and
                       ['xarm', 'yarm'][arm] in syserr_dict and
                       stage_label in syserr_dict[['xarm', 'yarm'][arm]]):
                        single_stage *= \
                            syserr_dict[['xarm', 'yarm'][arm]][stage_label]

                    darm_actuation += output_matrix[arm, stage] * single_stage

        return darm_actuation
