import utils as utl
import rwm
from sklearn.neighbors import NearestNeighbors
np = utl.np
plt = utl.plt
math = utl.math


"""
input: 
output: 
"""
class Tree:
  BAD_CUT_TOLERANCE = 3

  def __init__(self, parent, datapoints):
    self.datapoints = datapoints
    self.size = len(datapoints)
    self.dim = len(datapoints[0])
    self.left = None
    self.right = None
    self.parent = parent
    self.bad_cut = 0

    # set up level to switch method
    if parent is None:
      self.level = 0
    else:
      self.level = parent.level + 1
    
  # split current node into two property cluster by method
  def split(self, method):
    if method not in ["rwm", "tcf"]:
      msg = "'method' must be 'rwm' or 'tcf'"
      raise ValueError(msg)

    if method == 'rwm':
      cluster1, cluster2 = rwm.rwm_cut(self.datapoints)

    # create node by split result
    self.left = Tree(self, cluster1)
    self.right = Tree(self, cluster2)

    # get each cluster size
    self.left.size  = len(cluster1)
    self.right.size = len(cluster2)

    m1 = np.mean(cluster1, axis=0)
    m2 = np.mean(cluster2, axis=0)

    # get Kth dist as standard deviation
    kth_p1, s1 = utl.getKthNeighbor(m1, cluster1, 7)
    kth_p2, s2 = utl.getKthNeighbor(m2, cluster2, 7)

    v1 = s1 ** self.dim
    v2 = s2 ** self.dim

    # do `z-test`, to test two clusters whether have enough differential
    # intersection test from mean vector, if any test faild, z-test faild
    # z = (m1 - m2) / math.sqrt(v1 / size1 + v2 / size2)
    # z >= 2.58 means two cluster are very different
    # z >= 1.96 means two cluster are quite different
    for i, j in zip(m1, m2):
      z = (i - j) / math.sqrt(v1 / self.left.size + v2 / self.right.size)
      print("|z| = ", abs(z))
      if abs(z) < 1.96:
        self.left.bad_cut = self.bad_cut + 1
        self.right.bad_cut = self.bad_cut + 1
        print("split result bad_cut = ", self.left.bad_cut)
        break

    return

  # 
  def merge():
    return


def _ms2c(node, method):
  print("level = ", node.level)
  print("[bad]: ", node.bad_cut)
  # return condition:
  #   current node's bad cut times > BAD_CUT_TOLERANCE
  #                  size < 30 (Central Limit Theorem)
  if node.bad_cut >= node.BAD_CUT_TOLERANCE:
    print("return: bad cut")
    return
  if node.size < 30:
    print("return: 30")
    return

  # split current node
  # if n not define means use only one method to split
  if _ms2c.n == None:
    node.split(method)
  elif node.level < _ms2c.n:
    node.split(method[0])
  else:
    node.split(method[1])

  _ms2c(node.left, method)
  _ms2c(node.right, method)

  return


def paint_tree(root_node):
  dim = len(root_node.datapoints[0])

  if dim != 2:
    msg = "datapoints' dimension is not porperty, only can handle 2 dimension data."
    raise ValueError(msg)

  
  
  return


"""
method:
  a, a
  b, b
  a, b
  b, a
"""
def ms2c(datapoints, method='rwm', n=None):
  _ms2c.n = n
  root = Tree(None, datapoints)
  
  _ms2c(root, method)

  return


if __name__ == '__main__':
  points, label = utl.gaussian_data_generator(dim=40, objs_size=[100, 100], cls=2)

  print(len(points[0]))
  ms2c(points)




