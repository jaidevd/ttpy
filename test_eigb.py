import numpy as np
import tt
from tt.eigb import *
#from tt_tensor2 import *
import time
d = 8
f = 20
A = tt.qlaplace_dd([d]*f)
#A = (-1)*A
#A = tt.eye(2,d)
n = [2]*(d*f)
r = [5]*(d*f+1)
r[0] = 1
r[d*f] = 2 #Number of eigenvalues sought
x = tt.rand(n,d*f,r)
#x = tt_ones(2,d)
t = time.time()
y,lam=eigb(A,x,1e-6)

t1 = time.time()
print 'Eigenvalues:', lam
print 'Time is:', t1-t
