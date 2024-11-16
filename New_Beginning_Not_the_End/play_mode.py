import random

from pico2d import *

import game_framework

import game_world
from ground import Ground
from wall import Wall
from character import Character

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            character.handle_event(event)

def init():
    global character

    # 캐릭터
    character = Character()
    game_world.add_object(character, 1)

    # a, d 판정만 있는 블럭
    game_world.add_collision_pairs('character:wall', character, None)

    wall_positions = [
        (range(3, 12), 29),
    ]

    for i_range, j in wall_positions:
        walls = [Wall(j, i, 2) for i in i_range]
        game_world.add_objects(walls, 0)
        for wall in walls:
            game_world.add_collision_pairs('character:wall', None, wall)

    wall_positions = [
        (1, range(0, 30)),
        (0, range(0, 30)),
    ]

    for j, i_range in wall_positions:
        walls = [Wall(i, j, 0) for i in i_range]
        game_world.add_objects(walls, 0)
        for wall in walls:
            game_world.add_collision_pairs('character:wall', None, wall)

    # a, d, 점프, 추락 판정이 있는 블럭
    game_world.add_collision_pairs('character:ground', character, None)

    ground_positions = [
        (13, range(13, 21)),
        (12, range(26, 30)),
        (11, range(2, 4)),
        (9, range(6, 8)),
        (7, range(11, 16)),
        (5, range(19, 26)),
        (2, range(0, 30)),
    ]

    for j, i_range in ground_positions:
        grounds = [Ground(i, j, 1) for i in i_range]
        game_world.add_objects(grounds, 0)
        for ground in grounds:
            game_world.add_collision_pairs('character:ground', None, ground)

def finish():
    game_world.clear()
    pass

def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

