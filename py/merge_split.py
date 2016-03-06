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
  BAD_CUT_TOLERANCE = 1
  cut_count = 0

  def __init__(self, parent, datapoints):
    self.datapoints = datapoints
    self.size = len(datapoints)
    self.dim = len(datapoints[0])
    self.left = None
    self.right = None
    self.parent = parent
    self.bad_cut = 0
    self.dense = None

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

    """
    目前唯一中止條件
    """
    # if any node < 30, termination condition
    if self.left.size < 30 or self.right.size < 30:
      self.left.bad_cut = self.BAD_CUT_TOLERANCE
      self.right.bad_cut = self.BAD_CUT_TOLERANCE
      return

    m1 = np.mean(cluster1, axis=0)
    m2 = np.mean(cluster2, axis=0)


    # get Kth dist as standard deviation
    kth_p1, s1 = utl.getKthNeighbor(m1, cluster1, 7)
    kth_p2, s2 = utl.getKthNeighbor(m2, cluster2, 7)

    # v1 = s1 ** self.dim
    # v2 = s2 ** self.dim

    """
    do `z-test`, to test two clusters whether have enough differential mean,
      但是 z-rest 永遠都會過，因為 cut 完後 mean, std 都是從限制範圍內(群內)取的
      所以 mean 不可能會一樣
    intersection test from mean vector, if any test success, z-test success
    z = (m1 - m2) / math.sqrt(v1 / size1 + v2 / size2)
    z >= 2.58 means two cluster are very different
    z >= 1.96 means two cluster are quite different
    """
    # self.left.bad_cut = self.bad_cut + 1
    # self.right.bad_cut = self.bad_cut + 1
    # for i, j in zip(m1, m2):
    #   z = (i - j) / math.sqrt(v1 / self.left.size + v2 / self.right.size)
    #   # print("|z| = ", abs(z))
    #   if abs(z) >= 1.96:
    #     self.left.bad_cut = 0
    #     self.right.bad_cut = 0
    #     print("z-test success!")
    #     break

    return

  # 
  def merge():
    return


def _ms2c(node, method):
  # print("level = ", node.level)
  # print("[bad]: ", node.bad_cut)

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


def paint_tree(current_node, root_node):
  dim = len(root_node.datapoints[0])

  if dim != 2:
    msg = "datapoints' dimension is not porperty, only can handle 2 dimension data."
    raise ValueError(msg)
  if root_node is None:
    mag = "this tree is empty."
    raise ValueError(msg)

  # termination condition
  if current_node.left is None:
    return

  # paint all datapoints with color:black
  plt.plot(root_node.datapoints[:, 0], root_node.datapoints[:, 1], 'ko')
  # paint current clustering node with color:red/blue
  utl.draw_2cluster(current_node.left.datapoints, current_node.right.datapoints)
  plt.show()

  paint_tree(current_node.left, root_node)
  paint_tree(current_node.right, root_node)

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

  return root


if __name__ == '__main__':
  points, label = utl.gaussian_data_generator(dim=2, cls=5)

  # c1, c2 = rwm.rwm_cut(points)
  # utl.draw_2cluster(c1, c2)
  # print(len(points[0]))
  ms_tree = ms2c(points)
  paint_tree(ms_tree, ms_tree)




