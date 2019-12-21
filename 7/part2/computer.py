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

f = open("input", "r")

contents = f.read()

codes = map(int, contents.split(','))

def run_program(intcodes, input_vals, starting_index):
  cur_index = starting_index
  input_val = input_vals[0]
  n = 0
  output_val = input_vals[1]

  while cur_index < (len(intcodes) - 1):
    n += 1
    full_opcode = intcodes[cur_index]
    opcode = full_opcode % 100

    if opcode == HALT:
      return output_val, 0, True

    inputs = [intcodes[cur_index + 1], intcodes[cur_index + 2]]
    if (opcode != USER_OUTPUT):
      result_position = intcodes[cur_index + 3]

    if opcode == USER_INPUT:
      intcodes[inputs[0]] = input_val
      input_val = input_vals[1]
      cur_index += 2
      continue

    parameters = []
    n_parameters = 1 if opcode == USER_OUTPUT else 2
    for i in range(0, n_parameters):
      if (full_opcode / (10 ** (i + 2))) % 10 == 0:
        parameters.append(intcodes[inputs[i]])
      else:
        parameters.append(inputs[i])

    if opcode == ADD:
      intcodes[result_position] = parameters[0] + parameters[1]
      cur_index += 4

    if opcode == MULTIPLY:
      intcodes[result_position] = parameters[0] * parameters[1]
      cur_index += 4

    if opcode == USER_OUTPUT:
      output_val = parameters[0]
      cur_index += 2
      return output_val, cur_index, False

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

permutations = list(itertools.permutations(range(5, 10)))

max_output_val = -1
for phase_setting in permutations:
  output_value = 0
  current_indices = [0,0,0,0,0]
  codesets = [map(int, contents.split(',')), map(int, contents.split(',')), map(int, contents.split(',')), map(int, contents.split(',')), map(int, contents.split(','))]

  for j in range(0, 10):
    for i in range(0, len(phase_setting)):
      input_val1 = int(phase_setting[i]) if j == 0 else output_value
      output_value, current_index, halted  = run_program(codesets[i], [input_val1, output_value], current_indices[i])
      current_indices[i] = current_index
    if halted:
      break
  if max_output_val == -1 or max_output_val < output_value:
    max_output_val = output_value

print(max_output_val)
