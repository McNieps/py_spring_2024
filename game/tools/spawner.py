from game.entities.base_enemy import BaseEnemy
from game.entities.blob import Blob


enemy_dict = {"Blob": Blob}


class Spawner:
    def __init__(self,
                 waves_dict: dict) -> None:

        self.waves_dict = waves_dict
        self.last_spawn = 0

    def update(self,
               delta: float) -> list[BaseEnemy]:

        pass
        # print(self.waves_dict)
