import pydarm
import numpy as np
# import matplotlib.pyplot as plt
"""
This script gives a few example usages of the plot method pydarm/plot.py.
The method tries to be flexible with the input. See the code for all
possibilities.
The plot functions below DO NOT produce an interacive graph unless you
run plt.show()
"""

# --------------------------------------------------------------------
# Example with two darm models (there are other ways to make 2 models)

config = '../example_model_files/myH1_20190416.ini'

D1 = pydarm.darm.DARMModel(config)
D2 = pydarm.darm.DARMModel(config)
D2.sensing.coupled_cavity_pole_frequency = 150

# You can simply do the following to get the critique plots.
D1.plot(filename='plot_example_critique_1.pdf', label=['H1'])

# Do the following if you want to get critique plots and at the same
# time compare two models.
pydarm.plot.critique(D1, D2, label=['Normal D1', 'Crazy D2'],
                     filename='plot_example_critique_2.pdf', ifo='H1', ugf_start=10, ugf_end=100)

# If you don't want all the plots but just one kind do this
pydarm.plot.critique(D1, plot_selection='olg', label=['OLG'], filename='plot_example_just_olg.pdf')

# --------------------------------------------------------------------
# Example with different kinds of inputs. The data plotted are duplicates
# but that shouldn't matter for this demonstration.

# Frequency list for a freq, tf input.
freq = np.logspace(-1, 4, 1000)
tf = D1.compute_darm_olg(freq)

# Create a tuple to show that this works too for plotting
test_tuple2 = (freq, tf)

# Example of inputting data, to see that error bars are taken care of.

# These are the xml files we want to get our data from.
measurement_file_1 = \
    '../test/2020-01-03_H1_DARM_OLGTF_LF_SS_5to1100Hz_15min.xml'

meas_obj_1 = pydarm.measurement.Measurement(measurement_file_1)
channelA_1 = 'H1:LSC-DARM1_IN2'
channelB_1 = 'H1:LSC-DARM1_IN1'

measurement_tuple = meas_obj_1.get_raw_tf(channelA_1,
                                          channelB_1,
                                          cohThresh=0.0)
pydarm.plot.residuals(freq, -tf,
                      measurement_tuple[0], measurement_tuple[1], measurement_tuple[3],
                      mag_min=0.8, mag_max=1.2, phase_min=-5, phase_max=5,
                      filename='plot_example_residuals.pdf', plot_input=True, show=False)

# if you really want to save code, just input a method.
pydarm.plot.plot(D1.compute_darm_olg, label=['method'], filename='plot_example_method.pdf',
                 show=False, greed=True)

pydarm.plot.plot(test_tuple2,
                 freq, D1.compute_darm_olg(freq),
                 freq, D1.compute_darm_olg(freq)*2,
                 measurement_tuple,
                 title='Test Plot',
                 label=['2 tuple', '1+1', '1+1', '4 tuple'],
                 style='example.mplstyle',
                 filename='plot_example_multiinputs.pdf')
# plt.show()
