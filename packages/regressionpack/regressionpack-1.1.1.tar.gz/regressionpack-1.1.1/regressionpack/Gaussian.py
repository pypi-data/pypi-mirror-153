import numpy as np
from typing import Tuple
from .GenericCurveFit import GenericCurveFit
from numpy import ndarray

class Gaussian(GenericCurveFit):
    
    def FitFunc(self, x:ndarray, a:float, b:float, c:float, d:float) -> ndarray:
        """
        An exponantial function that goes like
        $$ y = a e^{-b*(x-c)^2} + d $$
        """
        return a * np.exp(-b * (x-c)**2) + d

    def Jacobian(self, x:ndarray, a:float, b:float, c:float, d:float) -> ndarray:
        """
        The jacobian of the exponential fit function. 
        Meant to return a matrix of shape [x.shape[0], 3], where
        every column contains the derivative of the function with 
        respect to the fit parameters in order. 
        """
        out = np.zeros((x.shape[0],4))
        out[:,0] = np.exp(-b * (x-c)**2)    # df/da
        out[:,1] = -a*(x-c)**2 * out[:,0]   # df/db
        out[:,2] = 2*a*b*(x-c) * out[:,0]   # df/dc
        out[:,3] = 1                        # df/dd

        return out

    def __init__(self, x:ndarray, y:ndarray, p0:ndarray=None, bounds=(-np.inf, np.inf), confidenceInterval:float=0.95, simult:bool=False, **kwargs):
        super(Gaussian, self).__init__(x, y, self.FitFunc, self.Jacobian, p0, bounds, confidenceInterval, simult, **kwargs )