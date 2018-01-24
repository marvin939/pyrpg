import math
from gameobjects.matrix44 import Matrix44
from entity import Entity
from gameobjects.vector3 import Vector3
from gameobjects.vector2 import Vector2
from components import GenericPhysicsComponent, GraphicsComponent, InputComponent, SurfaceInfo, RenderInfo, \
    RotationComponent
import pygame as pg


class PlayerEntity(Entity):
    def __init__(self, pos, world=None):
        super().__init__(pos, world)
        self.input = PlayerInputComponent()
        self.physics = PlayerPhysicsComponent()
        self.graphics = PlayerGraphicsComponent()
        self.rotation = PlayerRotationComponent()

        self.rotation.rate = 100
        self.speed = 100

    def update(self, seconds_elapsed):
        super().update(seconds_elapsed)
        # print('p angle:', self.rotation.angle)
        # print('p rot dir:', self.rotation.direction)
        # self.rotation.update(self, seconds_elapsed)
        # self.direction.x, self.direction.y = 0, 0
        # print(self.position)

    def render_info(self):
        return self.graphics.render_info(self)


class PlayerPhysicsComponent(GenericPhysicsComponent):
    def __init__(self):
        super().__init__()

    def update(self, entity, seconds_elapsed):
        super().update(entity, seconds_elapsed)

    # print('entity.rotation:', entity.rotation)


class PlayerRotationComponent(RotationComponent):
    def __init__(self):
        super().__init__()

    def update(self, entity, seconds_elapsed):
        # print('updating rotation component', 'rate:', self.rate)
        super().update(entity, seconds_elapsed)


class PlayerGraphicsComponent(GraphicsComponent):
    def __init__(self):
        super().__init__()
        self.SCALING_FACTOR = 2
        self._surface_idle = None
        self._initialise_surfaces()

    def _initialise_surfaces(self):
        idle = SurfaceInfo()
        idle_surface = pg.image.load('data/player.png').convert_alpha()
        idle_offset = Vector2(-8, -16)
        idle_si = SurfaceInfo.scale_surface(idle_surface, idle_offset, self.SCALING_FACTOR)
        self._surface_idle = idle_si

    def update(self, entity):
        # print(entity.rotation.angle)
        return

    def render_info(self, entity):
        ri = RenderInfo()
        ri.surface_info = self._surface_idle
        ri.world_pos = Vector2(entity.position)
        ri.follow_rotation = False
        return ri


class PlayerInputComponent(InputComponent):
    def __init__(self):
        super().__init__()

    def update(self, entity, seconds_elapsed):
        pressed = pg.key.get_pressed()

        if pressed[pg.K_UP]:
            entity.direction.y = -1
        elif pressed[pg.K_DOWN]:
            entity.direction.y = +1
        else:
            entity.direction.y = 0

        if pressed[pg.K_LEFT]:
            entity.direction.x = -1
        elif pressed[pg.K_RIGHT]:
            entity.direction.x = +1
        else:
            entity.direction.x = 0

        if entity.direction.get_length() > 0:   # avoid DIV/ZERO by ensuring that there is direction
            # Correct the direction based on the entity's angle
            rmatrix = Matrix44.z_rotation(math.radians(-entity.rotation.angle))
            normalized = entity.direction.get_normalized()
            rotated_direction = rmatrix.transform_vec3(Vector3(normalized.x, normalized.y, 0))
            entity.direction.x = rotated_direction.x
            entity.direction.y = rotated_direction.y

        # entity.direction.normalize()

        if pressed[pg.K_j]:
            entity.rotation.direction = -1
        elif pressed[pg.K_k]:
            entity.rotation.direction = +1
        else:
            entity.rotation.direction = 0
