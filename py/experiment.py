import utils as utl
from sklearn import (manifold, datasets)
from time import time
import matplotlib
matplotlib.use("Qt4Agg")
import matplotlib.pyplot as plt
import numpy as np
import merge_split as clustering
# import utils as utl

def data_seletor(dataset_name):
  if dataset_name == 'hand_write_digits':
    '''
    Classes                         10
    Samples per class             ~180
    Samples total                 1797
    Dimensionality                  64
    Features             integers 0-16
    '''
    seleted = datasets.load_digits(n_class=5)
    points = seleted.data
    label = seleted.target

  elif dataset_name == '5d5c':
    '''
    Classes                          5
    Samples per class                ?
    Samples total                    ?
    Dimensionality                  25
    '''
    points, label = utl.read_from_text('5d5c_std')

  elif dataset_name == "letter-recognition":
    points, label = utl.read_from_text('letter-recognition')

  elif dataset_name == "image_seg":
    points, label = utl.read_from_text('imgseg')

  elif dataset_name == '20d6c':
    points, label = utl.read_from_text('20d6c_std')

  elif dataset_name == '50d6c':
    points, label = utl.read_from_text('50d6c_std')

  return points, label


def plot_embedding(datapoints, label, title=None):
  # just normlize data
  x_min, x_max = np.min(datapoints, 0), np.max(datapoints, 0)
  datapoints = (datapoints - x_min) / (x_max - x_min)

  plt.figure()
  for i in range(datapoints.shape[0]):
    plt.text(datapoints[i, 0], datapoints[i, 1], int(label[i]),
            color=plt.cm.Set1(label[i] / 20),
            fontdict={'weight': 'bold', 'size': 9})

  plt.xticks([]), plt.yticks([])

  if title is not None:
    plt.title(title)


if __name__ == '__main__':

  # orig_points, orig_label = data_seletor('hand_write_digits')
  # orig_points, orig_label = data_seletor('image_seg')
  orig_points, orig_label = data_seletor('letter-recognition')
  # orig_points, orig_label = data_seletor('50d6c')
  # orig_points, orig_label = utl.read_from_text('20d6c_cov')
  # orig_points, orig_label = utl.read_from_text('200d5c_cov')
  # orig_points, orig_label = utl.read_from_text('100d8c_cov')
  #----------------------------------------------------------------------
  # t-SNE embedding of the digits dataset
  t0 = time()
  ms_tree = clustering.ms2c(orig_points)
  final_nodes = ms_tree.merge()
  my_time = time() - t0
  grounded_nodes = ms_tree.grounded_nodes
  final_cls = [x.datapoints for x in final_nodes]
  ground_cls = [x.datapoints for x in grounded_nodes]
  # utl.draw_clusters(final_cls)
  print(len(ground_cls))
  print(len(final_nodes))

  for label_id, cluster in enumerate(final_cls, 0):
    size = len(cluster)
    label = np.empty(size)
    label.fill(label_id)

    try:
      data
    except NameError:
      data = cluster
    else:
      data = np.append(data, cluster, axis=0)

    try:
      labels
    except NameError:
      labels = label
    else:
      labels = np.append(labels, label, axis=0)

  print("type(datapoints) = {}, type(data) = {}, type(labels) = {}".format(type(orig_points), type(data), type(labels)))
  print("shape(datapoints) = {}, shape(data) = {}, shape(labels) = {}".format(orig_points.shape, data.shape, labels.shape))

  print("strat calc tsne...")
  t0 = time()
  tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
  cls_data = tsne.fit_transform(data)
  tsne_time = time() - t0
  plot_embedding(cls_data,
                labels,
                "after clustering (my time = {}, tsne time = {})".format(my_time, tsne_time))
  plt.show()

  orig_data = tsne.fit_transform(orig_points)
  plot_embedding(orig_data,
                orig_label,
                "origin date & label")
  plt.show()


