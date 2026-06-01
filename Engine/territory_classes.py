import json
import time
from pydantic import BaseModel
from player_classes import Player, Unit


class Continent(BaseModel):
    name: str
    territories: list = []

    def __str__(self):
        return f"Continent: {self.name}; Territories: {self.territories}"


class Territory(BaseModel):
    id: str
    name : str
    adjacent: list = []
    units: list = []
    

    def __str__(self):
        return self.name


            
         






    
