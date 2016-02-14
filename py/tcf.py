import utils as utl
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
  res = np.zeros(dim, np.int)

  for i in range(dim - 1, -1, -1):  
    if(dec // (2 ** i) > 0):
      res[i] = 1
    else:
      res[i] = 0
    dec %= (2 ** i)

  return res


def _bin2dec(bools):
  res = 0

  for i in range(0, len(bools)):
    if bools[i]:
      res += 2 ** i

  return res


def _box_vote(datapoints):
  size, dim = datapoints.shape
  box = np.zeros(2 ** dim, np.int)

  for raw in (datapoints > 0):
    box[_bin2dec(raw)] += 1

  box = list(enumerate(box))
  box.sort(key=lambda x: x[1], reverse=True)

  return box[0][0], box[1][0]


def _bin2coeff(data):
  data[data == 0] = -1
  return data


def _boxnum2coeff(dec, dim):
  bin_num = _dec2bin(dec, dim)
  bin_num[bin_num == 0] = -1

  return bin_num


"""
assume that PA always has higher possibility

"""
def tcf(datapoints, table=None, method=3):
  size, dim = datapoints.shape
  center = np.mean(datapoints, axis=0)
 
  utl.pprint(datapoints - center) 
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

  print(datapoints)
  print(centroid_a)
  print(centroid_b)

  return centroid_a, centroid_b


if __name__ == '__main__':
  points, label = utl.gaussian_data_generator(dim=2, cls=2, objs_size=[200, 100])

  print(label)
  for i in np.unique(label):
    fetch_cluster = points[label == i]
    plt.scatter(fetch_cluster[:, 0], fetch_cluster[:, 1], color=np.random.rand(3));

  table = build_table(range(9, 12))
  ca, cb = tcf(points, table)

  ca = ca.astype(np.int)
  cb = cb.astype(np.int)

  plt.plot(ca[0], ca[1], "ro", ms=20)
  plt.plot(cb[0], cb[1], "go", ms=20)

  plt.show()
