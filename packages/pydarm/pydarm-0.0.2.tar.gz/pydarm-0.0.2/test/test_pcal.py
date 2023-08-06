import unittest
import pydarm
import numpy as np


class TestPcalDewhitenResponse(unittest.TestCase):

    def setUp(self):
        # Pre-computed values
        # frequencies = np.logspace(0, np.log10(5000.), 10)
        # pcal_dewhiten = 1.0, 1.0
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_pcal_dewhiten_response = np.array(
            [0-0.5j,
             -0.09664744749943081-0.08833721090114179j,
             -0.021210239147445686-0.0065396429418788145j,
             -0.00338506272710137-0.00039727801004293923j,
             -0.0005144644812257184-2.3368054441227016e-05j,
             -7.7612591723805e-05-1.3677683875486927e-06j,
             -1.169566056662415e-05-7.999812866147876e-08j,
             -1.7621560448865418e-06-4.678411892855308e-09j,
             -2.654929417882733e-07-2.7359600619251967e-10j,
             -3.999999520000034e-08-1.5999998720000092e-11j])

    def tearDown(self):
        del self.frequencies
        del self.known_pcal_dewhiten_response

    def test_pcal_dewhiten_response(self):
        """ Test the dewhitening filter response """
        pcal = pydarm.pcal.PcalModel('''
[metadata]
[interferometer]
[pcal]
pcal_dewhiten = 1.0, 1.0
''')
        dewhitening_response = pcal.pcal_dewhiten_response(self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(dewhitening_response[n]),
                np.abs(self.known_pcal_dewhiten_response[n]))
            self.assertAlmostEqual(
                np.angle(dewhitening_response[n], deg=True),
                np.angle(self.known_pcal_dewhiten_response[n], deg=True))


class TestComputePcalCorrection(unittest.TestCase):

    def setUp(self):
        # Pre-computed values
        # frequencies = np.logspace(0, np.log10(5000.), 10)
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_pcal_correction = np.array(
            [-0.00025358893371024303+0.49999958238994285j,
             0.09653186519726428+0.08846335096661345j,
             0.021188078968294916+0.0066109980202688125j,
             0.003381476169995326+0.0004266184275991344j,
             0.000513802030855575+3.485552121587564e-05j,
             7.739366982337172e-05+5.8303787826440386e-06j,
             1.1543776066542702e-05+1.806974404649834e-06j,
             1.6213496404216842e-06+6.607708336536615e-07j,
             1.329595567674792e-07+2.1863432594589902e-07j,
             -4.0222497230234286e-08+2.2455753017906737e-09j])

    def tearDown(self):
        del self.frequencies
        del self.known_pcal_correction

    def test_compute_pcal_correction(self):
        """ Test the Pcal correction """
        pcal = pydarm.pcal.PcalModel('''
[metadata]
[interferometer]
[pcal]
pcal_dewhiten = 1.0, 1.0
ref_pcal_2_darm_act_sign = -1
analog_anti_aliasing_file = test/H1aa.mat
anti_aliasing_rate_string = 16k
anti_aliasing_method = biquad
''')
        pcal_correction = pcal.compute_pcal_correction(self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(pcal_correction[n]),
                np.abs(self.known_pcal_correction[n]))
            self.assertAlmostEqual(
                np.angle(pcal_correction[n], deg=True),
                np.angle(self.known_pcal_correction[n], deg=True))

class TestDigitalFilterResponse(unittest.TestCase):

    def setUp(self):
        # Pre-computed values
        # frequencies = np.logspace(0, np.log10(5000.), 10)
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_digital_filter_response = np.array(
            [0.003032834984214-0.000852215454730j,
             0.000583953846217-0.000533208471501j,
             0.000630611562557-0.000194421040491j,
             0.000637732123677-0.000074841527594j,
             0.000638802551708-0.000029013638555j,
             0.000638963766980-0.000011258145407j,
             0.000638988054812-0.000004365874356j,
             0.000638991714044-0.000001684584793j,
             0.000638992265247-0.000000627782359j,
             0.000638992347469-0.000000172013907j])

    def tearDown(self):
        del self.frequencies
        del self.known_digital_filter_response

    def test_digital_filter_response(self):
        """ Test the digital filter response """
        pcal = pydarm.pcal.PcalModel('''
[metadata]
[interferometer]
[pcal]
pcal_filter_file           = test/H1CALEY_1123041152.txt
pcal_filter_bank           = PCALY_TX_PD
pcal_filter_modules_in_use = 6,8
pcal_filter_gain           = 1.0
''')
        digital_filter = pcal.digital_filter_response(self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(digital_filter[n]),
                np.abs(self.known_digital_filter_response[n]))
            self.assertAlmostEqual(
                np.angle(digital_filter[n], deg=True),
                np.angle(self.known_digital_filter_response[n], deg=True), places=6)

if __name__ == '__main__':
    unittest.main()
