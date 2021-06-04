from ncpol2sdpa import*
import scipy.io as sio
import numpy as np
import pandas as pd
from math import sqrt
import matplotlib.pyplot as plt 

# Load stock-market data
load_path = 'setting6.mat'
load_data = sio.loadmat(load_path)
seq=flatten(load_data['seq_d0'].tolist())

# Extract estimation data
start=0
stop=200
step=4
Y=seq[start:stop:step]
T=len(Y)

level = 1

# Decision Variables
G = generate_operators("G", n_vars=1, hermitian=True, commutative=False)[0]
Fdash = generate_operators("Fdash", n_vars=1, hermitian=True, commutative=False)[0]
m = generate_operators("m", n_vars=T+1, hermitian=True, commutative=False)
q = generate_operators("q", n_vars=T, hermitian=True, commutative=False)
p = generate_operators("p", n_vars=T, hermitian=True, commutative=True)
f = generate_operators("f", n_vars=T, hermitian=True, commutative=True)

# Objective
obj = sum((Y[i]-f[i])**2 for i in range(T)) + 0.1*sum(p[i]**2 for i in range(T))
# Constraints
ine1 = [f[i] - Fdash*m[i+1] - p[i] for i in range(T)]
ine2 = [-f[i] + Fdash*m[i+1] + p[i] for i in range(T)]
ine4 = [m[i+1] - G*m[i] - q[i] for i in range(T)]
ine5 = [-m[i+1] + G*m[i] + q[i] for i in range(T)]
ine3 = [sum((Y[i]-f[i])**2 for i in range(T))]
ines = ine1+ine2+ine4+ine5+ine3

 # Solve the NCPOP
sdp = SdpRelaxation(variables = flatten([G,Fdash,f,p,m,q]), verbose = 2)
sdp.get_relaxation(level, objective=obj, inequalities=ines)
sdp.solve(solver='sdpa', solverparameters={"executable":"sdpa_gmp","executable": "C:\\Users\\...\\Documents\\sdpa7-windows\\sdpa.exe"})
         
if (sdp[sum((Y[i]-f[i])**2 for i in range(T))]>0):
    nrmse_sim = 1-sqrt(sdp[sum((Y[i]-f[i])**2 for i in range(T))])/sqrt(sum((Y[i]-np.mean(Y))**2 for i in range(T)))
    print(sdp.status,nrmse_sim)
    
# Write experiment results of our method to 'stock_NCPO.csv'
stock_NCPO=open('stock_NCPO_try.csv','w')
for i in range(T):
    print(sdp[f[i]],file=stock_NCPO)
stock_NCPO.close()
