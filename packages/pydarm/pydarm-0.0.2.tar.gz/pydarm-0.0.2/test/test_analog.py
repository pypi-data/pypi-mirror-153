import unittest
import pydarm
import numpy as np


class TestAnalogAAFilterResponse(unittest.TestCase):

    def setUp(self):
        # Pre-computed values
        # This uses the H1 AA response that has a 0.99 gain
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_analog_aa_filter_response = np.array(
            [0.9902583151820756-0.00023625869326662408j,
             0.9902581352102275-0.0006086735508483027j,
             0.990256940678447-0.001568125690903292j,
             0.9902490122026717-0.00403995033942778j,
             0.9901963893790059-0.010407889389582571j,
             0.9898471618373895-0.02680975201205813j,
             0.9875313105265322-0.06899983685404412j,
             0.9722512045409587-0.17657342104176357j,
             0.8745742785659897-0.43547246366239517j,
             0.3390985734013402-0.8563173043598763j])

    def tearDown(self):
        del self.frequencies
        del self.known_analog_aa_filter_response

    def test_analog_aa_filter_response(self):
        """ Test the analog AA filter response """
        pcal = pydarm.pcal.PcalModel('''
[metadata]
[interferometer]
[pcal]
analog_anti_aliasing_file = test/H1aa.mat
''')
        analog_aa_response = pcal.analog_aa_or_ai_filter_response(
            self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(analog_aa_response[n]),
                np.abs(self.known_analog_aa_filter_response[n]))
            self.assertAlmostEqual(
                np.angle(analog_aa_response[n], deg=True),
                np.angle(self.known_analog_aa_filter_response[n], deg=True))


class TestAnalogAIFilterResponse(unittest.TestCase):

    def setUp(self):
        # Pre-computed values
        # This uses the H1 AI response that has a 0.99 gain
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_analog_ai_filter_response = np.array(
            [0.9902583151820756-0.00023625869326662408j,
             0.9902581352102275-0.0006086735508483027j,
             0.990256940678447-0.001568125690903292j,
             0.9902490122026717-0.00403995033942778j,
             0.9901963893790059-0.010407889389582571j,
             0.9898471618373895-0.02680975201205813j,
             0.9875313105265322-0.06899983685404412j,
             0.9722512045409587-0.17657342104176357j,
             0.8745742785659897-0.43547246366239517j,
             0.3390985734013402-0.8563173043598763j])

    def tearDown(self):
        del self.frequencies
        del self.known_analog_ai_filter_response

    def test_analog_aa_filter_response(self):
        """ Test the analog AI filter response """
        A = pydarm.actuation.ActuationModel('''
[metadata]
[interferometer]
[actuation_x_arm]
analog_anti_imaging_file = test/H1aa.mat
''',
                                            measurement='actuation_x_arm')
        analog_ai_response = A.analog_aa_or_ai_filter_response(
            self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(analog_ai_response[n]),
                np.abs(self.known_analog_ai_filter_response[n]))
            self.assertAlmostEqual(
                np.angle(analog_ai_response[n], deg=True),
                np.angle(self.known_analog_ai_filter_response[n], deg=True))


if __name__ == '__main__':
    unittest.main()
