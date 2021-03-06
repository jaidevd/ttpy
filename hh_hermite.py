#This is a clone of the MATLAB spectral discretization for the Henon-Heiles potential
#Using the Hermite-DVR representation
#The goal is to compute many eigenfunctions of this operator
import numpy as np
from scipy.linalg import toeplitz
from tt.eigb import *
import tt
import time
from math import pi,sqrt
import quadgauss
import os
import sys



f = 20 #The number of degrees of freedom
L = 7 #The domain is [-L, L], periodic
lm = 0.111803 #The magic constant
#lm = 0 #The magic constant
#lm = 1e-2
#lm = 
N = 15 # The size of the spectral discretization

x, ws = quadgauss.cdgqf(N,6,0,0.5) #Generation of hermite quadrature
#Generate Laplacian
lp = np.zeros((N,N))
for i in xrange(N):
    for j in xrange(N):
        if i is not j:
            lp[i,j] = (-1)**(i - j)*(2*(x[i] - x[j])**(-2) - 0.5)
        else:
            lp[i,j] = 1.0/6*(4*N - 1 - 2 * x[i]**2)
lp = tt.matrix(lp)
e = tt.eye([N])

lp2 = None
eps = 1e-8
for i in xrange(f):
    w = lp
    for j in xrange(i):
        w = tt.kron(e,w)
    for j in xrange(i+1,f):
        w = tt.kron(w,e)
    lp2 = lp2 + w
    lp2 = lp2.round(eps)


#Now we will compute Henon-Heiles stuff
xx = []
t = tt.tensor(x)
ee = tt.ones([N])
for  i in xrange(f):
    t0 = t
    for j in xrange(i):
        t0 = tt.kron(ee,t0)
    for j in xrange(i+1,f):
        t0 = tt.kron(t0,ee)
    xx.append(t0)

#Harmonic potential
harm = None
for i in xrange(f):
    harm = harm + (xx[i]*xx[i])
    harm = harm.round(eps)

#Henon-Heiles correction
V = None
for s in xrange(f-1):
    V = V + (xx[s]*xx[s]*xx[s+1] - (1.0/3)*xx[s+1]*xx[s+1]*xx[s+1])
    V = V.round(eps)
B = 4


A = 0.5*lp2 + tt.diag(0.5*harm + lm*V)
A0 = 0.5*lp2 + tt.diag(0.5*harm)
A = A.round(eps) 

n = A.n
d = A.tt.d
r = [2]*(d+1)
r[0] = 1
r[d] = B
x0 = tt.rand(n,d,r)

t1 = time.time()
print 'Matrices are done'
y,lam = eigb(A,x0,1e-6)
#y,lam = eigb(A0,y,1e-6)
#y,lam = eigb(A,y,1e-6,nswp=1)
#y,lam = eigb(A,y,1e-5)
#y,lam = eigb(A,y,1e-6)
t2 = time.time()
print 'Eigenvalues:',lam    
print 'Elapsed time:', t2-t1

