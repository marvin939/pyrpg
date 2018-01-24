import pygame as pg
import common
from gameobjects.vector2 import Vector2


class PhysicsComponent:
    def __init__(self):
        return

    def update(self, entity, seconds_elapsed):
        return


class GenericPhysicsComponent(PhysicsComponent):
    def __init__(self):
        self.velocity = Vector2()
        self.acceleration = Vector2()
        self.inverse_mass = 1 / 10

    def update(self, entity, seconds_elapsed):
        self.acceleration = self.velocity * -0.8
        self.velocity = entity.direction * entity.speed
        self.velocity += self.acceleration * seconds_elapsed
        entity.position += self.velocity * seconds_elapsed


class RenderInfo:
    def __init__(self):
        self.surface_info = None
        self.world_pos = None
        self.follow_rotation = False

    def image_pos(self):
        return self.world_pos + self.surface_info.offset


class SurfaceInfo:
    def __init__(self):
        self.surface = None
        self.offset = Vector2()

    @staticmethod
    def create(surface, offset):
        si = SurfaceInfo()
        si.surface = surface
        si.offset = offset
        return si

    @staticmethod
    def scale_surface(surface, offset, scale):
        new_size = Vector2(surface.get_size()) * scale
        new_surface = pg.transform.scale(surface, (int(new_size.x), int(new_size.y)))
        new_offset = offset * scale
        return SurfaceInfo.create(new_surface, new_offset)

    @staticmethod
    def scale(surface_info, scale):
        return SurfaceInfo.scale_surface(surface_info.surface, surface_info.offset, scale)

    @staticmethod
    def rotate(surface_info, degrees):
        center_vec = Vector2(surface_info.surface.get_rect().center)
        points_diff = surface_info.offset + center_vec  # offset is -ive already, so just add it

        rotated_surf = pg.transform.rotate(surface_info.surface, -degrees)
        rotated_surf_center = Vector2(rotated_surf.get_rect().center)
        rotated_points_diff = common.rotate_vector2(points_diff, degrees)

        offset = -(rotated_surf_center + rotated_points_diff)
        # ^ re-add both components and * -1 to make offset easier to use (outer functions just add it)

        return SurfaceInfo.create(rotated_surf, offset)

    @staticmethod
    def derive_offset_rotated_surface(original_si, rotated_surf, degrees):
        """
        Calculates the offset of an already rotated image using its original SurfaceInfo and the
        angle it was rotated.

        This is useful when you don't want to waste memory and clock cycles re-rotating dozens of surfaces
        when an existing rotated surface has already been provided.
        """

        center_vec = Vector2(original_si.surface.get_rect().center)
        points_diff = original_si.offset + center_vec  # offset is -ive already, so just add it

        rotated_surf_center = Vector2(rotated_surf.get_rect().center)
        rotated_points_diff = common.rotate_vector2(points_diff, degrees)

        offset = -(rotated_surf_center + rotated_points_diff)
        # ^ re-add both components and * -1 to make offset easier to use (outer functions just add it)

        return offset


class GraphicsComponent:
    def __init__(self):
        return

    def update(self, entity):
        return

    def render_info(self, entity):
        return



    @staticmethod
    def _rotate_surface(surface, offset, degrees):
        si = SurfaceInfo()
        rotated = pg.transform.rotate(surface, degrees)


class InputComponent:
    def __init__(self):
        return

    def update(self, entity, seconds_elapsed):
        return


class AIComponent:
    def __init__(self):
        return

    def update(self, entity, seconds_elapsed):
        return


class RotationComponent:
    def __init__(self):
        self.angle = 0
        self.rate = 0
        self.direction = 0

    def update(self, entity, seconds_elapsed):
        self.angle += self.direction * self.rate * seconds_elapsed


class NullRotationComponent(RotationComponent):
    def __init__(self):
        super().__init__()

    def update(self, entity, seconds_elapsed):
        return


class NullPhysicsComponent(PhysicsComponent):
    def __init__(self):
        super().__init__()

    def update(self, entity, seconds_elapsed):
        return


class NullGraphicsComponent(GraphicsComponent):
    _DUMMY_SURFACE_SIZE = Vector2(32, 32)
    _DUMMY_SURFACE_OFFSET = Vector2(-16, -32)
    _DUMMY_SURFACE = pg.Surface((32, 32))
    _DUMMY_SURFACE.fill(pg.Color('white'))

    def __init__(self):
        super().__init__()

    def render_info(self, entity):
        ri = RenderInfo()
        ri.surface_info = SurfaceInfo.create(self._DUMMY_SURFACE, self._DUMMY_SURFACE_OFFSET)
        ri.world_pos = entity.position
        return ri


class NullInputComponent(InputComponent):
    def __init__(self):
        super().__init__()


class NullAIComponent(AIComponent):
    def __init__(self):
        super().__init__()
