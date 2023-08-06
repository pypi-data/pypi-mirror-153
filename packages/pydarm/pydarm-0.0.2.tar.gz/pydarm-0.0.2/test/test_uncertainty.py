import unittest
import pydarm
import numpy as np
from gwpy.timeseries import TimeSeriesDict as tsd
import os


class TestTdcfMeanValues(unittest.TestCase):

    def setUp(self):
        self.known_values = np.array(
            [404.9034118652344,
             1.001456618309021,
             1.000232577323914,
             1.001761555671692,
             0.9874549508094788,
             0.001804656465537846,
             0.001688393531367183,
             0.001474045449867845,
             0.001592247281223536,
             0.001256731105968356])

    def tearDown(self):
        del self.known_values

    def test_tdcf_mean_values(self):
        data = tsd.read('./test/test_ch_data.hdf5')
        for idx, name in enumerate(list(data)):
            mean = np.mean(data[name].value)
            self.assertAlmostEqual(mean, self.known_values[idx])


class TestSampleLineUncertainty(unittest.TestCase):

    def setUp(self):
        self.data = tsd.read('./test/test_ch_data.hdf5')

    def tearDown(self):
        del self.data

    def test_no_uncertainty(self):
        config = '''[reference-model]
model = example_model_files/H1_20190416.ini
[sensing-tdcf]
pcal2_unc = 0
[x-arm-tdcf]
pcal1_unc = 0
uim_unc = 0
pum_unc = 0
tst_unc = 0
[tdcf-data]
frametype = R
duration = 130
[sample-tdcf]
kappa_c = False
f_cc = False
kappa_uim = False
kappa_pum = False
kappa_tst = False'''

        test_unc = pydarm.uncertainty.DARMUncertainty(config)
        a, b, c = test_unc.sample_line_uncertainty(1239958818, data=self.data)
        self.assertAlmostEqual(a, 1)
        for n in range(len(b)):
            self.assertAlmostEqual(b[n], 1)
            self.assertAlmostEqual(c[n], 1)

    def test_sample_line_uncertainty(self):
        config = '''[reference-model]
model = example_model_files/H1_20190416.ini
[sensing-tdcf]
[x-arm-tdcf]
[tdcf-data]
frametype = R
duration = 130
[sample-tdcf]
kappa_c = False
f_cc = False
kappa_uim = False
kappa_pum = False
kappa_tst = False'''

        test_unc = pydarm.uncertainty.DARMUncertainty(config)
        a, b, c = test_unc.sample_line_uncertainty(1239958818, data=self.data)
        self.assertAlmostEqual(a, 1, places=2)
        for n in range(len(b)):
            self.assertAlmostEqual(b[n], 1, places=2)
            self.assertAlmostEqual(c[n], 1, places=2)


class TestSamplePcalUnc(unittest.TestCase):

    def setUp(self):
        self.expected = 1

    def tearDown(self):
        del self.expected

    def test_sample_pcal_unc(self):
        test = pydarm.uncertainty.DARMUncertainty.sample_pcal_unc(err=1, unc=0)

        self.assertAlmostEqual(test, self.expected)


class TestGetModelPars(unittest.TestCase):

    def setUp(self):
        self.config = '''[metadata]
[interferometer]
[sensing]
coupled_cavity_optical_gain   = 3.22e6
coupled_cavity_pole_frequency = 410.6
detuned_spring_frequency      = 4.468
detuned_spring_Q              = 52.14
single_pole_approximation_delay_correction = -12e-6
[digital]
[actuation]
[actuation_x_arm]
uim_NpA       = 1.634
pum_NpA       = 0.02947
tst_NpV2      = 4.427e-11
uim_delay = 0
pum_delay = 0
tst_delay = 0
'''

    def tearDown(self):
        del self.config

    def test_get_model_pars(self):
        darm = pydarm.darm.DARMModel(self.config)

        sens_pars, act_pars = pydarm.uncertainty.DARMUncertainty.get_model_pars(darm)
        self.assertAlmostEqual(sens_pars['gain'],
                               darm.sensing.coupled_cavity_optical_gain)
        self.assertAlmostEqual(sens_pars['f_cc'],
                               darm.sensing.coupled_cavity_pole_frequency)
        self.assertAlmostEqual(sens_pars['f_s'],
                               darm.sensing.detuned_spring_frequency)
        self.assertAlmostEqual(sens_pars['Q'],
                               darm.sensing.detuned_spring_q)
        self.assertAlmostEqual(sens_pars['single_pole_delay_corr'],
                               darm.sensing.single_pole_approximation_delay_correction)
        self.assertAlmostEqual(act_pars['xarm']['UIM'][0],
                               darm.actuation.xarm.uim_npa)
        self.assertAlmostEqual(act_pars['xarm']['PUM'][0],
                               darm.actuation.xarm.pum_npa)
        self.assertAlmostEqual(act_pars['xarm']['TST'][0],
                               darm.actuation.xarm.tst_npv2)
        self.assertAlmostEqual(act_pars['xarm']['UIM'][1],
                               darm.actuation.xarm.uim_delay)
        self.assertAlmostEqual(act_pars['xarm']['PUM'][1],
                               darm.actuation.xarm.pum_delay)
        self.assertAlmostEqual(act_pars['xarm']['TST'][1],
                               darm.actuation.xarm.tst_delay)


class TestSampleResponse(unittest.TestCase):

    def setUp(self):
        self.data = tsd.read('./test/test_ch_data.hdf5')
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        
        os.environ['CAL_DATA_ROOT'] = './test'
        """ref_model = pydarm.darm.DARMModel('./example_model_files/H1_20190416.ini')
        ref_model.sensing.coupled_cavity_optical_gain *= 1.001456618309021
        ref_model.sensing.coupled_cavity_pole_frequency = 404.9034118652344
        ref_model.actuation.xarm.uim_npa *= 0.9874549508094788
        ref_model.actuation.xarm.pum_npa *= 1.0002325773239136
        ref_model.actuation.xarm.tst_npv2 *= 1.001761555671692
        known_response = ref_model.compute_response_function(self.frequencies)
        for n in range(len(known_response)):
            print(known_response[n])"""
        self.known_response = np.array(
            [2.028504986095783-0.3875242485008085j,
             0.001141684700656659-0.004462191049044788j,
             7.183993452924785e-06-1.428672439631115e-06j,
             -6.508352356473097e-07+1.554166057335518e-07j,
             -2.19294725075012e-09-1.989291669099206e-07j,
             1.672640015694479e-07+2.137038974884646e-08j,
             2.112268336596777e-07+3.617519908798565e-07j,
             -7.522130216217252e-08+6.428161477749937e-07j,
             -1.482755716524026e-06+3.028370715328025e-07j,
             4.522732922137328e-06-1.53996316224857e-06j])

    def tearDown(self):
        del self.data
        del self.frequencies
        del self.known_response
        del os.environ['CAL_DATA_ROOT']

    def test_sample_response_no_tdcf_application(self):
        config = '''[reference-model]
model = example_model_files/H1_20190416.ini
[sensing-measurement-files]
mcmc =
gpr =
[x-arm-measurement-files]
tst_mcmc =
pum_mcmc =
uim_mcmc =
tst_gpr =
pum_gpr =
uim_gpr =
[x-arm-sus-cal-lines]
uim = 15.6
pum = 16.4
tst = 17.6
[y-arm-pcal-cal-lines]
sus = 17.1
sensing = 410.3
pcal3 = 1083.7
pcal4 = 7.93
[tdcf-data]
frametype = R
duration = 130
[sensing-tdcf]
kappa_c = CAL-CS_TDEP_KAPPA_C_OUTPUT
f_cc = CAL-CS_TDEP_F_C_OUTPUT
pcal2_unc = CAL-CS_TDEP_PCAL_LINE2_UNCERTAINTY
pcal_arm = Y
[x-arm-tdcf]
kappa_uim = CAL-CS_TDEP_KAPPA_UIM_REAL_OUTPUT
kappa_pum = CAL-CS_TDEP_KAPPA_PUM_REAL_OUTPUT
kappa_tst = CAL-CS_TDEP_KAPPA_TST_REAL_OUTPUT
pcal1_unc = CAL-CS_TDEP_PCAL_LINE1_UNCERTAINTY
uim_unc = CAL-CS_TDEP_SUS_LINE1_UNCERTAINTY
pum_unc = CAL-CS_TDEP_SUS_LINE2_UNCERTAINTY
tst_unc = CAL-CS_TDEP_SUS_LINE3_UNCERTAINTY
pcal_arm = Y
[sample-tdcf]
kappa_c = False
f_cc = False
kappa_uim = False
kappa_pum = False
kappa_tst = False
[pcal]
sys_err =
sys_unc =
sample = False'''

        test_unc = pydarm.uncertainty.DARMUncertainty(config)
        test_response, data, c_pars, a_pars, c_syserr, a_syserr = \
            test_unc.sample_response(
                1239958818, self.frequencies, data=self.data)

        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(test_response[n]) / np.abs(self.known_response[n]), 1.0)
            self.assertAlmostEqual(
                np.angle(test_response[n], deg=True) -
                np.angle(self.known_response[n], deg=True), 0.0, places=5)

    def test_sample_response(self):
        config2 = '''[reference-model]
model = example_model_files/H1_20190416.ini
[sensing-measurement-files]
mcmc =
gpr =
[x-arm-measurement-files]
tst_mcmc =
pum_mcmc =
uim_mcmc =
tst_gpr =
pum_gpr =
uim_gpr =
[x-arm-sus-cal-lines]
uim = 15.6
pum = 16.4
tst = 17.6
[y-arm-pcal-cal-lines]
sus = 17.1
sensing = 410.3
pcal3 = 1083.7
pcal4 = 7.93
[tdcf-data]
frametype = R
duration = 130
[sensing-tdcf]
kappa_c = CAL-CS_TDEP_KAPPA_C_OUTPUT
f_cc = CAL-CS_TDEP_F_C_OUTPUT
pcal2_unc = 0
pcal_arm = Y
[x-arm-tdcf]
kappa_uim = CAL-CS_TDEP_KAPPA_UIM_REAL_OUTPUT
kappa_pum = CAL-CS_TDEP_KAPPA_PUM_REAL_OUTPUT
kappa_tst = CAL-CS_TDEP_KAPPA_TST_REAL_OUTPUT
pcal1_unc = 0
uim_unc = 0
pum_unc = 0
tst_unc = 0
pcal_arm = Y
[sample-tdcf]
kappa_c = False
f_cc = False
kappa_uim = True
kappa_pum = True
kappa_tst = True
[pcal]
sys_err = 1
sys_unc = 0
sample = True'''

        test_unc = pydarm.uncertainty.DARMUncertainty(config2)
        test_response, data, c_pars, a_pars, c_syserr, a_syserr = \
            test_unc.sample_response(
                1239958818, self.frequencies, data=self.data)

        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(test_response[n]) / np.abs(self.known_response[n]), 1.0)
            self.assertAlmostEqual(
                np.angle(test_response[n], deg=True) -
                np.angle(self.known_response[n], deg=True), 0.0, places=5)


class TestNominalResponse(unittest.TestCase):

    def setUp(self):
        self.data = tsd.read('./test/test_ch_data.hdf5')
        self.frequencies = np.logspace(0, np.log10(5000.), 10)

        """ref_model = pydarm.darm.DARMModel('./example_model_files/H1_20190416.ini')
        ref_model.sensing.coupled_cavity_optical_gain = 3224690.3109550476
        ref_model.sensing.coupled_cavity_pole_frequency = 404.9034118652344
        ref_model.actuation.xarm.uim_npa = 1.6135013896226882
        ref_model.actuation.xarm.pum_npa = 0.029476854053735745
        ref_model.actuation.xarm.tst_npv2 = 4.43479840695858e-11
        known_response = ref_model.compute_response_function(self.frequencies)
        for n in range(len(known_response)):
            print(known_response[n])"""
        self.known_response = np.array(
            [2.028504986095783-0.3875242485008085j,
             0.001141684700656659-0.004462191049044788j,
             7.183993452924785e-06-1.428672439631115e-06j,
             -6.508352356473097e-07+1.554166057335518e-07j,
             -2.19294725075012e-09-1.989291669099206e-07j,
             1.672640015694479e-07+2.137038974884646e-08j,
             2.112268336596777e-07+3.617519908798565e-07j,
             -7.522130216217252e-08+6.428161477749937e-07j,
             -1.482755716524026e-06+3.028370715328025e-07j,
             4.522732922137328e-06-1.53996316224857e-06j])
        os.environ['CAL_DATA_ROOT'] = './test'

    def tearDown(self):
        del self.data
        del self.frequencies
        del self.known_response
        del os.environ['CAL_DATA_ROOT']

    def test_nominal_response(self):
        config = '''[reference-model]
model = example_model_files/H1_20190416.ini
[x-arm-measurement-files]
tst_mcmc =
pum_mcmc =
uim_mcmc =
tst_gpr =
pum_gpr =
uim_gpr =
[x-arm-sus-cal-lines]
uim = 15.6
pum = 16.4
tst = 17.6
[y-arm-pcal-cal-lines]
sus = 17.1
sensing = 410.3
pcal3 = 1083.7
pcal4 = 7.93
[tdcf-data]
frametype = R
duration = 130
[sensing-tdcf]
kappa_c = CAL-CS_TDEP_KAPPA_C_OUTPUT
f_cc = CAL-CS_TDEP_F_C_OUTPUT
pcal2_unc = CAL-CS_TDEP_PCAL_LINE2_UNCERTAINTY
pcal_arm = Y
[x-arm-tdcf]
kappa_uim = CAL-CS_TDEP_KAPPA_UIM_REAL_OUTPUT
kappa_pum = CAL-CS_TDEP_KAPPA_PUM_REAL_OUTPUT
kappa_tst = CAL-CS_TDEP_KAPPA_TST_REAL_OUTPUT
pcal1_unc = CAL-CS_TDEP_PCAL_LINE1_UNCERTAINTY
uim_unc = CAL-CS_TDEP_SUS_LINE1_UNCERTAINTY
pum_unc = CAL-CS_TDEP_SUS_LINE2_UNCERTAINTY
tst_unc = CAL-CS_TDEP_SUS_LINE3_UNCERTAINTY
pcal_arm = Y
[hoft-tdcf-data-application]
kappa_c = True
f_cc = True
kappa_uim = True
kappa_pum = True
kappa_tst = True
pcal_sys_err = True
[pcal]
sys_err = 1'''

        test_unc = pydarm.uncertainty.DARMUncertainty(config)
        
        test_response, data = test_unc.nominal_response(
            1239958818, self.frequencies, data=self.data)

        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(test_response[n]) / np.abs(self.known_response[n]), 1.0)
            self.assertAlmostEqual(
                np.angle(test_response[n], deg=True) -
                np.angle(self.known_response[n], deg=True), 0.0, places=5)

class TestComputeResponseUncertainty(unittest.TestCase):

    def setUp(self):
        self.data = tsd.read('./test/test_ch_data.hdf5')
        self.frequencies = np.logspace(0, np.log10(5000.), 10)

        self.known_ratio = np.ones(len(self.frequencies), dtype='complex128')
        os.environ['CAL_DATA_ROOT'] = './test'

    def tearDown(self):
        del self.data
        del self.frequencies
        del os.environ['CAL_DATA_ROOT']

    def test_compute_response_uncertainty(self):
        config = '''[reference-model]
model = example_model_files/H1_20190416.ini
[sensing-measurement-files]
mcmc = 
gpr = 
[x-arm-measurement-files]
tst_mcmc = 
pum_mcmc = 
uim_mcmc = 
tst_gpr = 
pum_gpr = 
uim_gpr = 
[x-arm-sus-cal-lines]
uim = 15.6
pum = 16.4
tst = 17.6
[y-arm-pcal-cal-lines]
sus = 17.1
sensing = 410.3
pcal3 = 1083.7
pcal4 = 7.93
[tdcf-data]
frametype = R
duration = 130
[sensing-tdcf]
kappa_c = CAL-CS_TDEP_KAPPA_C_OUTPUT
f_cc = CAL-CS_TDEP_F_C_OUTPUT
pcal2_unc = CAL-CS_TDEP_PCAL_LINE2_UNCERTAINTY
pcal_arm = Y
[x-arm-tdcf]
kappa_uim = CAL-CS_TDEP_KAPPA_UIM_REAL_OUTPUT
kappa_pum = CAL-CS_TDEP_KAPPA_PUM_REAL_OUTPUT
kappa_tst = CAL-CS_TDEP_KAPPA_TST_REAL_OUTPUT
pcal1_unc = CAL-CS_TDEP_PCAL_LINE1_UNCERTAINTY
uim_unc = CAL-CS_TDEP_SUS_LINE1_UNCERTAINTY
pum_unc = CAL-CS_TDEP_SUS_LINE2_UNCERTAINTY
tst_unc = CAL-CS_TDEP_SUS_LINE3_UNCERTAINTY
pcal_arm = Y
[sample-tdcf]
kappa_c = False
f_cc = False
kappa_uim = False
kappa_pum = False
kappa_tst = False
[hoft-tdcf-data-application]
kappa_c = True
f_cc = True
kappa_uim = True
kappa_pum = True
kappa_tst = True
pcal_sys_err = False
[pcal]
sys_err =
sys_unc =
sample = False'''

        test_unc = pydarm.uncertainty.DARMUncertainty(config)
        
        samples = test_unc.compute_response_uncertainty(
            1239958818, self.frequencies, trials=1, data=self.data)

        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(samples[0][n]) / np.abs(self.known_ratio[n]), 1.0,
                places=6)
            self.assertAlmostEqual(
                np.angle(samples[0][n], deg=True) -
                np.angle(self.known_ratio[n], deg=True), 0.0, places=5)


class TestResponseQuantiles(unittest.TestCase):

    def setUp(self):
        self.response_samples = np.ones((10, 10), dtype='complex128')
        self.response_samples[0:4, :] *= 0.8
        self.response_samples[5:9, :] *= 1.2

    def tearDown(self):
        del self.response_samples

    def test_response_quantiles(self):
        response_mag_quant, response_pha_quant = \
          pydarm.uncertainty.DARMUncertainty.response_quantiles(
              self.response_samples)

        for m in range(3):
            for n in range(len(self.response_samples[0, :])):
                self.assertAlmostEqual(response_mag_quant[m, n], [0.8, 1, 1.2][m])
                self.assertAlmostEqual(response_pha_quant[m, n], 0)


class TestPlotResponseSamples(unittest.TestCase):

    def setUp(self):
        self.response_samples = np.ones((10, 10), dtype='complex128')
        self.freq = np.logspace(0, np.log10(5000.), 10)
        self.RRMag = np.ones((10, 10))
        self.RRPha = np.ones((10, 10))
        self.response_mag_quant, self.response_pha_quant = \
          pydarm.uncertainty.DARMUncertainty.response_quantiles(
              self.response_samples)

    def tearDown(self):
        del self.response_samples
        del self.freq
        del self.RRMag
        del self.RRPha
        del self.response_mag_quant
        del self.response_pha_quant

    def test_plot_response_samples(self):
        pydarm.uncertainty.DARMUncertainty.plot_response_samples(
            self.freq, self.RRMag, self.RRPha, self.response_mag_quant,
            self.response_pha_quant)
