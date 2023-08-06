import numpy as np
from . import Linear
from typing import Tuple
from numpy import ndarray

class Polynomial(Linear):
    """
    Used to perform polynomial regression. Inherits from Linear. 
    This class does the work of creating a Vandermonde matrix 
    and using it in a multivariate Linear regression for you. 
    The order is specified by the user. The polynomial is in this order:
    y = a + bx + cx**2 + dx**3 ...

    Typical use:
        Dataset X[...,FitDim], Y[...,FitDim]

        P = Polynomial(X, Y, order)
        P.Fit()

    """
    _Order:int

    @property
    def Order(self) -> int:
        """The order of the polynomial."""
        return self._Order

    @Order.setter
    def Order(self, value:int):
        assert not self._initialized, "Can't change this property after instanciation"
        assert isinstance(value, int) and 0 < value, "Order of the polynomial must be an integer greater than 0"
        self._Order = value

    @property
    def Beta(self) -> ndarray:
        return super(Polynomial, self).Beta[...,0]

    @property
    def BetaFitError(self) -> ndarray:
        return super(Polynomial, self).BetaFitError[...,0]

    def __init__(self, x:ndarray, y:ndarray, order:int, fitDim:int=0, confidenceInterval:float=0.95, simult:bool=False,  rescale:bool=False):
        self._initialized=False
        self.Order = order
        super(Polynomial, self).__init__(self._polify(x), y.reshape(y.shape + (1,)), fitDim, confidenceInterval, simult, x.ndim, rescale)

    def _polify(self, x:ndarray) -> ndarray:
        """
        Makes a vandermonde matrix of the right polynomial order
        using the provided array. The required dimension will be appended
        at the end. 
        """
        
        out = np.zeros(x.shape + (self.Order+1,) )

        for i in range(self.Order+1):
            out[...,i] = x**i

        return out

    def Eval(self, x:ndarray) -> ndarray:
        return super(Polynomial, self).Eval(self._polify(x))[...,0]

    def EvalFitError(self, x:ndarray) -> ndarray:
        return super(Polynomial, self).EvalFitError(self._polify(x))[...,0]

    def EvalPredictionError(self, x:ndarray) -> ndarray:
        return super(Polynomial, self).EvalPredictionError(self._polify(x))[...,0]

    def _computeFitStats(self):
        self._Residuals = self.Y - super(Polynomial,self).Eval(self.X)
        self._SSE = np.sum(self._Residuals**2, axis=self.FitDim, keepdims=True)
        self._SST = np.sum((self.Y - np.mean(self.Y, axis=self.FitDim, keepdims=True))**2, axis=self.FitDim, keepdims=True)
        self._MSE = self.SSE / self.DoF
        self._R2 = 1 - self.SSE / self.SST
        self._AdjR2 = 1 - (1-self.R2) * (self.Nb - 1)/self.DoF

