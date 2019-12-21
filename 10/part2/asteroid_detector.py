import math

with open('input') as textFile:
  space = [list(line[0:-1]) for line in textFile]

n_rows = len(space)
n_cols = len(space[0])

ASTEROID = '#'

def check_if_visible(curr_row, curr_col, row_to_check, col_to_check):
  min_row = min(curr_row, row_to_check)
  min_col = min(curr_col, col_to_check)
  max_row = max(curr_row, row_to_check)
  max_col = max(curr_col, col_to_check)

  if row_to_check == curr_row:
    for c in range(min_col + 1, max_col):
      if space[curr_row][c] == ASTEROID:
        return False
    return True

  if col_to_check == curr_col:
    for r in range(min_row + 1, max_row):
      if space[r][curr_col] == ASTEROID:
        return False
    return True

  row_diff = row_to_check - curr_row
  col_diff = col_to_check - curr_col

  for r in range(min_row + 1, max_row):
    for c in range(min_col + 1, max_col):
      if (space[r][c] == ASTEROID):
        # check if the asteroid lies on the line connected the two asteroid being tested
        # Calculating slope and intercept and using it down here (avoiding division)
        if r * col_diff == row_diff * c + (col_diff * curr_row - row_diff * curr_col):
          return False
  return True

def get_n_asteroids_in_sight(curr_col, curr_row):
  n_visible = 0
  visible_asteroids = []
  for r in range(n_rows):
    for c in range(n_cols):
      if space[r][c] == ASTEROID and (curr_row != r or curr_col != c):
        if check_if_visible(curr_row, curr_col, r, c):
          n_visible += 1
          visible_asteroids.append((c, r))
  return n_visible, visible_asteroids

# from part1
station_c = 26
station_r = 36

n_removed = 0
n_to_remove = 200
n_asteroids, visible_asteroids = get_n_asteroids_in_sight(station_c, station_r)

while(n_asteroids < (n_to_remove - n_removed)):
  for asteroid in visible_asteroids:
    space[asteroid[1]][asteroid[0]] = 'X'
  n_removed += n_asteroids
  n_asteroids, visible_asteroids = get_n_asteroids_in_sight(station_c, station_r)

asteroids_and_angles = {}
for asteroid in visible_asteroids:
  true_angle = math.degrees(math.atan2(asteroid[0] - station_c, station_r - asteroid[1]))
  positive_angle = true_angle if true_angle >= 0 else 360 + true_angle
  asteroids_and_angles[positive_angle] = asteroid

for angle in sorted(asteroids_and_angles):
  n_removed += 1
  if (n_removed == n_to_remove):
    print(asteroids_and_angles[angle])
    break