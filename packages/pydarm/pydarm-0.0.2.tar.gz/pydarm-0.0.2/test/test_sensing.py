import unittest
import pydarm
import numpy as np


class TestOpticalResponse(unittest.TestCase):

    def setUp(self):
        # Pre-computed values from an optical plant with
        # f_cc = 400 Hz, f_s = 1 Hz, Q = 10 (anti-spring)
        # And frequencies = np.logspace(0, np.log10(5000.), 10)
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_optical_response = np.array(
            [0.4988123437694849+0.023690625000925447j,
             0.8682289568018182+0.023690785759931294j,
             0.9775621260186113-0.0018192134833768408j,
             0.9949877935396494-0.03672708739347625j,
             0.9877484188511914-0.10651841758830315j,
             0.9256481649097499-0.26176414634118933j,
             0.6518895845322998-0.47619218998268714j,
             0.21999081206271484-0.41417325269496474j,
             0.04075815123481037-0.19770363308768762j,
             0.006360890045023226-0.0794911255643983j])
        optical_response_model = [400, 1, 10]
        self.optical_response = pydarm.sensing.SensingModel.optical_response(
            optical_response_model[0], optical_response_model[1],
            optical_response_model[2], pro_spring=False)

    def tearDown(self):
        del self.frequencies
        del self.known_optical_response
        del self.optical_response

    def test_optical_response(self):
        """ Test the optical plant model """
        optical_response_freqresp = pydarm.utils.freqrespZPK(
            self.optical_response, 2.0*np.pi*self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(np.abs(optical_response_freqresp[n]),
                                   np.abs(self.known_optical_response[n]))
            self.assertAlmostEqual(
                np.angle(optical_response_freqresp[n], deg=True),
                np.angle(self.known_optical_response[n], deg=True))


class TestOMCAnalaogDCPDReadoutResponse(unittest.TestCase):

    def setUp(self):
        # Pre-computed values
        # omc_meas_p_trans_amplifier_A   = 13.7e3, 17.8e3
        # omc_meas_p_trans_whitening_A = \
        #     11.346e3, 32.875e3, 32.875e3
        # analog_anti_aliasing_file_A = Common/pyDARM/H1aa.mat
        # frequencies = np.logspace(0, np.log10(5000.), 10)
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_analog_response = np.array(
            [0.9999998536665746-0.0005167286242298383j,
             0.9999990287350008-0.00133124823161614j,
             0.9999935534012022-0.003429689154918376j,
             0.9999572121767486-0.008835784518168556j,
             0.9997160196619771-0.02276144831389675j,
             0.998115856554862-0.0586028191391922j,
             0.9875263088271709-0.15033813445138738j,
             0.9186003414470439-0.3765222040547237j,
             0.5164527749967376-0.8019627240716991j,
             -0.617879650294782-0.4291979256047118j])

    def tearDown(self):
        del self.frequencies
        del self.known_analog_response

    def test_omc_analog_dcpd_readout_response(self):
        """ Test the uncompensated OMC DCPD poles response """
        C = pydarm.sensing.SensingModel('''
[metadata]
[interferometer]
[sensing]
omc_path_names = A
omc_meas_p_trans_amplifier = 13.7e3, 17.8e3
whitening_mode_names = test
omc_meas_p_whitening_test = 11.346e3, 32.875e3, 32.875e3
super_high_frequency_poles_apparent_delay = 0
analog_anti_aliasing_file = test/H1aa.mat
''')
        analog_dcpd_response = C.omc_analog_dcpd_readout_response('A',
            self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(analog_dcpd_response[n]),
                np.abs(self.known_analog_response[n]))
            self.assertAlmostEqual(
                np.angle(analog_dcpd_response[n], deg=True),
                np.angle(self.known_analog_response[n], deg=True))


class TestOMCDigitalCompensationResponse(unittest.TestCase):

    def setUp(self):
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_digital_response = np.array(
            [0.00031477507457620236-0.00041932541064786685j,
             6.351752486888009e-06-0.0002512689712022434j,
             -3.998380486351784e-05-6.492346501958175e-05j,
             -1.0702299095113614e-05-1.0070777528904742e-05j,
             -1.2659064264492532e-06-2.4689933152042374e-06j,
             3.0955872674940336e-07-8.70312552324717e-07j,
             5.502073347929391e-07-3.3236246245694016e-07j,
             5.865370982993107e-07-1.2794394638990852e-07j,
             5.920112453308542e-07-4.7663182537616464e-08j,
             5.928278462061573e-07-1.3059142838018548e-08j])

    def tearDown(self):
        del self.frequencies
        del self.known_digital_response

    def test_omc_digital_compensation_response(self):
        C = pydarm.sensing.SensingModel('''
[metadata]
[interferometer]
[sensing]
omc_path_names = A
omc_compensation_filter_file = test/H1OMC_1239468752.txt
omc_compensation_filter_bank = OMC_DCPD_A
omc_compensation_filter_modules_in_use = 1,4,5,7
omc_compensation_filter_gain = 1000
''')
        digital_compensation_response = C.omc_digital_compensation_response('A',
            self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(digital_compensation_response[n]),
                np.abs(self.known_digital_response[n]))
            self.assertAlmostEqual(
                np.angle(digital_compensation_response[n], deg=True),
                np.angle(self.known_digital_response[n], deg=True))


class TestOmcPathResponse(unittest.TestCase):

    def setUp(self):
        # Pre-computed values
        # omc_meas_p_trans_amplifier_A   = 13.7e3, 17.8e3
        # omc_meas_p_trans_whitening_A = \
        #     11.346e3, 32.875e3, 32.875e3
        # gain_ratio_A = 1
        # balance_matrix_A = 1
        # anti_aliasing_rate_string = 16k
        # anti_aliasing_method      = biquad
        # analog_anti_aliasing_file_A = test/H1aa.mat
        # frequencies = np.logspace(0, np.log10(5000.), 10)
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_response = np.array(
            [1.0000003891873206-0.0007853244803941936j,
             0.9999986653249536-0.0020232314749344927j,
             0.9999872235010034-0.005212435716577928j,
             0.9999112811210966-0.013428491813741426j,
             0.9994072604116898-0.03459048056077152j,
             0.996063400254325-0.08902383023813454j,
             0.9739348784621216-0.22778552216162168j,
             0.8299851258734532-0.5601596601010437j,
             0.010770373018644919-1.0030495286483354j,
             -0.2267642153914641+0.7704794442924117j])

    def tearDown(self):
        del self.frequencies
        del self.known_response

    def test_omc_path_response(self):
        """ Test the OMC DCPD path response """
        C = pydarm.sensing.SensingModel('''
[metadata]
[interferometer]
[sensing]
omc_path_names = A
omc_meas_z_trans_amplifier =
omc_meas_p_trans_amplifier = 13.7e3, 17.8e3
whitening_mode_names = test
omc_meas_z_whitening_test =
omc_meas_p_whitening_test = 11.346e3, 32.875e3, 32.875e3
super_high_frequency_poles_apparent_delay = 0
analog_anti_aliasing_file = test/H1aa.mat
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
gain_ratio = 1
balance_matrix = 1
adc_gain = 1638.001638001638
omc_compensation_filter_file = test/H1OMC_1239468752.txt
omc_compensation_filter_bank = OMC_DCPD_A
omc_compensation_filter_modules_in_use = 4
omc_compensation_filter_gain = 1
''')
        omc_dcpd_response = C.omc_path_response('A', self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(omc_dcpd_response[n]),
                np.abs(self.known_response[n]))
            self.assertAlmostEqual(
                np.angle(omc_dcpd_response[n], deg=True),
                np.angle(self.known_response[n], deg=True))


class TestCombinePathResponses(unittest.TestCase):

    def setUp(self):
        # Pre-computed values
        # omc_meas_p_trans_amplifier_A   = 13.7e3, 17.8e3
        # omc_meas_p_trans_amplifier_B   = 13.7e3, 17.8e3
        # omc_meas_p_trans_whitening_A = \
        #     11.346e3, 32.875e3, 32.875e3
        # omc_meas_p_trans_whitening_B = \
        #     11.521e3, 32.863e3, 32.863e3
        # gain_ratio_A = 1
        # gain_ratio_B = 1
        # balance_matrix_A = 1
        # balance_matrix_B = 1
        # anti_aliasing_rate_string = 16k
        # anti_aliasing_method      = biquad
        # analog_anti_aliasing_file_A = test/H1aa.mat
        # analog_anti_aliasing_file_B = test/H1aa.mat
        # frequencies = np.logspace(0, np.log10(5000.), 10)
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_response = np.array(
            [1.0000003897620588-0.0007846662038375172j,
             0.9999986691396795-0.002021535559784837j,
             0.9999872488204784-0.00520806659053789j,
             0.9999114491696466-0.013417236697166764j,
             0.9994083755791304-0.03456150226440034j,
             0.9960707920317725-0.0889494857211583j,
             0.9739835023107202-0.2275993050582223j,
             0.8302887998715469-0.5597681458332082j,
             0.012018214381908476-1.003248388113367j,
             -0.22916763899233059+0.7707887449719427j])

    def tearDown(self):
        del self.frequencies
        del self.known_response

    def test_omc_combine_path_responses(self):
        """ Test the combined OMC DCPD path response """
        C = pydarm.sensing.SensingModel('''
[metadata]
[interferometer]
[sensing]
omc_path_names = A, B
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
analog_anti_aliasing_file = test/H1aa.mat, test/H1aa.mat
omc_meas_p_trans_amplifier   = 13.7e3, 17.8e3: 13.7e3, 17.8e3
whitening_mode_names = test, test
omc_meas_p_whitening_test   = 11.346e3, 32.875e3, 32.875e3: 11.521e3, 32.863e3, 32.863e3
super_high_frequency_poles_apparent_delay = 0, 0
gain_ratio = 1, 1
balance_matrix = 1, 1
adc_gain = 1638.001638001638, 1638.001638001638
omc_compensation_filter_file = test/H1OMC_1239468752.txt
omc_compensation_filter_bank = OMC_DCPD_A, OMC_DCPD_B
omc_compensation_filter_modules_in_use = 4: 4
omc_compensation_filter_gain = 1, 1
''')
        omc_dcpd_response = C.omc_combine_path_responses(self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(omc_dcpd_response[n]),
                np.abs(self.known_response[n]))
            self.assertAlmostEqual(
                np.angle(omc_dcpd_response[n], deg=True),
                np.angle(self.known_response[n], deg=True))


class TestLightTravelTimeDelayResponse(unittest.TestCase):

    def setUp(self):
        # Pre-computed values
        # x_arm_length = 3994.4704
        # y_arm_length = 3994.4692
        # frequencies = np.logspace(0, np.log10(5000.), 10)
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_light_travel_time_delay_response = np.array(
            [0.999999996495657-8.371789635887121e-05j,
             0.9999999767405227-0.00021568253099713038j,
             0.9999998456192037-0.0005556631792446989j,
             0.9999989753240384-0.0014315554035123075j,
             0.9999931988952449-0.003688111068729696j,
             0.9999548591197768-0.009501564226344633j,
             0.9997003978414927-0.024476816695829077j,
             0.9980120016904314-0.0630241579226448j,
             0.9868296389458847-0.16176298618019783j,
             0.9136631851422247-0.40647211972749725j])

    def tearDown(self):
        del self.frequencies
        del self.known_light_travel_time_delay_response

    def test_light_travel_time_delay_response(self):
        """ Test the light travel time delay response """
        C = pydarm.sensing.SensingModel('''
[metadata]
[interferometer]
[sensing]
x_arm_length = 3994.4704
y_arm_length = 3994.4692
''')
        light_travel_time_response = \
            C.light_travel_time_delay_response(self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(light_travel_time_response[n]),
                np.abs(self.known_light_travel_time_delay_response[n]))
            self.assertAlmostEqual(
                np.angle(light_travel_time_response[n], deg=True),
                np.angle(self.known_light_travel_time_delay_response[n],
                         deg=True))


class TestSinglePoleCorrectionResponse(unittest.TestCase):

    def setUp(self):
        # Pre-computed values
        # single_pole_approximation_delay_correction = -12e-6
        # frequencies = np.logspace(0, np.log10(5000.), 10)
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_single_pole_correction_response = np.array(
            [0.9999999971575539+7.539822361471657e-05j,
             0.9999999811337508+0.00019424854695853638j,
             0.9999998747785026+0.000500442783004694j,
             0.999999168863843+0.0012892911320624648j,
             0.9999944834803304+0.0033215973427495236j,
             0.9999633852347264+0.008557347130170182j,
             0.9997569841231653+0.022044788430672032j,
             0.9983873919841177+0.05676808546315201j,
             0.9893128028198163+0.14580870405020152j,
             0.9297764858882515+0.36812455268467786j])

    def tearDown(self):
        del self.frequencies
        del self.known_single_pole_correction_response

    def test_single_pole_correction_response(self):
        """ Test the single pole approximation correction response """
        C = pydarm.sensing.SensingModel('''
[metadata]
[interferometer]
[sensing]
single_pole_approximation_delay_correction = -12e-6
''')
        single_pole_correction_response = \
            C.single_pole_approximation_delay_correction_response(
                self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(single_pole_correction_response[n]),
                np.abs(self.known_single_pole_correction_response[n]))
            self.assertAlmostEqual(
                np.angle(single_pole_correction_response[n], deg=True),
                np.angle(self.known_single_pole_correction_response[n],
                         deg=True))


class TestKnownSensingTermsForMeasurement(unittest.TestCase):

    def setUp(self):
        # Pre-computed values
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_terms = np.array(
            [1.0000003831992843-0.0007929858798234663j,
             0.9999986255804101-0.002042969515282428j,
             0.9999869597043105-0.005263286282389931j,
             0.9999095302557973-0.013559488366496985j,
             0.9993956411093267-0.034927799074183925j,
             0.995986356934377-0.08988999137528692j,
             0.9734269429695691-0.22996802633705746j,
             0.8267642616923517-0.5649608162253222j,
             -0.0041816426639013065-1.003311656263212j,
             -0.19691508479464048+0.779652195223653j])

    def tearDown(self):
        del self.frequencies
        del self.known_terms

    def test_known_sensing_terms_for_measurement(self):
        """ Test the computation of the known sensing parameters """
        C = pydarm.sensing.SensingModel('''
[metadata]
[interferometer]
[sensing]
x_arm_length = 3994.4704
y_arm_length = 3994.4692
sensing_sign = 1
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
''')
        correction_terms = C.known_sensing_terms_for_measurement(
            self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(correction_terms[n]) / np.abs(self.known_terms[n]), 1.0)
            self.assertAlmostEqual(
                np.angle(correction_terms[n], deg=True) -
                np.angle(self.known_terms[n], deg=True), 0.0)


class TestComputeSensing(unittest.TestCase):

    def setUp(self):
        # Pre-computed values
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_sensing = np.array(
            [-169801.8807036616-219.12048303424578j,
             -1603528.6580281004-13226.702333005833j,
             5879871.803166859-264958.70154167747j,
             3446578.5609586663-208980.6577969556j,
             3201530.8874004283-463525.30679096654j,
             2908780.7008725638-1096359.5702610482j,
             1729667.5321780506-1973342.1148503236j,
             -154875.32218105765-1535395.702427836j,
             -654801.7126515587-135654.7883568197j,
             200533.6778938555+68533.88088596147j])

    def tearDown(self):
        del self.frequencies
        del self.known_sensing

    def test_compute_sensing(self):
        """ Test the computation of the sensing function """
        C = pydarm.sensing.SensingModel('''
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
adc_gain = 1638.001638001638, 1638.001638001638
omc_compensation_filter_file = test/H1OMC_1239468752.txt
omc_compensation_filter_bank = OMC_DCPD_A, OMC_DCPD_B
omc_compensation_filter_modules_in_use = 4: 4
omc_compensation_filter_gain = 1, 1
''')
        sensing_tf = C.compute_sensing(self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(sensing_tf[n]) / np.abs(self.known_sensing[n]), 1.0)
            self.assertAlmostEqual(
                np.angle(sensing_tf[n], deg=True) -
                np.angle(self.known_sensing[n], deg=True), 0.0)


class TestSensingResidual(unittest.TestCase):

    def setUp(self):
        # Pre-computed values
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_residual = np.array(
            [1.0000003831992847-0.0007929858798234665j,
             0.9999986255804106-0.002042969515282433j,
             0.9999869597043107-0.0052632862823899385j,
             0.9999095302557972-0.013559488366496989j,
             0.9993956411093269-0.03492779907418393j,
             0.995986356934377-0.08988999137528689j,
             0.9734269429695694-0.22996802633705743j,
             0.8267642616923517-0.5649608162253222j,
             -0.004181642663901519-1.003311656263212j,
             -0.19691508479464048+0.7796521952236531j])

    def tearDown(self):
        del self.frequencies
        del self.known_residual

    def test_sensing_residual(self):
        """ Test the computation of the sensing function """
        C = pydarm.sensing.SensingModel('''
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
adc_gain = 1638.001638001638, 1638.001638001638
omc_compensation_filter_file = test/H1OMC_1239468752.txt
omc_compensation_filter_bank = OMC_DCPD_A, OMC_DCPD_B
omc_compensation_filter_modules_in_use = 4: 4
omc_compensation_filter_gain = 1, 1
''')
        C_res = C.sensing_residual(self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(C_res[n]) / np.abs(self.known_residual[n]), 1.0)
            self.assertAlmostEqual(
                np.angle(C_res[n], deg=True) -
                np.angle(self.known_residual[n], deg=True), 0.0)


class TestDisplacementToCalcsResidual(unittest.TestCase):

    def setUp(self):
        # Pre-computed values
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_tf = np.array(
            [3120586.3412569533+655915.5270972404j,
             3197195.229554253+345256.84788082656j,
             3218163.8630940774-81180.35305564835j,
             3219467.296264217-64484.499226105225j,
             3215576.1797485715-171881.23339198926j,
             3188897.081164594-445606.88013708417j,
             3015951.3533525704-1126845.0886107476j,
             1959665.9094738844-2573950.8323788345j,
             -2480555.5491107344-2268895.642652672j,
             3361273.3553359923-1392363.5366565972j])

    def tearDown(self):
        del self.frequencies
        del self.known_tf

    def test_displacement_to_calcs(self):
        """ Test the computation of the displacement to CALCS """
        C = pydarm.sensing.SensingModel('''
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
adc_gain = 1638.001638001638, 1638.001638001638
omc_compensation_filter_file = test/H1OMC_1239468752.txt
omc_compensation_filter_bank = OMC_DCPD_A, OMC_DCPD_B
omc_compensation_filter_modules_in_use = 4: 4
omc_compensation_filter_gain = 1, 1
gds_c_foton_invsensing_tf = \
  test/2019-04-04_H1CALCS_InverseSensingFunction_Foton_SRCD-2N_Gain_tf.txt
''')
        disp_to_calcs_tf = C.displacement_to_calcs_residual(self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(disp_to_calcs_tf[n]) / np.abs(self.known_tf[n]), 1.0)
            self.assertAlmostEqual(
                np.angle(disp_to_calcs_tf[n], deg=True) -
                np.angle(self.known_tf[n], deg=True), 0.0)


if __name__ == '__main__':
    unittest.main()
