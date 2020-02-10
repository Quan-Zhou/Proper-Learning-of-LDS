from inputlds import*
from ncpol2sdpa import*
import numpy as np
import pandas as pd
from math import sqrt
import matplotlib.pyplot as plt 

def SimCom(proc_noise_std,obs_noise_std,T,level):
# Define a function for solving the NCPO problems with 
# given standard deviations of process noise and observtion noise,
# length of  estimation data and required relaxation level. 
    
            # Generate Dynamic System ds1
            g = np.matrix([[0.99,0],[1,0.2]])
            f_dash = np.matrix([[1.0,1.0]])
            ds1 = dynamical_system(g,np.zeros((2,1)),f_dash,np.zeros((1,1)),
                  process_noise='gaussian',
                  observation_noise='gaussian', 
                  process_noise_std=proc_noise_std, 
                  observation_noise_std=obs_noise_std)
            h0= np.ones(ds1.d)
            inputs = np.zeros(T)
            ds1.solve(h0=h0, inputs=inputs, T=T)    
            Y=[]
            for i in range (0,T):
                Y.append(ds1.outputs[i].tolist())
            Y = flatten(Y)
            
            # Decision Variables
            G = generate_operators("G", n_vars=1, hermitian=True, commutative=False)[0]
            Fdash = generate_operators("Fdash", n_vars=1, hermitian=True, commutative=False)[0]
            m = generate_operators("m", n_vars=T+1, hermitian=True, commutative=False)
            q = generate_operators("q", n_vars=T, hermitian=True, commutative=False)
            p = generate_operators("p", n_vars=T, hermitian=True, commutative=True)
            f = generate_operators("f", n_vars=T, hermitian=True, commutative=True)

            # Objective
            obj = sum((Y[i]-f[i])**2 for i in range(T)) + 0.0005*sum(p[i]**2 for i in range(T)) #+ 0.01*sum(q[i]**2 for i in range(T))

            # Constraints
            ine1 = [f[i] - Fdash*m[i+1] - p[i] for i in range(T)]
            ine2 = [-f[i] + Fdash*m[i+1] + p[i] for i in range(T)]
            ine3 = [m[i+1] - G*m[i] - q[i] for i in range(T)]
            ine4 = [-m[i+1] + G*m[i] + q[i] for i in range(T)]
            ine5 = [(Y[i]-f[i])**2 for i in range(T)]
            ines = ine1+ine2+ine3+ine4+ine5

            # Solve the NCPO
            sdp = SdpRelaxation(variables = flatten([G,Fdash,f,p,m,q]),verbose = 2)
            sdp.get_relaxation(level, objective=obj, inequalities=ines)
            sdp.solve(solver='sdpa', solverparameters={"executable":"sdpa_gmp","executable": "C:\\Users\\zhouq\\Documents\\sdpa7-windows\\sdpa.exe"})
            #print(sdp.primal, sdp.dual, sdp.status)
            if (sdp[sum((Y[i]-f[i])**2 for i in range(T))] < 0):
                print("sum((Y[i]-f[i])**2 for i in range(T)) < 0")
                return 
            
            nrmse_sim = 1-sqrt(sdp[sum((Y[i]-f[i])**2 for i in range(T))])/sqrt(sum((Y[i]-np.mean(Y))**2 for i in range(T)))
            
            if(sdp.status != 'infeasible'):
                 print(nrmse_sim)
                 return nrmse_sim
            else:
                 print('Cannot find feasible solution.')


# Set parameters
start=0.1
stop=1.1
step=0.1
T=20
level=1

# Collect the nrmse value for each experiment
# The function SimCom() might fail to find any feasible solutions
pro_rang = np.arange(start,stop,step)
obs_rang = np.arange(start,stop,step)
proL=len(pro_rang)
obsL=len(obs_rang)
Z = np.zeros((proL,obsL))
N = np.zeros((proL,obsL))

for i in range(proL):
    for j in range(obsL):
        for n in range(6):
            print(n)
            tmp=SimCom(pro_rang[i],obs_rang[j],T,level)
            if (tmp):
                Z[i,j] = tmp
                N[i,j] = n
                break
           

# Check is there any failed experiment
# If yes, do the failed ones more times until success
for i in range(proL):
    for j in range(obsL):
        if (Z[i,j]==0):
            print(i,j)
            tmp=SimCom(pro_rang[i],obs_rang[j],T,level)
            if (tmp):
                Z[i,j] = tmp
                break

# Plot
cset = plt.contourf(X,Y,Z,cmap=plt.get_cmap('spring')) 
contour = plt.contour(X,Y,Z,3,colors='k')
plt.colorbar(cset)
plt.xlabel('process noise std',fontsize=10)
plt.ylabel('observation noise std',fontsize=10)
plt.show()



   