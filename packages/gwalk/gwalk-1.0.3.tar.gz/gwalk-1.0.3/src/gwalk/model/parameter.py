#!/usr/bin/env python3
'''Provide a generic infrastructure for optimizable parameters

Each parameter describes a quantity with a single value.

This structure will be useful for successive approximations and
    modeling
'''
import warnings

class Parameter(object):
    '''The description of a quantity we would like to know, but may not
    '''
    def __init__(
                 self,
                 name,
                 guess,
                 limits,
                 label=None,
                 random_state=None,
                ):
        '''Inialize a parameter object

        Parameters
        ----------
        name: str
            Input Some tag to identify the parameter by, which must be unique
        guess: float
            Input a value which might be true for this parameter
        limits: array like (2)
            Input What values can this parameter take?
        label: str, optional
            Input a LaTeX label to assign this parameter, optional
        random_state: np.RandomState, optional
            Input numpy random state
        '''
        ## Imports ##
        # Public
        import numpy as np

        ## Store quantities ##
        # The name of the parameter
        self.name = name

        # The label of the parameter
        if label==None:
            self.label = name
        else:
            self.label = label

        # The limits of the parameter
        self.update_limits(limits)

        # The default value of the parameter
        self.assign_guess(guess)

        # Initialize random state
        if random_state is None:
            self.rs = np.random.RandomState()
        else:
            self.rs = random_state

    def satisfies_constraints(self,X):
        '''Determine if a particular guess of the parameter, X is a valid guess

        Relationships will check each parameter's constraints to satisfy
            their own

        Parameters
        ----------
        X: array like, shape (npts)
            Input array of samples
        '''
        # Imports
        # Public
        import numpy as np
        # Constrained Samples
        constrained_indx = np.ones_like(X).astype(bool)

        # Remove samples for 1-D limits
        constrained_indx[X < self.limits[0]] = False
        constrained_indx[X > self.limits[1]] = False

        return constrained_indx

    def sample_uniform(self, samples):
        '''Sample the parameter uniformly within its limits

        Parameters
        ----------
        samples: int
            Input number of uniform samples to draw
        '''
        ## Imports
        # Public
        import numpy as np
        # Draw samples
        Xs = self.rs.uniform(self.limits[0], self.limits[1], samples)
        return Xs

    def assign_guess(self, guess):
        '''Update the guess carefully


        Parameters
        ----------
        guess: float
            New guess at the value of this parameter
        '''
        ## Imports ##
        # Public
        import numpy as np

        # Use numpy array
        guess = np.asarray(guess).flatten()

        # Check for invalid shapes
        if not (guess.size == 1):
            raise RuntimeError(
                "Parameters can only be assigned a single value"
                                )

        # Check for parameter limitations
        if not self.satisfies_constraints(guess):
            raise ValueError(
                "Guess for parameter %s does not fall in limits %s"%(
                    self.name, str(self.limits))
                            )
        # Assign the guess
        self.guess = guess[0]

    def update_limits(self, limits):
        '''Update the limits in an intelligent way

        Parameters
        ----------
        limits: array like, shape = (2)
            Input a new set of limits [min,max] for a single parameter
        '''
        ## Imports
        # Public
        import numpy as np
        # Update type of limits
        limits = np.asarray(limits).flatten()
        # Check that limits are sensible
        if not limits.size == 2:
            raise RuntimeError("Limits should have length 2")
        if not limits[1] > limits[0]:
            warnings.warn("Warning: limits[1] > limits[0]")
            limits = np.sort(limits)
        # Check that limits are finite
        if not all(np.isfinite(limits)):
            raise ValueError("Limits must be finite")

        # The limits of the parameter
        self.limits = limits

    def linspace(self, res, limits=None):
        '''Generate a linspace for the parameter in some limits

        Parameters
        ----------
        res: int
            Input desired linspace resolution
        limits: array like, shape = (2), optional
            Input optional alternative limits
        '''
        ## Imports 
        # Public
        import numpy as np

        # Check limits
        if limits is None:
            limits = self.limits

        # Generate linspace
        X = np.linspace(limits[0], limits[1], res)

        return X



