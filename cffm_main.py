import cloudProvider
import virtualMachine
import userRequest
from collections import defaultdict

import numpy as np



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

    userRequest1 = np.array([1, 0, 2, 3])
    

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
    allFederations = [[1,2,3,4,5,6],[7,8]]

    '''
    we have 
    [[1,2,3,4,5,6]]

    6 X [[cor, mem, storag]] -> available Resoursec
    6 X [4] -> costs of 4 VMs in each CP
    '''
    # this is for just 1 federation with 6 CPs
    availableResourcesInFed = []
    costsOfCPsInFed = []
    for i in range(6):
        cp = federation[i]
        resOfThisCP = [int(cp.availableCores*0.4), int(cp.availableMemory*0.4), int(cp.availableStorage*0.4)]
        availableResourcesInFed.append(resOfThisCP)
        costsOfCPsInFed.append(cp.costList)

    

    print("availableResourcesInFed : \n", availableResourcesInFed)
    print("="*80)
    print("costsOfCPsInFed : \n", costsOfCPsInFed)