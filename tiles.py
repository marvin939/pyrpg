from gameobjects.vector2 import Vector2
import pygame as pg
from entity import Entity
from components import GraphicsComponent, RenderInfo, SurfaceInfo


TILE_SIZE = 16  # dimension of square tiles
TILE_SCALING = 2
TILE_OFFSET = Vector2(-TILE_SIZE, -TILE_SIZE) * 0.5
TILE_SPACING = TILE_SIZE * TILE_SCALING


class TileGraphicsComponent(GraphicsComponent):

    def __init__(self, tile_surface):
        super().__init__()
        self.tile_surface_info = SurfaceInfo.scale_surface(tile_surface, TILE_OFFSET, TILE_SCALING)

    def render_info(self, entity):
        ri = RenderInfo()
        ri.surface_info = self.tile_surface_info
        ri.world_pos = entity.position
        ri.follow_rotation = True   # Rotate with the camera
        return ri


BRICK_TILE = TileGraphicsComponent(pg.image.load('data/tile.png'))


class GroundTileEntity(Entity):
    def __init__(self, pos, c_graphics, world=None):
        super().__init__(pos, world, c_graphics=c_graphics)
