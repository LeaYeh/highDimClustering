import utils as utl
import doctest
np = utl.np
plt = utl.plt


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
  (3, 0)

  5, 2, 7, 0, 7, 2, 2
  >>> _box_vote(np.array([[2, -1, 0], [-4, 2, -1], [2, 0, 2], [-2, -8, -10], [2, 2, 1], [-1, 2, -10], [-2, 4, -9]]))
  (2, 7)
  '''

  size, dim = datapoints.shape
  box = np.zeros(2 ** dim, np.int)

  for raw in (datapoints >= 0):
    box[_bin2dec(raw)] += 1

  box = list(enumerate(box))
  box.sort(key=lambda x: x[1], reverse=True)

  return box[0][0], box[1][0]


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


"""
assume that PA always has higher possibility

"""
def _tcf(datapoints, table=None, method=3):
  size, dim = datapoints.shape
  center = np.mean(datapoints, axis=0)
 
  pri_num, sec_num = _box_vote(datapoints - center)

  # method 3
  ravg2= sum(np.sqrt(np.sum(datapoints ** 2, axis=1))) / size
  r2avg = sum(np.sum(datapoints ** 2, axis=0)) / size
  r2list = np.sum(datapoints ** 2, axis=0) / size
  pa = 0.5 + 0.5 * (1 - ravg2 / r2avg) ** 2
  pb = 1 - pa
  val = np.sqrt((pb / pa) * r2list)

  # offset to origin 
  centroid_a = _boxnum2coeff(pri_num, dim) * val + center
  centroid_b = _boxnum2coeff(sec_num, dim) * val + center

  return centroid_a, centroid_b


"""
input: datapoints, table, type of method
output: two list of data in each cluster
"""
@utl.log_msg
def tcf_cut(datapoints, table=None, method=3):
  centroid_a, centroid_b = _tcf(datapoints, table, method)
  cluster_a = []
  cluster_b = []

  for point in datapoints:
    dist_ca = sum((point - centroid_a) ** 2)
    dist_cb = sum((point - centroid_b) ** 2)
    if dist_ca <= dist_cb:
      cluster_a.append(point)
    else:
      cluster_b.append(point)

  return np.array(cluster_a, np.float), np.array(cluster_b, np.float)


if __name__ == '__main__':
  doctest.testmod()
  points, label = utl.gaussian_data_generator(dim=3, cls=5)
  # _box_vote(np.array([2, -1], [4, 2], [0, 2], [-2, -10], [2, 1]))
  print("points[0] = ", points[0])
  _box_vote(points[0:2])
  # _box_vote(points)
  # for i in range(2, 26):
  #   points, label = utl.gaussian_data_generator(dim=i, cls=5, objs_size=[1000, 1000, 1000, 1000, 1000])
  #   print("dim = ", i)
  #   tcf_cut(points)

  # a, b = tcf_cut(points)


  # print(label)
  # for i in np.unique(label):
  #   fetch_cluster = points[label == i]
  #   plt.scatter(fetch_cluster[:, 0], fetch_cluster[:, 1], color=np.random.rand(3));
  #
  # table = build_table(range(9, 12))
  # ca, cb = _tcf(points, table)
  #
  #
  # plt.plot(ca[0], ca[1], "ro", ms=20)
  # plt.plot(cb[0], cb[1], "go", ms=20)
  #
  # plt.show()
