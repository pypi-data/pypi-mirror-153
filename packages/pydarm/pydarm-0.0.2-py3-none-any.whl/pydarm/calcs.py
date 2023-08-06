# Copyright (C) Evan Goetz (2022)
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
from scipy import signal
from .utils import load_foton_export_tf, digital_delay_filter
from .digital import daqdownsamplingfilters
from .model import Model
from .darm import DARMModel


class CALCSModel(DARMModel):

    def __init__(self, config, calcs=None):
        """
        Initialize a CALCSModel object

        Note that any string or path to file string in `calcs` will
        overwrite anything in the `config` parameter string or path to file
        """
        super().__init__(config)
        if 'calcs' in self._config:
            self.calcs = Model(config, measurement='calcs')
        if calcs is not None:
            self.calcs = Model(calcs, measurement='calcs')
        if not hasattr(self, 'calcs'):
            raise ValueError('No CALCS parameters have been defined')

    def optical_response_ratio(self, frequencies):
        """
        This computes (opt resp)_foton / (opt resp)

        It is a bit confusing because the FOTON filter is the inverse
        sensing function. So internally this computes
        [1/(opt resp)/FOTON] = (opt resp)_foton / (opt resp)

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies for the optical response ratio

        Returns
        -------
        foton_inv_sensing_interp : `complex128`, array-like
            ratio of interpolated values
        """

        # We need the coupled cavity LTI object
        coupled_cavity = self.sensing.optical_response(
            self.sensing.coupled_cavity_pole_frequency,
            self.sensing.detuned_spring_frequency,
            self.sensing.detuned_spring_q,
            pro_spring=self.sensing.is_pro_spring)

        # load inverse sensing data from foton file export (1/SRC_D2N)
        foton_freq, foton_tf = load_foton_export_tf(
            self.dpath(self.calcs.foton_invsensing_tf))

        # Take ratio of true optical response / foton response
        foton_inv_sensing_warp = (
            (1.0 / signal.freqresp(coupled_cavity, 2.0*np.pi*foton_freq)[1]) /
            foton_tf)

        # interpolate to the requested frequencies
        foton_inv_sensing_interp = np.interp(frequencies,
                                             foton_freq,
                                             foton_inv_sensing_warp)

        return foton_inv_sensing_interp

    def digital_out_to_displacement(self, frequencies):
        """
        Output of CALCS DRIVEALIGN to approximate TST displacement

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies for the CALCS approximated DARM actuation

        Returns
        -------
        xarm_uim : `complex128`, array-like
            X-arm UIM actuation approximation
        xarm_pum : `complex128`, array-like
            X-arm PUM actuation approximation
        xarm_tst : `complex128`, array-like
            X-arm TST actuation approximation
        yarm_uim : `complex128`, array-like
            Y-arm UIM actuation approximation
        yarm_pum : `complex128`, array-like
            Y-arm PUM actuation approximation
        yarm_tst : `complex128`, array-like
            Y-arm TST actuation approximation
        """

        arms = ['xarm', 'yarm']
        stages = ['uim', 'pum', 'tst']
        for m, arm in enumerate(arms):
            for n, stage in enumerate(stages):
                tf_dig_interp = np.ones(len(frequencies), dtype='complex128')
                tf_ana_interp = np.ones(len(frequencies), dtype='complex128')
                if hasattr(self.calcs, f'{arm}_{stage}_coiloutf'):
                    val = getattr(self.calcs, f'{arm}_{stage}_coiloutf')
                    if val != '':
                        [f, tf_dig] = load_foton_export_tf(self.dpath(val))
                        tf_dig_interp = np.interp(frequencies, f, tf_dig)
                if hasattr(self.calcs, f'{arm}_{stage}_analog'):
                    val = getattr(self.calcs, f'{arm}_{stage}_analog')
                    if val != '':
                        [f, tf_ana] = load_foton_export_tf(self.dpath(val))
                        tf_ana_interp = np.interp(frequencies, f, tf_ana)

                if hasattr(self.calcs, f'{arm}_output_matrix'):
                    out_mtrx = getattr(self.calcs, f'{arm}_output_matrix')[n + 1]
                else:
                    out_mtrx = 0

                vars()[f'{arm}_{stage}'] = out_mtrx * tf_dig_interp * tf_ana_interp

        return (vars()['xarm_uim'],
                vars()['xarm_pum'],
                vars()['xarm_tst'],
                vars()['yarm_uim'],
                vars()['yarm_pum'],
                vars()['yarm_tst'])

    def gds_sensing_correction(self, frequencies):
        """
        Compute the correction to the CAL-CS output for GDS

        We need to divide out the front end model optical response part only
        (filter is called usually SRC-D2N) and be sure to include 1 16k clock
        cycle delay from the model jump OMC to CAL-CS. There is an optical
        gain factor in the front end model, but it is fine to leave this in
        place. The output is basically C_pydarm / C_foton, and GDS will need to
        either divide the DARM_ERR data by this function or invert the output
        of this function and multiply by the DARM_ERR data.

        This is C_res*delay*(opt resp)/(opt resp)_foton

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the GDS sensing correction

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the correction
        """

        # Residual sensing function transfer function
        # This is everything in sensing except the optical gain and response
        C_res = self.sensing.sensing_residual(frequencies)

        # we will need to apply a delay because when it is inverted in GDS
        # this will become an advance (the correct thing to do)
        one_clock_cycle_filter = digital_delay_filter(1, 2**14)
        one_clock_cycle_filter_response = \
            signal.dfreqresp(one_clock_cycle_filter,
                             2.0*np.pi*frequencies/2**14)[1]

        # this is the sensing model without optical plant and with one clock
        # cycle delay applied
        C_res_with_calcs_delay = C_res * one_clock_cycle_filter_response

        # get the optical response ratio between FOTON and pyDARM
        foton_inv_sensing_interp = self.optical_response_ratio(frequencies)

        # the final correction is the sensing model divided by the interpolated
        # foton filter
        correction = C_res_with_calcs_delay / foton_inv_sensing_interp

        return correction

    def gds_actuation_correction(self, frequencies, arm, stage, daqdownsample=True):
        """
        Compute the correction to the CAL-CS output for GDS. Note that this
        implicitly assumes that the front end digital filters in CALCS is the
        same as that in the SUS path! If this is not the case, then this
        method will not return a correct answer

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the GDS sensing correction

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the correction
        """

        # Get the analog actuation transfer function from the front end
        foton_file = getattr(self.calcs,
                             f'{arm.lower()}_{stage.lower()}_analog')
        freq_foton, tf_foton = load_foton_export_tf(self.dpath(foton_file))

        # Get the full actuation for the stage and the digital filters
        if arm == 'xarm':
            sus_act = self.actuation.xarm.compute_actuation_single_stage(
                freq_foton, stage=stage)
            uim_filt, pum_filt, tst_filt = (
                self.actuation.xarm.sus_digital_filters_response(freq_foton))
        elif arm == 'yarm':
            sus_act = self.actuation.xarm.compute_actuation_single_stage(
                freq_foton, stage=stage)
            uim_filt, pum_filt, tst_filt = (
                self.actuation.xarm.sus_digital_filters_response(freq_foton))
        else:
            raise ValueError('arm must be either xarm or yarm')

        # CALCS output matrix
        out_matrix = getattr(self.calcs, f'{arm.lower()}_output_matrix')

        # This division here assumes that the CALCS FOTON filters match exactly
        # the SUS FOTON filters
        if stage == 'UIM':
            sus_act /= uim_filt * out_matrix[1]
        elif stage == 'PUM':
            sus_act /= pum_filt * out_matrix[2]
        elif stage == 'TST':
            sus_act /= tst_filt * out_matrix[3]
        else:
            raise ValueError('stage must be UIM, PUM, or TST')

        sus_act /= tf_foton
        # Now sus_act is basically A_i residual

        # Interpolate to the desired frequencies
        sus_act = np.interp(frequencies, freq_foton, sus_act)

        # Here we want the 1 clock cycle delay transfer function
        omc_to_sus = signal.dfreqresp(digital_delay_filter(1, 16384),
                                      2.0*np.pi*frequencies/16384)[1]

        if daqdownsample:
            # DAQ downsampling filters are applied so we need to account
            # for this
            daqdownsampling = signal.dfreqresp(
                daqdownsamplingfilters(2**14, 2**12, 'biquad', 'v3'),
                2.0*np.pi*frequencies/2**14)[1]
        else:
            daqdownsampling = 1

        # This removes the DAQ downsampling filters and the OMC to CAL-CS delay
        residual_actuation_filter = (sus_act / (daqdownsampling * omc_to_sus))

        return residual_actuation_filter

    def calcs_darm_actuation(self, frequencies):
        """
        Compute the CALCS approximated DARM actuation. This method implicitly
        assumes that the CALCS DARM output matrix and actuation digital
        filtering matches the installed in-loop DARM ouput matrix and actuation
        digital filtering. If they do not agree, then this method may give
        incorrect results, so it's best to confirm agreement

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies for the CALCS approximated DARM actuation

        Returns
        -------
        calcs_actuation : `complex128`, array-like
            Residual phase after removing the simulated delay
        """

        # Assume the same as in-loop DARM output matrix
        output_matrix = self.actuation.darm_output_matrix_values()

        # Compute the CALCS approximated "digitial out to displacement" =
        # output of CALCS DRIVEALIGN to displacement.
        # Order is UIM_x, PUM_x, TST_x, UIM_y, PUM_y, and TST_y
        calcs_dig_out_to_disp = self.digital_out_to_displacement(frequencies)

        # Put calcs_dig_out_to_disp into same order as the output matrix
        calcs_dig_out_to_disp = np.array(
            [[np.zeros(len(calcs_dig_out_to_disp[0]), dtype='complex128'),
              calcs_dig_out_to_disp[0],
              calcs_dig_out_to_disp[1],
              calcs_dig_out_to_disp[2]],
             [np.zeros(len(calcs_dig_out_to_disp[3]), dtype='complex128'),
              calcs_dig_out_to_disp[3],
              calcs_dig_out_to_disp[4],
              calcs_dig_out_to_disp[5]]])

        # Start with zeros
        calcs_actuation = np.zeros(len(frequencies), dtype='complex128')

        # Loop over arms and stages
        for arm in range(len(output_matrix[:, 0])):
            if np.any(output_matrix[arm, :]):
                if arm == 0:
                    dig_filt = (
                        self.actuation.xarm.sus_digital_filters_response(
                            frequencies))
                elif arm == 1:
                    dig_filt = (
                        self.actuation.yarm.sus_digital_filters_response(
                            frequencies))
            for stage in range(len(output_matrix[0, :])):
                if output_matrix[arm, stage] != 0.0:
                    # dig_filt only has UIM, PUM, and TST
                    # calcs_dig_out_to_disp has same order as output_matrix
                    calcs_actuation += (output_matrix[arm, stage] *
                                        dig_filt[stage - 1] *
                                        calcs_dig_out_to_disp[arm, stage])

        return calcs_actuation

    def residual_sensing_sim_delay(self, frequencies, clock=False):
        """
        Fit a simulated delay based on the residual sensing in units
        of seconds delay or (if clock=True) in units of 16384 samples/sec,
        i.e., 1 16384 Hz clock delay = 6.1035e-5 s. Positive indicates
        a delay, negative indicates an advance

        Internally, the fit domain is over the range of 10 Hz to 2000 Hz,
        though if your frequency range is smaller it will fit over the
        smaller.

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to model the phase delay
        clock : `boolean`, optional
            if clock is True, then the output delay_fit and residual will
            be computed and rounded to the nearest number of integer clock
            cycles (16384)

        Returns
        -------
        delay_fit : float
            Best fit to the data; either in units of seconds or rounded to
            the nearest integer clock cycle (if clock=True)
        residual : `float`, array-like
            Residual phase after removing the simulated delay
        """

        C_res = self.sensing.sensing_residual(frequencies)

        phase_delay = np.angle(C_res) / (2.0*np.pi*frequencies)

        poly = np.polynomial.Polynomial.fit(frequencies, phase_delay, 0,
                                            domain=[10, 2000])
        delay_fit = -poly.convert().coef[0]

        if clock is True:
            delay_fit = np.round(delay_fit * 16384) / 16384

        residual = np.angle(C_res) + delay_fit*(2.0*np.pi*frequencies)

        if clock is True:
            delay_fit *= 16384

        return delay_fit, residual

    def residual_actuation_sim_delay(self, frequencies, clock=False):
        """
        Fit a simulated delay based on the residual actuation in units
        of seconds delay or (if clock=True) in units of 16384 samples/sec,
        i.e., 1 16384 Hz clock delay = 6.1035e-5 s. Positive indicates
        a delay, negative indicates an advance

        Internally, the fit domain is over the range of 10 Hz to 2000 Hz,
        though if your frequency range is smaller it will fit over the
        smaller.

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to model the phase delay
        clock : `boolean`, optional
            if clock is True, then the output delay_fit and residual will
            be computed and rounded to the nearest number of integer clock
            cycles (16384)

        Returns
        -------
        delay_fit : float
            Best fit to the data; either in units of seconds or rounded to
            the nearest integer clock cycle (if clock=True)
        residual : `float`, array-like
            Residual phase after removing the simulated delay
        """

        A_res = (self.actuation.compute_actuation(frequencies) /
                 self.calcs_darm_actuation(frequencies))

        phase_delay = np.angle(A_res) / (2.0*np.pi*frequencies)

        poly = np.polynomial.Polynomial.fit(frequencies, phase_delay, 0,
                                            domain=[10, 2000])
        delay_fit = -poly.convert().coef[0]

        if clock is True:
            delay_fit = np.round(delay_fit * 16384) / 16384

        residual = np.angle(A_res) + delay_fit*(2.0*np.pi*frequencies)

        if clock is True:
            delay_fit *= 16384

        return delay_fit, residual

    def calcs_dtt_calibration(self, frequencies, include_whitening=True,
                              strain_calib=False, save_to_file=None):
        """
        Compute the calibration transfer function for the main control room
        calibrated sensitivity curve. One can save this data to a file
        with the needed frequency, dB magnitude, and degrees phase columns.

        Details (see T1900169):
        CAL-DELTAL_EXTERNAL = whiten * [d_err/C_foton + d_ctrl*A_foton] * delay
        where whiten is a whitening filter and delay is the 1 16384 clock cycle
        delay between the OMC model and CALCS
        real DELTAL_EXTERNAL = [d_err/C_real + d_ctrl*A_real]
        C_real != C_foton and A_real != A_foton, so the correction factor
        (or calibration factor) is going to be the ratio of
        real DELTAL_EXTERNAL / CAL-DELTAL_EXTERNAL
        So the calibration scaling is a multiplicative factor given by:
        (1+G)/(W*delay*C_r)*(opt resp)_foton/(opt resp) *
          [1+G/(C_r*A_r)*(opt resp)_foton/(opt resp)*FE]
        where G = C*D*A (the open loop gain)
        C_r = C/[H*(opt resp)]
        A_r = A/A_foton
        FE = the clock cycle delay or Thiran filter delay installed
             in the front end to delay the actuation path
        (see eq. 38 of T1900169)

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the CAL_DELTAL_EXTERNAL DTT
            calibration
        include_whitening : `bool`, optional
            if the whitening filter is on (default), then we'd like to remove
            its effect so by default this divides out the whitening filter
        strain_calib : `bool`, optional
            the output defaults to dL_true/dL_calcs, so that we can recalibrate
            CAL-DELTAL_EXTERNAL. If this option is True, then the output is
            h_true/dL_calcs
        save_to_file : `str`, optional
            Filename (ASCII) to save the data from this result. Note:
            the file columns are <frequency> <magnitude (dB)> <phase (deg)>

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the calibration
        """

        # This is C_r*delay*(opt resp)/(opt resp)_foton
        gds_corr = self.gds_sensing_correction(frequencies)

        # Whitening filter
        foton_freq, foton_tf = load_foton_export_tf(
            self.dpath(self.calcs.foton_deltal_whitening_tf))
        whitening_interp = np.interp(frequencies,
                                     foton_freq,
                                     foton_tf)
        if not include_whitening:
            whitening_interp = 1

        # Foton delay filter
        foton_freq, foton_tf = load_foton_export_tf(
            self.dpath(self.calcs.foton_delay_filter_tf))
        delay_interp = np.interp(frequencies, foton_freq, foton_tf)

        # Model loop gain CDA
        G = self.compute_darm_olg(frequencies)

        # optical response ratio
        foton_inv_sensing_interp = self.optical_response_ratio(frequencies)

        # Residual sensing is sensing / (gain * opt response)
        C_res = self.sensing.sensing_residual(frequencies)

        # Residual actuation is actuation / A_foton
        A_res = (self.actuation.compute_actuation(frequencies) /
                 self.calcs_darm_actuation(frequencies))

        # Old: calib = 1.0 / (whitening_interp * gds_corr)
        # New:
        calib = ((1.0 + G) / (whitening_interp * gds_corr) /
                 (1.0 + G*foton_inv_sensing_interp*delay_interp/(C_res*A_res)))

        if strain_calib:
            calib /= np.mean(np.array([self.sensing.x_arm_length,
                                       self.sensing.y_arm_length]))

        if save_to_file is not None:
            np.savetxt(save_to_file,
                       np.array([frequencies,
                                 20.0*np.log10(np.abs(calib)),
                                 np.angle(calib, deg=True)]).T,
                       fmt='%.7g')

        return calib
