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
from scipy import signal
from gwpy.time import tconvert, from_gps

from .model import Model
from .sensing import SensingModel
from .actuation import DARMActuationModel
from .pcal import PcalModel
from .utils import compute_digital_filter_response
from .digital import daqdownsamplingfilters
from .plot import critique


class DigitalModel(Model):
    """DARM digital controller model object

    """
    def __init__(self, config):
        super().__init__(config, measurement='digital')

    def compute_response(self, frequencies):
        """
        Compute DARM digital controller frequency response

        Uses filter ZPK transfer function response from Foton file.

        Parameters
        ----------
        frequencies

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the digital SUS filter

        """

        response = np.ones(len(frequencies), dtype='complex128')
        for n in range(len(self.digital_filter_bank)):
            if n == 0:
                tf, pfilt = compute_digital_filter_response(
                    self.dpath(self.digital_filter_file),
                    self.digital_filter_bank[n],
                    self.digital_filter_modules_in_use[n],
                    self.digital_filter_gain[n], frequencies, pfilt=None)
            else:
                tf = compute_digital_filter_response(
                    self.dpath(self.digital_filter_file),
                    self.digital_filter_bank[n],
                    self.digital_filter_modules_in_use[n],
                    self.digital_filter_gain[n], frequencies, pfilt=pfilt)[0]
            response *= tf
        return response


class DARMModel(Model):
    """DARM model object

    This is a class to set up the model for the DARM loop from a
    configuration file with all the information about where the data is stored

    """
    def __init__(self, config, sensing=None, actuation=None, digital=None, pcal=None):
        super().__init__(config)
        self.sensing = sensing or SensingModel(config)
        self.actuation = actuation or DARMActuationModel(config)
        self.digital = digital or DigitalModel(config)
        self.pcal = pcal
        if not self.pcal and 'pcal' in self._config:
            self.pcal = PcalModel(config)

    def compute_darm_olg(self, frequencies):
        """
        Compute the entire DARM open loop transfer function (see G1501518)

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the sensing function

        """
        C_response = self.sensing.compute_sensing(frequencies)
        A_response = self.actuation.compute_actuation(frequencies)
        D_response = self.digital.compute_response(frequencies)

        return C_response * A_response * D_response

    def compute_response_function(self, frequencies, sensing_syserr=None,
                                  actuation_syserr_dict=None):
        """
        Compute the entire DARM response transfer function (see G1501518)

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response
        sensing_syserr : `complex`, array-like, optional
            multiplicative factor to include relative sensing systematic error
        actuation_syserr_dict : `dict`, optional
            dict of multiplicative values, ex.:
            {'xarm': {'UIM': `complex`, array-like}}

        Returns
        -------
        tf : `complex128`, array-like
            transfer function of the DARM closed-loop response
        """

        C_response = self.sensing.compute_sensing(frequencies)
        A_response = self.actuation.compute_actuation(frequencies,
                                                      actuation_syserr_dict)
        D_response = self.digital.compute_response(frequencies)

        if sensing_syserr is not None:
            C_response *= sensing_syserr

        return (1.0/C_response + D_response * A_response)

    def compute_epics_records(self, f_pcal1, f_uim, f_pum, f_tst, f_pcal2,
                              f_pcal3, f_pcal4, arm, save_to_file=None):
        """
        This is a LIGO specific function for generating front end calibration
        and GDS EPICS records. This function is very specific for O3, but we
        may wish to extend it or generalize it for O4 and/or other detectors.
        Currently it accepts 4 PCAL injections frequencies and 3 SUS actuator
        frequencies.

        See T1700106-v10 and G1601472 for additional details

        Parameters
        ----------
        f_pcal1 : `float`
            Pcal frequency line 1 (the frequency for the SUS actuators)
        f_uim : `float`
            UIM line frequency
        f_pum : `float`
            PUM line frequency
        f_tst : `float`
            TST line frequency
        f_pcal2 : `float`
            Pcal line frequency 2 (the mid-frequency ~400 Hz line)
        f_pcal3 : `float`
            Pcal line frequency 3 (the high-frequency ~1080 Hz line)
        f_pcal4 : `float`
            Pcal line frequency 4 (the low frequency ~8 Hz line)
        arm : `str`
            'x' or 'y' to indicate which arm is used for the SUS actuators
        save_to_file : `str`, optional
            Filename (ASCII) to save the values for EPICS from this reference model


        Returns
        -------
        out : dict
            Dictionary of EPICS records

        """

        freq = np.array(
            [f_pcal1, f_uim, f_pum, f_tst, f_pcal2, f_pcal3, f_pcal4])

        R = self.compute_response_function(freq)

        daqdownsampling = daqdownsamplingfilters(2**14, 2**9, 'biquad', 'v3')
        daqdownsampling_response = signal.dfreqresp(daqdownsampling,
                                                    2.0*np.pi*freq/2**14)[1]

        # Pcal corrections
        # See T1700106
        pcal_correction = self.pcal.compute_pcal_correction(freq)
        PCAL_LINE1_CORRECTION = pcal_correction[0] * \
            np.exp(-2*np.pi*1j*freq[0]/16384)   # EP0
        PCAL_LINE2_CORRECTION = pcal_correction[4] * \
            np.exp(-2*np.pi*1j*freq[4]/16384)   # EP9
        PCAL_LINE3_CORRECTION = pcal_correction[5] * \
            np.exp(-2*np.pi*1j*freq[5]/16384)   # EP24
        PCAL_LINE4_CORRECTION = pcal_correction[6] * \
            np.exp(-2*np.pi*1j*freq[6]/16384)   # EP15

        # The actuator lines are injected at the input to the DRIVEALIGN bank
        # Also get the complete actuation model
        if arm == 'x':
            this_arm = self.actuation.xarm
        elif arm == 'y':
            this_arm = self.actuation.yarm
        else:
            raise ValueError('Must provide value of x or y to argument arm')

        uim_actuation_epics, pum_actuation_epics, tst_actuation_epics = \
            this_arm.drivealign_to_displacement(freq)
        uim_actuation_epics *= this_arm.darm_feedback_sign
        pum_actuation_epics *= this_arm.darm_feedback_sign
        tst_actuation_epics *= this_arm.darm_feedback_sign
        uim = this_arm.compute_actuation_single_stage(freq, stage='UIM')
        pum = this_arm.compute_actuation_single_stage(freq, stage='PUM')
        tst = this_arm.compute_actuation_single_stage(freq, stage='TST')

        # Actuator EPICS
        # Need to divide out a DAQ downsampling filter from the reference A
        # values because channels sampled at 512 Hz have an AA filter applied
        # See T1700106
        SUS_LINE1_REF_INVA_UIM_RESPRATIO = \
            (1.0/(uim_actuation_epics[1]/daqdownsampling_response[1])) * \
            (1.0/R[0]) * R[1] * np.exp(2*np.pi*1j*freq[1]/16384)  # EP3
        SUS_LINE2_REF_INVA_PUM_RESPRATIO = \
            (1.0/(pum_actuation_epics[2]/daqdownsampling_response[2])) * \
            (1.0/R[0]) * R[2] * np.exp(2*np.pi*1j*freq[2]/16384)  # EP2
        SUS_LINE3_REF_INVA_TST_RESPRATIO = \
            (1.0/(tst_actuation_epics[3]/daqdownsampling_response[3])) * \
            (1.0/R[0]) * R[3] * np.exp(2*np.pi*1j*freq[3]/16384)  # EP1

        # Need to add a phase delay to the PCAL readback because the
        # PCAL channel acquires a phase delay from the model jump
        # to CAL-CS and the calculation expects no delay (as in GDS)
        PCAL_LINE1_PCAL_DEMOD_PHASE = \
            np.angle(np.exp(-2*np.pi*1j*freq[0]/16384), deg=True)
        PCAL_LINE2_PCAL_DEMOD_PHASE = \
            np.angle(np.exp(-2*np.pi*1j*freq[4]/16384), deg=True)
        PCAL_LINE3_PCAL_DEMOD_PHASE = \
            np.angle(np.exp(-2*np.pi*1j*freq[5]/16384), deg=True)
        PCAL_LINE4_PCAL_DEMOD_PHASE = \
            np.angle(np.exp(-2*np.pi*1j*freq[6]/16384), deg=True)

        # Need to add a phase delay to the SUS excitation because the
        # SUS channel acquires a phase delay from the model jump
        # to CAL-CS and the calculation expects no delay (as in GDS).
        # Note that if a replica SUS excitation is used in the CAL-CS model
        # then these should actually be set to zero.
        SUS_LINE1_SUS_DEMOD_PHASE = \
            np.angle(np.exp(-2*np.pi*1j*freq[1]/16384), deg=True)
        SUS_LINE2_SUS_DEMOD_PHASE = \
            np.angle(np.exp(-2*np.pi*1j*freq[2]/16384), deg=True)
        SUS_LINE3_SUS_DEMOD_PHASE = \
            np.angle(np.exp(-2*np.pi*1j*freq[3]/16384), deg=True)

        # Compute the sensing function without the optical response but need to
        # include the optical gain
        coupled_cavity = self.sensing.optical_response(
            self.sensing.coupled_cavity_pole_frequency,
            self.sensing.detuned_spring_frequency,
            self.sensing.detuned_spring_q,
            pro_spring=self.sensing.is_pro_spring)
        sensing_no_cavity_response = \
            self.sensing.compute_sensing(freq) / \
            signal.freqresp(coupled_cavity, 2.0*np.pi*freq)[1]
        PCAL_LINE2_REF_C_NOCAVPOLE = sensing_no_cavity_response[4]  # EP4
        PCAL_LINE4_REF_C_NOCAVPOLE = sensing_no_cavity_response[6]  # EP10
        PCAL_LINE1_REF_C_NOCAVPOLE = sensing_no_cavity_response[0]  # EP19

        # DARM digital filtering
        darm_digital_filter_response = \
            self.digital.compute_response(freq)
        PCAL_LINE2_REF_D = darm_digital_filter_response[4]  # EP5
        PCAL_LINE4_REF_D = darm_digital_filter_response[6]  # EP11
        PCAL_LINE1_REF_D = darm_digital_filter_response[0]  # EP20

        # Actuation
        PCAL_LINE2_REF_A_TST = tst[4]  # EP6
        PCAL_LINE2_REF_A_PUM = pum[4]  # EP7
        PCAL_LINE2_REF_A_UIM = uim[4]  # EP8
        PCAL_LINE4_REF_A_TST = tst[6]  # EP12
        PCAL_LINE4_REF_A_PUM = pum[6]  # EP13
        PCAL_LINE4_REF_A_UIM = uim[6]  # EP14
        PCAL_LINE1_REF_A_TST = tst[0]  # EP21
        PCAL_LINE1_REF_A_PUM = pum[0]  # EP22
        PCAL_LINE1_REF_A_UIM = uim[0]  # EP23

        if save_to_file is not None:
            save_txt_epcis_value = np.vstack(
                (PCAL_LINE1_CORRECTION.real,
                 PCAL_LINE1_CORRECTION.imag,
                 SUS_LINE3_REF_INVA_TST_RESPRATIO.real,
                 SUS_LINE3_REF_INVA_TST_RESPRATIO.imag,
                 SUS_LINE2_REF_INVA_PUM_RESPRATIO.real,
                 SUS_LINE2_REF_INVA_PUM_RESPRATIO.imag,
                 SUS_LINE1_REF_INVA_UIM_RESPRATIO.real,
                 SUS_LINE1_REF_INVA_UIM_RESPRATIO.imag,
                 PCAL_LINE2_REF_C_NOCAVPOLE.real,
                 PCAL_LINE2_REF_C_NOCAVPOLE.imag,
                 PCAL_LINE2_REF_D.real,
                 PCAL_LINE2_REF_D.imag,
                 PCAL_LINE2_REF_A_TST.real,
                 PCAL_LINE2_REF_A_TST.imag,
                 PCAL_LINE2_REF_A_PUM.real,
                 PCAL_LINE2_REF_A_PUM.imag,
                 PCAL_LINE2_REF_A_UIM.real,
                 PCAL_LINE2_REF_A_UIM.imag,
                 PCAL_LINE2_CORRECTION.real,
                 PCAL_LINE2_CORRECTION.imag,
                 PCAL_LINE4_REF_C_NOCAVPOLE.real,
                 PCAL_LINE4_REF_C_NOCAVPOLE.imag,
                 PCAL_LINE4_REF_D.real,
                 PCAL_LINE4_REF_D.imag,
                 PCAL_LINE4_REF_A_TST.real,
                 PCAL_LINE4_REF_A_TST.imag,
                 PCAL_LINE4_REF_A_PUM.real,
                 PCAL_LINE4_REF_A_PUM.imag,
                 PCAL_LINE4_REF_A_UIM.real,
                 PCAL_LINE4_REF_A_UIM.imag,
                 PCAL_LINE4_CORRECTION.real,
                 PCAL_LINE4_CORRECTION.imag,
                 PCAL_LINE1_REF_C_NOCAVPOLE.real,
                 PCAL_LINE1_REF_C_NOCAVPOLE.imag,
                 PCAL_LINE1_REF_D.real,
                 PCAL_LINE1_REF_D.imag,
                 PCAL_LINE1_REF_A_TST.real,
                 PCAL_LINE1_REF_A_TST.imag,
                 PCAL_LINE1_REF_A_PUM.real,
                 PCAL_LINE1_REF_A_PUM.imag,
                 PCAL_LINE1_REF_A_UIM.real,
                 PCAL_LINE1_REF_A_UIM.imag,
                 PCAL_LINE3_CORRECTION.real,
                 PCAL_LINE3_CORRECTION.imag,
                 PCAL_LINE1_PCAL_DEMOD_PHASE,
                 PCAL_LINE2_PCAL_DEMOD_PHASE,
                 PCAL_LINE3_PCAL_DEMOD_PHASE,
                 PCAL_LINE4_PCAL_DEMOD_PHASE,
                 SUS_LINE1_SUS_DEMOD_PHASE,
                 SUS_LINE2_SUS_DEMOD_PHASE,
                 SUS_LINE3_SUS_DEMOD_PHASE))

            save_txt_epics_channel_name = np.vstack(
                ('CAL-CS_TDEP_PCAL_LINE1_CORRECTION_REAL',
                 'CAL-CS_TDEP_PCAL_LINE1_CORRECTION_IMAG'
                 'CAL-CS_TDEP_SUS_LINE3_REF_INVA_TST_RESPRATIO_REAL',
                 'CAL-CS_TDEP_SUS_LINE3_REF_INVA_TST_RESPRATIO_IMAG',
                 'CAL-CS_TDEP_SUS_LINE2_REF_INVA_PUM_RESPRATIO_REAL',
                 'CAL-CS_TDEP_SUS_LINE2_REF_INVA_PUM_RESPRATIO_IMAG',
                 'CAL-CS_TDEP_SUS_LINE1_REF_INVA_UIM_RESPRATIO_REAL',
                 'CAL-CS_TDEP_SUS_LINE1_REF_INVA_UIM_RESPRATIO_IMAG',
                 'CAL-CS_TDEP_PCAL_LINE2_REF_C_NOCAVPOLE_REAL',
                 'CAL-CS_TDEP_PCAL_LINE2_REF_C_NOCAVPOLE_IMAG',
                 'CAL-CS_TDEP_PCAL_LINE2_REF_D_REAL',
                 'CAL-CS_TDEP_PCAL_LINE2_REF_D_IMAG',
                 'CAL-CS_TDEP_PCAL_LINE2_REF_A_TST_REAL',
                 'CAL-CS_TDEP_PCAL_LINE2_REF_A_TST_IMAG',
                 'CAL-CS_TDEP_PCAL_LINE2_REF_A_PUM_REAL',
                 'CAL-CS_TDEP_PCAL_LINE2_REF_A_PUM_IMAG',
                 'CAL-CS_TDEP_PCAL_LINE2_REF_A_UIM_REAL',
                 'CAL-CS_TDEP_PCAL_LINE2_REF_A_UIM_IMAG',
                 'CAL-CS_TDEP_PCAL_LINE2_CORRECTION_REAL',
                 'CAL-CS_TDEP_PCAL_LINE2_CORRECTION_IMAG',
                 'CAL-CS_TDEP_PCAL_LINE4_REF_C_NOCAVPOLE_REAL',
                 'CAL-CS_TDEP_PCAL_LINE4_REF_C_NOCAVPOLE_IMAG',
                 'CAL-CS_TDEP_PCAL_LINE4_REF_D_REAL',
                 'CAL-CS_TDEP_PCAL_LINE4_REF_D_IMAG',
                 'CAL-CS_TDEP_PCAL_LINE4_REF_A_TST_REAL',
                 'CAL-CS_TDEP_PCAL_LINE4_REF_A_TST_IMAG',
                 'CAL-CS_TDEP_PCAL_LINE4_REF_A_PUM_REAL',
                 'CAL-CS_TDEP_PCAL_LINE4_REF_A_PUM_IMAG',
                 'CAL-CS_TDEP_PCAL_LINE4_REF_A_UIM_REAL',
                 'CAL-CS_TDEP_PCAL_LINE4_REF_A_UIM_IMAG',
                 'CAL-CS_TDEP_PCAL_LINE4_CORRECTION_REAL',
                 'CAL-CS_TDEP_PCAL_LINE4_CORRECTION_IMAG',
                 'CAL-CS_TDEP_PCAL_LINE1_REF_C_NOCAVPOLE_REAL',
                 'CAL-CS_TDEP_PCAL_LINE1_REF_C_NOCAVPOLE_IMAG',
                 'CAL-CS_TDEP_PCAL_LINE1_REF_D_REAL',
                 'CAL-CS_TDEP_PCAL_LINE1_REF_D_IMAG',
                 'CAL-CS_TDEP_PCAL_LINE1_REF_A_TST_REAL',
                 'CAL-CS_TDEP_PCAL_LINE1_REF_A_TST_IMAG',
                 'CAL-CS_TDEP_PCAL_LINE1_REF_A_PUM_REAL',
                 'CAL-CS_TDEP_PCAL_LINE1_REF_A_PUM_IMAG',
                 'CAL-CS_TDEP_PCAL_LINE1_REF_A_UIM_REAL',
                 'CAL-CS_TDEP_PCAL_LINE1_REF_A_UIM_IMAG',
                 'CAL-CS_TDEP_PCAL_LINE3_CORRECTION_REAL',
                 'CAL-CS_TDEP_PCAL_LINE3_CORRECTION_IMAG',
                 'CAL-CS_TDEP_PCAL_LINE1_PCAL_DEMOD_PHASE',
                 'CAL-CS_TDEP_PCAL_LINE2_PCAL_DEMOD_PHASE',
                 'CAL-CS_TDEP_PCAL_LINE3_PCAL_DEMOD_PHASE',
                 'CAL-CS_TDEP_PCAL_LINE4_PCAL_DEMOD_PHASE',
                 'CAL-CS_TDEP_SUS_LINE1_SUS_DEMOD_PHASE',
                 'CAL-CS_TDEP_SUS_LINE2_SUS_DEMOD_PHASE',
                 'CAL-CS_TDEP_SUS_LINE3_SUS_DEMOD_PHASE'))

            save_txt_epics = np.column_stack(
                (save_txt_epics_channel_name,
                 save_txt_epcis_value))

            utc_now = from_gps(tconvert())

            np.savetxt(
                f'epicsrecords_{self.name}'
                f'_model{self.model_date}'
                f'_create{utc_now.year}{utc_now.month}{utc_now.day}.txt',
                save_txt_epics,
                fmt='%s %.6e')

        # Output - see T1700106
        return {
            'CAL-CS_TDEP_PCAL_LINE1_CORRECTION': PCAL_LINE1_CORRECTION,
            'CAL-CS_TDEP_SUS_LINE3_REF_INVA_TST_RESPRATIO': SUS_LINE3_REF_INVA_TST_RESPRATIO,
            'CAL-CS_TDEP_SUS_LINE2_REF_INVA_PUM_RESPRATIO': SUS_LINE2_REF_INVA_PUM_RESPRATIO,
            'CAL-CS_TDEP_SUS_LINE1_REF_INVA_UIM_RESPRATIO': SUS_LINE1_REF_INVA_UIM_RESPRATIO,
            'CAL-CS_TDEP_PCAL_LINE2_REF_C_NOCAVPOLE': PCAL_LINE2_REF_C_NOCAVPOLE,
            'CAL-CS_TDEP_PCAL_LINE2_REF_D': PCAL_LINE2_REF_D,
            'CAL-CS_TDEP_PCAL_LINE2_REF_A_TST': PCAL_LINE2_REF_A_TST,
            'CAL-CS_TDEP_PCAL_LINE2_REF_A_PUM': PCAL_LINE2_REF_A_PUM,
            'CAL-CS_TDEP_PCAL_LINE2_REF_A_UIM': PCAL_LINE2_REF_A_UIM,
            'CAL-CS_TDEP_PCAL_LINE2_CORRECTION': PCAL_LINE2_CORRECTION,
            'CAL-CS_TDEP_PCAL_LINE4_REF_C_NOCAVPOLE': PCAL_LINE4_REF_C_NOCAVPOLE,
            'CAL-CS_TDEP_PCAL_LINE4_REF_D': PCAL_LINE4_REF_D,
            'CAL-CS_TDEP_PCAL_LINE4_REF_A_TST': PCAL_LINE4_REF_A_TST,
            'CAL-CS_TDEP_PCAL_LINE4_REF_A_PUM': PCAL_LINE4_REF_A_PUM,
            'CAL-CS_TDEP_PCAL_LINE4_REF_A_UIM': PCAL_LINE4_REF_A_UIM,
            'CAL-CS_TDEP_PCAL_LINE4_CORRECTION': PCAL_LINE4_CORRECTION,
            'CAL-CS_TDEP_PCAL_LINE1_REF_C_NOCAVPOLE': PCAL_LINE1_REF_C_NOCAVPOLE,
            'CAL-CS_TDEP_PCAL_LINE1_REF_D': PCAL_LINE1_REF_D,
            'CAL-CS_TDEP_PCAL_LINE1_REF_A_TST': PCAL_LINE1_REF_A_TST,
            'CAL-CS_TDEP_PCAL_LINE1_REF_A_PUM': PCAL_LINE1_REF_A_PUM,
            'CAL-CS_TDEP_PCAL_LINE1_REF_A_UIM': PCAL_LINE1_REF_A_UIM,
            'CAL-CS_TDEP_PCAL_LINE3_CORRECTION': PCAL_LINE3_CORRECTION,
            'CAL-CS_TDEP_PCAL_LINE1_PCAL_DEMOD_PHASE': PCAL_LINE1_PCAL_DEMOD_PHASE,
            'CAL-CS_TDEP_PCAL_LINE2_PCAL_DEMOD_PHASE': PCAL_LINE2_PCAL_DEMOD_PHASE,
            'CAL-CS_TDEP_PCAL_LINE3_PCAL_DEMOD_PHASE': PCAL_LINE3_PCAL_DEMOD_PHASE,
            'CAL-CS_TDEP_PCAL_LINE4_PCAL_DEMOD_PHASE': PCAL_LINE4_PCAL_DEMOD_PHASE,
            'CAL-CS_TDEP_SUS_LINE1_SUS_DEMOD_PHASE': SUS_LINE1_SUS_DEMOD_PHASE,
            'CAL-CS_TDEP_SUS_LINE2_SUS_DEMOD_PHASE': SUS_LINE2_SUS_DEMOD_PHASE,
            'CAL-CS_TDEP_SUS_LINE3_SUS_DEMOD_PHASE': SUS_LINE3_SUS_DEMOD_PHASE,
        }

    def plot(self, plot_selection='all', freq_min=0.1, freq_max=5000, filename=None, ifo='',
             label=None, style=None, ugf_start=10, ugf_end=1000, show=None, **kwargs):
        """
        Make DARM critique plots.
        This method produces critique models for 1 or 2 models.

        PARAMETERS
        ----------
        args: The first argumets should be 1 or 2 darm models.
                  - darm model object (DARMModel)

        The plots produced should be close to the final critique plot, but if
        one needs something special there are a few options to tw
        Options for the graphs: - freq_min (float) start frequency
                                - freq_max (float) end frequency
                                - **kwargs, you can also use all the available
                                            matplotlib keywords, but have to be common
                                            for all graphs.
                                - filename (string)
                                  if given, ALL generated graphs will be saved in one pdf.
                                - ifo (string)
                                  if given with a model to plot, it will appear in the
                                  graph titles.
                                - ugf_start, ugf_end (float)
                                  frequency range used for the search of the UGF
                                - greed (bool)
                                - plot_selection (string)
                                  'all':
                                  'optical':
                                  'actuation':
                                  'clg':
                                  'olg':
                                  'digital':
        RETURNS
        -------
        Plots critique plots of the given darm model, and saves them in one pdf file.
        """

        critique(self, freq_min=freq_min, freq_max=freq_max, filename=filename, label=label,
                 plot_selection=plot_selection, ifo=ifo, show=show,
                 ugf_start=ugf_start, ugf_end=ugf_end, **kwargs)
