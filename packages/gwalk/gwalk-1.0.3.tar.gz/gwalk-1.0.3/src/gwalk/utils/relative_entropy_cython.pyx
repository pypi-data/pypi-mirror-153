# cython: infer_types=True
'''Calculate the relative entropy using cython compiled functions

long description
'''
import cython
cimport cython
from cython.parallel import prange
from cython.cimports.libc.math import log, exp
import numpy as np

cdef extern from "math.h":
    double log(double x) nogil

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef double _rel_entr(
                     double[::1] P,
                     double[::1] Q,
                     Py_ssize_t Psize,
                     double max_value,
                    ) nogil:
    '''Calculate the relative entropy between P and Q
    '''
    cdef int i
    cdef double r = 0
    for i in range(Psize):
        if (P[i] > 0) & (Q[i] > 0):
            r += P[i]*log(P[i]/Q[i])
        elif P[i] < 0:
            r = max_value
            return r
    return r

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef double _rel_entr_alt(
                          double[::1] P,
                          double[::1] lnP,
                          double[::1] lnQ,
                          Py_ssize_t Psize,
                         ) nogil:
    '''Calculate the relative entropy between P and Q
    '''
    cdef int i
    cdef double r = 0
    cdef double Qc = 0
    cdef double lnQc
    # Calculate Q coefficient
    for i in range(Psize):
        Qc += exp(lnQ[i])
    lnQc = log(Qc)
    # Calculate relative entropy
    for i in range(Psize):
        r += P[i]*(lnP[i] - (lnQ[i] - lnQc))# - lnQc)
    return r

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
def relative_entropy(P, Q,):
    '''Calculate the relative entropy between P and Q for many Q
    '''
    # Handle inputs
    cdef Py_ssize_t Psize = P.size
    cdef Py_ssize_t Qnum
    cdef double max_value = np.finfo(np.double).max

    # define variables
    cdef int i
    Pc = P.copy(order='c')
    Qc = Q.copy(order='c')
    cdef double[::1] Pv = Pc
    cdef double[:,::1] Qv = Qc

    # Identify sizes
    if len(Q.shape) == 1:
        assert Q.size == Psize
        Q = Q.reshape((1,Psize))
        Qnum = 1
    else:
        assert Q.shape[1] == Psize
        Qnum = Q.shape[0]

    # Initialize output
    r = np.zeros(Qnum,dtype=np.double)
    cdef double[::1] r_view = r

    # Loop through Q
    for i in prange(Qnum,nogil=True):
        r_view[i] = _rel_entr(Pv, Qv[i], Psize, max_value)

    return r

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
def relative_entropy_alt(P, lnP, lnQ):
    '''Calculate the relative entropy between P and Q for many Q
    '''
    # Handle inputs
    cdef Py_ssize_t Psize = P.size
    cdef Py_ssize_t Qnum
    #Q = np.exp(lnQ)
    #Q /= np.sum(Q,axis=-1)[:,None]
    #lnQ = np.log(Q)


    # define variables
    cdef int i
    Pc = P.copy(order='c')
    lnPc = lnP.copy(order='c')
    lnQc = lnQ.copy(order='c')

    cdef double[::1] Pv = Pc
    cdef double[::1] lnPv = lnPc
    cdef double[:,::1] lnQv = lnQc

    # Identify sizes
    if len(lnQ.shape) == 1:
        assert lnQ.size == Psize
        lnQ = lnQ.reshape((1,Psize))
        Qnum = 1
    else:
        assert lnQ.shape[1] == Psize
        Qnum = lnQ.shape[0]

    # Initialize output
    r = np.zeros(Qnum,dtype=np.double)
    cdef double[::1] r_view = r

    # Loop through Q
    for i in prange(Qnum,nogil=True):
        r_view[i] = _rel_entr_alt(Pv, lnPv, lnQv[i], Psize)

    return r
