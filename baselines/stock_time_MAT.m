load('setting6.mat', 'seq_d0');
endpoint=3;
run_all=zeros(21,3);
for n=2:2
for T=20:30
    run=zeros(endpoint,1);
for s=1:endpoint
    sp=randi([1 100],1,1);
    outputs=transpose(seq_d0(sp:sp+T-1));
    %[Y_predit,rmse_temp]=StateSpaceID(T,pred,n,outputs);
    run(s,1)=StateSpaceID(T,n,outputs);
end
run_all(T-19,1:3)=[T,mean(run),std(run)];
end
writematrix(run_all,"stock_time_MAT_d"+string(n)+".csv")
end
%s=[mean(fit),std(fit)];
%writematrix(s,'stock_MATLAB.csv')

%type 'stock_MATLAB.csv'

%save stock_workspace

function runtime=StateSpaceID(T,n,outputs)
% Build an input-output data in the time domain
%inputs = zeros(T+pred,1); % Inputs are all zeros
z = iddata(outputs,[],T);

%%
ze = z(1:T);

%%
opt = ssestOptions;
opt.InitialState = 'estimate';%'estimate';
opt.Focus='simulation';
tic;
sys1=ssest(ze,n,opt);
runtime=toc;

%f=forecast(sys1,ze,pred);
%f.OutputData
%compare(f,zv)

%% Collect nrmse of each model
%rmse=abs(zv.OutputData-f.OutputData); 
%Y_predit=f.OutputData(pred);

end
