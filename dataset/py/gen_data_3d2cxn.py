import os.path
import numpy as np
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

mean = [(30, 30, 30),
        (-50, -50, -50)]

cov  = [
    [(100, 0, 0),
     (0, 100, 0),
     (0, 0, 100)],

    [(25, 0, 0),
     (0, 25, 0),
     (0, 0, 25)]
]


# plt.plot(x, y, z, 'x');
#
# plt.axis('equal');
# plt.show();
#plt.savefig(os.path.abspath('data_3d1c_1000'));

fig = plt.figure()
ax = plt.axes(projection='3d')

x, y, z = np.random.multivariate_normal(mean[0], cov[0], 500).T
ax.scatter(x, y, z)
with open('data_3d2cxn.txt', 'w') as f:
  for i,j,k in zip(x, y, z):
    f.write('{:>15} {:>15} {:>15}\n'.format(i, j, k))

x, y, z = np.random.multivariate_normal(mean[1], cov[1], 500).T
ax.scatter(x, y, z)
with open('data_3d2cxn.txt', 'a') as f:
  for i,j,k in zip(x, y, z):
    f.write('{:>15} {:>15} {:>15}\n'.format(i, j, k))

plt.savefig(os.path.abspath('data_3d2cxn_1000'));
plt.show()
