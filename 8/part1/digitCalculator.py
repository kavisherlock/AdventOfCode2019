f = open("input", "r")
image = f.read()

layer_area = 25 * 6
n_layers = (len(image) - 2) / layer_area

layer_digits = []
min_n_zeros = -1
min_n_zeros_index = -1
for i in range(0, n_layers):
  layer = image[i * layer_area : (i + 1) * layer_area]
  digits = [0, 0, 0, 0, 0, 0, 0, 0, 0]
  for digit in layer:
    digits[int(digit)] += 1
  if min_n_zeros == -1 or min_n_zeros > digits[0]:
    min_n_zeros = digits[0]
    min_n_zeros_index = i
  layer_digits.append(digits)

print(layer_digits[min_n_zeros_index][1] * layer_digits[min_n_zeros_index][2])