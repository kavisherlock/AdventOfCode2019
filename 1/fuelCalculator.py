import math

f = open("input", "r")

contents = f.readlines()

total_fuel = 0
for input_val in contents:
  fuel_needed = math.floor(int(input_val) / 3) - 2
  total_fuel += fuel_needed
  while (fuel_needed > 0):
    new_fuel = math.floor(int(fuel_needed) / 3) - 2
    if (new_fuel <= 0):
      break
    total_fuel += new_fuel
    fuel_needed = new_fuel

print(total_fuel)
