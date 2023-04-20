% clc
% clear
% availableResourcesInFed = [409, 696, 90; 
%      409, 696, 90; 
%      409, 696, 90; 
%      409, 696, 90; 
%      409, 696, 90; 
%      409, 696, 90];
% 
% costsOfCPsInFed = [0.03, 0.06, 0.12, 0.24; 0.045, 0.091, 0.182, 0.364; 0.048, 0.096, 0.192, 0.384; 0.033, 0.065, 0.13, 0.26;
%      0.055, 0.111, 0.222, 0.444; 0.04, 0.08, 0.16, 0.32];
% 
% vmInfo =  [1., 1.7, 0.22, 0.12;
%  2., 3.75, 0.48, 0.24;
%  4., 7.5, 0.98, 0.48;
%  8., 15., 1.99, 0.96];
% userRequest = [1 100 2 50];
% ipCfpm1(availableResourcesInFed, costsOfCPsInFed, vmInfo, userRequest)
% 

function X = ipCfpm(availableResourcesInFed, costsOfCPsInFed, vmInfo, userRequest)
    m = size(availableResourcesInFed,1)    %number of federations
    n = size(vmInfo,1)     %number of virtual machine types 
    
    p = vmInfo(:,4) %pricelist
    c = costsOfCPsInFed'    %costlist
    
    N = availableResourcesInFed(:,1)
    M = availableResourcesInFed(:,2)
    S = availableResourcesInFed(:,3)

    r = userRequest
    
    w_c = vmInfo(:,1)    
    w_m = vmInfo(:,2)    
    w_s = vmInfo(:,3)    
    

    %% cvx implementation: has bugs
    % cvx_begin
    %     cvx_solver gurobi
    %     variable x(m,n) integer;
    %     objective = 0;
    % 
    %     for i = 1:m
    %         objective = objective + x(i,:)*(p-c(:,i));
    %     end
    %     maximize(objective)
    %     subject to
    %         for i = 1:m
    %             x(i,:)*w_c<=N(i);
    %         end
    %         for i = 1:m
    %             x(i,:)*w_m<=M(i);
    %         end
    %         for i = 1:m
    %             x(i,:)*w_s<=S(i);
    %         end
    % 
    %         for j = 1:n
    %             sum(x(:,j))==r(:,j);
    %         end
    % 
    %         for i=1:m 
    %             sum(x(i,:))>=1;
    %         end
    %         for i = 1:m
    %             for j = 1:n
    %                 x(i,j)>=0;
    %             end
    %         end
    % cvx_end
    
    %% YALMIP implementation
    x = intvar(m,n);

    cons = [];
    for i = 1:m
        cons = [cons, x(i,:)*w_c<=N(i)];
    end
    for i = 1:m
        cons = [cons, x(i,:)*w_m<=M(i)];
    end
    for i = 1:m
        cons = [cons, x(i,:)*w_s<=S(i)];
    end

    for j = 1:n
        cons = [cons, sum(x(:,j))==r(:,j)];
    end

    for i=1:m 
        cons = [cons, sum(x(i,:))>=1];
    end
    for i = 1:m
        for j = 1:n
            cons = [cons, x(i,j)>=0];
        end
    end
    objective = 0;
    for i = 1:m
        objective = objective + x(i,:)*(p-c(:,i));
    end
    opt=sdpsettings('solver','gurobi','verbose',0);
    optimize(cons,-objective,opt)

    X = value(x);
end