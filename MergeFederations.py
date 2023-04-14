import numpy as np

merge = True

while merge is True:
    fed1 = np.random.randint(federations)
    fed2 = np.random.randint(federations)
    while fed1 == fed2:
        fed2 = np.random.randint(federations)
