import numpy as np
from .GenericCurveFit import GenericCurveFit
from scipy.signal import lsim, TransferFunction
from .utilities import NumericalJacobian
from numpy import ndarray

class SystemIdentification(GenericCurveFit):
    """
    Used to fit a transfer function of the shape

    F(s) = ( b[n]*s**n + b[n-1]*s**(n-1) + ... + b[1]*s + b[0] ) / ( s**n + a[n-1]*s**(n-1) + ... + a[1]*s + a[0] )

    on a time-domain data set. The transfer function numerator and denominator polynomials are used to find the poles and residues (r, p)
    of this fraction. It comes down to decomposing F(s) in partial fractions of the shape

    F(s) = r[i] * factorial(n[i]) / (s + p[i])**(n[i] + 1)

    which is easily converted into exponentials

    f(t) = r[i] * t**n[i] * exp(p[i] * t) / factorial(n[i])

    and fitted onto the data. 
    
    """
    _tol:float
    _nbDen:int
    _nbNum:int
    _time:ndarray
    _TransferFunction:TransferFunction

    @property
    def TransferFunction(self) -> TransferFunction:
        return TransferFunction(self.Numerator, self.Denominator)

    @property
    def Numerator(self) -> ndarray:
        return self.Beta[:self._nbNum]

    @property
    def NumeratorError(self) -> ndarray:
        return self.BetaFitError[:self._nbNum]

    @property
    def Denominator(self) -> ndarray:
        return np.hstack((1, self.Beta[self._nbNum:]))

    @property
    def DenominatorError(self) -> ndarray:
        return np.hstack((0, self.BetaFitError[self._nbNum:]))

    def _FitFunc(self, x:ndarray, *args:float) -> ndarray:
        # return self._laplace2time(x, *args)
        # num, den = args[:self._nbNum], (1,) + args[self._nbNum:]
        # _, c, _ = lsim(TransferFunction(num, den), x, self._time)
        # return c
        return self._FitFuncWithTime(self._time, x, *args)

    def _FitFuncWithTime(self, t:ndarray, x:ndarray, *args:float) -> ndarray:
        num, den = args[:self._nbNum], (1,) + args[self._nbNum:]
        _, c, _ = lsim(TransferFunction(num, den), x, t)
        return c

    def _Jacobian(self, x:ndarray, *args:float) -> ndarray:
        """
        Using a homemade numerical jacobian. This one cannot be done analytically -- 
        at least that I know of -- because of the use of numerical residue-finding function. 
        If there is a way to do this analytically, I'm very intrigued and eager to learn it. 
        """
        return NumericalJacobian(self.FitFunc, x, args)
    
    def __init__(self, t: ndarray, x:ndarray, y:ndarray, nbNum:int, nbDen:int, tol:float=1e-3, p0:ndarray=None, bounds=(-np.inf, np.inf), confidenceInterval:float=0.95, simult:bool=False, **kwargs):
        assert nbDen > nbNum, "The denominator must have a higher order than the numerator. "
        self._nbNum = nbNum
        self._nbDen = nbDen
        self._time = t
        if p0 is not None:
            assert p0.size == self._nbNum + self._nbDen - 1
        else:
            p0 = np.ones((self._nbDen + self._nbNum - 1,))

        self._tol = tol # tolerance for residue finding, also used for gradient calculation

        super(SystemIdentification, self).__init__(x, y, self.FitFunc, self.Jacobian, p0, bounds, confidenceInterval, simult, **kwargs )

    def ForcedResponse(self, t: ndarray, x: ndarray) -> ndarray:
        """
        Generalized the evaluation to allow the user to try arbitrary 
        inputs with potentially different time vectors. 
        """
        _, c, _ = lsim(self.TransferFunction, x, t)
        return c

    def ForcedResponseFitError(self, t:ndarray, x:ndarray) -> ndarray:
        localFunc = lambda x, *args: self._FitFuncWithTime(t, x, *args)
        J = NumericalJacobian(localFunc, x, self.Beta)
        return self.Student * np.sqrt( np.sum(  (self.VARS * J )**2, axis=1 ) * self.MSE )

    def ForcedResponsePredictionError(self, t:ndarray, x:ndarray) -> ndarray:
        localFunc = lambda x, *args: self._FitFuncWithTime(t, x, *args)
        J = NumericalJacobian(localFunc, x, self.Beta)
        return self.Student * np.sqrt( ( 1 + np.sum(  (self.VARS * J)**2, axis=1 ) ) * self.MSE )
