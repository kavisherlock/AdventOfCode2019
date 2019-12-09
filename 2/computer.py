import math

f = open("input", "r")

contents = f.read()

for i in range(1, 30):
  for j in range(1, 60):
    intcodes = map(int, contents.split(','))
    intcodes[1] = i
    intcodes[2] = j
    cur_index = 0

    while cur_index < (len(intcodes) - 1):
      opcode = intcodes[cur_index]
      if opcode == 1:
        intcodes[intcodes[cur_index + 3]] = intcodes[intcodes[cur_index + 1]] + intcodes[intcodes[cur_index + 2]]
      if opcode == 2:
        intcodes[intcodes[cur_index + 3]] = intcodes[intcodes[cur_index + 1]] * intcodes[intcodes[cur_index + 2]]
      if opcode == 99:
        break;
      cur_index += 4

    if intcodes[0] == 19690720:
      print(i, j, 100 * i + j)

