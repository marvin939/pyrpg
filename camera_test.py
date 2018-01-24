import pygame as pg
from gameobjects.vector2 import *
from gameobjects.vector3 import *
from gameobjects.matrix44 import *
import tiles
import sys
import math

from entity import Entity
from world import World
from camera import Camera2D
from playerentity import PlayerEntity

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

FPS = 60


def main():
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption('2D camera test')

    clock = pg.time.Clock()

    world = World()
    camera_margin = (50, 20)
    camera = Camera2D(camera_margin, (SCREEN_WIDTH - camera_margin[0] * 2, SCREEN_HEIGHT - camera_margin[1] * 2), world)
    # camera = Camera2D(Vector2(), (SCREEN_WIDTH, SCREEN_HEIGHT), world)

    dot = Entity(Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    world.add_entity(dot)

    dot2 = Entity(Vector2(SCREEN_WIDTH / 2 + 20, SCREEN_HEIGHT / 2 + 20))
    world.add_entity(dot2)

    dot3 = Entity(Vector2())
    world.add_entity(dot3)

    player_pos = Vector2(dot.position) + Vector2(20, -30)
    player = PlayerEntity(player_pos)
    world.add_entity(player)

    dot4 = Entity(player_pos + Vector2(-50, 50))
    world.add_entity(dot4)
    dot5 = Entity(player_pos + Vector2(50, -50))
    world.add_entity(dot5)

    tile1 = tiles.GroundTileEntity(player_pos, tiles.BRICK_TILE)
    world.add_entity(tile1)

    begin = Vector2(tile1.position)
    x_offset = Vector2(tiles.TILE_SPACING, 0)
    y_offset = Vector2(0, tiles.TILE_SPACING)
    tile2 = tiles.GroundTileEntity(begin, tiles.BRICK_TILE)
    world.add_entity(tile2)
    world.add_entity(tiles.GroundTileEntity(begin + x_offset, tiles.BRICK_TILE))
    world.add_entity(tiles.GroundTileEntity(begin + x_offset * 2, tiles.BRICK_TILE))
    world.add_entity(tiles.GroundTileEntity(begin + x_offset * 2 + y_offset, tiles.BRICK_TILE))

    camera.entity_follow = player

    while True:
        for event in pg.event.get():
            handle_event(event)
            camera.handle_event(event)

        seconds_passed = clock.tick(FPS) / 1000
        world.update(seconds_passed)
        camera.update(seconds_passed)
        # camera.center_on(player.position)

        screen.fill(pg.Color('black'))
        camera.render(screen)
        pg.display.update()


def handle_event(event):
    if event.type == pg.QUIT:
        quit()
    elif event.type == pg.KEYDOWN:
        key = event.key
        if key == pg.K_ESCAPE:
            quit()


def quit():
    print('quitting.')
    pg.quit()
    sys.exit()


if __name__ == '__main__':
    main()