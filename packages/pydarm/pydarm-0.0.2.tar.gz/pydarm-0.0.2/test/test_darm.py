import unittest
import pydarm
import numpy as np


class TestComputeDigitalFilterResponse(unittest.TestCase):

    def setUp(self):
        # frequencies = np.logspace(0, np.log10(5000.), 10)
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_digital_filter_response = np.array(
            [-3513076500191.6504+3327250871150.924j,
             -164538201540.2522+209970221596.44916j,
             -3242877524.3140893-646390346.0757524j,
             3152750901.033689+60862553.6703552j,
             5968957387.406848+6106710482.173726j,
             17063001608.677845+14901038698.213606j,
             59173157596.065796-25364518140.6575j,
             -46407563930.73129+21858627480.823456j,
             -9021881.73649469-6742239.626013521j,
             -27770965.672582164+52593450.2554684j])

    def tearDown(self):
        del self.frequencies
        del self.known_digital_filter_response

    def test_compute_digital_filter_response(self):
        """ Test the DARM digital filter repsonse """
        D = pydarm.darm.DigitalModel('''
[metadata]
[interferometer]
[digital]
digital_filter_file = test/H1OMC_1239468752.txt
digital_filter_bank = LSC_DARM1, LSC_DARM2
digital_filter_modules_in_use = 1,2,3,4,7,9,10: 3,4,5,6,7
digital_filter_gain = 400,1
''')
        test_response = D.compute_response(
            self.frequencies)
        for n in range(len(self.frequencies)):
            # Requires investigation why this delta tolerance has to be higher
            # on some systems in order to pass.
            # Can test using print() to check output and call test using
            # pytest -s test/darm_test.py
            self.assertAlmostEqual(
                np.abs(test_response[n]) /
                np.abs(self.known_digital_filter_response[n]), 1.0)
            self.assertAlmostEqual(
                np.angle(test_response[n], deg=True) -
                np.angle(self.known_digital_filter_response[n], deg=True), 0.0,
                places=5)


class TestComputeDarmOlg(unittest.TestCase):

    def setUp(self):
        # frequencies = np.logspace(0, np.log10(5000.), 10)
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_olg = np.array(
            [-346589.7289879694+67697.98179370671j,
             -1859.4410636292505+7152.898242047175j,
             40.79712693912431-10.496083469022562j,
             -3.200667505597764+0.6749176141222187j,
             -1.0964382128049217-0.6352470027806889j,
             -0.48849524504067693-0.12453097698086546j,
             0.07580387098963454+0.20189845660408226j,
             -0.010730361938738586+0.010017089450759862j,
             1.1367097388995271e-07-1.7573024415341907e-07j,
             -1.8569508267009735e-08+2.419265648650538e-08j])

    def tearDown(self):
        del self.frequencies
        del self.known_olg

    def test_compute_darm_olg(self):
        """ Test DARM open loop gain response """
        darm = pydarm.darm.DARMModel('''
[sensing]
x_arm_length = 3994.4704
y_arm_length = 3994.4692
coupled_cavity_optical_gain = 3.22e6
coupled_cavity_pole_frequency = 410.6
detuned_spring_frequency = 4.468
detuned_spring_Q = 52.14
sensing_sign = 1
is_pro_spring = True
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
analog_anti_aliasing_file = test/H1aa.mat, test/H1aa.mat
omc_meas_p_trans_amplifier   = 13.7e3, 17.8e3: 13.7e3, 17.8e3
whitening_mode_names = test, test
omc_meas_p_whitening_test   = 11.346e3, 32.875e3, 32.875e3: 11.521e3, 32.863e3, 32.863e3
super_high_frequency_poles_apparent_delay = 0, 0
gain_ratio = 1, 1
balance_matrix = 1, 1
omc_path_names = A, B
single_pole_approximation_delay_correction = -12e-6
adc_gain = 1638.001638001638, 1638.001638001638
omc_compensation_filter_file = test/H1OMC_1239468752.txt
omc_compensation_filter_bank = OMC_DCPD_A, OMC_DCPD_B
omc_compensation_filter_modules_in_use = 4: 4
omc_compensation_filter_gain = 1, 1

[actuation_x_arm]
darm_feedback_sign = -1
tst_NpV2 = 4.427e-11
linearization = OFF
actuation_esd_bias_voltage = -9.3
suspension_file = test/H1susdata_O3.mat
tst_driver_meas_Z_UL = 129.7e3
tst_driver_meas_Z_LL = 90.74e3
tst_driver_meas_Z_UR = 93.52e3
tst_driver_meas_Z_LR = 131.5e3
tst_driver_meas_P_UL = 3.213e3, 31.5e3
tst_driver_meas_P_LL = 3.177e3, 26.7e3
tst_driver_meas_P_UR = 3.279e3, 26.6e3
tst_driver_meas_P_LR = 3.238e3, 31.6e3
tst_driver_DC_gain_VpV_HV = 40
tst_driver_DC_gain_VpV_LV = 1.881
anti_imaging_rate_string = 16k
anti_imaging_method = biquad
analog_anti_imaging_file = test/H1aa.mat
dac_gain = 7.62939453125e-05
unknown_actuation_delay = 15e-6
pum_driver_DC_trans_ApV = 2.6847e-4
pum_coil_outf_signflip = 1
pum_NpA = 0.02947
uim_driver_DC_trans_ApV = 6.1535e-4
uim_NpA = 1.634
sus_filter_file = test/H1SUSETMX_1236641144.txt
tst_isc_inf_bank = ETMX_L3_ISCINF_L
tst_isc_inf_modules =
tst_isc_inf_gain = 1.0
tst_lock_bank = ETMX_L3_LOCK_L
tst_lock_modules = 5,8,9,10
tst_lock_gain = 1.0
tst_drive_align_bank = ETMX_L3_DRIVEALIGN_L2L
tst_drive_align_modules = 4,5
tst_drive_align_gain = -35.7
pum_lock_bank = ETMX_L2_LOCK_L
pum_lock_modules = 7
pum_lock_gain = 23.0
pum_drive_align_bank = ETMX_L2_DRIVEALIGN_L2L
pum_drive_align_modules = 6,7
pum_drive_align_gain = 1.0
uim_lock_bank = ETMX_L1_LOCK_L
uim_lock_modules = 10
uim_lock_gain = 1.06
uim_drive_align_bank = ETMX_L1_DRIVEALIGN_L2L
uim_drive_align_modules =
uim_drive_align_gain = 1.0

[actuation]
darm_output_matrix = 1.0, -1.0, 0.0, 0.0
darm_feedback_x = OFF, ON, ON, ON
darm_feedback_y = OFF, OFF, OFF, OFF

[digital]
digital_filter_file = test/H1OMC_1239468752.txt
digital_filter_bank = LSC_DARM1, LSC_DARM2
digital_filter_modules_in_use = 1,2,3,4,7,9,10: 3,4,5,6,7
digital_filter_gain = 400,1
''')
        test_olg = darm.compute_darm_olg(self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(test_olg[n]) / np.abs(self.known_olg[n]), 1.0)
            self.assertAlmostEqual(
                np.angle(test_olg[n], deg=True) -
                np.angle(self.known_olg[n], deg=True), 0.0, places=5)


class TestComputeResponseFunction(unittest.TestCase):

    def setUp(self):
        # frequencies = np.logspace(0, np.log10(5000.), 10)
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_response = np.array(
            [2.0406181004597967-0.4013213677915312j,
             0.0011220990463462926-0.004469979302356652j,
             7.174381300234404e-06-1.4617952572908577e-06j,
             -6.479990333472527e-07+1.5653156901534748e-07j,
             -1.3662040618868035e-09-1.9861756619000937e-07j,
             1.6810351811864666e-07+2.0548446256238736e-08j,
             2.1237360469410807e-07+3.590194203666282e-07j,
             -7.07952406495893e-08+6.371681259820066e-07j,
             -1.4643321723110076e-06+3.0336488559992614e-07j,
             4.465169869308327e-06-1.5260050031500522e-06j])

    def tearDown(self):
        del self.frequencies
        del self.known_response

    def test_compute_darm_response_function(self):
        """ Test DARM closed loop response function """
        model_string = '''
[metadata]
[interferometer]
[sensing]
x_arm_length = 3994.4704
y_arm_length = 3994.4692
coupled_cavity_optical_gain = 3.22e6
coupled_cavity_pole_frequency = 410.6
detuned_spring_frequency = 4.468
detuned_spring_Q = 52.14
sensing_sign = 1
is_pro_spring = True
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
analog_anti_aliasing_file = test/H1aa.mat, test/H1aa.mat
omc_meas_p_trans_amplifier   = 13.7e3, 17.8e3: 13.7e3, 17.8e3
whitening_mode_names = test, test
omc_meas_p_whitening_test   = 11.346e3, 32.875e3, 32.875e3: 11.521e3, 32.863e3, 32.863e3
super_high_frequency_poles_apparent_delay = 0, 0
gain_ratio = 1, 1
balance_matrix = 1, 1
omc_path_names = A, B
single_pole_approximation_delay_correction = -12e-6
adc_gain = 1, 1

[actuation_x_arm]
darm_feedback_sign = -1
tst_NpV2 = 4.427e-11
linearization = OFF
actuation_esd_bias_voltage = -9.3
suspension_file = test/H1susdata_O3.mat
tst_driver_meas_Z_UL = 129.7e3
tst_driver_meas_Z_LL = 90.74e3
tst_driver_meas_Z_UR = 93.52e3
tst_driver_meas_Z_LR = 131.5e3
tst_driver_meas_P_UL = 3.213e3, 31.5e3
tst_driver_meas_P_LL = 3.177e3, 26.7e3
tst_driver_meas_P_UR = 3.279e3, 26.6e3
tst_driver_meas_P_LR = 3.238e3, 31.6e3
tst_driver_DC_gain_VpV_HV = 40
tst_driver_DC_gain_VpV_LV = 1.881
anti_imaging_rate_string = 16k
anti_imaging_method = biquad
analog_anti_imaging_file = test/H1aa.mat
dac_gain = 7.62939453125e-05
unknown_actuation_delay = 15e-6
pum_driver_DC_trans_ApV = 2.6847e-4
pum_coil_outf_signflip = 1
pum_NpA = 0.02947
uim_driver_DC_trans_ApV = 6.1535e-4
uim_NpA = 1.634
sus_filter_file = test/H1SUSETMX_1236641144.txt
tst_isc_inf_bank = ETMX_L3_ISCINF_L
tst_isc_inf_modules =
tst_isc_inf_gain = 1.0
tst_lock_bank = ETMX_L3_LOCK_L
tst_lock_modules = 5,8,9,10
tst_lock_gain = 1.0
tst_drive_align_bank = ETMX_L3_DRIVEALIGN_L2L
tst_drive_align_modules = 4,5
tst_drive_align_gain = -35.7
pum_lock_bank = ETMX_L2_LOCK_L
pum_lock_modules = 7
pum_lock_gain = 23.0
pum_drive_align_bank = ETMX_L2_DRIVEALIGN_L2L
pum_drive_align_modules = 6,7
pum_drive_align_gain = 1.0
uim_lock_bank = ETMX_L1_LOCK_L
uim_lock_modules = 10
uim_lock_gain = 1.06
uim_drive_align_bank = ETMX_L1_DRIVEALIGN_L2L
uim_drive_align_modules =
uim_drive_align_gain = 1.0

[actuation]
darm_output_matrix = 1.0, -1.0, 0.0, 0.0
darm_feedback_x = OFF, ON, ON, ON
darm_feedback_y = OFF, OFF, OFF, OFF

[digital]
digital_filter_file = test/H1OMC_1239468752.txt
digital_filter_bank = LSC_DARM1, LSC_DARM2
digital_filter_modules_in_use = 1,2,3,4,7,9,10: 3,4,5,6,7
digital_filter_gain = 400,1
'''
        darm = pydarm.darm.DARMModel(model_string)
        test_response = darm.compute_response_function(self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(test_response[n]) / np.abs(self.known_response[n]), 1.0)
            self.assertAlmostEqual(
                np.angle(test_response[n], deg=True) -
                np.angle(self.known_response[n], deg=True), 0.0, places=5)


class TestComputeEpicsRecords(unittest.TestCase):

    def setUp(self):
        self.frequencies = np.array(
            [17.1, 15.6, 16.4, 17.6, 410.3, 1083.7, 7.93])
        self.known_epics = {
            'CAL-CS_TDEP_PCAL_LINE1_CORRECTION':
            0.003384106838174459+0.0004044180029064908j,
            'CAL-CS_TDEP_SUS_LINE3_REF_INVA_TST_RESPRATIO':
            1196925220371225.5-3841998698753872j,
            'CAL-CS_TDEP_SUS_LINE2_REF_INVA_PUM_RESPRATIO':
            -4.90204412692278e+17-1.9987201437993693e+17j,
            'CAL-CS_TDEP_SUS_LINE1_REF_INVA_UIM_RESPRATIO':
            2.643473241664109e+17-1.2695297228124422e+17j,
            'CAL-CS_TDEP_PCAL_LINE2_REF_C_NOCAVPOLE':
            3052033.7355621597-1030751.4694586383j,
            'CAL-CS_TDEP_PCAL_LINE2_REF_D':
            -243010006.4310854-1207741923.4087756j,
            'CAL-CS_TDEP_PCAL_LINE2_REF_A_TST':
            -3.6301159301930236e-19+5.17252131286287e-19j,
            'CAL-CS_TDEP_PCAL_LINE2_REF_A_PUM':
            -3.486603813748813e-21+2.854144501791321e-21j,
            'CAL-CS_TDEP_PCAL_LINE2_REF_A_UIM':
            9.669640696236252e-23+1.0084874176645285e-22j,
            'CAL-CS_TDEP_PCAL_LINE2_CORRECTION':
            5.919275925544666e-06+3.317567316630787e-07j,
            'CAL-CS_TDEP_PCAL_LINE4_REF_C_NOCAVPOLE':
            3219939.105380994-20248.45691682977j,
            'CAL-CS_TDEP_PCAL_LINE4_REF_D':
            -1334010103.6339288-1921974046.2409313j,
            'CAL-CS_TDEP_PCAL_LINE4_REF_A_TST':
            3.868595124883083e-17-7.793733735356113e-16j,
            'CAL-CS_TDEP_PCAL_LINE4_REF_A_PUM':
            -1.6867571291492549e-15+9.32181952713231e-16j,
            'CAL-CS_TDEP_PCAL_LINE4_REF_A_UIM':
            2.420118862241151e-16+3.3925102853622382e-16j,
            'CAL-CS_TDEP_PCAL_LINE4_CORRECTION':
            0.015159268559718102+0.003900900009459194j,
            'CAL-CS_TDEP_PCAL_LINE1_REF_C_NOCAVPOLE':
            3219708.6791652623-43662.16666949552j,
            'CAL-CS_TDEP_PCAL_LINE1_REF_D':
            3152795532.787565+60933868.87924543j,
            'CAL-CS_TDEP_PCAL_LINE1_REF_A_TST':
            -1.1944749080760831e-16-2.1720205784065532e-16j,
            'CAL-CS_TDEP_PCAL_LINE1_REF_A_PUM':
            -2.1758869487866404e-16+2.620157641796169e-16j,
            'CAL-CS_TDEP_PCAL_LINE1_REF_A_UIM':
            4.078008711853952e-17+4.992745126138772e-18j,
            'CAL-CS_TDEP_PCAL_LINE3_CORRECTION':
            8.319363469674813e-07+1.1949591405958398e-07j,
            'CAL-CS_TDEP_PCAL_LINE1_PCAL_DEMOD_PHASE': -0.37573242187500006,
            'CAL-CS_TDEP_PCAL_LINE2_PCAL_DEMOD_PHASE': -9.015380859375002,
            'CAL-CS_TDEP_PCAL_LINE3_PCAL_DEMOD_PHASE': -23.811767578125,
            'CAL-CS_TDEP_PCAL_LINE4_PCAL_DEMOD_PHASE': -0.17424316406249998,
            'CAL-CS_TDEP_SUS_LINE1_SUS_DEMOD_PHASE': -0.3427734375,
            'CAL-CS_TDEP_SUS_LINE2_SUS_DEMOD_PHASE': -0.36035156249999994,
            'CAL-CS_TDEP_SUS_LINE3_SUS_DEMOD_PHASE': -0.38671875}

    def tearDown(self):
        del self.frequencies
        del self.known_epics

    def test_compute_epics_records(self):
        model_string = '''
[metadata]
[interferometer]
[sensing]
x_arm_length = 3994.4704
y_arm_length = 3994.4692
coupled_cavity_optical_gain = 3.22e6
coupled_cavity_pole_frequency = 410.6
detuned_spring_frequency = 4.468
detuned_spring_Q = 52.14
sensing_sign = 1
is_pro_spring = True
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
analog_anti_aliasing_file = test/H1aa.mat, test/H1aa.mat
omc_meas_p_trans_amplifier   = 13.7e3, 17.8e3: 13.7e3, 17.8e3
whitening_mode_names = test, test
omc_meas_p_whitening_test   = 11.346e3, 32.875e3, 32.875e3: 11.521e3, 32.863e3, 32.863e3
super_high_frequency_poles_apparent_delay = 0, 0
gain_ratio = 1, 1
balance_matrix = 1, 1
omc_path_names = A, B
single_pole_approximation_delay_correction = -12e-6
adc_gain = 1, 1

[actuation_x_arm]
darm_feedback_sign = -1
tst_NpV2 = 4.427e-11
linearization = OFF
actuation_esd_bias_voltage = -9.3
suspension_file = test/H1susdata_O3.mat
tst_driver_meas_Z_UL = 129.7e3
tst_driver_meas_Z_LL = 90.74e3
tst_driver_meas_Z_UR = 93.52e3
tst_driver_meas_Z_LR = 131.5e3
tst_driver_meas_P_UL = 3.213e3, 31.5e3
tst_driver_meas_P_LL = 3.177e3, 26.7e3
tst_driver_meas_P_UR = 3.279e3, 26.6e3
tst_driver_meas_P_LR = 3.238e3, 31.6e3
tst_driver_DC_gain_VpV_HV = 40
tst_driver_DC_gain_VpV_LV = 1.881
anti_imaging_rate_string = 16k
anti_imaging_method = biquad
analog_anti_imaging_file = test/H1aa.mat
dac_gain = 7.62939453125e-05
unknown_actuation_delay = 15e-6
pum_driver_DC_trans_ApV = 2.6847e-4
pum_coil_outf_signflip = 1
pum_NpA = 0.02947
uim_driver_DC_trans_ApV = 6.1535e-4
uim_NpA = 1.634
sus_filter_file = test/H1SUSETMX_1236641144.txt
tst_isc_inf_bank = ETMX_L3_ISCINF_L
tst_isc_inf_modules =
tst_isc_inf_gain = 1.0
tst_lock_bank = ETMX_L3_LOCK_L
tst_lock_modules = 5,8,9,10
tst_lock_gain = 1.0
tst_drive_align_bank = ETMX_L3_DRIVEALIGN_L2L
tst_drive_align_modules = 4,5
tst_drive_align_gain = -35.7
pum_lock_bank = ETMX_L2_LOCK_L
pum_lock_modules = 7
pum_lock_gain = 23.0
pum_drive_align_bank = ETMX_L2_DRIVEALIGN_L2L
pum_drive_align_modules = 6,7
pum_drive_align_gain = 1.0
uim_lock_bank = ETMX_L1_LOCK_L
uim_lock_modules = 10
uim_lock_gain = 1.06
uim_drive_align_bank = ETMX_L1_DRIVEALIGN_L2L
uim_drive_align_modules =
uim_drive_align_gain = 1.0

[actuation]
darm_output_matrix = 1.0, -1.0, 0.0, 0.0
darm_feedback_x = OFF, ON, ON, ON
darm_feedback_y = OFF, OFF, OFF, OFF

[pcal]
pcal_dewhiten = 1.0, 1.0
ref_pcal_2_darm_act_sign = -1
analog_anti_aliasing_file = test/H1aa.mat
anti_aliasing_rate_string = 16k
anti_aliasing_method = biquad

[digital]
digital_filter_file = test/H1OMC_1239468752.txt
digital_filter_bank = LSC_DARM1, LSC_DARM2
digital_filter_modules_in_use = 1,2,3,4,7,9,10: 3,4,5,6,7
digital_filter_gain = 400,1
'''
        darm = pydarm.darm.DARMModel(model_string)
        test_epics = darm.compute_epics_records(
            self.frequencies[0], self.frequencies[1], self.frequencies[2],
            self.frequencies[3], self.frequencies[4], self.frequencies[5],
            self.frequencies[6], arm='x')
        for idx, (key, val) in enumerate(self.known_epics.items()):
            self.assertAlmostEqual(
                np.abs(test_epics[key]/self.known_epics[key]), 1.0, places=6)
            self.assertAlmostEqual(
                np.angle(test_epics[key], deg=True) -
                np.angle(self.known_epics[key], deg=True), 0.0, places=5)


if __name__ == '__main__':
    unittest.main()
