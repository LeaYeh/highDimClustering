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
    self.in_bound_record = []

    if parent is None:
      self.level = 0
    else:
      self.level = parent.level + 1


  # split current node into two property cluster by method
  def split(self, method):
    print("in split func")

    if method not in ["rwm", "tcf"]:
      msg = "'method' must be 'rwm' or 'tcf'"
      raise ValueError(msg)

    if self.active is False:
      return

    # before split, check whether continue happened BAD_CUT_TOLERANCE bad cut
    # withdraw those bad cuts and mark grounded sign on first parent
    print("self node = {}".format(self))
    print("self.bad_cut = {}, self.level = {}".format(self.bad_cut, self.level))

    if self.bad_cut >= Tree.BAD_CUT_TOLERANCE:
      node = self
      for i in range(Tree.BAD_CUT_TOLERANCE):
        node = node.parent
        node.left.active = False
        node.right.active = False
        print("set false: {}, {}".format(node.left, node.right))
      node.grounded = True
      print("set grounded: {}".format(node))
      return

    if self.size < 30:
      self.grounded = True
      print("[node.size < 30] set grounded: {}".format(self))
      return


    if method == 'rwm':
      cluster1, cluster2, in_boundary, coeff = rwm.rwm_cut(self.datapoints)
      bound_size = len(in_boundary[0]) + len(in_boundary[1])
      # if self.in_bound_record:
      #   rec_cut_id = self.in_bound_record[0]
      #   rec_points = self.in_bound_record[1]
      #   rec_color  = self.in_bound_record[2]
      #   b_left, b_right = rwm.cut_by_coeff(rec_points, coeff)
      #   self.left.in_bound_record.append((rec_cut_id, b_left, rec_color))
      #   self.right.in_bound_record.append((rec_cut_id, b_right, rec_color))

      # create node by split result
      self.right = Tree(self, cluster1)
      self.right.size = len(cluster1)
      self.left = Tree(self, cluster2)
      self.left.size = len(cluster2)

      # if bound_size > 0:
      #   self.right.in_bound_record.append((Tree.total_cut, in_boundary[0], '+'))
      #   self.left.in_bound_record.append((Tree.total_cut, in_boundary[1], '-'))

      if bound_size >= (self.size // 5):
        self.left.bad_cut = self.bad_cut + 1
        self.right.bad_cut = self.bad_cut + 1

      print("after split, child.bad_cut = {}".format(self.left.bad_cut))
      Tree.total_cut += 1

    return


  def find_merge_candidate(root):
    candidates = []
    def _get_cands(node, candidates):
      if node is None:
        return
      if node.in_bound_record and node.grounded and node.active:
        print("node.parent = {}, #in_bound_points = {}".format(node.parent, node.in_bound_record[0]))
        candidates.append(node)
        return
      _get_cands(node.left, candidates)
      _get_cands(node.right, candidates)

    _get_cands(root, candidates)

    return candidates


  def get_grounded_node(node, grounded_nodes):
    if node is None:
      return
    if node.grounded:
      grounded_nodes.append(node)
      return
    Tree.get_grounded_node(node.left, grounded_nodes)
    Tree.get_grounded_node(node.right, grounded_nodes)


  # [problem] less to consider dist between candidate node
  def merge(grounded_nodes):
    final_clusters = []

    while grounded_nodes:
      cur_node = grounded_nodes.pop(0)
      cur_recs = cur_node.in_bound_record


      print("cur_recs = ", cur_recs)
      if not cur_node.active:
        continue
      if not cur_recs:
        final_clusters.append(cur_node)
      else:
        for other_node in grounded_nodes:
          if not other_node.active:
            continue
          need_merge = False
          other_recs = other_node.in_bound_record
          if other_recs:
            for crec in cur_recs:
              cur_cut_id = crec[0]
              cur_color = crec[1]
              cur_points = crec[2]
              for orec in other_recs:
                other_cut_id = orec[0]
                other_color = orec[1]
                other_points = orec[2]
                if (cur_cut_id == other_cut_id) and (cur_color != other_color):
                  need_merge = True
          if need_merge:
            np.append(cur_node.datapoints, other_node.datapoints, axis=0)
            cur_node.in_bound_record.extend(other_recs)
            other_node.active = False
        final_clusters.append(cur_node)

    print("final_clusters = ", len(final_clusters))

    return final_clusters


def _build_split_tree(node, method):
  if node is None:
    print("return: node is None")
    return
  if node.active is False:
    print("return: {}, node.active is False".format(node))
    return
    
  # if Tree.total_leaves >= Tree.MAX_LEAVES:
  #   return
  # if node.size < 30:
  #   print("return: node.size < 30")
  #   return

  # split current node
  # if n not define means use only one method to split
  # if _build_split_tree.n == None:
  node.split(method)
  # elif node.level < _build_split_tree.n:
  #   node.split(method[0])
  # else:
  #   node.split(method[1])

  print("{}, node.active = {}".format(node, node.active))
  print(node.left)
  print(node.right)

  print("\ncall _build_split_tree, left")
  _build_split_tree(node.left, method)
  print("\ncall _build_split_tree, right")
  _build_split_tree(node.right, method)

  return


def paint_tree(current_node, root_node, deep=0):
  dim = len(root_node.datapoints[0])

  if dim != 2:
    msg = "datapoints' dimension is not porperty, only can handle 2 dimension data."
    raise ValueError(msg)
  if root_node is None:
    mag = "this tree is empty."
    raise ValueError(msg)

  print('    ' * deep, current_node.grounded)
  if current_node.left is None:
    return 
  if current_node.grounded:
    return
  # if current_node.active is False:
  #   return

  # paint all datapoints with color:black
  plt.plot(root_node.datapoints[:, 0], root_node.datapoints[:, 1], 'ko')
  # paint current clustering node with color:red/blue
  utl.draw_2cluster(current_node.left.datapoints, current_node.right.datapoints)
  plt.show()

  paint_tree(current_node.left, root_node, deep+1)
  paint_tree(current_node.right, root_node, deep+1)

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

  print("start build split tree\n")
  _build_split_tree(root, method)

  return root


if __name__ == '__main__':
  points, label = utl.read_from_text('2d5c_std')

  ms_tree = ms2c(points)
  paint_tree(ms_tree, ms_tree)

  grounded_list = []
  Tree.get_grounded_node(ms_tree, grounded_list)

  print("\n\n============================")
  for node in grounded_list:
    # print("cut_id = {}, ")

