import utils as utl
np = utl.np
plt = utl.plt
# import tcf as tcf
from copy import deepcopy



"""
input:  datapoints
output: a boundary/hyperplane, split two cluster
"""
def _rwm(datapoints):
  size, dim = datapoints.shape
  center = np.mean(datapoints, axis=0)

  r = np.sqrt(np.sum((datapoints - center) ** 2, axis=1))
  # r = np.sum((datapoints - center) ** 2, axis=1)
  R = sum(r)
  w = r.dot(datapoints) / R
  v = w - center
  coeff = np.append(v, sum(-v * w))

  return coeff


def cut_by_coeff(orig_datapoints, coeff):
  # each cut need to centralize and normalize
  datapoints = deepcopy(orig_datapoints)
  datapoints = utl.centralize_data(datapoints)
  datapoints = utl.normalize_data(datapoints)

  c_left = []
  c_right = []
  unit_len = sum(coeff[:-1] ** 2) ** 0.5

  for point in datapoints:
    p2b_dist = (sum(point * coeff[:-1]) + coeff[-1]) / unit_len
    if p2b_dist >= 0:
      c_right.append(point)
    else:
      c_left.append(point)
  c_left = np.array(c_left, np.float)
  c_right = np.array(c_right, np.float)

  return (c_left, c_right)


"""
input:  datapoints(numpy.ndarray)
output: two list of data in each cluster
"""
def rwm_cut(orig_datapoints, boundary_width=0.1, n=2):
  datapoints = deepcopy(orig_datapoints)
  datapoints = utl.centralize_data(datapoints)
  datapoints = utl.normalize_data(datapoints)

  in_boundary = 0
  size, dim = datapoints.shape
  c_left = []
  c_right = []

  coeff = _rwm(datapoints)

  r_bp = []
  l_bp = []

  r_nbp = []
  l_nbp = []

  for orig_point, copy_point in zip(orig_datapoints, datapoints):
    # calc distance from point to boundary
    unit_len = sum(coeff[:-1] ** 2) ** 0.5
    p2b_dist = (sum(copy_point * coeff[:-1]) + coeff[-1]) / unit_len

    if abs(p2b_dist) <= boundary_width * n:
      if p2b_dist >= 0:
        r_nbp.append(orig_point)
      else:
        l_nbp.append(orig_point)

    if abs(p2b_dist) <= boundary_width:
      if p2b_dist >= 0:
        r_bp.append(orig_point)
      else:
        l_bp.append(orig_point)

    if p2b_dist >= 0:
      c_right.append(orig_point)
    else:
      c_left.append(orig_point)

  c_left = np.array(c_left, np.float)
  c_right = np.array(c_right, np.float)
  r_bp = np.array(r_bp, np.float)
  l_bp = np.array(l_bp, np.float)
  r_nbp = np.array(r_nbp, np.float)
  l_nbp = np.array(l_nbp, np.float)

  # left, right, in boundary point, coeff
  return c_left, c_right, (r_bp, l_bp), (r_nbp, l_nbp), coeff


if __name__ == '__main__':
  data = np.array(((3, 6), (3, 1), (8, 2), (7, 4), (6, 9),  (14, 13), (14, 17), (16, 11)))
  _rwm(data)

  # # for i in range(2, 256):
  # #   points, label = utl.gaussian_data_generator(dim=i, objs_size=[1000, 1000, 1000, 1000, 1000], cls=5)
  # #   print("dim = ", i)
  # #   rwm_cut(points)
  # points, label = utl.gaussian_data_generator(dim=2, cls=7)
  # # rwm_cut(points)
  #
  # # for i in np.unique(label):
  # #   fetch_cluster = points[label == i]
  # #   plt.scatter(fetch_cluster[:, 0], fetch_cluster[:, 1], color=np.random.rand(3));
  #
  #
  # c1, c2, d = rwm_cut(points)
  #
  # plt.show()


