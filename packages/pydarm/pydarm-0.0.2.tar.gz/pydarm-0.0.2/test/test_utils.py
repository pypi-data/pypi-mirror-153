import unittest
import os
import numpy as np
from scipy import signal
from pydarm.utils import (serielZPK, parallelZPK,
                          freqrespZPK, dfreqrespZPK,
                          digital_delay_filter,
                          save_chain_to_hdf5,
                          read_chain_from_hdf5,
                          save_gpr_to_hdf5,
                          read_gpr_from_hdf5)


class TestSerielZPK(unittest.TestCase):

    def setUp(self):
        self.filter1 = signal.ZerosPolesGain(
            -2.0*np.pi*np.array([1.0, 1.0]),
            -2.0*np.pi*np.array([100.0, 100.0]),
            100.0**2/1.0**2)
        self.filter2 = signal.ZerosPolesGain(
            -2.0*np.pi*np.array([2.0, 2.0]),
            -2.0*np.pi*np.array([200.0, 200.0]),
            200.0**2/2.0**2)
        self.filter = signal.ZerosPolesGain(
            -2.0*np.pi*np.array([1.0, 1.0, 2.0, 2.0]),
            -2.0*np.pi*np.array([100.0, 100.0, 200.0, 200.0]),
            (100.0**2*200.0**2/(1.0**2*2.**2)))

    def tearDown(self):
        del self.filter1
        del self.filter2
        del self.filter

    def test_serielZPK(self):
        test_filter = serielZPK(self.filter1, self.filter2)
        self.assertEqual(len(test_filter.zeros), len(self.filter.zeros))
        self.assertEqual(len(test_filter.poles), len(self.filter.poles))
        for n in range(len(self.filter.zeros)):
            self.assertAlmostEqual(test_filter.zeros[n], self.filter.zeros[n])
        for n in range(len(self.filter.poles)):
            self.assertAlmostEqual(test_filter.poles[n], self.filter.poles[n])
        self.assertAlmostEqual(test_filter.gain, self.filter.gain)


class TestParallelZPK(unittest.TestCase):

    def setUp(self):
        self.filter1 = signal.ZerosPolesGain(
            -2.0*np.pi*np.array([1.0, 1.0]),
            -2.0*np.pi*np.array([100.0, 100.0]),
            100.0**2/1.0**2)
        self.filter2 = signal.ZerosPolesGain(
            -2.0*np.pi*np.array([2.0, 2.0]),
            -2.0*np.pi*np.array([200.0, 200.0]),
            200.0**2/2.0**2)
        self.filter = signal.ZerosPolesGain(
            np.array([-944.3717956376961+313.51778225283215j,
                      -944.3717956376961-313.51778225283215j,
                      -7.530778400011287+2.5001095474423356j,
                      -7.530778400011287-2.5001095474423356j]),
            np.array([-1256.6370614359168+5.624423698413676e-05j,
                      -1256.6370614359168-5.624423698413676e-05j,
                      -628.3185344963764+0j,
                      -628.3185269395391+0j]),
            20000.0)

    def tearDown(self):
        del self.filter1
        del self.filter2
        del self.filter

    def test_parallelZPK(self):
        test_filter = parallelZPK(self.filter1, self.filter2)
        self.assertEqual(len(test_filter.zeros), len(self.filter.zeros))
        self.assertEqual(len(test_filter.poles), len(self.filter.poles))
        for n in range(len(self.filter.zeros)):
            self.assertAlmostEqual(np.real(test_filter.zeros[n]),
                                   np.real(self.filter.zeros[n]))
            self.assertAlmostEqual(np.imag(test_filter.zeros[n]),
                                   np.imag(self.filter.zeros[n]))
        for n in range(len(self.filter.poles)):
            self.assertAlmostEqual(np.real(test_filter.poles[n]),
                                   np.real(self.filter.poles[n]), places=3)
            self.assertAlmostEqual(np.imag(test_filter.poles[n]),
                                   np.imag(self.filter.poles[n]), places=3)
        self.assertAlmostEqual(test_filter.gain, self.filter.gain)


class TestFreqrespZPK(unittest.TestCase):

    def setUp(self):
        self.filter = signal.ZerosPolesGain(
            [], -2.0*np.pi*np.array([1, 1]),
            np.prod(2.0*np.pi*np.asarray([1, 1])))
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_response = np.array(
            [0.0-0.5j,
             -0.09664744749943084-0.08833721090114179j,
             -0.021210239147445683-0.0065396429418788145j,
             -0.003385062727101369-0.00039727801004293907j,
             -0.0005144644812257184-2.336805444122701e-05j,
             -7.761259172380499e-05-1.367768387548693e-06j,
             -1.1695660566624151e-05-7.999812866147877e-08j,
             -1.762156044886542e-06-4.678411892855308e-09j,
             -2.654929417882733e-07-2.7359600619251977e-10j,
             -3.999999520000035e-08-1.5999998720000092e-11j])

    def tearDown(self):
        del self.filter
        del self.frequencies
        del self.known_response

    def test_freqrespZPK(self):
        test_response = freqrespZPK(self.filter, 2.0*np.pi*self.frequencies)
        for n in range(len(test_response)):
            self.assertAlmostEqual(np.abs(test_response[n]),
                                   np.abs(self.known_response[n]))
            self.assertAlmostEqual(np.angle(test_response[n], deg=True),
                                   np.angle(self.known_response[n], deg=True))


class TestDfreqrespZPK(unittest.TestCase):

    def setUp(self):
        self.filter = signal.ZerosPolesGain(
            [], np.zeros(4), 1, dt=1.0/2**16)
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_response = np.array(
            [0.9999999264657179-0.00038349518757139556j,
             0.9999995119288227-0.0009879990467211066j,
             0.9999967605125888-0.002545380978905176j,
             0.9999784985222522-0.006557628624898654j,
             0.9998572905048693-0.01689374512241721j,
             0.9990529171554058-0.04351170788734579j,
             0.9937194923983442-0.11189982317938384j,
             0.9585599169648092-0.2848910065067314j,
             0.7355794304443074-0.6774384854045631j,
             -0.3397768844068262-0.9405060705932685j])

    def tearDown(self):
        del self.filter
        del self.frequencies
        del self.known_response

    def test_dfreqrespZPK(self):
        test_response = dfreqrespZPK(self.filter,
                                     2.0*np.pi*self.frequencies/2**16)[1]
        for n in range(len(test_response)):
            self.assertAlmostEqual(np.abs(test_response[n]),
                                   np.abs(self.known_response[n]))
            self.assertAlmostEqual(np.angle(test_response[n], deg=True),
                                   np.angle(self.known_response[n], deg=True))


class TestDigitalDelayFilter(unittest.TestCase):

    def setUp(self):
        self.delay_cycles = 4
        self.filter = signal.ZerosPolesGain(
            [], np.zeros(self.delay_cycles), 1, dt=1.0/2**16)

    def tearDown(self):
        del self.delay_cycles
        del self.filter

    def test_digial_delay_filter(self):
        test_filter = digital_delay_filter(self.delay_cycles, 2**16)
        self.assertEqual(len(test_filter.zeros), len(self.filter.zeros))
        self.assertEqual(len(test_filter.poles), len(self.filter.poles))
        for n in range(len(test_filter.poles)):
            self.assertAlmostEqual(test_filter.poles[n], self.filter.poles[n])


class TestSaveChainToHdf5(unittest.TestCase):

    def setUp(self):
        self.filename = 'test.h5'
        self.model_string = 'test'
        self.fmin = 20
        self.fmax = 5000
        self.measurement = 'sensing'
        self.chain = np.arange(10)

    def tearDown(self):
        del self.filename
        del self.model_string
        del self.fmin
        del self.fmax
        del self.measurement
        del self.chain

    def test_save_chain_to_hdf5(self):
        save_chain_to_hdf5(
            self.filename, self.model_string, self.fmin, self.fmax,
            self.measurement, self.chain)

        assert os.path.exists(self.filename)


class TestReadChainFromHdf5(unittest.TestCase):

    def setUp(self):
        self.filename = 'test.h5'
        self.model_string = 'test'
        self.fmin = 20
        self.fmax = 5000
        self.measurement = 'sensing'
        self.chain = np.arange(10)

    def tearDown(self):
        del self.filename
        del self.model_string
        del self.fmin
        del self.fmax
        del self.measurement
        del self.chain

    def test_save_chain_to_hdf5(self):
        save_chain_to_hdf5(
            self.filename, self.model_string, self.fmin, self.fmax,
            self.measurement, self.chain)

        test = read_chain_from_hdf5(self.filename)

        assert test[0] == self.model_string
        assert test[1] == self.fmin
        assert test[2] == self.fmax
        assert test[3] == self.measurement
        assert np.allclose(test[4], self.chain)


class TestSaveGPRToHDF5(unittest.TestCase):

    def setUp(self):
        self.filename = 'test_GPR.h5'
        self.meas_model = 'test'
        self.measurement = 'sensing'
        self.known_y_pred = np.array(
             [1.1275231 -0.14775j, 1.11947795-0.1391194j])
        self.known_cov = np.array(
             [[ 1.20202662e-03, 1.11412775e-03, 1.06308187e-03, 1.01441776e-03,
                9.46456817e-04, 9.01659923e-04, 8.68963687e-04, 8.27314896e-04,
                7.66540580e-04, 7.29937311e-04, 6.03345479e-04, 5.34071642e-04,
                4.88979305e-04, 4.51309020e-04, 2.66398796e-04, 2.33383085e-04,
                2.07102041e-04, 1.89673520e-04, 1.43273106e-04, 4.98941061e-05,
                1.10710651e-05, -5.57882617e-05, -8.43420325e-05, -9.91110312e-05,
               -1.02160096e-04, -9.56746538e-05, -8.18911186e-05, -6.66049353e-05,
               -5.83790161e-05, -4.12302913e-05, -2.70112688e-05, -8.50187956e-06,
                3.36873466e-06, 2.33652634e-05, 3.84648854e-05, 5.48991959e-05,
                5.52764965e-05, 5.13437276e-05, 5.04097799e-05, 4.82236629e-05,
                4.76158458e-05, 1.78903912e-05, -2.83320392e-05, -6.83616761e-05],
              [ 1.11412775e-03, 1.03573118e-03, 9.90122350e-04, 9.46583654e-04,
                8.85681902e-04, 8.45472537e-04, 8.16090363e-04, 7.78619630e-04,
                7.23850749e-04, 6.90809621e-04, 5.76190547e-04, 5.13215977e-04,
                4.72115876e-04, 4.37709440e-04, 2.67681956e-04, 2.37077016e-04,
                2.12647158e-04, 1.96409834e-04, 1.53020146e-04, 6.47648751e-05,
                2.75239570e-05, -3.81327643e-05, -6.76286278e-05, -8.44823971e-05,
               -9.04436045e-05, -8.73904016e-05, -7.72683371e-05, -6.49851674e-05,
               -5.81547009e-05, -4.35844053e-05, -3.12326276e-05, -1.48324160e-05,
               -4.12176291e-06, 1.43260424e-05, 2.87599399e-05, 4.63037980e-05,
                4.77436656e-05, 4.58545026e-05, 4.52409985e-05, 4.37349213e-05,
                4.33033826e-05, 1.99378176e-05, -1.90976763e-05, -5.40446567e-05]])
        self.known_frequencies = np.array([10, 20])

    def tearDown(self):
        del self.filename
        del self.meas_model 
        del self.measurement
        del self.known_y_pred
        del self.known_cov
        del self.known_frequencies

    def test_save_gpr_to_hdf5(self):
        save_gpr_to_hdf5(self.filename,
                         self.meas_model,
                         self.measurement,
                         self.known_y_pred,
                         self.known_cov,
                         self.known_frequencies)

        assert os.path.exists(self.filename)


class TestReadGPRFromHDF5(unittest.TestCase):

    def setUp(self):
        self.filename = 'test_GPR.h5'
        self.meas_model = 'test'
        self.measurement = 'sensing'
        self.known_y_pred = np.array(
             [1.1275231 -0.14775j, 1.11947795-0.1391194j])
        self.known_cov = np.array(
             [[ 1.20202662e-03, 1.11412775e-03, 1.06308187e-03, 1.01441776e-03,
                9.46456817e-04, 9.01659923e-04, 8.68963687e-04, 8.27314896e-04,
                7.66540580e-04, 7.29937311e-04, 6.03345479e-04, 5.34071642e-04,
                4.88979305e-04, 4.51309020e-04, 2.66398796e-04, 2.33383085e-04,
                2.07102041e-04, 1.89673520e-04, 1.43273106e-04, 4.98941061e-05,
                1.10710651e-05, -5.57882617e-05, -8.43420325e-05, -9.91110312e-05,
               -1.02160096e-04, -9.56746538e-05, -8.18911186e-05, -6.66049353e-05,
               -5.83790161e-05, -4.12302913e-05, -2.70112688e-05, -8.50187956e-06,
                3.36873466e-06, 2.33652634e-05, 3.84648854e-05, 5.48991959e-05,
                5.52764965e-05, 5.13437276e-05, 5.04097799e-05, 4.82236629e-05,
                4.76158458e-05, 1.78903912e-05, -2.83320392e-05, -6.83616761e-05],
              [ 1.11412775e-03, 1.03573118e-03, 9.90122350e-04, 9.46583654e-04,
                8.85681902e-04, 8.45472537e-04, 8.16090363e-04, 7.78619630e-04,
                7.23850749e-04, 6.90809621e-04, 5.76190547e-04, 5.13215977e-04,
                4.72115876e-04, 4.37709440e-04, 2.67681956e-04, 2.37077016e-04,
                2.12647158e-04, 1.96409834e-04, 1.53020146e-04, 6.47648751e-05,
                2.75239570e-05, -3.81327643e-05, -6.76286278e-05, -8.44823971e-05,
               -9.04436045e-05, -8.73904016e-05, -7.72683371e-05, -6.49851674e-05,
               -5.81547009e-05, -4.35844053e-05, -3.12326276e-05, -1.48324160e-05,
               -4.12176291e-06, 1.43260424e-05, 2.87599399e-05, 4.63037980e-05,
                4.77436656e-05, 4.58545026e-05, 4.52409985e-05, 4.37349213e-05,
                4.33033826e-05, 1.99378176e-05, -1.90976763e-05, -5.40446567e-05]])
        self.known_frequencies = np.array([10, 20])

    def tearDown(self):
        del self.filename
        del self.meas_model
        del self.measurement
        del self.known_y_pred
        del self.known_cov
        del self.known_frequencies

    def test_read_gpr_from_hdf5(self):
        save_gpr_to_hdf5(self.filename,
                         self.meas_model,
                         self.measurement,
                         self.known_y_pred,
                         self.known_cov,
                         self.known_frequencies)

        test = read_gpr_from_hdf5(self.filename, self.measurement)

        self.assertTrue(test[0] == self.meas_model)
        for n in range(len(test[1])):
            self.assertAlmostEqual(
                np.abs(test[1][n])/np.abs(self.known_y_pred[n]), 1.0, places=4)
            self.assertAlmostEqual(np.angle(test[1][n], deg=True) -
                np.angle(self.known_y_pred[n], deg=True), 0.0, places=4)
        for n in range(len(test[2])):
            self.assertTrue(np.allclose(test[2][n], self.known_cov[n]))
        self.assertTrue(np.allclose(test[3], self.known_frequencies))


if __name__ == '__main__':
    unittest.main()
