from player_classes import Player, init_players
from territory_classes import Continent, init_territory
import random


ACTIONS_PER_TURN = 3

# Initialize both players and territories
def init_players_territory():
    name1 = input("insert the name of the first player: ")
    name2 = input("insert the name of the second player: ")
    player1, player2 = init_players(name1, name2)
    continents = init_territory()
    return player1, player2, continents

# function that returns the number rolled plus the unit bonus
def dice_roll(unit: Player.Army.Division.Unit) -> int:
    return random.randint(1, 10) + unit.bonus

# decide the outcome of the battle
def battle(unit1: Player.Army.Division.Unit, unit2: Player.Army.Division.Unit):
    unit1_roll = dice_roll(unit1) # attacker roll
    unit2_roll = dice_roll(unit2) # defender roll
    if unit1_roll > unit2_roll:
        return unit1.level_up()
    else:
        # in case of tie the defender wins
        return unit2.level_up()
    

if __name__ == "__main__":
    player1, player2, continents = init_players_territory()
    