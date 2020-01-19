function fit=CompareSysIden(T,proc_std,obs_std)
% The function is used to compare the simulation of four system identification methods

% Inputs:
% T: the length of estimation data
% proc_std: the standard deviation of process noise
% obs_std: the standard deviation of observation noise

% Outputs:
% fit: nrmse values of four system identification methods.

% Required Toolboxs:
% System Identification Toolbox
% https://ww2.mathworks.cn/help/ident/
% Optimization Toolbox
% https://ww2.mathworks.cn/help/optim/

%% Creates an IDDATA object with outputs of LDS and zero inputs
% Generate Outputs of the underlying LDS
g = [0.99 0; 1 0.2];
fdash = [1 1];
m0 = [1;1];
Y=zeros(T,1);
m=cell(T+1,1);
m{1,1}=m0;

for t=1:T
    proc_noise=randn(2,1)*proc_std;
    obs_noise=randn*obs_std;
    m{t+1}=g*m{t}+proc_noise;
    Y(t,1)=fdash*m{t+1}+obs_noise;
end

% Build an input-output data in the time domain
outputs=Y;
inputs = zeros(T,1); % Inputs are all zeros
z = iddata(outputs,inputs,T);

%% Estimate state-space models with structured parameterization
% Construct the parameter matrices 
A = g;
B = zeros(2,1); 
C = fdash; 
D = 0; 
K = [1;1];
sys = idss(A,B,C,D,K,'Ts',T);

S = sys.Structure;
S.B.Free = false;
S.D.Free = false;
sys.Structure = S;

opt = ssestOptions;
opt.Focus = 'simulation';
%opt.EnforceStability = true;
def=ssest(z,sys,'Ts',T,opt);
optlsq=opt;
optlsq.SearchMethod='lsqnonlin';
lsq = ssest(z,sys,'Ts',T,optlsq);

optss=n4sidOptions;
optss.InitialState = idpar(m0);
optss.Focus = 'simulation';%
optss.EnforceStability = true;
N4sid=n4sid(z,2,'Ts',T,optss);
optssa=optss;
optssa.N4Weight='SSARX';
ssa = n4sid(z,sys,'Ts',T,optssa);

%% Collect nrmse of each model
[~,fit,~]=compare(z,def,lsq,N4sid,ssa);

end



