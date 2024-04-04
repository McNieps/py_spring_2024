import typing

from isec.app import Resource
from isec.environment import EntityScene, Entity, Sprite, Pos

from game.gui.xp_bar import XPBar
from game.gui.health_bar import HealthBar

if typing.TYPE_CHECKING:
    from game.utils import Level


class GUI(EntityScene):
    def __init__(self,
                 level: "Level"):
        super().__init__(fps=Resource.data["instance"]["game"]["fps"])
        self.level = level

        frame = Entity(Pos(), Sprite(Resource.image["gui"]["frame"], position_anchor="topleft"))
        self.add_entities(XPBar(self.level.player), HealthBar(self.level.player), frame)

    def update(self,
               _delta: float = 0) -> None:
        super().update(_delta)
