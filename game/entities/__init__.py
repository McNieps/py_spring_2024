from game.entities.gummy import Gummy
from game.entities.player import Player
from game.entities.xp_chunk import XPChunk
from game.entities.campfire import Campfire
from game.entities.peanut import Peanut

entities = {"Gummy": Gummy, "Player": Player, "XPChunk": XPChunk, "Campfire": Campfire, "Peanut": Peanut}

__all__ = ["Gummy", "Player", "XPChunk", "entities", "Campfire", "Peanut"]
