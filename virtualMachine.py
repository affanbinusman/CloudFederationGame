class virtualMachine():
    def __init__(self, size, core, memory, price):
        self.size = size
        self.core = core
        self.memory = memory
        self.price = price
        self.cloudProvider = None
        