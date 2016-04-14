import utils as utl
import rwm
from sklearn.neighbors import NearestNeighbors
np = utl.np
plt = utl.plt
math = utl.math


class Tree:
  total_cut = 1
  BAD_CUT_TOLERANCE = 3
  MAX_POINT_IN_BOUND = 20

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
  def split(self, method):
    if method not in ["rwm", "tcf"]:
      msg = "'method' must be 'rwm' or 'tcf'"
      raise ValueError(msg)

    if self.active is False:
      return

    if self.bad_cut >= Tree.BAD_CUT_TOLERANCE:
      node = self
      for i in range(Tree.BAD_CUT_TOLERANCE):
        node = node.parent
        node.left.active = False
        node.right.active = False
      node.grounded = True
      return

    if self.size < 30:
      self.grounded = True
      return

    if method == 'rwm':
      clusterL, clusterR, in_boundary, coeff = rwm.rwm_cut(self.datapoints)
      bound_size = len(in_boundary[0]) + len(in_boundary[1])

      # create node by split result
      self.right = Tree(self, clusterR)
      self.right.size = len(clusterR)
      self.left = Tree(self, clusterL)
      self.left.size = len(clusterL)

      # not a good condiction, just walkaround first
      if bound_size >= (self.size // 10):
        self.left.bad_cut = self.bad_cut + 1
        self.right.bad_cut = self.bad_cut + 1
        self.left.in_bound_record.append((Tree.total_cut, 'L', in_boundary[0]))
        self.right.in_bound_record.append((Tree.total_cut, 'R', in_boundary[1]))

      for bound_rec in self.in_bound_record:
        rec_cut_id = bound_rec[0]
        rec_color  = bound_rec[1]
        rec_points = bound_rec[2]
        b_left, b_right = rwm.cut_by_coeff(rec_points, coeff)

        if b_left.shape[0]:
          self.left.in_bound_record.append((rec_cut_id, rec_color, b_left))
        if b_right.shape[0]:
          self.right.in_bound_record.append((rec_cut_id, rec_color, b_right))

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
    threshold = utl.euclideanDistance(cur_rep, other_rep) / 10
    min_dist, min_point = Tree._two_cluster_min_dist(cur_points, other_points)

    if min_dist <= threshold:
      return True

    return False


  def _two_cluster_min_dist(cur_points, other_points):
    min_dist = utl.euclideanDistance(cur_points[0], other_points[0])

    for cp in cur_points:
      for op in other_points:
        tmp_dist = utl.euclideanDistance(cp, op)
        if tmp_dist < min_dist:
          min_dist = tmp_dist
          min_point = [cp, op]

    return min_dist, min_point


  # [problem] less to consider dist between candidate node
  def merge(root):
    if not root.grounded_nodes:
      set_grounded_node(root)

    grounded_nodes = root.grounded_nodes
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
    return
  if node.active is False:
    return
    
  node.split(method)
  _build_split_tree(node.left, method)
  _build_split_tree(node.right, method)

  return


def repaint(grounded_nodes):
  plt.clf()
  for gnode in grounded_nodes:
    plt.scatter(gnode[:, 0], gnode[:, 1], color=(0, 0, 0))

  return


def paint_tree(current_node, root_node, deep=0):
  dim = len(root_node.datapoints[0])

  if dim != 2:
    msg = "datapoints' dimension is not porperty, only can handle 2 dimension data."
    raise ValueError(msg)
  if root_node is None:
    mag = "this tree is empty."
    raise ValueError(msg)

  if (current_node.left and current_node.right) is None:
    return 
  if current_node.grounded:
    return
  if current_node.active is False:
    return

  repaint(root_node.grounded_nodes)
  # paint current clustering node with color:red/blue
  utl.draw_2cluster(current_node.left.datapoints, current_node.right.datapoints)
  plt.show()

  paint_tree(current_node.left, root_node, deep+1)
  paint_tree(current_node.right, root_node, deep+1)

  return


def ms2c(datapoints, method='rwm', n=None):
  _build_split_tree.n = n
  root = Tree(None, datapoints)

  _build_split_tree(root, method)

  return root


if __name__ == '__main__':
  points, label = utl.read_from_text('2d5c_std')

  ms_tree = ms2c(points)
  grounded_nodes = ms_tree.set_grounded_node()

  final_nodes = ms_tree.merge()
  final_cls = [x.datapoints for x in final_nodes]

  utl.draw_clusters(final_cls)


