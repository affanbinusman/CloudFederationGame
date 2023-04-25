function [x, profit] = ipCfpm(availableResourcesInFed, costsOfCPsInFed, vmInfo, userRequest)
    m = size(availableResourcesInFed,1);    %number of federations
    n = size(vmInfo,1);     %number of virtual machine types 
    
    p = vmInfo(:,4); %pricelist
    c = costsOfCPsInFed';    %costlist

    N = availableResourcesInFed(:,1);
    M = availableResourcesInFed(:,2);
    S = availableResourcesInFed(:,3);

    r = userRequest;
    
    w_c = vmInfo(:,1);    
    w_m = vmInfo(:,2);    
    w_s = vmInfo(:,3);    
    

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

    cons = []; %constraints

    % (2)
    for i = 1:m
        cons = [cons, x(i,:)*w_c<=N(i)];
    end
    % (3)
    for i = 1:m
        cons = [cons, x(i,:)*w_m<=M(i)];
    end

    % (4)
    for i = 1:m
        cons = [cons, x(i,:)*w_s<=S(i)];
    end

    % (5)
    for j = 1:n
        cons = [cons, sum(x(:,j))==r(:,j)];
    end
    
    % (6)
    for i=1:m 
        cons = [cons, sum(x(i,:))>=1];
    end

    % (7)
    for i = 1:m
        for j = 1:n
            cons = [cons, x(i,j)>=0];
        end
    end

    % objective (1)
    objective = 0;
    for i = 1:m
        objective = objective + x(i,:)*(p-c(:,i));
    end

    % solver settings
    opt=sdpsettings('solver','gurobi','verbose',0);
    optimize(cons,-objective,opt);

    % federation profit
    profit = value(objective);

    %V Ms required from each CP
    x = value(x);
end