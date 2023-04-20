import numpy as np

def MergeFederations(self, FederationsStructure, checkedMergeFed, V_CheckProfit):
    if len(FederationsStructure) < 2:
        return FederationsStructure, checkedMergeFed, V_CheckProfit

    i = np.random.randint(0, len(FederationsStructure) - 1)
    j = np.random.randint(0, len(FederationsStructure) - 1)
    while i == j:
        j = np.random.randint(0, len(FederationsStructure) - 1)

    f1 = FederationsStructure[i]
    f2 = FederationsStructure[j]

    




# merge = True

# while merge is True:
#     fed1 = np.random.randint(federations)
#     fed2 = np.random.randint(federations)
#     while fed1 == fed2:
#         fed2 = np.random.randint(federations)
