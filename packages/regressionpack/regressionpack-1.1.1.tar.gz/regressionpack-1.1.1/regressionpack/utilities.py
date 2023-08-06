import numpy as np
from typing import Callable, Tuple
from numpy import ndarray
from scipy.linalg import eig

def _parseAxis(A:ndarray, axis:Tuple[int,int]) -> Tuple[int,int]:
    assert all([-A.ndim <= x < A.ndim for x in axis]), "Specified dimension must respect -X.ndim <= ParmDim < X.ndim"
    return tuple([x % A.ndim for x in axis])

def getOrder(A:ndarray, axis:Tuple[int,int]=(-2,-1)) -> Tuple[Tuple[int,...],Tuple[int,...]]:

    axis = _parseAxis(A, axis)
    # Define how the axis are to be re-ordered (must put the axis of interest in the last two positions)
    order = tuple([x for x in range(A.ndim) if x not in axis]) + axis

    # Define how to re-order the result at the end
    reorder = list()
    counter = 0
    for i in range(A.ndim):
        if i == axis[0]:
            reorder.append(A.ndim-2)
        elif i == axis[1]:
            reorder.append(A.ndim-1)
        else:
            reorder.append(counter)
            counter += 1

    return order, tuple(reorder)

def MatMul(A:ndarray, B:ndarray, axis:Tuple[int,int]=(-2,-1)) -> ndarray:
        """
        Computes the matrix product between the chosen two axis. By default, it will
        use the last two. 
        """

        parsedAxis = _parseAxis(A, axis)

        # Shortcut if the axis are the last two
        if parsedAxis == (A.ndim-2, A.ndim-1):
            return np.matmul(A, B)

        # Find how to reorder these
        order, reorder = getOrder(A, parsedAxis)

        # Compute and return the result
        return np.matmul(A.transpose(order), B.transpose(order)).transpose(reorder)

def MatInv(A:ndarray, axis:Tuple[int,int]=(-2,-1), rcond:float = 1e-15) -> ndarray:
    """
    Compute the inverse of the matrix on the two axis of interest. 
    By default uses the last two axis
    
    Now using inv instead of pinv. This is more restrictive in that it will 
    only work on square matrices, but will yield more precise results. 
    """
    axis = _parseAxis(A, axis)

    # Shortcut if the axis are the last two
    if axis == (A.ndim-2, A.ndim-1):
        #return np.linalg.pinv(A, rcond=rcond)
        return np.linalg.inv(A)

    # Find how to reorder these
    order, reorder = getOrder(A, axis)

    # Compute and return the result
    # return np.linalg.pinv(A.transpose(order), rcond=rcond).transpose(reorder)
    return np.linalg.inv(A.transpose(order)).transpose(reorder)

def MatDiag(A:ndarray, axis:Tuple[int,int]=(-2,-1)) -> ndarray:
    """
    Returns the diagonal of the selected two axis. 
    """

    axis = _parseAxis(A, axis)

    assert A.shape[axis[0]] == A.shape[axis[1]], "The two selected axis must have the same size"

    # Shortcut if the axis are the last two
    if axis == (A.ndim-2, A.ndim-1):
        # Create an output array
        shape = list(A.shape)
        shape[-2] = 1
        out = np.zeros(shape)

        # Get the diagonal
        for k in range(A.shape[axis[0]]):
            out[...,0,k] = A[...,k,k]

        return out

    # Find how to reorder these
    order, reorder = getOrder(A, axis)

    # Create an output array
    temp = A.transpose(order)
    shape = list(temp.shape)
    shape[-2] = 1
    out = np.zeros(shape)

    # Get the diagonal
    for k in range(A.shape[axis[0]]):
        out[...,0,k] = temp[...,k,k]

    # Reshape and return
    return out.transpose(reorder)

def MatFlip(A:ndarray, axis:Tuple[int,int]=(-2,-1)) -> ndarray:
    """
    Flips those two axis in the matrix
    """
    axis = _parseAxis(A, axis)

    order = list(range(A.ndim))
    order[axis[0]] = axis[1]
    order[axis[1]] = axis[0]
    return A.transpose(order)

def MatRemoveDim(A:ndarray, axis=int) -> ndarray:
    assert A.shape[axis] == 1, 'Can only remove a dimension of size 1'
    order = [x for x in range(A.ndim) if x != axis] + [axis]
    return A.transpose(order)[...,0]

def FFTGuess(x:ndarray, y:ndarray, axis:int=-1, warningEnabled:bool=True) -> Tuple[float, float, float, float]:
    """
    Guesses the parameters used for a CosineFit using the Fourier transform. 
    This approach can be limited if more than one frequency is prominent, 
    as it only takes the most prominent one. 

    Only the frequencies below Nyquist will be used for this, also if
    the x vector is not evenly spaced, interpolation will be used. 

    Returns the following parameters:
        amplitude (amp)
        frequency (omega)
        phase shift (phi)
        vertical offset (voff)

    """
    assert x.ndim == 1 and y.ndim == 1, "Only 1D arrays are supported for now. "

    dx = np.diff(x, axis=axis)
    if not np.allclose(dx[0],dx):
        # If the x values are not evenly spaced enough, interpolate
        dx = np.abs(np.min(dx))
        nb = int( (x.max() - x.min())//dx + 1 )
        xi = np.linspace(x.min(), x.max(), nb)

        # sort x, otherwise np.interp has unwanted behaviour
        order = np.argsort(x)
        yi = np.interp(xi, x[order], y[order])
        
        # Replace with interpolated values
        x, y = xi, yi

    # Perform the fft of the function
    nb = y.shape[axis]
    Y = np.fft.fft(y, axis=axis)[:nb//2] / nb # Normalize by number of points
    Y[1:] *= 2 # Correction when taking only positive frequencies
    A = np.abs(Y) # Amplitude

    # Obtain the frequencies as well
    F = np.fft.fftfreq(nb, (x.max() - x.min())/(nb -1))[:nb//2]

    # Find the most prominent peak after the DC offset
    amp = np.max(A[1:])

    # Find the frequency and phase of that peak
    crit = A == amp
    omega = F[crit][0] * 2*np.pi
    phi = np.angle(Y[crit])[0]

    # Grab the DC offset
    voff = Y[0].real

    # Warn if the most prominent peak is not dominant enough
    totalEnergy = np.sum(A[1:]**2) # without counting the DC offset
    peakEnergy = amp**2

    if warningEnabled and (peakEnergy/totalEnergy < 0.5):
        print("Warning: the most prominent peak does not account for more than half the energy, the FFTGuess may not be the best one. ")

    return amp, omega, phi, voff

def NumericalJacobian(f:Callable, x: ndarray, parms:Tuple[float, ...], dx:float = 1e-8) -> ndarray:
    """
    Computes a numerical jacobian on the provided function using central differences.
    Input parameters:
        f:  FitFunc(self, x:ndarray, *args:List[float]) -> ndarray
        x:  the array of independant variable
        parms:  a tuple containing the parameters
        dx:     how much to nudge the function in each direction to get a gradient

    Output parameters:
        the jacobian matrix, a numpy.ndarray of shape [x.size, len(parms)]
    """

    jac = np.zeros((x.size, len(parms)))

    for i, parm in enumerate(parms):
        parm_plus = list(parms)
        parm_plus[i] += dx
        parm_minus = list(parms)
        parm_minus[i] -= dx
        jac[:,i] = (f(x, *parm_plus) - f(x, *parm_minus))/(2*dx)

    return jac

class Scaler:
    """
    From a starting numpy.ndarray, extracts the mean and std along the specified 
    axis (assumes the last dimension if none are provided). Can then use the .Scale()
    function to obtained the scaled version of the original array, or apply it to a new one. 
    Can also use it to un-scale an array using the mean and stdev from the original array. 
    """
    _X:     ndarray
    _muX:   ndarray
    _sigX:  ndarray
    _Axis:  int
    _noSpread: ndarray

    def __init__(self, x:ndarray, axis:int = -1):

        self._X = x
        self._Axis = axis

        self._muX = np.mean(self._X, self._Axis, keepdims=True)
        self._sigX = np.std(self._X, self._Axis, keepdims=True)
        self._noSpread = self._sigX == 0

    def Scale(self, x:ndarray = None) -> ndarray:
        """
        Apply the scaling from the original array to the given array. If none are
        provided, returns the scaled version of the original array. 
        """
        
        if x is None:
            x = self._X
        else:
            assert x.ndim == self._X.ndim, "Provided data must have the same number of dimensions as the original dataset"

        return (x - self._muX)/self._sigX

    def Unscale(self, x:ndarray) -> ndarray:
        """
        Unscales the given array using the scaling parameters from the array used at inscanciation. 
        This is useful if, for example, you scaled the dependant variable before performing a fit, 
        and now want to unscale the values obtained from Eval() back to the original scale. 
        """
        return self._sigX * x + self._muX

def Eig(A:ndarray, B:ndarray, axis:Tuple[int, int]=(-2,-1)) -> ndarray:
    """Eig
    Solves the generalized eigenvalues problem. 
    This uses scipy.linalg.eig, with a small wrapper 
    to allow quick and easy choosing of the two axis of interest. 
    """
    parsedAxis = _parseAxis(A, axis)

    # Shortcut if the axis are the last two
    if parsedAxis == (A.ndim-2, A.ndim-1):
        return eig(A, B)

    # Find how to reorder these
    order, reorder = getOrder(A, parsedAxis)

    # Compute and return the result
    eigenvalues, eigenvectors = eig(A.transpose(order), B.transpose(order))

    # TODO: might be a slight difference for the eigenvalues, since they have 1 less dimension
    return eigenvalues.transpose(reorder), eigenvectors.transpose(reorder)
