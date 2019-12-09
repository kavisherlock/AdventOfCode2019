HALT = 99
ADD = 1
MULTIPLY = 2
USER_INPUT = 3
PRINT = 4
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUAL = 8

f = open("input", "r")

input_val = 5
contents = f.read()
intcodes = map(int, contents.split(','))

cur_index = 0
while cur_index < (len(intcodes) - 1):
  full_opcode = intcodes[cur_index]
  opcode = full_opcode % 100

  if opcode == HALT:
    break;

  inputs = [intcodes[cur_index + 1], intcodes[cur_index + 2]]
  result_position = intcodes[cur_index + 3]

  if opcode == USER_INPUT:
    intcodes[inputs[0]] = input_val
    cur_index += 2
    continue;

  parameters = []
  n_parameters = 1 if opcode == PRINT else 2
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

  if opcode == PRINT:
    print(parameters[0])
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
