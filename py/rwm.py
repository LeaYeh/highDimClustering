import utils as utl
np = utl.np
plt = utl.plt

"""
input:  datapoints
output: a boundary/hyperplane, split two cluster
"""
def rwm(datapoints):
  size, dim = datapoints.shape
  center = np.mean(datapoints, axis=0)

  r = np.sum((datapoints - center) ** 2, axis=1)
  R = sum(r)
  w = r.dot(datapoints) / R
  v = w - center
  coeff = np.append(v, sum(-v * w))

  return coeff


if __name__ == '__main__':
  points, label = utl.gaussian_data_generator(dim=2, cls=2)
 
  for i in np.unique(label):
    fetch_cluster = points[label == i]
    plt.scatter(fetch_cluster[:, 0], fetch_cluster[:, 1], color=np.random.rand(3));

  coeff = rwm(points)
  utl.graph(coeff, range(-1000, 1000))

  plt.show()


