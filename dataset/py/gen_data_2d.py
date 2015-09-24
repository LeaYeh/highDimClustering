import os.path
import numpy as np
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt



mean = [[100, 100], 
        [-40, -40]]
cov = [[[50, 0], 
        [0, 50]], 
        [[100, 0],
        [0, 100]]]
x,y = np.random.multivariate_normal(mean[0], cov[0], 500).T
plt.plot(x, y, 'x');
x,y = np.random.multivariate_normal(mean[1], cov[1], 500).T
plt.plot(x, y, 'x');
 
plt.axis('equal');
plt.show();
#plt.savefig(os.path.abspath('data_2d2c_1000'));
