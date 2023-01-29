import sys
#sys.path.append("/home/zhouqua1") 
sys.path.append("/home/zhouqua1/NCPOP") 
from inputlds import*
from functions import*
from ncpol2sdpa import*
import numpy as np
import pandas as pd
from math import sqrt

# Set parameters
start=0.1
stop=1.0
step=0.1
repeat=30
T=20
level=1

# Collect the nrmse value for each experiment
# The function SimCom() might fail to find any feasible solutions
noise_rang = np.arange(start,stop,step)
noiL=len(noise_rang)
g = np.matrix([[0.9,0.2],[0.1,0.1]])
f1_dash = np.matrix([[1],[1]])
f2_dash = np.matrix([[0.2],[0.5]])
Z = np.zeros((repeat,noiL))
N = np.zeros((repeat,noiL))
Ydf=pd.DataFrame(index=[*range(T)],columns=[(r,n) for r in range(repeat) for n in range(noiL)])

for n in range(noiL):
    for r in range(repeat):
        for i in range(10):
            print(n)
            Y=data_generation_higher(g,f1_dash,f2_dash,noise_rang[n],noise_rang[n],T)
            Ydf[(r,n)]=Y
            tmp=SimCom_higher(Y,T,level)
            if (tmp):
                Z[r,n] = tmp
                N[r,n] = n
                break
       
Zdf=pd.DataFrame(Z)
Zdf.columns=noise_rang
Zdf.to_csv('NCPOP/ncpop300_highersd.csv',index=True)
Ydf.to_csv('NCPOP/ncpop300_ydata_highersd.csv',index=True)