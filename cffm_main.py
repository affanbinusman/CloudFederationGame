import cloudProvider
import virtualMachine
import userRequest
from collections import defaultdict
import matlab
import matlab.engine
import MergeFederations
import SplitFederation
# import BanzhafValue
# import OptimizerSolver

import numpy as np

eng = matlab.engine.start_matlab()

def OptimizerSolver(availableResourcesInFed, costsOfCPsInFed, vmInfo, userRequest):
        
        availableResourcesInFed = matlab.double(availableResourcesInFed)
        costsOfCPsInFed = matlab.double(costsOfCPsInFed)
        vmInfo = matlab.double(vmInfo)
        userRequest = matlab.double(userRequest)
        x, profit = eng.ipCfpm(availableResourcesInFed, costsOfCPsInFed, vmInfo, userRequest, nargout=2)
        
        if profit == 0:
            print("Problem not solvable")
        else:
            x = np.array(x).round()
            
            # print()
            # # print(x)
            # print(profit)
        return x, profit

def updateFederationResources(federationResouce, cp):
    federationResouce["availableCores"] += int(cp.availableCores * 0.4)
    federationResouce["availableMemory"] += int(cp.availableMemory * 0.4)
    federationResouce["availableStorage"] += int(cp.availableStorage * 0.4)
    return federationResouce

if __name__ == "__main__":
    
    # print("Entering")
    ## Adding a sample comment
    federation = []
    federationResouce = {"availableCores" : 0, "availableMemory" : 0, "availableStorage" : 0}

    priceList = [0.12, 0.24, 0.48, 0.96]

    cl1 = [0.03, 0.06, 0.12, 0.24]
    cp1 = cloudProvider.cloudProvider("cp1", 1024, 1740, 225, cl1)
    federation.append(cp1)
    federationResouce = updateFederationResources(federationResouce, cp1)

    cl2 = [0.045, 0.091, 0.182, 0.364]
    cp2 = cloudProvider.cloudProvider("cp2", 1024, 1740, 225, cl2)
    federation.append(cp2)
    federationResouce = updateFederationResources(federationResouce, cp2)

    cl3 = [0.048, 0.096, 0.192, 0.384]
    cp3 = cloudProvider.cloudProvider("cp3", 1024, 1740, 225, cl3)
    federation.append(cp3)
    federationResouce = updateFederationResources(federationResouce, cp3)

    cl4 = [0.033, 0.065, 0.130, 0.260]
    cp4 = cloudProvider.cloudProvider("cp4", 1024, 1740, 225, cl4)
    federation.append(cp4)
    federationResouce = updateFederationResources(federationResouce, cp4)

    cl5 = [0.055, 0.111, 0.222, 0.444]
    cp5 = cloudProvider.cloudProvider("cp5", 1024, 1740, 225, cl5)
    federation.append(cp5)
    federationResouce = updateFederationResources(federationResouce, cp5)

    cl6 = [0.04, 0.08, 0.16, 0.32]
    cp6 = cloudProvider.cloudProvider("cp6", 1024, 1740, 225, cl6)
    federation.append(cp6)
    federationResouce = updateFederationResources(federationResouce, cp6)

    cl7 = [0.058, 0.115, 0.230, 0.460]
    cp7 = cloudProvider.cloudProvider("cp7", 1024, 1740, 225, cl7)
    federation.append(cp7)
    federationResouce = updateFederationResources(federationResouce, cp7)

    cl8 = [0.044, 0.088, 0.175, 0.350]
    cp8 = cloudProvider.cloudProvider("cp8", 1024, 1740, 225, cl8)
    federation.append(cp8)
    federationResouce = updateFederationResources(federationResouce, cp8)
   
    inputToOptimizer = []

    ur1 = userRequest.userRequest(1, 0, 2, 3)
    userRequest1 = np.array([100.0, 50.0, 200.0, 50.0])
    userRequest1 = np.array([1.0, 0.0, 0.0, 0.0])
    

    '''
    The following variable vmInfo contains the information of 
    all 4 VM types(S, M, L, XL) and 
    their 4 attributes(cores, memory, storage, price) respectively
    '''
    vmInfo = np.array([[1, 1.7, 0.22, 0.12],\
                       [2, 3.75, 0.48, 0.24],\
                       [4, 7.5, 0.98, 0.48],\
                       [8, 15, 1.99, 0.96]])
    

    ## Cloud Federation Structure
    # allFederations = [[1,2,3,4,5,6],[7,8]]
    FS = [[1], [2], [3], [4], [5], [6, 7], [8]]
    FS = { 1: [federation[0]],
          2: [federation[1]],
          3: [federation[2]],
          4: [federation[3]],
          5: [federation[4]],
          6: [federation[5]],
          7: [federation[6]],
          8: [federation[7]]
    }
    # print(FS)
    '''
    we have 
    [[1,2,3,4,5,6]]

    6 X [[cor, mem, storag]] -> available Resoursec
    6 X [4] -> costs of 4 VMs in each CP
    '''
    # this is for just 1 federation with 6 CPs
    def fed_res_cost(federation):
        availableResourcesInFed = []
        costsOfCPsInFed = []
        # print(len(federation))
        for i in range(len(federation)):
            cp = federation[i]
            resOfThisCP = [int(cp.availableCores*0.4), int(cp.availableMemory*0.4), int(cp.availableStorage*0.4)]
            availableResourcesInFed.append(resOfThisCP)
            costsOfCPsInFed.append(cp.costList)

        # print("availableResourcesInFed : \n", availableResourcesInFed)
        # print("="*80)
        # print("costsOfCPsInFed : \n", costsOfCPsInFed)

        return availableResourcesInFed, costsOfCPsInFed


    # availableResourcesInFed, costsOfCPsInFed = fed_res_cost(federation)
    # OptimizerSolver(availableResourcesInFed, costsOfCPsInFed, vmInfo, userRequest1)
    

    # Algo 1
    V_Check = 0
    V_CheckProfit = list()
    for i in FS:
        # print("federation: ", federation)
        # print("federation[i] :", federation[i])
        availableResourcesInFed, costsOfCPsInFed = fed_res_cost(FS[i])
        _, profit = OptimizerSolver(availableResourcesInFed, costsOfCPsInFed, vmInfo, userRequest1)
        V_CheckProfit.append(profit)
        V_Check += 1
    
    print(V_CheckProfit)
    # checkMSFlag = True
    # checkedMergeFed = defaultdict()
    # while checkMSFlag:
    #     FS, checkedMergeFed, V_CheckProfit = MergeFederations.MergeFederations(FS, checkedMergeFed, V_CheckProfit)
    #     currLength = len(FS)
    #     FS, V_CheckProfit = SplitFederation.SplitFederation(FS, V_CheckProfit)
    #     if currLength == len(FS):
    #         break
    

    # maxFederation = np.argmax(V_CheckProfit)

    # for F in FS[maxFederation]:
    #     BV = BanzhafValue.BanzhafValue()
    #     # Ouput result // VM types + Numbers by each cloud provider Ci in the Federation Fk

    # Do this at the end of the program
    eng.quit()