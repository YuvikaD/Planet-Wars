import sys, logging
sys.path.insert(0, '../')
from planet_wars import issue_order
from math import sqrt

def reinforce_defense(state):

    enemy_attacks = [fleet for fleet in state.enemy_fleets() # get list of enemy attacks to our planets
                     if any(fleet.destination_planet == planet.ID for planet in state.my_planets())]

    for attacking_fleet in enemy_attacks: # for each enemy fleet

        target_planet = None # get destination planet of fleet
        for planet in state.my_planets():
            if planet.ID is attacking_fleet.destination_planet:
                target_planet = planet
                break

        if target_planet is not None: # if we get the target_planet successfully

            if not (any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())):

                ship_difference = attacking_fleet.num_ships - (target_planet.num_ships * planet.growth_rate)
                if ship_difference > 0: # if fleet can take the planet
                    for planet in state.my_planets(): # for each planet we own
                        if planet.ID is not attacking_fleet.destination_planet: # check if current planet is not the one being attacked
                            if state.distance(planet.ID, target_planet.ID) <= attacking_fleet.turns_remaining: # check if current planet can reach target planet in time
                                if planet.num_ships > ship_difference:
                                    return issue_order(state, planet.ID, target_planet.ID, ship_difference)

    return False

# ===================================================================================================================

def attack_weakest_enemy_planet(state):

    weakest_planets = [planet for planet in state.enemy_planets()
                        if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    weakest_planets.sort(key=lambda p: p.num_ships)

    if not weakest_planets: # check if we have a legal source
        return False

    our_planets = [planet for planet in state.my_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.enemy_fleets())]
    our_planets.sort(key=lambda our_planet: state.distance(weakest_planets[0].ID, our_planet.ID))

    if len(our_planets) == 0:
        return False

    for i in range(len(our_planets)): # for each of our planets, sorted by army
        required_ships = weakest_planets[0].num_ships + \
            state.distance(our_planets[i].ID, weakest_planets[0].ID) * weakest_planets[0].growth_rate + 1
        if our_planets[i].num_ships > required_ships:
            return issue_order(state, our_planets[i].ID, weakest_planets[0].ID, required_ships)

    return False

# ===================================================================================================================

def spread_to_optimal_neutral_planet(state):

    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet: # check if we have a legal source
        return False

    weakest_planets = [planet for planet in state.neutral_planets() # get and sort weakest planets
                        if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    weakest_planets.sort(key=lambda p: p.num_ships)

    closest_planets = [planet for planet in state.neutral_planets()
                        if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    closest_planets.sort(key=lambda closest_planet: state.distance(strongest_planet.ID, closest_planet.ID))
    del closest_planets[5:]

    for i in range(len(weakest_planets)): # for each neutral planet, sorted by army
        if not i > int(len(weakest_planets)):
            if weakest_planets[i] in closest_planets:
                required_ships = weakest_planets[i].num_ships + 1
                if strongest_planet.num_ships > required_ships:
                    return issue_order(state, strongest_planet.ID, weakest_planets[i].ID, required_ships)

    return False