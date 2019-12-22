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

EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

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
      # print ('HALT', output_val)
      # return
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
input_val = 0
halted = False
n_block_tiles = -1
paddle_xpos = 0
ball_xpos = 0
score = -1
turns = 0
while n_block_tiles != 0:
  turns += 1
  n_block_tiles = 0
  buckets = [['_' for col in range(35)] for row in range(25)]

  while not halted:
    x, current_index, halted, relative_base = run_program(codes, [input_val], current_index, relative_base)
    if halted:
      break
    y, current_index, halted, relative_base = run_program(codes, [input_val], current_index, relative_base)
    if halted:
      break
    tile_id, current_index, halted, relative_base = run_program(codes, [input_val], current_index, relative_base)

    if x == -1 and y == 0 and tile_id != 0:
      score = tile_id
    else:
      buckets[y][x] = str(tile_id) if tile_id != EMPTY else ' '

    if tile_id == BLOCK:
      n_block_tiles += 1
    if tile_id == PADDLE:
      paddle_xpos = x
    if tile_id == BALL:
      ball_xpos = x

  if paddle_xpos < ball_xpos:
    input_val = 1
  elif paddle_xpos > ball_xpos:
    input_val = -1
  else:
    input_val = 0
  print(n_block_tiles, score)


  halted = False

  for bucket in buckets:
    print(''.join(bucket))

print('Only took', turns, 'turns')