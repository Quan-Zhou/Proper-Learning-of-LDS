clear all
close all

%% Experimental set-up
num=10; % 10 noise standard deviations from 0.1 to 1.0
noise_std=linspace(0.1,1,num);
repeat=30; % the number of experiments at the each noise std
met=3; % the number of system identification methods for comparison
T=20; % length of time windows in each experiment
nrmse=cell(num,repeat,met);

%% Experiments
for n=1:num
   s=noise_std(n);
   for r=1:repeat
       fit_tmp=CompareSysIden(T,s,s);
       for m=1:met
           nrmse{n,r,m}=fit_tmp{m,1};
       end
   end
end

%% Sort out experiment results
yData=cell(met+1,1); 
errors=cell(met+1,2);
for m=2:met+1
    nrmse_tmp=nrmse(:,:,m-1);
    fit=cell2mat(nrmse_tmp);
    fit_mean=mean(fit,2);
    fit_std=std(fit,0,2);
    yData{m,1}=fit_mean;
    errors{m,1}=fit_mean-fit_std;
    errors{m,2}=fit_mean+fit_std;
end

%% Plot
% Read experiment results of our method
data = csvread('Zout.csv');
Z = transpose(data*100);
Z_mean=mean(Z,2);
Z_std=std(Z,0,2);
yData{1,1}=Z_mean;
errors{1,1}=Z_mean-Z_std;
errors{1,2}=Z_mean+Z_std;

options.errors = errors;
options.errorStyle = {'--'};
options.errorColors = [1 0 1
    0 0 1
    .5 1 .83
    .92 .64 .38];

options.colors = [1 0 1
    0 0 1
    .5 1 .83
    .92 .64 .38];

options.title = '';
options.xlabel = 'noise std';
options.ylabel = 'nrmse(%)';
options.legend = {'our method','least squares auto','subspace auto','ssarx'};%{,'N4sid'
options.legendLoc = 'Southeast';
options.labelLines = 0;
options.errorFill = 0;
options.lineWidth = 1.5;

figure;
prettyPlot(noise_std,yData,options);
xlim([0.1 1.0])
xticks([0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0])
ylim([-350 150])
yticks([-350 -100 0 50 100])
%legend("boxoff")


save All_prettyPlot_workspace