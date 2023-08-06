#!/usr/bin/env python3
'''Provide Relation support for a covariance matrix

Split into characteristic standard deviation and correlation factors

'''
######## Imports #########
from gwalk.model.parameter import Parameter
from gwalk.model.relation import Relation
from gwalk.utils.multivariate_normal import cov_of_std_cor
from gwalk.utils.multivariate_normal import std_of_cov
from gwalk.utils.multivariate_normal import cor_of_cov


class Covariance(Relation):
    '''It is useful to have a subclass of relationship for Covariance Matricies
    '''
    def __init__(
                 self,
                 ndim,
                 sig_max = 3.,
                 random_state=None,
                ):
        '''Initialize a relationship which represents a covaraince matrix

        This includes initializing parameters for each entree

        Inputs:
            ndim (int): The number of variables for the covariance matrix
            sig_max (float array): 
                Set a naive upper limit for the covariance matrix

        The covariance matrix will be made of (n^2 + n)/2 parameters,
            each representing a degree of freedom

        There are n degrees of freedom in the variance, sigma
        There are (n^2 - n)/2 degrees of freedom in the correlation matrix, rho

        Parameters
        ----------
        ndim: int
            Input The number of dimensions of data (not number of parameters)
        sig_max: float, optional
            Input The maximum allowed standard deviation for a relation
        random_state: np.RandomState
            Input numpy random state object for randomness
        '''
        ## Inputs ##
        # Public
        import numpy as np

        # Initialize a relationship
        super().__init__(random_state=random_state)
        # Define size
        self.ndim = ndim

        # Check sig_max
        if np.asarray(sig_max).size == 1:
            sig_max = np.ones((self.ndim))*sig_max
        elif np.asarray(sig_max).size == self.ndim:
            sig_max = np.asarray(sig_max).flatten()
        else:
            raise RuntimeError("sig_max must be scalar or 1d array of size n")

        # Generate Scale parameters
        # There will be n of these
        for i in range(self.ndim):
            # Name this entry
            tag = "std_%d"%(i)
            # Guess
            guess = 1.0
            # Guess limits
            limits = [1e-3, sig_max[i]]
            # Label
            label = r"$\sigma_{%d}$"%(i)

            # Initialize parameter
            p = Parameter(tag, guess, limits, label=label)
            self.add_parameter(p)

        # Generate Rho parameters
        for i in range(self.ndim):
            for j in range(i):
                # There are only half as many of these as CoV elements
                tag = "cor_%d_%d"%(i,j)
                # Guess these off diagonal elements to be uncorrelated
                guess = 0.
                # Limits are easy
                limits = [-1.,1.]
                # Label parameter
                label = r"$\rho_{%d,%d}$"%(i,j)

                # Initialize parameter
                p = Parameter(tag, guess, limits, label=label)
                self.add_parameter(p)


    def read_std(self):
        '''Return an std matrix with our current guess'''
        ## Imports ##
        # Public
        import numpy as np
        # Initialize std
        std = np.zeros((self.ndim,))
        # Loop through std parameters
        for i in range(self.ndim):
            # Generate tag
            tag = "std_%d"%(i)
            # Load value
            std[i] = self._parameters[tag].guess

        return std

    def read_cor(self):
        '''Return a correlation matrix with our current guesses'''
        ## Imports ##
        # Public
        import numpy as np
        # Initialize correlation
        cor = np.eye(self.ndim)
        # Loop through parameters
        for i in range(self.ndim):
            for j in range(i):
                # Generate tag
                tag = "cor_%d_%d"%(i,j)
                # Load value
                cor[i,j] = cor[j,i] = self._parameters[tag].guess

        return cor

    def read_cov(self):
        '''Return a covariance matrix with our current guesses'''
        ## Imports ##
        # Public
        import numpy as np
        # Load variance and correlation guesses
        std = np.atleast_2d(self.read_std())
        cor = self.read_cor()
        # Build covariance matrix
        var = std*std.T
        cov = cor.copy()*var
        return cov

    def std_of_params(self,X):
        '''Extract std parameters from samples

        Parameters
        ----------
        X: array like, shape = (npts, nd)
            Input sample points for parameters
        '''
        ## Imports ##
        # Public
        import numpy as np
        # First check samples
        X = self.check_sample(X)

        ## Construct Variance ##
        # Initialize std
        std = np.zeros((X.shape[0],self.ndim,))
        # Loop through std parameters
        for i in range(self.ndim):
            # Generate tag
            tag = "std_%d"%(i)
            # Generate p_id
            p_id = self.p_map[tag]
            # Load value
            std[:,i] = X[:,p_id]

        return std

    def cor_of_params(self, X):
        '''Extract correlation matrix from samples

        Parameters
        ----------
        X: array like, shape = (npts, nd)
            Input sample points for parameters
        '''
        ## Imports ##
        # Public
        import numpy as np
        # First check samples
        X = self.check_sample(X)

        # Initialize Correlation matrix
        cor = np.ones((X.shape[0], self.ndim, self.ndim))*np.eye(self.ndim)
        # Loop through correlation parameters
        for i in range(self.ndim):
            for j in range(i):
                # Generate tag
                tag = "cor_%d_%d"%(i,j)
                # Generate p_id
                p_id = self.p_map[tag]
                # Load value
                cor[:,i,j] = cor[:,j,i] = X[:,p_id]

        return cor

    def cov_of_params(self,X):
        '''Extract cov from samples

        Parameters
        ----------
        X: array like, shape = (npts, nd)
            Input sample points for parameters
        '''
        ## Imports ##
        # Public
        import numpy as np
        # First check samples
        X = self.check_sample(X)

        ## Construct Variance ##
        std = self.std_of_params(X)

        # Initialize Correlation matrix
        cor = self.cor_of_params(X)

        # Find the covariance
        cov = cov_of_std_cor(std, cor)
        return cov

    def std_of_cov(self, cov):
        '''Compute the std for an array of covariance matrixes

        Parameters
        ----------
        cov: array like, shape = (npts, ndim, ndim)
            Input covariance matrix
        '''
        return std_of_cov(cov)

    def cor_of_cov(self, cov):
        '''Compute the correlation for an array of covariance matrixes

        Parameters
        ----------
        cov: array like, shape = (npts, ndim, ndim)
            Input covariance matrix
        '''
        return cor_of_cov(cov)

    def params_of_cov(self, cov):
        '''Compute the list of params from a covariance matrix

        Parameters
        ----------
        cov: array like, shape = (npts, ndim, ndim)
            Input covariance matrix
        '''
        ## Imports ##
        # Public
        import numpy as np

        # Check dimensionality of cov
        if len(cov.shape) == 2:
            cov = np.asarray([cov])

        # Check the covariance matrix
        if not ((cov.shape[1] == self.ndim) and (cov.shape[2] == self.ndim)):
            raise RuntimeError("Invalid covariance matrix")
        
        # Initialize list of parameters
        X = np.empty((cov.shape[0], len(self._parameters)))
        
        # Compute variance and correlation
        std = std_of_cov(cov)
        cor = cor_of_cov(cov)
    
        # Loop through the std parameters
        for i in range(self.ndim):
            # Identify the std tag
            tag = "std_%d"%(i)
            # Identify parameter id
            p_id = self.p_map[tag]
            # Assign std parameters
            X[:,p_id] = std[:,i]

        # Loop through correlation parameters
        for i in range(self.ndim):
            for j in range(i):
                # Identify the correlation tag
                tag = "cor_%d_%d"%(i,j)
                # Identify parameter id
                p_id = self.p_map[tag]
                # Assign correlation parameters
                X[:,p_id] = cor[:,i,j]

        # Check samples
        X = self.check_sample(X)

        return X

    def satisfies_constraints(self, X):
        ''' Check if covariance Relation constraints are satisfied

        A Covariance Matrix must have positive Eigenvalues
        
        Parameters
        ----------
        X: array like, shape = (npts, nd)
            Input sample points for parameters
        '''
        ## Inputs ##
        # Public
        import numpy as np
        from numpy.linalg import eigvals, eigvalsh
        # First check samples
        X = self.check_sample(X)

        ## Construct Covariance Matrix ##
        cov = self.cov_of_params(X)

        # Find lower bound
        t = cov.dtype.char.lower()
        factor = {'f':1E3, 'd':1E6}
        cond = factor[t] * np.finfo(t).eps
        eps = cond * np.max(abs(cov))

        # Make sure variance guesses make sense
        c1 = super().satisfies_constraints(X)
        # Find if all the eigenvalues are positive
        c2 = np.bitwise_and.reduce(np.atleast_2d(eigvalsh(cov) > eps),axis=1)
        # Find the valid samples
        constrained_indx = c1 & c2
        return constrained_indx
                
