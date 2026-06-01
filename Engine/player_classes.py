from uuid import uuid4
from pydantic import BaseModel, PrivateAttr, computed_field


class Player(BaseModel):
    _id: str = PrivateAttr(default_factory=lambda: str(uuid4())) 
    name: str
    units: list = []

    @computed_field
    @property
    def item_id(self) -> str:
        return self._id


class Unit(BaseModel):
    _id: str = PrivateAttr(default_factory=lambda: str(uuid4()))
    level: int = 0
    player: Player

    @computed_field
    @property
    def item_id(self) -> str:
        return self._id

    def level_up(self):
        self.level += 1



if __name__ == "__main__":
    player1 = Player(name="TestPlayer")
    print(player1)
    