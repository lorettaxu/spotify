import numpy as np
from scipy import sparse
l = sparse.lil_matrix((4, 4))
l[1, 1] = 1
l[1, 3] =2
l[2, 3] = 3

import random

train_pid=random.sample(range(0,1000000),200000)
print(len(train_pid))