#!/usr/bin/env python
#

"""
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn

# You have to improve this tree or create an entire new one that is capable
# of winning against all the 5 opponent bots
def setup_behavior_tree():

    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')

    # Name plans
    offense_plan = Sequence(name='Offense Pattern Hit em Really Hard')
    defense_plan = Sequence(name='Defense Pattern Alpha Atari Omega')
    spread_plan = Sequence(name='Spread Red Menace')

    # Name nodes
    largest_fleet_check = Check(have_largest_fleet)
    attack_weakest = Action(attack_weakest_enemy_planet)

    enemy_attack_check = Check(if_enemy_attacking)
    defense_reinforce = Action(reinforce_defense)

    neutral_planet_check = Check(if_neutral_planet_available)
    spread_to_optimal = Action(spread_to_optimal_neutral_planet)

    # Attach nodes
    offense_plan.child_nodes = [largest_fleet_check, attack_weakest]
    defense_plan.child_nodes = [enemy_attack_check, defense_reinforce]
    spread_plan.child_nodes = [neutral_planet_check, spread_to_optimal]
    root.child_nodes = [offense_plan, defense_plan, spread_plan, attack_weakest.copy()]

    logging.info('\n' + root.tree_to_string())
    return root

# You don't need to change this function
def do_turn(state):
    behavior_tree.execute(planet_wars)

if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")