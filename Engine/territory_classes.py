import json




class Continent:
    def __init__(self, name: str) -> None:
        self.countries: set[Continent.Country] = set() # set of countries in the continent
        self.name: str = name # name of the continent

    def __repr__(self) -> str:
        message = "\n".join([country.name for country in self.countries])
        message = ":\n".join([self.name, message])
        return message + "\n-------"
    
    # Initialize the country and assigns it to the continent
    def new_country(self, name):
        country = self.Country(self, name)
        self.countries.add(country)
        return country
    
    
    class Country:
        def __init__(self, continent, name) -> None:
            self.regions: set[Continent.Country.Region] = set() # set of regions in the country
            self.name: str = name # name of the country
            self.continent: Continent = continent # Continent parent of the country
        
        def __repr__(self) -> str:
            message = "\n".join([region.name for region in self.regions])
            message = ":\n".join([self.name, message])
            return message
        
        # Initialize a region and assigns it to the country
        def new_region(self, name, id):
            region = self.Region(name, self, id)
            self.regions.add(region)
        
        
        class Region:
            def __init__(self, name: str, country, id: int) -> None:
                self.name: str = name # name of the region
                self.id: int = id # id of the region
                self.units: dict = {"1": [], "2": [], "3": [], "4": [], "5": []} # dictionary with lists of units in the region
                self.country: Continent.Country = country # parent country
            
            def __repr__(self) -> str:
                return self.name
            

def init_territory():
    continent_list = []
    # extracts region data (name, continent, country, id)
    with open("./data/risk_realistic_world_territories.json", "r") as f:
        data = json.load(f)

    for continent in data.keys():
        # Creates continent
        new_cont: Continent = Continent(continent)
        continent_list.append(new_cont)

        for country in data[continent].keys():
            # Creates country and adds it to continent
            new_country: Continent.Country = new_cont.new_country(country)

            for region in data[continent][country]:
                # creates region and adds it to country
                new_country.new_region(region["name"], region["id"])
    
    print("Territory initialization complete")
    return continent_list


def check_adjacency():
    with open("./data/risk_realistic_world_adjacency.json", "r") as f:
        data = json.load(f)

    




if __name__ == "__main__":
    # continent_list = init_territory()
    # for continent in continent_list:
    #     print(continent)
    with open("./data/risk_realistic_world_adjacency.json") as f:
        data = json.load(f)
    for id in data.keys():
        print(id)
            
