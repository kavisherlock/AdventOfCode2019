passwords = 0
for candidate in range(231832, 767346 + 1):
  candidate = str(candidate)
  digits = [0, 0, 0, 0, 0, 0, 0, 0, 0]
  for digit in candidate:
    digits[int(digit) - 1] += 1
  same_adjacent_digits = 2 in digits

  increasing_digits = True
  for j in range(0, 5):
    if candidate[j] > candidate[j + 1]:
      increasing_digits = False
  
  if increasing_digits and same_adjacent_digits:
    passwords += 1

print(passwords)
