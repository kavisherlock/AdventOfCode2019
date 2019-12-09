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

def run_program(intcodes, input_vals):
  cur_index = 0
  input_val = input_vals[0]
  while cur_index < (len(intcodes) - 1):
    full_opcode = intcodes[cur_index]
    opcode = full_opcode % 100

    if opcode == HALT:
      break;

    inputs = [intcodes[cur_index + 1], intcodes[cur_index + 2]]
    result_position = intcodes[cur_index + 3]

    if opcode == USER_INPUT:
      intcodes[inputs[0]] = input_val
      input_val = input_vals[1]
      cur_index += 2
      continue;

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
      return parameters[0]
      cur_index += 2

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

# Using the tool
permutations = list(itertools.permutations(range(0, 5)))

# Manual permutations
permutations = []

def permute(data, i, length):
  if i==length:
    permutations.append(''.join(data))
  else:
    for j in range(i,length):
      #swap
      data[i], data[j] = data[j], data[i]
      permute(data, i+1, length)
      data[i], data[j] = data[j], data[i]

permute(list('01234'), 0, 5)

max_output_val = -1
for phase_setting in permutations:
  output_val = 0
  for i in phase_setting:
    output_val = run_program(map(int, contents.split(',')), [int(i), output_val])
  if max_output_val == -1 or max_output_val < output_val:
    max_output_val = output_val

print(max_output_val)
