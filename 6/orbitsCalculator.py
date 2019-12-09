f = open("input", "r")

object_map = f.read().splitlines()

object_dict = {
  'COM': -1
}

total_orbits = 0

for object_pair in object_map:
  objects = object_pair.split(')')
  object_dict[objects[1]] = objects[0]

for object in object_dict:
  parent = object_dict[object]
  while parent != -1:
    object = parent
    total_orbits += 1
    parent = object_dict[object]

print total_orbits

path = 0
object = object_dict['YOU']
while object != 'COM':
  parent = object_dict[object]
  print (object, parent, path)
  object_dict[object] = (parent, path)
  object = parent
  path += 1

path = 0
object = object_dict['SAN']
while object != 'COM':
  if len(object_dict[object]) == 2:
    path += int(object_dict[object][1])
    break
  path += 1
  parent = object_dict[object]
  object = parent

print path