import utils as utl
import rwm
from sklearn.neighbors import NearestNeighbors
np = utl.np
plt = utl.plt
math = utl.math
from sklearn import datasets
import doctest 

"""
input: 
output: 
"""
class Tree:
  total_leaves = 0
  total_cut = 1
  BAD_CUT_TOLERANCE = 3
  MAX_POINT_IN_BOUND = 20

  '''
  ==================================================
  [64, 32, 16, 8]
  '''
  MAX_LEAVES = 8

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
    self.grounded_nodes = None

    if parent is None:
      self.level = 0
    else:
      self.level = parent.level + 1


  # split current node into two property cluster by method
  @utl.log_msg
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

    if 2 ** (self.level) >= Tree.MAX_LEAVES:
      self.grounded = True
      Tree.total_leaves += 1
      print("[> MAX_LEAVES] set grounded: {}".format(self))
      return

    if self.bad_cut >= Tree.BAD_CUT_TOLERANCE:
      node = self
      for i in range(Tree.BAD_CUT_TOLERANCE):
        node = node.parent
        node.left.active = False
        node.right.active = False
        print("set false: {}, {}".format(node.left, node.right))
      node.grounded = True
      Tree.total_leaves += 1
      print("set grounded: {}".format(node))
      return

    if self.size < 30:
      self.grounded = True
      Tree.total_leaves += 1
      print("[node.size < 30] set grounded: {}".format(self))
      return


    if method == 'rwm':
      clusterL, clusterR, in_boundary, coeff = rwm.rwm_cut(self.datapoints)
      cluster_size_L = len(clusterL)
      cluster_size_R = len(clusterR)
      bound_size_L = len(in_boundary[0])
      bound_size_R = len(in_boundary[1])
      bound_size = bound_size_L + bound_size_R

      # create node by split result
      self.right = Tree(self, clusterR)
      self.right.size = cluster_size_R
      self.left = Tree(self, clusterL)
      self.left.size = cluster_size_L
      
      print("[FUCK] bound_size_L = {}, cluster_size_L = {}, rate = {}".format(bound_size_L, cluster_size_L, bound_size_L / cluster_size_L))
      print("[FUCK] bound_size_R = {}, cluster_size_R = {}, rate = {}".format(bound_size_R, cluster_size_R, bound_size_R / cluster_size_R))
      '''
      ==================================================
      0.5 and/or 0.5 [64: b/1, 32: b/1, 16: n/1, 8: g/n]
      0.3 and/or 0.3 [64: , 32: , 16: , 8: ]
      0.1 and/or 0.1 [64: , 32: , 16: , 8: ]
      '''
      if (bound_size_L / cluster_size_L) > 0.3 and (bound_size_R / cluster_size_R) > 0.3:
        self.left.bad_cut = self.bad_cut + 1
        self.right.bad_cut = self.bad_cut + 1
        print("cut id ", Tree.total_cut, " is bad cut")
        self.left.in_bound_record.append((Tree.total_cut, 'L', in_boundary[0]))
        self.right.in_bound_record.append((Tree.total_cut, 'R', in_boundary[1]))

      if self.in_bound_record:
        print("self.in_bound_record = ", len(self.in_bound_record))
        print("node addr = ", self)
      for bound_rec in self.in_bound_record:
        rec_cut_id = bound_rec[0]
        rec_color  = bound_rec[1]
        rec_points = bound_rec[2]
        b_left, b_right = rwm.cut_by_coeff(rec_points, coeff)

        if b_left.shape[0]:
          self.left.in_bound_record.append((rec_cut_id, rec_color, b_left))
        if b_right.shape[0]:
          self.right.in_bound_record.append((rec_cut_id, rec_color, b_right))
        print("cur cid = {}, rec_cut_id = {}".format(Tree.total_cut, rec_cut_id))

      print("after split, child.bad_cut = {}".format(self.left.bad_cut))
      Tree.total_cut += 1

    return


  def find_merge_candidate(root):
    if not root.grounded_nodes:
      set_grounded_node(root)

    candidates = []
    grounded_nodes = root.grounded_nodes

    for node in grounded_nodes:
      if node.in_bound_record:
        candidates.append(node)

    return candidates


  def set_grounded_node(root):
    grounded_nodes = []

    def _get_grounded(node, gnodes):
      if node is None:
        return
      if node.grounded:
        gnodes.append(node)
        return
      _get_grounded(node.left, gnodes)
      _get_grounded(node.right, gnodes)

    _get_grounded(root, grounded_nodes)

    if not root.grounded_nodes:
      root.grounded_nodes = grounded_nodes

    return grounded_nodes


  def is_close_enough(cur_points, other_points):
    cur_rep = np.mean(cur_points, axis=0)
    other_rep = np.mean(other_points, axis=0)
    '''
    ==================================================
    [10, 5, 3, 2.5, 2]
    '''
    # cur_size = len(cur_points)
    # other_size = len(other_points)
    threshold = utl.euclideanDistance(cur_rep, other_rep) / 3
    min_dist, min_point = Tree._two_cluster_min_dist(cur_points, other_points)

    print("threshold = {}, min_dist = {}".format(threshold, min_dist))

    # plt.clf()
    #
    # plt.plot(cur_points[:, 0], cur_points[:, 1], 'ko')
    # plt.plot(other_points[:, 0], other_points[:, 1], 'k+')
    #
    # plt.plot(cur_rep[0], cur_rep[1], 'ro')
    # plt.plot(other_rep[0], other_rep[1], 'g+')
    #
    # plt.plot(min_point[0][0], min_point[0][1], 'bo')
    # plt.plot(min_point[1][0], min_point[1][1], 'yo')
    #
    # plt.axes().set_aspect('equal', 'datalim')
    # # plt.axis([0, 500, 0, 500])
    # plt.show()

    '''
    ==================================================
    [10, 5, 0]
    '''
    if min_dist <= (threshold+5):
      # plt.show()
      return True
    # else:
    #   plt.clf()
    #
    #   plt.plot(cur_points[:, 0], cur_points[:, 1], 'ko')
    #   plt.plot(other_points[:, 0], other_points[:, 1], 'k+')
    #
    #   plt.plot(cur_rep[0], cur_rep[1], 'ro')
    #   plt.plot(other_rep[0], other_rep[1], 'g+')
    #
    #   plt.plot(min_point[0][0], min_point[0][1], 'bo')
    #   plt.plot(min_point[1][0], min_point[1][1], 'yo')
    #
    #   plt.axes().set_aspect('equal', 'datalim')
    #   # plt.axis([0, 500, 0, 500])
    #   plt.show()

    return False
    # return True


  def _two_cluster_min_dist(cur_points, other_points):
    '''
    >>> cur_points = np.array([ (1, 1), (2, 4), (6, 2), (3, -1) ])
    >>> other_points = np.array([ (3, 2), (6, 1), (1, -3), (5.5, -2.5) ])
    >>> Tree._two_cluster_min_dist(cur_points, other_points)
    (1.0, [array([6, 2]), array([ 6.,  1.])])
    '''
    min_dist = utl.euclideanDistance(cur_points[0], other_points[0])
    min_point = [ cur_points[0], other_points[0] ]

    for cp in cur_points:
      for op in other_points:
        # tmp_dist = ( (cp[0] - op[0]) ** 2 + (cp[1] - op[1]) ** 2 ) ** 0.5
        tmp_dist = utl.euclideanDistance(cp, op)
        if tmp_dist < min_dist:
          # print("tmp_dist = {}, min_dist = {}".format(tmp_dist, min_dist))
          min_dist = tmp_dist
          min_point = [cp, op]
          #
          # plt.clf()
          # plt.plot(cur_points[:, 0], cur_points[:, 1], 'ko')
          # plt.plot(other_points[:, 0], other_points[:, 1], 'k+')
          # plt.plot(min_point[0][0], min_point[0][1], 'bo')
          # plt.plot(min_point[1][0], min_point[1][1], 'yo')
          # plt.show()

    return min_dist, min_point


  # [problem] less to consider dist between candidate node
  @utl.log_msg
  def merge(root):
    if not root.grounded_nodes:
      root.set_grounded_node()

    grounded_nodes = root.grounded_nodes[:]
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
        no_merge_occour = True

        for other_node in grounded_nodes[1:]:
          need_merge = False
          other_recs = other_node.in_bound_record

          if not other_node.active:
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
                  gdatas = [node.datapoints for node in grounded_nodes]
                  repaint(gdatas)
                  if Tree.is_close_enough(cur_points, other_points):
                    print("{} and {} is close".format(cur_node, other_node))
                    need_merge = True
          if need_merge:
            cur_node.datapoints = np.append(cur_node.datapoints, other_node.datapoints, axis=0)
            cur_node.in_bound_record.extend(other_recs)
            other_node.active = False
            no_merge_occour = False
        if no_merge_occour:
          grounded_nodes.pop(0)
          final_clusters.append(cur_node)

    return final_clusters


def _build_split_tree(node, method):
  if node is None:
    print("return: node is None")
    return
  if not node.active:
    return

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

  # print('    ' * deep, current_node.grounded)
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


def repaint(grounded_nodes):
  plt.clf()
  for gnode in grounded_nodes:
    plt.scatter(gnode[:, 0], gnode[:, 1], color=(0, 0, 0))

  return


def check_bound_rec(grounded_nodes, merge_candidates):
  # check place of merge_candidates
  repaint(grounded_nodes)
  for mnode in merge_candidates:
    plt.scatter(mnode.datapoints[:, 0], mnode.datapoints[:, 1], color=np.random.rand(3))
  plt.show()

  # check the bound_rec in each node
  for mnode in merge_candidates:
    repaint(grounded_nodes)
    plt.scatter(mnode.datapoints[:, 0], mnode.datapoints[:, 1], color=(0, 1, 0))
    for bound_rec in mnode.in_bound_record:
      clr=np.random.rand(3)
      points = bound_rec[2]
      plt.scatter(points[:, 0], points[:, 1], color=(1, 0, 0))
    plt.show()
      # plt.scatter(points[:, 0], points[:, 1], color=(0, 0, 0))

  return


if __name__ == '__main__':
  doctest.testmod()

  points, label = utl.read_from_text('2d5c_cov')
  # seleted = datasets.load_digits()                                                                                                   
  # points = seleted.data                                                       
  # label = seleted.target
  #
  ms_tree = ms2c(points)
  # paint_tree(ms_tree, ms_tree)

  final_nodes = ms_tree.merge()
  grounded_nodes = ms_tree.grounded_nodes
  grounded_cls = [x.datapoints for x in grounded_nodes]
  final_cls = [x.datapoints for x in final_nodes]

  merge_num = sum( x.shape[0] for x in final_cls )
  split_num = sum( x.datapoints.shape[0] for x in grounded_nodes )

  print("\norigin #points = {}".format(points.shape[0]))
  print("split #points = {}".format(split_num))
  print("merge #points = {}\n".format(merge_num))

  print("grounded_nodes len = ", len(grounded_nodes))
  print("total leaves = ", ms_tree.total_leaves)
  print("final_nodes len = ", len(final_nodes))

  utl.draw_clusters(grounded_cls)
  ms_cands = ms_tree.find_merge_candidate()
  check_bound_rec(grounded_cls, ms_cands)
  utl.draw_clusters(final_cls)


  # ms_tree = ms2c(points)
  # # paint_tree(ms_tree, ms_tree)
  #
  # grounded_list = []
  # Tree.get_grounded_node(ms_tree, grounded_list)
  # ms_cands = Tree.find_merge_candidate(grounded_list)
  #
  # print("\n#grounded = ", len(grounded_list))
  # for g in grounded_list:
  #   print(g, " , level = ", g.level)
  # gnodes = [node.datapoints for node in grounded_list]
  # gnode_bounds = [node.in_bound_record for node in grounded_list if node.in_bound_record]
  #
  #
  # # check_bound_rec(gnodes, ms_cands)
  #
  # i = 0
  # for node in gnode_bounds:
  #   print("node", i)
  #   for rec in node:
  #     print("   cid = {}, side = {}".format(rec[0], rec[1]))
  #     print("   #points = ", len(rec[2]))
  #   i += 1
  #
  # print("\n#m_candidates = ", len(ms_cands))
  # for c in ms_cands:
  #   print(c, " , level = ", c.level, ", #bound_rec = ", len(c.in_bound_record))
  #
  # utl.draw_clusters(gnodes)
  #
  # mnodes = [node.datapoints for node in ms_cands]
  # # repaint(gnodes)
  # # utl.draw_clusters(mnodes)
  #
  #
  #
  #
  # """
  # ======================================================================
  # """
  # # repaint(gnodes)
  #
  # final_node = Tree.merge(grounded_list)
  # final_cls = [x.datapoints for x in final_node]
  #
  # # repaint(gnodes)
  # print("#final_cls = ", len(final_cls))
  # utl.draw_clusters(final_cls)

