# cython: infer_types=True
'''Calculate the pdf of the multivariate normal function
'''
import cython
cimport cython
from cython.parallel import prange
from cython.cimports.libc.math import exp
import numpy as np 

#### Globals ####
_INV_RT2 = 1./np.sqrt(2)
_LOG_2PI = np.log(2*np.pi)

######## C functions ########

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef double _maha_ij(
                     double[::1] Y,
                     double[::1] scale,
                     double[::1] X_mu,
                     double[:,::1] U,
                     Py_ssize_t ndim,
                    ) nogil:
    '''Calculate the maha distance for a single gaussian for a single point
    '''
    cdef int k, l
    cdef double psum
    cdef double maha = 0
    for k in range(ndim):
        psum = 0
        for l in range(ndim):
            psum += U[l,k]*((Y[l]/scale[l])-X_mu[l])
        maha += psum**2
    return maha

#cdef double _pdf_ij(
#                   ) nogil :

######## General functions ########

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
def mahalanobis_cython(
                       double[:,::1] Y,
                       double[:,::1] scale,
                       double[:,::1] X_mu,
                       double[:,:,::1] U,
                       Py_ssize_t nx,
                       Py_ssize_t ny,
                       Py_ssize_t ndim,
                      ):
    # Initialize intermediate data step
    cdef int i, j
    maha = np.zeros((nx,ny),order='c')
    cdef double[:,::1] maha_view = maha 

    for i in range(nx):
        for j in prange(ny,nogil=True):
            maha_view[i,j] = _maha_ij(Y[j],scale[i],X_mu[i],U[i],ndim)
    
    return maha

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
def pdf_exp_product(
                    double[:,::1] maha,
                    double[::1] log_det_cov,
                    double const,
                    Py_ssize_t nx,
                    Py_ssize_t ny,
                    Py_ssize_t ndim,
                    bint log_scale = False,
                   ):
    cdef int i, j
    cdef double minus_half = -0.5
    L = np.zeros((nx,ny),order='c')
    cdef double[:,::1] L_view = L

    if log_scale:
        for i in range(nx):
            for j in prange(ny,nogil=True):
                L_view[i,j] = minus_half * (const + log_det_cov[i] + maha[i,j])
    else:
        for i in range(nx):
            for j in prange(ny,nogil=True):
                L_view[i,j] = exp(minus_half * (const + log_det_cov[i] + maha[i,j]))

    return L

def mahalanobis_numpy(Y, scale, X_mu, U):
    # Initialize intermediate data step
    maha = np.sum(
          np.square(
               np.sum(
                      (Y[None,:,:,None]/scale[:,None,:,None] - X_mu[:,None,:,None])*
                            U[:,None,:,:],
                       axis=-2
                      )
                    ),
                   axis=-1,
                  )
    return maha
        
