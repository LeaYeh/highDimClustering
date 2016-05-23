import random
import numpy as np
from numpy.random import multivariate_normal
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


#---------------------- Data pre-processing -------------------------
def standardize_data(datasets):
  size = len(datasets)
  center = np.mean(datasets, axis=0)

  return datasets - center


def gaussian_data_generator(dim=2, cls=5, objs_size=None, cov=None):

  """
  init necessary parameters
  """
  if cov is None:
    cov = [random.randrange(100, 500, 100) for _ in range(cls)]

  if objs_size is None:
    # random each cluster size; min=100, max=1000
    objs_size = [random.randrange(100, 500, 50) for _ in range(cls)]
    # print("random object size = ", objs_size)

  means = [[random.randrange(100, 200, 20) for __ in range(dim)] for _ in range(cls)] 
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
  return standardize_data(np.array(point)), np.array(label)


def normal_data_generator(dim=2, cls=5):
  point = []
  label = []

  for i in range(cls):
    mean = [random.randrange(100, 500, 50) for _ in range(dim)]
    _ = np.random.randint(1, 10, size=(dim, dim)) * 50
    cov = (_ + _.T)/2
    for r in range(dim):
      for c in range(dim):
        if r != c:
          cov[r, c] = 0
    size = random.randrange(100, 1500, 100)
    print(cov)

    tmp_point = np.random.multivariate_normal(mean, cov, size)
    list(map(lambda x: point.append(x), tmp_point))
    [label.append(i) for _ in range(len(tmp_point))]

  return standardize_data(np.array(point)), np.array(label)


def read_from_text(name):
  data = np.loadtxt("dataset_text/" + name, delimiter=' ')
  points, label = data[:, :-1], data[:, -1]

  return points, label


def write_to_text(name, points, label):
  data = np.append(points, label.reshape(len(label), 1), axis=1)
  np.savetxt("dataset_text/" + name, data, delimiter=' ')

  return

#--------------------------- Math tools -----------------------------
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
    distance += (instance1[x] - instance2[x]) ** 2

  return math.sqrt(distance)


#---------------------- Algorithm related ---------------------------
def getKthNeighbor(point, datasets, k):
  distances = []

  for i in range(len(datasets)):
    dist = euclideanDistance(point, datasets[i])
    distances.append((datasets[i], dist))

  distances.sort(key=operator.itemgetter(1))

  # output kth point and distance
  return distances[k]



#------------------------- Other tools ------------------------------
def log_msg(func):                                                              
  def with_logging(*arg, **kwargs):                                             
    print(func.__name__ + "...", end="", flush=True)                            
    t0 = time.time()                                                            
    res = func(*arg, **kwargs)                                                  
    t1 = time.time()                                                            
    print("done  %.2g sec" % (t1 - t0))                                         
                                                                                
    return res                                                                  
                                                                                
  return with_logging


def graph(coeff, x_range, mark='ro'):
  x = np.array(x_range)
  y = (-coeff[0] * x - coeff[2]) / coeff[1]
  plt.plot(x, y, mark, ms=3)

  return


def draw_2cluster(cluster1, cluster2):
  plt.plot(cluster1[:, 0], cluster1[:, 1], 'ro')
  plt.plot(cluster2[:, 0], cluster2[:, 1], 'bo')

  return


def draw_clusters(cluster_itr):
  for cls in cluster_itr:
    plt.scatter(cls[:, 0], cls[:, 1], color=np.random.rand(3));
  plt.show()

  return


def calc_accuracy_rate(true_labels, pred_labels):
  def compare_two_index_score(true_labels, pred_labels):
    correct = 0
    total = 0

    for index_combo in itertools.combinations(range(len(true_labels)), 2):
      index1 = index_combo[0]
      index2 = index_combo[1]
      same_class = (true_labels[index1] == true_labels[index2])
      same_cluster = (pred_labels[index1] == pred_labels[index2])

      if same_class and same_cluster:
        correct += 1
      elif not same_class and not same_cluster:
        correct += 1
      total += 1

    return float(correct) / total

  homo = metrics.homogeneity_score(true_labels, pred_labels)
  comlet = metrics.completeness_score(true_labels, pred_labels)
  v = metrics.v_measure_score(true_labels, pred_labels)
  ami = metrics.adjusted_mutual_info_score(true_labels, pred_labels)
  ari = metrics.adjusted_rand_score(true_labels, pred_labels)
  tis = compare_two_index_score(true_labels, pred_labels)

  print('homogeneity_score = ', homo)
  print('completeness_score = ', comlet)
  print('v_measure_score = ', v)
  print('adjusted_mutual_info_score = ', ami)
  print('adjusted_rand_score = ', ari)
  print('compare_two_index_score = ', tis)

if __name__ == '__main__':
  # points, label = gaussian_data_generator(dim=2, cls=5)
  points, label = normal_data_generator(dim=20, cls=5)

  # pprint(read_from_text('2d5c_std'))
  write_to_text('20d5c_noncycle_close', points, label)

  for i in np.unique(label):
    fetch_cluster = points[label == i]
    plt.scatter(fetch_cluster[:, 0], fetch_cluster[:, 1], color=np.random.rand(3))


  plt.show()


