'''Utilities for the Matern kernel'''

__author__ = "Vera Del Favero"

######## Module Imports ########
import numpy as np
import sys

from gp_api.gaussian_process import GaussianProcess
from gp_api.kernels import MaternKernel, WhiteNoiseKernel
from gp_api.utils.hypercube import sample_hypercube

######## Autofit ########

def fit_matern_nd(
                   x_train, y_train,
                   whitenoise=0.0,
                   nu=0.5,
                   use_cython=True,
                   xpy=None,
                   **kwargs
                  ):
    '''Fit data for an arbitrary function using the compact kernel

    Parameters
    ----------
    x_train: array like, shape = (npts, dim)
        Training data samples
    y_train: array like, shape = (npts,)
        Training data values
    whitenoise: float, optional
        White noise kernel threshold
    sparse: bool, optional
        Use sparse matrix operations from scikit-sparse?
    xpy: ModuleType, optional
        A module, either ``numpy`` or ``cupy``.  ``cupy`` is not yet
        supported.
    use_cython: bool, optional
        Whether to use Cython compiled kernel functions.
    '''
    # Extract dimensions from data
    if len(x_train.shape) == 2:
        npts, dim = x_train.shape
    elif len(x_train.shape) == 1:
        npts, dim = x_train.size, 1
    else:
        raise TypeError("Data is not of shape (npts, dim)")

    # Check for invalid options
    if use_cython and not (xpy is None):
        import numpy as np
        if not (xpy == np):
            raise RuntimeError("use_cython is incompatible with alternative numpy")

    # Create the compact kernel
    k1 = MaternKernel.fit(
                          x_train,
                          method="sample_covariance",
                          nu=nu,
                          use_cython=use_cython,
                         )

    # Use noise
    if whitenoise != 0.0:
        k2 = WhiteNoiseKernel.fit(
                                  x_train,
                                  method="simple",
                                  sparse=False,
                                  scale=whitenoise,
                                  use_cython=use_cython,
                                 )
        # Add kernels
        kernel = k1 + k2
    else:
        # No noise
        kernel = k1

    # Fit the training data
    gp_fit = GaussianProcess.fit(x_train, y_train, kernel=kernel, **kwargs)

    return gp_fit
