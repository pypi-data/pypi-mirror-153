import unittest
import pydarm
import numpy as np


class TestAnalogDriverResponse(unittest.TestCase):

    def setUp(self):
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_response = {
            'UIM': {
                'UL': np.ones(len(self.frequencies), dtype='complex128'),
                'LL': np.ones(len(self.frequencies), dtype='complex128'),
                'UR': np.ones(len(self.frequencies), dtype='complex128'),
                'LR': np.ones(len(self.frequencies), dtype='complex128')},
            'PUM': {
                'UL': np.ones(len(self.frequencies), dtype='complex128'),
                'LL': np.ones(len(self.frequencies), dtype='complex128'),
                'UR': np.ones(len(self.frequencies), dtype='complex128'),
                'LR': np.ones(len(self.frequencies), dtype='complex128')},
            'TST': {
                'UL': np.array(
                    [0.9999998948885249-0.0003352715041293239j,
                     0.9999993023409579-0.0008637599652766293j,
                     0.9999953694243224-0.002225297865133263j,
                     0.9999692660865103-0.005732898947830594j,
                     0.9997960415022515-0.014767298626171824j,
                     0.9986476944616459-0.03800441737197289j,
                     0.9910869734117239-0.09722224905346574j,
                     0.9434615871897538-0.23929884983400718j,
                     0.7100118921447782-0.47534426423585624j,
                     0.23350097886085233-0.48059520727971594j]),
                'LL': np.array(
                    [0.9999998916146684-0.00034119500566379466j,
                     0.9999992806113166-0.0008790206699527335j,
                     0.9999952251984726-0.002264613688569092j,
                     0.9999683088528678-0.0058341823535449635j,
                     0.999789689822471-0.01502813255515821j,
                     0.9986056151986867-0.03867465221930742j,
                     0.990811116442425-0.09891939009102466j,
                     0.9417711330516-0.2432045844267566j,
                     0.7028366049212413-0.48037909581270577j,
                     0.22293976812324173-0.47855091024022334j]),
                'UR': np.ones(len(self.frequencies), dtype='complex128'),
                'LR': np.ones(len(self.frequencies), dtype='complex128')}}

    def tearDown(self):
        del self.frequencies
        del self.known_response

    def test_analog_driver_response(self):
        A = pydarm.actuation.ActuationModel('''
[metadata]
[interferometer]
[actuation_x_arm]
tst_driver_meas_Z_UL = 129.7e3
tst_driver_meas_Z_LL = 90.74e3
tst_driver_meas_Z_UR =
tst_driver_meas_Z_LR =
tst_driver_meas_P_UL = 3.213e3, 31.5e3
tst_driver_meas_P_LL = 3.177e3, 26.7e3
tst_driver_meas_P_UR =
tst_driver_meas_P_LR =
''',
                                            measurement='actuation_x_arm')

        test_response = A.analog_driver_response(self.frequencies)
        for i, stage in enumerate(test_response.keys()):
            for j, quadrant in enumerate(test_response[stage].keys()):
                for k, val in enumerate(test_response[stage][quadrant]):
                    self.assertAlmostEqual(
                        np.abs(val),
                        np.abs(self.known_response[stage][quadrant][k]))
                    self.assertAlmostEqual(
                        np.angle(val, deg=True),
                        np.angle(self.known_response[stage][quadrant][k], deg=True))


class TestUIMDCGainApct(unittest.TestCase):

    def setUp(self):
        # uim_driver_DC_trans_ApV = 6.1535e-4
        # dac_gain = 7.62939453125e-05
        self.known_uim_dc_gain = 4.694747924804687e-08

    def tearDown(self):
        del self.known_uim_dc_gain

    def test_uim_dc_gain_Apct(self):
        """ Test the UIM DC gain A / ct """
        A = pydarm.actuation.ActuationModel('''
[metadata]
[interferometer]
[actuation_x_arm]
uim_driver_DC_trans_ApV = 6.1535e-4
dac_gain = 7.62939453125e-05
''',
                                            measurement='actuation_x_arm')
        uim_gain = A.uim_dc_gain_Apct()
        self.assertAlmostEqual(uim_gain, self.known_uim_dc_gain)


class TestPUMDCGainApct(unittest.TestCase):

    def setUp(self):
        # pum_driver_DC_trans_ApV = 2.6847e-4
        # dac_gain = 7.62939453125e-05
        # pum_coil_outf_signflip = -1
        self.known_pum_dc_gain = -2.0482635498046874e-08

    def tearDown(self):
        del self.known_pum_dc_gain

    def test_pum_dc_gain_Apct(self):
        """ Test the PUM DC gain A / ct """
        A = pydarm.actuation.ActuationModel('''
[metadata]
[interferometer]
[actuation_x_arm]
pum_driver_DC_trans_ApV = 2.6847e-4
dac_gain = 7.62939453125e-05
pum_coil_outf_signflip = -1
''',
                                            measurement='actuation_x_arm')
        pum_gain = A.pum_dc_gain_Apct()
        self.assertAlmostEqual(pum_gain, self.known_pum_dc_gain)


class TestTSTDCGainV2pct(unittest.TestCase):

    def setUp(self):
        # tst_driver_DC_gain_VpV_HV = 40
        # tst_driver_DC_gain_VpV_LV = 1.881
        # dac_gain = 7.62939453125e-05
        # actuation_esd_bias_voltage = -9.3
        self.known_tst_dc_gain = -0.10677062988281251

    def tearDown(self):
        del self.known_tst_dc_gain

    def test_tst_dc_gain_Apct(self):
        """ Test the TST DC gain V**2 / ct """
        A = pydarm.actuation.ActuationModel('''
[metadata]
[interferometer]
[actuation_x_arm]
tst_driver_DC_gain_VpV_HV = 40
tst_driver_DC_gain_VpV_LV = 1.881
actuation_esd_bias_voltage = -9.3
dac_gain = 7.62939453125e-05
''',
                                            measurement='actuation_x_arm')
        tst_gain = A.tst_dc_gain_V2pct()
        self.assertAlmostEqual(tst_gain, self.known_tst_dc_gain)


class TestUIMDCGainNpct(unittest.TestCase):

    def setUp(self):
        # uim_driver_DC_trans_ApV = 6.1535e-4
        # dac_gain = 7.62939453125e-05
        # uim_NpA       = 1.634
        self.known_uim_dc_gain = 7.671218109130858e-08

    def tearDown(self):
        del self.known_uim_dc_gain

    def test_uim_dc_gain_Apct(self):
        """ Test the UIM DC gain N / ct """
        A = pydarm.actuation.ActuationModel('''
[metadata]
[interferometer]
[actuation_x_arm]
uim_driver_DC_trans_ApV = 6.1535e-4
dac_gain = 7.62939453125e-05
uim_NpA = 1.634
''',
                                            measurement='actuation_x_arm')
        uim_gain = A.uim_dc_gain_Npct()
        self.assertAlmostEqual(uim_gain, self.known_uim_dc_gain)


class TestPUMDCGainNpct(unittest.TestCase):

    def setUp(self):
        # pum_driver_DC_trans_ApV = 2.6847e-4
        # dac_gain = 7.62939453125e-05
        # pum_coil_outf_signflip = -1
        # pum_NpA       = 0.02947
        self.known_pum_dc_gain = -6.036232681274414e-10

    def tearDown(self):
        del self.known_pum_dc_gain

    def test_pum_dc_gain_Npct(self):
        """ Test the PUM DC gain N / ct """
        A = pydarm.actuation.ActuationModel('''
[metadata]
[interferometer]
[actuation_x_arm]
pum_driver_DC_trans_ApV = 2.6847e-4
dac_gain = 7.62939453125e-05
pum_NpA = 0.02947
pum_coil_outf_signflip = -1
''',
                                            measurement='actuation_x_arm')
        pum_gain = A.pum_dc_gain_Npct()
        self.assertAlmostEqual(pum_gain, self.known_pum_dc_gain)


class TestTSTDCGainNpct(unittest.TestCase):

    def setUp(self):
        # tst_driver_DC_gain_VpV_HV = 40
        # tst_driver_DC_gain_VpV_LV = 1.881
        # dac_gain = 7.62939453125e-05
        # actuation_esd_bias_voltage = -9.3
        # tst_NpV2    = 4.427e-11
        self.known_tst_dc_gain = -4.72673578491211e-12

    def tearDown(self):
        del self.known_tst_dc_gain

    def test_tst_dc_gain_Npct(self):
        """ Test the TST DC gain N / ct """
        A = pydarm.actuation.ActuationModel('''
[metadata]
[interferometer]
[actuation_x_arm]
tst_driver_DC_gain_VpV_HV = 40
tst_driver_DC_gain_VpV_LV = 1.881
actuation_esd_bias_voltage = -9.3
dac_gain = 7.62939453125e-05
tst_NpV2 = 4.427e-11
''',
                                            measurement='actuation_x_arm')
        tst_gain = A.tst_dc_gain_Npct()
        self.assertAlmostEqual(tst_gain, self.known_tst_dc_gain)


class TestSUSDigitalFiltersResponse(unittest.TestCase):

    def setUp(self):
        # Pre-defined values
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.TST_digital_filter_response = np.array(
            [-0.03129874344172154+0.30517065377704694j,
             2.4260093192870076+0.5395598117548245j,
             4.746279555953268-14.440418228455206j,
             -10.900389910048899-21.609152361943185j,
             -31.403510154862442-18.172294970461078j,
             -39.725084402162665-5.666968424942829j,
             -36.05682088340858+2.638797989766907j,
             -35.07010453075894+7.434176388352742j,
             -22.901848297541846+31.97868922991029j,
             -25.240115692074934-28.531649366848185j])
        self.PUM_digital_filter_response = np.array(
            [-0.15850099452070285+0.12925881299779612j,
             -2.9964600482668753+0.30212842737343387j,
             -30.56202717042201+13.53346379254984j,
             -117.79715294911026+133.5495986262722j,
             65.71236422447501+691.9714772832681j,
             2010.62556364388+287.8260317781964j,
             -445.7019123170684-210.3550825010501j,
             66.70979808782154-184.31083381342648j,
             -92.35598766208558-56.12007069513851j,
             -3.187299362497145-11.170597438197754j])
        self.UIM_digital_filter_response = np.array(
            [0.0007693760416669129+0.0021754411075238186j,
             -0.015583440206531879-0.014783007553054835j,
             -0.4609157605911597-0.7647563380084396j,
             -17.58562534776213-2.6979597757334934j,
             -15.023972869782675+61.1697093779249j,
             84.18892695637918+136.61857120681844j,
             175.86077619832767-194.04205619047102j,
             22.11561257101802-78.64207839731334j,
             -30.972277953914173-3.640637204710241j,
             -1.168041821378937-2.944313819270134j])

    def tearDown(self):
        del self.frequencies
        del self.TST_digital_filter_response
        del self.PUM_digital_filter_response
        del self.UIM_digital_filter_response

    def test_sus_digital_filters_response(self):
        A = pydarm.actuation.ActuationModel('''
[metadata]
[interferometer]
[actuation_x_arm]
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
''',
                                            measurement='actuation_x_arm')
        [uim, pum, tst] = A.sus_digital_filters_response(self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(np.abs(uim[n]),
                                   np.abs(self.UIM_digital_filter_response[n]))
            self.assertAlmostEqual(
                np.angle(uim[n], deg=True),
                np.angle(self.UIM_digital_filter_response[n], deg=True))
            self.assertAlmostEqual(np.abs(pum[n]),
                                   np.abs(self.PUM_digital_filter_response[n]))
            self.assertAlmostEqual(
                np.angle(pum[n], deg=True),
                np.angle(self.PUM_digital_filter_response[n], deg=True))
            self.assertAlmostEqual(np.abs(tst[n]),
                                   np.abs(self.TST_digital_filter_response[n]))
            self.assertAlmostEqual(
                np.angle(tst[n], deg=True),
                np.angle(self.TST_digital_filter_response[n], deg=True))


class TestSUSDigitalCompensationResponse(unittest.TestCase):

    def setUp(self):
        # Pre-defined values
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_digital_response = {
            'UIM': {
                'UL': np.ones(len(self.frequencies), dtype='complex128'),
                'LL': np.ones(len(self.frequencies), dtype='complex128'),
                'UR': np.ones(len(self.frequencies), dtype='complex128'),
                'LR': np.ones(len(self.frequencies), dtype='complex128')},
            'PUM': {
                'UL': np.ones(len(self.frequencies), dtype='complex128'),
                'LL': np.ones(len(self.frequencies), dtype='complex128'),
                'UR': np.ones(len(self.frequencies), dtype='complex128'),
                'LR': np.ones(len(self.frequencies), dtype='complex128')},
            'TST': {
                'UL': np.ones(len(self.frequencies), dtype='complex128'),
                'LL': np.ones(len(self.frequencies), dtype='complex128'),
                'UR': np.ones(len(self.frequencies), dtype='complex128'),
                'LR': np.ones(len(self.frequencies), dtype='complex128')}}

    def tearDown(self):
        del self.frequencies
        del self.known_digital_response

    def test_sus_digital_filters_response(self):
        A = pydarm.actuation.ActuationModel('''
[metadata]
[interferometer]
[actuation_x_arm]
sus_filter_file = test/H1SUSETMX_1236641144.txt
tst_compensation_filter_bank_UL =
tst_compensation_filter_modules_in_use_UL =
tst_compensation_filter_gain_UL =
''',
                                            measurement='actuation_x_arm')

        test_response = A.sus_digital_compensation_response(self.frequencies)
        for i, stage in enumerate(test_response.keys()):
            for j, quadrant in enumerate(test_response[stage].keys()):
                for k, val in enumerate(test_response[stage][quadrant]):
                    self.assertAlmostEqual(
                        np.abs(val),
                        np.abs(self.known_digital_response[stage][quadrant][k]))
                    self.assertAlmostEqual(
                        np.angle(val, deg=True),
                        np.angle(self.known_digital_response[stage][quadrant][k], deg=True))


class TestCombineSusQuadrants(unittest.TestCase):

    def setUp(self):
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_response_uim = np.ones(10, dtype='complex128')
        self.known_response_pum = np.ones(10, dtype='complex128')
        self.known_response_tst = np.array(
            [0.9999999466257983-0.00016911662744827964j,
             0.9999996457380687-0.0004356951588073407j,
             0.9999976486556987-0.0011224778884255887j,
             0.9999843937348445-0.002891770325343889j,
             0.9998964328311806-0.007448857795332509j,
             0.9993133274150832-0.01916976739782008j,
             0.9954745224635373-0.0490354097861226j,
             0.9713081800603385-0.12062585856519095j,
             0.853212124266505-0.2389308400121405j,
             0.6141101867460235-0.23978652937998482j])

    def tearDown(self):
        del self.frequencies
        del self.known_response_uim
        del self.known_response_pum
        del self.known_response_tst

    def test_combine_sus_quadrants(self):
        A = pydarm.actuation.ActuationModel('''
[metadata]
[interferometer]
[actuation_x_arm]
tst_driver_meas_Z_UL = 129.7e3
tst_driver_meas_Z_LL = 90.74e3
tst_driver_meas_Z_UR =
tst_driver_meas_Z_LR =
tst_driver_meas_P_UL = 3.213e3, 31.5e3
tst_driver_meas_P_LL = 3.177e3, 26.7e3
tst_driver_meas_P_UR =
tst_driver_meas_P_LR =
''',
                                            measurement='actuation_x_arm')

        uim, pum, tst = A.combine_sus_quadrants(self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(uim[n]),
                np.abs(self.known_response_uim[n]))
            self.assertAlmostEqual(
                np.angle(uim[n], deg=True),
                np.angle(self.known_response_uim[n], deg=True))
            self.assertAlmostEqual(
                np.abs(pum[n]),
                np.abs(self.known_response_pum[n]))
            self.assertAlmostEqual(
                np.angle(pum[n], deg=True),
                np.angle(self.known_response_pum[n], deg=True))
            self.assertAlmostEqual(
                np.abs(tst[n]),
                np.abs(self.known_response_tst[n]))
            self.assertAlmostEqual(
                np.angle(tst[n], deg=True),
                np.angle(self.known_response_tst[n], deg=True))


class TestMatlabForce2LengthResponse(unittest.TestCase):

    def setUp(self):
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.TST_known_F2L_response = np.array(
            [-0.00041148596021480487-0.0015143517370263232j,
             -0.00010354107678528522-1.1765319216695903e-07j,
             -1.4644930853742117e-05-3.5466075041766223e-09j,
             -2.188160606001966e-06-2.0395742130086124e-10j,
             -3.292677675426089e-07-1.1898037360168971e-11j,
             -4.9599253544478063e-08-6.955427397606517e-13j,
             -7.47255300169034e-09-4.067318835723566e-14j,
             -1.1258397964013227e-09-2.378592628361941e-15j,
             -1.6961994305038427e-10-1.390972048985424e-16j,
             -2.5555839369830415e-11-8.134681297265418e-18j])
        self.PUM_known_F2L_response = np.array(
            [-0.0009424811357710207+0.0019062104335214956j,
             1.0293251164397253e-05+7.073109949162567e-07j,
             1.4774003935897678e-07+7.750438534956482e-11j,
             3.1997187919682874e-09+6.030048116065241e-13j,
             7.28815782626994e-11+5.275371501679252e-15j,
             1.771401646942218e-12+4.970091549924512e-17j,
             6.80485101377138e-14+7.4184509850763135e-19j,
             -3.939882987588383e-15-1.656518616222811e-20j,
             -2.4980183082476873e-15-3.735923277186558e-21j,
             9.851007172567447e-18+6.41299576873862e-24j])
        self.UIM_known_F2L_response = np.array(
            [-0.0004539112097792617+0.0016706807311863258j,
             -3.270608446356798e-06-2.0483033482849557e-06j,
             -1.0732718463641292e-08+9.358318080529727e-13j,
             -3.040012769594837e-11+1.284586711941435e-14j,
             -1.142690304598126e-13+2.062418770178432e-16j,
             6.853638405500286e-16+1.2429532362755387e-16j,
             3.1125363563944354e-17-8.449710365518706e-19j,
             9.159264149563957e-22+1.3178814099168241e-23j,
             -2.6561794705370495e-25-7.338344152095596e-27j,
             -1.1726221364201392e-30-2.4464769898562298e-30j])

    def tearDown(self):
        del self.frequencies
        del self.TST_known_F2L_response
        del self.PUM_known_F2L_response
        del self.UIM_known_F2L_response

    def test_matlab_force2length_response(self):
        A = pydarm.actuation.ActuationModel('''
[metadata]
[interferometer]
[actuation_x_arm]
''',
                                            measurement='actuation_x_arm')
        [uim, pum, tst] = A.matlab_force2length_response(
            'test/H1susdata_O3.mat', self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(np.abs(uim[n]),
                                   np.abs(self.UIM_known_F2L_response[n]))
            self.assertAlmostEqual(
                np.angle(uim[n], deg=True),
                np.angle(self.UIM_known_F2L_response[n], deg=True))
            self.assertAlmostEqual(np.abs(pum[n]),
                                   np.abs(self.PUM_known_F2L_response[n]))
            self.assertAlmostEqual(
                np.angle(pum[n], deg=True),
                np.angle(self.PUM_known_F2L_response[n], deg=True))
            self.assertAlmostEqual(np.abs(tst[n]),
                                   np.abs(self.TST_known_F2L_response[n]))
            self.assertAlmostEqual(
                np.angle(tst[n], deg=True),
                np.angle(self.TST_known_F2L_response[n], deg=True))


class TestDigitalOutToDisplacement(unittest.TestCase):

    def setUp(self):
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.TST_known_tf = np.array(
            [1.9381128366288105e-15+7.084923321696425e-15j,
             4.846416041981388e-16-1.5765449186707969e-18j,
             6.854411598086494e-17-7.585382386850981e-19j,
             1.0237678592541069e-17-2.9738538652980284e-19j,
             1.5367561509460086e-18-1.1550321717363778e-19j,
             2.2772458041669347e-19-4.4586564579385514e-20j,
             3.063100975597829e-20-1.665633663061682e-20j,
             1.472512511979171e-21-4.948808065557348e-21j,
             -6.970960601188869e-22+1.0099474651594038e-22j,
             -3.8963114263552186e-23-5.016546730668483e-23j])
        self.PUM_known_tf = np.array(
            [-5.618021460861343e-13+1.1401945563127125e-12j,
             6.154175662825378e-15+4.010967874186301e-16j,
             8.830745619372059e-17-7.557564507542089e-19j,
             1.9121021132528307e-18-4.4390085030266175e-20j,
             4.3486514554534227e-20-2.6215994978040016e-21j,
             1.0462587696100501e-21-1.6379277822286195e-22j,
             3.749784155222869e-23-1.5864846571311978e-23j,
             -1.2139274103725887e-24+2.0358371914030717e-24j,
             1.3971705879842376e-24+6.693133108398555e-25j,
             2.6080357979757855e-27-5.232778377591158e-27j])
        self.UIM_known_tf = np.array(
            [-3.430763161527003e-11+1.2696021299733796e-10j,
             -2.4899857500856507e-13-1.547223638897765e-13j,
             -8.152763544441236e-16+7.476151512063072e-18j,
             -2.3086963982589343e-18+5.500858196896584e-20j,
             -8.663921746539537e-21+5.386329216110624e-22j,
             5.290544966557914e-23+1.2746440643491213e-24j,
             2.154672382803322e-24-9.81407533663976e-25j,
             3.672997786320173e-29-5.963176342634914e-29j,
             1.863046548604978e-32+9.566192650734058e-33j,
             -2.0460864930999043e-37-3.153188911481507e-39j])

    def tearDown(self):
        del self.frequencies
        del self.TST_known_tf
        del self.PUM_known_tf
        del self.UIM_known_tf

    def test_digital_out_to_displacement(self):
        A = pydarm.actuation.ActuationModel('''
[metadata]
[interferometer]
[actuation_x_arm]
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
''',
                                            measurement='actuation_x_arm')
        [uim_response, pum_response, tst_response] = \
            A.digital_out_to_displacement(self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(np.abs(uim_response[n]),
                                   np.abs(self.UIM_known_tf[n]))
            self.assertAlmostEqual(
                np.angle(uim_response[n], deg=True),
                np.angle(self.UIM_known_tf[n], deg=True))
            self.assertAlmostEqual(np.abs(pum_response[n]),
                                   np.abs(self.PUM_known_tf[n]))
            self.assertAlmostEqual(
                np.angle(pum_response[n], deg=True),
                np.angle(self.PUM_known_tf[n], deg=True))
            self.assertAlmostEqual(np.abs(tst_response[n]),
                                   np.abs(self.TST_known_tf[n]))
            self.assertAlmostEqual(
                np.angle(tst_response[n], deg=True),
                np.angle(self.TST_known_tf[n], deg=True))


class TestDrivealignToDisplacement(unittest.TestCase):

    def setUp(self):
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.TST_known_tf = np.array(
            [-2.222881500981626e-15+3.691011841669097e-16j,
             1.1764193182970055e-15+2.5849635956379406e-16j,
             3.1617534435707367e-16-9.92839053775603e-16j,
             -1.1700305084971196e-16-2.1853458973419276e-16j,
             -5.006230661758991e-17-2.4902470964105e-17j,
             -9.308653195938007e-18+1.9222273202986028e-19j,
             -1.1111368291657706e-18+5.936117452101705e-19j,
             -5.412995749774128e-20+1.7611360028653088e-19j,
             2.4897361921808887e-20-3.511338429355629e-21j,
             1.3890965613664794e-21+1.7923601565333542e-21j])
        self.PUM_known_tf = np.array(
            [-5.636311671296026e-13+1.1503626120207196e-12j,
             6.539680039025585e-15+3.344573000972991e-16j,
             9.436017253315024e-17-3.810611139309467e-17j,
             1.2201453005199638e-18-1.1859853195589023e-18j,
             2.3160192732375865e-21-2.230152515596516e-20j,
             -1.7088823698982324e-22-1.4723824048886304e-22j,
             -3.9895135060052445e-25+2.9092246327605506e-25j,
             1.1353220905153887e-26+8.382906433078052e-27j,
             3.841572759246625e-27-3.1425560227349834e-27j,
             -4.588083981792824e-30-2.906408489212469e-30j])
        self.UIM_known_tf = np.array(
            [-3.430763161527003e-11+1.2696021299733796e-10j,
             -2.4899857500856507e-13-1.547223638897765e-13j,
             -8.152763544441236e-16+7.476151512063072e-18j,
             -2.3086963982589343e-18+5.500858196896584e-20j,
             -8.663921746539537e-21+5.386329216110624e-22j,
             5.290544966557914e-23+1.2746440643491213e-24j,
             2.154672382803322e-24-9.81407533663976e-25j,
             3.672997786320173e-29-5.963176342634914e-29j,
             1.863046548604978e-32+9.566192650734058e-33j,
             -2.0460864930999043e-37-3.153188911481507e-39j])

    def tearDown(self):
        del self.frequencies
        del self.TST_known_tf
        del self.PUM_known_tf
        del self.UIM_known_tf

    def test_drivealign_to_displacement(self):
        A = pydarm.actuation.ActuationModel('''
[metadata]
[interferometer]
[actuation_x_arm]
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
tst_drive_align_bank = ETMX_L3_DRIVEALIGN_L2L
tst_drive_align_modules = 4,5
tst_drive_align_gain = -35.7
pum_drive_align_bank = ETMX_L2_DRIVEALIGN_L2L
pum_drive_align_modules = 6,7
pum_drive_align_gain = 1.0
uim_drive_align_bank = ETMX_L1_DRIVEALIGN_L2L
uim_drive_align_modules =
uim_drive_align_gain = 1.0
''',
                                            measurement='actuation_x_arm')
        [uim_response, pum_response, tst_response] = \
            A.drivealign_to_displacement(self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(np.abs(uim_response[n]),
                                   np.abs(self.UIM_known_tf[n]))
            self.assertAlmostEqual(
                np.angle(uim_response[n], deg=True),
                np.angle(self.UIM_known_tf[n], deg=True))
            self.assertAlmostEqual(np.abs(pum_response[n]),
                                   np.abs(self.PUM_known_tf[n]))
            self.assertAlmostEqual(
                np.angle(pum_response[n], deg=True),
                np.angle(self.PUM_known_tf[n], deg=True))
            self.assertAlmostEqual(np.abs(tst_response[n]),
                                   np.abs(self.TST_known_tf[n]))
            self.assertAlmostEqual(
                np.angle(tst_response[n], deg=True),
                np.angle(self.TST_known_tf[n], deg=True))


class TestDrivealignToDisplacementForMeasurement(unittest.TestCase):

    def setUp(self):
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.TST_known_tf = np.array(
            [5.021191554058338e-05-8.337501336501237e-06j,
             -2.65737365777503e-05-5.83908650471638e-06j,
             -7.1419775097599665e-06+2.2426904309365334e-05j,
             2.642942192222995e-06+4.9364036533587704e-06j,
             1.1308404476528101e-06+5.625134620308336e-07j,
             2.1027000668484317e-07-4.3420540327504015e-09j,
             2.5099092594663896e-08-1.3408894176873065e-08j,
             1.222723232386295e-09-3.9781703249724626e-09j,
             -5.623980556089653e-10+7.931643165474655e-11j,
             -3.137783061591325e-11-4.0487015056095644e-11j])
        self.PUM_known_tf = np.array(
            [1.912559101220233e-11-3.903503943063181e-11j,
             -2.2190974004158754e-13-1.1349077030787211e-14j,
             -3.20190609206482e-15+1.293047553209863e-15j,
             -4.140296235222137e-17+4.024381810515447e-17j,
             -7.858904897311117e-20+7.567534834056722e-19j,
             5.798718594836214e-21+4.996207685404243e-21j,
             1.3537541588073445e-23-9.871817552631662e-24j,
             -3.852467222651472e-25-2.8445559664330002e-25j,
             -1.3035537018142603e-25+1.0663576595639575e-25j,
             1.5568659592103235e-28+9.862261585383335e-29j])
        self.UIM_known_tf = np.array(
            [2.0996102579724625e-11-7.769902876214075e-11j,
             1.523859088179713e-13+9.468932918590974e-14j,
             4.989451373587049e-16-4.575368122437622e-18j,
             1.4129108924473284e-18-3.366498284514433e-20j,
             5.302277690660671e-21-3.29640710900283e-22j,
             -3.237787617232506e-23-7.800759267742482e-25j,
             -1.3186489490840405e-24+6.006166056695082e-25j,
             -2.2478566623746473e-29+3.6494347262147576e-29j,
             -1.1401753663433159e-32-5.8544630665447124e-33j,
             1.2521949162178118e-37+1.929736175937275e-39j])

    def tearDown(self):
        del self.frequencies
        del self.TST_known_tf
        del self.PUM_known_tf
        del self.UIM_known_tf

    def test_known_actuation_terms_for_measurement(self):
        A = pydarm.actuation.ActuationModel('''
[metadata]
[interferometer]
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
tst_drive_align_bank = ETMX_L3_DRIVEALIGN_L2L
tst_drive_align_modules = 4,5
tst_drive_align_gain = -35.7
pum_drive_align_bank = ETMX_L2_DRIVEALIGN_L2L
pum_drive_align_modules = 6,7
pum_drive_align_gain = 1.0
uim_drive_align_bank = ETMX_L1_DRIVEALIGN_L2L
uim_drive_align_modules =
uim_drive_align_gain = 1.0
''',
                                            measurement='actuation_x_arm')
        [uim_response, pum_response, tst_response] = \
            A.known_actuation_terms_for_measurement(self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(np.abs(uim_response[n]),
                                   np.abs(self.UIM_known_tf[n]))
            self.assertAlmostEqual(
                np.angle(uim_response[n], deg=True),
                np.angle(self.UIM_known_tf[n], deg=True))
            self.assertAlmostEqual(np.abs(pum_response[n]),
                                   np.abs(self.PUM_known_tf[n]))
            self.assertAlmostEqual(
                np.angle(pum_response[n], deg=True),
                np.angle(self.PUM_known_tf[n], deg=True))
            self.assertAlmostEqual(np.abs(tst_response[n]),
                                   np.abs(self.TST_known_tf[n]))
            self.assertAlmostEqual(
                np.angle(tst_response[n], deg=True),
                np.angle(self.TST_known_tf[n], deg=True))


class TestComputeActuationSingleStage(unittest.TestCase):

    def setUp(self):
        # TST stage
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_single_stage = np.array(
            [-2.2226292345691665e-15+3.7055835896161056e-16j,
             1.1768496904693823e-15+2.5650581888551325e-16j,
             3.1184631196028356e-16-9.942029247767746e-16j,
             -1.1944786777482867e-16-2.1720731539345392e-16j,
             -5.076181343593909e-17-2.344496830068076e-17j,
             -9.269325912589879e-18+8.84859270770252e-19j,
             -9.775946787962668e-19+7.95794257011437e-19j,
             3.8327563676853116e-20+1.8108722537309245e-19j,
             -7.300815076923215e-21-2.6726320383495696e-20j,
             2.3885715105224723e-21-3.8671879493130684e-22j])

    def tearDown(self):
        del self.frequencies
        del self.known_single_stage

    def test_compute_actuation_single_stage(self):
        """ Test a single actuation stage """
        A = pydarm.actuation.ActuationModel('''
[metadata]
[interferometer]
[actuation_x_arm]
darm_feedback_sign = -1
tst_NpV2 = 4.427e-11
linearization = OFF
actuation_esd_bias_voltage = -9.3
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
''',
                                            measurement='actuation_x_arm')
        single_stage = A.compute_actuation_single_stage(self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(np.abs(single_stage[n]),
                                   np.abs(self.known_single_stage[n]))
            self.assertAlmostEqual(
                np.angle(single_stage[n], deg=True),
                np.angle(self.known_single_stage[n], deg=True))


class TestDARMOutputMatrixValues(unittest.TestCase):

    def setUp(self):
        # darm_output_matrix = 1.0, -1.0, 0.0, 0.0
        # darm_feedback_x    = OFF, ON, ON, ON
        # darm_feedback_y    = OFF, OFF, OFF, OFF
        self.known_output_matrix = np.array([[0, 1.0, 1.0, 1.0],
                                             [0, 0, 0, 0]])

    def tearDown(self):
        del self.known_output_matrix

    def test_output_matrix_values(self):
        A = pydarm.actuation.DARMActuationModel('''
[metadata]
[interferometer]
[actuation]
darm_output_matrix = 1.0, -1.0, 0.0, 0.0
darm_feedback_x = OFF, ON, ON, ON
darm_feedback_y = OFF, OFF, OFF, OFF
''')
        output_matrix = A.darm_output_matrix_values()
        for n in range(len(output_matrix[:, 0])):
            for m in range(len(output_matrix[0, :])):
                self.assertAlmostEqual(output_matrix[n, m],
                                       self.known_output_matrix[n, m])


class TestComputeActuation(unittest.TestCase):

    def setUp(self):
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_A = np.array(
            [-3.63234851552863e-13-2.297849477733715e-13j,
             -1.5785405207037768e-14+7.022803250131525e-15j,
             -1.9906028977349535e-15+8.499087530441956e-16j,
             -2.9626430309517743e-16+4.980882746237151e-17j,
             -4.5497245018124926e-17+5.851368523167505e-18j,
             -7.117215795049456e-18+7.70258488252587e-19j,
             -9.974890659056889e-19+7.966180520139261e-19j,
             3.8712043816670766e-20+1.8134804487474165e-19j,
             -7.463095731015656e-21-2.67674977773168e-20j,
             2.3885824821188465e-21-3.8665176935995385e-22j])

    def tearDown(self):
        del self.frequencies
        del self.known_A

    def test_computeActuation(self):
        A = pydarm.actuation.DARMActuationModel('''
[metadata]
[interferometer]
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
''')
        actuation_tf = A.compute_actuation(self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(np.abs(actuation_tf[n]),
                                   np.abs(self.known_A[n]))
            self.assertAlmostEqual(
                np.angle(actuation_tf[n], deg=True),
                np.angle(self.known_A[n], deg=True))


class TestComputeMultiArmActuation(unittest.TestCase):

    def setUp(self):
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_A = 2*np.array(
            [-3.63234851552863e-13-2.297849477733715e-13j,
             -1.5785405207037768e-14+7.022803250131525e-15j,
             -1.9906028977349535e-15+8.499087530441956e-16j,
             -2.9626430309517743e-16+4.980882746237151e-17j,
             -4.5497245018124926e-17+5.851368523167505e-18j,
             -7.117215795049456e-18+7.70258488252587e-19j,
             -9.974890659056889e-19+7.966180520139261e-19j,
             3.8712043816670766e-20+1.8134804487474165e-19j,
             -7.463095731015656e-21-2.67674977773168e-20j,
             2.3885824821188465e-21-3.8665176935995385e-22j])

    def tearDown(self):
        del self.frequencies
        del self.known_A

    def test_computeActuation(self):
        A = pydarm.actuation.DARMActuationModel('''
[metadata]
[interferometer]
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

[actuation_y_arm]
darm_feedback_sign = 1
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
darm_feedback_y = OFF, ON, ON, ON
''')
        actuation_tf = A.compute_actuation(self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(np.abs(actuation_tf[n]),
                                   np.abs(self.known_A[n]))
            self.assertAlmostEqual(
                np.angle(actuation_tf[n], deg=True),
                np.angle(self.known_A[n], deg=True))


if __name__ == '__main__':
    unittest.main()
