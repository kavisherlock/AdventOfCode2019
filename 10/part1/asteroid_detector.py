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

def get_n_asteroids_in_sight(curr_row, curr_col):
  n_visible = 0
  for r in range(n_rows):
    for c in range(n_cols):
      if space[r][c] == ASTEROID and (curr_row != r or curr_col != c):
        if check_if_visible(curr_row, curr_col, r, c):
          n_visible += 1
  return n_visible

max_asteroids = -1
for c in range(n_cols):
  for r in range(n_rows):
    if space[r][c] == ASTEROID:
      n_asteroids = get_n_asteroids_in_sight(r, c)
      if max_asteroids <= n_asteroids:
        max_asteroids = n_asteroids
        max_asteroid_r = r
        max_asteroid_c = c

print(max_asteroid_c, max_asteroid_r, max_asteroids)
