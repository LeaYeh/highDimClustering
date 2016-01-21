from numpy import linalg as LA

with open("../dataset/py/data_2d2cxn.txt", "r") as f:
  data = f.read()
  points = data.split()
x_pos = list(map(float, points[::2]))
y_pos = list(map(float, points[1::2]))
x_bar = sum(x_pos)/len(x_pos)
y_bar = sum(y_pos)/len(y_pos)
ri = [((i-x_bar)**2 + (j-y_bar)**2) ** (1/2) for i,j in zip(x_pos, y_pos)]
R = sum(ri)
x = sum((i*j) for i,j in zip(ri, x_pos)) / R
y = sum((i*j) for i,j in zip(ri, y_pos)) / R
print("x  = {}, y  = {}".format(x_bar, y_bar))
print("x' = {}, y' = {}".format(x, y))
boundary = [-(y_bar-y), (x_bar-x)]
norm = LA.norm(boundary)
boundary = [boundary[0]/norm, boundary[1]/norm]
print(boundary)
