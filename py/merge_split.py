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

      # create node by split result
      self.right = Tree(self, cluster1)
      self.right.size = len(cluster1)
      self.left = Tree(self, cluster2)
      self.left.size = len(cluster2)

      print("cid = ", Tree.total_cut, ", bound_size = ", bound_size, "self.size/6 = ", self.size // 5)
      if bound_size >= (self.size // 5):
        self.left.bad_cut = self.bad_cut + 1
        self.right.bad_cut = self.bad_cut + 1
        print("cut id ", Tree.total_cut, " is bad cut")
        self.left.in_bound_record.append((Tree.total_cut, '-', in_boundary[0]))
        self.right.in_bound_record.append((Tree.total_cut, '+', in_boundary[1]))

      if self.in_bound_record:
        print("self.in_bound_record = ", len(self.in_bound_record))
        print("node addr = ", self)
      for bound_rec in self.in_bound_record:
        rec_cut_id = bound_rec[0]
        rec_color  = bound_rec[1]
        rec_points = bound_rec[2]
        b_left, b_right = rwm.cut_by_coeff(rec_points, coeff)
        self.left.in_bound_record.append((rec_cut_id, rec_color, b_left))
        self.right.in_bound_record.append((rec_cut_id, rec_color, b_right))
        print("cur cid = {}, rec_cut_id = {}".format(Tree.total_cut, rec_cut_id))


      print("after split, child.bad_cut = {}".format(self.left.bad_cut))
      Tree.total_cut += 1

    return


  def _is_all_leves_grounded():
    return


  def find_merge_candidate(root, grounded_list):
    candidates = []

    for node in grounded_list:
      if node.in_bound_record:
        candidates.append(node)

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
      cur_node = grounded_nodes[0]
      cur_recs = cur_node.in_bound_record

      if not cur_node.active:
        grounded_nodes.pop(0)
        continue
      if not cur_recs:
        grounded_nodes.pop(0)
        final_clusters.append(cur_node)
      else:
        other_size = len(grounded_nodes[1:])
        other_nonactive = 0

        for other_node in grounded_nodes[1:]:
          need_merge = False
          other_recs = other_node.in_bound_record

          if not other_node.active:
            other_nonactive += 1
            continue
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
            # print("\n\n================ before\n", cur_node.datapoints, "\n-----------\n", other_node.datapoints)
            cur_node.datapoints = np.append(cur_node.datapoints, other_node.datapoints, axis=0)
            # print("================after\n", cur_node.datapoints)
            cur_node.in_bound_record.extend(other_recs)
            other_node.active = False
          else:
            grounded_nodes.pop(0)
            final_clusters.append(cur_node)
        if other_nonactive == other_size:
          grounded_nodes.pop(0)
          final_clusters.append(cur_node)

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
  if (current_node.left and current_node.right) is None:
    return 
  # if current_node.grounded:
  #   return
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
  # paint_tree(ms_tree, ms_tree)

  grounded_list = []
  Tree.get_grounded_node(ms_tree, grounded_list)

  ms_cands = Tree.find_merge_candidate(ms_tree, grounded_list)


  print("\n#grounded = ", len(grounded_list))
  for g in grounded_list:
    print(g, " , level = ", g.level)
  gnodes = [node.datapoints for node in grounded_list]
  gnode_bounds = [node.in_bound_record for node in grounded_list if node.in_bound_record]

  i = 0
  for node in gnode_bounds:
    print("node", i)
    for rec in node:
      print("   cid = {}, side = {}".format(rec[0], rec[1]))
    i += 1

  print("\n#m_candidates = ", len(ms_cands))
  for c in ms_cands:
    print(c, " , level = ", c.level)


  # for g in grounded_list:
  #   print("g node: ", g.in_bound_record)
  #


  # utl.draw_clusters(gnodes)

  mnodes = [node.datapoints for node in ms_cands]
  # print("mnodes = \n", mnodes)

  final_node = Tree.merge(grounded_list)
  final_cls = [x.datapoints for x in final_node]

  # for node in final_node:
  #   print(node)

  print("#final_cls = ", len(final_cls))
  utl.draw_clusters(final_cls)

  # print("\n\n============================")
  # for node in grounded_list:
    # print("cut_id = {}, ")

