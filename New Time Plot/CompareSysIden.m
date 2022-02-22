function fit=CompareSysIden(T)
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
% Randomly Select a Trajectory of Time Series
load('setting6.mat', 'seq_d0');
%T=25;
pred=1;
sp=randi([1 100],1,1);

% Build an input-output data in the time domain
outputs=transpose(seq_d0(sp:sp+T-1));
inputs = zeros(T,1); % Inputs are all zeros
z = iddata(outputs,inputs,T);

%% Estimate state-space models with structured parameterization
% Construct the parameter matrices 
A = [1 0;0 1];
B = zeros(2,1); 
C = [0 0]; 
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
%optlsq=opt;
%optlsq.SearchMethod='lsqnonlin';
%lsq = ssest(z,sys,'Ts',T,optlsq);

optss=n4sidOptions;
%optss.InitialState = idpar([]);
optss.Focus = 'simulation';%
optss.EnforceStability = true;
N4sid=n4sid(z,2,'Ts',T,optss);
optssa=optss;
optssa.N4Weight='SSARX';
ssa = n4sid(z,sys,'Ts',T,optssa);

%% Collect nrmse of each model
[~,fit,~]=compare(z,def,N4sid,ssa);

end



