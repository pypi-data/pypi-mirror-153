import numpy as np
from regressionpack import Linear
from typing import Tuple
from regressionpack.utilities import MatMul, MatInv, MatDiag, MatFlip, Scaler
from numpy import ndarray

class Ellipse(Linear):

    _CanonicalBeta:ndarray
    _CanonicalBetaFitError:ndarray
    _CanonicalBetaPredictionError:ndarray

    def __init__(self, x:ndarray, y:ndarray, fitDim:int=0, confidenceInterval:float=0.95, simult:bool=False,  rescale:bool=False):

        # Create the intermediate vectors
        X = np.stack([x*x, x*y, y*y, x, y], axis=x.ndim)
        Y = np.ones(x.shape + (1,))

        # Use regular Linear regression
        super(Ellipse, self).__init__(X, Y, fitDim, confidenceInterval, simult, x.ndim, rescale)

    def _computeFitStats(self):
        """
        Computes various useful fit stats:
            Residuals:  The raw difference between the model and the data
            SSE:        Sum of squared errors
            SST:        Sum of Squared totals
            MSE:        Mean squared error
            R2:         Coefficient of determination
            AdjR2:      Adjusted coefficient of determination
            
        """
        self._Residuals = self.Y - super(Ellipse, self).Eval(self.X)
        self._SSE = np.sum(self._Residuals**2, axis=self.FitDim, keepdims=True)
        self._SST = 1 #np.sum( ( self.Y - np.mean(self.Y, axis=self.FitDim, keepdims=True) )**2, axis=self.FitDim, keepdims=True)
        self._MSE = self.SSE / self.DoF
        self._R2 = 1 - self.SSE / self.SST
        self._AdjR2 = 1 - (1-self.R2) * (self.Nb - 1)/self.DoF

    def _computeCanonicals(self):
        # Extract parameters
        A, B, C, D, E = [self.Beta[tuple([k if i == self.FitDim else slice(None) for i in range(self.X.ndim)])] for k in range(5)]
        F = -1 # All the other constants are normalized by F in this paper

        a, b, x0, y0, theta = Ellipse.FlatToCanonical(A, B, C, D, E, F)

        self._CanonicalBeta = np.stack([a, b, x0, y0, theta], axis = self.FitDim)

        # TODO: Propagate errors from BetaFitError to the canonicals
        self._computeCanonicalBetaFitError()

    def _computeCanonicalBetaFitError(self):

        # Grab the flat parameters and their errors for easier manipulations
        A, B, C, D, E = [self.Beta[tuple([k if i == self.FitDim else slice(None) for i in range(self.X.ndim)])] for k in range(5)]
        F = -1 # Having it -1 everywhere else and 1 here makes no sense...
        # Compute all the derivatives, yes this is a monster!
        dCandFlat = [
            # da/d ABCDE
            [
                np.sqrt(2)*np.sqrt((A + C + np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2)))*(-8*C*np.sqrt(B**2 + (A - C)**2)*(A + C + np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2)) + (4*A*C - B**2)*(-np.sqrt(B**2 + (A - C)**2)*(4*C*F - E**2)*(A + C + np.sqrt(B**2 + (A - C)**2)) + (A - C + np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2))))/(2*np.sqrt(B**2 + (A - C)**2)*(4*A*C - B**2)**2*(A + C + np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2))),
                np.sqrt(2)*np.sqrt((A + C + np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2)))*(4*B*np.sqrt(B**2 + (A - C)**2)*(A + C + np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2)) + (4*A*C - B**2)*(B*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2)) + np.sqrt(B**2 + (A - C)**2)*(2*B*F - D*E)*(A + C + np.sqrt(B**2 + (A - C)**2))))/(2*np.sqrt(B**2 + (A - C)**2)*(4*A*C - B**2)**2*(A + C + np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2))),
                -np.sqrt(2)*np.sqrt((A + C + np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2)))*(8*A*np.sqrt(B**2 + (A - C)**2)*(A + C + np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2)) + (4*A*C - B**2)*(np.sqrt(B**2 + (A - C)**2)*(4*A*F - D**2)*(A + C + np.sqrt(B**2 + (A - C)**2)) + (A - C - np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2))))/(2*np.sqrt(B**2 + (A - C)**2)*(4*A*C - B**2)**2*(A + C + np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2))),
                np.sqrt(2)*np.sqrt((A + C + np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2)))*(-B*E + 2*C*D)/(2*(4*A*C - B**2)*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2))),
                np.sqrt(2)*np.sqrt((A + C + np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2)))*(2*A*E - B*D)/(2*(4*A*C - B**2)*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2))),
            ],
            # db/d ABCDE
            [
                -np.sqrt(2)*np.sqrt((A + C - np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2)))*(8*C*np.sqrt(B**2 + (A - C)**2)*(A + C - np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2)) + (4*A*C - B**2)*(np.sqrt(B**2 + (A - C)**2)*(4*C*F - E**2)*(A + C - np.sqrt(B**2 + (A - C)**2)) + (A - C - np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2))))/(2*np.sqrt(B**2 + (A - C)**2)*(4*A*C - B**2)**2*(A + C - np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2))),
                np.sqrt(2)*np.sqrt((A + C - np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2)))*(4*B*np.sqrt(B**2 + (A - C)**2)*(A + C - np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2)) + (4*A*C - B**2)*(-B*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2)) + np.sqrt(B**2 + (A - C)**2)*(2*B*F - D*E)*(A + C - np.sqrt(B**2 + (A - C)**2))))/(2*np.sqrt(B**2 + (A - C)**2)*(4*A*C - B**2)**2*(A + C - np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2))),
                -np.sqrt(2)*np.sqrt((A + C - np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2)))*(8*A*np.sqrt(B**2 + (A - C)**2)*(A + C - np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2)) + (4*A*C - B**2)*(np.sqrt(B**2 + (A - C)**2)*(4*A*F - D**2)*(A + C - np.sqrt(B**2 + (A - C)**2)) + (-A + C - np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2))))/(2*np.sqrt(B**2 + (A - C)**2)*(4*A*C - B**2)**2*(A + C - np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2))),
                np.sqrt(2)*np.sqrt((A + C - np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2)))*(-B*E + 2*C*D)/(2*(4*A*C - B**2)*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2))),
                np.sqrt(2)*np.sqrt((A + C - np.sqrt(B**2 + (A - C)**2))*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2)))*(2*A*E - B*D)/(2*(4*A*C - B**2)*(A*E**2 - B*D*E + C*D**2 - F*(4*A*C - B**2))),
            ],
            # dx0/d ABCDE
            [
                -4*C*(B*E - 2*C*D)/(4*A*C - B**2)**2,
                (2*B*(B*E - 2*C*D) + E*(4*A*C - B**2))/(4*A*C - B**2)**2,
                -2*B*(2*A*E - B*D)/(16*A**2*C**2 - 8*A*B**2*C + B**4),
                -2*C/(4*A*C - B**2),
                B/(4*A*C - B**2),
            ],
            # dy0/d ABCDE
            [
                2*B*(B*E - 2*C*D)/(16*A**2*C**2 - 8*A*B**2*C + B**4),
                (-2*B*(2*A*E - B*D) + D*(4*A*C - B**2))/(4*A*C - B**2)**2,
                4*A*(2*A*E - B*D)/(4*A*C - B**2)**2,
                B/(4*A*C - B**2),
                -2*A/(4*A*C - B**2),
            ],
            # dtheta/d ABCDE
            [
                -B/(2*A**2 - 4*A*C + 2*B**2 + 2*C**2),
                (A/2 - C/2)/(A**2 - 2*A*C + B**2 + C**2),
                B/(2*(A**2 - 2*A*C + B**2 + C**2)),
                0,
                0,
            ]
        ]

        # Compute the error for all the canonicals by propagation
        dABCDE_fit = [self.BetaFitError[tuple([k if i == self.FitDim else slice(None) for i in range(self.X.ndim)])] for k in range(5)]
        dABCDE_pred = [self.BetaPredictionError[tuple([k if i == self.FitDim else slice(None) for i in range(self.X.ndim)])] for k in range(5)]

        err_fit_canon = [None for i in range(5)]
        err_pred_canon = [None for i in range(5)]

        # Iterate over canonicals
        for i in range(5):
            
            temp_fit = np.zeros(dCandFlat[i][0].shape)
            temp_pred = np.zeros(dCandFlat[i][0].shape)

            # Iterate over flats
            for k in range(5):
                # Sum the square of derivative times the error
                temp_fit += dCandFlat[i][k]**2 * dABCDE_fit[k]**2
                temp_pred += dCandFlat[i][k]**2 * dABCDE_pred[k]**2

            # Recover the square root
            err_fit_canon[i] = np.sqrt(temp_fit)
            err_pred_canon[i] = np.sqrt(temp_pred)

        # Stack them in the same array
        self._CanonicalBetaFitError = np.stack(err_fit_canon, axis = self.FitDim)
        self._CanonicalBetaPredictionError = np.stack(err_pred_canon, axis = self.FitDim)

    def Fit(self):
        super(Ellipse, self).Fit()
        self._computeCanonicals()

    def _ExpandPhi(self, phi:ndarray) -> ndarray:
        for i in range(self.X.ndim):
            if i != self.FitDim:
                phi = np.repeat(phi, self.X.shape[i], axis=i)

        return phi

    def Eval(self, nbPts:int=100) -> Tuple[ndarray, ndarray]:
        """Evaluates the fitted result and returns both x and y. 

        Args:
            nbPts (int, optional): Number of points to evaluate the ellipse at. Defaults to 100.

        Returns:
            Tuple[ndarray, ndarray]: The x and y values. 
        """

        # Grab the canonical parameters
        a, b, x0, y0, theta = [self.CanonicalBeta[tuple([k if i == self.FitDim else slice(None) for i in range(self.X.ndim)])] for k in range(5)]

        # Generate a 2pi around which to create the ellipse 
        phi = self._ExpandPhi(np.linspace(0,2*np.pi, nbPts).reshape([-1 if i == self.FitDim else 1 for i in range(self.X.ndim)]))
        
        return makeEllipse(a, b, x0, y0, theta, phi)

    def EvalFitError(self, nbPts:int=100) -> Tuple[Tuple[ndarray, ndarray], Tuple[ndarray, ndarray]]:
        """
        The means to generate the error here is not rigorous:
            I neglect the impact of the angle error, because: the angle 
            error will increase the closer a and b are from each-other, 
            which results in a circle. 

            I also neglect the error on the centre of the ellipse. 

            In the end, I only take into account the impact on a and b to generate
            two concentric ellipses. 
        """
        # Grab the canonical parameters
        a, b, x0, y0, theta = [self.CanonicalBeta[tuple([k if i == self.FitDim else slice(None) for i in range(self.X.ndim)])] for k in range(5)]
        da, db, dx0, dy0, dtheta = [self.CanonicalBetaFitError[tuple([k if i == self.FitDim else slice(None) for i in range(self.X.ndim)])] for k in range(5)]

        # Generate a 2pi around which to create the ellipse 
        phi = self._ExpandPhi(np.linspace(0,2*np.pi, nbPts).reshape([-1 if i == self.FitDim else 1 for i in range(self.X.ndim)]))

        # Deal with the case where uncertainty is bigger than the value
        # amin = max(a-da, 0)
        # bmin = max(b-db, 0)

        # return makeEllipse(amin, bmin, x0, y0, theta, phi), makeEllipse(a+da, b+db, x0, y0, theta, phi)

        x, y = makeEllipse(a, b, 0,0,0,phi)
        r = np.sqrt(x**2 + y**2)
        dr = 1/r * np.sqrt(a**2 * da**2 + b**2 * db**2)
        rmin = r-dr
        rmin[rmin < 0] = 0 # ensure no negatives
        rmax = r+dr

        x1min = np.cos(phi) * rmin
        x1max = np.cos(phi) * rmax
        y1min = np.sin(phi) * rmin
        y1max = np.sin(phi) * rmax

        x2min, y2min = rotate(x1min, y1min, theta)
        x2max, y2max = rotate(x1max, y1max, theta)

        return (x2min + x0, y2min + y0), (x2max + x0, y2max + y0)

    def EvalPredictionError(self, nbPts:int=100) -> ndarray:
        """
        Just as non-rigorous as the fit error. 
        """
        # Grab the canonical parameters
        a, b, x0, y0, theta = [self.CanonicalBeta[tuple([k if i == self.FitDim else slice(None) for i in range(self.X.ndim)])] for k in range(5)]
        da, db, dx0, dy0, dtheta = [self.CanonicalBetaPredictionError[tuple([k if i == self.FitDim else slice(None) for i in range(self.X.ndim)])] for k in range(5)]

        # Generate a 2pi around which to create the ellipse 
        phi = self._ExpandPhi(np.linspace(0,2*np.pi, nbPts).reshape([-1 if i == self.FitDim else 1 for i in range(self.X.ndim)]))

        # Deal with the case where uncertainty is bigger than the value
        # amin = max(a-da, 0)
        # bmin = max(b-db, 0)

        # return (makeEllipse(amin, bmin, x0, y0, theta, phi), makeEllipse(a+da, b+db, x0, y0, theta, phi))

        x, y = makeEllipse(a, b, 0,0,0,phi)
        r = np.sqrt(x**2 + y**2)
        dr = 1/r * np.sqrt(a**2 * da**2 + b**2 * db**2)
        rmin = r-dr
        rmin[rmin < 0] = 0 # ensure no negatives
        rmax = r+dr

        x1min = np.cos(phi) * rmin
        x1max = np.cos(phi) * rmax
        y1min = np.sin(phi) * rmin
        y1max = np.sin(phi) * rmax

        x2min, y2min = rotate(x1min, y1min, theta)
        x2max, y2max = rotate(x1max, y1max, theta)

        return (x2min + x0, y2min + y0), (x2max + x0, y2max + y0)
        
    @property
    def CanonicalBeta(self) -> ndarray:
        return self._CanonicalBeta

    @property
    def CanonicalBetaFitError(self) -> ndarray:
        return self._CanonicalBetaFitError

    @property
    def CanonicalBetaPredictionError(self) -> ndarray:
        return self._CanonicalBetaPredictionError

    @staticmethod
    def CanonicalToFlat(a:float, b:float, x0:float, y0:float, theta:float) -> Tuple[ndarray,ndarray,ndarray,ndarray,ndarray]:
        pass

    @staticmethod
    def FlatToCanonical(A:float, B:float, C:float, D:float, E:float, F:float=1) -> Tuple[ndarray,ndarray,ndarray,ndarray,ndarray]:
        """
        Converts the coefficients from 
        Ax^2 + Bxy + Cy^2 + Dx + Ey + F = 0

        into the canonical form, rotated by angle theta
        (x-x0)^2 / a^2 + (y-y0)^2 / b^2 = 1

        """
        ## From wikipedia
        a = -np.sqrt( 2 * (A*E**2 + C*D**2 - B*D*E + (B**2 - 4*A*C)*F) * ((A+C) + np.sqrt( (A-C)**2 + B**2) ) ) / (B**2 - 4*A*C)
        b = -np.sqrt( 2 * (A*E**2 + C*D**2 - B*D*E + (B**2 - 4*A*C)*F) * ((A+C) - np.sqrt( (A-C)**2 + B**2) ) ) / (B**2 - 4*A*C)
        x0 = (2*C*D - B*E)/(B**2 - 4*A*C)
        y0 = (2*A*E - B*D)/(B**2 - 4*A*C)
        theta = np.arctan2(C-A-np.sqrt((A-C)**2 + B**2), B)

        ## From Yan Zhan
        # theta = .5 * np.arctan2(B, A-C)
        # s = np.sin(theta)
        # c = np.cos(theta)

        # Ap = (A*c**2 + B*c*s + C*s**2)
        # Bp = (-2*A*c*s+(c**2 - s**2)*B + 2*C*c*s)
        # Cp = (A*s**2 - B*c*s + C*c**2)
        # Dp = (D*c + E*s)
        # Ep = (-D*s + E*c)
        # Fp = -1 + Dp**2/4/Ap + Ep**2/4/Cp

        # a = np.sqrt(Fp/Ap)
        # b = np.sqrt(Fp/Cp)

        # x0 = -c*Dp/2/Ap + s*Ep/2/Cp
        # y0 = -s*Dp/2/Ap - c*Ep/2/Cp

        return a, b, x0, y0, theta

def makeEllipse(a:ndarray, b:ndarray, x0:ndarray, y0:ndarray, theta:ndarray, phi:ndarray=np.linspace(0,2*np.pi, 100)) -> Tuple[ndarray, ndarray]:
    x, y = rotate(a*np.cos(phi), b*np.sin(phi), theta)
    return x+x0, y+y0

def rotate(x:ndarray, y:ndarray, theta:ndarray):
    return x * np.cos(theta) + y * np.sin(theta), x * np.sin(theta) - y*np.cos(theta)
