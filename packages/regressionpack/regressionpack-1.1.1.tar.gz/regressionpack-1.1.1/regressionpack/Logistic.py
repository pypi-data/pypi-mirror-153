import numpy as np
from typing import Tuple
from .GenericCurveFit import GenericCurveFit
from numpy import ndarray

class Logistic(GenericCurveFit):
    
    def FitFunc(self, x:ndarray, a:float, b:float, c:float, d:float) -> ndarray:
        """
        An logistic function that goes like
        $$ y = \frac{a}{1 + e^{-b(x-c)}} + d $$
        """
        return a / (1 + np.exp(-b*(x-c))) + d

    def Jacobian(self, x:ndarray, a:float, b:float, c:float, d:float) -> ndarray:
        """
        The jacobian of the exponential fit function. 
        Meant to return a matrix of shape [x.shape[0], 3], where
        every column contains the derivative of the function with 
        respect to the fit parameters in order. 
        """
        out = np.zeros((x.shape[0],4))
        out[:,0] = 1/(1 + np.exp(-b*(x-c))) # df/da
        out[:,1] = a/(1 + np.exp(-b*(x-c)))**2 * -(x-c)*np.exp(-b*(x-c)) # df/db
        out[:,2] = a/(1 + np.exp(-b*(x-c)))**2 * b * np.exp(-b*(x-c)) # df/dc
        out[:,3] = 1 # df/dd

        return out

    def __init__(self, x:ndarray, y:ndarray, p0:ndarray=None, bounds=(-np.inf, np.inf), confidenceInterval:float=0.95, simult:bool=False, **kwargs):
        super(Logistic, self).__init__(x, y, self.FitFunc, self.Jacobian, p0, bounds, confidenceInterval, simult, **kwargs )