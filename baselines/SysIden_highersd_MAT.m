clear all
close all

%% Experimental set-up
repeat=30; % the number of experiments at the each noise std
met=3; % the number of system identification methods for comparison
T=20; % length of time windows in each experiment
num=9; % 10 noise standard deviations from 0.1 to 0.9
nrmse=cell(num,repeat,met);
noise_std=linspace(0.1,0.9,num);
nx=2;

%% load Y
Y=readmatrix('ncpop300_ydata_highersd.csv',Range=[2 2]);

%% Experiments with system identification toolbox
for n=1:num
   for r=1:repeat
       fit_tmp=CompareSysIden_new(T,Y(:,n+9*(r-1)),nx);
       for m=1:met
           nrmse{n,r,m}=fit_tmp{m,1};
       end
   end
end

%% Sort out experiment results
yData=cell(met,1); 
errors=cell(met,2);
for m=1:met
    nrmse_tmp=nrmse(:,:,m);
    fit=cell2mat(nrmse_tmp);
    fit_mean=mean(fit,2);
    fit_std=std(fit,0,2);
    yData{m,1}=fit_mean;
    errors{m,1}=fit_mean-fit_std;
    errors{m,2}=fit_mean+fit_std;
end

%% our method
% Read experiment results of our method
data = readmatrix('ncpop300_highersd.csv',Range=[2 2]);
Z = transpose(data*100);
Z_mean=mean(Z,2);
Z_std=std(Z,0,2);
yData{met+1,1}=Z_mean;
errors{met+1,1}=Z_mean-Z_std;
errors{met+1,2}=Z_mean+Z_std;

%% save
save SysIden_highersd_workspace
writecell(yData,'ncpop300_highersd_mean_plot.csv')
writecell(errors,'ncpop300_highersd_std_plot.csv')

%% pretty plot
options.errors = errors;
options.errorStyle = {'--'};
options.errorColors = [.55 .55 1
	.55 1 .55
	1 .35 .75
    1 .65 0];

options.colors = [.55 .55 1
	.55 1 .55
	1 .35 .75
    1 .65 0];

options.title = '';
options.xlabel = 'noise std';
options.ylabel = 'nrmse(%)';
options.legend = {'least squares auto','subspace auto','ssarx','our method'};%{,'N4sid'
options.legendLoc = 'SouthEast';
options.labelLines = 0;
options.errorFill = 0;
options.lineWidth = 1.5;

figure;
prettyPlot(noise_std,yData,options);
xlim([0.1 0.9])
xticks([0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9])
ylim([-150 150])
yticks([-100 0 50 100])

%% box plot

titles={'least squares auto','subspace auto','ssarx','our method'};

figure;
% Other system identification methods
for m=1:met
    nrmse_tmp=nrmse(:,:,m);
    yData_tmp=cell2mat(nrmse_tmp)';
    subplot(ceil(met/2),2,m);
    boxplot(yData_tmp,roundn(noise_std,-2),'PlotStyle','compact')
    title(titles(m));
end

% Our method
% load experiment results of our method
%data = readmatrix('ncpop300_highersd.csv',Range=[2 2]);
subplot(ceil(met/2),2,met+1);
boxplot(data*100,roundn(noise_std,-2),'PlotStyle','compact')
title(titles(met+1));

suplabel('noise std','x');
suplabel('nrmse(%)','y');
%suplabel('All System Identification Methods boxplot','t');
