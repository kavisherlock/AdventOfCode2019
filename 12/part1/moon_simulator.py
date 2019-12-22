import copy

initial_position = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
initial_velocity = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
positions = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
velocities = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

with open('input') as textFile:
  space = [(line[1:-2]) for line in textFile]
  for moon_ind in range(len(space)):
    for i in range(3):
      initial_position[moon_ind][i] = int(space[moon_ind].split(',')[i].split('=')[1])
      positions[moon_ind][i] = int(space[moon_ind].split(',')[i].split('=')[1])

# for i in range(4):
#   print(positions[i], velocities[i])

def gravity(pos, vel):
  new_vel = copy.deepcopy(vel)
  for moon_ind1 in range(len(pos)):
    for moon_ind2 in range(moon_ind1 + 1, len(pos)):
      for coord_ind in range(3):
        if pos[moon_ind1][coord_ind] < pos[moon_ind2][coord_ind]:
          new_vel[moon_ind1][coord_ind] = new_vel[moon_ind1][coord_ind] + 1
          new_vel[moon_ind2][coord_ind] = new_vel[moon_ind2][coord_ind] - 1
        elif pos[moon_ind1][coord_ind] > pos[moon_ind2][coord_ind]:
          new_vel[moon_ind1][coord_ind] = new_vel[moon_ind1][coord_ind] - 1
          new_vel[moon_ind2][coord_ind] = new_vel[moon_ind2][coord_ind] + 1
  return new_vel

def velocity(pos, vel):
  new_pos = copy.deepcopy(pos)
  for moon_ind in range(len(vel)):
    for coord_ind in range(3):
      new_pos[moon_ind][coord_ind] = pos[moon_ind][coord_ind] + vel[moon_ind][coord_ind]
  return new_pos

def timestep(pos, vel):
  new_vel = gravity(pos, vel)
  new_pos = velocity(pos, new_vel)

  return (new_pos, new_vel)

def calculate_energy(pos, vel):
  total = 0
  for i in range(4):
    pot = sum([abs(ele) for ele in pos[i]])
    kin = sum([abs(ele) for ele in vel[i]])
    total += pot * kin
  return total

n_steps = 1000
for i in range(n_steps):
  positions, velocities = (timestep(positions, velocities))
  # print('_')
  # for i in range(4):
  #   print(positions[i], velocities[i])

for i in range(4):
  print(positions[i], velocities[i])
print(calculate_energy(positions, velocities))
