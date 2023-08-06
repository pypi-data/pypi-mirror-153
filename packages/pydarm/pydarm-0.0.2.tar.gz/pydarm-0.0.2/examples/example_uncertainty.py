import pydarm
import numpy as np
from gwpy.timeseries import TimeSeriesDict as tsd
import os

os.environ['CAL_DATA_ROOT'] = '../test'

frequencies = np.logspace(0, np.log10(5000.), 10)

# Reading in data from GWPY
# This data was previously saved, and is completely optional to provide
data = tsd.read('../test/test_ch_data.hdf5')

# See ../example_model_files/H1_20190416_uncertainty.ini
# for more details
config = '''[reference-model]
model = ../example_model_files/H1_20190416.ini
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
sys_unc = 0.005
sample = True'''

# Intialize a DARMUncertainy object
test_unc = pydarm.uncertainty.DARMUncertainty(config)

# Sample the uncertainty
samples = test_unc.compute_response_uncertainty(
    1239958818, frequencies, trials=10, data=data)
