import pymunk

from isec.environment.position.pymunk_pos import PymunkShapeInfo


__all__ = ["PlayerShapeInfo", "TerrainShapeInfo", "EnemyShapeInfo"]


_collision_masks_input = {"PLAYER": ["TERRAIN", "ENEMY"],
                          "TERRAIN": ["*"],
                          "ENEMY": ["ENEMY", "PLAYER"],
                          "ETHEREAL": ["TERRAIN"]}


_collision_types = {key: i for i, key in enumerate(_collision_masks_input)}
_collision_categories = {collision_type: 2**i for i, collision_type in enumerate(_collision_types)}
_collision_masks = {}
for mask_input in _collision_masks_input:
    mask = 0
    for collision_type in _collision_masks_input[mask_input]:
        if collision_type == "*":
            mask = 0xFFFFFFFF
            break

        mask |= _collision_categories[collision_type]
    _collision_masks[mask_input] = mask


class PlayerShapeInfo(PymunkShapeInfo):
    collision_type: int = 0
    collision_category: int = _collision_categories["PLAYER"]
    collision_mask: int = _collision_masks["PLAYER"]
    shape_filter: pymunk.ShapeFilter = pymunk.ShapeFilter(group=collision_type,
                                                          categories=collision_category,
                                                          mask=collision_mask)

    elasticity: float = 0
    friction: float = 0
    density: float = 0
    sensor: bool = False


class TerrainShapeInfo(PymunkShapeInfo):
    collision_type: int = 1
    collision_category: int = _collision_categories["TERRAIN"]
    collision_mask: int = _collision_masks["TERRAIN"]
    shape_filter: pymunk.ShapeFilter = pymunk.ShapeFilter(group=collision_type,
                                                          categories=collision_category,
                                                          mask=collision_mask)

    elasticity: float = 0
    friction: float = 0
    density: float = 0
    sensor: bool = False


class EnemyShapeInfo(PymunkShapeInfo):
    collision_type: int = 0
    collision_category: int = _collision_categories["ENEMY"]
    collision_mask: int = _collision_masks["ENEMY"]
    shape_filter: pymunk.ShapeFilter = pymunk.ShapeFilter(group=collision_type,
                                                          categories=collision_category,
                                                          mask=collision_mask)

    elasticity: float = 0
    friction: float = 0
    density: float = 0
    sensor: bool = False


class EtherealPlayerShapeInfo(PymunkShapeInfo):
    collision_type: int = 3
    collision_category: int = _collision_categories["ETHEREAL"]
    collision_mask: int = _collision_masks["ETHEREAL"]
    shape_filter: pymunk.ShapeFilter = pymunk.ShapeFilter(group=collision_type,
                                                          categories=collision_category,
                                                          mask=collision_mask)

    elasticity: float = 0
    friction: float = 0
    density: float = 0
    sensor: bool = False
