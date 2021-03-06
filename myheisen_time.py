
import sys
import os
sys.path.append("/Users/ivan/work/python/ttpy")
sys.path.append("/Users/iv/work/python/ttpy")
import tt
import numpy as np
from tt.ksl import ksl
import time
#This example is about the spin-system example
def gen_1d(mat,e,i,d):
    w = mat
    for j in xrange(i):
        w = tt.kron(e,w)
    for j in xrange(d-i-1):
        w = tt.kron(w,e)
    return w

def gen_heisen(d):
    sx = [[0,1],[1,0]]
    sx = np.array(sx,dtype=np.float)
    sz = [[1,0],[0,-1]]
    sz = np.array(sz,dtype=np.float)
    sz = 0.5 * sz
    sp = [[0,1],[0,0]]; sp =  np.array(sp,dtype=np.float)
    sm = sp.T
    e = np.eye(2)
    sx = tt.matrix(sx,1e-12)
    sz = tt.matrix(sz,1e-12)
    sp = tt.matrix(sp,1e-12)
    sm = tt.matrix(sm,1e-12)
    e = tt.matrix(e,1e-12)
    #Generate ssx, ssz
    ssp = [gen_1d(sp,e,i,d) for i in xrange(d)]
    ssz = [gen_1d(sz,e,i,d) for i in xrange(d)]
    ssm = [gen_1d(sm,e,i,d) for i in xrange(d)]
    A = None
    for i in xrange(d-1):
        A = A + 0.5 * (ssp[i] * ssm[i+1] + ssm[i] * ssp[i+1]) +  (ssz[i] * ssz[i+1])
        A = A.round(1e-8)
    return A

if __name__ == '__main__':
    d =  5
    A = gen_heisen(d)
    n = A.n
    d = A.tt.d
#In this case we will start from the rank-1 tensor "all spins up"
#It is not good, since it leads to an eigenvector
#Random start also seems to be quite useless
#Maybe first d/2 is up other d/2 are down?
    v0 = np.array([1,0],dtype=np.float); v0 = tt.tensor(v0,1e-12)
    v1 = np.array([0,1],dtype=np.float); v1 = tt.tensor(v1,1e-12)
    e1 = None
    for j in xrange(d):
        if j % 2:
            e0 = v0#np.random.rand(2)
        else:
            e0 = v1#e0 = tt.tensor(e0,1e-12)
        e1 = tt.kron(e1,e0)
    r = [1]*(d+1)
    r[0] = 1
    r[d] = 1
    x0 = tt.rand(n,d,r)
    tau = 1e-2
    tf = 100
    t = 0
    start = e1 
    psi = start + 0 * x0
    psi1 = start + 0 * x0
    cf = []
    while t <= tf: 
        print '%f/%f' % (t,tf)
        psi = ksl(-1.0j*A,psi,tau)
        #psi1 = kls(-1.0j*A,psi1,tau)
        cf.append(tt.dot(psi,start))
        #import ipdb; ipdb.set_trace()
        t += tau
    #x0 = tt.rand(n,d,r)
    #t1 = time.time()
    #print 'Matrices are done'
    #y, lam = eigb(A,x0,1e-3)
    #lm.append(d)
    #t2 = time.time()
