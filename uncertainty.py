from logging import ERROR
import numpy as np
import pandas as pd
from uncertainties.core import sqrt

def studentFuncError(array, weights=None, sigma=1):
    """
    Gives the error of an array of numbers according to the Student's
    Function for a limited amount of samples using the numpy and pandas
    libraries.
    """
    t = [
        (1.84, 1.32, 1.20, 1.15, 1.11, 1.08, 1.06, 1.03, 1.02, 1.01, 1.0, 1.0),
        (13.97, 4.53, 3.31, 2.87, 2.65, 2.43, 2.32, 2.14, 2.09, 2.05, 2.03, 2.01),
        (235.8, 19.21, 9.22, 6.62, 5.51, 4.53, 4.09, 3.45, 3.28, 3.16, 3.08, 3.04)
    ]

    weights_flag = type(weights) != type(None)

    if isinstance(array, pd.Series):
        array.to_numpy()

    if isinstance(array, pd.DataFrame):
        if weights_flag:
            raise NotImplementedError("weighted standard deviation is not yet supported for DataFrames")
        n = len(array.columns)
        stdev = lambda x: x.std(axis=1, ddof=0) # For numpy behaviour
    else:
        n = len(array)
        
        if weights_flag:
            stdev = lambda x: np.sqrt(np.average(
                (x - np.average(x, weights=weights))**2, weights=weights
            ))
        else:
            stdev = lambda x: np.std(x)
    #print(f"n: {n}")
    i = n - 2
    if n not in (2, 3, 4, 5):
        if n >= 200:   i = -1
        elif n >= 100: i = -2
        elif n >= 50:  i = -3
        elif n >= 30:  i = -4
        elif n >= 20:  i = -5
        elif n >= 10:  i = -6
        elif n >= 8:   i = -7
        elif n >= 6:   i = -8
    try:
        return t[sigma-1][i]*stdev(array)/np.sqrt(n)
    except IndexError:
        raise NotImplementedError("The function only works up to sigma=3")

def roundToSigFigs(x, sigfigs):
    """
    Rounds the value(s) in x to the number of significant figures in sigfigs.
    Return value has the same type as x.

    Restrictions:
    sigfigs must be an integer type and store a positive value.
    x must be a real value or an array like object containing only real values.
    """
    # Based on the work of: Sean Lake Copyright (c) 2019, BSD 3-Clause License

    if not ( type(sigfigs) is int or type(sigfigs) is long or
             isinstance(sigfigs, np.integer) ):
        raise TypeError("roundToSigFigs: sigfigs must be an integer." )

    if sigfigs <= 0:
        raise ValueError("roundToSigFigs: sigfigs must be positive." )

    if not np.all(np.isreal(x)):
        raise TypeError("roundToSigFigs: all x must be real." )

    matrixflag = False
    if isinstance(x, np.matrix): #Convert matrices to arrays
        matrixflag = True
        x = np.asarray(x)
    if isinstance(x, pd.Series): #Support for pandas Series object 
        x = x.to_numpy()

    xsgn = np.sign(x)
    absx = xsgn * x
    mantissas, binaryExponents = np.frexp(absx)

    decimalExponents = np.log10(2)*binaryExponents
    omags = np.floor(decimalExponents)

    mantissas = mantissas*10**(decimalExponents - omags)

    if matrixflag:
        for i in range(len(mantissas)):
            for j in range(len(mantissas[i])):
                if mantissas[i,j] < 1:
                    mantissas[i,j] *= 10
                    omags[i,j] -= 1
    elif isinstance(mantissas, np.ndarray) and not matrixflag:
        for i in range(len(mantissas)):
            if mantissas[i] < 1:
                mantissas[i] *= 10
                omags[i] -= 1
    else: # if mantissas is float
        if mantissas < 1:
            mantissas *= 10
            omags -= 1

    result = xsgn*np.around(mantissas, sigfigs -1)*10**omags

    if matrixflag:
        result = np.matrix(result, copy=False)

    return result

def multimeterStdev(quantity, percent, digits, resolution):
    stdev = np.sqrt(
        (quantity*percent/(100*np.sqrt(3)))**2 + (digits**2 + 1)*(resolution/np.sqrt(3))**2
    )
    return stdev

def lengthStdev(length, ruler=False, calipers=False):
    """Returns standart deviation for length measurements in meters,
    pass the length in meters"""
    a = 0.1/10**3
    b = 0.1/10**3
    if ruler and calipers:
        raise ERROR("Only one of ruler or calipers can be True")
    elif ruler:
        a = 0.3/10**3
        b = 0.2/10**3
    elif calipers:
        try:
            check_iterable = iter(length)
            iterable = True
        except TypeError as te:
            iterable = False
        if iterable:
            err = []
            for value in length:
                if value > 100/10**3:
                    err.append(0.07/10**3)
                elif value < 50/10**3:
                    err.append(0.05/10**3)
                else:
                    err.append(0.06/10**3)
            return np.array(err)
        if length > 100/10**3:
            return 0.07/10**3
        elif length < 50/10**3:
            return 0.05/10**3
        else:
            return 0.06/10**3
    return a + b*np.ceil(length)

if __name__ == "__main__":
    __N = 10
    __l = [i for i in range(N)]
    print(f"l: {__l}")
    print(studentFuncError(__l))
    __df = pd.DataFrame([__l for i in range(__N)])
    print(__df)
    print(studentFuncError(__df))

# Licenses =====================================================================

# BSD 3-Clause License
# 
# Copyright (c) 2019, Sean Lake
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

