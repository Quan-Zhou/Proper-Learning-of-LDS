load('setting6.mat', 'seq_d0');
T=20;
pred=1;
nx=4;
endpoint=100;


for n=1:nx
    fit=zeros(endpoint,2);
    for s=1:endpoint
        sp=s;%randi([1 100],1,1);
        outputs=transpose(seq_d0(sp:sp+T+pred-1));
        [Y_predit,rmse_temp]=StateSpaceID(T,pred,n,outputs);
        fit(s,1)=Y_predit;
        fit(s,2)=rmse_temp;
    end
    writematrix(fit,"stock_MATLAB_d"+string(n)+".csv")
end

%s=[mean(fit),std(fit)];
%writematrix(s,'stock_MATLAB.csv')

%type 'stock_MATLAB.csv'

save stock_workspace

function [Y_predit,rmse]=StateSpaceID(T,pred,n,outputs)
% Build an input-output data in the time domain
%inputs = zeros(T+pred,1); % Inputs are all zeros
z = iddata(outputs,[],T+pred);

%%
ze = z(1:T);
zv = z(T+1:T+pred);
%plot(ze,zv)

%%
opt = ssestOptions;
opt.InitialState = 'estimate';%'estimate';
opt.Focus='prediction';
sys1=ssest(ze,n,opt);

f=forecast(sys1,ze,pred);
%f.OutputData
%compare(f,zv)

%% Collect nrmse of each model
rmse=abs(zv.OutputData-f.OutputData); 
Y_predit=f.OutputData(pred);
end
