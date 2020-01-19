% Requirements
% Statistics and Machine Learning Toolbox
% https://ww2.mathworks.cn/help/stats/
% System Identification Toolbox
% https://ww2.mathworks.cn/help/ident/
% Optimization Toolbox
% https://ww2.mathworks.cn/help/optim/
% suplable
% https://ww2.mathworks.cn/matlabcentral/fileexchange/7772-suplabel
% CompareSysIden
% https://github.com/Quan-Zhou/Proper-Learning-of-LDS/blob/master/CompareSysIden.m

% This file is used to conduct experiments with four system identification
% methods and illustrate the results as box-plots.

clear all
close all
%% Parameters
num=25; % the number of noise standard deviations
repeat=30; % repeating times at the same noise std
met=4; % the number of system identification methods

std=linspace(0.01,1,num);
nrmse=cell(num,repeat,met);
T=20; % length of estimation data of each experiment

%% Experiments
for n=1:num
   s=std(n);
   for r=1:repeat
       fit_tmp=CompareSysIden(T,s,s);
       for m=1:met
           nrmse{n,r,m}=fit_tmp{m,1};
       end
   end
end

%% Outputs
titles={'least squares auto','lsqnonlin','subspace auto','ssarx'};
figure;
for m=1:met
    nrmse_tmp=nrmse(:,:,m);
    yData_tmp=cell2mat(nrmse_tmp)';
    subplot(floor(met/2),2,m);
    boxplot(yData_tmp,roundn(std,-2),'PlotStyle','compact')
    title(titles(m));
end
suplabel('noise standard deviations','x');
suplabel('nrmse(%)','y');
suplabel('Other System Identification Methods','t');






