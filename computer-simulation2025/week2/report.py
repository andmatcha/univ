import numpy as np

a = np.int32(25)
b = np.int32(2)
c = np.int32(30)
p = np.float32(2.0)

x = a * b * c
y = a * p * c
z = a / p * c

print("x={}, データ型は{}".format(x, type(x)))
print("y={}, データ型は{}".format(y, type(y)))
print("z={}, データ型は{}".format(z, type(z)))

if x == y:
    print("x is equal to y.")
else:
    print("x is NOT equal to y.")
