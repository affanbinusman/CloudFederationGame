import cloudProvider
import virtualMachine
import userRequest
from collections import defaultdict

def updateFederationResources(federationResouce, cp):
    federationResouce["availableCores"] += int(cp.availableCores * 0.4)
    federationResouce["availableMemory"] += int(cp.availableMemory * 0.4)
    federationResouce["availableStorage"] += int(cp.availableStorage * 0.4)
    return federationResouce

if __name__ == "__main__":
    
    print("GIT experiment")
    federation = []
    federationResouce = {"availableCores" : 0, "availableMemory" : 0, "availableStorage" : 0}
    cp1 = cloudProvider.cloudProvider("cp1", 1024, 1740, 225)
    federation.append(cp1)
    federationResouce = updateFederationResources(federationResouce, cp1)

    cp2 = cloudProvider.cloudProvider("cp2", 1024, 1740, 225)
    federation.append(cp2)
    federationResouce = updateFederationResources(federationResouce, cp2)


    ur1 = userRequest.userRequest(1, 0, 2, 3)
    cp1.assign(ur1)

    print("federationResouce: ", federationResouce)
