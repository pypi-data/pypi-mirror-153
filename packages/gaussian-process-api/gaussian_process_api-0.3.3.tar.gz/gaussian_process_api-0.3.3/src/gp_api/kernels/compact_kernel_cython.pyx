# cython: infer_types=True
'''
compact_kernel_cython.py
Authors: Vera Delfavero, Daniel Wysocki

Compact kernel evaluation function using cython
'''
import cython
cimport cython
from cython.parallel import prange
from cython.cimports.libc.math import sqrt
import numpy as np

## Load square root
#cdef extern from "math.h":
#    double sqrt(double)

# Initialize an evaluation
cdef double norm(
                 double[::1] x_svi,
                 double[::1] x_psvj,
                 Py_ssize_t ndim,
                ) nogil:
    cdef int k
    cdef double ksum = 0.
    cdef double r
    for k in range(ndim):
        ksum += (x_svi[k] - x_psvj[k])**2
    r = sqrt(ksum)
    return r

cdef double K_q_0(
                  double r,
                  int j_Dq,
                 ) nogil:
    cdef float K_value
    K_value = ((1. - r)**j_Dq)
    return K_value

cdef double K_q_1(
                  double r,
                  int j_Dq_p1,
                 ) nogil:
    cdef float K_value
    K_value = ((1. - r)**j_Dq_p1) * (j_Dq_p1*r + 1.0)
    return K_value

cdef double K_q_2(
                  double r,
                  int j_Dq_p2,
                  int j_poly_r,
                  int j_poly_r2,
                 ) nogil:
    cdef float r2
    cdef float K_value
    r2 = r**2
    K_value = (1. - r)**(j_Dq_p2) * (
        j_poly_r2*r2 + j_poly_r*r + 3.) / 3.
    return K_value


cdef double K_q_3(
                  double r,
                  int j_Dq_p3,
                  int j_poly_r,
                  int j_poly_r2,
                  int j_poly_r3,
                 ) nogil:
    cdef float r2
    cdef float r3
    cdef float K_value
    r2 = r**2
    r3 = r2 * r
    K_value = (1. - r)**(j_Dq_p3) * (
        j_poly_r3*r3 + j_poly_r2*r2 + j_poly_r*r + 15.) / 15.
    return K_value




@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
def compact_kernel_evaluate(
                            x,
                            x_prime,
                            double[::1] scale,
                            train_err,
                            int q = 1,
                           ):
        '''
        Evaluates the compact kernel K(x, x').
        '''
        # Check number of points in x
        cdef Py_ssize_t npts = x.shape[0]
        # Check number of points in x_prime
        cdef Py_ssize_t npts_prime = x_prime.shape[0]
        # Check number of dimensions
        cdef Py_ssize_t ndim = x.shape[1]
                        
        if not q in [0,1,2,3]:
            raise ValueError("Invalid q. Should be in [0,1,2,3]")

        # Declare scaled coordinates and contain scope
        x_scaled = x.copy(order='C')/scale
        x_prime_scaled = x_prime.copy(order='C')/scale
        if train_err is None:
            train_err = np.asarray([0.])
        else:
            train_err = train_err.copy(order='C')
        cdef double[::1] train_err_view = train_err

        #x_scaled = np.asarray(x) / scale
        #x_prime_scaled = np.asarray(x_prime) / scale
        # Declare cython viewing
        cdef double[:,::1] x_sv = x_scaled
        cdef double[:,::1] x_psv = x_prime_scaled
        
        # Constant required for basis functions (see R&W)
        #j_plus_1 = ndim // 2 + 3
        #cdef Py_ssize_t j_plus_1 = ndim//2 + 3
        cdef Py_ssize_t j_Dq = ndim//2 + q + 1
        cdef Py_ssize_t j_exp
        cdef Py_ssize_t j_poly_r1
        cdef Py_ssize_t j_poly_r2
        cdef Py_ssize_t j_poly_r3

        # Update coefficients
        if q == 0:
            pass
        elif q == 1:
            j_exp = j_Dq + 1
        elif q == 2:
            j_exp = j_Dq + 2
            j_poly_r1 = 3*j_Dq + 6
            j_poly_r2 = j_Dq**2 + 4*j_Dq + 3
        elif q == 3:
            j_exp = j_Dq + 3
            j_poly_r1 = 15*j_Dq + 45
            j_poly_r2 = 6*j_Dq**2 + 36*j_Dq + 45
            j_poly_r3 = j_Dq**3 + 9*j_Dq**2 + 23*j_Dq + 15

        # Initialize Kernel 
        K = np.zeros((npts, npts_prime),dtype=np.double)
        cdef double[:,::1] K_view = K
        cdef double r
        #cdef double ksum
        cdef int i, j#, k

        for i in prange(npts, nogil=True):
            for j in range(npts_prime):
                #ksum = 0
                #for k in range(ndim):
                #    ksum += (x_sv[i,k] - x_psv[j,k])**2
                #r = sqrt(ksum)
                r = norm(x_sv[i], x_psv[j], ndim)

                if r < 1.:
                    #K_view[i,j] = ((1. - r)**j_plus_1) * (j_plus_1*r + 1.0)
                    if q == 0:
                        K_view[i,j] = K_q_0(r, j_Dq)
                    elif q == 1:
                        K_view[i,j] = K_q_1(r, j_exp)
                    elif q == 2:
                        K_view[i,j] = K_q_2(r, j_exp, j_poly_r1, j_poly_r2)
                    elif q == 3:
                        K_view[i,j] = K_q_3(r, j_exp, j_poly_r1, j_poly_r2, j_poly_r3)

        if (npts == npts_prime) and (not (train_err[0] == 0.)):
            for i in range(npts):
                for j in range(npts_prime):
                    if i == j:
                        if train_err.size == 1:
                            K_view[i,j] += train_err_view[0]
                        elif train_err.size == npts:
                            K_view[i,j] += train_err_view[i]
                        else:
                            raise TypeError("Training error is not the right size")
                                

        return K
