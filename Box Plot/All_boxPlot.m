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


%% Plot
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
% Read experiment results of our method
data = csvread('Zout.csv');
subplot(ceil(met/2),2,met+1);
boxplot(data*100,roundn(noise_std,-2),'PlotStyle','compact')
title(titles(met+1));

suplabel('noise std','x');
suplabel('nrmse(%)','y');
%suplabel('All System Identification Methods boxplot','t');

save All_boxPlot_workspace




