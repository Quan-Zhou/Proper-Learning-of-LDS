function fit=CompareSysIden_new(T,Y,nx)
% The function is used to compare the simulation of four system identification methods

% Inputs:
% T: the length of estimation data
% Y: the time series
% Outputs:
% fit: nrmse values of four system identification methods.

% Required Toolboxs:
% System Identification Toolbox
% https://ww2.mathworks.cn/help/ident/
% Optimization Toolbox
% https://ww2.mathworks.cn/help/optim/

%% Creates an IDDATA object with outputs of LDS and zero inputs
% Build an input-output data in the time domain
outputs=Y;%transpose(Y);
inputs = zeros(T,1); % Inputs are all zeros
z = iddata(outputs,inputs,T);

%% Estimate state-space models with structured parameterization

opt = ssestOptions;
opt.Focus = 'simulation';
%opt.EnforceStability = true;
def=ssest(z,nx,'Ts',T,opt);
%optlsq=opt;
%optlsq.SearchMethod='lsqnonlin';
%lsq = ssest(z,sys,'Ts',T,optlsq);

optss=n4sidOptions;
%optss.InitialState = idpar([]);
optss.Focus = 'simulation';%
optss.EnforceStability = true;
N4sid=n4sid(z,nx,'Ts',T,optss);
optssa=optss;
optssa.N4Weight='SSARX';
ssa = n4sid(z,nx,'Ts',T,optssa);

%% Collect nrmse of each model
[~,fit,~]=compare(z,def,N4sid,ssa);

end



