#!/usr/bin/env python3
'''\
Provide infrastructure for models and hyperparameters
'''
#### Public Imports ####
import numpy as np
from maha_cython import mahalanobis_cython, pdf_exp_product
#### Globals ####
_INV_RT2 = 1./np.sqrt(2)
_LOG_2PI = np.log(2*np.pi)

#### General functions ####

def cov_of_std_cor(std,cor):
    '''Reconstruct the covariance from std and corelation
    Parameters
    ----------
    std: array like, shape = (npts, ndim)
        Input array of sigma values
    cor: array like, shape = (npts, ndim, ndim)
        Input array of correlation matrix values
    '''
    # Check dimensionality of std
    if len(std.shape) == 1:
        npts, ndim = 1, std.size
        std = std.reshape((npts,ndim))
    else:
        npts, ndim = std.shape
    # Check dimensionality of cor
    if len(cor.shape) == 2:
        cor = cor.reshape((npts,ndim,ndim))
    # Assert dimensionality match up
    assert cor.shape == ((npts,ndim,ndim))

    # DO NOT CHANGE THIS!
    std_expand = np.tensordot(std, np.ones(ndim), axes=0)
    var = std_expand * np.transpose(std_expand, axes=[0,2,1])
    # Reconstruct the covariance matrix
    cov = cor * var
    return cov

def std_of_cov(cov):
    '''Extract the vectorized std from the vectorized covariance
    Parameters
    ----------
    cov: array like, shape = (npts, ndim, ndim)
        Input Array of cov values
    '''
    # Protect against usage
    if len(cov.shape) == 2:
        cov = cov[None,:,:]
    elif len(cov.shape) != 3:
        raise ValueError("Error cor_of_cov")
    # Check squareness
    ndim = cov.shape[-1]
    if not (cov.shape[-2] == ndim):
        raise ValueError("cov must be square")
    # Identify std values
    std = np.sqrt(np.sum(cov*np.eye(ndim),axis=1))
    return std

def cor_of_cov(cov):
    '''Reconstruct the vectorized correlation matrix from the covariance
    Parameters
    ----------
    cov: array like, shape = (npts, ndim, ndim)
        Input Array of cov values
    '''
    # Protect against usage
    if len(cov.shape) == 2:
        cov = cov[None,:,:]
    elif len(cov.shape) != 3:
        raise ValueError("Error cor_of_cov")
    # Check squareness
    ndim = cov.shape[-1]
    if not (cov.shape[-2] == ndim):
        raise ValueError("cov must be square")
    # Identify std values
    std = np.sqrt(np.sum(cov*np.eye(ndim),axis=1))
    # Compute the inverse variance
    istd = 1./std
    # Compute the expansion of istd
    istd_expand = np.tensordot(istd, np.ones(ndim), axes=0)
    # Compute the inverse of the fully correlated covariance
    isig2 = istd_expand * np.transpose(istd_expand, axes=[0,2,1])
    # Calculate the correlation matrix
    cor = cov*isig2
    return cor


#### Functions that assume normal model object ####

## dimension checking/reduction ##
def n_param_of_ndim(ndim):
    '''Return the number of parameters associated witha guess in n dimensions
    Parameters
    ----------
    ndim: int
        Input number of dimensions
    '''
    return int((ndim*ndim + 3*ndim)//2)

def ndim_of_n_param(n_param, max_dim=100):
    '''find the dimensionality of a guess
    Parameters
    ----------
    n_param: int
        Input number of parameters
    max_dim: int, optional
        Input maximum number of dimensions to try
    '''
    for i in range(max_dim):
        if n_param == n_param_of_ndim(i):
            return i
    raise RuntimeError("Failed to get number of dimensions for guess")

def params_reduce_1d(X, index):
    '''Reduce to a 1D marginal set of parameters
    Parameters
    ----------
    X: array like, shape = (npts, nparams)
        Input Array of parameter guesses
    index: int
        Input which dimension would we like to generate an evaluation set for
    '''
    # Protect against single set of parameters
    if len(X.shape) == 1:
        X = X[None,:]
    # Extract dimensionality
    n_gauss, n_param = X.shape
    ndim = ndim_of_n_param(n_param)
    # Protect against invalid choices
    assert ndim > index
    # Reduce dimensionality
    Xi = np.asarray([X[:,index],X[:,index+ndim]]).T
    return Xi

def params_reduce_2d(X, index, jndex):
    '''Reduce to a 2D marginal set of parameters
    Parameters
    ----------
    X: array like, shape = (npts, nparams)
        Input Array of parameter guesses
    index: int
        Input which dimension would we like to generate an evaluation set for
    jndex: int
        Input which other dimension would we like to generate an evaluation set for
    '''
    # Protect against single set of parameters
    if len(X.shape) == 1:
        X = X[None,:]
    # Extract dimensionality
    n_gauss, n_param = X.shape
    ndim = ndim_of_n_param(n_param)
    # Protect usage
    assert ndim > index
    assert index > jndex
    # Reduce dimensionality
    Xij = np.asarray([
                      X[:,index],
                      X[:,jndex],
                      X[:,index+ndim],
                      X[:,jndex+ndim],
                      X[:,2*ndim + ((index*(index-1))//2) + jndex]
                     ]).T
    return Xij

def params_reduce_dd(X, indices):
    '''Reduce to indexed marginals
    Parameters
    ----------
    X: array like, shape = (npts, nparams)
        Input Array of parameter guesses
    indices: list
        Input list of indices we would like parameters for
    '''
    # Protect against single set of parameters
    if len(X.shape) == 1:
        X = X[None,:]
    # Extract dimensionality
    n_gauss, n_param = X.shape
    ndim = ndim_of_n_param(n_param)
    # Extract dimensionality of indices
    ndim_index = len(indices)
    n_param_index = n_param_of_ndim(ndim_index)
    # Initialize array
    Xp = np.empty((n_gauss, n_param_index))
    # Loop through Xp dimensions
    for i in range(ndim_index):
         Xp[:,i] =              X[:,indices[i]]
         Xp[:,i+ndim_index] =   X[:,indices[i]+ndim]
    # Loop through correlation factors
    for i in range(ndim_index):
        for j in range(i):
            if indices[i] > indices[j]:
                index, jndex = indices[i], indices[j]
            elif indices[i] < indices[j]:
                index, jndex = indices[j], indices[i]
            else:
                raise RuntimeError("indices[i] == indices[j]")
            Xp[:,2*ndim_index + ((i*(i-1))//2) + j] = \
                X[:,2*ndim + ((index*(index-1))//2) + jndex]
    return Xp

                



## Conversions ##

def mu_of_params(X):
    '''Reconstruct the vectorized mu parameters of input Gaussian parameters
    Parameters
    ----------
    X: array like, shape = (npts, nparams)
        Input Array of parameter guesses
    '''
    # Protect against single set of parameters
    if len(X.shape) == 1:
        X = X[None,:]
    # Identify n_gauss
    n_gauss = X.shape[0]
    # Identify ndim
    n_param = X.shape[1]
    ndim = ndim_of_n_param(n_param)
    # Reconstruct mu
    mu = X[:,:ndim]
    return mu

def std_of_params(X):
    '''Reconstruct the vectorized sigma parameters of input Gaussian parameters
    Parameters
    ----------
    X: array like, shape = (npts, nparams)
        Input Array of parameter guesses
    '''
    # Protect against single set of parameters
    if len(X.shape) == 1:
        X = X[None,:]
    # Identify n_gauss
    n_gauss = X.shape[0]
    # Identify ndim
    n_param = X.shape[1]
    ndim = ndim_of_n_param(n_param)
    # Reconstruct std
    std = X[:,ndim:2*ndim]
    return std

def cor_of_params(X):
    '''Reconstruct the vectorized correlation matrix of input Gaussian parameters
    Parameters
    ----------
    X: array like, shape = (npts, nparams)
        Input Array of parameter guesses
    '''
    # Protect against single set of parameters
    if len(X.shape) == 1:
        X = X[None,:]
    # Identify n_gauss
    n_gauss = X.shape[0]
    # Identify ndim
    n_param = X.shape[1]
    ndim = ndim_of_n_param(n_param)
    # Calculate std of params
    std = std_of_params(X)
    # Reconstruct correlation matrices
    cor = np.ones((n_gauss, ndim, ndim))*np.eye(ndim)
    # The correlation index is carefully kept consistent
    # DO NOT CHANGE THIS!
    cor_index = 2*ndim
    for i in range(ndim):
        for j in range(i):
            cor[:,i,j] = cor[:,j,i] = X[:,cor_index]
            cor_index += 1
    if not cor_index == n_param:
        raise RuntimeError("Correlation Matrix reconstruction is broken")
    return cor

def cov_of_params(X):
    '''Reconstruct the vectorized corvariance of input Gaussian parameters
    Parameters
    ----------
    X: array like, shape = (npts, nparams)
        Input Array of parameter guesses
    '''
    # Protect against single set of parameters
    if len(X.shape) == 1:
        X = X[None,:]
    # Identify n_gauss
    n_gauss = X.shape[0]
    # Identify ndim
    n_param = X.shape[1]
    ndim = ndim_of_n_param(n_param)
    # Calculate std of params
    std = std_of_params(X)
    # Calculate correlation matrix
    cor = cor_of_params(X)
    # Reconstruct the variance matrix
    # DO NOT CHANGE THIS!
    std_expand = np.tensordot(std, np.ones(ndim), axes=0)
    var = std_expand * np.transpose(std_expand, axes=[0,2,1])
    # Reconstruct the covariance matrix
    cov = cor * var
    return cov

def mu_cov_of_params(X):
    '''Reconstruct vectorized mu and covariance of input Gaussian parameters
    Parameters
    ----------
    X: array like, shape = (npts, nparams)
        Input Array of parameter guesses
    '''
    mu = mu_of_params(X)
    cov = cov_of_params(X)
    return mu, cov

def params_of_mu_cov(mu, cov):
    '''Reconstruct Gaussian vectorized parameters for given mu and covariance
    Parameters
    ----------
    mu: array like, shape = (npts, ndim)
        Input Array of mu values
    cov: array like, shape = (npts, ndim, ndim)
        Input Array of cov values
    '''
    # Protect against usage
    if (len(mu.shape) == 1) and (len(cov.shape) == 2):
        mu = mu[None,:]
        cov = cov[None,:,:]
    elif (len(mu.shape) != 2) or (len(cov.shape) != 3):
        raise ValueError("mu or cov is not the right shape!")
    # Identify useful information
    n_gauss = mu.shape[0]
    ndim = mu.shape[1]
    n_param = n_param_of_ndim(ndim)
    # Protect against usage
    if cov.shape != (n_gauss, ndim, ndim):
        raise ValueError("cov is not shape (n_gauss, ndim, ndim)")
    # Initialize array
    X = np.empty((n_gauss,n_param))
    # Insert mu values
    X[:,:ndim] = mu
    # Insert std values
    X[:,ndim:2*ndim] = np.sqrt(np.sum(cov*np.eye(ndim),axis=1))
    ## Compute Correlation ##
    cor = cor_of_cov(cov)
    ## Insert Correlation Values ##
    cor_index = 2*ndim
    for i in range(ndim):
        for j in range(i):
            X[:,cor_index] = cor[:,i,j]
            cor_index += 1
    if not cor_index == n_param:
        raise RuntimeError("Correlation matrix not extracted properly")
    # And we're done!
    return X

#### multivariate normal pdf ####
def multivariate_normal_pdf(
                            X,
                            Y,
                            scale = False,
                            log_scale = False,
                           ):
    '''Find the likelihood of some data with a particular guess of parameters
    Parameters
    ----------
    X: array like, shape = (npts, nparams)
        Input Array of parameter guesses
    Y: array like, shape = (npts, ndim)
        Input Array of samples to be evaluated
    scale: array like, shape = (ngauss,ndim)
        Input scale for different parameter guesses
            if False: assume input data is PHYSICAL
            if True: assume input data is SCALED
            if (len(Y),) array: scale input by given values
            if (ngauss, len(Y)): Each sample gaussian has its own scale
    log_scale: bool, optional
        Input return log likelihood instead of likelihood?

    Outputs:
        L - array of likelihoods (n_gauss, n_pts)
    '''
    ## Imports ##
    # Public
    import numpy as np
    from scipy import stats

    ## Check Usage ##
    # Load data shapes
    X_shape = X.shape
    Y_shape = Y.shape

    # Intended use: X and Y are both rank 2
    if (len(X_shape) == 2) and (len(Y_shape) == 2):
        # Identify key shape values
        n_gauss = X_shape[0]
        n_param = X_shape[1]
        n_pts   = Y_shape[0]
        ndim   = Y_shape[1]
        # Check dimensionality
        if not n_param_of_ndim(ndim) == n_param:
            raise ValueError("Usage: X should be (n_guass, n_param)," + \
                                "Y should be (n_pts, ndim)")

    # If n_gauss is 1, we can work with that
    elif (len(X_shape) == 1) and (len(Y_shape) == 2):
        # Identify key shape values
        n_gauss = 1
        n_param = X_shape[0]
        n_pts   = Y_shape[0]
        ndim   = Y_shape[1]
        # Check dimensionality
        if not n_param_of_ndim(ndim) == n_param:
            raise ValueError("Usage: X should be (n_guass, n_param)," + \
                                "Y should be (n_pts, ndim)")
        else:
            # Correct dimensionality
            X = X[None,:]

    # If n_pts is 1, we can work with that
    elif (len(X_shape) == 2) and (len(Y_shape) == 1):
        # Identify key shape values
        n_gauss = X_shape[0]
        n_param = X_shape[1]
        n_pts   = 1
        ndim   = Y_shape[0]
        # Check dimensionality
        if not n_param_of_ndim(ndim) == n_param:
            raise ValueError("Usage: X should be (n_guass, n_param)," + \
                                "Y should be (n_pts, ndim)")
        else:
            # Correct dimensionality
            Y = Y[None,:]

    # If n_gauss is 1 and n_pts is 1, we can work with that
    elif (len(X_shape) == 1) and (len(Y_shape) == 1):
        # Identify key shape values
        n_gauss = 1
        n_param = X_shape[0]
        n_pts   = 1
        ndim   = Y_shape[0]
        # Check dimensionality
        if not n_param_of_ndim(ndim) == n_param:
            raise ValueError("Usage: X should be (n_guass, n_param)," + \
                                "Y should be (n_pts, ndim)")
        else:
            # Correct dimensionality
            X = X[None,:]
            Y = Y[None,:]

    # Other shapes are an error
    else:
        raise ValueError("Usage: X.shape = %s, Y.shape = %s"%(
                str(X_shape), str(Y_shape)))

    # Check scale
    if scale is False:
        # Scale not being used
        scale = np.ones((n_gauss, ndim))
    elif (len(scale.shape) == 1) and \
         (scale.shape[0] == ndim):
        # One scale fits all
        scale = np.ones((n_gauss, ndim)) * scale
    elif (len(scale.shape) == 2) and \
         (scale.shape[0] == n_gauss) and \
         (scale.shape[1] == ndim):
        # Dimensions are correct. Protect scope
        scale = scale.copy()
    else:
        raise ValueError("Usage: scale.shape = %s"%str(scale.shape))
        
    ## Reconstruct mu and covariance ##
    X_mu, X_cov = mu_cov_of_params(X)
    X_mu = np.asarray(X_mu,order='c')
    #XA = params_of_mu_cov(X_mu, X_cov)
    #print(np.max(np.abs(X - XA)))
    #raise Exception("Break")

    ## Eigenvector Decomposition ##
    # Find eigenvalues and eigenvectors (see scipy)
    s, u = np.linalg.eigh(X_cov)
    # Find the precision of the datatype used to store eigenvalues
    eps = stats._multivariate._eigvalsh_to_eps(s)
    # Initialize the log of the covariances
    d = np.zeros((n_gauss, ndim))
    # Find the eigenvalues which aren't zero
    keep = np.prod(s > eps, axis=1).astype(bool)

    # Find the log of the values which aren't zero
    d[keep] = np.log(s[keep])
    # Sum that quantity
    log_det_cov = np.sum(d, axis=1)

    # The goal of this section is to come up with a function U,
    # Such that ((x - mu) dot U)^2 is something like 
    # matmul((x - mu).T, matmul(Cov^-1, (x - mu)))
    # Note that this is done with arrays
    s_pinv = np.zeros_like(s)
    s_pinv[keep] = np.power(s[keep], -0.5)
    #raise Exception()
    U = u*s_pinv[:,None,:]

    # Calculate the mahalanobis factor
    maha = mahalanobis_cython(np.asarray(Y,order='c'), scale, X_mu, U, n_gauss, n_pts, ndim)
    # Compute the likelihood!
    L = pdf_exp_product(maha, log_det_cov, ndim*_LOG_2PI, n_gauss, n_pts, ndim, log_scale=log_scale)
    L[~keep] = 0.

    return L

#### Helper Functions ####
def multivariate_normal_marginal1d(
                                   X,
                                   Y,
                                   index,
                                   scale = False,
                                  ):
    '''marginal1d evaluations
    Parameters
    ----------
    X: array like, shape = (npts, nparams)
        Input Array of parameter guesses
    Y: array like, shape = (npts, ndim)
        Input Array of samples to be evaluated
    scale: array like, shape = (ngauss,ndim)
        Input scale for different parameter guesses
            if False: assume input data is PHYSICAL
            if True: assume input data is SCALED
            if (len(Y),) array: scale input by given values
            if (ngauss, len(Y)): Each sample gaussian has its own scale
    index: int
        Input which dimension would we like to generate an evaluation set for
    '''
    # Assert dimensionality of data
    assert len(X.shape) == 2
    # Upack n_gauss and n_param
    n_gauss, n_param = X.shape
    # Retrieve ndim
    ndim = ndim_of_n_param(n_param)
    # Assert dimensionality of Y
    if len(Y.shape) == 2:
        if Y.shape[1] == ndim:
            Y = Y[:,index,None]
        elif Y.size == np.prod(Y.size):
            Y = Y.reshape(Y.size,1)
        else:
            raise RuntimeError("Y is some kind of weird shape")
    elif len(Y.shape) == 1:
        Y = Y.reshape(Y.size,1)
    else:
       raise RuntimeError("Y is some kind of weird shape")
        
    # Investigate scale
    if isinstance(scale,np.ndarray):
        if scale.size == ndim:
            scale = scale[index].flatten()
        elif scale.shape[1] == ndim:
            scale = scale[:,i].reshape((n_gauss,1))
    # Pick out X
    X = params_reduce_1d(X, index)
    L = multivariate_normal_pdf(X,Y,scale=scale)
    return L

def multivariate_normal_marginal2d(
                                   X,
                                   Y,
                                   index, jndex,
                                   scale = False,
                                  ):
    '''marginal1d evaluations
    Parameters
    ----------
    X: array like, shape = (npts, nparams)
        Input Array of parameter guesses
    Y: array like, shape = (npts, ndim)
        Input Array of samples to be evaluated
    scale: array like, shape = (ngauss,ndim)
        Input scale for different parameter guesses
            if False: assume input data is PHYSICAL
            if True: assume input data is SCALED
            if (len(Y),) array: scale input by given values
            if (ngauss, len(Y)): Each sample gaussian has its own scale
    index: int
        Input which dimension would we like to generate an evaluation set for
    jndex: int
        Input which other dimension would we like to generate an evaluation set for
    '''
    # Assert dimensionality of data
    assert len(X.shape) == 2
    # Upack n_gauss and n_param
    n_gauss, n_param = X.shape
    # Retrieve ndim
    ndim = ndim_of_n_param(n_param)
    # Assert dimensionality of Y
    assert len(Y.shape) == 2
    if Y.shape[1] == ndim:
        Y = Y[:,[index,jndex]]
    elif Y.shape[1] != 2:
        raise RuntimeError("Y is some kind of weird shape")
    # Investigate scale
    if isinstance(scale,np.ndarray):
        if scale.size == ndim:
            scale = scale[[index,jndex]].flatten()
        elif scale.shape[1] == ndim:
            scale = scale[:,[index,jndex]].reshape((n_gauss,2))
    # Pick out X
    X = params_reduce_2d(X, index, jndex)
    L = multivariate_normal_pdf(X,Y,scale=scale)
    return L
