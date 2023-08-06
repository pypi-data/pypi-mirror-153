# Copyright (C) Jameson Rollins (2021)
#               Evan Goetz (2021)
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

import os
import signal
import logging
import argparse

import numpy as np

from . import __version__
from .darm import DARMModel


logger = logging.getLogger('pydarm')
logger.setLevel(os.getenv('LOG_LEVEL', 'WARNING').upper())
formatter = logging.Formatter('%(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


########################################

DEFAULT_FREQ = '0.01:5000:3000'

DATA_SAVE_FORMATS = ['.hdf5', '.h5']


def freq_from_spec(spec=None):
    """logarithmicly spaced frequency array, based on specification string

    Specification string should be of form 'START:[NPOINTS:]STOP'.  If
    `spec` is an array, then the array is returned as-is, and if it's
    None the DEFAULT_FREQ specification is used.

    """
    if isinstance(spec, np.ndarray):
        return spec
    elif spec is None:
        spec = DEFAULT_FREQ
    fspec = spec.split(':')
    if len(fspec) == 2:
        fspec = fspec[0], DEFAULT_FREQ.split(':')[1], fspec[1]
    return np.logspace(
        np.log10(float(fspec[0])),
        np.log10(float(fspec[2])),
        int(fspec[1]),
    )


########################################

parser = argparse.ArgumentParser(
    description="""pyDARM calibration modelling

""",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument(
    '--version', '-v', action='version', version=__version__)
subparsers = parser.add_subparsers(
    metavar='COMMAND',
)


def _subcommand(func, **kwargs):
    """helper function for adding a new subcommand to the parser

    This function helps in adding sub-commands to the argparse
    ArgumentParser.  The code to .

    Each sub-command should be encoded as a function, with
    arguments/options mapped to function keyword arguments.  The
    function docstring will be used as the sub-command description,
    with first line used as the help.  Additional keyword arguments
    are passed to the add_parser method.

    The subparser itself will be returned, and it's add_argument()
    method should be used to add arguments and options to the
    sub-command.

    The main() function below handles the parsing of arguments, and
    executing the sub-command function with the the arguments/options
    passed in as keyword arguments.

    """
    name = func.__name__.split('_')[1]
    sp = subparsers.add_parser(
        name,
        help=func.__doc__.splitlines()[0],
        description=func.__doc__.strip(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        **kwargs
    )
    sp.set_defaults(func=func)
    return sp

##########


def cmd_fr(model, freq, plot=True, save=False):
    """calculate model frequency response and plot

    """
    import h5py
    from matplotlib import pyplot as plt

    from .plot import BodePlot

    out_data_files = set()
    out_plot_files = set()
    if save:
        plot = False
        out_files = set(save)
        for path in out_files:
            if os.path.splitext(path)[1] in DATA_SAVE_FORMATS:
                out_data_files.add(path)
        out_plot_files = out_files - out_data_files

    ##########

    if os.path.splitext(model)[1] in DATA_SAVE_FORMATS:
        with h5py.File(model) as f:
            title = f.attrs.get('title', '')
            freq = f['Frequency'][:]
            G = f['Data']['DARM'][:]
            R = f['Data']['Response'][:]
            C = f['Data']['Sensing'][:]
            A = f['Data']['Actuation'][:]
            D = f['Data']['Digital'][:]

    else:
        freq = freq_from_spec(freq)
        DARM = DARMModel(model)
        title = f'{DARM.name} {DARM.run} {DARM.model_date}'
        G = DARM.compute_darm_olg(freq)
        R = DARM.compute_response_function(freq)
        C = DARM.sensing.compute_sensing(freq)
        A = DARM.actuation.compute_actuation(freq)
        D = DARM.digital.compute_response(freq)

    if plot or out_plot_files:
        bp = BodePlot(title=title)
        bp.plot(
            freq, G,
            label='DARM',
        )
        bp.plot(
            freq, C,
            label='Sensing',
            linestyle='--',
        )
        bp.plot(
            freq, A,
            label='Actuation',
            linestyle='--',
        )
        bp.plot(
            freq, D,
            label='Digital',
            linestyle='--',
        )
        bp.plot(
            freq, R,
            label='Response',
        )
        bp.legend()

        if out_plot_files:
            for path in out_plot_files:
                logger.info(f'saving plot: {path}')
                try:
                    bp.save(path)
                except Exception as e:
                    parser.exit(2, f'Error saving plot: {e}.\n')
        else:
            plt.show()

    if out_data_files:
        for path in out_data_files:
            logger.info(f'saving frequency response data: {path}')
            with h5py.File(path, 'w') as f:
                f.attrs['title'] = title
                f.create_dataset('Frequency', data=freq)
                g = f.create_group('Data')
                g.create_dataset('DARM', data=G)
                g.create_dataset('Sensing', data=C)
                g.create_dataset('Actuation', data=A)
                g.create_dataset('Digital', data=D)
                g.create_dataset('Response', data=R)


sp = _subcommand(cmd_fr, aliases=['plot'])
sp.add_argument(
    'model', metavar='MODEL',
    help='model INI config file, or hdf5 frequency response data')
sp.add_argument(
    '--freq', '-f', metavar='FLO:[NPOINTS:]FHI',
    help=f'logarithmic frequency array specification in Hz [{DEFAULT_FREQ}]')
group = sp.add_mutually_exclusive_group()
group.add_argument(
    '--save', '-s', metavar='PATH', action='append',
    help=("save plot (.png/.pdf/.svg) or response data (.hdf5/.h5) to file"
          "(may be specified multiple times)"))
group.add_argument(
    '--no-plot', '-np', action='store_false', dest='plot',
    help="suppress plotting")


########################################


def main():
    args = parser.parse_args()
    logger.debug(args)
    if 'func' not in args:
        parser.print_help()
        parser.exit()
    kwargs = dict(args._get_kwargs())
    del kwargs['func']
    args.func(**kwargs)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
