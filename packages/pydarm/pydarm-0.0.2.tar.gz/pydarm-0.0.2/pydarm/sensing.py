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
from scipy import signal, io, constants
from collections import namedtuple

from .utils import (serielZPK, digital_delay_filter, load_foton_export_tf,
                    compute_digital_filter_response)
from .digital import iopdownsamplingfilters
from .model import Model


class SensingModel(Model):
    """
    A sensing function model object

    This is a class to set up the model for the sensing function from a
    configuration file with all the information about where the data is stored

    Parameters
    ----------

    Returns
    -------


    """

    def __init__(self, config):
        super().__init__(config, measurement='sensing')

        # TODO need some way of validating the configuration file is
        # appropriate

    @staticmethod
    def optical_response(pole_frequency, detune_spring_frequency,
                         detune_spring_Q, pro_spring=False):
        """
        Compute the coupled cavity response approximated by a single cavity
        pole and a detuned spring frequency and Q

        Parameters
        ----------
        pole_frequency : `float`
            Coupled cavity pole frequency in Hz
        detune_spring_frequency : `float`
            Detuning spring frequency in Hz
        detune_spring_Q : `float`
            Unitless Q
        pro_spring : `boolean`, optional
            logic flag to indicate pro-spring

        Returns
        -------
        optical_response : `LTI object`
            coupled cavity optical response
        """

        cavity_pole = signal.ZerosPolesGain(
            [], -2.0*np.pi*pole_frequency, 2.0*np.pi*pole_frequency)
        if not pro_spring:
            # Anti-spring: f^2 / (f^2 + fs^2 - 1j * f * fs / Q)
            # see alog LHO 48057
            detuning = signal.TransferFunction(
                [1, 0, 0],
                [1, 2.0*np.pi*detune_spring_frequency/detune_spring_Q,
                 -(2.0*np.pi*detune_spring_frequency)**2])
            detuning = detuning.to_zpk()
        else:
            # Pro-spring: f^2 / (f^2 - fs^2 + 1j * f * fs / Q)
            # see alog LHO 48057
            detuning = signal.TransferFunction(
                [1, 0, 0],
                [1, -2.0*np.pi*detune_spring_frequency/detune_spring_Q,
                 (2.0*np.pi*detune_spring_frequency)**2])
            detuning = detuning.to_zpk()
        coupled_cavity = serielZPK(cavity_pole, detuning)
        return coupled_cavity

    def omc_analog_dcpd_readout_response(self, name, frequencies):
        """
        The transfer function of the analog OMC DCPD readout electronics

        Parameters
        ----------
        name : str
            a string (e.g., 'A' or 'A_A') indicating the OMC path name to be
            evaluated. This string should be listed in
            SensingModel.omc_path_names variable
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        response : `complex128`, array-like
            transfer function response of the analog electronics in path `name`
        """

        # Make sure that name is listed uniquely in self.omc_path_names
        idx = self.omc_path_names.index(name)
        assert len(set(self.omc_path_names)) == len(self.omc_path_names)

        # First the transimpedence amplifier is computed
        if (hasattr(self, 'omc_meas_z_trans_amplifier') and
                hasattr(self, 'omc_meas_p_trans_amplifier')):
            if idx < len(self.omc_meas_z_trans_amplifier):
                meas_z_trans_amp = np.asarray(
                    self.omc_meas_z_trans_amplifier[idx])
            else:
                meas_z_trans_amp = np.asarray([])
            meas_p_trans_amp = np.asarray(
                self.omc_meas_p_trans_amplifier[idx])
        elif hasattr(self, 'omc_meas_p_trans_amplifier'):
            meas_z_trans_amp = np.asarray([])
            meas_p_trans_amp = np.asarray(
                self.omc_meas_p_trans_amplifier[idx])
        assert len(meas_z_trans_amp) <= len(meas_p_trans_amp)
        if len(meas_p_trans_amp) > 0:
            omc_trans_amplifier_response = signal.freqresp(
                signal.ZerosPolesGain(-2*np.pi*meas_z_trans_amp,
                                      -2*np.pi*meas_p_trans_amp,
                                      np.prod(2*np.pi*meas_p_trans_amp) /
                                      np.prod(2*np.pi*meas_z_trans_amp)),
                2*np.pi*frequencies)[1]
        else:
            omc_trans_amplifier_response = np.ones(len(frequencies),
                                                   dtype='complex128')

        # Whitening filter
        # The zeros and poles need to have the name appended to them
        whitening_name = getattr(self, 'whitening_mode_names')[idx]
        if (hasattr(self, f'omc_meas_z_whitening_{whitening_name}') and
                hasattr(self, f'omc_meas_p_whitening_{whitening_name}')):
            zeros = getattr(self, f'omc_meas_z_whitening_{whitening_name}')
            if idx < len(zeros):
                meas_z_whitening = np.asarray(zeros[idx])
            else:
                meas_z_whitening = np.asarray([])
            poles = getattr(self, f'omc_meas_p_whitening_{whitening_name}')
            meas_p_whitening = np.asarray(poles[idx])
        elif getattr(self, f'omc_meas_p_whitening_{whitening_name}'):
            meas_z_whitening = np.asarray([])
            poles = getattr(self, f'omc_meas_p_whitening_{whitening_name}')
            meas_p_whitening = np.asarray(poles[idx])
        assert len(meas_z_whitening) <= len(meas_p_whitening)
        if len(meas_p_whitening) > 0:
            omc_whitening_response = signal.freqresp(
                signal.ZerosPolesGain(-2*np.pi*meas_z_whitening,
                                      -2*np.pi*meas_p_whitening,
                                      np.prod(2*np.pi*meas_p_whitening) /
                                      np.prod(2*np.pi*meas_z_whitening)),
                2*np.pi*frequencies)[1]
        else:
            omc_whitening_response = np.ones(len(frequencies),
                                             dtype='complex128')

        # super high frequency poles look like a delay (see G2200551)
        super_high_frequency_poles_apparent_delay = np.exp(
            -2.0*np.pi*1j *
            self.super_high_frequency_poles_apparent_delay[idx] *
            frequencies)

        # Normalized analog anti-aliasing frequency response
        analog_aa_filter_response = \
            self.analog_aa_or_ai_filter_response(frequencies, idx)
        norm = np.abs(self.analog_aa_or_ai_filter_response(1e-2,
                                                           idx))
        analog_aa_filter_response_hi_f = analog_aa_filter_response / norm

        # Return a the combined transfer function response
        return (omc_trans_amplifier_response * omc_whitening_response *
                analog_aa_filter_response_hi_f *
                super_high_frequency_poles_apparent_delay)

    def omc_digital_compensation_response(self, name, frequencies):
        """
        The transfer function of the OMC digital compensation filters

        Parameters
        ----------
        name : str
            a string (e.g., 'A' or 'A_A') indicating the OMC path name to be
            evaluated. This string should be listed in
            SensingModel.omc_path_names variable
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        compensation_response : `complex128`, array-like
            transfer function response of the digital compensation filters in
            the path labeled by `name`
        """

        idx = self.omc_path_names.index(name)
        assert len(set(self.omc_path_names)) == len(self.omc_path_names)

        # Always return a compensation of 1 for all frequencies if nothing is
        # provided in the configuration
        compensation_response = np.ones(len(frequencies), dtype='complex128')

        # If filter file provided and filter bank provided with at least one
        # element, then we'll get a transfer function
        if (hasattr(self, 'omc_compensation_filter_file') and
                self.omc_compensation_filter_file != '' and
                len(self.omc_compensation_filter_bank) > idx and
                self.omc_compensation_filter_bank[idx] != '' and
                len(self.omc_compensation_filter_modules_in_use) > idx and
                self.omc_compensation_filter_modules_in_use[idx] != '' and
                len(self.omc_compensation_filter_gain) > idx and
                self.omc_compensation_filter_gain[idx] != ''):
            tf, pfilt = compute_digital_filter_response(
                self.dpath(self.omc_compensation_filter_file),
                self.omc_compensation_filter_bank[idx],
                self.omc_compensation_filter_modules_in_use[idx],
                self.omc_compensation_filter_gain[idx],
                frequencies)
            compensation_response *= tf
        elif (hasattr(self, 'omc_compensation_filter_file') and
                self.omc_compensation_filter_file != '' and
                len(self.omc_compensation_filter_bank) > idx and
                self.omc_compensation_filter_bank[idx] != '' and
                len(self.omc_compensation_filter_gain) > idx and
                self.omc_compensation_filter_gain[idx] != ''):
            compensation_response *= self.omc_compensation_filter_gain[idx]

        return compensation_response

    def omc_path_response(self, name, frequencies):
        """
        Compute the frequency response for a single OMC DCPD readout as shown
        in G1501518-v21 (the bracketed term directly below "O4 Calibration").
        This includes the gain ratio (= path idx / ref path, usually path A)
        and the balance matrix coefficient for path idx.

        The reference path (usually path A) should have gain ratio = 1.

        Parameters
        ----------
        name : str
            a string (e.g., 'A' or 'A_A') indicating the OMC path name to be
            evaluated. This string should be listed in
            SensingModel.omc_path_names variable
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        path_response : `complex128`, array-like
            transfer function response of the path labeled by `idx`
        """

        idx = self.omc_path_names.index(name)
        assert len(set(self.omc_path_names)) == len(self.omc_path_names)

        # analog OMC readout electronics
        analog_readout_response = self.omc_analog_dcpd_readout_response(
            name, frequencies)

        # ADC gain
        adc_gain = self.adc_gain[idx]

        # front end digital compensation of analog OMC electronics
        omc_fe_tf = self.omc_digital_compensation_response(name, frequencies)

        # digital anti-aliasing filter
        digital_aa_filter_response = \
            self.digital_aa_or_ai_filter_response(frequencies)

        # Gain ratio (note this does not include the balance matrix)
        gain_ratio = self.gain_ratio[idx]

        # balance matrix
        matrix_value = self.balance_matrix[idx]

        # The complete path response is:
        # OMC analog readout response (trans. amp, whitening, analog AA)
        # OMC digital compensation, if any
        # OMC digital AA filtering
        # Gain ratio
        # Matrix element
        path_response = analog_readout_response * adc_gain * omc_fe_tf * \
            digital_aa_filter_response * gain_ratio * matrix_value

        return path_response

    def omc_combine_path_responses(self, frequencies):
        """
        Compute the frequency response from the OMC DCPD electronics as shown
        in G1501518-v21 (the bracketed term directly below "O4 Calibration")

        Note however, that this is the WEIGHTED MEAN! Meaning that for N paths,
        we would sum the paths and divide by N if they were perfectly balanced

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        combined_paths : `complex128`, array-like
            transfer function response
        """

        # Initialize the total weight to be 0
        sum_of_weights = 0
        response = np.zeros(len(frequencies), dtype='complex128')

        # For each OMC path, add the path response to the overall response
        # and add the gain ratio value x balance matrix value for that path
        # to the sum_of_weights variable
        for n in range(len(self.omc_path_names)):
            response += self.omc_path_response(self.omc_path_names[n],
                                               frequencies)
            sum_of_weights += \
                (self.gain_ratio[n] * self.balance_matrix[n])

        # Divide the response by the sum_of_weights to calculate the weighted
        # mean OMC path response
        response /= sum_of_weights

        return response

    def light_travel_time_delay_response(self, frequencies):
        """
        Compute the frequency response from the light travel time delay

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response
        """

        return np.exp(-2.0*np.pi*1j *
                      np.mean(np.array([self.x_arm_length,
                                        self.y_arm_length])) /
                      constants.c * frequencies)

    def single_pole_approximation_delay_correction_response(self, frequencies):
        """
        Compute the frequency response from the time delay correction to the
        single pole approximation

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response
        """

        return np.exp(-2.0*np.pi*1j *
                      self.single_pole_approximation_delay_correction *
                      frequencies)

    def known_sensing_terms_for_measurement(self, frequencies):
        """
        Compute the known terms in the sensing measurement that we account
        for by dividing out. See G1501518-v21

        Note that we are now allocating all gain on the sensing path to
        the overall optical gain (previously a 0.99 gain on AA was not
        allocated to the optical gain)

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the known sensing terms

        Returns
        -------
        sensing_correction : `complex128`, array-like
            correction terms
        """

        light_travel_time_delay = \
            self.light_travel_time_delay_response(frequencies)
        single_pole_approximation_delay_correction = \
            self.single_pole_approximation_delay_correction_response(
                frequencies)
        omc_paths_response = self.omc_combine_path_responses(frequencies)

        sensing_correction = \
            self.sensing_sign * \
            light_travel_time_delay * \
            single_pole_approximation_delay_correction * \
            omc_paths_response

        return sensing_correction

    def compute_sensing(self, frequencies):
        """
        Compute the entire sensing function transfer function (see G1501518)

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the sensing function
        """

        # coupled cavity response without the optical gain
        coupled_cavity = self.optical_response(
            self.coupled_cavity_pole_frequency, self.detuned_spring_frequency,
            self.detuned_spring_q, pro_spring=self.is_pro_spring)
        coupled_cavity_filter_response = \
            signal.freqresp(coupled_cavity, 2.0*np.pi*frequencies)[1]

        # By design there are no digital delays to the OMC user model
        # see G1601472

        # light travel time delay
        light_travel_time_delay = \
            self.light_travel_time_delay_response(frequencies)

        # single pole approximation needs a correction for too much delay
        # see G1501316
        single_pole_approximation_delay_correction = \
            self.single_pole_approximation_delay_correction_response(
                frequencies)

        # OMC paths response
        omc_paths_response = self.omc_combine_path_responses(frequencies)

        # All together:
        # sensing sign
        # overall optical gain
        # coupled-cavity filter response
        # light travel time delay
        # single pole approximation delay correction
        # OMC DCPD electronics paths
        tf = self.sensing_sign * \
            self.coupled_cavity_optical_gain * \
            coupled_cavity_filter_response * \
            light_travel_time_delay * \
            single_pole_approximation_delay_correction * \
            omc_paths_response

        return tf

    def sensing_residual(self, frequencies):
        """
        Compute the residual sensing function

        This is everything in the sensing function except the optical gain
        and the optical response

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute displacement to CAL-CW residual

        Returns
        -------
        C_res : `complex128`, array-like
            transfer function response
        """

        coupled_cavity = self.optical_response(
            self.coupled_cavity_pole_frequency,
            self.detuned_spring_frequency,
            self.detuned_spring_q,
            pro_spring=self.is_pro_spring)
        C_res = (self.compute_sensing(frequencies) / (
            self.coupled_cavity_optical_gain *
            signal.freqresp(coupled_cavity, 2.0*np.pi*frequencies)[1]))

        return C_res

    def displacement_to_calcs_residual(self, frequencies):
        """
        Compute the ETM displacement to CAL-CS residual

        This will be C * 1 16k clock cycle delay * foton inverse sensing filter

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute displacement to CAL-CW residual

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response
        """

        # Get the sensing model
        C_pydarm = self.compute_sensing(frequencies)

        # Need the coupled cavity model
        coupled_cavity = self.optical_response(
            self.coupled_cavity_pole_frequency, self.detuned_spring_frequency,
            self.detuned_spring_q, pro_spring=self.is_pro_spring)

        # Need one 16k clock cycle delay going from OMC to CAL-CS
        one_clock_cycle_filter = digital_delay_filter(1, 2**14)
        one_clock_cycle_filter_response = \
            signal.dfreqresp(one_clock_cycle_filter,
                             2.0*np.pi*frequencies/2**14)[1]

        # load inverse sensing data from foton file export (1/SRC_D2N)
        if hasattr(self, 'gds_c_foton_invsensing_tf') and \
                self.gds_c_foton_invsensing_tf != '':
            [foton_export_freq, foton_export_tf] = \
                load_foton_export_tf(
                    self.dpath(self.gds_c_foton_invsensing_tf))
        else:
            # This is the fake if no foton export file is provided
            foton_export_freq = frequencies
            foton_export_tf = 1.0 / \
                signal.freqresp(
                    coupled_cavity,
                    2.0*np.pi*foton_export_freq)[1]

        # interpolate the foton filter data to the frequencies used
        foton_inv_sensing_interp = np.interp(frequencies,
                                             foton_export_freq,
                                             foton_export_tf)

        return C_pydarm * \
            one_clock_cycle_filter_response * \
            foton_inv_sensing_interp

    def old_school_senspars(self, frequencies):
        """
        The old version of pyDARM stored intermediate data products in a
        namedtuple for use when making other computations. This is not normally
        used for this version of pyDARM since there are now function calls
        but for backwards compatibility with other scripts, there is a request
        that this be available for use. NOTE: this currently does not contain
        everything, like the pcalCorrection or OMC delay

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute intermediate data products
            responses

        Returns
        -------
        sensingProducts : namedtuple
            namedtuple of all the intermediate data products
        """
        sensingProducts = \
            namedtuple('sensingProducts',
                       ['coupledCavity', 'AAanalog', 'AAanalog_delay',
                        'AAdigital', 'uncompensatedOMCDCPD', 'omcDCPDAtf',
                        'omcDCPDBtf', 'omcDCPDtf', 'delay', 'sensIOPdelay',
                        'omcDelay', 'omcDelay_freqresp',
                        'totalSensingDigital', 'totalSensingDigital_freqresp',
                        'totalSensingAnalog_freqresp',
                        'totalSensingAnalogNoCav_freqresp',
                        'singlePoleApproxDelayCorrection', 'pcaldewhitening',
                        'pcalCorrection', 'C_NoCav',
                        'calcsResid2gdsInvSensOut', 'displ2calcsResid',
                        'IIRwarp_interp'])

        coupled_cavity = self.optical_response(
            self.coupled_cavity_pole_frequency, self.detuned_spring_frequency,
            self.detuned_spring_q, pro_spring=self.is_pro_spring)
        mat = io.loadmat(self.dpath(self.analog_anti_aliasing_file))
        analog_aa_zpk = signal.ZerosPolesGain(mat['AAzeros'][:, 0],
                                              mat['AApoles'][:, 0],
                                              mat['AAgain'][0, 0])
        analog_aa_delay = np.exp(
            -2.0*np.pi*mat['AAdelay'][0, 0]*1j*frequencies)
        digital_aa_filter = iopdownsamplingfilters(
            self.anti_aliasing_rate_string, self.anti_aliasing_method,
            rcg_ver=3)
        digital_aa_filter = digital_aa_filter.to_zpk()
        uncompensated_omc_poles_trans_whitening_mean = \
            0.5*(self.uncompensated_omc_poles_trans_whitening_a +
                 self.uncompensated_omc_poles_trans_whitening_b)
        combined_uncompensated_poles = np.append(
              self.uncompensated_omc_poles_trans_amplifier,
              uncompensated_omc_poles_trans_whitening_mean)
        uncompensated_omc_dcpd = \
            signal.ZerosPolesGain(
                [], -2.0*np.pi*combined_uncompensated_poles,
                np.prod(2.0*np.pi*combined_uncompensated_poles))
        light_travel_time_delay = \
            self.light_travel_time_delay_response(frequencies)
        digital_aa_filter_response = signal.dfreqresp(
            digital_aa_filter, 2.0*np.pi*frequencies/2**16)[1]
        single_pole_approximation_delay_correction = \
            self.single_pole_approximation_delay_correction_response(
                frequencies)
        sensing_analog_nocav = self.coupled_cavity_optical_gain * \
            self.sensing_sign * \
            light_travel_time_delay * \
            single_pole_approximation_delay_correction * \
            signal.freqresp(uncompensated_omc_dcpd, 2*np.pi*frequencies)[1] * \
            signal.freqresp(analog_aa_zpk, 2*np.pi*frequencies)[1] * \
            analog_aa_delay
        sensing_analog = sensing_analog_nocav * \
            signal.freqresp(coupled_cavity, 2*np.pi*frequencies)[1]
        sensing_nocav = self.compute_sensing(frequencies) / \
            signal.freqresp(coupled_cavity, 2*np.pi*frequencies)[1]
        if self.gds_c_foton_invsensing_tf is not None:
            foton_inv_sensing_data = np.loadtxt(
                self.dpath(self.gds_c_foton_invsensing_tf))
            foton_inv_sensing_frequencies = foton_inv_sensing_data[:, 0]
            foton_inv_sensing_response = foton_inv_sensing_data[:, 1] + \
                1j*foton_inv_sensing_data[:, 2]
        else:
            foton_inv_sensing_frequencies = frequencies
            foton_inv_sensing_response = np.ones(len(frequencies))
        coupled_cavity_response = \
            signal.freqresp(coupled_cavity,
                            2.0*np.pi*foton_inv_sensing_frequencies)[1]
        foton_inv_sensing_warp = (1.0/coupled_cavity_response) / \
            foton_inv_sensing_response

        # interpolate the foton filter data to the frequencies used
        foton_inv_sensing_interp = np.interp(frequencies,
                                             foton_inv_sensing_frequencies,
                                             foton_inv_sensing_warp)

        return sensingProducts(coupled_cavity, analog_aa_zpk, analog_aa_delay,
                               digital_aa_filter, uncompensated_omc_dcpd,
                               [], [], [], light_travel_time_delay, [],
                               [], [], digital_aa_filter,
                               digital_aa_filter_response, sensing_analog,
                               sensing_analog_nocav,
                               single_pole_approximation_delay_correction,
                               [], [], sensing_nocav,
                               self.gds_sensing_correction(frequencies),
                               self.displacement_to_calcs_residual(
                                   frequencies),
                               foton_inv_sensing_interp)
