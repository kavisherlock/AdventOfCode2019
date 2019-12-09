f = open("input", "r")

contents = f.readlines()

wires_coordinates = []

for wire_path in contents:
  wire_paths = wire_path.split(',')
  wire_coordinates = []
  lastx = 0
  lasty = 0
  for path_section in wire_paths:
    direction = path_section[0]
    distance = int(path_section[1:])
    for i in range(0, distance):
      if direction == 'R':
        wire_coordinates.append((lastx + 1, lasty))
        lastx = lastx + 1
      if direction == 'L':
        wire_coordinates.append((lastx - 1, lasty))
        lastx = lastx - 1
      if direction == 'U':
        wire_coordinates.append((lastx, lasty + 1))
        lasty = lasty + 1
      if direction == 'D':
        wire_coordinates.append((lastx, lasty - 1))
        lasty = lasty - 1
  wires_coordinates.append(wire_coordinates)

intersections = set(wires_coordinates[0]).intersection(set(wires_coordinates[1]))

min_distance = -1
for intersection in intersections:
  # distance = abs(intersectiion[0]) + abs(intersection[1])
  distance = wires_coordinates[0].index(intersection) + wires_coordinates[1].index(intersection)
  if min_distance == -1 or distance < min_distance:
    min_distance = distance

print('sets and intersections', min_distance)

