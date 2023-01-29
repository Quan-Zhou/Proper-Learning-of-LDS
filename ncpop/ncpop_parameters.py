import sys
sys.path.append("/home/zhouqua1/NCPOP") 
from inputlds import*
from functions import*
from ncpol2sdpa import*
import numpy as np
import pandas as pd
from math import sqrt

# set std of noises to be 0.5
# tune c1 and c2
level=1
pro_std=0.5
obs_std=0.5
T=20
g = np.matrix([[0.9,0.2],[0.1,0.1]])
f_dash = np.matrix([[1.0,1.0]])

cstart=0.0001
crange=[cstart*(sqrt(sqrt(10)))**ig for ig in range(9)]
Z = np.zeros((9,9))
N = np.zeros((9,9))
i=-1
for c1 in crange:
    i+=1
    j=-1
    for c2 in crange:
        j+=1
        for n in range(20):
            print(n)
            Y=data_generation(g,f_dash,pro_std,obs_std,T)
            tmp=SimCom_para(Y,T,level,c1,c2)
            if (tmp):
                Z[i,j] = tmp
                N[i,j] = n
                break

Zdf=pd.DataFrame(Z)
#Zdf.index=pro_rang
Zdf.columns=crange
Zdf.to_csv('NCPOP/ncpop100_c.csv')

