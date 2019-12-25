import math

stoichiometry_hash = {}

with open('input') as textFile:
  reactions = [(line[0:-1]) for line in textFile]
  for reaction in reactions:
    components = reaction.split(' => ')
    reactants = [component.split(' ') for component in components[0].split(', ')]
    product = components[1].split(' ')
    stoichiometry_hash[product[1]] = (product[0], reactants)

# print(stoichiometry_hash)

def get_distance_from_ore(product):
  if product == 'ORE':
    return 0

  return 1 + max([get_distance_from_ore(reactant[1]) for reactant in stoichiometry_hash[product][1]])

cur_products = { 'FUEL': 1 }
cur_distance = get_distance_from_ore('FUEL')

# print(cur_distance, stoichiometry_hash['FUEL'])

while cur_distance > 0:
  # for product in cur_products:
  #   print('Products', product, cur_products[product])

  products_over_depth = []
  for product in cur_products:
    if get_distance_from_ore(product) >= cur_distance:
      products_over_depth.append(product)

  for product in products_over_depth:
    product_amount = stoichiometry_hash[product][0]
    reactants = stoichiometry_hash[product][1]
    for reactant in reactants:
      if reactant[1] in cur_products:
        cur_products[reactant[1]] += int(math.ceil(cur_products[product] * 1. / int(product_amount)) * int(reactant[0]))
      else:
        cur_products[reactant[1]] = int(math.ceil(cur_products[product] * 1. / int(product_amount)) * int(reactant[0]))

    del cur_products[product]

  # print(cur_products)
  cur_distance -= 1

print(cur_products['ORE'])

''' DOES NOT TAKE LEFTOVER REACTANTS INTO ACCOUNT
leftover_ore = 0
def get_ore_needed(product):
  global leftover_ore
  reactants = stoichiometry_hash[product][1]

  if reactants[0][1] == 'ORE':
    if leftover_ore >= int(reactants[0][0]):
      leftover_ore -= int(reactants[0][0])
      return 0
    return int(reactants[0][0])

  total_ore_needed = 0
  for reactant in reactants:
    leftover_ore += max(int(stoichiometry_hash[reactant[1]][0]) - int(reactant[0]), 0)
    ore_needed = int(math.ceil(int(reactant[0]) * 1. / int(stoichiometry_hash[reactant[1]][0]))) * get_ore_needed(reactant[1])
    total_ore_needed += ore_needed

  return total_ore_needed

print(get_ore_needed('FUEL') + leftover_ore)
'''


