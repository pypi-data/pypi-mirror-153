import numpy as np
from .AbstractRegression import AbstractRegression
from typing import Tuple
from .utilities import MatMul, MatInv, MatDiag, MatFlip, Scaler
from numpy import ndarray

class Linear(AbstractRegression):
    """
    Used to perform multivariate linear regressions. 

    Typical use involves:
        a matrix of independant variables X[...,F, P]
        a matrix of dependant variable Y[...,F, 1]
        where F is the number of points in the Fit Dimension (FitDim)
        and P is the number of parameters in the Parameters Dimension (ParmDim)

        For example, one could have a 2D X matrix with columns: age, height
        and another 2D matrix (but only one column) for Y: weight

        Note that this package allows the FitDim and ParmDim to be elsewhere than at the
        end, in which case the user must specify which dimensions fill that purpose. 

        L = Linear(X, Y)
        L.Fit()

        Fitted constants and their errors are found in
        Beta
        BetaFitError
        BetaPredictionError

        Evaluating the function using given input matrix X' is done using
        Eval(X)
        EvalFitError(X)
        EvalPredictionError(X)

    """
    _Xt:ndarray
    _XtXinv:ndarray
    _ParmDim:int
    _Rescale:bool
    _Scaler:Scaler
    _Xscaled:ndarray
    _Omega:ndarray

    @property
    def ParmDim(self) -> int:
        """
        The dimension containing the parameters. 
        """
        return self._ParmDim

    @ParmDim.setter
    def ParmDim(self, value:int):
        assert not self._initialized, "Can't change this property after instanciation"
        assert -self._X.ndim <= value < self._X.ndim, "Specified dimension must respect -X.ndim <= ParmDim < X.ndim"
        assert value % self._X.ndim != self.FitDim, "Cannot use the same dimension for both ParmDim and FitDim"
        self._ParmDim = value % self._X.ndim
        
    @property
    def Axis(self) -> Tuple[int,int]:
        """
        Returns a tuple containing (FitDim, ParmDim)
        """
        return (self.FitDim, self.ParmDim)

    def __init__(self, x:ndarray, y:ndarray, fitDim:int=-2, confidenceInterval:float=0.95, simult:bool=False, parmDim:int=-1, rescale:bool=False):
        
        # Instanciate using superclass constructor
        super(Linear, self).__init__(x, y, x.shape[parmDim], fitDim, confidenceInterval, simult)
        
        # Unlock modifying properties
        self._initialized = False

        # The add the missing properties
        self.ParmDim = parmDim
        self._Rescale = rescale

        if self._Rescale:
            self._Scaler = Scaler(x, axis=fitDim)

        # Re-lock modifying properties
        self._initialized = True

    def _computeXtXinv(self):
        """
        Computes the most useful intermediate matrices
        used in a Linear regression. 
        """
        if self._Rescale:
            self._Xscaled = self._Scale(self._X)
            
            self._Xt = MatFlip(self._Xscaled, (self.FitDim, self.ParmDim))
            self._XtXinv = MatInv(MatMul(self._Xt, self._Xscaled, self.Axis), self.Axis)

            self._Omega = MatMul(self._XtXinv, self._Xt, self.Axis)
        else:
            self._Xt = MatFlip(self._X, (self.FitDim, self.ParmDim))
            self._XtXinv = MatInv(MatMul(self._Xt, self._X, self.Axis), self.Axis)

    def Fit(self):
        self._computeXtXinv()
        self._Beta = MatMul( MatMul(self._XtXinv, self._Xt, self.Axis), self._Y, self.Axis )
        self._computeFitStats()
        self._BetaFitError = self.Student * np.sqrt( MatDiag(self._XtXinv, tuple(reversed(self.Axis))) * self.MSE )
        self._BetaPredictionError = self.Student * np.sqrt( MatDiag(self._XtXinv + 1, tuple(reversed(self.Axis))) * self.MSE )

    def Eval(self, x:ndarray) -> ndarray:
        """
        Evaluates the fitted function using the values of the
        input array x. 
        """
        if self._Rescale:
            xs = self._Scale(x)
            assert xs.ndim == self._X.ndim, "Must match the number of dimensions of the training data"
            assert all([xs.shape[i] == self._X.shape[i] for i in range(self._X.ndim) if i != self.FitDim]), "All dimensions other than the fit dimension must match"
            return MatMul(xs, self._Beta, self.Axis)
        else:
            assert x.ndim == self._X.ndim, "Must match the number of dimensions of the training data"
            assert all([x.shape[i] == self._X.shape[i] for i in range(self._X.ndim) if i != self.FitDim]), "All dimensions other than the fit dimension must match"
            return MatMul(x, self._Beta, self.Axis)

    def EvalFitError(self, x:ndarray) -> ndarray:
        """
        The error on the fit. This one is smaller
        and represents where the real curve likely sits, within the
        current confidence interval. 
        """
        if self._Rescale:
            xs = self._Scale(x)
            return self.Student * np.sqrt( MatDiag( MatMul( MatMul(xs, self._XtXinv, self.Axis), MatFlip(xs, self.Axis), self.Axis ), tuple(reversed(self.Axis)) ) * self.MSE )
        else:
            return self.Student * np.sqrt( MatDiag( MatMul( MatMul(x, self._XtXinv, self.Axis), MatFlip(x, self.Axis), self.Axis ), tuple(reversed(self.Axis)) ) * self.MSE )

    def EvalPredictionError(self, x:ndarray) -> ndarray:
        """
        The prediction interval. This one is bigger and represents
        where a new data point is likely to be found, within the 
        current confidence interval. 
        """
        if self._Rescale:
            xs = self._Scale(x)
            return self.Student * np.sqrt( MatDiag( 1 + MatMul( MatMul(xs, self._XtXinv, self.Axis), MatFlip(xs, self.Axis), self.Axis ), tuple(reversed(self.Axis)) ) * self.MSE )
        else:
            # Using the reversed axis in the MatDiag ensures that the dimension that gets removed at the end in Polynomial is the "hidden" one that contains the poly variables
            return self.Student * np.sqrt( MatDiag( 1 + MatMul( MatMul(x, self._XtXinv, self.Axis), MatFlip(x, self.Axis), self.Axis ), tuple(reversed(self.Axis)) ) * self.MSE )

    # Override
    @property
    def Beta(self) -> ndarray:
        """
        The fitted parameters. 
        """
        if self._Rescale:
            """
            Omega = (X^T X)^(-1) X^T
            beta = (Omega X)^(-1) beta'
            """
            #Omega = MatMul(self._XtXinv, self._Xt, self.Axis)
            return MatMul(MatInv(MatMul(self._Omega, self._X, self.Axis), self.Axis), self._Beta, self.Axis)
        else:
            return self._Beta

    @property
    def BetaFitError(self) -> ndarray:
        """
        The error on the fit parameters. This one is smaller
        and represents where the real estimators likely sits, within the
        current confidence interval. 
        """
        if self._Rescale:
            # Not sure if this is right, though! Will have to verify!
            return MatMul(MatInv(MatMul(self._Omega, self._X, self.Axis), self.Axis), self._BetaFitError, self.Axis)
        else:
            return self._BetaFitError

    @property
    def BetaPredictionError(self) -> ndarray:
        """
        The prediction error on the fit parameters. Not sure if this is legit yet, 
        but I computed it in a similar way than what is used for the EvalPredictionError. 
        """
        if self._Rescale:
            # Not sure if this is right, though! Will have to verify!
            return MatMul(MatInv(MatMul(self._Omega, self._X, self.Axis), self.Axis), self._BetaPredictionError, self.Axis)
        else:
            return self._BetaPredictionError

    def _Scale(self, x:ndarray) -> ndarray:
        # Wraps the rescaling to have it in a one liner, including the replacing infs with 1.0
        temp = self._Scaler.Scale(x)
        temp[~np.isfinite(temp)] = 1.0
        return temp