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


def war(from_region: Continent.Country.Region, to_region: Continent.Country.Region):
    if check_adjacency(from_region, to_region):
        # if the owner of the region is the same or the destination region is empty move the troops
        if check_region_owner(from_region) == check_region_owner(to_region) or check_region_units(to_region) == 0:
            number_units = int(input(f"How many troops do you want to move from {from_region.name} to {to_region.name}? "))
            n = 1
            while n <= number_units:
                move(from_region, to_region)
                n += 1
            return True
        
        elif check_region_owner(from_region) != check_region_owner(to_region) and check_region_units(to_region) != 0:
                player1_units = pick_units(from_region)
                player2_units = pick_units(to_region)
                while len(player1_units) != 0 and len(player2_units) != 0:
                    return


# decide the outcome of the battle
def battle(unit1: Player.Army.Division.Unit, 
           unit2: Player.Army.Division.Unit, 
           region1: Continent.Country.Region, 
           region2: Continent.Country.Region
           ) -> bool:

    # Region1 is attacker, region2 is defender
    unit1_roll = dice_roll(unit1) # attacker roll
    unit2_roll = dice_roll(unit2) # defender roll
    print(f"{unit1.division.army.player}'s {unit1.name} rolled: {unit1_roll}")
    print(f"{unit2.division.army.player}'s {unit2.name} rolled: {unit2_roll}")


    if unit1_roll > unit2_roll:
        # level up and remove losing unit
        unit1.level_up()
        remove_unit_from_region(unit2, region2)
        # check if the region becomes empty
        if check_region_units(region2) == 0:

            # ask to move units into the empty region
            move(from_region=region1, to_region=region2)
        return True

    # in case of tie the defender wins
    else:
        # level up and remove losing unit
        unit2.level_up()
        remove_unit_from_region(unit1, region1)
        # check if the region becomes empty
        if check_region_units(region1) == 0:
            # move units into the empty region
            move(from_region=region2, to_region=region1)
        return True

# function to move units from one region to the other 
def move(from_region: Continent.Country.Region, 
                to_region: Continent.Country.Region):
    
    # loop for the choice of unit to move
    while True:
        units = []
        i = 0
        success = False

        # creates a list with all the units in the starting region and prints it
        for key in from_region.units.keys():

            # gets units for each level
            for unit in from_region.units[key]:

                # appends the unit number, name and level
                units.append([i, unit.name, unit.level])
                i += 1
        print(units)

        # ask for the ID of the unit from the print statement
        input_unit_number = int(input(f"pick the ID number of the unit you want to move to {to_region.name}: "))
        # check that the ID is present in the list of units
        if input_unit_number < len(units) and input_unit_number >= 0:

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
                print("The ID number you chose has no match in the list of units")
                continue


# returns the number of units in the region
def check_region_units(region: Continent.Country.Region) -> int:
    units_in_region = 0
    for key in region.units.keys():
        units_in_region += len(region.units[key])
    return units_in_region

# obsolete since the region class has a player variable
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
        print(f"{unit.name} has been removed from {region.name}.")
        region.units[str(unit.level)].remove(unit)
        return unit
    
    else:
        print("Unit not found.")
        return False


# add unit to a specific region
def add_unit_to_region(unit: Player.Army.Division.Unit, region: Continent.Country.Region):
    region.units[str(unit.level)].append(unit)
    print(f"{unit.name} has been added to {region.name}")
    if region.player != unit.division.army.player:
        region.player = unit.division.army.player
        print(f"{region.name} is now owned by {region.player.name}")


# pick units that will fight
def pick_units(region: Continent.Country.Region) -> list:
    units: list = []
    units_chosen: list = []
    i: int = 0
    success = False

    # creates the list of units available in the region
    for key in region.units.keys():

        for unit in region.units[key]:

            # append unit to the units list with [ID, unit]
            units.append([i, unit])
            i += 1

    while True:
        if region.player is not None:
            input_number = int(input(f"{region.player.name} choose the number of units you want to use in the battle. (maximum {len(units)}): "))
        
            # check that the number is between the minimum and maximum allowed
            if input_number > len(units) or input_number < 0:
                print("The number you chose is outside the bounds of the units IDs.")
                continue
            
            # if the number of units chosen is 0, exit combat
            if input_number == 0:
                print("You chose 0 units, exiting combat.")
                break
            
            # loop through the units for a "chosen n of units" times
            for n in range(input_number):
                
                # prints the list of units available in the region
                for unit in units:
                    print(unit[0], unit[1].name, unit[1].level)

                # asks for the id (unit[0]) of the unit
                unit_input = int(input("Choose the id number of the unit as seen in the list: "))

                # make sure the input number is between the minimum id number and the maximum length of units
                if unit_input < len(units) and unit_input >= units[0][0]:
                    
                    # loop through the units to find the one with the input id
                    for unit in units:
                        if unit[0] == unit_input:
                            units.remove(unit)
                            units_chosen.append(unit)
                            break
            break
    return units_chosen


# creates a list of all region under a player control
def region_list(player, continents) -> list:
    player_regions = []

    for continent in continents:
        for country in continent.countries:
            for region in country.regions:
                if region.player == player:
                    player_regions.append(region)
    
    return player_regions

if __name__ == "__main__":
    player1, player2, continents = init_players_territory()
    player1_regions = region_list(player1, continents)
    player2_regions = region_list(player2, continents)
    player1.first_army.divisions[0].train_units(5)
    print(player1)