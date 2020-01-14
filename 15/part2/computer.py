HALT = 99
ADD = 1
MULTIPLY = 2
USER_INPUT = 3
USER_OUTPUT = 4
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUAL = 8
RELATIVE_BASE_ADJUST = 9

WALL = 0
OPEN = 1
OXYGEN_SYSTEM = 2
N = 1
S = 2
W = 3
E = 4
OXYGENATED = 3

def run_program(intcodes, input_vals, starting_index, starting_relative_base):
  cur_index = starting_index
  input_ind = 0
  input_val = input_vals[input_ind]
  n = 0
  output_val = 0
  relative_base = starting_relative_base

  # print(intcodes)

  while cur_index < (len(intcodes) - 1):
    n += 1
    full_opcode = intcodes[cur_index]
    opcode = full_opcode % 100

    if opcode == HALT:
      # return
      print ('HALT', output_val)
      return output_val, 0, True, relative_base

    inputs = [intcodes[cur_index + 1], intcodes[cur_index + 2]]

    # print(n, cur_index, full_opcode, opcode, inputs, relative_base, len(intcodes))

    if opcode == USER_INPUT:
      # print ('USER_INPUT', input_val)
      param_mode = (full_opcode / 100) % 10
      if param_mode == 0:
        intcodes[inputs[0]] = input_val
      elif param_mode == 2:
        intcodes[relative_base + inputs[0]] = input_val

      input_ind += 1
      if input_ind < len(input_vals):
        input_val = input_vals[input_ind]
      cur_index += 2
      continue

    parameters = []
    n_parameters = 1 if opcode == USER_OUTPUT or opcode == RELATIVE_BASE_ADJUST else 2
    for i in range(0, n_parameters):
      param_mode = (full_opcode / (10 ** (i + 2))) % 10
      if param_mode == 1:
        parameters.append(inputs[i])
      else:
        if param_mode == 0:
          param_position = inputs[i]
        elif param_mode == 2:
          param_position = relative_base + inputs[i]
        if param_position >= len(intcodes):
          for i in range(0, (param_position - len(intcodes) + 1)):
            intcodes.append(0)
        parameters.append(intcodes[param_position])

    if (opcode in [ADD, MULTIPLY, LESS_THAN, EQUAL]):
      param_mode = (full_opcode / 10000) % 10
      result_position = intcodes[cur_index + 3]
      if param_mode == 2:
        result_position = relative_base + intcodes[cur_index + 3]
      if result_position >= len(intcodes):
        for i in range(0, (result_position - len(intcodes) + 1)):
          intcodes.append(0)

    if opcode == ADD:
      intcodes[result_position] = parameters[0] + parameters[1]
      cur_index += 4

    if opcode == MULTIPLY:
      intcodes[result_position] = parameters[0] * parameters[1]
      cur_index += 4

    if opcode == USER_OUTPUT:
      output_val = parameters[0]
      cur_index += 2
      # print(output_val)
      # print ('USER_OUTPUT', output_val)
      return output_val, cur_index, False, relative_base

    if opcode == JUMP_IF_TRUE:
      cur_index = parameters[1] if parameters[0] != 0 else cur_index + 3

    if opcode == JUMP_IF_FALSE:
      cur_index = parameters[1] if parameters[0] == 0 else cur_index + 3

    if opcode == LESS_THAN:
      intcodes[result_position] = 1 if parameters[0] < parameters[1] else 0
      cur_index += 4

    if opcode == EQUAL:
      intcodes[result_position] = 1 if parameters[0] == parameters[1] else 0
      cur_index += 4

    if opcode == RELATIVE_BASE_ADJUST:
      relative_base += parameters[0]
      cur_index += 2

f = open("input", "r")
contents = f.read()
codes = map(int, contents.split(','))
current_index = 0
relative_base = 0
output_value = 0
n = 0
start_node = (0, 0)
queue = [(start_node, current_index, codes)]
maze = {start_node: (1, 0)}
done = False

# Breadth First Search
while len(queue) != 0:
  popped = queue.pop(0)
  node = popped[0]
  current_current_index = popped[1]
  codes = popped[2]
  depth = maze[node][1]
  for direction in [N, S, W, E]:
    current_codes = [elem for elem in codes]
    output_value, current_index, halted, relative_base = run_program(current_codes, [direction], current_current_index, relative_base)

    if direction == N:
      next_node = (node[0], node[1] + 1)
    if direction == S:
      next_node = (node[0], node[1] - 1)
    if direction == W:
      next_node = (node[0] - 1, node[1])
    if direction == E:
      next_node = (node[0] + 1, node[1])

    # print (current_current_index, current_index, direction, output_value, node, next_node)

    if not next_node in maze:
      maze[next_node] = (output_value, depth + 1)
      if output_value == OPEN:
        queue.append((next_node, current_index, current_codes))

    if output_value == OXYGEN_SYSTEM:
      new_start_node = next_node
      print('DONE!')
      print('Oxygen starts at '+ str(new_start_node))
      done = True


start_node = new_start_node
queue = [start_node]
maze[start_node] = (OXYGENATED, 0)

# Breadth First Search on existing maze for all depths
while len(queue) != 0:
  node = queue.pop(0)
  depth = maze[node][1]
  for direction in [N, S, W, E]:
    if direction == N:
      next_node = (node[0], node[1] + 1)
    if direction == S:
      next_node = (node[0], node[1] - 1)
    if direction == W:
      next_node = (node[0] - 1, node[1])
    if direction == E:
      next_node = (node[0] + 1, node[1])

    if next_node in maze:
      if maze[next_node][0] == OPEN:
        maze[next_node] = (OXYGENATED, depth + 1)
        queue.append(next_node)

max_depth = -1
for node in maze.values():
  if node[1] > max_depth:
    max_depth = node[1]

print('Max Depth: ' + str(max_depth))
