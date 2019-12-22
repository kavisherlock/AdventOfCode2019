ADD = 1
MULTIPLY = 2
USER_INPUT = 3
USER_OUTPUT = 4
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUAL = 8
RELATIVE_BASE_ADJUST = 9
HALT = 99

LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3


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
      # print ('HALT', output_val)
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

    if opcode == 42:
      return output_val, cur_index, True


def get_robot_position(cur_position, next_direction):
  if next_direction == LEFT:
    return (cur_position[0] - 1, cur_position[1])
  if next_direction == RIGHT:
    return (cur_position[0] + 1, cur_position[1])
  if next_direction == UP:
    return (cur_position[0], cur_position[1] + 1)
  if next_direction == DOWN:
    return (cur_position[0], cur_position[1] - 1)


def get_robot_direction(cur_direction, turn):
  if (cur_direction == UP and turn == LEFT) or (cur_direction == DOWN and turn == RIGHT):
    return LEFT
  if (cur_direction == UP and turn == RIGHT) or (cur_direction == DOWN and turn == LEFT):
    return RIGHT
  if (cur_direction == LEFT and turn == LEFT) or (cur_direction == RIGHT and turn == RIGHT):
    return DOWN
  if (cur_direction == RIGHT and turn == LEFT) or (cur_direction == LEFT and turn == RIGHT):
    return UP


f = open("input", "r")

contents = f.read()

codes = map(int, contents.split(','))

halted = False
current_index = 0
relative_base = 0
cur_paint = 1
robot_position = (5, 10)
robot_direction = UP

panels = {robot_position: cur_paint}
panel_visited = {robot_position: 1}

while not halted:
  if robot_position in panels.keys():
    panel_visited[robot_position] += 1
    cur_paint = panels[robot_position]
  else:
    panel_visited[robot_position] = 1
    cur_paint = 0

  paint, current_index, halted, relative_base = run_program(codes, [cur_paint], current_index, relative_base)
  if halted:
    break
  turn_direction, current_index, halted, relative_base = run_program(codes, [cur_paint], current_index, relative_base)

  panels[robot_position] = paint

  robot_direction = get_robot_direction(robot_direction, turn_direction)
  robot_position = get_robot_position(robot_position, robot_direction)

  # print (len(panels))

# print (panels)
# print (panel_visited)
print (len(panels))

min_x = -1
max_x = -1
min_y = -1
max_y = -1
for panel in panels.keys():
  if min_x == -1 or min_x > panel[0]:
    min_x = panel[0]
  if max_x == -1 or max_x < panel[0]:
    max_x = panel[0]
  if min_y == -1 or min_y > panel[1]:
    min_y = panel[1]
  if max_y == -1 or max_y < panel[1]:
    max_y = panel[1]
print(min_x, min_y, max_x, max_y)


buckets = [['_' for col in range(20)] for row in range(50)]

for panel in panels.keys():
  if panels[panel] == 1:
    buckets[panel[0]][panel[1]] = 'O'
  else:
    buckets[panel[0]][panel[1]] = '_'

for bucket in buckets:
  print(''.join(bucket))
