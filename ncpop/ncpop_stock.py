import sys
#sys.path.append("/home/zhouqua1") 
sys.path.append("/home/zhouqua1/NCPOP") 
from functions import*
from ncpol2sdpa import*
import numpy as np
import pandas as pd

"""
# Load stock-market data
load_path = 'setting6.mat'
load_data = sio.loadmat(load_path)
seq=flatten(load_data['seq_d0'].tolist())
"""

ts=pd.read_csv("/home/zhouqua1/NCPOP/stock-market.txt",header=None)[0].tolist()
level=1
T=20
pred=pd.DataFrame(columns=['prediction','rmse'],index=[*range(20,120)])
for start in range(100):
    Y=ts[start:start+T+1]
    pred_tem=PredCom(Y[0:T],level) # the prediction of Y[T]
    pred.loc[start+T]=[pred_tem,abs(Y[T]-pred_tem)]

pred.to_csv('NCPOP/stock_NPA_k'+str(level)+'.csv',index=True)