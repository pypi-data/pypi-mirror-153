import numpy as np
from .AbstractRegression import AbstractRegression
from typing import Tuple, Callable, Dict, Union
from .utilities import MatMul, MatInv, MatDiag, MatFlip, getOrder
from scipy.optimize import curve_fit
from inspect import signature
from numpy import ndarray

class GenericCurveFit(AbstractRegression):
    """
    This is a high level wrapper of the scipy curve_fit function
    that deals with the error-bars for you. For it to work, you have 
    to provide a tuple containing the analytical derivative
    of the fit function with respect to every fit parameter. 
    This will then be used to compute the errorbars, with the pcov matrix. 

    Because this fit is done using the least squares method, which is more 
    computationnally intensive than just solving a matrix equations, 
    it will only support one dataset at a time, meaning you will have to solve
    different datasets separately. 

    See https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
    for documentation on curve_fit. 

    This class can be used as is, with you providing the function and Jacobian, but
    I highly recommend that you create a class that inherits this class and implements
    the FitFunc and Jacobian inside it. See CosineFit.py for example. 

    """
    _FitFunc:Callable
    _Jacobian:Callable
    _Pcov:ndarray
    _P0:Union[Tuple[float], ndarray, None]
    _Bounds:Tuple[ndarray]
    _VARS:ndarray
    _kwargs:Dict

    @property
    def FitFunc(self) -> Callable:
        """
        The function used to fit the data. Same signature as the one used by scipy.curve_fit
        ydata = f(xdata, *params) + eps
        """
        return self._FitFunc

    @property
    def Jacobian(self) -> Callable:
        """
        Callable that returns the jacobian of the problem 
        """
        return self._Jacobian

    @property
    def Pcov(self) -> ndarray:
        """
        The pcov outputted from scipy.curve_fit. 
        """
        return self._Pcov

    @property
    def P0(self) -> Union[Tuple[float], ndarray]:
        """
        The initial guess for the fit parameters. 
        A tuple of the same length as the number of parameters. 
        """
        return self._P0

    @property
    def Bounds(self) -> Tuple[ndarray]:
        """
        The fit boundaries. A length-2 tuple containing the
        lower and upper bounds, which can be:
        (float, float)
        (ndarray, ndarray) # containing the bounds for every parameter

        The default value is (-np.inf, np.inf)
        """
        return self._Bounds

    @property
    def VARS(self) -> ndarray:
        """
        The variance of the fit parameters. 
        """
        return self._VARS

    def __init__(self, x:ndarray, y:ndarray, fitFunc:Callable, jacobian:Callable, p0:Union[Tuple[float,...],ndarray]=None, bounds=(-np.inf, np.inf), confidenceInterval:float=0.95, simult:bool=False, **kwargs):
        self._initialized = False
        self._FitFunc = fitFunc
        self._Jacobian = jacobian
        self._P0 = p0
        self._Bounds = bounds
        self._kwargs = kwargs

        assert x.ndim == 1 and y.ndim == 1, "Curve fitting only accepts one-dimensional data vectors"
        super(GenericCurveFit, self).__init__(x, y, len(signature(self.FitFunc).parameters) - 1, 0, confidenceInterval, simult)

    def Fit(self):

        self._Beta, self._Pcov = curve_fit(self.FitFunc, self.X, self.Y, self.P0, jac=self.Jacobian, bounds=self.Bounds, **self._kwargs)
        self._computeFitStats()
        self._VARS = np.diag(self.Pcov).reshape((1, -1))

        self._BetaFitError = self.Student * np.sqrt(self.VARS*self.MSE).flatten()

    def Eval(self, x:ndarray) -> ndarray:
        return self.FitFunc(x, *self.Beta)

    def EvalFitError(self, x:ndarray) -> ndarray:
        return self.Student * np.sqrt( np.sum(  (self.VARS * self.Jacobian(x,*self.Beta))**2, axis=1 ) * self.MSE )

    def EvalPredictionError(self, x:ndarray) -> ndarray:
        return self.Student * np.sqrt( ( 1 + np.sum(  (self.VARS * self.Jacobian(x,*self.Beta))**2, axis=1 ) ) * self.MSE )