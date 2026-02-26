import time


# PLAYER CLASS AND METHODS
class Player:
    def __init__(self, name) -> None:
        self.name: str = name # sets the name of the player
        print(f"Player {self.name} created")
        time.sleep(1)
        self.first_army: Player.Army = self.Army(self) # initialize the first army
        self.armies: dict[str, Player.Army] = {"1": self.first_army} # creates a dictionary to hold the armies of the player
        self.first_army.name_army()
        time.sleep(1.5)
        self.first_army.create_division()
        time.sleep(1.5)
        self.first_army.divisions[0].train_units(1) # trains the first unit, the first division for the first army
        
    
    def __repr__(self) -> str:
        message = ""
        for army in self.armies.values():
            message = "\n".join([message, army.name])
            for division in army.divisions:
                message = "\n".join([message, str(division)])
        return message
    # Creates a new army for the player in a specific region
    def new_army(self):
        army = self.Army(self)
        self.armies[str(len(self.armies) + 1)] = army
        print(f"Army #{len(self.armies)} created.")
    
    # ARMY CLASS AND METHODS
    class Army:
        def __init__(self, player):
            self.player: Player = player
            self.name: str = ""
            self.divisions: list[Player.Army.Division] = [] # creates a list to hold the divisions of the army
            
        
        def __repr__(self) -> str:
            message = "Divisions:\n" + " ".join([division.name for division in self.divisions])
            return message
        
        def name_army(self) -> None:
            self.name = " ".join(["Army #", str(len(self.player.armies))])
        # Creates a division if there are less than 3 in the army
        def create_division(self):
            if len(self.divisions) == 3:
                print("You reached the maximum number of divisions in this army, create another army to add more divisions")
                return
            name = " ".join([self.get_division_name(), "Division"])
            self.divisions.append(self.Division(name, self))
            print(f"{name} created successfully")
        
        # function to get the division number as string once they it gets created
        def get_division_name(self) -> str:
            final_n = len(self.divisions) + 1
            if final_n == 1:
                n = "".join([str(final_n), "st"])
            elif final_n == 2:
                n = "".join([str(final_n), "nd"])
            else:
                n = "".join([str(final_n), "rd"])
            return n

        # DIVISION CLASS AND METHODS
        class Division:
            def __init__(self, name, army) -> None:
                self.name: str = name
                self.units: dict[str, list[Player.Army.Division.Unit]] = {"1": [], "2": [], "3": [], "4": [], "5": []}
                self.army = army
            
            def __repr__(self) -> str:
                one = [unit.name for unit in self.units["1"]]
                two = [unit.name for unit in self.units["2"]]
                three = [unit.name for unit in self.units["3"]]
                four = [unit.name for unit in self.units["4"]]
                five = [unit.name for unit in self.units["5"]]
                message = "\n".join([self.name, "Level 1 Units:", str(one), "Level 2 Units:", str(two), "Level 3 Units:", str(three),
                                     "Level 4 Units:", str(four), "Level 5 Units:", str(five)])
                return message

            # Train units and add them to the division
            def train_units(self, n: int):
                # gets the number of units currently in the division
                n_units = sum([len(value) for value in self.units.values()])
                # Checks that there are no more than 10 Battallions in each Division
                if n_units == 10:
                    print("You reached the maximum number of batallions in this division, create another division to add one.")
                    return
                # Checks that the number of units to train plus the units already trained are not > 10
                if n_units + n > 10:
                    print("You reached the maximum number of battalions in this division.")
                    time.sleep(0.5)
                    print(f"You can only train {10 - n_units} Battalions in this division.")
                    time.sleep(0.5)
                    print("Training...")
                    time.sleep(1.5)
                    for i in range(10 - n_units):
                        new_unit: Player.Army.Division.Unit = self.Unit(self)
                        self.units["1"].append(new_unit)
                        time.sleep(0.5)
                        print(f"{new_unit.name} trained.")
                    print("Training complete.")
                    
                else:
                    print("Training...")
                    for i in range(n):
                        new_unit: Player.Army.Division.Unit = self.Unit(self)
                        self.units["1"].append(new_unit)
                        time.sleep(0.5)
                        print(f"{new_unit.name} trained.")
                    print("Training complete.")


            # UNIT CLASS AND METHODS
            class Unit:
                def __init__(self, division) -> None:
                    self.level: int = 1
                    self.bonus: int = 0
                    self.division: Player.Army.Division = division
                    self.name = " ".join([f"{self.get_unit_number()}", "Battalion"])
                
                def __repr__(self) -> str:
                    return f"Unit level: {self.level}, part of division: {self.division.name}"
                
                # level up the unit when they win a battle
                def level_up(self):
                    if self.level < 5:
                        self.division.units[str(self.level)].remove(self)
                        self.bonus += 1
                        self.level += 1
                        self.division.units[str(self.level)].append(self)
                        
                    else: return
                
                # function to get the unit number as string once they get trained
                def get_unit_number(self) -> str:
                    # gets the number of units in the current division
                    n_units = sum([len(value) for value in self.division.units.values()])
                    final_n = n_units + 1
                    if final_n == 1:
                        n = "".join([str(final_n), "st"])
                    elif final_n == 2:
                        n = "".join([str(final_n), "nd"])
                    elif final_n == 3:
                        n = "".join([str(final_n), "rd"])
                    else:
                        n = "".join([str(final_n), "th"])
                    return n

def init_players(name1, name2):
    player1 = Player(name1)
    player2 = Player(name2)
    return player1, player2


if __name__ == "__main__":
    player1 = Player("luca")
    player1.armies["1"].divisions[0].train_units(4)
    print(player1)
    