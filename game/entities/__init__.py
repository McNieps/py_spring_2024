from game.entities.blob import Blob
from game.entities.player import Player
from game.entities.xp_chunk import XPChunk
from game.entities.campfire import Campfire

entities = {"Blob": Blob, "Player": Player, "XPChunk": XPChunk, "Campfire": Campfire}

__all__ = ["Blob", "Player", "XPChunk", "entities", "Campfire"]
