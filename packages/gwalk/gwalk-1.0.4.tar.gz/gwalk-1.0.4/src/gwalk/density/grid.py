'''Grids for direct evaluation fits
'''

class Grid(object):
    '''\
    Mesh object
    '''
    def __init__(
                 self,
                 Y,
                 lnL,
                 limits,
                ):
        '''Initialize a mesh object

        Parameters
        ----------
        Y: array like, shape = (npts,ndim)
            Input Samples to fit
        L: array like, shape = (npts,)
            Input sample likelihood values
        std: array like, shape = (ndim,)
            Input sample variance, useful for some things
        limits: array like, shape = (2,ndim)
            Input limits for space of mesh
        '''
        # Imports
        import numpy as np
        # Exponentiate likelihood
        L = np.exp(lnL)
        # Downselect data
        keep = L > 0
        Y = Y[keep]
        L = L[keep]
        lnL = lnL[keep]
        # Normalize
        Lsum = np.sum(L)
        lnLsum = np.log(Lsum)
        # Save data
        self.Y = Y
        self.L = L/Lsum
        self.lnL = lnL - lnLsum

        # Hold onto these
        self.ndim = Y.shape[1]
        self.mean = np.average(Y,weights=L,axis=0)
        self.cov = np.cov(Y.T,aweights=L)
        self.std = np.sqrt(np.diag(self.cov))
        self.limits = limits

    def polyfit_mu_sig_1d(self, x, y, sig_default, limits):
        '''\
        Return polynomial coefficients or best guess

        Parameters
        ----------
        x: array like, shape = (npts,)
            Input space values
        y: array like, shape = (npts,)
            Input function values
        sig_default: float
            Input default value of sigma
        limits: array like, shape = (2,)
            Input limits for x space
        '''
        # Imports 
        import numpy as np
        # Call polyfit
        a, b, c = np.polyfit(x,y,2)
        # check if a is viable
        if a < 0:
            # Use polynomial coefficients
            mu = -(0.5*b/a)
            sig = -0.5/a
        else:
            # Use maximum of data
            x = x[1:-1]
            y = y[1:-1]
            mu = x[np.argmax(y)]
            sig = sig_default
        # check limits
        if (mu < limits[0]) or (mu > limits[1]):
            # Use maximum of data
            x = x[1:-1]
            y = y[1:-1]
            mu = x[np.argmax(y)]

        return mu, sig

    ######## MultivariateNormal tools ########

    #### Call Constructor ####
    def construct_nal(
                      self,
                      seed=0,
                      sig_max=None,
                      labels=None,
                     ):
        ''' Construct a bounded multivariate normal model

        Parameters
        ----------
        seed: int, optional
            Input seed for random state
        sig_max: float, optional
            Input maximum sigma parameters, relative to scale
        '''
        # Imports
        import numpy as np
        from gwalk.model.parameter import Parameter
        from gwalk.bounded_multivariate_normal import MultivariateNormal
        # Initialize parameter list
        params = []
        # Loop parameters
        for i in range(self.ndim):
            # Pick a parameter guess
            guess = (self.limits[i][1] + self.limits[i][0])/2

            # Pick a label
            if labels is None:
                label = None
            else:
                label = labels[i]

            # Construct parameter 
            p = Parameter("p_%d"%i,guess,self.limits[i],label)
            params.append(p)

        # Construct Bounded Multivariate Normal object
        MV = MultivariateNormal(
                                params,
                                self.std,
                                seed,
                                sig_max,
                               )
        return MV

    def nal_save_kl(
                    self,
                    MV,
                    fname_nal,
                    label,
                    attrs=None,
                    mode='mean',
                    better='False',
                   ):
        '''Save MV object with kl divergence
        
        Parameters
        ----------
        MV: MultivaraiteNormal object
            Input bounded multivariate normal object
        fname_nal: str
            Input file location for nal fits
        label: str
            Input path to fit group
        attrs: dict, optional
            Input additional attributes to save with nal fit
        better: bool, optional
            Input save fit only if better?
        '''
        # Imports
        from gwalk.bounded_multivariate_normal import MultivariateNormal
        # Initialize attrs if none
        if attrs is None:
            attrs = {}
        # Get kl divergence
        attrs["kl"] = self.nal_kl_div(MV,MV.read_guess(),mode=mode).flatten()
        # Check for better
        if better:
            # Check if the fit already exists
            if MV.exists(fname_nal, label):
                # Load the existing fit
                MVexist = MultivariateNormal.load(fname_nal, label)
                # check MVexist[kl]
                kl_exist = self.nal_kl_div(MVexist,MVexist.read_guess(),mode=mode).flatten()
                # If kl_exist is lower than kl, return
                if kl_exist < attrs["kl"]:
                    return
        # Save fit
        MV.save(fname_nal, label, attrs=attrs)

    #### Convergence ####
    def nal_kl_div(
                   self,
                   MV,
                   X=None,
                  ):
        ''' Calculate the KL Divergence for a set of parameters

        Parameters
        ----------
        MV: MultivariateNormal object
            Input bounded multivariate normal object
        X: array like, shape = (npts, nparams),optional
            Input test params for kl divergence
        '''
        # Imports 
        import numpy as np
        from relative_entropy_cython import relative_entropy_alt
        # Use built in value for X
        if X is None:
            X = MV.read_guess()
        ## Prep ##
        X = MV.check_sample(X)
        ## Calculate kl divergences ##
        # Get lnL_norm
        lnL_norm = MV.likelihood(
                                 self.Y,
                                 X=X,
                                 scale=MV.scale,
                                 log_scale=True,
                                )

        # Calculate the kl divergence
        kl = relative_entropy_alt(self.L, self.lnL, lnL_norm)
        return kl

    def nal_kl_opt_fn(self,MV,k=-1.):
        ''' Return a function which evaluates the kl divergence given params

        Parameters
        ----------
        MV: MultivariateNormal object
            Input bounded multivariate normal object
        k: float, optional
            Input power of kl divergence
        '''
        import numpy as np
        def kl_div(X):
            kl = self.nal_kl_div(MV,X=X)
            return np.power(kl,k)
        return kl_div

    #### Guessing ####
    def nal_grid_guesses(
                         self,
                         MV,
                        ):
        ''' Fit the bounded multivariate normal model to the grid
        
        Parameters
        ----------
        MV: MultivariateNormal object
            Input some initialized Multivariate Normal object
        '''
        # Imports 
        import numpy as np
        from gwalk.utils.multivariate_normal import params_of_mu_cov
        # Identify number of guesses
        n_guess = 2
        # Generate simple guess
        _mu_scaled = self.mean/self.std
        _cov_scaled = self.cov/np.outer(self.std,self.std)
        Xs = params_of_mu_cov(_mu_scaled,_cov_scaled)
        # Initialize guesses
        Xg = np.tile(MV.read_guess(),(n_guess,1))
        Xg[1] = Xs
        '''
        # Generate 1D evaluation guesses
        for i in range(self.ndim):
            y_test = y_test[keep].flatten()/MV.scale[i]
            L_test = np.log(L_test[keep].flatten())
            # Find maximum
            mu, sig = self.polyfit_mu_sig_1d(y_test, L_test, X[i+self.ndim], self.limits[i])
            Xg[0,i] = mu
            Xg[0,i+self.ndim] = sig

        # Generate 1D training guesses
        for i in range(self.ndim):
            # Load values
            y_train = self.marginals["1d_%d_x_train"%i]
            L_train = self.marginals["1d_%d_y_train"%i]
            bins = int(self.marginals["1d_%d_bins"%i])

            # Rescale training set 1
            y_train_1 = y_train[:bins].flatten()/MV.scale[i]
            L_train_1 = L_train[:bins].flatten()
            keep_1 = L_train_1 > 0
            y_train_1 = y_train_1[keep_1]
            L_train_1 = np.log(L_train_1[keep_1])
            # Rescale training set 2
            y_train_2 = y_train[bins:].flatten()/MV.scale[i]
            L_train_2 = L_train[bins:].flatten()
            keep_2 = L_train_2 > 0
            y_train_2 = y_train_2[keep_2]
            L_train_2 = np.log(L_train_2[keep_2])

            # fit training set 1
            mu, sig = self.polyfit_mu_sig_1d(y_train_1, L_train_1, X[i+self.ndim], self.limits[i])
            Xg[1,i] = mu
            Xg[1,i+self.ndim] = sig

            # fit training set 2
            mu, sig = self.polyfit_mu_sig_1d(y_train_2, L_train_2, X[i+self.ndim], self.limits[i])
            Xg[2,i] = mu
            Xg[2,i+self.ndim] = sig
        '''

        return Xg


    #### Initialization ####
    def nal_init_walkers(
                         self,
                         MV,
                         nwalk,
                         Xg=None,
                         f_opt=None,
                         sig_multiplier=3,
                         sig_min=1e-5,
                        ):
        '''Initialize random walkers for bounded normal fit optimization

        Parameters
        ----------
        MV: MultivariateNormal object
            Input bounded multivariate normal object
        nwalk: int
            Input number of random walkers to initialize
        Xg: array like, shape = (npts, nparams), optional
            Input parameters for guesses
        f_opt: function, optional
            Input likelihood function for likelihood evaluation
        sig_multiplier: float, optional
            Input used for generating initial guesses
        '''
        # Imports 
        import numpy as np
        
        ## Check inputs ##
        # Initialize optimization function
        if f_opt is None:
            f_opt = self.nal_kl_opt_fn(MV)

        # Initialize guesses
        if Xg is None:
            Xg = self.nal_grid_guesses(MV)
        Xg = MV.check_sample(Xg)
        # Determine guess goodness
        Lg = f_opt(Xg)
        keep = Lg > 0.
        # Downselect guesses
        Xg = Xg[keep]
        Lg = Lg[keep]

        # Determine number of guesses
        nguess = Xg.shape[1]

        # Sort guesses
        sort_index = np.argsort(Lg)[::-1]
        Xg = Xg[sort_index]
        Lg = Lg[sort_index]

        # If we have more guesses than we need, return the number we need
        if not (nguess <= nwalk):
            Xg = Xg[:nwalk]
            return Xg

        # If we have less guesses than we need, generate new guesses
        while nguess < nwalk:
            # Generate new random guesses
            mu = np.average(Xg,axis=0)
            sig = sig_multiplier*np.std(Xg,axis=0)
            sig[sig < sig_min] = sig_min
            Xn = mu + MV.rs.randn(nwalk-nguess,Xg.shape[1])*sig
            #Xn = MV.sample_uniform_unconstrained(nwalk - nguess)
            k = MV.satisfies_constraints(Xn)
            Xk = Xn[k]
            Xg = np.append(Xg,Xk,axis=0)
            nguess = Xg.shape[0]

        return Xg

    #### Fit methods ####

    def nal_fit_to_samples(self,MV,**kwargs):
        ''' Fit the bounded multivariate normal model to some samples
        Parameters
        ----------
        MV: MultivariateNormal object
            Input some initialized Multivariate Normal object
        '''
        # Imports
        import numpy as np
        from gwalk.utils.multivariate_normal import params_of_mu_cov
        # Generate simple guess
        _mu_scaled = self.mean/self.std
        _cov_scaled = self.cov/np.outer(self.std,self.std)
        Xs = params_of_mu_cov(_mu_scaled,_cov_scaled)
        # Fit to samples
        MV.assign_guess(Xs)
        return MV

    def nal_genetic_step(
                         self,
                         MV,
                         cur,
                         f_opt,
                         nwalk,
                         carryover = 0.03,
                         sig_factor = 1.0,
                        ):
        '''Draw a new step randomly within bounds, compare the likelihood
        Parameters
        ----------
        MV: MultivariateNormal object
            Input bounded multivariate normal object
        cur: array like, shape = (npts, nparams), optional
            Input parameters for guesses
        f_opt: function
            Input likelihood function for likelihood evaluation
        nwalk: int
            Input number of random walkers to initialize
        carryover: float, optional
            Input carryover fraction for genetic algorithm
        sig_factor: float, optional
            Input number of sigma to vary new guesses by
        '''
        ## Imports ##
        # Public
        import numpy as np
        from scipy.stats import multivariate_normal
        import time

        # Use variance of guesses to determine jump scale
        sig = np.std(cur, axis=0)

        # Generate parameter likelihood
        Lcur = f_opt(cur)
        keep = Lcur > 0

        # Identify best guesses
        n_carry = int(carryover*nwalk)
        if n_carry > np.sum(keep):
            n_carry = np.sum(keep)
        carry_index = np.argsort(Lcur)[-n_carry:]
        carry = cur[carry_index]
        Lcarry = Lcur[carry_index]

        ## Breeding ##
        # The breeding pool excludes candidates with fitness zero
        Xb = cur[keep].copy()
        Lb = Lcur[keep]
        Lb /= np.sum(Lb)
        # Pick random parents
        p1 = MV.rs.choice(np.arange(Xb.shape[0]),size=nwalk,p=Lb)
        p2 = MV.rs.choice(np.arange(Xb.shape[0]),size=nwalk,p=Lb)
        '''
                choices[j] = MV.rs.choice(
                       [True,False],
                       p=[
                          Lb_p[p1[i]][j]/Lb_p_sum[j],
                          Lb_p[p2[i]][j]/Lb_p_sum[j],
                         ]
                      )
            cur[i,choices] =  cur[p1][i,choices]
        '''
        choices = MV.rs.choice([True,False],size=Xb.shape)
        cur[choices] = cur[p1][choices]
        cur[~choices] = cur[p2][~choices]
        # Re-evaluate likelihood
        Lcur = f_opt(cur)

        # Hold best guesses over through breeding
        drop_index = np.argsort(Lcur)[:n_carry]
        cur[drop_index] = carry
        Lcur[drop_index] = Lcarry
        # Identify new best guesses
        carry_index = np.argsort(Lcur)[-n_carry:]
        carry = cur[carry_index]
        Lcarry = Lcur[carry_index]

        ## Generate new steps ##
        # loop through each random walker
        new = cur + MV.rs.randn(nwalk,cur.shape[1])*sig*sig_factor
        keep = MV.satisfies_constraints(new)
        new[~keep] = cur[~keep]

        # Determine the likelihood of the new guess
        Lnew = f_opt(new)

        # Determine alpha
        alpha = Lnew/Lcur

        # Decide if to jump
        jumpseed = (MV.rs.uniform(size=nwalk) > (1 - alpha)).astype(bool)
        jumpseed[Lcur==0] = True

        # Jump
        new[~jumpseed] = cur[~jumpseed]
        Lnew[~jumpseed] = Lcur[~jumpseed]

        # Hold best guesses
        drop_index = np.argsort(Lnew)[:n_carry]
        new[drop_index] = carry
        Lnew[drop_index] = Lcarry

        return new, Lnew

    #### Random Walk Algorithms ####

    def nal_fit_random_walk(
                            self,
                            MV,
                            cur,
                            f_opt = None,
                            nwalk=100,
                            nstep=100,
                            carryover=0.03,
                            sig_factor=1.0,
                           ):
        '''\
        Begin using a random walk to find the MLE value for our model
        Parameters
        ----------
        MV: MultivariateNormal object
            Input bounded multivariate normal object
        cur: array like, shape = (npts, nparams), optional
            Input parameters for guesses
        f_opt: function, optional
            Input likelihood function for likelihood evaluation
        nwalk: int, optional
            Input number of random walkers to initialize
        nstep: int, optional
            Input number of steps for random walkers
        carryover: float, optional
            Input carryover fraction for genetic algorithm
        sig_factor: float, optional
            Input number of sigma to vary new guesses by
        '''
        ## Imports ##
        # Public
        import time
        import numpy as np
        ## Check inputs ##
        # Initialize optimization function
        if f_opt is None:
            f_opt = self.nal_kl_opt_fn(MV)

        # Initialize the best fit
        Lcur = f_opt(cur)
        index = np.argmax(Lcur)
        best_guess = cur[index].copy()
        Lbest = Lcur[index]

        # Do the fit
        for i in range(nstep):
            cur, Lcur = \
                self.nal_genetic_step(
                                      MV,
                                      cur,
                                      f_opt,
                                      nwalk,
                                      carryover=carryover,
                                      sig_factor=sig_factor,
                                     )
            # Testing
            if np.max(Lcur) > Lbest:
                j = np.argmax(Lcur)
                if MV.satisfies_constraints(cur[j,:]):
                    best_guess = cur[j,:].copy()
                    Lbest = Lcur[j].copy()

        # Assign the best guess!
        MV.assign_guess(best_guess)#, force=True)

        return

