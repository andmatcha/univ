import numpy as np

a = np.int64(1)

for i in range(24):
    a *= np.int64(i + 1)
    print("{}! = {}".format(i + 1, a))
