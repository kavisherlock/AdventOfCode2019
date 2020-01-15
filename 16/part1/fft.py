f = open("input", "r")
signal = f.read() * 10000
n_digits = len(signal)
base_pattern = [0, 1, 0, -1]
n_phases = 100

patterns = []
for output_ind in range(1, n_digits + 1):
  pattern = []
  for i in range(0, len(base_pattern)):
    for j in range(0, output_ind):
      pattern.append(base_pattern[i])
  patterns.append(pattern)

phase_input = signal
for phase_ind in range(0, n_phases):
  print('Running phase ' + str(phase_ind))
  phase_output = ''
  for output_ind in range(0, n_digits):
    output_sum = 0
    pattern = patterns[output_ind]
    for input_ind in range(0, n_digits):
      output_sum += int(phase_input[input_ind]) * pattern[(input_ind + 1) % len(pattern)]
    phase_output += str(abs(output_sum) % 10)
  phase_input = phase_output

print(phase_output[0:8])
