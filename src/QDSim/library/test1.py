import numpy as np

size = 10
# create an numpy tensor of size 10x10 initialized to zeros except the main diagonal which is 1
a = np.eye(size)

# add a little gausian noise to the tensor
a += np.around(abs(np.random.normal(0, 0.1, (size, size))), decimals=2)

# save the tensor to a file
np.savetxt('test1.txt', a)
