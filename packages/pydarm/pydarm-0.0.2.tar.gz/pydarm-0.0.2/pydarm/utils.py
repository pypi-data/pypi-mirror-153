# Copyright (C) Evan Goetz (2021)
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

from scipy import signal
import numpy as np
from numpy.polynomial import polynomial as P
from collections import namedtuple
import re
import h5py

cds_filter = namedtuple('cds_filter', ['name', 'soscoef', 'fs', 'design'])
cds_filter_bank = namedtuple('cds_filter_bank',
                             ['name', 'filters', 'headerAndBody'])


def serielZPK(sys1, sys2):
    """Multiply two ZPK filters together as though they were in a seriel path

    Parameters
    ----------
    sys1 : :obj:`scipy.signal.ZerosPolesGain`
        First filter object
    sys2 : :obj:`scipy.signal.ZerosPolesGain`
        Second filter object

    Returns
    -------
    sys : :obj:`scipy.signal.ZerosPolesGain`
        Combined filter object

    Examples
    --------
    >>> out = serielZPK(in1, in2)
    """

    sys = sys1.to_zpk()
    sys.zeros = np.append(sys1.zeros, sys2.zeros)
    sys.poles = np.append(sys1.poles, sys2.poles)
    sys.gain *= sys2.gain
    return sys


def parallelZPK(sys1, sys2):
    """Add two ZPK filters together as though they were
    in parallel paths and summed

    Parameters
    ----------
    sys1 : :obj:`scipy.signal.ZerosPolesGain`
        First filter object
    sys2 : :obj:`scipy.signal.ZerosPolesGain`
        Second filter object

    Returns
    -------
    sys : :obj:`scipy.signal.ZerosPolesGain`
        Combined filter object

    Examples
    --------
    >>> out = parallelZPK(in1, in2)
    """

    # Need to add the paths together. Do this using polynomials
    # from roots and polynomial add.
    # Note that polyfromroots and polyadd have increasing exponent
    # order while TransferFunction needs descending exponent order
    numerator_poly = np.flip(P.polyadd(sys1.gain * P.polyfromroots(
                             np.append(sys1.zeros, sys2.poles)),
                             sys2.gain * P.polyfromroots(
                                 np.append(sys2.zeros, sys1.poles))), 0)
    denominator_poly = np.flip(
        P.polyfromroots(np.append(sys1.poles, sys2.poles)), 0)
    systf = signal.TransferFunction(numerator_poly, denominator_poly)
    syszpk = systf.to_zpk()
    return syszpk


def freqrespZPK(sys, w):
    """Compute the frequency response of a continuous ZPK filter

    Parameters
    ----------
    sys : :obj:`scipy.signal.ZerosPolesGain`
        Filter object
    w : `float`, array-like
        Angular frequencies at which to compute the filter response

    Returns
    -------
    g : `complex128`, array-like
        Filter response

    Examples
    --------
    >>> filt = signal.ZerosPolesGain(-2.0*np.pi*np.asarray([1.]),
                   -2.0*np.pi*np.asarray([20.]), 20.0/1.0)
    >>> out = freqrespZPK(filt, 2.0*np.pi*np.logspace(0, 3, 100))
    """

    s = s = 1j * np.complex128(w)
    numPoles = len(sys.poles)
    g = sys.gain * np.ones(len(w), dtype='complex128')

    sortedPolesIdx = np.argsort(abs(sys.poles))
    sortedZerosIdx = np.argsort(abs(sys.zeros))

    for i in range(0, numPoles):
        if i < len(sys.zeros):
            tmp = s - sys.zeros[sortedZerosIdx[i]]
        else:
            tmp = 1
        g = g * tmp / (s - sys.poles[sortedPolesIdx[i]])

    return g


def dfreqrespZPK(sys, w):
    """Compute the frequency response of a discrete ZPK filter

    Note that  control room computers don't have the latest
    scipy so this is brought from scipy>=0.19.0. It
    basically does the same as freqz_zpk():

    Parameters
    ----------
    sys : :obj:`scipy.signal.ZerosPolesGain`
        Filter object
    w : `float`, array-like
        Angular frequencies at which to compute the filter response

    Returns
    -------
    w : `float`, array-like
        Angular frequencies at which to compute the filter response
    h : `complex128`, array-like
        Filter response

    Examples
    --------
    >>> filt = signal.ZerosPolesGain(-2.0*np.pi*np.asarray([1.]),
                   -2.0*np.pi*np.asarray([20.]), 20.0/1.0, 1.0/16384)
    >>> out = dfreqrespZPK(filt, 2.0*np.pi*np.logspace(0, 3, 100))
    """

    zm1 = np.exp(1j * w)
    h = sys.gain * P.polyvalfromroots(zm1, sys.zeros) / \
        P.polyvalfromroots(zm1, sys.poles)

    return w, h


def digital_delay_filter(clock_cycles, sample_frequency):
    """Compute a digital delay filter

    Parameters
    ----------
    clock_cycles : `int`
        Number of cycles delay with sample_frequency
    sample_frequency : `int`
        Sampling frequency

    Returns
    -------
    filter : :obj:`scipy.signal.ZerosPolesGain`
        Zeros poles gain object
    """
    return signal.ZerosPolesGain([], np.zeros(clock_cycles), 1,
                                 dt=1.0/sample_frequency)


# Copy of scipy normalize() for tf2zp with smaller tolerance
def normalize(b, a):
    num, den = b, a

    den = np.atleast_1d(den)
    num = np.atleast_2d(_align_nums(num))

    if den.ndim != 1:
        raise ValueError("Denominator polynomial must be rank-1 array.")
    if num.ndim > 2:
        raise ValueError("Numerator polynomial must be rank-1 or"
                         " rank-2 array.")
    if np.all(den == 0):
        raise ValueError("Denominator must have at least on nonzero element.")

    # Trim leading zeros in denominator, leave at least one.
    den = np.trim_zeros(den, 'f')

    # Normalize transfer function
    num, den = num / den[0], den / den[0]

    # Count numerator columns that are all zero
    leading_zeros = 0
    for col in num.T:
        if np.allclose(col, 0, atol=1e-32):  # smaller tolerance value
            leading_zeros += 1
        else:
            break

    # Trim leading zeros of numerator
    if leading_zeros > 0:
        print("Badly conditioned filter coefficients (numerator): the "
              "results may be meaningless")
        # Make sure at least one column remains
        if leading_zeros == num.shape[1]:
            leading_zeros -= 1
        num = num[:, leading_zeros:]

    # Squeeze first dimension if singular
    if num.shape[0] == 1:
        num = num[0, :]

    return num, den


# Copy of what scipy does - we need this for tf2zp
def _align_nums(nums):
    try:
        # The statement can throw a ValueError if one
        # of the numerators is a single digit and another
        # is array-like e.g. if nums = [5, [1, 2, 3]]
        nums = np.asarray(nums)

        if not np.issubdtype(nums.dtype, np.number):
            raise ValueError("dtype of numerator is non-numeric")

        return nums

    except ValueError:
        nums = [np.atleast_1d(num) for num in nums]
        max_width = max(num.size for num in nums)

        # pre-allocate
        aligned_nums = np.zeros((len(nums), max_width))

        # Create numerators with padded zeros
        for index, num in enumerate(nums):
            aligned_nums[index, -num.size:] = num

        return aligned_nums


# Copy of what scipy.signal.tf2zpk() does. Needed a lower tolerance value
# inside normalize()
def tf2zp(b, a):
    b, a = normalize(b, a)
    b = (b + 0.0) / a[0]
    a = (a + 0.0) / a[0]
    k = b[0]
    b /= b[0]
    z = np.roots(b)
    p = np.roots(a)
    return z, p, k


def sos2zp(sos):
    """
    Replicate the MATLAB version of sos2zp because the scipy version is
    not like the MATLAB version

    Parameters
    ----------
    sos : `float`, array-like
        Second order sections

    Returns
    -------
    z : `float`
        Zeros of the ZPK filter
    p : `float`, array-like
    """

    sos = np.atleast_2d(np.asarray(sos))
    n_sections = sos.shape[0]
    z = np.empty(0, np.complex128)
    p = np.empty(0, np.complex128)
    k = 1
    for section in range(n_sections):
        if sos[section, 5] == 0 and sos[section, 2] == 0:
            b = sos[section, 0:2]
            a = sos[section, 3:5]
        else:
            b = sos[section, 0:3]
            a = sos[section, 3:6]
        if b[-1] == 0 and a[-1] == 0:
            b = b[0]
            a = a[0]
        # [zt,pt,kt] = signal.tf2zpk(b,a)
        # Use our own tf2zp because the scipy version has a very tight
        # tolerance on coefficients
        [zt, pt, kt] = tf2zp(b, a)
        z = np.append(z, zt)
        p = np.append(p, pt)
        k *= kt
    return z, p, k


def compute_digital_filter_response(filter_filename, filter_bank_name,
                                    filter_bank_modules, filter_bank_gain,
                                    frequencies, pfilt=None):
    """
    Compute a digital filter ZPK transfer function response from a
    Foton file

    Parameters
    ----------
    filter_filename : str
        Path to file and filename of Foton filter file
    filter_bank_name : str
        Name of the filter bank
    filter_bank_modules : int, array-like
        filter modules requested from the bank, from 1 .. 10
    filter_bank_gain : float
        Digital gain of the filter bank
    frequencies : float, array-like
        Array of frequencies (in Hz) for the transfer function
    pfilt : array-like (optional)
        Use this as input when reading from the same Foton filter file
        multiple times. pfilt can be passed back in because it has all the
        file stored in the namedtuple

    Returns
    -------
    tf : `complex128`, array-like
        transfer function response of the digital SUS filter
    pfilt : array-like
        The Foton file is stored in this array for later re-use
    """

    if pfilt is None:
        pfilt = []

    sysd, pfilt = read_filter_sys(filter_filename, filter_bank_name,
                                  filter_bank_modules, data=pfilt)
    sysd.gain *= filter_bank_gain

    tf = signal.dfreqresp(sysd, 2.0*np.pi*frequencies*sysd.dt)[1]

    return tf, pfilt


def read_filter_sys(filename, bank, module, **kwargs):
    """
    Read a filter system from a file and return a ZPK filter and pfilt
    (a structure containing the filter info from the file)

    Parameters
    ----------
    filename : `str`
        Path and filename of FOTON filter file
    bank : `str`
        Name of the filter bank
    module : `int`, array-like
        Module numers ranging from 1 to 10
    data : array-like, optional
        Array containing [filename, filter .. filter]. This is passed as an
        optional argument in case the file has already been read once and you
        don't want to spend more I/O time re-reading this again

    Returns
    -------
    sysd : :obj:`scipy.signal.ZerosPolesGain`
        ZPK object of the requested FOTON filters
    pfilt : array-like
        Data from the FOTON filter file.
        Passing this back to the same function speeds up searching more
        filters in the file
    """

    if len(module) == 0:
        sysd = signal.ZerosPolesGain([], [], 1, dt=1.0/2**14)
        if len(kwargs) > 0 and kwargs['data']:
            pfilt = kwargs['data']
        else:
            pfilt = []
    else:
        if len(kwargs) == 0 or not kwargs['data']:
            pfilt = read_filter_file(filename)
        elif len(kwargs) > 0 and kwargs['data']:
            pfilt = kwargs['data']
            if not re.match(filename, pfilt[0]):
                raise ValueError('Wrong filter filename when using optional \
                                 data input')
        filterbank_index = 1
        while (filterbank_index < len(pfilt) and not
               re.fullmatch(bank, pfilt[filterbank_index].name)):
            filterbank_index += 1
        if filterbank_index >= len(pfilt):
            raise ValueError(f'There was no bank with name {bank} in the filter \
                             file {pfilt[0]}')
        fs = pfilt[filterbank_index].filters[module[0]-1].fs
        sysd = signal.ZerosPolesGain([], [], 1, dt=1.0/fs)
        for n in range(0, len(module)):
            index = module[n] - 1
            # removed because this because it is not like Matlab
            # [zd,pd,kd] = signal.sos2zpk(\
            #     pfilt[filterbank_index].filters[index].soscoef)
            # This follows the Matlab function sos2zp()
            [z, p, k] = sos2zp(pfilt[filterbank_index].filters[index].soscoef)
            sysd.zeros = np.append(sysd.zeros, z)
            sysd.poles = np.append(sysd.poles, p)
            sysd.gain *= k
    return sysd, pfilt


def read_filter_file(filename):
    """
    Read a filter file and return all the SOS coefficients info for the filters

    Parameters
    ----------
    filename : `str`
        Path and filename of FOTON filter file

    Returns
    -------
    out : array-like
        Data from the FOTON filter file
    """
    out = [filename]
    with open(filename) as file:
        for line in file:
            line = line.rstrip()
            if (re.match('^#', line) and len(line) > 2 and not
                    re.match(r'^### \w+', line)):
                if re.search('MODULES', line):
                    line_el = line.split(' ')
                    for n in range(2, len(line_el)):
                        new_filter_bank = \
                            cds_filter_bank(line_el[n], [cds_filter]*10, False)
                        for m in range(0, 10):
                            new_filter_bank.filters[m] = \
                              cds_filter('empty', np.array([1, 0, 0, 1, 0, 0]),
                                         16384, '<none>')
                        out.append(new_filter_bank)
                elif re.search('SAMPLING', line):
                    line_el = line.split(' ')
                    if line_el[2] == 'RATE':
                        for n in range(1, len(out)):
                            for m in range(0, 10):
                                out[n].filters[m] = \
                                    out[n].filters[m]._replace(
                                        fs=int(line_el[3]))
                elif re.search('DESIGN', line):
                    line_el = line.split()
                    fname = line_el[2]
                    index = int(line_el[3])
                    design_str = line_el[4]
                    while line_el[len(line_el)-1] == '\\':
                        line = next(file)
                        line_el = line.split()
                        if len(line_el) == 1:
                            break
                        else:
                            design_str += line_el[1]
                    filterbank_index = 1
                    while not re.fullmatch(fname, out[filterbank_index].name):
                        filterbank_index += 1
                    out[filterbank_index].filters[index] = \
                        out[filterbank_index].filters[index]._replace(
                            design=design_str)
            elif re.match(r'^### \w+', line):
                line_el = line.split()
                fname = line_el[1]
                filterbank_index = 1
                while (filterbank_index < len(out)-1 and
                       fname != out[filterbank_index].name):
                    filterbank_index += 1
                if fname == out[filterbank_index].name:
                    out[filterbank_index] = \
                        out[filterbank_index]._replace(headerAndBody=True)
            elif len(line.split()) == 12:
                line_el = line.split()
                fname = line_el[0]
                index = int(line_el[1])
                mname = line_el[6]
                gain = float(line_el[7])
                sos_coeff_lines = int(line_el[3])
                soscoeffs = np.ones((sos_coeff_lines, 6))
                for n in range(0, sos_coeff_lines):
                    if n == 0:
                        soscoeffs[n, 1] = float(line_el[10])
                        soscoeffs[n, 2] = float(line_el[11])
                        soscoeffs[n, 4] = float(line_el[8])
                        soscoeffs[n, 5] = float(line_el[9])
                    else:
                        line = next(file)
                        line_el = line.split()
                        soscoeffs[n, 1] = float(line_el[2])
                        soscoeffs[n, 2] = float(line_el[3])
                        soscoeffs[n, 4] = float(line_el[0])
                        soscoeffs[n, 5] = float(line_el[1])
                soscoeffs[0, :] = np.multiply(
                    soscoeffs[0, :], np.array([gain, gain, gain, 1, 1, 1]))
                filterbank_index = 1
                while not re.fullmatch(fname, out[filterbank_index].name):
                    filterbank_index += 1
                out[filterbank_index].filters[index] = \
                    out[filterbank_index].filters[index]._replace(name=mname)
                out[filterbank_index].filters[index] = \
                    out[filterbank_index].filters[index]._replace(
                        soscoef=soscoeffs)

    for n in range(1, len(out)-1):
        if not out[n].headerAndBody:
            raise ValueError(f'Header contains module {out[n].name} but does \
                             not exist in body')

    return out


def load_foton_export_tf(filename):
    """
    This function is designed to take a filename and load the data.
    The filename must be an ASCII file with three columns:
    frequency, real term, imaginary term (I think this is the
    default export behavior of FOTON)

    Parameters
    ----------
    filename : `str`
        full path and filename to the ASCII export of FOTON data

    Returns
    -------
    file_data_freq : `float`, array-like
        frequency array of the data in the file in units of Hz
    file_data_response : `complex128`, array-like
        transfer function data of the FOTON filter
    """

    file_data = np.loadtxt(filename)
    file_data_freq = file_data[:, 0]
    file_data_response = file_data[:, 1] + 1j*file_data[:, 2]

    return file_data_freq, file_data_response


def save_chain_to_hdf5(filename, meas_model, fmin, fmax, measurement, chain):
    """
    Save the MCMC chain to an HDF5 file

    Parameters
    ----------
    filename : str
        Output filename
    meas_model : str
        Configuration string for the model
    fmin : float
        Minimum frequency used in the MCMC fit
    fmax : float
        Maximum frequency used in the MCMC fit
    measurement : str
        Either 'sensing' or 'actuation'
    chain : `float`, array-like
        The MCMC chain
    """

    with h5py.File(filename, 'w') as f:
        f.create_dataset('measurement_model', data=str(meas_model))
        f.create_dataset('fmin', data=fmin)
        f.create_dataset('fmax', data=fmax)
        f.create_dataset('measurement', data=str(measurement))
        f.create_dataset('posteriors', data=chain)

    return


def read_chain_from_hdf5(filename):
    """
    Read the MCMC chain from an HDF5 file

    Parameters
    ----------
    filename : str
        HDF5 filename

    Returns
    -------
    meas_model : str
        Configuration string for the model
    fmin : float
        Minimum frequency used in the MCMC fit
    fmax : float
        Maximum frequency used in the MCMC fit
    measurement : str
        Either 'sensing' or 'actuation'
    chain : `float`, array-like
        The MCMC chain
    """

    with h5py.File(filename, 'r') as f:
        meas_model = f.get('measurement_model')[()].decode('utf-8')
        fmin = f.get('fmin')[()]
        fmax = f.get('fmax')[()]
        measurement = f.get('measurement')[()].decode('utf-8')
        chain = f.get('posteriors')[()]

    return meas_model, fmin, fmax, measurement, chain


def save_gpr_to_hdf5(filename, meas_model, measurement, y_pred, cov,
                     frequencies):
    """
    Save GPR results to an HDF5 file

    Parameters
    ----------
    filename : str
        Output filename
    meas_model : str
        Configuration string for the model
    measurement : str
        Either 'sensing' or 'actuation'
    y_pred : `complex128`, array-like
        Best fit curve using the GPR and covariance kernel
    cov : `float`, array-like
        Covariance matrix for the GPR
    frequencies : `float`, array-like
        Array of frequencies the GPR is valid for
    """
    with h5py.File(filename, 'w') as f:
        if measurement == 'sensing' or 'actuation' in measurement:
            group = f.create_group(measurement)
        else:
            raise ValueError('measurement option must specify sensing \
                              or type of actuation; e.g., actuation_x_pum')
        group.create_dataset('measurement_model', data=str(meas_model))
        group.create_dataset('GPR_MAP', data=y_pred)
        group.create_dataset('GPR_covariance', data=cov)
        group.create_dataset('frequencies', data=frequencies)


def read_gpr_from_hdf5(filename, measurement):
    """
    Read GPR results from an HDF5 file

    Parameters
    ----------
    filename : str
        Output filename
    measurement : str
        Either 'sensing' or 'actuation'

    Returns
    -------
    meas_model : str
        Configuration string for the model
    y_pred : `complex128`, array-like
        Best fit curve using the GPR and covariance kernel
    cov : `float`, array-like
        Covariance matrix for the GPR
    frequencies : `float`, array-like
        Array of frequencies the GPR is valid for
    """
    with h5py.File(filename, 'r') as f:
        assert measurement == list(f.keys())[0], f'{measurement} is not an hdf5 group in {filename}'

        meas = f.get(measurement)
        meas_model = meas.get('measurement_model')[()].decode('utf-8')
        y_pred = meas.get('GPR_MAP')[()]
        cov = meas.get('GPR_covariance')[()]
        frequencies = meas.get('frequencies')[()]

    return meas_model, y_pred, cov, frequencies
