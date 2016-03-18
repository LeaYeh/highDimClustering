import utils as utl
import rwm
from sklearn.neighbors import NearestNeighbors
np = utl.np
plt = utl.plt
math = utl.math


def get_clusters(node, clusters):
  if node.left is None or node.right is None:
    clusters.append(node.datapoints)
    return

  get_clusters(node.left, clusters)
  get_clusters(node.right, clusters)

  return


"""
input: 
output: 
"""
class Tree:
  total_leaves = 0
  total_cut = 1
  BAD_CUT_TOLERANCE = 3
  MAX_POINT_IN_BOUND = 20
  MAX_LEAVES = 64

  def __init__(self, parent, datapoints):
    self.datapoints = datapoints
    self.size = len(datapoints)
    self.dim = len(datapoints[0])
    self.left = None
    self.right = None
    self.parent = parent
    self.bad_cut = 0
    self.grounded = False
    self.active = True
    self.bad_cut_record = None

    if parent is None:
      self.level = 0
    else:
      self.level = parent.level + 1


  # split current node into two property cluster by method
  def split(self, method):
    if method not in ["rwm", "tcf"]:
      msg = "'method' must be 'rwm' or 'tcf'"
      raise ValueError(msg)

    if self.active is False:
      return

    # before split, check whether continue happened BAD_CUT_TOLERANCE bad cut
    # withdraw those bad cuts and mark grounded sign on first parent
    if self.bad_cut >= Tree.BAD_CUT_TOLERANCE:
      for i in range(Tree.BAD_CUT_TOLERANCE):
        node = self.parent
        node.left.active = False
        node.right.active = False
      node.grounded = True
      return

    if method == 'rwm':
      cluster1, cluster2, in_boundary = rwm.rwm_cut(self.datapoints)
      bound_size = len(in_boundary[0]) + len(in_boundary[1])

      # create node by split result
      self.right = Tree(self, cluster1)
      self.right.size = len(cluster1)
      self.right.bad_cut_record = (Tree.total_cut, in_boundary[0])
      self.left = Tree(self, cluster2)
      self.left.size = len(cluster2)
      self.left.bad_cut_record = (Tree.total_cut, in_boundary[1])

      if bound_size >= (self.size // 5):
        self.left.bad_cut = self.bad_cut + 1
        self.right.bad_cut = self.bad_cut + 1

      Tree.total_cut += 1

      print("total size = ", self.size, "bound_size/MAX_POINT_IN_BOUND = {} / {}".format(bound_size, (self.size // 5)))
      print('bad_cut = ', self.left.bad_cut)

    return

  # 
  def merge():
    return


def _build_split_tree(node, method):
  if node is None:
    return
  # if Tree.total_leaves >= Tree.MAX_LEAVES:
  #   return
  if node.size < 30:
    return

  # split current node
  # if n not define means use only one method to split
  if _build_split_tree.n == None:
    node.split(method)
  elif node.level < _build_split_tree.n:
    node.split(method[0])
  else:
    node.split(method[1])

  _build_split_tree(node.left, method)
  _build_split_tree(node.right, method)

  return


def paint_tree(current_node, root_node):
  dim = len(root_node.datapoints[0])

  if dim != 2:
    msg = "datapoints' dimension is not porperty, only can handle 2 dimension data."
    raise ValueError(msg)
  if root_node is None:
    mag = "this tree is empty."
    raise ValueError(msg)

  if current_node.left is None:
    return 
  if current_node.grounded:
    print("grounded")
    return
  # if current_node.active is False:
  #   return

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
  _build_split_tree.n = n
  root = Tree(None, datapoints)
  
  _build_split_tree(root, method)

  return root


if __name__ == '__main__':
  points, label = utl.read_from_text('2d5c_std')

  ms_tree = ms2c(points)
  paint_tree(ms_tree, ms_tree)




