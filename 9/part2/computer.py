import itertools

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

def run_program(intcodes, input_vals, starting_index = 0):
  cur_index = starting_index
  input_ind = 0
  input_val = input_vals[input_ind]
  n = 0
  output_val = 0
  relative_base = 0

  # print(intcodes)

  while cur_index < (len(intcodes) - 1):
    n += 1
    full_opcode = intcodes[cur_index]
    opcode = full_opcode % 100

    if opcode == HALT:
      return
      # print ('HALT', output_val)
      # return output_val, 0, True

    inputs = [intcodes[cur_index + 1], intcodes[cur_index + 2]]

    if opcode == USER_INPUT:
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
      if param_mode == 0:
        parameters.append(intcodes[inputs[i]])
      elif param_mode == 1:
        parameters.append(inputs[i])
      elif param_mode == 2:
        parameters.append(intcodes[relative_base + inputs[i]])

    if (opcode != USER_OUTPUT):
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
      print(output_val)
      # print ('USER_OUTPUT', output_val)
      # return output_val, cur_index, False

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

run_program(codes, [2])
