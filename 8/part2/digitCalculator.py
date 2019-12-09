import numpy as np

f = open("input", "r")
image = f.read()

layer_area = 25 * 6
n_layers = (len(image) - 2) / layer_area

final_image = np.ones((6, 25)) * 2

layers = []
for i in range(0, n_layers):
  layer = image[i * layer_area : (i + 1) * layer_area]
  layers.append(layer)

  for row in range(0, 6):
    for column in range(0, 25):
      if final_image[row][column] == 2:
        final_image[row][column] = layer[row * 25 + column]

for i in final_image:
  row = []
  for j in i:
    to_append = '\033[92m'+str(int(j)) if j == 1 else '\033[94m'+str(int(j))
    row.append(to_append)
  print ' '.join(row)