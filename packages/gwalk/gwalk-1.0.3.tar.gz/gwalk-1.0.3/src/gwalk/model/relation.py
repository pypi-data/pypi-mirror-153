#!/usr/bin/env python3
'''Provide generic infrastructure for models with parameters

Relations contain organized sets of parameters.

'''
from gwalk.model.parameter import Parameter
class Relation(object):
    '''Base class for containing parameters and relationships among them

    Ideally, these will be additive,
        which means we must use a dictionary rather than a list

    '''
    def __init__(
                 self,
                 parameters=None,
                 random_state=None,
                ):
        '''Initialize model with some parameters
        
        Parameters
        ----------
        parameters: list, optional
            Input A list, tuple, or dict of parameters
                These are optional, and can be added afterwards
        random_state: np.RandomState, optional
            A random state for random number generation
        '''
        ## Imports
        # Public
        import numpy as np
        # Initialize random state
        if random_state is None:
            self.rs = np.random.RandomState()
        else:
            self.rs = random_state

        # Initialize self._parameters
        self._parameters = {}

        # determine if there are any starting parameters
        if not (parameters is None):
            if isinstance(parameters, dict):
                for key in parameters:
                    self.add_parameter(parameters[key])
            if isinstance(parameters, list) or isinstance(parameters, tuple):
                for item in parameters:
                    self.add_parameter(item)
            elif isinstance(parameters, Parameter):
                self.add_parameter(parameters)
            else:
                raise TypeError("Unknown Parameter type: %s"%(str(type(parameters))))


    def add_parameter(self, p):
        '''Append a parameter to our list of parameters

        Parameters
        ----------
        p: Parameter
            Input new parameter object to append to relation
        '''
        if p.name in self._parameters:
            raise RuntimeError(
                    "Failed to add %s! Parameters must be unique!"%(p.name)
                              )
        self._parameters[p.name] = p
        self._parameters[p.name].rs = self.rs
        # Update parameter map
        self.map_parameters()

    def assign_guess(self, X):
        '''Assign guesses to each parameter

        Parameters
        ----------
        X: array like, shape = nd
            An array of guesses for our parameters,
        '''
        # Check that sample is valid
        X = self.check_sample(X)

        # Initialize constrained Samples
        ns, nd = X.shape

        # Assert things about the shape
        assert ns == 1
        assert nd == len(self._parameters)

        # Check if our guess makes sense
        assert self.satisfies_constraints(X)

        # Assign the guess
        for i, key in enumerate(self._parameters):
            # Do it
            self._parameters[key].assign_guess(X[0,i])

    def read_guess(self):
        '''Read the current guess'''
        ## Imports ##
        # Public
        import numpy as np
        guess = []
        for key in self._parameters:
            guess.append(self._parameters[key].guess)
        return np.asarray(guess)

    def read_limits(self):
        '''Read limits of parameters'''
        ## Imports ##
        # Public
        import numpy as np
        limits = []
        for key in self._parameters:
            limits.append(self._parameters[key].limits)
        return np.asarray(limits)

    def update_limits(self, limits):
        '''Update the limits in an intelligent way

        Parameters
        ----------
        limits: array like, shape = (nd, 2)
            Input a new list of limits [min,max] for each parameter
        '''
        ## Imports
        # Public
        import numpy as np
        # Check dimensionality of limits
        if not np.asarray(limits).shape == (len(self._parameters),2):
            raise RuntimeError("limits shape is %s, but should be %s"%(
                str(np.asarray(limits.shape)), str(len(self._parameters),2)))
        for i, key in enumerate(self._parameters):
            self._parameters[key].update_limits(limits[i])

    def map_parameters(self):
        '''Generate a map of parameters to linear indicies'''
        # Next, get a parameter dictionary
        param_ids = {}
        for i, key in enumerate(self._parameters):
            param_ids[key] = i

        # Hold onto that dictionary
        self.p_map = param_ids

        return self.p_map

        
    def satisfies_constraints(self, X):
        '''Check if samples satisfy constraints

        By default there are no constraints on a relationship
            apart from parameter constraints

        Parameters
        ----------
        X: array like, shape = (npts, nd)
            Input an array of samples which may describe 
                the parameters of this relationship.
        '''
        ## Imports 
        # Public
        import numpy as np
        
        # Check that samples are valid
        X = self.check_sample(X)

        # Initialize constrained Samples
        ns, nd = X.shape
        constrained_indx = np.ones(ns).astype(bool)

        # Constrain by each parameter
        for i, key in enumerate(self._parameters):
            # Identify the parameter index
            p_indx = self._parameters[key].satisfies_constraints(X[:,i])
            # Bitwise and with relationship constraints
            constrained_indx = constrained_indx & p_indx

        return constrained_indx

    # Draw random samples
    def sample_uniform_unconstrained(self, samples):
        '''Sample all parameters uniformly

        Parameters
        ----------
        samples: int
            Input the number of uniform samples we would like to draw
        '''
        ## Imports
        # Public
        import numpy as np
        # Initialize sample shape
        sample_shape = (samples, len(self._parameters.keys()))
        # Initialize samples
        Xs = np.zeros(sample_shape)

        # Fill in values
        for i, key in enumerate(self._parameters):
            Xs[:,i] = self._parameters[key].sample_uniform(samples)

        return Xs

    # Draw random samples in a constrained way
    def sample_uniform(self, samples):
        '''Sample parameters, being careful with constraints

        Parameters
        ----------
        samples: int
            Input the number of uniform samples we would like to draw
        '''
        ## Imports
        # Public
        import numpy as np

        # Initialize the number of valid samples we have
        n_keep = 0

        # Initialize sample shape
        sample_shape = (samples, len(self._parameters.keys()))
        # Initialize samples to keep
        Xk = np.zeros(sample_shape)

        # Continue doing this until we have the right number of samples
        while n_keep < samples:
            # How many samples do we still need
            n_need = samples - n_keep
            # Draw that many samples
            Xs = self.sample_uniform_unconstrained(n_need)
            # Check if these samples satisfy our constraints
            k_indx = self.satisfies_constraints(Xs)
            # Identify the number of new samples to keep from this iteration
            n_it = np.sum(k_indx)
            # keep iterating if there are no valid samples
            if n_it != 0:
                # Keep valid samples
                Xs = Xs[k_indx]
                # Add them to Xk
                Xk[n_keep:n_keep+n_it,:] = Xs
                # Updated n_keep
                n_keep += n_it

        # Return samples
        return Xk

    def check_sample(
                       self,
                       X,
                       w = None,
                       *args,
                       **kwargs
                     ):
        '''Check dimensionality of samples
        
        This function is setup for inheirtance.

        Other relation objects may not have methods this simple

        Parameters
        ----------
        X: array like, shape = (npts, nd)
            Input sample we would like to check as a valid sample
        w: array like, shape = (npts)
            Input weights for valid sample
        '''
        ## Imports ##
        # Public
        import numpy as np
        import warnings

        # Make sure data is the right shape
        if not (len(X.shape) == 2):
            # Check if the data is only one dimensional
            if len(X.shape) == 1:
                # We can make this two dimensional
                X = np.atleast_2d(X)
            else:
                # The data must be two dimensional
                raise RuntimeError(
                    "X.shape = %s, model has %d parameters!"%(str(X.shape), nd)
                    )

        # Check the dimensionality of our parameters
        nd = len(self._parameters)

        # Make sure data has the right dimensions
        if not X.shape[1] == nd:
            # Check if the data just needs to be transposed
            if X.shape[0] == nd:
                warnings.warn(
                    "X.shape = %s, model has %d parameters!"%(str(X.shape), nd)
                    )
                # Transpose data
                X = X.T
            else:
                raise RuntimeError(
                        "X.shape = %s, model has %d parameters!"%(str(X.shape), nd)
                        )

        # Check weights
        if not (w is None):
            # Check that weights have the right shape
            if not len(w.shape) == 1:
                raise RuntimeError(
                    "Weights has shape %s, but should be one dimensional"%(
                     str(w.shape)),
                    )

            # Check number of weights
            if not (x.shape[0] == w.size):
                # We have a different number of weights and samples
                raise RuntimeError(
                    "X.shape = %s, w.shape = %s"%(str(X.shape), str(w.shape))
                   )

        return X


    def likelihood(
                   self,
                   X,
                   return_product=False,
                   log_scale=False,
                   *args,
                   **kwargs
                  ):
        '''Placeholder function for likelihood
        
        In general, relationship objects will have more complicated 
            likelihood functions

        Parameters
        ----------
        X: array like (npts, nd)
            Input sample we would like to evaluate
        return_product: bool, optional
            Input return product of values instead of array?
        log_scale: bool, optional
            Input return lnL instead of L
        '''
        ## Imports ##
        # Public
        import numpy as np
        import warnings

        # Check that the samples make sense
        X = self.check_sample(X)

        # Check the number of samples being evaluated
        ns, nd = X.shape

        # This is only a placeholder likelihood function
        L = np.ones((ns,))

        # Check if we want the log scale
        if log_scale and return_prod:
            return np.sum(np.log(L))
        elif log_scale:
            return np.log(L)
        elif return_prod:
            return np.prod(L)
        else:
            return L

    def hypercube(
                  self,
                  res=None,
                  size=None,
                  limits=None,
                  constrained=False,
                 ):
        '''Generate a hypercube in all of our parameters

        Parameters
        ----------
        res: array like, shape = (nd), optional
            Input Desired hypercube resolution in each dimension
        size: int, optional
            Input maximum number of hypercube points
        limits: array like, shape = (nd, 2), optional
            Alternative limits for hypercube
        '''
        ## Imports ##
        # Public
        import numpy as np
        from gp_api.utils import sample_hypercube
        import warnings

        ## Initialize resolution ##
        # Check dimensionality
        ndim = len(self._parameters)

        # Check cases
        if (res is None):
            if (size is None):
                raise RuntimeError("Usage: hypercube must specify res or size")
            else:
                # Generate maximum resolution for given size
                res = int(size**(1/ndim))
                # This is not a very dense hypercube if res < 5
                if res < 5:
                    warnings.warn(
                        "Maximum res for %d-D hypercube wiht size %d is %d"%(
                            (ndim, size, res))
                                 )
        elif type(res) == int:
            if (size is None):
                # Make res an array
                res = (res*np.ones(ndim)).astype(int)
            else:
                if res > int(size**(1/ndim)):
                    raise RuntimeError(
                        "resolution and size both specified and conflict!")
                else:
                    # Make res an array
                    res = (res*np.ones(ndim)).astype(int)
        elif not(type(res) in [list, tuple, np.ndarray]):
            raise RuntimeError("Unknown resolution type %s"%(str(type(res))))
        elif not (len(res) == ndimn):
            raise RuntimeError("Resolution is not the correct length")
        else:
            # Make res an array
            res = np.asarray(res).astype(int)
            

        ## Initialize limits ##
        if limits is None:
            limits = self.read_limits()
        else:
            # Make limits an array
            limits = np.asarray(limits)
            # Check that limits make sense
            if not limits.shape == (ndim, 2):
                raise RuntimeError("Strange limits fed to hypercube: %s"%(
                        str(limits)))

        ## Generate hypercube ##
        cube_space = sample_hypercube(limits, res)

        # Check where constraints are satisfied
        if constrained:
            k_indx = self.satisfies_constraints(cube_space)
            cube_space = cube_space[k_indx]

        return cube_space
                    
    def __add__(self, other):
        '''Add two relationships by combining parameters and constraints

        Parameters
        ----------
        other: Relationship
            Input: other relationship you wish to add
        '''
        new = _AddRelation(self, other)

        return new

class _AddRelation(Relation):
    '''This is a relationship that results from adding other relationships

    It should not be initialized by a user
    '''
    def __init__(self, summand1, summand2):
        '''Initialize the added parameters

        Parameters
        ----------
        summand1: Relation
            Input first summand for add relation
        summand2: Relation
            Input second summand for add relation
        '''
        # Initialize random state
        self.rs = summand1.rs
        # Hold summands
        self.summands=[]
        # Update summands with summand 1
        if isinstance(summand1, _AddRelation):
            for item in summand1.summands:
                self.summands.append(item)
        else:
            self.summands.append(summand1)

        # Update summands with summand 2
        if isinstance(summand2, _AddRelation):
            for item in summand2.summands:
                self.summands.append(item)
        else:
            self.summands.append(summand2)

        # Define paremeters
        self._parameters = {}
        for summand in self.summands:
            for item in summand._parameters:
                self.add_parameter(summand._parameters[item])

            

    def satisfies_constraints(self, X):
        '''Check if add relation satisfies constraints

        This part is a little sneaky

        Parameters
        ----------
        X: array like, shape = (npts, nd)
            Input sample to evaluate constraints on
        '''
        ## Imports ##
        # Public
        import numpy as np

        # Identify information
        ns, nd = X.shape
        # Initialize Constrained Index 
        constrained_indx = np.ones(ns).astype(bool)
        
        ## Loop the summands ##
        for summand in self.summands:
            # Identify the number of parameters
            n_param = len(summand.p_map.keys())
            # Initialize an array for parameter values
            Xp = np.zeros((ns, n_param))
            # Fill that array
            for key in summand.p_map.keys():
                Xp[:,summand.p_map[key]] = X[:,self.p_map[key]]
            # Update summand parameters
            for key in summand.p_map.keys():
                summand._parameters[key].update_limits(self._parameters[key].limits)
                summand._parameters[key].assign_guess(self._parameters[key].guess)

            # Calculate summand constraints
            constrained_indx &= summand.satisfies_constraints(Xp)

        # Return constrained indx
        return constrained_indx
