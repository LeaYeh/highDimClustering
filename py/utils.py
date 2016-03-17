import random
import numpy as np
from sklearn.datasets import make_gaussian_quantiles
import matplotlib
matplotlib.use("Qt4Agg")
import matplotlib.pyplot as plt
from pprint import pprint
import matplotlib.cm as cmx
import matplotlib.colors as colors
import time                                                                                                                                           
import math
import operator


def standardize_data(datasets):
  size = len(datasets)
  center = np.mean(datasets, axis=0)
  print(center)

  return datasets - center


def stats_accuracy(y_pred, y_true):
  n = len(y_pred)
  tp = 0

  for i in range(n):
    if y_pred[i] is y_true[i]:
      tp += 1

  return tp / n


def euclideanDistance(instance1, instance2):
  dim = len(instance1)
  distance = 0


  for x in range(dim):
    distance += pow((instance1[x] - instance2[x]), 2)

  return math.sqrt(distance)


def getKthNeighbor(point, datasets, k):
  distances = []

  for i in range(len(datasets)):
    dist = euclideanDistance(point, datasets[i])
    distances.append((datasets[i], dist))

  distances.sort(key=operator.itemgetter(1))

  # output kth point and distance
  return distances[k]


def log_msg(func):                                                              
  def with_logging(*arg, **kwargs):                                             
    print(func.__name__ + "...", end="", flush=True)                            
    t0 = time.time()                                                            
    res = func(*arg, **kwargs)                                                  
    t1 = time.time()                                                            
    print("done  %.2g sec" % (t1 - t0))                                         
                                                                                
    return res                                                                  
                                                                                
  return with_logging


def gaussian_data_generator(dim=2, cls=5, objs_size=None, cov=None):

  """
  init necessary parameters
  """
  if cov is None:
    cov = [random.randrange(100, 500, 50) for _ in range(cls)]

  if objs_size is None:
    # random each cluster size; min=100, max=1000
    objs_size = [random.randrange(100, 1000, 50) for _ in range(cls)]
    # print("random object size = ", objs_size)

  means = [[random.randrange(0, 500, 50) for __ in range(dim)] for _ in range(cls)] 
  # print("object's mean = ", means)

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


def graph(coeff, x_range):
  x = np.array(x_range)
  y = (-coeff[0] * x - coeff[2]) / coeff[1]
  plt.plot(x, y, 'ro')

  return


def draw_2cluster(cluster1, cluster2):
  plt.clf()
  plt.plot(cluster1[:, 0], cluster1[:, 1], 'ro');
  plt.plot(cluster2[:, 0], cluster2[:, 1], 'bx');
  plt.show()
def read_from_text(name):
  return np.loadtxt("dataset_text/" + name, delimiter=',')


def write_to_text(name, points, label):
  data = np.append(points, label.reshape(len(label), 1), axis=1)
  np.savetxt("dataset_text/" + name, data, fmt='%10.2f', delimiter=' ')

  return


if __name__ == '__main__':
  points, label = gaussian_data_generator(objs_size=[5, 5, 5], cls=3)
  print(points)
  print(standardize_data(points))

  for i in np.unique(label):
    fetch_cluster = points[label == i]
    plt.scatter(fetch_cluster[:, 0], fetch_cluster[:, 1], color=np.random.rand(3));


  plt.show()
