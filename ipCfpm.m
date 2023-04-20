function X = ipCfpm(availableResourcesInFed, costsOfCPsInFed, vmInfo, userRequest)
    m = size(availableResourcesInFed,1);    %number of federations
    

    cvx_begin
        cvx_solver gurobi
    cvx_end
    X = availableResourcesInFed;
end