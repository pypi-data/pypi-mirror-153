import numpy as np
from pydarm import measurement
from matplotlib import pyplot as plt

"""
Example code on how to use the following classes from sensing.py:
    - ProcessSensingMeasurement
"""

# Note that you may need to specify where the aligocalibration SVN repo
# base path is on your local checkout. For example, you may have it checked
# out to your home directory instead of /ligo/svncommon/ so in the example
# configuration file, you would change
#   cal_data_root = /ligo/svncommon/aligocalibration/trunk
# to
#   cal_data_root = /home/albert.einstein/aligocalibration/trunk
# This can also be overridden with the CAL_DATA_ROOT environment variable.

# These are the xml files we want to get our data from.
measurement_file_1 = \
    '../test/2020-01-03_H1_DARM_OLGTF_LF_SS_5to1100Hz_15min.xml'
measurement_file_2 = \
    '../test/2020-01-03_H1_PCALY2DARMTF_LF_SS_5t1100Hz_10min.xml'

# This is the model file that we need to use in order to process the data.
model_file = '../example_model_files/H1_20190416.ini'

# ----------------------------------------------------------------------
# If you want to get the processed sensing data for input to the  MCMC
# process, do the following:
meas1 = measurement.Measurement(measurement_file_1)
meas2 = measurement.Measurement(measurement_file_2)

process_sensing = measurement.ProcessSensingMeasurement(
    model_file, meas1, meas2,
    ('H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_EXC'),
    ('H1:CAL-PCALY_RX_PD_OUT_DQ', 'H1:LSC-DARM_IN1_DQ'),
    0.9, 0.9999)

# The method below returns 3 arrays:
# frequency, corrected sensing, relative uncertainty.
# Here is where you tell the ProcessMeasurement object what channels
# are used. The list (channel A, channel B) will extract the transfer
# function channel B / channel A from the DTT file. The first of the two
# transfer functions should be the closed loop gain, and the second should
# be the PCAL to DARM transfer function
frequencies, processed_optical_response, processed_optical_response_unc = \
    process_sensing.get_processed_measurement_response()

# Now we can plot the data.

plt.figure(1)
plt.subplot(211)
plt.loglog(frequencies, np.abs(processed_optical_response), 'ro')
plt.subplot(212)
plt.semilogx(frequencies, np.angle(processed_optical_response, deg=True), 'ro')
plt.show(block=True)
