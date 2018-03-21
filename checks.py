def if_enemy_attacking(state):
    for fleet in state.enemy_fleets(): # get list of enemy attacks to our planets
        for planet in state.my_planets():
            if fleet.destination_planet == planet.ID:
                return True
    return False

def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())
