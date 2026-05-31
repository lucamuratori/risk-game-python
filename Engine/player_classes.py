from pydantic import BaseModel


class Player(BaseModel):
    id: int
    name: str
    units: list = []


class Unit(BaseModel):
    level: int = 0
    player: Player

    def level_up(self):
        self.level += 1








if __name__ == "__main__":
    player1 = Player(id=1, name="luca")
    print(player1)
    