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
    seleted = datasets.load_digits()
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
  elif dataset_name == '20d6c':
    points, label = utl.read_from_text('20d6c_std')

  return points, label


def plot_embedding(datapoints, label, title=None):
  # just normlize data
  x_min, x_max = np.min(datapoints, 0), np.max(datapoints, 0)
  datapoints = (datapoints - x_min) / (x_max - x_min)

  plt.figure()
  for i in range(datapoints.shape[0]):
    plt.text(datapoints[i, 0], datapoints[i, 1], str(label[i]),
            color=plt.cm.Set1(label[i] / 10.),
            fontdict={'weight': 'bold', 'size': 9})

  plt.xticks([]), plt.yticks([])

  if title is not None:
    plt.title(title)


if __name__ == '__main__':

  orig_points, orig_label = data_seletor('hand_write_digits')
  # orig_points, orig_label = data_seletor('20d6c')
  #----------------------------------------------------------------------
  # t-SNE embedding of the digits dataset

  ms_tree = clustering.ms2c(orig_points)
  ms_tree.set_grounded_node()
  final_nodes = ms_tree.merge()
  final_cls = [x.datapoints for x in final_nodes]

  # utl.draw_clusters(final_cls)
  print(len(final_nodes))

  for label_id, cluster in enumerate(final_cls, 1):
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

  # print("type(datapoints) = {}, type(data) = {}, type(labels) = {}".format(type(points), type(data), type(labels)))
  # print("shape(datapoints) = {}, shape(data) = {}, shape(labels) = {}".format(points.shape, data.shape, labels.shape))

  print("strat calc tsne...")
  tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
  data_tsne = tsne.fit_transform(data)
  plot_embedding(data_tsne,
                labels,
                "t-SNE embedding")
  plt.show()


