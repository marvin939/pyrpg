import math
from gameobjects.vector2 import Vector2
from gameobjects.vector3 import Vector3
from gameobjects.matrix44 import Matrix44
import pygame as pg
from entity import Entity
from components import GenericPhysicsComponent, InputComponent, PhysicsComponent, AIComponent, SurfaceInfo
import common


class Camera2D(Entity):
    def __init__(self, pos, size, world, speed=200, entity_follow=None):
        """
        Parameters:
            pos - Vector2 indicating where on the screen the camera should render
            size - Size of the camera
            world - World object that the camera will take entities from to render
            speed - Movement speed of the camera
            entity_follow - The entity the camera should follow
        """
        super().__init__(pos, world)

        # self.position = Vector2(pos)
        self.size = Vector2(size)
        self.speed = speed
        self.physics = CameraPhysicsComponent()
        self.input = CameraInputComponent()

        self.world_pos = Vector2()
        self.scale = 1  # [unused]
        # self.rotation = 0  # [unused] Z-rotation degrees
        # self.rotation_speed = 10
        # self.rotation_direction = 0  # -1 to 1

        # self.world = world
        self.entity_follow = entity_follow

        self._current_entity_index = -1

    def get_center(self):
        return Vector2(self.size.x / 2, self.size.y / 2)

    def get_tmatrix(self):
        c = self.get_center()
        tmatrix = Matrix44.identity()
        # tmatrix = Matrix44.z_rotation(math.radians(self.rotation))
        tmatrix.translate += Vector3(-c.x, -c.y, 0)
        tmatrix.translate += Vector3(self.world_pos.x, self.world_pos.y, 0)

        # z_rotation_matrix = Matrix44.z_rotation(math.radians(self.rotation))
        # z_rotation_matrix.invert()
        # tmatrix *= z_rotation_matrix
        # Can't get rotation working :(

        # Working:
        # tmatrix = Matrix44.translation(self.world_pos.x, self.world_pos.y, 0)
        return tmatrix

    def center_on(self, position):
        # self.world_pos = position - self.get_center()
        self.world_pos.x, self.world_pos.y = position.x, position.y

    def handle_event(self, event):
        self.input.handle_event(self, event)

    def screen_to_world(self, pos):
        """Convert screen coordinates (Vector2) to world coordinates (Vector2)"""
        pos = Vector2(pos)
        pos -= self.position
        transformed = self.get_tmatrix().transform(Vector3(pos.x, pos.y, 0))
        return Vector2(transformed[0], transformed[1])

    def world_to_screen(self, pos):
        """Convert world coordinates (Vector2) to screen coordinates (Vector2)"""
        vec2to3 = Vector3(pos.x, pos.y, 0)
        transformed = self.get_tmatrix().get_inverse().transform(vec2to3)  # World to screen
        return Vector2(transformed[0] + self.position.x, transformed[1] + self.position.y)

    def _cycle_entities(self):
        try:
            self._current_entity_index = (self._current_entity_index + 1) % len(self.world.entities)
            return self.world.entities[self._current_entity_index]
        except:
            return self.world.entities[0]

    def update(self, seconds_passed):
        super().update(seconds_passed)

        if self.entity_follow is not None:
            self.center_on(self.entity_follow.position)

    def render(self, surface):
        self._render_bg_rect(surface)
        self._render_entities(surface)
        # print(self.rotation)

    def _render_bg_rect(self, surface):
        pos = (self.position.x, self.position.y)
        size = (self.size.x, self.size.y)
        pg.draw.rect(surface, pg.Color('#2E3436'), (pos, size), )

    def _render_entities(self, screen_surface):
        x_offset, y_offset = self.position.x, self.position.y
        camera_rect = pg.Rect(int(self.world_pos.x), int(self.world_pos.y), int(self.size.x), int(self.size.y))
        for entity in self.world.entities:
            pos = entity.position
            # if not camera_rect.collidepoint(pos):
            #     continue

            ri = entity.render_info()
            if ri is None:
                continue
            surface = ri.surface_info.surface
            offset = ri.surface_info.offset
            world_pos = ri.world_pos #+ render_info.surface_info.offset

            screen_pos = self.world_to_screen(world_pos)

            if self.entity_follow and entity is not self.entity_follow:
                center_relativity = world_pos - self.world_pos
                rotated = common.rotate_vector2(center_relativity, self.entity_follow.rotation.angle)
                screen_pos = self.world_to_screen(self.world_pos + rotated)

            if not ri.follow_rotation:
                screen_pos += offset
            else:
                if self.entity_follow:
                    rotated_si = SurfaceInfo.rotate(ri.surface_info, self.entity_follow.rotation.angle)
                    surface = rotated_si.surface
                    offset = rotated_si.offset
                    screen_pos += offset

            screen_surface.blit(surface, screen_pos)

            # wx = int(render_info.world_pos.x)
            # wy = int(render_info.world_pos.y)
            # wpos = self.world_to_screen(Vector2(wx, wy))
            wx = int(screen_pos.x - offset.x)
            wy = int(screen_pos.y - offset.y)
            wpos = Vector2(wx, wy)
            # pg.draw.circle(screen_surface, pg.Color('green'), (int(wpos.x), int(wpos.y)), 1)
            # pg.draw.line(screen_surface, pg.Color('green'), (int(wpos.x), int(wpos.y)), (int(wpos.x), int(wpos.y + 5)))
            pg.draw.line(screen_surface, pg.Color('grey'), (int(wpos.x) - 5, int(wpos.y) - 5),
                         (int(wpos.x + 5), int(wpos.y + 5)))
            pg.draw.line(screen_surface, pg.Color('grey'), (int(wpos.x) - 5, int(wpos.y) + 5),
                         (int(wpos.x + 5), int(wpos.y - 5)))


class CameraPhysicsComponent(PhysicsComponent):
    def __init__(self):
        super().__init__()
        self.velocity = Vector2()

    def update(self, entity, seconds_elapsed):
        self.velocity = entity.direction * entity.speed
        entity.world_pos += self.velocity * seconds_elapsed
        # entity.rotation += entity.rotation_direction * entity.rotation_speed * seconds_elapsed


class CameraInputComponent(InputComponent):
    def __init__(self):
        super().__init__()
        self.scroll_up_key = pg.K_w
        self.scroll_down_key = pg.K_s
        self.scroll_left_key = pg.K_a
        self.scroll_right_key = pg.K_d
        self.print_center_key = pg.K_c
        self.print_tmatrix_key = pg.K_t
        self.print_position_key = pg.K_p

    def update(self, entity, seconds_passed):
        pressed = pg.key.get_pressed()

        if pressed[self.scroll_up_key]:
            entity.direction.y = -1
        elif pressed[self.scroll_down_key]:
            entity.direction.y = +1
        else:
            entity.direction.y = 0

        if pressed[self.scroll_left_key]:
            entity.direction.x = -1
        elif pressed[self.scroll_down_key]:
            entity.direction.x = +1
        else:
            entity.direction.x = 0

        entity.direction.normalize()

        if pressed[pg.K_q]:
            entity.rotation.direction = -1
        elif pressed[pg.K_e]:
            entity.rotation.direction = 1
        else:
            entity.rotation.direction = 0
        # print(entity.rotation_direction)

    def handle_event(self, camera, event):
        if event.type == pg.KEYDOWN:
            key = event.key

            # Display Info
            if key == self.print_tmatrix_key:
                print('tmatrix:\n', camera.get_tmatrix(), sep='')
            elif key == self.print_center_key:
                print('center:', camera.get_center())
            elif key == self.print_position_key:
                print('position:', camera.world_pos)

            # Swap focus
            # elif key == pg.K_r:
            #     entity = self._cycle_entities()
            #     print('swapped entity to:', entity)
            #     self.center_on(entity.position)

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                print('mouse button down event:', event)

            elif event.button == 2:
                mouse_pos = event.pos
                print('-------------------------------------')
                print('mouse_pos:', mouse_pos)
                print('mouse\'s world location:', camera.screen_to_world(mouse_pos))

            elif event.button == 3:
                camera.center_on(camera.screen_to_world(event.pos))


class CameraAIComponent(AIComponent):
    def __init__(self):
        return