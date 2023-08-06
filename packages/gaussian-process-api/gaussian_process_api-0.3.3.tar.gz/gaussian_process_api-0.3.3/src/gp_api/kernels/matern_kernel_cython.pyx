'''
matern_kernel_evaluate.py
Authors: Vera Delfavero, Daniel Wysocki

This script provides functions for the matern kernel 

Code adapted from sklearn.gaussian_process.kernels.Matern
<https://scikit-learn.org/stable/modules/generated/sklearn.gaussian_process.kernels.Matern.html>
'''

import cython
cimport cython
from cython.parallel import prange
from cython.cimports.libc.math import sqrt, pow as cpow
from cython.cimports.libc.math import exp
#from cython.cimports.libc.tgmath import tgamma
import numpy as np


cdef extern from "math.h":
    double exp(double x) nogil
    double sqrt(double x) nogil
    #double cpow(double x) nogil


cdef double norm(
                 double[::1] x_vi,
                 double[::1] x_pvj,
                 Py_ssize_t dim,
                ) nogil:
    cdef int k
    cdef double ksum = 0.
    cdef double r
    for k in range(dim):
        ksum += (x_vi[k] - x_pvj[k])**2
    r = sqrt(ksum)
    return r

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
def matern_kernel_evaluate(
                           x,
                           x_prime,
                           double nu,
                           train_err=None,
                          ):
    '''
    Evaluates the Matern kernel K(x, x').

    '''
    #import math
    #from scipy.spatial.distance import cdist
    from scipy.special import kv, gamma

    # Check number of points in x
    cdef Py_ssize_t npts = x.shape[0]
    # Check number of points in x_prime
    cdef Py_ssize_t npts_prime = x_prime.shape[0]
    # Check number of dimensions
    cdef Py_ssize_t ndim = x.shape[1]

    # Contain scope and c order coordinates
    x = x.copy(order='C')
    x_prime = x_prime.copy(order='C')

    # Declare viewing
    cdef double[:,::1] x_v = x
    cdef double[:,::1] x_vp = x_prime

    # Fix training error
    if train_err is None:
        train_err = np.asarray([0.])
    else:
        train_err = train_err.copy(order='C')
    cdef double[::1] train_err_view = train_err

    # Initialize K
    K = np.zeros((npts, npts_prime),dtype=np.double)
    cdef double[:,::1] K_view = K
    tmp = np.empty((npts, npts_prime),dtype=np.double)
    cdef double[:,::1] tmp_view = tmp
    
    # Initialize distance
    cdef double r
    # Initialize loop variables
    cdef int i, j
    # Define useful constants
    cdef double sqrt3 = sqrt(3.)
    cdef double sqrt5 = sqrt(5.)
    cdef double sqrt2nu = sqrt(2.*nu)
    cdef double eps = np.finfo(float).eps # strict zeros result in nan
    #K.fill((2 ** (1. - nu)) / gamma(nu))
    cdef double Kfill = (2**(1. - nu)) / gamma(nu)

    # Loop and calculate distances
    #for i in prange(npts, nogil=True):
    #    for j in range(npts_prime):
    #        r = norm(x_v[i], x_vp[j], ndim)

    # Handle nu cases
    # Note, once we find a kv function with a nogil c implementation
    # We can combine these loops

    if nu == 0.5:
        #K = xpy.exp(-dists)
        for i in prange(npts, nogil=True):
            for j in range(npts_prime):
                r = norm(x_v[i], x_vp[j], ndim)
                K_view[i,j] = exp(-r)
    elif nu == 1.5:
        #K = dists * math.sqrt(3)
        #K = (1.0 + K) * xpy.exp(-K)
        for i in prange(npts, nogil=True):
            for j in range(npts_prime):
                r = sqrt3*norm(x_v[i], x_vp[j], ndim)
                K_view[i,j] = (1.0 + r) * exp(-r)

    elif nu == 2.5:
        #K = dists * math.sqrt(5)
        #K = (1.0 + K + xpy.square(K) / 3.0) * xpy.exp(-K)
        for i in prange(npts, nogil=True):
            for j in range(npts_prime):
                r = norm(x_v[i], x_vp[j], ndim) *sqrt5
                K_view[i,j] = (1.0 + r + cpow(r,2)/3) * exp(-r)
    else:  # general case; expensive to evaluate
        #K = dists
        #K[K == 0.0] += numpy.finfo(float).eps  # strict zeros result in nan
        #tmp = (math.sqrt(2 * nu) * K)
        #K.fill((2 ** (1. - nu)) / gamma(nu))
        #K *= tmp ** nu
        for i in prange(npts, nogil=True):
            for j in range(npts_prime):
                # Estimate distances
                r = norm(x_v[i], x_vp[j], ndim)
                if r == 0.0:
                    r = eps # strict zeros result in nan
                # Estimate temp
                tmp_view[i,j] = (sqrt2nu*r)
                #cdef double Kfill = (2**(1. - nu)) / tgamma(nu)
                K_view[i,j] = Kfill*cpow(tmp_view[i,j], nu)

        K *= kv(nu, tmp)

    return K

