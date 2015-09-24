import os.path
import numpy as np
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

mean = [(30, 30, 30, 30, 30, 30, 30, 30),
        (-50, -50, -50, -50, -50, -50, -50, -50)]

cov  = [
    [(100, 0, 0, 0, 0, 0, 0, 0),
     (0, 100, 0, 0, 0, 0, 0, 0),
     (0, 0, 100, 0, 0, 0, 0, 0),
     (0, 0, 0, 100, 0, 0, 0, 0),
     (0, 0, 0, 0, 100, 0, 0, 0),
     (0, 0, 0, 0, 0, 100, 0, 0),
     (0, 0, 0, 0, 0, 0, 100, 0),
     (0, 0, 0, 0, 0, 0, 0, 100),
    ],

    [(25, 0, 0, 0, 0, 0, 0, 0),
     (0, 25, 0, 0, 0, 0, 0, 0),
     (0, 0, 25, 0, 0, 0, 0, 0),
     (0, 0, 0, 25, 0, 0, 0, 0),
     (0, 0, 0, 0, 25, 0, 0, 0),
     (0, 0, 0, 0, 0, 25, 0, 0),
     (0, 0, 0, 0, 0, 0, 25, 0),
     (0, 0, 0, 0, 0, 0, 0, 25),
    ]
]

dn = np.random.multivariate_normal(mean[0], cov[0], 500).T
with open('data_8d2cxn.txt', 'w') as f:
  for row in zip(*dn):
    f.write(' '.join('{:>15}'.format(i) for i in row)+'\n')
dn = np.random.multivariate_normal(mean[1], cov[1], 500).T
with open('data_8d2cxn.txt', 'a') as f:
  for row in zip(*dn):
    f.write(' '.join('{:>15}'.format(i) for i in row)+'\n')
