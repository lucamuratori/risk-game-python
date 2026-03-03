from player_classes import Player, init_players
from territory_classes import Continent, init_territory, check_adjacency
import random



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
def battle(unit1: Player.Army.Division.Unit, 
           unit2: Player.Army.Division.Unit, 
           region1: Continent.Country.Region, 
           region2: Continent.Country.Region
           ):
    if check_adjacency(region1, region2):
        # Region1 is attacker, region2 is defender
        unit1_roll = dice_roll(unit1) # attacker roll
        unit2_roll = dice_roll(unit2) # defender roll
        units_left = 0

        if unit1_roll > unit2_roll:
            unit1.level_up()

            # check if the region becomes empty
            if check_region_units(region2) == 0:

                # ask to move units into the empty region
                ask_to_move(from_region=region1, to_region=region2)
            return True
        
        else:

            # in case of tie the defender wins
            unit2.level_up()
            return True
    else:
        return False

def ask_to_move(from_region: Continent.Country.Region, 
                to_region: Continent.Country.Region):
    
    if check_possible_movement(from_region, to_region):    
        units = []
        i = 0
        success = False

        # creates a list with all the units in the region and prints it
        for key in from_region.units.keys():

            # gets units for each level
            for unit in from_region.units[key]:

                # appends the unit number, name and level
                units.append([i, unit.name, unit.level])
                i += 1
        
        print(units)

        # loop for the choice of unit to move
        while True:
            # ask for the number of the unit from the print statement
            input_unit_number = int(input("pick the number of the unit you want to move to the region."))

            # find the unit with the matching number in the list
            for unit in units:

                # match the unit number with the input number
                if unit[0] == input_unit_number:

                    unit_list_level: list = from_region.units[str(unit[2])]
                    for full_unit in unit_list_level:

                        # check if the name of the unit matches one of the units in the region
                        if unit[1] == full_unit.name:

                            # remove unit from the starting region
                            remove_unit_from_region(full_unit, from_region)

                            # add the unit to the final region
                            add_unit_to_region(full_unit, to_region)

                            success = True
                            print(f"{full_unit.name} moved from {from_region.name} to {to_region.name}")
                            break
                        else:
                            continue
                
                if success:
                    break
                else:
                    continue
            
            if success:
                break
            else:
                print("The number you chose has no match in the list of units")
                continue


# returns the number of units in the region
def check_region_units(region: Continent.Country.Region) -> int:
    units_in_region = 0
    for key in region.units.keys():
        units_in_region += len(region.units[key])
    return units_in_region


def check_region_owner(region: Continent.Country.Region) -> Player | None:
        # gets the player owning the region
        for key in region.units.keys():
            if len(region.units[key]) != 0:
                player: Player = region.units[key][0].division.army.player
                return player
            

# check if movement is possible between two regions
def check_possible_movement(from_region: Continent.Country.Region, to_region: Continent.Country.Region) -> bool:
    adjacency = check_adjacency(from_region, to_region)
    if check_region_owner(from_region) == check_region_owner(to_region):
        if adjacency:
            return True
        else:
            return False
    elif check_region_units(to_region) == 0:
        if adjacency:
            return True
        else:
            return False
    else:
        return False
        
            
    


# remove the unit from the region and return it
def remove_unit_from_region(unit: Player.Army.Division.Unit, 
                            region: Continent.Country.Region) -> Player.Army.Division.Unit | bool:
    if unit in region.units[str(unit.level)]:

        region.units[str(unit.level)].remove(unit)
        return unit
    
    else:
        print("Unit not found.")
        return False


# add unit to a specific region
def add_unit_to_region(unit: Player.Army.Division.Unit, region: Continent.Country.Region):
    region.units[str(unit.level)].append(unit)

    

if __name__ == "__main__":
    player1, player2, continents = init_players_territory()
    