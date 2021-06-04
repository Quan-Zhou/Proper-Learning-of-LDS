
from ncpol2sdpa import*
import scipy.io as sio
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt 
import pandas as pd
import time

experiment=open('stock_experiment_time.csv','a')

# Load stock-market data
load_path = 'setting6.mat'
load_data = sio.loadmat(load_path)
seq=flatten(load_data['seq_d0'].tolist())

level = 1

# Experiments
for T in range(5,51):
         start = time.time()
         Y=seq[0:T]

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

         # Solve the NCPO
         sdp = SdpRelaxation(variables = flatten([G,Fdash,f,p,m,q]), verbose = 2)
         sdp.get_relaxation(level, objective=obj, inequalities=ines)
         sdp.solve(solver='sdpa', solverparameters={"executable":"sdpa_gmp","executable": "C:\\Users\\zhouq\\Documents\\sdpa7-windows\\sdpa.exe"})
         
         end = time.time()
         
         print(T,',',end-start,file=experiment)
    
experiment.close()

runtimeSec=pd.read_csv('stock_experiment_time.csv',header=None,index_col=0)
runtime=runtimeSec/60
ax=runtime.plot()
ax.set_ylabel('runtime of our method (minutes)')
ax.set_xlabel('length T of time windows')
ax.legend_.remove()
plt.show()




