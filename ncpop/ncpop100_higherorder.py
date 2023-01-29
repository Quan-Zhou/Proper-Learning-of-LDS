import sys
sys.path.append("/home/zhouqua1") 
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
T=20
level=1

# Collect the nrmse value for each experiment
# The function SimCom() might fail to find any feasible solutions
pro_rang = np.arange(start,stop,step)
obs_rang = np.arange(start,stop,step)
proL=len(pro_rang)
obsL=len(obs_rang)

g = np.matrix([[0.9,0.2],[0.1,0.1]])
f1_dash = np.matrix([[1],[1]])
f2_dash = np.matrix([[0.2],[0.5]])

Z = np.zeros((proL,obsL))
N = np.zeros((proL,obsL))

for i in range(proL):
    for j in range(obsL):
        for n in range(10):
            print(n)
            Y=data_generation_higher(g,f1_dash,f2_dash,pro_rang[i],obs_rang[j],T)
            tmp=SimCom_higher(Y,T,level)
            if (tmp):
                Z[i,j] = tmp
                N[i,j] = n
                break

Zdf=pd.DataFrame(Z)
#Zdf.index=pro_rang
Zdf.columns=obs_rang
Zdf.to_csv('NCPOP/ncpop100_highersd.csv') #,index=False