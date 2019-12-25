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

def get_ore_needed(fuel_amount):
  cur_products = { 'FUEL': fuel_amount }
  cur_distance = get_distance_from_ore('FUEL')

  while cur_distance > 0:
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

    cur_distance -= 1

  return cur_products['ORE']

ore_needed = 0
fuel_amount = 0
prev_ore_needed = 0
for i in range(5, -1, -1):
  while ore_needed >= prev_ore_needed and ore_needed < 10**12:
    fuel_amount += 10**i
    prev_ore_needed = ore_needed
    ore_needed = get_ore_needed(fuel_amount)

  fuel_amount -= 10**i
  ore_needed = get_ore_needed(fuel_amount)

print(fuel_amount, ore_needed)

