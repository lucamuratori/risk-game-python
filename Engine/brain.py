from player_classes import Player, Unit
from territory_classes import Continent, Territory
import json
import random
import time


# Initialization functions begin ------

# Extract adjacency data from json file
with open("./data/risk_realistic_world_adjacency.json", "r") as f:
    adjacency = json.load(f)

# Extract world data from json file
with open("./data/risk_realistic_world_territories.json", "r") as f:
    world = json.load(f)

# Initialize the world
def init_territory():
    continent_list: list = []

    for continent in world.keys():
        # Creates continent
        new_cont: Continent = Continent(name=continent)
        continent_list.append(new_cont)

        for country in world[continent].keys():
            for region in world[continent][country]:
                # Creates territory and adds it to continent
                # Initialize the territory
                new_terr = Territory(id=str(region["id"]), name=region["name"])
                # Adds the territory to the continent
                new_cont.territories.append(new_terr)
                # Fills adjacency list for the territory
                new_terr.adjacent = adjacency[new_terr.id]
    
    print("Territory initialization complete")
    time.sleep(0.5)
    return continent_list

# Initialization functions end ------


# Utility functions begin ------

# Checks adjacency between two territories
def check_adjacency(region1: Territory, region2: Territory) -> bool:
    if region2.id in region1.adjacent:
        return True
    else:
        return False


def battle(unit1: Unit, unit2: Unit):
    # unit1 = attacker, unit2 = defender
    roll1 = random.randint(1, 10) + unit1.level
    roll2 = random.randint(1, 10) + unit2.level
    if roll1 > roll2:
        return unit1
    elif roll2 >= roll1:
        return unit2

    
def move(unit: Unit, start_terr: Territory, end_terr: Territory):
    if check_adjacency(start_terr, end_terr):
        pass