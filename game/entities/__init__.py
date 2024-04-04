from game.entities.blob import Blob
from game.entities.player import Player
from game.entities.xp_chunk import XPChunk

entities = {"Blob": Blob, "Player": Player, "XPChunk": XPChunk}

__all__ = ["Blob", "Player", "XPChunk", "entities"]
