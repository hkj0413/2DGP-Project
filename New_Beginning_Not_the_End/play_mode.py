from pico2d import *

import game_framework

import game_world

import server

from ground import Ground
from wall import Wall
from ladder import Ladder
from character import Character
from ui import UI
from background import Background

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            server.character.handle_event(event)

def init():
    global character

    server.background = Background()
    game_world.add_object(server.background, 0)

    # 캐릭터
    server.character = Character()
    game_world.add_object(server.character, 1)

    ui = UI()
    game_world.add_object(ui, 3)

    # 사다리
    game_world.add_collision_pairs('server.character:ladder', server.character, None)

    ladder_positions = [
        (range(3, 15), 39),
    ]

    for i_range, j in ladder_positions:
        ladders = [Ladder(j, i, 3, 0) for i in i_range]
        game_world.add_objects(ladders, 0)
        for ladder in ladders:
            game_world.add_collision_pairs('server.character:ladder', None, ladder)


    # a, d 판정만 있는 블럭
    game_world.add_collision_pairs('server.character:wall', server.character, None)

    wall_positions = [
        (range(3, 12), 29),
    ]

    for i_range, j in wall_positions:
        walls = [Wall(j, i, 2, 0) for i in i_range]
        game_world.add_objects(walls, 0)
        for wall in walls:
            game_world.add_collision_pairs('server.character:wall', None, wall)

    wall_positions = [
        (1, range(0, 30)),
        (1, range(35, 44)),
        (1, range(50, 109)),
        (0, range(0, 30)),
        (0, range(35, 44)),
        (0, range(50, 109)),
    ]

    for j, i_range in wall_positions:
        walls = [Wall(i, j, 0, 0) for i in i_range]
        game_world.add_objects(walls, 0)
        for wall in walls:
            game_world.add_collision_pairs('server.character:wall', None, wall)

    # a, d, 점프, 추락 판정이 있는 블럭
    game_world.add_collision_pairs('server.character:ground', server.character, None)

    ground_positions = [
        (13, range(13, 21)),
        (12, range(26, 30)),
        (11, range(2, 4)),
        (9, range(6, 8)),
        (7, range(11, 16)),
        (5, range(19, 26)),
        (2, range(0, 30)),
        (2, range(35, 44)),
        (2, range(50, 109)),
    ]

    for j, i_range in ground_positions:
        grounds = [Ground(i, j, 1, 0) for i in i_range]
        game_world.add_objects(grounds, 0)
        for ground in grounds:
            game_world.add_collision_pairs('server.character:ground', None, ground)

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

