

class cloudProvider:
    def __init__(self, name, availableCores, availableMemory, availableStorage, costList):
        self.name = name
        self.availableCores = availableCores
        self.availableMemory = availableMemory
        self.availableStorage = availableStorage
        self.costList = costList

    # def assign(self, userRequest):
    #     if self.availableCores == 0 or self.availableMemory == 0 or self.availableStorage == 0:
    #         print("Request Denied: Insufficient Resoucres")
    #         return -1

    #     if self.availableMemory < userRequest.small:
    #         pass
            
        # return 0
            


        

