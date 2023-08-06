import unittest
import pydarm
import numpy as np


class TestDigitalOutToDisplacement(unittest.TestCase):

    def setUp(self):
        self.frequencies = np.logspace(0, np.log10(5000), 10)
        self.known_uim = np.array(
            [-3.2384137e-11+1.483989e-10j,
             -2.188945972686536e-13-1.2821508810405059e-13j,
             -8.234200643560679e-16+1.1169244294905415e-17j,
             -2.2717420347907865e-18+3.807342138536326e-20j,
             -7.726119625430656e-21+2.8214932702925883e-22j,
             -3.069732345677177e-23+2.802950992149116e-24j,
             -3.704319539709616e-25+8.513701178490709e-26j,
             -5.653288121207401e-27+2.7782015024014825e-27j,
             -1.5560945676686243e-31+2.607011234489723e-32j,
             -9.098758961097676e-36-9.111012675704881e-38j])
        self.known_pum = np.array(
            [-5.4778843e-13+1.4553857e-12j,
             6.1674380978210205e-15+3.4762120220135732e-16j,
             8.921932231901915e-17+2.2792783479902217e-20j,
             1.9323859014810564e-18+1.0535512865143826e-22j,
             4.400811235483015e-20-6.018608690596686e-24j,
             1.0685095149460138e-21-5.042308039593894e-25j,
             4.081625444413661e-23-6.30387648126196e-26j,
             -2.1494074798072415e-24+3.4967578294744665e-27j,
             -1.5121705995043745e-24+1.300063249989611e-24j,
             7.827170138404585e-30+6.024637399728448e-33j])
        self.known_tst = np.array(
            [2.0621199e-15+8.4896537e-15j,
             4.89214604312554e-16-9.01637436812509e-20j,
             6.918986659580851e-17-1.3207006022659344e-19j,
             1.0338241669028436e-17-5.271193383475367e-20j,
             1.5553903186367166e-18-2.0538433774482745e-20j,
             2.340140539847166e-19-7.96916836082613e-21j,
             3.4987150429586586e-20-3.0743642439267104e-21j,
             5.00747100100983e-21-1.1451048744099044e-21j,
             5.384311898907294e-22-3.4040562248054892e-22j,
             5.6616355059267466e-24-2.2891454307309875e-23j])

    def tearDown(self):
        del self.frequencies
        del self.known_uim
        del self.known_pum
        del self.known_tst

    def test_digital_out_to_displacement(self):
        calcs = pydarm.calcs.CALCSModel('''
[metadata]
[interferometer]
[digital]
[sensing]
[actuation]
[calcs]
xarm_uim_analog = test/H1CALCS_ETMX_L1_ANALOG.txt
xarm_pum_analog = test/H1CALCS_ETMX_L2_ANALOG.txt
xarm_tst_analog = test/H1CALCS_ETMX_L3_ANALOG.txt
xarm_output_matrix = 0.0, -1.0, -1.0, -1.0
''')
        test_val = calcs.digital_out_to_displacement(self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(np.abs(test_val[0][n]) /
                                   np.abs(self.known_uim[n]), 1)
            self.assertAlmostEqual(np.angle(test_val[0][n], deg=True),
                                   np.angle(self.known_uim[n], deg=True))
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(np.abs(test_val[1][n]) /
                                   np.abs(self.known_pum[n]), 1)
            self.assertAlmostEqual(np.angle(test_val[1][n], deg=True),
                                   np.angle(self.known_pum[n], deg=True))
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(np.abs(test_val[2][n]) /
                                   np.abs(self.known_tst[n]), 1)
            self.assertAlmostEqual(np.angle(test_val[2][n], deg=True),
                                   np.angle(self.known_tst[n], deg=True))


class TestGdsSensingCorrection(unittest.TestCase):

    def setUp(self):
        # Pre-computed values
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_gds_correction = np.array(
            [0.9690033852334485+0.20365794827583145j,
             0.9927987646118267+0.10720767795338881j,
             0.9995343186109982-0.02522505158501547j,
             0.9998404602187019-0.020026699698845397j,
             0.9986274140857612-0.05337950666950692j,
             0.990340781284894-0.13838726808361723j,
             0.9366306998135968-0.3499516654414869j,
             0.6085919634346818-0.7993628692627002j,
             -0.7703530428602053-0.7046255544033636j,
             1.0438558226239525-0.4323558661431118j])

    def tearDown(self):
        del self.frequencies
        del self.known_gds_correction

    def test_gds_correction(self):
        """ Test the computation of the GDS correction """
        calcs = pydarm.calcs.CALCSModel('''
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
gain_ratio = 1, 1
balance_matrix = 1, 1
omc_path_names = A, B
single_pole_approximation_delay_correction = -12e-6
super_high_frequency_poles_apparent_delay = 0, 0
adc_gain = 1638.001638001638, 1638.001638001638
omc_compensation_filter_file = test/H1OMC_1239468752.txt
omc_compensation_filter_bank = OMC_DCPD_A, OMC_DCPD_B
omc_compensation_filter_modules_in_use = 4: 4
omc_compensation_filter_gain = 1, 1
[calcs]
foton_invsensing_tf = \
  test/2019-04-04_H1CALCS_InverseSensingFunction_Foton_SRCD-2N_Gain_tf.txt
[actuation]
[digital]
''')
        gds_corr = calcs.gds_sensing_correction(self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(gds_corr[n]), np.abs(self.known_gds_correction[n]))
            self.assertAlmostEqual(
                np.angle(gds_corr[n], deg=True),
                np.angle(self.known_gds_correction[n], deg=True))


class TestGdsActuationCorrection(unittest.TestCase):

    def setUp(self):
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_gds_correction = np.array(
            [0.8404488998343337-0.022545686714606425j,
             0.9908290951853058+0.001861584876492708j,
             0.9907789577670048+0.003548405194091888j,
             0.9906872359775547+0.00879715846913863j,
             0.9901223467767045+0.022559519681502986j,
             0.9864104022073169+0.05857374075130294j,
             0.9631144733694313+0.15905228767814172j,
             0.8408664107673387+0.5034878332334102j,
             -1.1858038780396527-1.5941855321764649j,
             -1981.4519437513227+6029.303646102826j])

    def tearDown(self):
        del self.frequencies
        del self.known_gds_correction

    def test_gds_actuation_correction(self):
        model_string = '''
[metadata]
[interferometer]
[sensing]
[digital]
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
[calcs]
xarm_tst_analog = test/H1CALCS_ETMX_L3_ANALOG.txt
xarm_output_matrix = 0.0, 0.0, 0.0, -1.0
'''
        calcs = pydarm.calcs.CALCSModel(model_string)
        gds_corr = calcs.gds_actuation_correction(self.frequencies, arm='xarm',
                                                 stage='TST')
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(gds_corr[n]) / np.abs(self.known_gds_correction[n]),
                1.0)
            self.assertAlmostEqual(
                np.angle(gds_corr[n], deg=True),
                np.angle(self.known_gds_correction[n], deg=True))


class TestCalcsDarmActuation(unittest.TestCase):

    def setUp(self):
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_actuation = np.array(
            [-4.517003985979567e-13-2.5739820500242955e-13j,
             -1.588289401731322e-14+6.31941977517119e-15j,
             -2.012475480149785e-15+8.315600546471824e-16j,
             -3.014208282446126e-16+4.06904159579703e-17j,
             -4.6223086310101606e-17+2.3550867748198696e-18j,
             -7.195838704691822e-18-7.07001181949773e-19j,
             -1.2716665575478529e-18+1.9470486466093807e-19j,
             -1.6724226841165708e-19+7.778226870607795e-20j,
             -1.2327261604799712e-21+2.4979036114116563e-20j,
             -7.960313078495676e-22+4.1624706852500895e-22j])

    def tearDown(self):
        del self.frequencies
        del self.known_actuation

    def test_calcs_darm_actuation(self):
        calcs = pydarm.calcs.CALCSModel('''
[metadata]
[interferometer]
[sensing]
[digital]
[actuation]
darm_output_matrix = 1.0, -1.0, 0.0, 0.0
darm_feedback_x = OFF, ON, ON, ON
darm_feedback_y = OFF, OFF, OFF, OFF
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
[calcs]
xarm_uim_analog = test/H1CALCS_ETMX_L1_ANALOG.txt
xarm_pum_analog = test/H1CALCS_ETMX_L2_ANALOG.txt
xarm_tst_analog = test/H1CALCS_ETMX_L3_ANALOG.txt
xarm_output_matrix = 0.0, -1.0, -1.0, -1.0
''')
        test_actuation = calcs.calcs_darm_actuation(self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs((test_actuation[n]) /
                        np.abs(self.known_actuation[n])), 1)
            self.assertAlmostEqual(
                np.angle(test_actuation[n], deg=True),
                np.angle(self.known_actuation[n], deg=True))


class TestResidualSensingSimDelay(unittest.TestCase):

    def setUp(self):
        self.frequencies = np.logspace(1, np.log10(2000), 10)
        self.known_delay_clock = 2.0
        self.known_residual = np.array(
            [-0.0002599549829148569,
             -0.0004683671560390401,
             -0.0008439481877466903,
             -0.001521172222149647,
             -0.0027445617215542534,
             -0.004967805924162266,
             -0.009085228950770963,
             -0.017159067181484577,
             -0.035558432561595854,
             -0.09134727188320468])

    def tearDown(self):
        del self.frequencies
        del self.known_delay_clock
        del self.known_residual

    def test_residual_sensing_sim_delay(self):
        calcs = pydarm.calcs.CALCSModel('''
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
gain_ratio = 1, 1
balance_matrix = 1, 1
omc_path_names = A, B
single_pole_approximation_delay_correction = -12e-6
super_high_frequency_poles_apparent_delay = 0, 0
adc_gain = 1638.001638001638, 1638.001638001638
omc_compensation_filter_file = test/H1OMC_1239468752.txt
omc_compensation_filter_bank = OMC_DCPD_A, OMC_DCPD_B
omc_compensation_filter_modules_in_use = 4: 4
omc_compensation_filter_gain = 1, 1
[calcs]
foton_invsensing_tf = \
  test/2019-04-04_H1CALCS_InverseSensingFunction_Foton_SRCD-2N_Gain_tf.txt
[actuation]
[digital]
''')
        delay, resid = calcs.residual_sensing_sim_delay(
            self.frequencies, True)
        self.assertAlmostEqual(delay / self.known_delay_clock, 1)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(resid[n] / self.known_residual[n], 1)


class TestResidualActuationSimDelay(unittest.TestCase):

    def setUp(self):
        self.frequencies = np.logspace(np.log10(20), np.log10(100), 10)
        self.known_delay_clock = 5.0
        self.known_residual = np.array(
            [0.0022960052374513124,
             0.004385542965465158,
             0.005768518798942149,
             0.006605530426938483,
             0.007230000719800206,
             0.00785839433869226,
             0.008620916182953034,
             0.00961709910221882,
             0.010968032356544699,
             0.013005931495730039])

    def tearDown(self):
        del self.frequencies
        del self.known_delay_clock
        del self.known_residual

    def test_residual_actuation_sim_delay(self):
        calcs = pydarm.calcs.CALCSModel('''
[metadata]
[interferometer]
[sensing]
[digital]
[actuation]
darm_output_matrix = 1.0, -1.0, 0.0, 0.0
darm_feedback_x = OFF, ON, ON, ON
darm_feedback_y = OFF, OFF, OFF, OFF
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
[calcs]
xarm_uim_analog = test/H1CALCS_ETMX_L1_ANALOG.txt
xarm_pum_analog = test/H1CALCS_ETMX_L2_ANALOG.txt
xarm_tst_analog = test/H1CALCS_ETMX_L3_ANALOG.txt
xarm_output_matrix = 0.0, -1.0, -1.0, -1.0
''')
        delay, resid = calcs.residual_actuation_sim_delay(
            self.frequencies, True)
        self.assertAlmostEqual(delay / self.known_delay_clock, 1)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(resid[n] / self.known_residual[n], 1)


class TestCalcsDttCalibration(unittest.TestCase):

    def setUp(self):
        # Pre-computed values
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_dtt_calibration = np.array(
            [0.00019355937169565073-0.00042493504315625405j,
             -9.45217382540534e-07-2.284500637532835e-06j,
             1.779965780007878e-10-9.718222697085616e-09j,
             6.618139747982113e-11+6.655385100436983e-12j,
             -3.0537832562235266e-12+9.777348752549816e-13j,
             1.7321383343635742e-13-1.2481618669283242e-12j,
             9.817239462985217e-13-2.360955109821865e-13j,
             7.728766895114454e-13+6.281613267148073e-13j,
             -6.47936524092584e-13+7.062114699132063e-13j,
             8.255796530695559e-13+3.1897090218792677e-13j])

    def tearDown(self):
        del self.frequencies
        del self.known_dtt_calibration

    def test_calcs_dtt_calibration(self):
        calcs = pydarm.calcs.CALCSModel('''
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
gain_ratio = 1, 1
balance_matrix = 1, 1
omc_path_names = A, B
single_pole_approximation_delay_correction = -12e-6
super_high_frequency_poles_apparent_delay = 0, 0
adc_gain = 1638.001638001638, 1638.001638001638
omc_compensation_filter_file = test/H1OMC_1239468752.txt
omc_compensation_filter_bank = OMC_DCPD_A, OMC_DCPD_B
omc_compensation_filter_modules_in_use = 4: 4
omc_compensation_filter_gain = 1, 1
[digital]
digital_filter_file = test/H1OMC_1239468752.txt
digital_filter_bank = LSC_DARM1, LSC_DARM2
digital_filter_modules_in_use = 1,2,3,4,7,9,10: 3,4,5,6,7
digital_filter_gain = 400,1
[actuation]
darm_output_matrix = 1.0, -1.0, 0.0, 0.0
darm_feedback_x = OFF, ON, ON, ON
darm_feedback_y = OFF, OFF, OFF, OFF
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
[calcs]
foton_invsensing_tf = \
  test/2019-04-04_H1CALCS_InverseSensingFunction_Foton_SRCD-2N_Gain_tf.txt
foton_deltal_whitening_tf = \
  test/H1CALCS_DELTAL_EXTERNAL_WHITENING_tf.txt
xarm_uim_analog = test/H1CALCS_ETMX_L1_ANALOG.txt
xarm_pum_analog = test/H1CALCS_ETMX_L2_ANALOG.txt
xarm_tst_analog = test/H1CALCS_ETMX_L3_ANALOG.txt
xarm_output_matrix = 0.0, -1.0, -1.0, -1.0
foton_delay_filter_tf = test/H1CALCS_8_CLK_DELAY.txt
''')

        calcs_dtt_calib = calcs.calcs_dtt_calibration(self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs((calcs_dtt_calib[n]) /
                        np.abs(self.known_dtt_calibration[n])), 1)
            self.assertAlmostEqual(
                np.angle(calcs_dtt_calib[n], deg=True),
                np.angle(self.known_dtt_calibration[n], deg=True))


if __name__ == '__main__':
    unittest.main()
