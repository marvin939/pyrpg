import pygame as pg
from gameobjects.vector2 import Vector2
from components import NullGraphicsComponent, NullPhysicsComponent, NullInputComponent, NullAIComponent, \
    NullRotationComponent


class Entity:
    def __init__(self, pos, world=None,
                 c_input=None,
                 c_ai=None,
                 c_physics=None,
                 c_graphics=None,
                 c_rotation=None):
        self.position = Vector2(pos)
        self.direction = Vector2()
        self.speed = 0
        self.world = world

        self.input = NullInputComponent() if c_input is None else c_input
        self.ai = NullAIComponent() if c_ai is None else c_ai
        self.physics = NullPhysicsComponent() if c_physics is None else c_physics
        self.graphics = NullGraphicsComponent() if c_graphics is None else c_graphics
        self.rotation = NullRotationComponent() if c_rotation is None else c_rotation

    def update(self, seconds_elapsed):
        self._update_components(seconds_elapsed)

    def _update_components(self, seconds_elapsed):
        self.input.update(self, seconds_elapsed)
        self.rotation.update(self, seconds_elapsed)
        self.ai.update(self, seconds_elapsed)
        self.physics.update(self, seconds_elapsed)
        self.graphics.update(self)

    def render(self, surface):
        return

    def render_info(self):
        return self.graphics.render_info(self)
