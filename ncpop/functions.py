import sys
sys.path.append("/home/zhouqua1/NCPOP") 
from inputlds import*
from ncpol2sdpa import*
import numpy as np
import pandas as pd
from math import sqrt

def SimCom(Y,T,level):
# Define a function for solving the NCPO problems with 
# given standard deviations of process noise and observtion noise,
# length of  estimation data and required relaxation level. 

    # Decision Variables
    G = generate_operators("G", n_vars=1, hermitian=True, commutative=False)[0]
    Fdash = generate_operators("Fdash", n_vars=1, hermitian=True, commutative=False)[0]
    m = generate_operators("m", n_vars=T+1, hermitian=True, commutative=False)
    q = generate_operators("q", n_vars=T, hermitian=True, commutative=False)
    p = generate_operators("p", n_vars=T, hermitian=True, commutative=False)
    f = generate_operators("f", n_vars=T, hermitian=True, commutative=False)

    # Objective
    obj = sum((Y[i]-f[i])**2 for i in range(T)) + 0.0005*sum(p[i]**2 for i in range(T)) + 0.0001*sum(q[i]**2 for i in range(T))
    # Constraints
    ine1 = [f[i] - Fdash*m[i+1] - p[i] for i in range(T)]
    ine2 = [-f[i] + Fdash*m[i+1] + p[i] for i in range(T)]
    ine3 = [m[i+1] - G*m[i] - q[i] for i in range(T)]
    ine4 = [-m[i+1] + G*m[i] + q[i] for i in range(T)]
    #ine5 = [(Y[i]-f[i])**2 for i in range(T)]
    ines = ine1+ine2+ine3+ine4 #+ine5

    # Solve the NCPO
    sdp = SdpRelaxation(variables = flatten([G,Fdash,f,p,m,q]),verbose = 1)
    sdp.get_relaxation(level, objective=obj, inequalities=ines)
    sdp.solve(solver='mosek')
    #sdp.solve(solver='sdpa', solverparameters={"executable":"sdpa_gmp","executable": "C:/Users/zhouq/Documents/sdpa7-windows/sdpa.exe"})
    #print(sdp.primal, sdp.dual, sdp.status)
    if (sdp[sum((Y[i]-f[i])**2 for i in range(T))] < 0):
        print("sum((Y[i]-f[i])**2 for i in range(T)) < 0")
        return 

    nrmse_sim = 1-sqrt(sdp[sum((Y[i]-f[i]+q[i])**2 for i in range(T))])/sqrt(sum((Y[i]-np.mean(Y))**2 for i in range(T)))
    #nrmse_sim = 1-sqrt(sdp[sum((Y[i]-f[i])**2 for i in range(T))])/sqrt(sum((Y[i]-np.mean(Y))**2 for i in range(T)))

    if(sdp.status != 'infeasible'):
        print(nrmse_sim)
        return nrmse_sim
    else:
        print('Cannot find feasible solution.')
        return

def SimCom_higher(Y,T,level):
# learning a higher order dynamic system
# Define a function for solving the NCPO problems with 
# given standard deviations of process noise and observtion noise,
# length of estimation data and required relaxation level. 

    # Decision Variables
    G = generate_operators("G", n_vars=1, hermitian=True, commutative=False)[0]
    Fdash = generate_operators("Fdash", n_vars=2, hermitian=True, commutative=False)
    m = generate_operators("m", n_vars=T+1, hermitian=True, commutative=False)
    q = generate_operators("q", n_vars=T, hermitian=True, commutative=False)
    p = generate_operators("p", n_vars=T, hermitian=True, commutative=True)
    f = generate_operators("f", n_vars=T, hermitian=True, commutative=True)

    # Objective
    obj = sum((Y[i]-f[i])**2 for i in range(T)) + 0.0005*sum(p[i]**2 for i in range(T)) + 0.001*sum(q[i]**2 for i in range(T))

    # Constraints
    ine1 = [ f[i] - Fdash[0]*m[i+1] -Fdash[1]*(m[i]-m[i-1]) - p[i] for i in range(1,T)]
    ine2 = [-f[i] + Fdash[0]*m[i+1] +Fdash[1]*(m[i]-m[i-1]) + p[i] for i in range(1,T)]
    ine3 = [ m[i+1] - G*m[i] - q[i] for i in range(T)]
    ine4 = [-m[i+1] + G*m[i] + q[i] for i in range(T)]
    ines = ine1+ine2+ine3+ine4

    # Solve the NCPO
    sdp = SdpRelaxation(variables = flatten([G,Fdash,f,p,m,q]),verbose = 1)
    sdp.get_relaxation(level, objective=obj, inequalities=ines)
    sdp.solve(solver='mosek')
    #sdp.solve(solver='sdpa', solverparameters={"executable":"sdpa_gmp","executable": "C:/Users/zhouq/Documents/sdpa7-windows/sdpa.exe"})
    #print(sdp.primal, sdp.dual, sdp.status)
    if (sdp[sum((Y[i]-f[i])**2 for i in range(T))] < 0):
        print("sum((Y[i]-f[i])**2 for i in range(T)) < 0")
        return 

    nrmse_sim = 1-sqrt(sdp[sum((Y[i]-f[i]+q[i])**2 for i in range(T))])/sqrt(sum((Y[i]-np.mean(Y))**2 for i in range(T)))
    #nrmse_sim = 1-sqrt(sdp[sum((Y[i]-f[i])**2 for i in range(T))])/sqrt(sum((Y[i]-np.mean(Y))**2 for i in range(T)))

    if(sdp.status != 'infeasible'):
        print(nrmse_sim)
        return nrmse_sim
    else:
        print('Cannot find feasible solution.')
        return

def data_generation(g,f_dash,proc_noise_std,obs_noise_std,T):
# Generate Dynamic System ds1
    dim=len(g)
    ds1 = dynamical_system(g,np.zeros((dim,1)),f_dash,np.zeros((1,1)),
          process_noise='gaussian',
          observation_noise='gaussian', 
          process_noise_std=proc_noise_std, 
          observation_noise_std=obs_noise_std)
    h0= np.ones(ds1.d)
    inputs = np.zeros(T)
    ds1.solve(h0=h0, inputs=inputs, T=T)    
    return np.asarray(ds1.outputs).reshape(-1).tolist()

def data_generation_higher(g,f1_dash,f2_dash,proc_noise_std,obs_noise_std,T):
# Generate higher order Dynamic System
    dim=len(g)
    ds1 = dynamical_system(g,np.zeros((dim,1)),np.matrix([[1,0],[0,1]]),np.zeros((2,1)),
          process_noise='gaussian',
          observation_noise='gaussian', 
          process_noise_std=proc_noise_std, 
          observation_noise_std=0)
    h0= np.ones(ds1.d)
    inputs = np.zeros(T)
    ds1.solve(h0=h0, inputs=inputs, T=T) # output m 
    m=[np.matrix([[1],[1]])]+ds1.outputs#m0 to m20
    difference=[m[i+1]-m[i] for i in range(T)]
    observation_noise=np.matrix(np.random.normal(loc=0, scale=obs_noise_std, size=(1,T)))
    M=[np.dot(f1_dash.T,m[i])+np.dot(f2_dash.T,difference[i]) for i in range(T)]
    Y=np.matrix(np.asarray(M).reshape(-1))+observation_noise
    return np.asarray(Y).reshape(-1).tolist()

def SimCom_para(Y,T,level,c1,c2):
# Define a function for solving the NCPO problems with 
# given standard deviations of process noise and observtion noise,
# length of  estimation data and required relaxation level. 

    # Decision Variables
    G = generate_operators("G", n_vars=1, hermitian=True, commutative=False)[0]
    Fdash = generate_operators("Fdash", n_vars=1, hermitian=True, commutative=False)[0]
    m = generate_operators("m", n_vars=T+1, hermitian=True, commutative=False)
    q = generate_operators("q", n_vars=T, hermitian=True, commutative=False)
    p = generate_operators("p", n_vars=T, hermitian=True, commutative=False)
    f = generate_operators("f", n_vars=T, hermitian=True, commutative=False)

    # Objective
    obj = sum((Y[i]-f[i])**2 for i in range(T)) + c1*sum(p[i]**2 for i in range(T)) + c2*sum(q[i]**2 for i in range(T))
# change c_1 c_2
    # Constraints
    ine1 = [f[i] - Fdash*m[i+1] - p[i] for i in range(T)]
    ine2 = [-f[i] + Fdash*m[i+1] + p[i] for i in range(T)]
    ine3 = [m[i+1] - G*m[i] - q[i] for i in range(T)]
    ine4 = [-m[i+1] + G*m[i] + q[i] for i in range(T)]
    #ine5 = [(Y[i]-f[i])**2 for i in range(T)]
    ines = ine1+ine2+ine3+ine4 #+ine5

    # Solve the NCPO
    sdp = SdpRelaxation(variables = flatten([G,Fdash,f,p,m,q]),verbose = 2)
    sdp.get_relaxation(level, objective=obj, inequalities=ines)
    sdp.solve(solver='mosek')
    #sdp.solve(solver='sdpa', solverparameters={"executable":"sdpa_gmp","executable": "C:/Users/zhouq/Documents/sdpa7-windows/sdpa.exe"})
    #print(sdp.primal, sdp.dual, sdp.status)
    if (sdp[sum((Y[i]-f[i])**2 for i in range(T))] < 0):
        print("sum((Y[i]-f[i])**2 for i in range(T)) < 0")
        return 

    nrmse_sim = 1-sqrt(sdp[sum((Y[i]-f[i]+q[i])**2 for i in range(T))])/sqrt(sum((Y[i]-np.mean(Y))**2 for i in range(T)))
    #nrmse_sim = 1-sqrt(sdp[sum((Y[i]-f[i])**2 for i in range(T))])/sqrt(sum((Y[i]-np.mean(Y))**2 for i in range(T)))

    if(sdp.status != 'infeasible'):
        print(nrmse_sim)
        return nrmse_sim
    else:
        print('Cannot find feasible solution.')
        return

def PredCom(Y,level):
    T=len(Y)
    # Decision Variables
    G = generate_operators("G", n_vars=1, hermitian=True, commutative=False)[0]
    m = generate_operators("m", n_vars=T+1, hermitian=True, commutative=False)
    q = generate_operators("q", n_vars=T-1, hermitian=True, commutative=False)
    p = generate_operators("p", n_vars=T, hermitian=True, commutative=True)
    f = generate_operators("f", n_vars=T+1, hermitian=True, commutative=True)

    # Objective
    obj = sum((Y[i]-f[i])**2 for i in range(T)) + 0.01*sum(p[i]**2 for i in range(T)) + 0.01*sum(q[i]**2 for i in range(T-1))

    #ine5 = [m[T+1] - G*m[T],-m[T+1] + G*m[T]]
    # Constraints
    ine1 = [ f[i] - m[i+1] - p[i] for i in range(T)]
    ine2 = [-f[i] + m[i+1] + p[i] for i in range(T)]
    ine3 = [ m[i+1] - G*m[i] - q[i] for i in range(T-1)]
    ine4 = [-m[i+1] + G*m[i] + q[i] for i in range(T-1)]
    ine5 = [m[T] - G*m[T-1],-m[T] + G*m[T-1]]
    ines = ine1+ine2+ine3+ine4+ine5

    # Solve the NCPO
    sdp = SdpRelaxation(variables = flatten([G,f,p,m,q]),verbose = 2)
    sdp.get_relaxation(level, objective=obj, inequalities=ines)
    #sdp.write_to_file('sdpa_'+str(T)+'.dat-s')
    sdp.solve(solver='mosek')
    #sdp.solve(solver='sdpa', solverparameters={"executable":"sdpa_gmp","executable": "C:/Users/zhouq/Documents/sdpa7-windows/sdpa.exe"})
    print(sdp.status)
    if(sdp.status != 'infeasible'):
        return sdp[m[T]]
    else:
        print('Cannot find feasible solution.')
        return