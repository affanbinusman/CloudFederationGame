import cloudProvider
from collections import defaultdict
import matlab
import matlab.engine
import matplotlib.pyplot as plt
import numpy as np

noOfTestCases = 10
eng = matlab.engine.start_matlab()

'''
    The following variable vmInfo contains the information of 
    all 4 VM types(S, M, L, XL) and 
    their 4 attributes(cores, memory, storage, price) respectively
    '''
vmInfo = np.array([[1, 1.7, 0.22, 0.12],\
                    [2, 3.75, 0.48, 0.24],\
                    [4, 7.5, 0.98, 0.48],\
                    [8, 15, 1.99, 0.96]])

def OptimizerSolver(availableResourcesInFed, costsOfCPsInFed, userRequest, vmInfo = vmInfo):
        
        availableResourcesInFed = matlab.double(availableResourcesInFed)
        costsOfCPsInFed = matlab.double(costsOfCPsInFed)
        vmInfo = matlab.double(vmInfo)
        userRequest = matlab.double(userRequest)
        x, profit = eng.ipCfpm(availableResourcesInFed, costsOfCPsInFed, vmInfo, userRequest, nargout=2)
        
        if profit == 0:
            # print("Problem not solvable")
            pass
        else:
            x = np.array(x).round()

        return x, profit

def updateFederationResources(federationResouce, cp):
    federationResouce["availableCores"] += int(cp.availableCores * 0.4)
    federationResouce["availableMemory"] += int(cp.availableMemory * 0.4)
    federationResouce["availableStorage"] += int(cp.availableStorage * 0.4)
    return federationResouce

def fed_res_cost(federation):
    availableResourcesInFed = []
    costsOfCPsInFed = []
    for i in range(len(federation)):
        cp = federation[i]
        resOfThisCP = [int(cp.availableCores*0.4), int(cp.availableMemory*0.4), int(cp.availableStorage*0.4)]
        availableResourcesInFed.append(resOfThisCP)
        costsOfCPsInFed.append(cp.costList)

    return availableResourcesInFed, costsOfCPsInFed

def mergeFederations(FS, profitList, userRequest):

    i = 0
    while (i < len(FS)):
        j = i + 1

        while(j < len(FS)):

            keysList = list(FS.keys())
            combinedF = FS[keysList[i]].copy()
            combinedF += FS[keysList[j]]
            
            availableResourcesInFed, costsOfCPsInFed = fed_res_cost(combinedF)
            _, profit = OptimizerSolver(availableResourcesInFed, costsOfCPsInFed, userRequest)
            
            if (profit > profitList[i] and profit > profitList[j]) \
                or (profit == 0 and profitList[i]==0 and profitList[j]==0):
                profitList[i] = profit
                profitList.pop(j)
                FS[keysList[i]] = combinedF
                del FS[keysList[j]]
            else:
                j += 1 

        i += 1

    return FS, profitList

def splitFederations(FS, profitList, userRequest):
    res = defaultdict()
    newProfitList = list()

    for iVal, kVal in enumerate(FS):
        flag = False
        currentFed = FS[kVal]
        if len(currentFed) > 1:
            combinedProfit = profitList[iVal]
            
            if combinedProfit != 0:
                for i in range(len(currentFed)):
                    
                    Fj = [currentFed[i]]
                    availableResourcesInFed, costsOfCPsInFed = fed_res_cost(Fj)
                    x, profitFj = OptimizerSolver(availableResourcesInFed, costsOfCPsInFed, userRequest)
                    
                    Fk = currentFed[0:i] + currentFed[i+1:]
                    availableResourcesInFed, costsOfCPsInFed = fed_res_cost(Fk)
                    x2, profitFk = OptimizerSolver(availableResourcesInFed, costsOfCPsInFed, userRequest)
                    
                    if profitFj >= combinedProfit or profitFk >= combinedProfit:
                        res[kVal] = Fj
                        newProfitList.append(profitFj)
                        for index in range(1, list(FS.keys())[-1] + 200):     # FS is not dynamically being updated & issue with Fk
                            if (index not in list(FS.keys())) and (index not in list(res.keys())):
                                res[index] = Fk
                                newProfitList.append(profitFk)
                                break
                        flag = True
                        break
            if flag == False:
                res[kVal] = FS[kVal]
                newProfitList.append(profitList[iVal])
        else: 
            res[kVal] = FS[kVal]
            newProfitList.append(profitList[iVal])
        
    return res, newProfitList

def writename(FS_algo1_2):
        l = list()
        for i in FS_algo1_2:
            print("This is Federation ", i)
            _ = [print(j.name) for j in FS_algo1_2[i]]

def myMain(userRequest1):
    
    federation = []
    federationResouce = {"availableCores" : 0, "availableMemory" : 0, "availableStorage" : 0}

    cl1 = [0.03, 0.06, 0.12, 0.24]
    cp1 = cloudProvider.cloudProvider("cp1", 1024*0.25, 1740*0.25, 225*0.25, cl1)
    federation.append(cp1)
    federationResouce = updateFederationResources(federationResouce, cp1)

    cl2 = [0.045, 0.091, 0.182, 0.364]
    cp2 = cloudProvider.cloudProvider("cp2", 1024*0.5, 1740*0.5, 225*0.5, cl2)
    federation.append(cp2)
    federationResouce = updateFederationResources(federationResouce, cp2)

    cl3 = [0.048, 0.096, 0.192, 0.384]
    cp3 = cloudProvider.cloudProvider("cp3", 1024*0.75, 1740*0.75, 225*0.75, cl3)
    federation.append(cp3)
    federationResouce = updateFederationResources(federationResouce, cp3)

    cl4 = [0.033, 0.065, 0.130, 0.260]
    cp4 = cloudProvider.cloudProvider("cp4", 1024, 1740, 225, cl4)
    federation.append(cp4)
    federationResouce = updateFederationResources(federationResouce, cp4)

    cl5 = [0.055, 0.111, 0.222, 0.444]
    cp5 = cloudProvider.cloudProvider("cp5", 1024*1.125, 1740*1.125, 225*1.125, cl5)
    federation.append(cp5)
    federationResouce = updateFederationResources(federationResouce, cp5)

    cl6 = [0.04, 0.08, 0.16, 0.32]
    cp6 = cloudProvider.cloudProvider("cp6", 1024*1.25, 1740*1.25, 225*1.25, cl6)
    federation.append(cp6)
    federationResouce = updateFederationResources(federationResouce, cp6)

    cl7 = [0.058, 0.115, 0.230, 0.460]
    cp7 = cloudProvider.cloudProvider("cp7", 1024*1.4, 1740*1.4, 225*1.4, cl7)
    federation.append(cp7)
    federationResouce = updateFederationResources(federationResouce, cp7)

    cl8 = [0.044, 0.088, 0.175, 0.350]
    cp8 = cloudProvider.cloudProvider("cp8", 1024*1.5, 1740*1.5, 225*1.5, cl8)
    federation.append(cp8)
    federationResouce = updateFederationResources(federationResouce, cp8)

    # Cloud Federation Structure
    FS = { 1: [federation[0]],
          2: [federation[1]],
          3: [federation[2]],
          4: [federation[3]],
          5: [federation[4]],
          6: [federation[5]],
          7: [federation[6]],
          8: [federation[7]]
    }
    
    # Algo 1
    V_Check = 0
    V_CheckProfit = list()
    for i in FS:
        availableResourcesInFed, costsOfCPsInFed = fed_res_cost(FS[i])
        _, profit = OptimizerSolver(availableResourcesInFed, costsOfCPsInFed, userRequest1)
        V_CheckProfit.append(profit)
        V_Check += 1
    
    print(V_CheckProfit)
    initialMax = max(V_CheckProfit)

    FS_algo1_2 = FS.copy()
    
    while(1):
         
        # call Merge Federations
        FS_algo1_2, V_CheckProfit = mergeFederations(FS_algo1_2, V_CheckProfit, userRequest1)
        print()
        print("-"*60)
        print("After Merge, the Federation Structure includes:")
        writename(FS_algo1_2)
        print("\nWith the following profit list")
        print(V_CheckProfit)
            
        if len(V_CheckProfit) == 1:
            if V_CheckProfit[0] == 0:
                print("Problem too big to be solved by Grand Federation")
                break
        
        curr_length = len(FS_algo1_2)
        
        # Call SPlit federations
        FS_algo1_2, V_CheckProfit = splitFederations(FS_algo1_2, V_CheckProfit, userRequest1)
        print()
        print("-"*60)
        print("After Split, the Federation Structure includes:")
        writename(FS_algo1_2)
        print("\nWith the following profit list")
        print(V_CheckProfit)

        if curr_length == len(FS_algo1_2):
            break
    
    maxProfit = max(V_CheckProfit)
    maxProfitIndex = V_CheckProfit.index(maxProfit)
    
    print("-"*60)
    print("-"*60)
    print("-"*60)
    print("Finally, the follow Federation allocates & provides the requested VM instances.\n")
    print("Maximum Profit:", maxProfit)
    maxProfitKey = list(FS_algo1_2.keys())[maxProfitIndex]
    maxProfitFed = FS_algo1_2[maxProfitKey]
    writename({maxProfitKey: maxProfitFed})
    print("-"*60)
    print("-"*60)
    print("-"*60)
    print()
    return initialMax, maxProfit

if __name__ == "__main__":
    
    initialMax, maxProfit, reqNames, ureqs = list(), list(), list(), list()
    for i in range(noOfTestCases):
        s = float(np.random.randint(20,50))
        m = float(np.random.randint(10,50))
        l = float(np.random.randint(15,40))
        xl = float(np.random.randint(5,40))
        userRequest1 = np.array([s, m, l, xl])
        r1, r2 = myMain(userRequest1)
        initialMax.append(r1)
        maxProfit.append(r2)
        reqNames.append(i+1)
        ureqs.append(userRequest1)

    print()
    print(initialMax, "\n", maxProfit)
    print(ureqs)

    # Plotting the bars
    bar_width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(reqNames, initialMax, bar_width, label='Individual Max Profit')
    rects2 = ax.bar([req + bar_width for req in reqNames], maxProfit, bar_width, label='Federation Max Profit')
    
    # Adding labels and legend
    ax.set_xlabel('User Requests')
    ax.set_ylabel('Maximum Profit')
    ax.set_title('Profit Comparison')
    ax.set_xticks([month + bar_width/2 for month in range(len(reqNames)+1)])
    ax.set_yticks([i for i in range(0, int(max(maxProfit))+20, 10)])
    reqNames = [0] + reqNames
    ax.set_xticklabels(reqNames)
    ax.legend()
    plt.show()
    
    # Do this at the end of the program
    eng.quit()