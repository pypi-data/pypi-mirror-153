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

from scipy import signal, io
import numpy as np


def analog_aa_or_ai_filter_response(mat_file, frequencies):
    """
    This comes from an export of a Matlab LTI object which was a fit of
    measurements made at LHO and LLO by JeffK, JoeB, et al. The object has
    zeros, poles, gain, and a delay, so the exported mat-file has the arrays
    of zeros and poles, gain, and delay in the file. Measurements were made
    around ER7. TODO: find alog entries?

    Parameters
    ----------
    mat_file : `str`
        path and filename of the Matlab mat-file export
    frequencies : `float`, array-like
        array of frequencies to compute the response

    Returns
    -------
    tf : `complex128`, array-like
        transfer function response of the analog AA or AI filter
    """

    mat = io.loadmat(mat_file)
    analog_aa_or_ai_zpk = signal.ZerosPolesGain(mat['AAzeros'][:, 0],
                                                mat['AApoles'][:, 0],
                                                mat['AAgain'][0, 0])
    analog_aa_or_ai_delay = np.exp(
        -2.0*np.pi*mat['AAdelay'][0, 0]*1j*frequencies)

    return signal.freqresp(analog_aa_or_ai_zpk,
                           2.0*np.pi*frequencies)[1] * analog_aa_or_ai_delay
