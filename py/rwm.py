import utils as utl
np = utl.np
plt = utl.plt

"""
input:  datapoints
output: a boundary/hyperplane, split two cluster
"""
def _rwm(datapoints):
  size, dim = datapoints.shape
  center = np.mean(datapoints, axis=0)

  r = np.sum((datapoints - center) ** 2, axis=1)
  R = sum(r)
  w = r.dot(datapoints) / R
  v = w - center
  coeff = np.append(v, sum(-v * w))

  return coeff


"""
input:  datapoints(numpy.ndarray)
output: list
"""
def rwm_cut(datapoints):
  size, dim = datapoints.shape
  c_left = []
  c_right = []

  coeff = _rwm(datapoints)

  for point in datapoints:
    if sum(point * coeff[:-1]) + coeff[-1] >= 0:
      c_right.append(point)
    else:
      c_left.append(point)

  return np.array(c_left, np.float), np.array(c_right, np.float)



if __name__ == '__main__':
  points, label = utl.gaussian_data_generator(dim=2, cls=2)
 
  for i in np.unique(label):
    fetch_cluster = points[label == i]
    plt.scatter(fetch_cluster[:, 0], fetch_cluster[:, 1], color=np.random.rand(3));

  coeff = rwm(points)
  utl.graph(coeff, range(-1000, 1000))

  plt.show()


