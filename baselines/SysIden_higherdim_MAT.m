clear all
close all

%% Experimental set-up
repeat=30; % the number of experiments at the each noise std
met=3; % the number of system identification methods for comparison
T=30; % length of time windows in each experiment
num=3; % 4 dimensions of system matrices;
nrmse=cell(num,repeat,met);
%noise_std=linspace(0.1,0.9,num);
%nx_range=linspace(1,4,num);

%% load Y
Y=readmatrix('ncpop300_ydata_higherdim.csv',Range=[2 2]);

%% Experiments with system identification toolbox
for n=1:num
   for r=1:repeat
       fit_tmp=CompareSysIden_new(T,Y(:,n+3*(r-1)),n+1);
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
data = readmatrix('ncpop300_higherdim.csv',Range=[2 2]);
Z = transpose(data*100);
Z_mean=mean(Z,2);
Z_std=std(Z,0,2);
yData{met+1,1}=Z_mean;
errors{met+1,1}=Z_mean-Z_std;
errors{met+1,2}=Z_mean+Z_std;

%% save
save SysIden_higherdim_workspace
writecell(yData,'ncpop300_higherdim_mean_plot.csv')
writecell(errors,'ncpop300_higherdim_std_plot.csv')