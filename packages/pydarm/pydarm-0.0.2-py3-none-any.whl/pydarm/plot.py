# Copyright (C) Jameson Rollins (2021)
#
# This file is part of pyDARM.
#
# pyDARM is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# pyDARM is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# pyDARM. If not, see <https://www.gnu.org/licenses/>.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from matplotlib.backends.backend_pdf import PdfPages
from pydarm import darm
from scipy.interpolate import interp1d

plt.rcParams.update({'text.usetex': False,
                     'lines.linewidth': 3,
                     'font.family': 'sans-serif',
                     'font.serif': 'Helvetica',
                     'font.size': 10,
                     'xtick.labelsize': 'x-large',
                     'xtick.direction': 'in',
                     'ytick.labelsize': 'x-large',
                     'ytick.direction': 'in',
                     'axes.labelsize': 'medium',
                     'axes.titlesize': 'x-large',
                     'axes.grid': True,
                     'grid.alpha': 0.5,
                     'lines.markersize': 12,
                     'legend.borderpad': 0.2,
                     'legend.fancybox': True,
                     'legend.fontsize': 'medium',
                     'legend.framealpha': 0.7,
                     'legend.handletextpad': 0.1,
                     'legend.labelspacing': 0.2,
                     'legend.loc': 'best',
                     'figure.figsize': (12, 8),
                     'savefig.dpi': 100,
                     'savefig.orientation': 'landscape',
                     'pdf.compression': 9})


class BodePlot:
    """bode plotting object

    """
    def __init__(self, fig=None, title=None, figsize=(12, 8), only=''):
        """
        PARAMETERS
        ----------
        only (string): if set to 'mag' or 'phase', this object will only
        plot magnitude or phase, and not the usual 2x1 body plot.

        NOTES
        -----

        """
        self.fig = fig or plt.figure(figsize=figsize)
        self.only = only

        if self.only == '':
            self.ax_mag = self.fig.add_subplot(211)
            self.ax_mag.grid(True)
            self.ax_mag.grid(which='minor', axis='both', linestyle='--')
            # self.ax_mag.axhline(1, color='k', linestyle='dashed')
            self.ax_mag.set_ylabel('Magnitude')

            self.ax_phase = self.fig.add_subplot(212)
            self.ax_phase.grid(True)
            self.ax_phase.grid(which='minor', axis='both', linestyle='--')
            self.ax_phase.set_yticks(np.arange(-180, 180+30, 30))
            self.ax_phase.set_ylabel('Phase [deg]')
            self.ax_phase.set_xlabel('Frequency [Hz]')
            self.ax_phase.set_ylim(-185, 185)

        if self.only == 'mag' or self.only == 'magnitude':
            self.ax_mag = self.fig.add_subplot(111)
            self.ax_mag.grid(True)
            self.ax_mag.grid(which='minor', axis='both', linestyle='--')
            # self.ax_mag.axhline(1, color='k', linestyle='dashed')
            self.ax_mag.set_ylabel('Magnitude')
            self.ax_mag.set_xlabel('Frequency [Hz]')

        if self.only == 'phase':
            self.ax_phase = self.fig.add_subplot(111)
            self.ax_phase.grid(True)
            self.ax_phase.grid(which='minor', axis='both', linestyle='--')
            self.ax_phase.set_yticks(np.arange(-180, 180+30, 30))
            self.ax_phase.set_ylabel('Phase [deg]')
            self.ax_phase.set_xlabel('Frequency [Hz]')
            self.ax_phase.set_ylim(-185, 185)

        if title:
            self.fig.suptitle(title, y=0.9)

    def plot(self, freq, tf, **kwargs):
        """add frequency response to plot"""
        if self.only == '' or self.only == 'mag' or self.only == 'magnitude':
            self.ax_mag.loglog(freq, np.abs(tf), **kwargs)
        if self.only == '' or self.only == 'phase':
            self.ax_phase.semilogx(freq, np.angle(tf, deg=True), **kwargs)

    def error(self, freq, tf, tf_error, **kwargs):
        """add frequency response to plot with error
           Note: Error should be relative.
        """
        if self.only == '' or self.only == 'mag' or self.only == 'magnitude':
            self.ax_mag.errorbar(freq, np.abs(tf), np.abs(tf)*tf_error, **kwargs)
            self.ax_mag.set_xscale('log')
            self.ax_mag.set_yscale('log')
        if self.only == '' or self.only == 'phase':
            self.ax_phase.errorbar(freq, np.angle(tf, deg=True), tf_error*180/np.pi, **kwargs)
            self.ax_phase.set_xscale('log')
            self.ax_phase.set_yscale('linear')

    def legend(self, labels):
        """add legend"""
        if self.only == '' or self.only == 'mag' or self.only == 'magnitude':
            self.ax_mag.legend(labels)
        if self.only == 'phase':
            self.ax_phase.legend(labels)

    def save(self, path):
        """save bode plot to file"""
        self.fig.savefig(path)

    def show(self):
        """show interactive plot"""
        plt.show()

    def xlim(self, freq_min, freq_max):
        """set min max for frequency axis"""
        if self.only == '' or self.only == 'mag' or self.only == 'magnitude':
            self.ax_mag.set_xlim(freq_min, freq_max)
            self.autoscale_mag_y()
        if self.only == '' or self.only == 'phase':
            self.ax_phase.set_xlim(freq_min, freq_max)

    def ylim(self, mag_min, mag_max, phase_min=-185, phase_max=185):
        """set min max for the magnitude (and phase) axis"""
        if self.only == '' or self.only == 'mag' or self.only == 'magnitude':
            self.ax_mag.set_ylim(mag_min, mag_max)
        if self.only == '' or self.only == 'phase':
            self.ax_phase.set_ylim(phase_min, phase_max)

    def vlines(self, vfreq):
        """add vertical line at specific frequency in both mag and phase plot"""
        if self.only == '' or self.only == 'mag' or self.only == 'magnitude':
            self.ax_mag.axvline(vfreq, color='red', lw=1.0, linestyle='--', label='_nolegend_')
        if self.only == '' or self.only == 'phase':
            self.ax_phase.axvline(vfreq, color='red', lw=1.0, linestyle='--', label='_nolegend_')

    def text(self, x, y, plot_text):
        """add text in plot"""
        if self.only == '' or self.only == 'mag' or self.only == 'magnitude':
            self.ax_mag.text(x, y, plot_text)
        if self.only == 'phase':
            self.ax_phase.text(x, y, plot_text)

    def autoscale_mag_y(self, margin=0.1):
        """This function rescales the y-axis based on the data that is visible given
        the current xlim of the axis."""

        def get_bottom_top(line):
            xd = np.array(line.get_xdata())
            yd = np.array(line.get_ydata())
            lo, hi = self.ax_mag.get_xlim()
            y_displayed = yd[((xd > lo) & (xd < hi))]
            bot = np.min(np.abs(y_displayed[np.nonzero(y_displayed)]))*(1-margin)
            top = np.max(y_displayed)*(1+margin)
            return bot, top

        lines = self.ax_mag.get_lines()
        bot, top = np.inf, -np.inf

        for line in lines:
            new_bot, new_top = get_bottom_top(line)
            if new_bot < bot:
                bot = new_bot
            if new_top > top:
                top = new_top
        self.ax_mag.set_ylim(bot, top)

    def greed(self, more_minor=True):
        """add a finer grid than the default"""
        if self.only == '' or self.only == 'mag' or self.only == 'magnitude':
            self.ax_mag.yaxis.set_major_locator(plticker.LogLocator(base=10, numticks=200))
            if more_minor:
                locmin = plticker.LogLocator(base=10,
                                             subs=(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9),
                                             numticks=6000)
                self.ax_mag.yaxis.set_minor_locator(locmin)
            self.ax_mag.grid(which='major', axis='both', linestyle='-')

        if self.only == '' or self.only == 'phase':
            self.ax_phase.yaxis.set_major_locator(plticker.MultipleLocator(base=45))
            self.ax_phase.yaxis.set_minor_locator(plticker.MultipleLocator(base=5))
            self.ax_phase.grid(which='major', axis='both', linestyle='-')


def plot(*args, freq_min=0.1, freq_max=5000, freq_points=1001, filename=None,
         mag_min=None, mag_max=None, phase_min=-185, phase_max=185, label=None,
         title=None, style=None, show=None, greed=False, figsize=(12, 8), **kwargs):
    """
    This method provides a simple way to plot quickly anything you want.

    PARAMETERS
    ----------
    args: Here you can input any kind of transfer function related data.
          It accepts multiple sets in multiple formats.
          FORMATS: - 2-tuple (freq,transfer function)
                - 3-tuple (freq,transfer function, rel unc)
                - 4-tuple (freq,transfer function, coherence, rel unc)
                - freq, transfer function (two lists or 1d arrays separated by comma)
                - method that returns a transfer function
                  e.g. D.compute_darm_olg
                  (assuming D is a darm model object)

    Options for the graphs: - freq_min (float) start frequency
                - freq_max (float) end frequency
                - freq_points (int) number of points to calculate
                - filename (string)
                  if given, ALL generated graphs will be saved in one pdf.
                - mag_min (float) minimum magnitude scale
                - mag_max (float) maximum magnitude scale
                - phase_min (float) minimum phase scale
                - phase_max (float) maximum phase scale
                - label (list of strings)
                  legend string for the data sets given
                  e.g. ['first data', 'second']
                - title (str) title of the graph
                - style (str) one of the styles matplotlib has
                  or a user filename with style
                - show (boolean) if true the plot will show
                - greed (boolean) if true a finer grid is drawn for all figs
                - figsize: figure size
                - **kwargs, you can also use all the available
                  matplotlib keywords, but have to be common
                  for all graphs.
    RETURNS
    -------
    Plots all data sets in one graph.
    Give a filename, if you want to save a pdf of your plots.
    ALSO RETURNS HANDLE OF BODY PLOT

    NOTES
    -----
    """
    if filename:
        plt.close('all')
    if style:
        plt.style.use(style)

    # BodyPlot object.
    bp = BodePlot(title=title, figsize=figsize)

    # Temporary index used to identify frequency inputs and transfer function inputs.
    temp_pair_index = 0

    for argument in args:
        # Check if a simple list. If so, then this assumes it is frequency
        # The next one will be taken to be a TF
        if isinstance(argument, (np.ndarray, list)):
            temp_pair_index = temp_pair_index+1
            if (temp_pair_index % 2) == 1:
                # This array should be the frerquency array
                freq_in = argument
            if (temp_pair_index % 2) == 0:
                # This array should then be a TF array
                tf_in = argument
                bp.plot(freq_in, tf_in, **kwargs)
        # Check if this is a tuple. If so, a tuple of size 2 is assumed to
        # be (freq,tf) pair, and if a tuple of size 4 is assumed to be a TF
        # that comes from the measurement class with (freq,tf,coh,unc).
        elif isinstance(argument, (tuple)):
            if len(argument) == 2:
                # This tuple should be (freq,tf)
                freq_in = argument[0]
                tf_in = argument[1]
                bp.plot(freq_in, tf_in, **kwargs)
            elif len(argument) == 3:
                # This tuple should be (freq,tf,unc)
                freq_in = argument[0]
                tf_in = argument[1]
                # Uncertainty is relative, and needs to be for error plot.
                tf_unc = argument[2]
                bp.error(freq_in, tf_in, tf_unc, fmt='ro', linestyle='None', **kwargs)
            elif len(argument) == 4:
                # This tuple should be (freq,tf,coh,unc)
                freq_in = argument[0]
                tf_in = argument[1]
                # tf_coh = argument[2]
                # Uncertainty is relative, and needs to be for error plot.
                tf_unc = argument[3]
                bp.error(freq_in, tf_in, tf_unc, fmt='ro', linestyle='None', **kwargs)
            else:
                raise ValueError('Bad tuple given for plotting')
        else:
            # This argument is a method. We use the frequencies given
            # or the default ones.
            freq = np.logspace(np.log10(float(freq_min)),
                               np.log10(float(freq_max)), int(freq_points))
            tf_in = argument(freq)
            bp.plot(freq, tf_in, **kwargs)

    if label:
        bp.legend(label)
    bp.xlim(freq_min, freq_max)
    if greed:
        bp.greed()
    if mag_min:
        bp.ylim(mag_min, mag_max, phase_min=phase_min, phase_max=phase_max)
    if filename:
        bp.save(filename)
    if show:
        plt.show()
    # Return the handle of the bode plot in case you want to do more things
    # to your plot. Does not return handles of critiques.
    return bp


def residuals(freq_model, tf_model, freq_data, tf_data, unc_data,
              mag_min=0.8, mag_max=1.2, phase_min=-5, phase_max=5,
              mag_major_tick=0.05, mag_minor_tick=0.01,
              phase_major_tick=2, phase_minor_tick=0.5,
              filename=None, show=None, plot_input=False):
    """
    EXAMPLE USAGE
    measurement_tuple = freq_data, tf_data, unc_data
    plot(freq_model, tf_model, measurement_tuple,
         freq_min=freq_data[0], freq_max=freq_data[-1],
         title='Measurement vs Model')
    """
    f_mag_model = interp1d(freq_model, np.abs(tf_model), kind='cubic')
    f_phase_model = interp1d(freq_model, np.angle(tf_model), kind='cubic')
    residuals_mag = np.abs(tf_data)/f_mag_model(freq_data)
    residuals_phase = np.angle(tf_data)-f_phase_model(freq_data)
    residuals_tf = residuals_mag*np.exp(1j*residuals_phase)
    residuals_tuple = freq_data, residuals_tf, unc_data

    if plot_input:
        if filename is not None:
            filename_input = filename[0:-4]+'_input'+filename[len(filename)-4:len(filename)]
        else:
            filename_input = None
        plot(freq_model, tf_model, (freq_data, tf_data, unc_data), title='Measurement vs Model',
             freq_min=freq_data[0], freq_max=freq_data[-1], filename=filename_input)

    bode_handle = plot(residuals_tuple, freq_min=freq_data[0], freq_max=freq_data[-1],
                       mag_min=mag_min, mag_max=mag_max, phase_min=phase_min,
                       phase_max=phase_max, show=show, title='Measurement vs Model Residuals')
    bode_handle.ax_mag.set_yscale('linear')

    bode_handle.ax_mag.yaxis.set_major_locator(plticker.MultipleLocator(base=mag_major_tick))
    bode_handle.ax_mag.yaxis.set_minor_locator(plticker.MultipleLocator(base=mag_minor_tick))
    bode_handle.ax_mag.grid(which='major', axis='both', linestyle='-')
    bode_handle.ax_phase.yaxis.set_major_locator(plticker.MultipleLocator(base=phase_major_tick))
    bode_handle.ax_phase.yaxis.set_minor_locator(plticker.MultipleLocator(base=phase_minor_tick))
    bode_handle.ax_phase.grid(which='major', axis='both', linestyle='-')

    if filename:
        bode_handle.save(filename)


def get_ugf(freq, tf, search_start=5., search_end=1000., n_points=10000):
    """
    Very non-fancy function for easily finding UGF in the simplest of cases.
    PARAMETERS
    ----------
    freq: (float) array of frequencies corresponding to the given tf
    tf: (complex) array of the transfer function you want the ugf of
    search_start: (float) frequency to start UGF search
    search_end: (float) frequency to end UGF search
    n_points: (int) increase for increased accuracy of UGF frequency
    RETURNS
    -------
    2-tuple float: UGF frequency, phase margin

    """
    mag = np.abs(tf)
    phase = np.angle(tf)*180/np.pi
    f_mag = interp1d(freq, mag, kind='cubic', fill_value="extrapolate")
    f_phase = interp1d(freq, phase, kind='cubic', fill_value="extrapolate")
    freq_new = np.logspace(np.log10(search_start), np.log10(search_end), n_points)
    i = 1
    while f_mag(freq_new[i]) > 1 and i < (n_points-1):
        i = i+1
    if i == n_points-1:
        print('WARNING: UGF NOT FOUND WITHIN THE RANGE GIVEN')
        return -1, 0
    else:
        return np.round(freq_new[i]), np.round(f_phase(freq_new[i]))


def save_multifig(filename, figs=None, dpi=200):
    """ method to save all existing (or list of given) figures in one pdf file
    """

    pp = PdfPages(filename)
    if figs is None:
        figs = [plt.figure(n) for n in plt.get_fignums()]
    for fig in figs:
        fig.savefig(pp, format='pdf')
    pp.close()


def critique(*args, filename=None, plot_selection='all', ifo='', show=None,
             label=None, freq_min=0.1, freq_max=5000, freq_points=1001,
             ugf_start=10, ugf_end=1000, greed=True, figsize=(12, 8), **kwargs):
    """
    This method produces critique models for 1 or 2 models.

    PARAMETERS
    ----------
    args: The first argumets should be 1 or 2 darm models.
              - darm model object (DARMModel)

    The plots produced should be close to the final critique plot, but if
    one needs something special there are a few options to tweak
    Options for the graphs: - freq_min (float) start frequency
                            - freq_max (float) end frequency
                            - freq_points (int) number of points to calculate
                            - label (list of strings)
                            - **kwargs, you can also use all the available
                                        matplotlib keywords, but have to be common
                                        for all graphs.
                            - filename (string)
                              if given, ALL generated graphs will be saved in one pdf.
                            - ifo (string)
                              if given with a model to plot, it will appear in the
                              graph titles.
                            - ugf_start, ugf_end (float)
                              frequency range used for the search of the UGF
                            - greed (bool)
                            - plot_selection (string)
                              'all':
                              'optical':
                              'actuation':
                              'clg':
                              'olg':
                              'digital':
    RETURNS
    -------
    Plots critique plots of the given darm model, and saves them in one pdf file.

    NOTES
    -----
    I list some hard coded defaults that are not options of the method.
    """
    # See bp1 plot
    default_olg_yspan = 1e12
    # See bp2 plot
    default_olg_zoom_fmin = 10
    default_olg_zoom_fmax = 200
    # See bp3b plot
    default_clg_zoom_fmin = 20
    default_clg_zoom_fmax = 400
    # See bp4 plot
    default_dig_yspan = 1e7
    # See bp6 plot
    default_act_strength_yspan = 1e17
    # See bp8, bp11 plot
    default_act_displ_yspan = 1e17

    if filename:
        plt.close('all')

    # Check if all inputs are darm models. If so, it count the number of
    # models given (1 or 2). If not, it complains.
    if all(isinstance(argument, (darm.DARMModel)) for argument in args):
        if len(args) > 2:
            print('You asked critique plots for more than 2 models. Results might be unpleasant.')
    else:
        ValueError('Function plot.critique only takes DARMModel objects as inputs')

    # Temporary index used to identify the first darm model given.
    temp_model_index = 1
    list_of_figures = []

    plt.rc('legend', fontsize=18)

    for argument in args:
        freq = np.logspace(np.log10(float(freq_min)),
                           np.log10(float(freq_max)), int(freq_points))

        G = argument.compute_darm_olg(freq)
        D = argument.digital.compute_response(freq)
        C = argument.sensing.compute_sensing(freq)
        R = argument.compute_response_function(freq)
        # For all actuation calculations I am using param names that
        # (I think) match old pydarm

        # TF from output of actuation digital filter bank
        # to displacement, for each stage
        x_UIM_strength, x_PUM_strength, x_TST_strength = \
            argument.actuation.xarm.digital_out_to_displacement(freq)
        # TF of suspension digital filters
        x_UIM_umodel, x_PUM_umodel, x_TST_umodel = \
            argument.actuation.xarm.sus_digital_filters_response(freq)
        # TF from LOCK_IN to displacement by stage
        x_UIM_authority = \
            argument.actuation.xarm.compute_actuation_single_stage(freq, stage='UIM')
        x_PUM_authority = \
            argument.actuation.xarm.compute_actuation_single_stage(freq, stage='PUM')
        x_TST_authority = \
            argument.actuation.xarm.compute_actuation_single_stage(freq, stage='TST')
        x_ALL_authority = x_UIM_authority+x_PUM_authority+x_TST_authority
        # TF from DARM_IN to discplacement scaled by optical gain
        x_UIM_total = x_UIM_authority*D*argument.sensing.coupled_cavity_optical_gain
        x_PUM_total = x_PUM_authority*D*argument.sensing.coupled_cavity_optical_gain
        x_TST_total = x_TST_authority*D*argument.sensing.coupled_cavity_optical_gain

        # Relative contribution of actuation stages
        x_UIM_rel = x_UIM_authority*D/R
        x_PUM_rel = x_PUM_authority*D/R
        x_TST_rel = x_TST_authority*D/R
        x_ALL_rel = x_ALL_authority*D/R
        invCnorm = 1/C/R

        if temp_model_index == 1:
            if plot_selection == 'all' or plot_selection == 'olg':
                bp1 = BodePlot(title=f'{ifo} DARM Open Loop Gain: G', figsize=figsize)
                list_of_figures.append(plt.gcf())
            if plot_selection == 'all':
                bp2 = BodePlot(title=f'{ifo} DARM Open Loop Gain: G (ZOOM)', figsize=figsize)
                list_of_figures.append(plt.gcf())
            if plot_selection == 'all' or plot_selection == 'clg':
                bp3 = BodePlot(title=f'{ifo} DARM Closed Loop Gain: 1/(1+G)', figsize=figsize)
                list_of_figures.append(plt.gcf())
                bp3b = BodePlot(title=f'{ifo} DARM Closed Loop Gain: 1/(1+G) (ZOOM)',
                                figsize=figsize)
                list_of_figures.append(plt.gcf())
            if plot_selection == 'all' or plot_selection == 'digital':
                bp4 = BodePlot(title=f'{ifo} DARM Digital Filter: D', figsize=figsize)
                list_of_figures.append(plt.gcf())
            if plot_selection == 'all' or plot_selection == 'optical':
                bp5 = BodePlot(title=f'{ifo} Optical Plant Response: C', figsize=figsize)
                list_of_figures.append(plt.gcf())
            if plot_selection == 'all' or plot_selection == 'actuation':
                bp6 = BodePlot(title=f'{ifo} Act. stage strength', figsize=figsize)
                list_of_figures.append(plt.gcf())
                bp7 = BodePlot(title=f'{ifo} Act. stage digital filters', figsize=figsize)
                list_of_figures.append(plt.gcf())
                bp8 = BodePlot(title=f'{ifo} Act. stage LOCK_IN to Displ.', figsize=figsize)
                list_of_figures.append(plt.gcf())
                bp9 = BodePlot(title=f'{ifo} Act. stage LOCK_IN to Displ. (low zoom)',
                               figsize=figsize)
                list_of_figures.append(plt.gcf())
                bp10 = BodePlot(title=f'{ifo} Act. stage LOCK_IN to Displ. (high zoom)',
                                figsize=figsize)
                list_of_figures.append(plt.gcf())
                bp11 = BodePlot(title=f'{ifo} Act. stage DARM_IN to Disp. (D*A)', figsize=figsize)
                list_of_figures.append(plt.gcf())
                bp12 = BodePlot(title=f'{ifo} Act. stage relative contributions', figsize=figsize,
                                only='magnitude')
                list_of_figures.append(plt.gcf())

        ugf_freq, phase_margin = get_ugf(freq, G, search_start=ugf_start, search_end=ugf_end)
        phase_margin = 180+phase_margin

        if plot_selection == 'all' or plot_selection == 'olg':
            bp1.plot(freq, G, **kwargs)
            if label:
                bp1.legend(label)
            bp1.xlim(freq_min, freq_max)
            if greed:
                bp1.greed()
            bp1.vlines(ugf_freq)
            bp1.text(freq_min*1.1, 1.1*10**(-(temp_model_index)),
                     f'UGF {temp_model_index} = {ugf_freq}Hz, {phase_margin}deg')
            temp_bottom, temp_top = bp1.ax_mag.get_ylim()
            bp1.ylim(temp_top/default_olg_yspan, temp_top)

        if plot_selection == 'all':
            bp2.plot(freq, G, **kwargs)
            if label:
                bp2.legend(label)
            bp2.xlim(default_olg_zoom_fmin, default_olg_zoom_fmax)
            if greed:
                bp2.greed()
            bp2.vlines(ugf_freq)
            bp2.text(default_olg_zoom_fmin*1.04, 10**((1-temp_model_index)/8),
                     f'UGF {temp_model_index} = {ugf_freq}Hz, {phase_margin}deg')

        if plot_selection == 'all' or plot_selection == 'clg':
            bp3.plot(freq, 1./(1.+G), **kwargs)
            bp3b.plot(freq, 1./(1.+G), **kwargs)
            if label:
                bp3.legend(label)
                bp3b.legend(label)
            bp3.xlim(freq_min, freq_max)
            bp3b.xlim(default_clg_zoom_fmin, default_clg_zoom_fmax)
            if greed:
                bp3.greed()
                bp3b.greed()

        if plot_selection == 'all' or plot_selection == 'digital':
            bp4.plot(freq, D, **kwargs)
            if label:
                bp4.legend(label)
            bp4.xlim(freq_min, freq_max)
            if greed:
                bp4.greed()
            temp_bottom, temp_top = bp4.ax_mag.get_ylim()
            bp4.ylim(temp_top/default_dig_yspan, temp_top)

        if plot_selection == 'all' or plot_selection == 'optical':
            bp5.plot(freq, C, **kwargs)
            if label:
                bp5.legend(label)
            bp5.xlim(freq_min, freq_max)
            if greed:
                bp5.greed()

        if plot_selection == 'all' or plot_selection == 'actuation':
            if temp_model_index == 2:
                bp6.plot(freq, x_UIM_strength, ls='--')
                bp6.plot(freq, x_PUM_strength, ls='--')
                bp6.plot(freq, x_TST_strength, ls='--')
            else:
                bp6.plot(freq, x_UIM_strength, **kwargs)
                bp6.plot(freq, x_PUM_strength, **kwargs)
                bp6.plot(freq, x_TST_strength, **kwargs)
                bp6.ax_mag.set_prop_cycle(None)
                bp6.ax_phase.set_prop_cycle(None)
            bp6.xlim(freq_min, freq_max)
            temp_bottom, temp_top = bp6.ax_mag.get_ylim()
            bp6.ylim(temp_top/default_act_strength_yspan, temp_top)

            if greed:
                bp6.greed()

            if temp_model_index == 2:
                bp7.plot(freq, x_UIM_umodel, ls='--')
                bp7.plot(freq, x_PUM_umodel, ls='--')
                bp7.plot(freq, x_TST_umodel, ls='--')
            else:
                bp7.plot(freq, x_UIM_umodel, **kwargs)
                bp7.plot(freq, x_PUM_umodel, **kwargs)
                bp7.plot(freq, x_TST_umodel, **kwargs)
                bp7.ax_mag.set_prop_cycle(None)
                bp7.ax_phase.set_prop_cycle(None)
            bp7.xlim(freq_min, freq_max)

            if greed:
                bp7.greed()

            if temp_model_index == 2:
                bp8.plot(freq, x_UIM_authority, ls='--')
                bp8.plot(freq, x_PUM_authority, ls='--')
                bp8.plot(freq, x_TST_authority, ls='--')
                bp8.plot(freq, x_ALL_authority, ls='--')
            else:
                bp8.plot(freq, x_UIM_authority, **kwargs)
                bp8.plot(freq, x_PUM_authority, **kwargs)
                bp8.plot(freq, x_TST_authority, **kwargs)
                bp8.plot(freq, x_ALL_authority, **kwargs)
                bp8.ax_mag.set_prop_cycle(None)
                bp8.ax_phase.set_prop_cycle(None)
            bp8.xlim(freq_min, freq_max)
            temp_bottom, temp_top = bp8.ax_mag.get_ylim()
            bp8.ylim(temp_top/default_act_displ_yspan, temp_top)

            if greed:
                bp8.greed()

            if temp_model_index == 2:
                bp9.plot(freq, x_UIM_authority, ls='--')
                bp9.plot(freq, x_PUM_authority, ls='--')
                bp9.plot(freq, x_TST_authority, ls='--')
                bp9.plot(freq, x_ALL_authority, ls='--')
            else:
                bp9.plot(freq, x_UIM_authority, **kwargs)
                bp9.plot(freq, x_PUM_authority, **kwargs)
                bp9.plot(freq, x_TST_authority, **kwargs)
                bp9.plot(freq, x_ALL_authority, **kwargs)
                bp9.ax_mag.set_prop_cycle(None)
                bp9.ax_phase.set_prop_cycle(None)
            bp9.xlim(1e-1, 1e2)

            if greed:
                bp9.greed()

            if temp_model_index == 2:
                bp10.plot(freq, x_UIM_authority, ls='--')
                bp10.plot(freq, x_PUM_authority, ls='--')
                bp10.plot(freq, x_TST_authority, ls='--')
                bp10.plot(freq, x_ALL_authority, ls='--')
            else:
                bp10.plot(freq, x_UIM_authority, **kwargs)
                bp10.plot(freq, x_PUM_authority, **kwargs)
                bp10.plot(freq, x_TST_authority, **kwargs)
                bp10.plot(freq, x_ALL_authority, **kwargs)
                bp10.ax_mag.set_prop_cycle(None)
                bp10.ax_phase.set_prop_cycle(None)
            bp10.xlim(1e2, 1e3)

            if greed:
                bp10.greed()

            if temp_model_index == 2:
                bp11.plot(freq, x_UIM_total, ls='--')
                bp11.plot(freq, x_PUM_total, ls='--')
                bp11.plot(freq, x_TST_total, ls='--')
                bp11.plot(freq, (x_UIM_total+x_PUM_total+x_TST_total), ls='--')
            else:
                bp11.plot(freq, x_UIM_total, **kwargs)
                bp11.plot(freq, x_PUM_total, **kwargs)
                bp11.plot(freq, x_TST_total, **kwargs)
                bp11.plot(freq, (x_UIM_total+x_PUM_total+x_TST_total), **kwargs)
                bp11.ax_mag.set_prop_cycle(None)
                bp11.ax_phase.set_prop_cycle(None)
            bp11.xlim(freq_min, freq_max)
            temp_bottom, temp_top = bp11.ax_mag.get_ylim()
            bp11.ylim(temp_top/default_act_displ_yspan, temp_top)

            if greed:
                bp11.greed()

            if temp_model_index == 2:
                bp12.plot(freq, x_UIM_rel, ls='--')
                bp12.plot(freq, x_PUM_rel, ls='--')
                bp12.plot(freq, x_TST_rel, ls='--')
                bp12.plot(freq, x_ALL_rel, ls='--')
                bp12.plot(freq, invCnorm, ls='--')
            else:
                bp12.plot(freq, x_UIM_rel, **kwargs)
                bp12.plot(freq, x_PUM_rel, **kwargs)
                bp12.plot(freq, x_TST_rel, **kwargs)
                bp12.plot(freq, x_ALL_rel, **kwargs)
                bp12.plot(freq, invCnorm, **kwargs)
                bp12.ax_mag.set_prop_cycle(None)
                # bp12.ax_phase.set_prop_cycle(None)
            bp12.xlim(5, 1000)
            bp12.ylim(1e-3, 4e0)

            if greed:
                bp12.greed()

        if label:
            if plot_selection == 'all' or plot_selection == 'actuation':
                combined_model_label = []
                for labels in label:
                    combined_model_label.append(labels+' UIM')
                    combined_model_label.append(labels+' PUM')
                    combined_model_label.append(labels+' TST')
                bp6.legend(combined_model_label)
                bp7.legend(combined_model_label)
                combined_model_label_tot = []
                for labels in label:
                    combined_model_label_tot.append(labels+' UIM')
                    combined_model_label_tot.append(labels+' PUM')
                    combined_model_label_tot.append(labels+' TST')
                    combined_model_label_tot.append(labels+' Total')
                bp8.legend(combined_model_label_tot)
                bp9.legend(combined_model_label_tot)
                bp10.legend(combined_model_label_tot)
                bp11.legend(combined_model_label_tot)
                combined_model_label_tot = []
                for labels in label:
                    combined_model_label_tot.append(labels+' UIM*D/R')
                    combined_model_label_tot.append(labels+' PUM*D/R')
                    combined_model_label_tot.append(labels+' TST*D/R')
                    combined_model_label_tot.append(labels+' Total')
                    combined_model_label_tot.append(labels+' 1/C')
                bp12.legend(combined_model_label_tot)
        else:
            if plot_selection == 'all' or plot_selection == 'actuation':
                combined_model_label = []
                combined_model_label.append('UIM')
                combined_model_label.append('PUM')
                combined_model_label.append('TST')
                bp6.legend(combined_model_label)
                bp7.legend(combined_model_label)
                combined_model_label_tot = []
                combined_model_label_tot.append('UIM')
                combined_model_label_tot.append('PUM')
                combined_model_label_tot.append('TST')
                combined_model_label_tot.append('Total')
                bp8.legend(combined_model_label_tot)
                bp9.legend(combined_model_label_tot)
                bp10.legend(combined_model_label_tot)
                bp11.legend(combined_model_label_tot)
                combined_model_label_tot = []
                combined_model_label_tot.append('UIM*D/R')
                combined_model_label_tot.append('PUM*D/R')
                combined_model_label_tot.append('TST*D/R')
                combined_model_label_tot.append('Total*D/R')
                combined_model_label_tot.append('1/C')
                bp12.legend(combined_model_label_tot)
        temp_model_index = temp_model_index+1

    if filename:
        save_multifig(filename, list_of_figures)
    if show:
        plt.show()
