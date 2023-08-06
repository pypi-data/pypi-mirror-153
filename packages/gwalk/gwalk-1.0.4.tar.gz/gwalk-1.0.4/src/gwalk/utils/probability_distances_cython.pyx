# cython: infer_types=True
'''Calculate the Bhattacharyya distance of two distributions
'''
import cython
cimport cython
from cython.parallel import prange
from cython.cimports.libc.math import sqrt, log
import numpy as np 

######## C functions ########

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef double _BC_coef(
                     double[::1] P,
                     double[::1] Q,
                     Py_ssize_t Psize,
                    ) nogil:
    '''Calculate the Bhattacharyya distance for two distributions

    Parameters
    ----------
    P: Memoryview C array, shape = (Psize)
        Input First distribution for comparison
    Q: Memoryview C array, shape = (Psize)
        Input Second distribution for comparison
    Psize: Py_ssize_t
        Input numper of points in domain
    '''
    cdef int k
    cdef double BC = 0
    for k in range(Psize):
        BC += sqrt(P[k] * Q[k])
    return BC

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef double _BC_dist(
                     double[::1] P,
                     double[::1] Q,
                     Py_ssize_t Psize,
                    ) nogil:
    '''Calculate the Bhattacharyya distance for two distributions

    Parameters
    ----------
    P: Memoryview C array, shape = (Psize)
        Input First distribution for comparison
    Q: Memoryview C array, shape = (Psize)
        Input Second distribution for comparison
    Psize: Py_ssize_t
        Input numper of points in domain
    '''
    cdef int k
    cdef double BC = 0
    for k in range(Psize):
        BC += sqrt(P[k] * Q[k])
    BC = -log(BC)
    return BC

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef double _H_dist(
                    double[::1] P,
                    double[::1] Q,
                    Py_ssize_t Psize,
                   ) nogil:
    '''Calculate the Hellinger distance for two distributions

    Parameters
    ----------
    P: Memoryview C array, shape = (Psize)
        Input First distribution for comparison
    Q: Memoryview C array, shape = (Psize)
        Input Second distribution for comparison
    Psize: Py_ssize_t
        Input numper of points in domain
    '''
    cdef int k
    cdef double H = 0 
    for k in range(Psize):
        H += sqrt(P[k] * Q[k])
    H = sqrt(1. - H)
    return H



######## General functions ########

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
def bhattacharyya_coefficient(P,Q):
    '''Calculate the Bhattacharyya distance between two distributions'''
    # Handle inputs
    cdef Py_ssize_t Psize = P.size
    cdef Py_ssize_t Qnum
    cdef double max_value = np.finfo(np.double).max

    # Identify shapes
    if len(Q.shape) == 1:
        assert Q.size == Psize
        Q = Q.reshape((1,Psize))
        Qnum = 1
    else:
        assert Q.shape[1] == P.size
        Qnum = Q.shape[0]

    # Define vairables
    cdef int i, j
    Pc = np.asarray(P,order='c')
    Qc = np.asarray(Q,order='c')
    cdef double[::1] Pv = Pc
    cdef double[:,::1] Qv = Qc

    # Initialize output
    BC =  np.zeros(Qnum,dtype=np.double)
    cdef double[::1] BC_view = BC

    # Loop through Q
    for i in prange(Qnum,nogil=True):
        BC_view[i] = _BC_coef(Pv,Qv[i],Psize)

    return BC

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
def bhattacharyya_distance(P,Q):
    '''Calculate the Bhattacharyya distance between two distributions'''
    # Handle inputs
    cdef Py_ssize_t Psize = P.size
    cdef Py_ssize_t Qnum
    cdef double max_value = np.finfo(np.double).max

    # Identify shapes
    if len(Q.shape) == 1:
        assert Q.size == Psize
        Q = Q.reshape((1,Psize))
        Qnum = 1
    else:
        assert Q.shape[1] == P.size
        Qnum = Q.shape[0]

    # Define vairables
    cdef int i, j
    Pc = np.asarray(P,order='c')
    Qc = np.asarray(Q,order='c')
    cdef double[::1] Pv = Pc
    cdef double[:,::1] Qv = Qc

    # Initialize output
    d =  np.zeros(Qnum,dtype=np.double)
    cdef double[::1] d_view = d

    # Loop through Q
    for i in prange(Qnum,nogil=True):
        d_view[i] = _BC_dist(Pv,Qv[i],Psize)

    return d

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
def hellinger_distance(P,Q):
    '''Calculate the Hellinger distance between two distributions'''
    # Handle inputs
    cdef Py_ssize_t Psize = P.size
    cdef Py_ssize_t Qnum
    cdef double max_value = np.finfo(np.double).max

    # Identify shapes
    if len(Q.shape) == 1:
        assert Q.size == Psize
        Q = Q.reshape((1,Psize))
        Qnum = 1
    else:
        assert Q.shape[1] == P.size
        Qnum = Q.shape[0]

    # Define vairables
    cdef int i, j
    Pc = np.asarray(P,order='c')
    Qc = np.asarray(Q,order='c')
    cdef double[::1] Pv = Pc
    cdef double[:,::1] Qv = Qc

    # Initialize output
    d =  np.zeros(Qnum,dtype=np.double)
    cdef double[::1] d_view = d

    # Loop through Q
    for i in prange(Qnum,nogil=True):
        d_view[i] = _H_dist(Pv,Qv[i],Psize)

    return d
