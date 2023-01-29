import sys
#sys.path.append("/home/zhouqua1") 
sys.path.append("/home/zhouqua1/NCPOP") 
from inputlds import*
from functions import*
from ncpol2sdpa import*
import numpy as np
import pandas as pd
from math import sqrt
from scipy.stats import unitary_group

# Set parameters
repeat=30
T=30
level=1
proc_noise_std=0.5
obs_noise_std=0.5
nx_range=[*range(2,5)]
Z = np.zeros((repeat,3))
N = np.zeros((repeat,3))
Ydf=pd.DataFrame(index=[*range(T)],columns=[(r,ig) for r in range(repeat) for ig in range(3)])

for nx in nx_range:
    for r in range(repeat):
        for i in range(10):
            # Collect the nrmse value for each experiment
            # The function SimCom() might fail to find any feasible solutions
            x = unitary_group.rvs(nx)
            g=np.matrix(np.dot(x, x.conj().T))
            f_dash = np.matrix([[1.0]*nx])
            Y_complex=data_generation(g,f_dash,proc_noise_std,obs_noise_std,T)
            Y=np.real(Y_complex)
            #Y=data_generation(g,f_dash,proc_noise_std,obs_noise_std,T)
            tmp=SimCom(Y,T,level)
            if (tmp):
                Z[r,nx-2] = tmp
                N[r,nx-2] = i
                Ydf[(r,nx-2)]=Y
                break

Zdf=pd.DataFrame(Z)
Zdf.columns=nx_range
Zdf.to_csv('NCPOP/ncpop300_higherdim.csv',index=True)
Ydf.to_csv('NCPOP/ncpop300_ydata_higherdim.csv',index=True)