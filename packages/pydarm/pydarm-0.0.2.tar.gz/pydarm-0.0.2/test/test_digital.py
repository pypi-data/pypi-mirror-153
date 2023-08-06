import unittest
import pydarm
import numpy as np


class TestDigitalAAFilterResponse(unittest.TestCase):

    def setUp(self):
        # Pre-computed values
        # anti_aliasing_rate_string = 16k
        # anti_aliasing_method      = biquad
        # frequencies = np.logspace(0, np.log10(5000.), 10)
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_digital_aa_filter_response = np.array(
            [1.0000006743118521-0.00026859554703262606j,
             1.0000005577918698-0.0006919831728579482j,
             0.9999997844069123-0.0017827587938075234j,
             0.9999946510415249-0.004592951080196375j,
             0.9999605723740017-0.011833290098468159j,
             0.9997340799606691-0.03049404992719877j,
             0.9982174966256611-0.07869700811767119j,
             0.9875624565339749-0.20500805282580065j,
             0.8902071582110597-0.5598509390584541j,
             -0.3367135303069774-1.013081908852281j])

    def tearDown(self):
        del self.frequencies
        del self.known_digital_aa_filter_response

    def test_digital_aa_filter_response(self):
        """ Test the digital AA filter response """
        C = pydarm.sensing.SensingModel('''
[metadata]
[interferometer]
[sensing]
anti_aliasing_rate_string = 16k
anti_aliasing_method = biquad
''')
        digital_aa_filter_response = C.digital_aa_or_ai_filter_response(
            self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(digital_aa_filter_response[n]),
                np.abs(self.known_digital_aa_filter_response[n]))
            self.assertAlmostEqual(
                np.angle(digital_aa_filter_response[n], deg=True),
                np.angle(self.known_digital_aa_filter_response[n], deg=True))


class TestDigitalAIFilterResponse(unittest.TestCase):

    def setUp(self):
        # Pre-computed values
        # anti_imaging_rate_string = 16k
        # anti_imaging_method      = biquad
        # frequencies = np.logspace(0, np.log10(5000.), 10)
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_digital_ai_filter_response = np.array(
            [1.0000006743118521-0.00026859554703262606j,
             1.0000005577918698-0.0006919831728579482j,
             0.9999997844069123-0.0017827587938075234j,
             0.9999946510415249-0.004592951080196375j,
             0.9999605723740017-0.011833290098468159j,
             0.9997340799606691-0.03049404992719877j,
             0.9982174966256611-0.07869700811767119j,
             0.9875624565339749-0.20500805282580065j,
             0.8902071582110597-0.5598509390584541j,
             -0.3367135303069774-1.013081908852281j])

    def tearDown(self):
        del self.frequencies
        del self.known_digital_ai_filter_response

    def test_digital_ai_filter_response(self):
        """ Test the digital AI filter response """
        A = pydarm.actuation.ActuationModel('''
[metadata]
[interferometer]
[actuation_x_arm]
anti_imaging_rate_string = 16k
anti_imaging_method = biquad
''',
                                            measurement='actuation_x_arm')
        digital_ai_filter_response = A.digital_aa_or_ai_filter_response(
            self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(digital_ai_filter_response[n]),
                np.abs(self.known_digital_ai_filter_response[n]))
            self.assertAlmostEqual(
                np.angle(digital_ai_filter_response[n], deg=True),
                np.angle(self.known_digital_ai_filter_response[n], deg=True))


if __name__ == '__main__':
    unittest.main()
