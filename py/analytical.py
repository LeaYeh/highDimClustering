import utils as utl
import doctest
from rwm import cut_by_coeff
import heapq
np = utl.np
plt = utl.plt
from copy import deepcopy


def build_table(dim_range):
  table = np.zeros((51, len(dim_range)), np.float)

  for d in dim_range:
    table[0, d - dim_range[0]] = d
    for b in range(1, 51):
      pb = b / 100
      pa = 1 - pb
      table[b, d - dim_range[0]] = \
        (pa + pa ** d / pb ** (d - 1)) ** (d - 1) / \
        (pa + pa ** (d - 1) / pb ** (d - 2)) ** d

  np.savetxt("tcf_table", table, fmt='%12.6f', delimiter=',')

  return table


def _dec2bin(dec, dim):
  '''
  :input: dec, dim
  :output: binary
  >>> _dec2bin(5, 3)
  array([1, 0, 1])
  >>> _dec2bin(5, 5)
  array([1, 0, 1, 0, 0])
  >>> _dec2bin(17, 5) 
  array([1, 0, 0, 0, 1])
  >>> _dec2bin(17, 7) 
  array([1, 0, 0, 0, 1, 0, 0])
  '''
  res = np.zeros(dim, np.int)

  for i in range(dim - 1, -1, -1):  
    if(dec // (2 ** i) > 0):
      res[i] = 1
    else:
      res[i] = 0
    dec %= (2 ** i)

  return res


def _bin2dec(bools):
  '''
  :input: ndarray
  :output: dec
  >>> _bin2dec([0, 0, 1, 1, 0, 1, 0])
  44
  >>> _bin2dec([1, 1, 0, 1, 0])
  11
  '''

  res = 0

  for i in range(0, len(bools)):
    # if bools[i] > 0:
    if bools[i]:
      res += 2 ** i

  return res


def _box_vote(datapoints):
  ''' check point's quadrant then vote it, then find the first and second boxes
  :input: datapoints <- ndarray
  :output: first and second boxes id <- (int, int)

  1, 3, 3, 0, 0, 3
  >>> _box_vote(np.array([[2, -1], [4, 2], [0, 2], [-2, -10], [-2, -1], [33, 2]]))
  3

  5, 2, 7, 0, 7, 2, 2
  >>> _box_vote(np.array([[2, -1, 0], [-4, 2, -1], [2, 0, 2], [-2, -8, -10], [2, 2, 1], [-1, 2, -10], [-2, 4, -9]]))
  2
  '''

  box_dict = {}

  for point in (datapoints >= 0):
    hash_idx = _bin2dec(point)
    num = box_dict.get(hash_idx, 0)
    box_dict[hash_idx] = num + 1

  res = max(box_dict, key=box_dict.get)

  return res


def _bin2coeff(data):
  '''
  :input: data <- list
  :output: data replace 0 to -1 <- list
  >>> _bin2coeff(np.array([1, 0, 1, 1, 0, 0]))
  array([ 1, -1,  1,  1, -1, -1])
  '''
  data[data == 0] = -1
  return data


def _boxnum2coeff(dec, dim):
  ''' translate box id to quadrant representation
  :input: box id(dec) <- int, dim
  :output: quadrant <- list
  >>> _boxnum2coeff(4, 5)
  array([-1, -1,  1, -1, -1])
  >>> _boxnum2coeff(11, 7)
  array([ 1,  1, -1,  1, -1, -1, -1])
  '''
  bin_num = _dec2bin(dec, dim)
  bin_num[bin_num == 0] = -1

  return bin_num


def ensure_pa_is_greater(pa, pb):
  if pa < pb:
    tmp = pa
    pa = pb
    pb = tmp

  return pa, pb



def sort_points_by_variance(points):
  p2 = points ** 2
  var = np.mean(p2, axis=0)

  sort_indexs = np.argsort(-var)
  points = points[:, sort_indexs]

  return points



def cut_by_coeff(orig_datapoints, coeff):
  datapoints = deepcopy(orig_datapoints)
  datapoints = utl.centralize_data(datapoints)
  datapoints = utl.normalize_data(datapoints)
  datapoints = sort_points_by_variance(datapoints)[:, :12]

  c_left = []
  c_right = []
  unit_len = sum(coeff[:-1] ** 2) ** 0.5

  for orig_point, copy_point in zip(orig_datapoints, datapoints):
    p2b_dist = (sum(copy_point * coeff[:-1]) + coeff[-1]) / unit_len
    if p2b_dist >= 0:
      c_right.append(orig_point)
    else:
      c_left.append(orig_point)
  c_left = np.array(c_left, np.float)
  c_right = np.array(c_right, np.float)

  return (c_left, c_right)



"""
assume that PA always has higher possibility

"""
def _tcf(orig_datapoints):
  datapoints = deepcopy(orig_datapoints)
  # datapoints = utl.centralize_data(datapoints)
  # datapoints = utl.normalize_data(datapoints)
  size, dim = datapoints.shape

  data2 = datapoints ** 2
  data2_bar = np.mean(data2, axis=0)


  r = np.sqrt( np.sum(data2, axis = 1) )
  rbar_2 = ( np.sum(r, axis=0) / size ) ** 2
  r2_bar = np.sum((r ** 2), axis=0) / size
  pa = 0.5 + 0.5 * np.sqrt(1 - rbar_2 / r2_bar)
  pb = 1 - pa
  pa, pb = ensure_pa_is_greater(pa, pb)
  val = np.sqrt((pb / pa) * data2_bar)


  pri_num = _box_vote(datapoints)
  ca_coeff = _boxnum2coeff(pri_num, dim)
  cb_coeff = [-i for i in ca_coeff]

  print('ca_coeff = ', ca_coeff)
  print('cb_coeff = ', cb_coeff)

  centroid_a = ca_coeff * val
  centroid_b = cb_coeff * val

  print('centroid_a = {}, centroid_b = {}'.format(centroid_a, centroid_b))

  v = centroid_b - centroid_a
  o = (centroid_a + centroid_b) / 2
  coeff = np.append(v, sum(-v * o))

  return coeff, centroid_a, centroid_b


"""
input: datapoints, table, type of method
output: two list of data in each cluster
"""
@utl.log_msg
def tcf_cut(orig_datapoints, boundary_width=0.1, n=2):
  datapoints = deepcopy(orig_datapoints)
  datapoints = utl.centralize_data(datapoints)
  datapoints = utl.normalize_data(datapoints)
  datapoints = sort_points_by_variance(datapoints)[:, :12]

  coeff, oa, ob = _tcf(datapoints)

  c_left = []
  c_right = []

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
  # doctest.testmod()

  from experiment import data_seletor
  # points, labels = data_seletor('hand_write_digits')

  # points, label = utl.gaussian_data_generator(dim=2, cls=2)
  points, label = utl.normal_data_generator(dim=2, cls=2)
  # points = np.array([ [0, 0], [0, 1], [0, 2], [0, 3], [0, -1], [0, -2], [25, -3], [25, -2], [25, -4], [25, -6], [25, -5], [-5, 0], [-5, 1], [30, -4] ])


  import rwm as rwm

  c1, c2, in_boundary, in_n_boundary, coeff = rwm.rwm_cut(points)
  a, b, in_boundary, in_n_boundary, coeff = tcf_cut(points)
  coeff, oa, ob = _tcf(points)

  fig, axs = plt.subplots(1, 2)

  axs[0].set_title('rwm')
  axs[0].plot(c1[:, 0], c1[:, 1], 'ro')
  axs[0].plot(c2[:, 0], c2[:, 1], 'bo')

  axs[1].set_title('analytical')
  axs[1].plot(a[:, 0], a[:, 1], 'ro')
  axs[1].plot(b[:, 0], b[:, 1], 'bo')

  axs[1].plot(oa[0], oa[1], 'go')
  axs[1].plot(ob[0], ob[1], 'go')

  plt.tight_layout()
  plt.show()
