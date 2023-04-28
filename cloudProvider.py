class cloudProvider:
    def __init__(self, name, availableCores, availableMemory, availableStorage, costList):
        self.name = name
        self.availableCores = int(availableCores)
        self.availableMemory = int(availableMemory)
        self.availableStorage = int(availableStorage)
        self.costList = costList
