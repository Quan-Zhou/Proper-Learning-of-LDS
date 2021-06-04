clear all
close all

%% Experiment
% "Least squares auto" method
load setting6;
start=1;
stop=200;
step=4;
Y=transpose(seq_d0(start:step:stop));
T=size(Y,1);
inputs = zeros(T,1); % Inputs are all zeros
z = iddata(Y,inputs,T);

order = 3;
opt = ssestOptions;
def = ssest(z,order,'Ts',T,opt);
[sim,fit,~]=compare(z,def);

% Our method
% Read from 'stock_NCPO.csv'
stock_NCPO=csvread('stock_NCPO.csv');

%% Plot
hold on
plot(Y, 'linestyle',':','marker','+','markersize',10,'color','black','linewidth',1);
plot(stock_NCPO,'color','m','linewidth',2);
plot(sim.outputdata,'color','b','linewidth',2);
legend_str=cell(3,1);
legend_str{1}= ['ground truth'];
legend_str{2}= ['our method 95.73%'];
legend_str{3}= ['least squares auto ' num2str(fit, '%4.2f') '%'];
legend(legend_str,'Location','NorthWest')
xlabel('time t')
ylabel('forecast f(t)')
ylim([30,41]);
box on
hold off

save Two_timePlot_workspace


ps = get(gcf, 'Position');
ratio = (ps(4)-ps(2)) / (ps(3)-ps(1))
paperWidth = 10;
paperHeight = paperWidth*ratio;

set(gcf, 'paperunits', 'centimeters');
set(gcf, 'papersize', [paperWidth paperHeight]);
set(gcf, 'PaperPosition', [0    0   paperWidth paperHeight]);

print(gcf, '-dpdf', 'timePlot.pdf');


