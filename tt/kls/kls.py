""" Dynamical TT-approximation """
import numpy as np
import dyn_tt
from tt import tensor
def kls(A,y0,tau,rmax=150,kickrank=5,verb=1,nswp=10):
    """ Dynamical TT-approximation """
    ry = y0.r.copy()
    #lam = np.zeros(ry[y0.d])
    #for i in xrange(10):
    #Check for dtype
    y = tensor()
    if np.iscomplex(A.tt.core).any() or np.iscomplex(y0.core).any():
        dyn_tt.dyn_tt.ztt_kls(y0.d,A.n,A.m,A.tt.r,A.tt.core +0j, y0.core+0j, ry, tau, rmax, kickrank, nswp, verb)
        y.core = dyn_tt.dyn_tt.zresult_core.copy()    
    else:
        A.tt.core = np.real(A.tt.core)
        y0.core = np.real(y0.core) 
        dyn_tt.dyn_tt.tt_kls(y0.d,A.n,A.m,A.tt.r,A.tt.core, y0.core, ry, tau, rmax, kickrank, nswp, verb)
        y.core = dyn_tt.dyn_tt.result_core.copy()
    dyn_tt.dyn_tt.deallocate_result()
    y.d = y0.d
    y.n = A.n.copy()
    y.r = ry 
    y.get_ps()
    return y
"""
def ksl(A,y0,tau,rmax=150,kickrank=5,verb=1,nswp=10):
    ry = y0.r.copy()
    #lam = np.zeros(ry[y0.d])
    #for i in xrange(10):
    #Check for dtype
    y = tensor()
    if np.iscomplex(A.tt.core).any() or np.iscomplex(y0.core).any():
        dyn_tt.dyn_tt.ztt_ksl(y0.d,A.n,A.m,A.tt.r,A.tt.core +0j, y0.core+0j, ry, tau, rmax, kickrank, nswp, verb)
        y.core = dyn_tt.dyn_tt.zresult_core.copy()    
    else:
        A.tt.core = np.real(A.tt.core)
        y0.core = np.real(y0.core) 
        dyn_tt.dyn_tt.tt_ksl(y0.d,A.n,A.m,A.tt.r,A.tt.core, y0.core, ry, tau, rmax, kickrank, nswp, verb)
        y.core = dyn_tt.dyn_tt.result_core.copy()
    dyn_tt.dyn_tt.deallocate_result()
    y.d = y0.d
    y.n = A.n.copy()
    y.r = ry 
    y.get_ps()
    return y
 """
