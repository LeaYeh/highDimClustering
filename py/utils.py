import random
import numpy as np
from sklearn.datasets import make_gaussian_quantiles
import matplotlib
matplotlib.use("Qt4Agg")
import matplotlib.pyplot as plt
from pprint import pprint
import matplotlib.cm as cmx
import matplotlib.colors as colors


def gaussian_data_generator(dim=4, cls=5, objs_size=None, cov=None):

  """
  init necessary parameters
  """
  if cov is None:
    cov = [300 for _ in range(cls)]

  if objs_size is None:
    # random each cluster size; min=100, max=1000
    objs_size = [random.randrange(100, 1000, 50) for _ in range(cls)]

  means = [[random.randrange(0, 500, 50) for __ in range(dim)] for _ in range(cls)] 

  point = []
  label = []
  for i in range(cls):
    tmp_point, tmp_label = make_gaussian_quantiles(mean = means[i],
                                                   cov = cov[i],
                                                   n_features = dim, 
                                                   n_classes = 1, 
                                                   n_samples = objs_size[i])

    list(map(lambda x: point.append(x), tmp_point))
    list(map(lambda x: label.append(x + i), tmp_label))

  # [temp] redundant translate to np.array
  return np.array(point), np.array(label)


if __name__ == '__main__':
  point, label = gaussian_data_generator()
  pprint(point)
  p = sum(point)

  for i in np.unique(label):
    fetch_cluster = point[label == i]
    plt.scatter(fetch_cluster[:, 0], fetch_cluster[:, 1], color=np.random.rand(3));

  plt.show()





