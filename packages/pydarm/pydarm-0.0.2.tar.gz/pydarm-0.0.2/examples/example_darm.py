import pydarm
import os
import numpy as np

# A configuration of the DARM model can be passed as a string to an ini
# file or as a string with all of the parameters. Here we pass a path and
# filename to the ini file
config = '../example_model_files/H1_20190416.ini'

# Note that you may need to specify where the aligocalibration SVN repo
# base path is on your local checkout. For example, you may have it checked
# out to your home directory instead of /ligo/svncommon/ so in the example
# configuration file, you would change
#   cal_data_root = /ligo/svncommon/aligocalibration/trunk
# to
#   cal_data_root = /home/albert.einstein/aligocalibration/trunk
# This can also be overridden with the CAL_DATA_ROOT environement variable.

# Set an environment variable that is the base path to imported files
# (see note above)
os.environ['CAL_DATA_ROOT'] = './test'

# Load sensing parameters of the config file into the SensingModel object
# This has everything you need to compute transfer functions or other products
# using methods of the SensingModel class
C = pydarm.sensing.SensingModel(config)

# Load actuation parameters into the DARMActuationModel. Note that you
# need to provide the appropriately expected values meaning that if
# the output matrix has a non-zero element for an arm and the arm has
# feedback path to some stage turned on, then the DARM model
# parameters for that stage must be provided. If the elements are
# turned off, then it doesn't matter what is listed, they will go
# unused. To be used, both output matrix and feedback on that arm must
# be ON
A = pydarm.actuation.DARMActuationModel(config)

# Complete the DARM model by bringing everything together
# This has everything you need to compute transfer functions or other products
# using methods of the DARMModel class
darm = pydarm.darm.DARMModel(config)

# File path and filename to the uncertainty budgeting configuration.
# This can also be a string of parameters with key value pairs in sections
config_uncertainty = '../example_model_files/H1_20190416_uncertainty.ini'

# Create an instance of the DARMUncertainty class so that we can compute
# an uncertainty budget
unc = pydarm.uncertainty.DARMUncertainty(config_uncertainty)

# Create a frequency vector to evalute the response function
frequencies = np.logspace(np.log10(20), np.log10(2000), 10)

# Generate response function uncertainty trials at a specific GPS time
# and specific frequencies. If you run this command, you will need
# your LIGO.ORG credentials to access data
# 1240581618 = April 29 2019 14:00:00 UTC
trials = unc.compute_response_uncertainty(1240581618, frequencies)
