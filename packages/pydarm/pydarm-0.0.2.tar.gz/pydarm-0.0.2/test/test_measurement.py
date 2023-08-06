import unittest
import pydarm
import numpy as np
from scipy.signal import freqresp


class TestGetRawTF(unittest.TestCase):

    def setUp(self):
        data_from_dtt = np.genfromtxt(
                       ('./test/2020-01-03_H1_'
                        'DARM_OLGTF_LF_SS_A_DARMIN2_B_DARMIN1_tf.txt'),
                       dtype='float',
                       delimiter=None
        )
        coh_data_from_dtt = np.loadtxt(
            ('./test/2020-01-03_H1_DARM_OLGTF_LF_SS_'
             'A_DARMIN2_B_DARMIN1_coh.txt'))

        self.freq_from_dtt = data_from_dtt[:, 0]
        self.mag_from_dtt = np.abs(data_from_dtt[:, 1]+1j*data_from_dtt[:, 2])
        self.pha_from_dtt = np.angle(data_from_dtt[:, 1]
                                     + 1j*data_from_dtt[:, 2],
                                     deg=True)
        self.coh_from_dtt = coh_data_from_dtt[:, 1]
        self.unc_from_dtt = np.sqrt((1.0 - self.coh_from_dtt) /
                                    (2.0*(self.coh_from_dtt + 1e-6)*5))

        self.freq_from_dtt_with_coh_thresh = \
            self.freq_from_dtt[coh_data_from_dtt[:, 1] > 0.9]
        self.mag_from_dtt_with_coh_thresh = \
            self.mag_from_dtt[coh_data_from_dtt[:, 1] > 0.9]
        self.pha_from_dtt_with_coh_thresh = \
            self.pha_from_dtt[coh_data_from_dtt[:, 1] > 0.9]
        self.coh_from_dtt_with_coh_thresh = \
            self.coh_from_dtt[coh_data_from_dtt[:, 1] > 0.9]
        self.unc_from_dtt_with_coh_thresh = \
            self.unc_from_dtt[coh_data_from_dtt[:, 1] > 0.9]

    def tearDown(self):
        del self.freq_from_dtt
        del self.mag_from_dtt
        del self.pha_from_dtt
        del self.coh_from_dtt
        del self.unc_from_dtt

        del self.freq_from_dtt_with_coh_thresh
        del self.mag_from_dtt_with_coh_thresh
        del self.pha_from_dtt_with_coh_thresh
        del self.coh_from_dtt_with_coh_thresh
        del self.unc_from_dtt_with_coh_thresh

    def test_get_raw_tf(self):
        """ Test get_raw_tf() """
        meas_object = pydarm.measurement.Measurement(
            './test/2020-01-03_H1_DARM_OLGTF_LF_SS_5to1100Hz_15min.xml')
        freq, tf, coh, unc = meas_object.get_raw_tf(
            'H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_IN1')
        freq2, tf2, coh2, unc2 = meas_object.get_raw_tf(
            'H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_IN1', cohThresh=0.9)

        # Note: For some reason, the txt file is missing one frequency.
        # This is unrelated to the coherence, at least of this TF.
        freq = np.delete(freq, 22)
        tf = np.delete(tf, 22)
        coh = np.delete(coh, 22)
        unc = np.delete(unc, 22)

        freq2 = np.delete(freq2, 22)
        tf2 = np.delete(tf2, 22)
        coh2 = np.delete(coh2, 22)
        unc2 = np.delete(unc2, 22)

        tf_mag = np.abs(tf)
        tf_pha = np.angle(tf, deg=True)
        tf2_mag = np.abs(tf2)
        tf2_pha = np.angle(tf2, deg=True)

        # Test with no coherence threshold
        for n in range(len(self.freq_from_dtt)):
            # Test absolute differences
            self.assertAlmostEqual(freq[n], self.freq_from_dtt[n], places=4)
            self.assertAlmostEqual(tf_mag[n], self.mag_from_dtt[n],
                                   places=4)
            self.assertAlmostEqual(tf_pha[n], self.pha_from_dtt[n],
                                   places=4)
            self.assertAlmostEqual(coh[n], self.coh_from_dtt[n])
            self.assertAlmostEqual(unc[n], self.unc_from_dtt[n], places=6)
            # Test relative differences
            self.assertAlmostEqual(freq[n] / self.freq_from_dtt[n], 1.0,
                                   places=6)
            self.assertAlmostEqual(tf_mag[n] / self.mag_from_dtt[n], 1.0,
                                   places=6)
            self.assertAlmostEqual(tf_pha[n] / self.pha_from_dtt[n], 1.0,
                                   places=6)
            self.assertAlmostEqual(coh[n] / self.coh_from_dtt[n], 1.0)
            self.assertAlmostEqual(unc[n] / self.unc_from_dtt[n], 1.0,
                                   places=2)

        # Second test with coherence threshold of 0.9
        for n in range(len(self.freq_from_dtt_with_coh_thresh)):
            self.assertAlmostEqual(freq2[n],
                                   self.freq_from_dtt_with_coh_thresh[n],
                                   places=4)
            self.assertAlmostEqual(tf2_mag[n],
                                   self.mag_from_dtt_with_coh_thresh[n],
                                   places=4)
            self.assertAlmostEqual(tf2_pha[n],
                                   self.pha_from_dtt_with_coh_thresh[n],
                                   places=4)
            self.assertAlmostEqual(coh2[n],
                                   self.coh_from_dtt_with_coh_thresh[n])
            self.assertAlmostEqual(unc2[n],
                                   self.unc_from_dtt_with_coh_thresh[n],
                                   places=6)


class TestGetRawASD(unittest.TestCase):

    def setUp(self):
        data_from_dtt = np.genfromtxt(
                       ('./test/2019-03-27_H1DARM_OLGTF_BB.txt'),
                       dtype='float',
                       delimiter=None
        )

        self.freq_from_dtt = data_from_dtt[:, 0]
        self.asd_from_dtt = data_from_dtt[:, 1]

        measurement_file = ('./test/2019-03-27_H1DARM_OLGTF_BB.xml')
        channelA = 'H1:LSC-DARM1_IN2'
        meas_object = pydarm.measurement.Measurement(measurement_file)
        freq, asd = meas_object.get_raw_asd(channelA)

        self.freq_from_xml = freq
        self.asd_from_xml = asd

    def tearDown(self):
        del self.freq_from_dtt
        del self.asd_from_dtt

        del self.freq_from_xml
        del self.asd_from_xml

    def test_measurement_class(self):
        for n in range(len(self.freq_from_dtt)):
            # Test absolute differences
            self.assertAlmostEqual(self.freq_from_dtt[n],
                                   self.freq_from_xml[n], places=5)
            self.assertAlmostEqual(self.asd_from_dtt[n],
                                   self.asd_from_xml[n], places=5)
            # Test relative differences
            # Cannot do a relative comparison for frequencies because of
            # f = 0; Cannot do a 0/0
            self.assertAlmostEqual(self.asd_from_dtt[n]/self.asd_from_xml[n],
                                   1.0)


class TestGetSetOfChannels(unittest.TestCase):

    def setUp(self):
        self.channels_to_compare = ['H1:LSC-DARM1_EXC',
                                    'H1:LSC-DARM1_IN1',
                                    'H1:LSC-DARM1_IN2']

        measurement_file = ('./test/2019-03-27_H1DARM_OLGTF_BB.xml')
        meas_object = pydarm.measurement.Measurement(measurement_file)
        self.set_of_A_channels, self.set_of_B_channels = \
            meas_object.get_set_of_channels()

    def tearDown(self):
        del self.channels_to_compare
        del self.set_of_A_channels
        del self.set_of_B_channels

    def test_measurement_class(self):
        for i in range(len(self.channels_to_compare)):
            self.assertTrue(self.channels_to_compare[i] in
                            self.set_of_A_channels)


class TestPreProcessTransferFunctions(unittest.TestCase):

    def setUp(self):
        self.meas_object = pydarm.measurement.Measurement(
            './test/2020-01-03_H1_DARM_OLGTF_LF_SS_5to1100Hz_15min.xml')

    def tearDown(self):
        del self.meas_object

    def test_pre_process_transfer_functions(self):
        # This function has already been tested by a previous unit test above
        freq, tf, coh, unc = self.meas_object.get_raw_tf(
            'H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_IN1', cohThresh=0.9)

        # This is the model that we need to use in order to process the data.
        model_string = '''
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
adc_gain = 1, 1
[pcal]
pcal_dewhiten               = 1.0, 1.0
ref_pcal_2_darm_act_sign    = -1.0
analog_anti_aliasing_file = test/H1aa.mat
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
'''

        # Set up the ProcessMeasurement object
        meas = pydarm.measurement.ProcessMeasurement(
            model_string,
            self.meas_object, self.meas_object,
            ('H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_IN1'),
            ('H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_IN1'),
            meas1_cohThresh=0, meas2_cohThresh=0.9)

        # Now call the function being tested
        frequencies, tf_meas1, tf_meas2, pcal_corr, combined_unc = \
            meas.pre_process_transfer_functions()

        # The main thing to test is the combination of transfer functions
        # The other pieces of the pre_process_transfer_functions() are
        # tested in other unit tests either in test_measurement.py or
        # test_sensing.py
        # If the frequency vectors are matching, then everything else should
        # be working correctly
        # We also check the combination of the uncertainties is correct
        self.assertTrue(np.allclose(frequencies, freq))
        self.assertTrue(np.allclose(combined_unc, np.sqrt(unc**2 + unc**2)))


class TestCropData(unittest.TestCase):
    def setUp(self):
        meas_object = pydarm.measurement.Measurement(
            './test/2020-01-03_H1_DARM_OLGTF_LF_SS_5to1100Hz_15min.xml')

        model_string = '''
[metadata]
[interferometer]
[sensing]
[pcal]
'''

        self.meas = pydarm.measurement.ProcessMeasurement(
            model_string, meas_object, meas_object,
            ('H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_IN1'),
            ('H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_IN1'))
        self.frequencies = np.arange(1, 11, dtype=int)
        self.values = np.ones(len(self.frequencies), dtype=int)
        self.err = np.zeros(len(self.frequencies), dtype=int)

    def tearDown(self):
        del self.meas
        del self.frequencies
        del self.values
        del self.err

    def test_mcmc(self):
        """ Test the internal _mcmc() function """
        x, y, z = self.meas.crop_data(self.frequencies, self.values,
                                      self.err, fmin=2, fmax=8)

        # Compare relative errors
        self.assertTrue(np.array_equal(x, np.arange(2, 9, dtype=int)))
        self.assertTrue(np.array_equal(y, np.ones(7, dtype=int)))
        self.assertTrue(np.array_equal(z, np.zeros(7, dtype=int)))


class TestSensingGetProcessedMeasurementResponse(unittest.TestCase):

    def setUp(self):
        data_in = np.genfromtxt(
            ('test/2020-01-03_H1_sensingFunction_'
             'processedOpticalResponse_corr.txt'),
            dtype='float',
            delimiter=None)

        self.known_freq = data_in[:, 0]
        self.known_tf_mag = data_in[:, 1]
        self.known_tf_angle = data_in[:, 2]

    def tearDown(self):
        del self.known_freq
        del self.known_tf_mag
        del self.known_tf_angle

    def test_sensing_get_processed_measurement_response(self):
        """ Test the processing of the optical response """

        # These are the xml files we want to get our data from.
        meas_file_1 = \
            'test/2020-01-03_H1_DARM_OLGTF_LF_SS_5to1100Hz_15min.xml'
        meas_file_2 = \
            'test/2020-01-03_H1_PCALY2DARMTF_LF_SS_5t1100Hz_10min.xml'

        # This is the model that we need to use in order to process the data.
        model_string = '''
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
adc_gain = 1, 1
[pcal]
pcal_dewhiten               = 1.0, 1.0
ref_pcal_2_darm_act_sign    = -1.0
analog_anti_aliasing_file = test/H1aa.mat
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
'''
        meas1 = pydarm.measurement.Measurement(meas_file_1)
        meas2 = pydarm.measurement.Measurement(meas_file_2)
        process_sensing = \
            pydarm.measurement.ProcessSensingMeasurement(
                model_string, meas1, meas2,
                ('H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_EXC'),
                ('H1:CAL-PCALY_RX_PD_OUT_DQ', 'H1:LSC-DARM_IN1_DQ'),
                meas1_cohThresh=0.90, meas2_cohThresh=0.992)

        freq, processed_opt_resp, processed_opt_resp_unc = \
            process_sensing.get_processed_measurement_response()

        for n in range(len(freq)):
            # Test absolute differences
            self.assertAlmostEqual(freq[n], self.known_freq[n], places=3)
            self.assertAlmostEqual(np.abs(processed_opt_resp[n]),
                                   self.known_tf_mag[n], places=-1)
            self.assertAlmostEqual(
                np.angle(processed_opt_resp[n], deg=True),
                self.known_tf_angle[n],
                places=5)
            # Test relative differences
            self.assertAlmostEqual(freq[n] / self.known_freq[n], 1.0, places=3)
            self.assertAlmostEqual(
                np.abs(processed_opt_resp[n]) / self.known_tf_mag[n], 1.0,
                places=6)
            self.assertAlmostEqual(np.angle(processed_opt_resp[n], deg=True) /
                                   self.known_tf_angle[n], 1.0, places=5)


class TestRescaleSensingByTDCFVals(unittest.TestCase):

    def setUp(self):
        meas_object = pydarm.measurement.Measurement(
            './test/2020-01-03_H1_DARM_OLGTF_LF_SS_5to1100Hz_15min.xml')
        model_string = '''
[metadata]
[interferometer]
[sensing]
coupled_cavity_optical_gain   = 1e6
coupled_cavity_pole_frequency = 400
detuned_spring_frequency      = 1
detuned_spring_Q              = 10
sensing_sign                  = 1
is_pro_spring                 = False
[pcal]
'''
        self.meas = pydarm.measurement.ProcessSensingMeasurement(
            model_string,
            meas_object, meas_object,
            ('H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_IN1'),
            ('H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_IN1'))
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.tdcf_vals = np.array([3, 420, 1, 10])
        optical_response = pydarm.sensing.SensingModel.optical_response(
            self.tdcf_vals[1], self.tdcf_vals[2], self.tdcf_vals[3])
        self.optical_freqresp = self.tdcf_vals[0] * 1e6 * freqresp(
            optical_response, 2.0*np.pi*self.frequencies)[1]
        # Pre-computed values from an optical plant with
        # f_cc = 400 Hz, f_s = 1 Hz, Q = 10 (anti-spring)
        # And frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_scaled_optical_response = 1e6 * np.array(
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

    def tearDown(self):
        del self.meas
        del self.frequencies
        del self.tdcf_vals
        del self.optical_freqresp
        del self.known_scaled_optical_response

    def test_rescale_sensing_by_tdcf_vals(self):
        """ Test rescale_sensing_by_tdcf_vals() """
        rescaled_response = self.meas.rescale_sensing_by_tdcf_vals(
            self.frequencies, self.optical_freqresp, self.tdcf_vals[0],
            self.tdcf_vals[1])

        self.assertTrue(np.allclose(rescaled_response,
                                    self.known_scaled_optical_response))


class TestSensingRunMCMC(unittest.TestCase):

    def setUp(self):
        meas_obj1 = pydarm.measurement.Measurement(
            './test/2020-01-03_H1_DARM_OLGTF_LF_SS_5to1100Hz_15min.xml')
        meas_obj2 = pydarm.measurement.Measurement(
            './test/2020-01-03_H1_PCALY2DARMTF_LF_SS_5t1100Hz_10min.xml')

        model_string = '''
[metadata]
[interferometer]
[sensing]
x_arm_length = 3994.4704
y_arm_length = 3994.4692
sensing_sign = 1
is_pro_spring = False
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
[pcal]
pcal_dewhiten               = 1.0, 1.0
ref_pcal_2_darm_act_sign    = -1.0
analog_anti_aliasing_file = test/H1aa.mat
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
'''

        self.meas = pydarm.measurement.ProcessSensingMeasurement(
            model_string, meas_obj1, meas_obj2,
            ('H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_EXC'),
            ('H1:CAL-PCALY_RX_PD_OUT_DQ', 'H1:LSC-DARM_IN1_DQ'),
            meas1_cohThresh=0.90, meas2_cohThresh=0.992)
        self.known_optical_pars = np.array(
            [3.14e6, 408.2, 0.2, 0.6, -2.4])
        self.known_std = np.array(
            [1.31938561e+03, 6.27393687e-01, 1.20974870e-01, 2.22589748e-01,
             3.63299973e-01])

    def tearDown(self):
        del self.meas
        del self.known_optical_pars
        del self.known_std

    def test_run_mcmc(self):
        chain = self.meas.run_mcmc(fmin=20, fmax=5000,
                                   burn_in_steps=100, steps=2000)

        optical_pars = np.median(chain, axis=0)
        std_vals = np.std(chain, axis=0)

        for n in range(len(optical_pars)):
            self.assertAlmostEqual(
                optical_pars[0] / self.known_optical_pars[0], 1.0, places=3)
            self.assertAlmostEqual(
                optical_pars[1] / self.known_optical_pars[1], 1.0, places=3)
            self.assertAlmostEqual(
                optical_pars[2] / self.known_optical_pars[2], 1.0, places=0)
            self.assertAlmostEqual(
                optical_pars[3] / self.known_optical_pars[3], 1.0, places=0)
            self.assertAlmostEqual(
                optical_pars[4], self.known_optical_pars[4], places=1)
        self.assertAlmostEqual(std_vals[0] / self.known_std[0], 1.0, places=1)
        self.assertAlmostEqual(std_vals[1] / self.known_std[1], 1.0, places=1)
        self.assertAlmostEqual(std_vals[2] / self.known_std[2], 1.0, places=1)
        self.assertAlmostEqual(std_vals[3] / self.known_std[3], 1.0, places=1)
        self.assertAlmostEqual(std_vals[4] / self.known_std[4], 1.0, places=1)


class TestInverseSensingFotonFilter(unittest.TestCase):

    def setUp(self):
        meas_obj1 = pydarm.measurement.Measurement(
            './test/2020-01-03_H1_DARM_OLGTF_LF_SS_5to1100Hz_15min.xml')
        meas_obj2 = pydarm.measurement.Measurement(
            './test/2020-01-03_H1_PCALY2DARMTF_LF_SS_5t1100Hz_10min.xml')

        model_string = '''
[metadata]
[interferometer]
[sensing]
x_arm_length = 3994.4704
y_arm_length = 3994.4692
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
[pcal]
pcal_dewhiten               = 1.0, 1.0
ref_pcal_2_darm_act_sign    = -1.0
analog_anti_aliasing_file = test/H1aa.mat
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
'''

        self.meas = pydarm.measurement.ProcessSensingMeasurement(
            model_string, meas_obj1, meas_obj2,
            ('H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_EXC'),
            ('H1:CAL-PCALY_RX_PD_OUT_DQ', 'H1:LSC-DARM_IN1_DQ'),
            meas1_cohThresh=0.90, meas2_cohThresh=0.992)

        model_string = '''
[metadata]
[interferometer]
[sensing]
x_arm_length = 3994.4704
y_arm_length = 3994.4692
sensing_sign = 1
is_pro_spring = False
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
[pcal]
pcal_dewhiten               = 1.0, 1.0
ref_pcal_2_darm_act_sign    = -1.0
analog_anti_aliasing_file = test/H1aa.mat
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
'''

        self.meas2 = pydarm.measurement.ProcessSensingMeasurement(
            model_string, meas_obj1, meas_obj2,
            ('H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_EXC'),
            ('H1:CAL-PCALY_RX_PD_OUT_DQ', 'H1:LSC-DARM_IN1_DQ'),
            meas1_cohThresh=0.90, meas2_cohThresh=0.992)

        self.median_vals = np.atleast_2d(np.array([3.e6, 430., 1., 1/10., -1.]))

    def tearDown(self):
        del self.meas
        del self.meas2
        del self.median_vals

    def test_inverse_sensing_foton_filter(self):
        out = self.meas.inverse_sensing_foton_filter(self.median_vals)
        assert (out ==
                '''Inverse Sensing FOTON values: [NB: SRCD2N zpk gain based on sensing sign in parameters file]
SRCD2N: zpk([430.0000;0.0500+i*0.9987;0.0500-i*0.9987],[0.1;0.1;7000],1,"n")gain(100.00)
Gain: gain(3.333e-07)

Inverse Sensing without cavity pole FOTON values for CFTD path: [NB: SRCD2N zpk gain based on sensing sign in parameters file]
SRCD2N: zpk([0.0500+i*0.9987;0.0500-i*0.9987],[0.1;0.1],1,"n")gain(100.00)
Gain: gain(3.333e-07)''')

        out = self.meas2.inverse_sensing_foton_filter(self.median_vals)
        assert (out ==
                '''Inverse Sensing FOTON values: [NB: SRCD2N zpk gain based on sensing sign in parameters file]
SRCD2N: zpk([430.0000;0.9512;-1.0512],[0.1;0.1;7000],1,"n")gain(100.00)
Gain: gain(3.333e-07)

Inverse Sensing without cavity pole FOTON values for CFTD path: [NB: SRCD2N zpk gain based on sensing sign in parameters file]
SRCD2N: zpk([0.9512;-1.0512],[0.1;0.1],1,"n")gain(100.00)
Gain: gain(3.333e-07)''')


class TestSensingSaveResultsToJson(unittest.TestCase):

    def setUp(self):
        self.filename = 'test.json'
        self.fmin = None
        self.fmax = None
        self.mcmc_map_vals = np.atleast_2d(
            np.array([3.e6, 430., 1., 1/10., -1.]))

    def tearDown(self):
        del self.filename
        del self.fmin
        del self.fmax
        del self.mcmc_map_vals

    def test_save_results_to_json(self):
        model_string = '''
[metadata]
[interferometer]
[sensing]
[pcal]
'''

        meas_obj1 = pydarm.measurement.Measurement(
            './test/2020-01-03_H1_DARM_OLGTF_LF_SS_5to1100Hz_15min.xml')
        meas_obj2 = pydarm.measurement.Measurement(
            './test/2020-01-03_H1_PCALY2DARMTF_LF_SS_5t1100Hz_10min.xml')

        meas = pydarm.measurement.ProcessSensingMeasurement(
            model_string, meas_obj1, meas_obj2,
            ('H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_EXC'),
            ('H1:CAL-PCALY_RX_PD_OUT_DQ', 'H1:LSC-DARM_IN1_DQ'))

        meas.save_results_to_json(self.filename, self.fmin, self.fmax,
                                  self.mcmc_map_vals, 'sensing')


class TestSensingQueryResultsFromJson(unittest.TestCase):

    def setUp(self):
        model_string = model_string = '''
[metadata]
[interferometer]
[sensing]
x_arm_length = 3994.4704
y_arm_length = 3994.4692
sensing_sign = 1
is_pro_spring = False
anti_aliasing_rate_string = 16k
anti_aliasing_method = biquad
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
[pcal]
pcal_dewhiten               = 1.0, 1.0
ref_pcal_2_darm_act_sign    = -1.0
analog_anti_aliasing_file = test/H1aa.mat
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
'''
        meas_obj1 = pydarm.measurement.Measurement(
            './test/2020-01-03_H1_DARM_OLGTF_LF_SS_5to1100Hz_15min.xml')
        meas_obj2 = pydarm.measurement.Measurement(
            './test/2020-01-03_H1_PCALY2DARMTF_LF_SS_5t1100Hz_10min.xml')

        self.meas = pydarm.measurement.ProcessSensingMeasurement(
            model_string, meas_obj1, meas_obj2,
            ('H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_EXC'),
            ('H1:CAL-PCALY_RX_PD_OUT_DQ', 'H1:LSC-DARM_IN1_DQ'),
            json_results_file='./test/O3_H1_sensing.json',
            meas1_cohThresh=0.90, meas2_cohThresh=0.992)
        self.known_vals = np.asarray([3170611.467085059,
                                      408.1817342117136,
                                      0.19227856654546951,
                                      0.6197211439122837,
                                      -2.3711268610322085])
        self.known_is_pro_spring = False

    def tearDown(self):
        del self.meas
        del self.known_vals
        del self.known_is_pro_spring

    def test_query_results_from_json(self):
        test = self.meas.query_results_from_json(
            'sensing', fmin=20, fmax=5000)
        self.assertTrue(np.allclose(test[1], self.known_vals))
        self.assertEqual(test[2], self.known_is_pro_spring)


class TestSensingStackMeasurements(unittest.TestCase):

    def setUp(self):
        meas_obj1 = pydarm.measurement.Measurement(
            './test/2020-01-03_H1_DARM_OLGTF_LF_SS_5to1100Hz_15min.xml')
        meas_obj2 = pydarm.measurement.Measurement(
            './test/2020-01-03_H1_PCALY2DARMTF_LF_SS_5t1100Hz_10min.xml')

        model_string = '''
[metadata]
[interferometer]
[sensing]
x_arm_length = 3994.4704
y_arm_length = 3994.4692
sensing_sign = 1
is_pro_spring = False
anti_aliasing_rate_string = 16k
anti_aliasing_method = biquad
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
[pcal]
pcal_dewhiten               = 1.0, 1.0
ref_pcal_2_darm_act_sign    = -1.0
analog_anti_aliasing_file = test/H1aa.mat
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
'''

        self.meas = pydarm.measurement.ProcessSensingMeasurement(
            model_string, meas_obj1, meas_obj2,
            ('H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_EXC'),
            ('H1:CAL-PCALY_RX_PD_OUT_DQ', 'H1:LSC-DARM_IN1_DQ'),
            meas1_cohThresh=0.90, meas2_cohThresh=0.992,
            json_results_file='./test/O3_H1_sensing.json')

        self.meas2 = pydarm.measurement.ProcessSensingMeasurement(
            model_string, meas_obj1, meas_obj2,
            ('H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_EXC'),
            ('H1:CAL-PCALY_RX_PD_OUT_DQ', 'H1:LSC-DARM_IN1_DQ'),
            meas1_cohThresh=0.90, meas2_cohThresh=0.992,
            json_results_file='./test/O3_H1_sensing.json')

        self.known_freq = np.array(
            [6.0565, 6.4972, 6.7742, 7.0544, 7.475, 7.773, 8.002, 8.309, 8.791,
             9.103, 10.334, 11.131, 11.709, 12.234, 15.6, 16.4, 17.1, 17.6,
             19.1, 23.248, 25.751, 32.758, 38.886, 46.16, 54.794, 65.043,
             77.209, 88.939, 95.201, 108.795, 121.102, 139.447, 153.302,
             182.997, 216.016, 305.066, 341.623, 401.433, 410.3, 428.909,
             433.7, 610.055, 851.613, 1083.7])
        self.known_opt_resp = np.array(
            [4934296.824246803-881267.8050210752j,
             4223790.251636657-901279.8889312955j,
             4014518.4794295947-799775.716328531j,
             3922021.112178207-667864.8052401808j,
             3692504.5075529777-468837.469588845j,
             3574954.3579922593-578947.5756646723j,
             3437707.7681817445-458126.1116090667j,
             3401828.560971251-327187.9508750953j,
             3361791.3034861763-322424.82677631377j,
             3281309.440448998-182847.40615941168j,
             3301534.171548379+74121.81980029726j,
             3343277.789095726-44646.23230142693j,
             3350108.2175412257-57645.45000132245j,
             3289274.1900720336-109975.74709488206j,
             3237607.0986972805-57279.1598471469j,
             3245118.971389657-103292.5312854583j,
             3205672.5724586463-133756.02084738613j,
             3201063.0906945537-138735.0277155783j,
             3207711.019461757-143470.91674952986j,
             3149857.4149646815-174251.62488467124j,
             3129414.4679895462-187252.13963650496j,
             3113143.229522848-227152.7369155042j,
             3098827.091208541-281044.29138424783j,
             3079083.8015063754-320952.4149203036j,
             3078480.4097145568-379644.6825549526j,
             3060603.349085048-444155.0857105063j,
             3028541.863102633-555706.4637572238j,
             3008324.345077513-625408.7589730328j,
             2982894.751564159-665314.0025169546j,
             2965132.8059645565-756560.4991038231j,
             2895770.1300818617-846545.1906184796j,
             2823040.577129127-947493.7297318504j,
             2742897.001708313-1042354.4634583262j,
             2629105.4068403738-1179458.7590034904j,
             2458731.6133123157-1296012.7705170403j,
             2020021.1299997028-1482561.374370173j,
             1860720.6792274246-1530226.4164044785j,
             1599074.91656462-1546895.413379534j,
             1569988.113268239-1567031.0387250397j,
             1495861.0360880133-1552633.810315972j,
             1475319.3134686488-1555582.148874394j,
             969119.7933364433-1440847.3247283248j,
             594187.0600354406-1216410.2614188304j,
             404607.11990471353-1025077.131040621j])
        self.known_unc = np.array(
            [0.033149388, 0.022653876, 0.023699189, 0.020984136,
             0.014443759, 0.009388175, 0.008028116, 0.006663013,
             0.006328261, 0.0050811693, 0.016016474, 0.008068703,
             0.005768871, 0.017839255, 0.010922797, 0.009457669,
             0.0032619617, 0.01023592, 0.0036131348, 0.00081705215,
             0.001400364, 0.001897415, 0.0012472747, 0.0014970546,
             0.0026261336, 0.001779066, 0.0015784509, 0.0012732864,
             0.0012872535, 0.0020959463, 0.0029591555, 0.0021354023,
             0.0053300364, 0.0036761549, 0.003559982, 0.002179605,
             0.0024981925, 0.0041950326, 0.0023519339, 0.0015859917,
             0.0017689841, 0.002548984, 0.0032408999, 0.0077597047])

    def tearDown(self):
        del self.meas
        del self.meas2
        del self.known_freq
        del self.known_opt_resp
        del self.known_unc

    def test_stack_measurements(self):
        test = self.meas.stack_measurements([self.meas2], 20, 5000,
                                            [20], [5000])

        for n in range(len(test[0][0])):
            self.assertAlmostEqual(test[0][0][n] / self.known_freq[n], 1.0)
            self.assertAlmostEqual(
                np.abs(test[0][1][n])/np.abs(self.known_opt_resp[n]), 1.0)
            self.assertAlmostEqual(
                np.abs(np.angle(test[0][1][n], deg=True) -
                       np.angle(self.known_opt_resp[n], deg=True)),
                0.0)
            self.assertAlmostEqual(test[0][2][n] / self.known_unc[n], 1.0)

class TestSensingGPR(unittest.TestCase):

    def setUp(self):
        meas_obj1 = pydarm.measurement.Measurement(
            './test/2020-01-03_H1_DARM_OLGTF_LF_SS_5to1100Hz_15min.xml')
        meas_obj2 = pydarm.measurement.Measurement(
            './test/2020-01-03_H1_PCALY2DARMTF_LF_SS_5t1100Hz_10min.xml')

        model_string = '''
[metadata]
[interferometer]
[sensing]
x_arm_length = 3994.4704
y_arm_length = 3994.4692
sensing_sign = 1
is_pro_spring = False
anti_aliasing_rate_string = 16k
anti_aliasing_method = biquad
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
[pcal]
pcal_dewhiten               = 1.0, 1.0
ref_pcal_2_darm_act_sign    = -1.0
analog_anti_aliasing_file = test/H1aa.mat
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
'''

        self.meas = pydarm.measurement.ProcessSensingMeasurement(
            model_string, meas_obj1, meas_obj2,
            ('H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_EXC'),
            ('H1:CAL-PCALY_RX_PD_OUT_DQ', 'H1:LSC-DARM_IN1_DQ'),
            meas1_cohThresh=0.90, meas2_cohThresh=0.992,
            json_results_file='./test/O3_H1_sensing.json')

        self.meas2 = pydarm.measurement.ProcessSensingMeasurement(
            model_string, meas_obj1, meas_obj2,
            ('H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_EXC'),
            ('H1:CAL-PCALY_RX_PD_OUT_DQ', 'H1:LSC-DARM_IN1_DQ'),
            meas1_cohThresh=0.90, meas2_cohThresh=0.992,
            json_results_file='./test/O3_H1_sensing.json')

        self.freq = np.logspace(np.log10(5),np.log10(1200),20)

        self.known_y_pred = np.array(
             [1.143865894198042-0.13218101017142667j,
              1.1126738395181432-0.10366451924822398j,
              1.0836963507505653-0.07737683533919569j,
              1.0577031562674817-0.05396437865115298j,
              1.0352778806177692-0.03390360123989659j,
              1.0167899306790116-0.017479181654318884j,
              1.0023810124014758-0.004775264441794614j,
              0.9919672034132536+0.004319683366717252j,
              0.9852562389123264+0.010094936243535751j,
              0.9817784289849473+0.01298809526463786j,
              0.9809285335400385+0.013546709996471113j,
              0.9820150801429735+0.012384133100614942j,
              0.9843130974163637+0.010133187112890083j,
              0.9871160948859689+0.007401278899534934j,
              0.9897833528694234+0.004730329206782792j,
              0.9917791585510201+0.0025643288004492896j,
              0.9927014685996143+0.0012265532696415942j,
              0.9922985015825642+0.0009075500198081508j,
              0.9904728583448656+0.001664047719329993j,
              0.9872738273572552+0.0034280242769106333j])

        self.known_sigma = np.array(
             [0.04027781477576714, 0.030308227084443286, 0.022747613590672393,
              0.017586693851760402, 0.01454809330369326, 0.013007019870077623,
              0.012248682735241323, 0.01182434942424862, 0.011611384881395851,
              0.011649505059387692, 0.011952702932418378, 0.01241794153628566,
              0.012871282857891506, 0.013204576992935896, 0.013555319233350337,
              0.014494382538793819, 0.01699713562007634, 0.021912838040168352,
              0.029512044766968195, 0.03967875375309495])

    def tearDown(self):
        del self.meas
        del self.meas2
        del self.freq
        del self.known_y_pred
        del self.known_sigma

    def test_sensing_gpr(self):
        test = self.meas.run_gpr(self.freq, [self.meas2], 20, 5000,[20], [5000])

        for n in range(len(test[0])):
            self.assertAlmostEqual(
                np.abs(test[0][n])/np.abs(self.known_y_pred[n]), 1.0, places=4)
            self.assertAlmostEqual(np.angle(test[0][n], deg=True) -
                np.angle(self.known_y_pred[n], deg=True), 0.0, places=4)
            self.assertAlmostEqual(test[1][n] / self.known_sigma[n], 1.0, places=4)


class TestGetProcessedTSTResponse(unittest.TestCase):

    def setUp(self):
        data_in = np.genfromtxt(
            'test/2019-04-24_TST.txt',
            dtype='float',
            delimiter=None)

        self.known_freq = data_in[:, 0]
        self.known_tf_mag = data_in[:, 1]
        self.known_tf_angle = data_in[:, 2]
        self.known_tf_unc = data_in[:, 3]

    def tearDown(self):
        del self.known_freq
        del self.known_tf_mag
        del self.known_tf_angle
        del self.known_tf_unc

    def test_get_processed_tst_response(self):
        """ Test the processing of the TST response """

        # These are the xml files we want to get our data from.
        meas_file_1 = \
            'test/2019-04-24_H1SUSETMX_L3_iEXC2DARM_8min.xml'
        meas_file_2 = \
            'test/2019-04-24_H1SUSETMX_L3_PCAL2DARM_8min.xml'

        # This is the model that we need to use in order to process the data.
        model_string = '''
[metadata]
[interferometer]
[actuation_x_arm]
darm_feedback_sign = -1
uim_NpA       = 1.634
pum_NpA       = 0.02947
tst_NpV2      = 4.427e-11
linearization = OFF
actuation_esd_bias_voltage = -9.3
sus_filter_file = test/H1SUSETMX_1256232808.txt
tst_isc_inf_bank    = ETMX_L3_ISCINF_L
tst_isc_inf_modules =
tst_isc_inf_gain    = 1.0
tst_lock_bank       = ETMX_L3_LOCK_L
tst_lock_modules    = 5,8,9,10
tst_lock_gain       = 1.0
tst_drive_align_bank     = ETMX_L3_DRIVEALIGN_L2L
tst_drive_align_modules  = 4,5
tst_drive_align_gain     = -35.7
pum_lock_bank    = ETMX_L2_LOCK_L
pum_lock_modules = 7
pum_lock_gain    = 23.0
pum_drive_align_bank    = ETMX_L2_DRIVEALIGN_L2L
pum_drive_align_modules = 6,7
pum_drive_align_gain    = 1.0
pum_coil_outf_signflip  = 1
uim_lock_bank    = ETMX_L1_LOCK_L
uim_lock_modules = 10
uim_lock_gain    = 1.06
uim_drive_align_bank    = ETMX_L1_DRIVEALIGN_L2L
uim_drive_align_modules =
uim_drive_align_gain    = 1.0
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
pum_driver_DC_trans_ApV = 2.6847e-4
uim_driver_DC_trans_ApV = 6.1535e-4
anti_imaging_rate_string = 16k
anti_imaging_method      = biquad
analog_anti_imaging_file = test/H1aa.mat
dac_gain = 7.62939453125e-05
unknown_actuation_delay = 15e-6
[pcal]
pcal_dewhiten               = 1.0, 1.0
ref_pcal_2_darm_act_sign    = -1.0
analog_anti_aliasing_file = test/H1aa.mat
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
'''
        meas1 = pydarm.measurement.Measurement(meas_file_1)
        meas2 = pydarm.measurement.Measurement(meas_file_2)
        process_sensing = \
            pydarm.measurement.ProcessActuationMeasurement(
                model_string, 'actuation_x_arm', meas1, meas2,
                ('H1:SUS-ETMX_L3_CAL_EXC', 'H1:LSC-DARM_IN1_DQ'),
                ('H1:CAL-PCALY_RX_PD_OUT_DQ', 'H1:LSC-DARM_IN1_DQ'),
                meas1_cohThresh=0.9, meas2_cohThresh=0.9)

        freq, processed_tst_resp, processed_tst_resp_unc = \
            process_sensing.get_processed_measurement_response()

        for n in range(len(self.known_freq)):
            # Test absolute differences
            self.assertAlmostEqual(freq[n], self.known_freq[n], places=3)
            self.assertAlmostEqual(np.abs(processed_tst_resp[n]),
                                   self.known_tf_mag[n])
            self.assertAlmostEqual(np.angle(processed_tst_resp[n], deg=True),
                                   self.known_tf_angle[n], places=3)
            self.assertAlmostEqual(processed_tst_resp_unc[n],
                                   self.known_tf_unc[n], places=5)
            # Test relative differences
            self.assertAlmostEqual(freq[n] / self.known_freq[n], 1.0, places=4)
            self.assertAlmostEqual(
                np.abs(processed_tst_resp[n]) / self.known_tf_mag[n], 1.0,
                places=4)
            self.assertAlmostEqual(np.angle(processed_tst_resp[n], deg=True) /
                                   self.known_tf_angle[n], 1.0, places=2)
            self.assertAlmostEqual(
                processed_tst_resp_unc[n] / self.known_tf_unc[n], 1.0,
                places=2)


class TestGetProcessedPUMResponse(unittest.TestCase):

    def setUp(self):
        data_in = np.genfromtxt(
            'test/2019-04-24_PUM.txt',
            dtype='float',
            delimiter=None)

        self.known_freq = data_in[:, 0]
        self.known_tf_mag = data_in[:, 1]
        self.known_tf_angle = data_in[:, 2]
        self.known_tf_unc = data_in[:, 3]

    def tearDown(self):
        del self.known_freq
        del self.known_tf_mag
        del self.known_tf_angle
        del self.known_tf_unc

    def test_get_processed_pum_response(self):
        """ Test the processing of the PUM response """

        # These are the xml files we want to get our data from.
        meas_file_1 = \
            'test/2019-04-24_H1SUSETMX_L2_iEXC2DARM_17min.xml'
        meas_file_2 = \
            'test/2019-04-24_H1SUSETMX_L2_PCAL2DARM_8min.xml'

        # This is the model that we need to use in order to process the data.
        model_string = '''
[metadata]
[interferometer]
[actuation_x_arm]
darm_feedback_sign = -1
uim_NpA       = 1.634
pum_NpA       = 0.02947
tst_NpV2      = 4.427e-11
linearization = OFF
actuation_esd_bias_voltage = -9.3
sus_filter_file = test/H1SUSETMX_1256232808.txt
tst_isc_inf_bank    = ETMX_L3_ISCINF_L
tst_isc_inf_modules =
tst_isc_inf_gain    = 1.0
tst_lock_bank       = ETMX_L3_LOCK_L
tst_lock_modules    = 5,8,9,10
tst_lock_gain       = 1.0
tst_drive_align_bank     = ETMX_L3_DRIVEALIGN_L2L
tst_drive_align_modules  = 4,5
tst_drive_align_gain     = -35.7
pum_lock_bank    = ETMX_L2_LOCK_L
pum_lock_modules = 7
pum_lock_gain    = 23.0
pum_drive_align_bank    = ETMX_L2_DRIVEALIGN_L2L
pum_drive_align_modules = 6,7
pum_drive_align_gain    = 1.0
pum_coil_outf_signflip  = 1
uim_lock_bank    = ETMX_L1_LOCK_L
#uim_lock_modules = 10
uim_lock_modules = 2,10
uim_lock_gain    = 1.06
uim_drive_align_bank    = ETMX_L1_DRIVEALIGN_L2L
uim_drive_align_modules =
uim_drive_align_gain    = 1.0
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
pum_driver_DC_trans_ApV = 2.6847e-4
uim_driver_DC_trans_ApV = 6.1535e-4
anti_imaging_rate_string = 16k
anti_imaging_method      = biquad
analog_anti_imaging_file = test/H1aa.mat
dac_gain = 7.62939453125e-05
unknown_actuation_delay = 15e-6
[pcal]
pcal_dewhiten               = 1.0, 1.0
ref_pcal_2_darm_act_sign    = -1.0
analog_anti_aliasing_file = test/H1aa.mat
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
'''
        meas1 = pydarm.measurement.Measurement(meas_file_1)
        meas2 = pydarm.measurement.Measurement(meas_file_2)
        process_sensing = \
            pydarm.measurement.ProcessActuationMeasurement(
                model_string, 'actuation_x_arm', meas1, meas2,
                ('H1:SUS-ETMX_L2_CAL_EXC', 'H1:LSC-DARM_IN1_DQ'),
                ('H1:CAL-PCALY_RX_PD_OUT_DQ', 'H1:LSC-DARM_IN1_DQ'),
                meas1_cohThresh=0.9, meas2_cohThresh=0.9)

        freq, processed_pum_resp, processed_pum_resp_unc = \
            process_sensing.get_processed_measurement_response()

        for n in range(len(self.known_freq)):
            # Test absolute differences
            self.assertAlmostEqual(freq[n], self.known_freq[n], places=3)
            self.assertAlmostEqual(np.abs(processed_pum_resp[n]),
                                   self.known_tf_mag[n], places=6)
            self.assertAlmostEqual(np.angle(processed_pum_resp[n], deg=True),
                                   self.known_tf_angle[n], places=2)
            self.assertAlmostEqual(processed_pum_resp_unc[n],
                                   self.known_tf_unc[n], places=6)
            # Test relative differences
            self.assertAlmostEqual(freq[n] / self.known_freq[n], 1.0,
                                   places=6)
            self.assertAlmostEqual(
                np.abs(processed_pum_resp[n]) / self.known_tf_mag[n], 1.0,
                places=4)
            self.assertAlmostEqual(np.angle(processed_pum_resp[n], deg=True) /
                                   self.known_tf_angle[n], 1.0, places=3)
            self.assertAlmostEqual(
                processed_pum_resp_unc[n] / self.known_tf_unc[n], 1.0,
                places=3)


class TestGetProcessedUIMResponse(unittest.TestCase):

    def setUp(self):
        data_in = np.genfromtxt(
            'test/2019-04-24_UIM.txt',
            dtype='float',
            delimiter=None)

        self.known_freq = data_in[:, 0]
        self.known_tf_mag = data_in[:, 1]
        self.known_tf_angle = data_in[:, 2]
        self.known_tf_unc = data_in[:, 3]

    def tearDown(self):
        del self.known_freq
        del self.known_tf_mag
        del self.known_tf_angle
        del self.known_tf_unc

    def test_get_processed_uim_response(self):
        """ Test the processing of the UIM response """

        # These are the xml files we want to get our data from.
        meas_file_1 = \
            'test/2019-04-24_H1SUSETMX_L1_iEXC2DARM_10min.xml'
        meas_file_2 = \
            'test/2019-04-24_H1SUSETMX_L1_PCAL2DARM_8min.xml'

        # This is the model that we need to use in order to process the data.
        model_string = '''
[metadata]
[interferometer]
[actuation_x_arm]
darm_feedback_sign = -1
uim_NpA       = 1.634
pum_NpA       = 0.02947
tst_NpV2      = 4.427e-11
linearization = OFF
actuation_esd_bias_voltage = -9.3
sus_filter_file = test/H1SUSETMX_1256232808.txt
tst_isc_inf_bank    = ETMX_L3_ISCINF_L
tst_isc_inf_modules =
tst_isc_inf_gain    = 1.0
tst_lock_bank       = ETMX_L3_LOCK_L
tst_lock_modules    = 5,8,9,10
tst_lock_gain       = 1.0
tst_drive_align_bank     = ETMX_L3_DRIVEALIGN_L2L
tst_drive_align_modules  = 4,5
tst_drive_align_gain     = -35.7
pum_lock_bank    = ETMX_L2_LOCK_L
pum_lock_modules = 7
pum_lock_gain    = 23.0
pum_drive_align_bank    = ETMX_L2_DRIVEALIGN_L2L
pum_drive_align_modules = 6,7
pum_drive_align_gain    = 1.0
pum_coil_outf_signflip  = 1
uim_lock_bank    = ETMX_L1_LOCK_L
#uim_lock_modules = 10
uim_lock_modules = 2,10
uim_lock_gain    = 1.06
uim_drive_align_bank    = ETMX_L1_DRIVEALIGN_L2L
uim_drive_align_modules =
uim_drive_align_gain    = 1.0
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
pum_driver_DC_trans_ApV = 2.6847e-4
uim_driver_DC_trans_ApV = 6.1535e-4
anti_imaging_rate_string = 16k
anti_imaging_method      = biquad
analog_anti_imaging_file = test/H1aa.mat
dac_gain = 7.62939453125e-05
unknown_actuation_delay = 15e-6
[pcal]
pcal_dewhiten               = 1.0, 1.0
ref_pcal_2_darm_act_sign    = -1.0
analog_anti_aliasing_file = test/H1aa.mat
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
'''
        meas1 = pydarm.measurement.Measurement(meas_file_1)
        meas2 = pydarm.measurement.Measurement(meas_file_2)
        process_sensing = \
            pydarm.measurement.ProcessActuationMeasurement(
                model_string, 'actuation_x_arm', meas1, meas2,
                ('H1:SUS-ETMX_L1_CAL_EXC', 'H1:LSC-DARM_IN1_DQ'),
                ('H1:CAL-PCALY_RX_PD_OUT_DQ', 'H1:LSC-DARM_IN1_DQ'),
                meas1_cohThresh=0.9, meas2_cohThresh=0.9)

        freq, processed_uim_resp, processed_uim_resp_unc = \
            process_sensing.get_processed_measurement_response()

        for n in range(len(self.known_freq)):
            # Test absolute differences
            self.assertAlmostEqual(freq[n], self.known_freq[n], places=3)
            self.assertAlmostEqual(np.abs(processed_uim_resp[n]),
                                   self.known_tf_mag[n], places=-1)
            self.assertAlmostEqual(np.angle(processed_uim_resp[n], deg=True),
                                   self.known_tf_angle[n], places=4)
            self.assertAlmostEqual(processed_uim_resp_unc[n],
                                   self.known_tf_unc[n], places=6)
            # Test relative differences
            self.assertAlmostEqual(freq[n] / self.known_freq[n], 1.0,
                                   places=6)
            self.assertAlmostEqual(
                np.abs(processed_uim_resp[n]) / self.known_tf_mag[n], 1.0,
                places=5)
            self.assertAlmostEqual(np.angle(processed_uim_resp[n], deg=True) /
                                   self.known_tf_angle[n], 1.0, places=5)
            self.assertAlmostEqual(
                processed_uim_resp_unc[n] / self.known_tf_unc[n], 1.0,
                places=2)


class TestRescaleActuationByTDCFVal(unittest.TestCase):

    def setUp(self):
        meas_object = pydarm.measurement.Measurement(
            './test/2020-01-03_H1_DARM_OLGTF_LF_SS_5to1100Hz_15min.xml')
        model_string = '''
[metadata]
[interferometer]
[actuation]
[actuation_x_arm]
[pcal]
'''
        self.meas = pydarm.measurement.ProcessActuationMeasurement(
            model_string, 'actuation_x_arm',
            meas_object, meas_object,
            ('H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_IN1'),
            ('H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_IN1'))
        self.tdcf_val = 2.0
        self.known_scaled_tf = np.ones(10, dtype='complex')
        self.known_tf = self.tdcf_val * self.known_scaled_tf

    def tearDown(self):
        del self.meas
        del self.tdcf_val
        del self.known_tf
        del self.known_scaled_tf

    def test_rescale_actuation_by_tdcf_val(self):
        """ Test rescale_actuation_by_tdcf_val() """
        rescaled_response = self.meas.rescale_actuation_by_tdcf_val(
            self.known_tf, self.tdcf_val)

        self.assertTrue(np.allclose(rescaled_response, self.known_scaled_tf))


class TestActuationRunMCMC(unittest.TestCase):

    def setUp(self):
        meas_obj1 = pydarm.measurement.Measurement(
            './test/2019-04-24_H1SUSETMX_L3_iEXC2DARM_8min.xml')
        meas_obj2 = pydarm.measurement.Measurement(
            './test/2019-04-24_H1SUSETMX_L3_PCAL2DARM_8min.xml')
        model_string = '''
[metadata]
[interferometer]
[actuation_x_arm]
darm_feedback_sign = -1
uim_NpA       = 1.634
pum_NpA       = 0.02947
tst_NpV2      = 4.427e-11
linearization = OFF
actuation_esd_bias_voltage = -9.3
sus_filter_file = test/H1SUSETMX_1236641144.txt
tst_isc_inf_bank    = ETMX_L3_ISCINF_L
tst_isc_inf_modules =
tst_isc_inf_gain    = 1.0
tst_lock_bank       = ETMX_L3_LOCK_L
tst_lock_modules    = 5,8,9,10
tst_lock_gain       = 1.0
tst_drive_align_bank     = ETMX_L3_DRIVEALIGN_L2L
tst_drive_align_modules  = 4,5
tst_drive_align_gain     = -35.7
pum_lock_bank    = ETMX_L2_LOCK_L
pum_lock_modules = 7
pum_lock_gain    = 23.0
pum_drive_align_bank    = ETMX_L2_DRIVEALIGN_L2L
pum_drive_align_modules = 6,7
pum_drive_align_gain    = 1.0
pum_coil_outf_signflip  = 1
uim_lock_bank    = ETMX_L1_LOCK_L
uim_lock_modules = 10
uim_lock_gain    = 1.06
uim_drive_align_bank    = ETMX_L1_DRIVEALIGN_L2L
uim_drive_align_modules =
uim_drive_align_gain    = 1.0
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
pum_driver_DC_trans_ApV = 2.6847e-4
uim_driver_DC_trans_ApV = 6.1535e-4
anti_imaging_rate_string = 16k
anti_imaging_method      = biquad
analog_anti_imaging_file = test/H1aa.mat
dac_gain = 7.62939453125e-05
unknown_actuation_delay = 15e-6
[pcal]
pcal_dewhiten               = 1.0, 1.0
ref_pcal_2_darm_act_sign    = -1.0
analog_anti_aliasing_file = test/H1aa.mat
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
'''

        self.meas = pydarm.measurement.ProcessActuationMeasurement(
            model_string, 'actuation_x_arm', meas_obj1, meas_obj2,
            ('H1:SUS-ETMX_L3_CAL_EXC', 'H1:LSC-DARM_IN1_DQ'),
            ('H1:CAL-PCALY_RX_PD_OUT_DQ', 'H1:LSC-DARM_IN1_DQ'),
            meas1_cohThresh=0.9, meas2_cohThresh=0.9)

        self.known_map_vals = np.array([4.41748043e-11, 7.55158561e+00])
        self.known_std = np.array([9.33932576e-15, 5.12740323e-01])

    def tearDown(self):
        del self.meas
        del self.known_map_vals
        del self.known_std

    def test_run_mcmc(self):
        chain = self.meas.run_mcmc(fmin=20, fmax=600,
                                   burn_in_steps=200, steps=2000)
        map_vals = np.median(chain, axis=0)
        std_vals = np.std(chain, axis=0)

        # Compare relative errors
        self.assertAlmostEqual(map_vals[0] / self.known_map_vals[0], 1.0,
                               places=5)
        self.assertAlmostEqual(map_vals[1], self.known_map_vals[1], places=1)
        self.assertAlmostEqual(std_vals[0] / self.known_std[0], 1.0, places=1)
        self.assertAlmostEqual(std_vals[1] / self.known_std[1], 1.0, places=2)


class TestActuationSaveResultsToJson(unittest.TestCase):

    def setUp(self):
        self.filename = 'test.json'
        self.fmin = None
        self.fmax = None
        self.mcmc_map_vals = np.atleast_2d(
            np.array([4e-11, 4.]))

    def tearDown(self):
        del self.filename
        del self.fmin
        del self.fmax
        del self.mcmc_map_vals

    def test_save_results_to_json(self):
        model_string = '''
[metadata]
[interferometer]
[actuation_x_arm]
[pcal]
'''
        meas_obj1 = pydarm.measurement.Measurement(
            './test/2019-04-24_H1SUSETMX_L3_iEXC2DARM_8min.xml')
        meas_obj2 = pydarm.measurement.Measurement(
            './test/2019-04-24_H1SUSETMX_L3_PCAL2DARM_8min.xml')

        meas = pydarm.measurement.ProcessActuationMeasurement(
            model_string, 'actuation_x_arm', meas_obj1, meas_obj2,
            ('H1:SUS-ETMX_L3_CAL_EXC', 'H1:LSC-DARM_IN1_DQ'),
            ('H1:CAL-PCALY_RX_PD_OUT_DQ', 'H1:LSC-DARM_IN1_DQ'))

        meas.save_results_to_json(self.filename, self.fmin, self.fmax,
                                  self.mcmc_map_vals, 'actuation')


class TestActuationQueryResultsFromJson(unittest.TestCase):

    def setUp(self):
        model_string = model_string = '''
[metadata]
[interferometer]
[actuation_x_arm]
darm_feedback_sign = -1
uim_NpA       = 1.634
pum_NpA       = 0.02947
tst_NpV2      = 4.427e-11
linearization = OFF
actuation_esd_bias_voltage = -9.3
sus_filter_file = test/H1SUSETMX_1236641144.txt
tst_isc_inf_bank    = ETMX_L3_ISCINF_L
tst_isc_inf_modules =
tst_isc_inf_gain    = 1.0
tst_lock_bank       = ETMX_L3_LOCK_L
tst_lock_modules    = 5,8,9,10
tst_lock_gain       = 1.0
tst_drive_align_bank     = ETMX_L3_DRIVEALIGN_L2L
tst_drive_align_modules  = 4,5
tst_drive_align_gain     = -35.7
pum_lock_bank    = ETMX_L2_LOCK_L
pum_lock_modules = 7
pum_lock_gain    = 23.0
pum_drive_align_bank    = ETMX_L2_DRIVEALIGN_L2L
pum_drive_align_modules = 6,7
pum_drive_align_gain    = 1.0
pum_coil_outf_signflip  = 1
uim_lock_bank    = ETMX_L1_LOCK_L
uim_lock_modules = 10
uim_lock_gain    = 1.06
uim_drive_align_bank    = ETMX_L1_DRIVEALIGN_L2L
uim_drive_align_modules =
uim_drive_align_gain    = 1.0
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
pum_driver_DC_trans_ApV = 2.6847e-4
uim_driver_DC_trans_ApV = 6.1535e-4
anti_imaging_rate_string = 16k
anti_imaging_method      = biquad
analog_anti_imaging_file = test/H1aa.mat
dac_gain = 7.62939453125e-05
unknown_actuation_delay = 15e-6
[pcal]
pcal_dewhiten               = 1.0, 1.0
ref_pcal_2_darm_act_sign    = -1.0
analog_anti_aliasing_file = test/H1aa.mat
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
'''
        meas_obj1 = pydarm.measurement.Measurement(
            './test/2019-04-24_H1SUSETMX_L3_iEXC2DARM_8min.xml')
        meas_obj2 = pydarm.measurement.Measurement(
            './test/2019-04-24_H1SUSETMX_L3_PCAL2DARM_8min.xml')

        self.meas = pydarm.measurement.ProcessActuationMeasurement(
            model_string, 'actuation_x_arm', meas_obj1, meas_obj2,
            ('H1:SUS-ETMX_L3_CAL_EXC', 'H1:LSC-DARM_IN1_DQ'),
            ('H1:CAL-PCALY_RX_PD_OUT_DQ', 'H1:LSC-DARM_IN1_DQ'),
            json_results_file='./test/O3_H1_actuation.json',
            meas1_cohThresh=0.9, meas2_cohThresh=0.9)
        self.known_vals = np.asarray([4.417471244302878e-11,
                                      7.546965155950316])

    def tearDown(self):
        del self.meas
        del self.known_vals

    def test_query_results_from_json(self):
        test = self.meas.query_results_from_json(
            'actuation_x_arm', fmin=20, fmax=600)
        self.assertTrue(np.allclose(test[1], self.known_vals))


class TestActuationStackMeasurements(unittest.TestCase):

    def setUp(self):
        meas_obj1 = pydarm.measurement.Measurement(
            './test/2019-04-24_H1SUSETMX_L3_iEXC2DARM_8min.xml')
        meas_obj2 = pydarm.measurement.Measurement(
            './test/2019-04-24_H1SUSETMX_L3_PCAL2DARM_8min.xml')
        model_string = '''
[metadata]
[interferometer]
[actuation_x_arm]
darm_feedback_sign = -1
uim_NpA       = 1.634
pum_NpA       = 0.02947
tst_NpV2      = 4.427e-11
linearization = OFF
actuation_esd_bias_voltage = -9.3
sus_filter_file = test/H1SUSETMX_1236641144.txt
tst_isc_inf_bank    = ETMX_L3_ISCINF_L
tst_isc_inf_modules =
tst_isc_inf_gain    = 1.0
tst_lock_bank       = ETMX_L3_LOCK_L
tst_lock_modules    = 5,8,9,10
tst_lock_gain       = 1.0
tst_drive_align_bank     = ETMX_L3_DRIVEALIGN_L2L
tst_drive_align_modules  = 4,5
tst_drive_align_gain     = -35.7
pum_lock_bank    = ETMX_L2_LOCK_L
pum_lock_modules = 7
pum_lock_gain    = 23.0
pum_drive_align_bank    = ETMX_L2_DRIVEALIGN_L2L
pum_drive_align_modules = 6,7
pum_drive_align_gain    = 1.0
pum_coil_outf_signflip  = 1
uim_lock_bank    = ETMX_L1_LOCK_L
uim_lock_modules = 10
uim_lock_gain    = 1.06
uim_drive_align_bank    = ETMX_L1_DRIVEALIGN_L2L
uim_drive_align_modules =
uim_drive_align_gain    = 1.0
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
pum_driver_DC_trans_ApV = 2.6847e-4
uim_driver_DC_trans_ApV = 6.1535e-4
anti_imaging_rate_string = 16k
anti_imaging_method      = biquad
analog_anti_imaging_file = test/H1aa.mat
dac_gain = 7.62939453125e-05
unknown_actuation_delay = 15e-6
[pcal]
pcal_dewhiten               = 1.0, 1.0
ref_pcal_2_darm_act_sign    = -1.0
analog_anti_aliasing_file = test/H1aa.mat
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
'''

        self.meas = pydarm.measurement.ProcessActuationMeasurement(
            model_string, 'actuation_x_arm', meas_obj1, meas_obj2,
            ('H1:SUS-ETMX_L3_CAL_EXC', 'H1:LSC-DARM_IN1_DQ'),
            ('H1:CAL-PCALY_RX_PD_OUT_DQ', 'H1:LSC-DARM_IN1_DQ'),
            meas1_cohThresh=0.9, meas2_cohThresh=0.9,
            json_results_file='./test/O3_H1_actuation.json')

        self.meas2 = pydarm.measurement.ProcessActuationMeasurement(
            model_string, 'actuation_x_arm', meas_obj1, meas_obj2,
            ('H1:SUS-ETMX_L3_CAL_EXC', 'H1:LSC-DARM_IN1_DQ'),
            ('H1:CAL-PCALY_RX_PD_OUT_DQ', 'H1:LSC-DARM_IN1_DQ'),
            meas1_cohThresh=0.9, meas2_cohThresh=0.9,
            json_results_file='./test/O3_H1_actuation.json')

        self.known_freq = np.array(
            [7.0, 7.6529, 8.3666, 10.0, 12.1153, 14.678, 15.6, 16.4, 17.1,
             17.6, 19.1, 21.5443, 26.1016, 31.6228, 38.3119, 46.4159, 56.2341,
             68.1292, 82.54, 100.0, 134.224, 177.828, 237.137, 292.211,
             340.654, 433.7, 490.327, 543.213, 625.742, 699.465, 749.894,
             824.265, 962.764, 1221.57])
        self.known_act_resp = np.array(
            [4.600713959860163e-11+1.0080589647955395e-12j,
             4.3249832259388226e-11+4.408071320942729e-13j,
             4.48155795609468e-11+3.86874225385866e-13j,
             4.4660708979444904e-11-3.8004875444982484e-13j,
             4.425263927858843e-11-3.5425549114772793e-14j,
             4.421476396126438e-11-1.4203840636546456e-13j,
             4.421522955625061e-11-1.2553594713881172e-13j,
             4.418636660252522e-11-1.0700918520635529e-13j,
             4.4187661466837905e-11-7.898033591443161e-14j,
             4.426465311599576e-11-5.757913893767196e-14j,
             4.426198835523701e-11-4.836467037182701e-14j,
             4.4212504188651004e-11-9.98667602352944e-14j,
             4.417750488110072e-11-6.587983024452382e-14j,
             4.4171939096159955e-11-5.183099895588114e-14j,
             4.4144233164685666e-11-8.0896350040868e-14j,
             4.4165781727314084e-11-8.928868719903062e-14j,
             4.420975466340609e-11-1.0683151491413745e-13j,
             4.413865448552216e-11-1.2087638132471638e-13j,
             4.415523144790698e-11-2.1795609414185902e-13j,
             4.4083317409918716e-11-2.139793293142482e-13j,
             4.401117360813622e-11-2.57927709143044e-13j,
             4.416408137947615e-11-4.1265399688173483e-13j,
             4.435259473093628e-11-2.2381956444257016e-13j,
             4.366185379385905e-11-7.636270168782189e-13j,
             4.438924517531857e-11-9.074260365559163e-13j,
             4.383262308491154e-11-6.937746864860927e-13j,
             4.3839230496539004e-11-6.027727906294568e-13j,
             4.417041964253939e-11-1.3423056309147865e-12j,
             4.3744330940010925e-11-1.4039314062379411e-12j,
             4.4228525304498916e-11-5.450496421816152e-13j,
             4.43374152373744e-11-7.487397304199775e-13j,
             4.210386132796535e-11-3.4919213295478316e-13j,
             4.3893120670781536e-11-1.5316483233478304e-12j,
             4.4104164987097186e-11-1.113668550447501e-12j])
        self.known_unc = np.array(
            [0.04250459, 0.012876861, 0.010742824, 0.007582212, 0.0015632747,
             0.0009036516, 0.0010863609, 0.0009886964, 0.00071596145,
             0.0013702465, 0.0005567265, 0.00044350346, 0.00042286396,
             0.00064130547, 0.0005777424, 0.00079860573, 0.0009036517,
             0.0010697736, 0.0007159614, 0.0017246293, 0.0041964506,
             0.0033547822, 0.005654715, 0.008364857, 0.0037388739,
             0.0041864677, 0.003776119, 0.0048317686, 0.0060286755,
             0.0065562637, 0.0060102274, 0.0333514, 0.014210214, 0.023705741])

    def tearDown(self):
        del self.meas
        del self.meas2
        del self.known_freq
        del self.known_act_resp
        del self.known_unc

    def test_stack_measurements(self):
        test = self.meas.stack_measurements([self.meas2], 20, 600,
                                            [20], [600])

        for n in range(len(test[0][0])):
            self.assertAlmostEqual(test[0][0][n] / self.known_freq[n], 1.0,
                                   places=6)
            self.assertAlmostEqual(
                np.abs(test[0][1][n])/np.abs(self.known_act_resp[n]), 1.0)
            self.assertAlmostEqual(
                np.abs(np.angle(test[0][1][n], deg=True) -
                       np.angle(self.known_act_resp[n], deg=True)),
                0.0, places=6)
            self.assertAlmostEqual(test[0][2][n] / self.known_unc[n], 1.0)

class TestActuationGPR(unittest.TestCase):

    def setUp(self):
        meas_obj1 = pydarm.measurement.Measurement(
            './test/2019-04-24_H1SUSETMX_L3_iEXC2DARM_8min.xml')
        meas_obj2 = pydarm.measurement.Measurement(
            './test/2019-04-24_H1SUSETMX_L3_PCAL2DARM_8min.xml')
        model_string = '''
[metadata]
[interferometer]
[actuation_x_arm]
darm_feedback_sign = -1
uim_NpA       = 1.634
pum_NpA       = 0.02947
tst_NpV2      = 4.427e-11
linearization = OFF
actuation_esd_bias_voltage = -9.3
sus_filter_file = test/H1SUSETMX_1236641144.txt
tst_isc_inf_bank    = ETMX_L3_ISCINF_L
tst_isc_inf_modules =
tst_isc_inf_gain    = 1.0
tst_lock_bank       = ETMX_L3_LOCK_L
tst_lock_modules    = 5,8,9,10
tst_lock_gain       = 1.0
tst_drive_align_bank     = ETMX_L3_DRIVEALIGN_L2L
tst_drive_align_modules  = 4,5
tst_drive_align_gain     = -35.7
pum_lock_bank    = ETMX_L2_LOCK_L
pum_lock_modules = 7
pum_lock_gain    = 23.0
pum_drive_align_bank    = ETMX_L2_DRIVEALIGN_L2L
pum_drive_align_modules = 6,7
pum_drive_align_gain    = 1.0
pum_coil_outf_signflip  = 1
uim_lock_bank    = ETMX_L1_LOCK_L
uim_lock_modules = 10
uim_lock_gain    = 1.06
uim_drive_align_bank    = ETMX_L1_DRIVEALIGN_L2L
uim_drive_align_modules =
uim_drive_align_gain    = 1.0
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
pum_driver_DC_trans_ApV = 2.6847e-4
uim_driver_DC_trans_ApV = 6.1535e-4
anti_imaging_rate_string = 16k
anti_imaging_method      = biquad
analog_anti_imaging_file = test/H1aa.mat
dac_gain = 7.62939453125e-05
unknown_actuation_delay = 15e-6
[pcal]
pcal_dewhiten               = 1.0, 1.0
ref_pcal_2_darm_act_sign    = -1.0
analog_anti_aliasing_file = test/H1aa.mat
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
'''

        self.meas = pydarm.measurement.ProcessActuationMeasurement(
            model_string, 'actuation_x_arm', meas_obj1, meas_obj2,
            ('H1:SUS-ETMX_L3_CAL_EXC', 'H1:LSC-DARM_IN1_DQ'),
            ('H1:CAL-PCALY_RX_PD_OUT_DQ', 'H1:LSC-DARM_IN1_DQ'),
            meas1_cohThresh=0.9, meas2_cohThresh=0.9,
            json_results_file='./test/O3_H1_actuation.json')

        self.meas2 = pydarm.measurement.ProcessActuationMeasurement(
            model_string, 'actuation_x_arm', meas_obj1, meas_obj2,
            ('H1:SUS-ETMX_L3_CAL_EXC', 'H1:LSC-DARM_IN1_DQ'),
            ('H1:CAL-PCALY_RX_PD_OUT_DQ', 'H1:LSC-DARM_IN1_DQ'),
            meas1_cohThresh=0.9, meas2_cohThresh=0.9,
            json_results_file='./test/O3_H1_actuation.json')

        self.freq = np.logspace(np.log10(5),np.log10(500),20)

        self.known_y_pred = np.array(
             [1.0006795 -0.00373967j,
              1.0010006 -0.00311973j,
              1.00117371-0.0025628j,
              1.00121982-0.00209224j,
              1.00116073-0.00173205j,
              1.00101813-0.00150601j,
              1.0008127 -0.00143684j,
              1.00056321-0.00154525j,
              1.00028577-0.00184909j,
              0.99999319-0.00236248j,
              0.99969445-0.00309507j,
              0.99939444-0.00405139j,
              0.99909381-0.00523045j,
              0.99878906-0.00662545j,
              0.99847277-0.00822369j,
              0.99813409-0.01000678j,
              0.9977593 -0.01195099j,
              0.99733252-0.01402785j,
              0.99683654-0.01620487j,
              0.99625362-0.0184465j ])

        self.known_sigma = np.array(
             [0.04130269, 0.03193534, 0.02395265, 0.0174245, 0.0124513, 0.00919158,
              0.0077308, 0.00769416, 0.00836436, 0.00926477, 0.01023673, 0.01125869,
              0.01232628, 0.01341221, 0.01447537, 0.01549535, 0.01651721, 0.01769553,
              0.01931754, 0.0217703 ])

    def tearDown(self):
        del self.meas
        del self.meas2
        del self.freq
        del self.known_y_pred
        del self.known_sigma

    def test_actuation_gpr(self):
        test = self.meas.run_gpr(self.freq, [self.meas2], 20, 600,[20], [600])

        for n in range(len(test[0])):
            self.assertAlmostEqual(
                np.abs(test[0][n])/np.abs(self.known_y_pred[n]), 1.0, places=4)
            self.assertAlmostEqual(np.angle(test[0][n], deg=True) -
                np.angle(self.known_y_pred[n], deg=True), 0.0, places=4)
            self.assertAlmostEqual(test[1][n] / self.known_sigma[n], 1.0, places=4)


if __name__ == '__main__':
    unittest.main()
