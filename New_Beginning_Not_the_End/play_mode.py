from pico2d import *

import game_framework
import game_world
import server

from ground import Ground
from wall import Wall
from ladder import Ladder
from character import Character
from ui import UI
from coconut import Coconut
from heal import Heal
from background import Background
from spore import Spore
from slime import Slime
from pig import Pig

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
        (range(3, 18), 39),
    ]

    for i_range, j in ladder_positions:
        ladders = [Ladder(j, i, 4) for i in i_range]
        game_world.add_objects(ladders, 0)
        for ladder in ladders:
            game_world.add_collision_pairs('server.character:ladder', None, ladder)


    # a, d 판정만 있는 블럭
    game_world.add_collision_pairs('server.character:wall', server.character, None)

    wall_positions = [
        (range(18, 23), 49),
        (range(3, 12), 29),
    ]

    for i_range, j in wall_positions:
        walls = [Wall(j, i, 3) for i in i_range]
        game_world.add_objects(walls, 0)
        for wall in walls:
            game_world.add_collision_pairs('server.character:wall', None, wall)

    wall_positions = [
        (1, range(0, 30)),
        (1, range(35, 44)),
        (1, range(50, 57)),
        (1, range(62, 109)),
        (0, range(0, 30)),
        (0, range(35, 44)),
        (0, range(50, 57)),
        (0, range(62, 109)),
    ]

    for j, i_range in wall_positions:
        walls = [Wall(i, j, 1) for i in i_range]
        game_world.add_objects(walls, 0)
        for wall in walls:
            game_world.add_collision_pairs('server.character:wall', None, wall)

    # a, d, 점프, 추락 판정이 있는 블럭
    game_world.add_collision_pairs('server.character:ground', server.character, None)

    ground_positions = [
        (18, range(38, 41)),
        (16, range(46, 48)),
        (14, range(41, 45)),
        (13, range(13, 21)),
        (12, range(26, 30)),
        (11, range(2, 4)),
        (9, range(6, 8)),
        (7, range(11, 16)),
        (5, range(19, 26)),
        (2, range(0, 30)),
        (2, range(35, 44)),
        (2, range(50, 57)),
        (2, range(62, 109)),
    ]

    for j, i_range in ground_positions:
        grounds = [Ground(i, j, 2) for i in i_range]
        game_world.add_objects(grounds, 0)
        for ground in grounds:
            game_world.add_collision_pairs('server.character:ground', None, ground)

    projectile_group = [
        'normalsg1', 'normalsg2', 'normalsg3', 'normalrf', 'normalrfsp', 'normalhg', 'reloadrf', 'rcskillrf', 'eskillhg',
        'rcskillhg',
                        ]

    # 몹 스포아
    game_world.add_collision_pairs('server.character:spore', server.character, None)

    spore_positions = [
        (7, 3),
        (11, 3),
        (13, 3),
        (17, 3),
        (22, 6),
        (16, 14),
    ]

    for i, j in spore_positions:
        spores = [Spore(i, j)]
        game_world.add_objects(spores, 2)
        for spore in spores:
            game_world.add_collision_pairs('server.character:spore', None, spore)
            for projectile in projectile_group:
                game_world.add_collision_pairs(f'{projectile}:spore', None, spore)

    # 몹 슬라임
    game_world.add_collision_pairs('server.character:slime', server.character, None)

    slime_positions = [
        (9, 3),
        (39, 3),
    ]

    for i, j in slime_positions:
        slimes = [Slime(i, j)]
        game_world.add_objects(slimes, 2)
        for slime in slimes:
            game_world.add_collision_pairs('server.character:slime', None, slime)
            for projectile in projectile_group:
                game_world.add_collision_pairs(f'{projectile}:slime', None, slime)

    # 몹 돼지
    game_world.add_collision_pairs('server.character:pig', server.character, None)

    pig_positions = [
        (17, 14),
        (53, 3),
    ]

    for i, j in pig_positions:
        pigs = [Pig(i, j)]
        game_world.add_objects(pigs, 2)
        for pig in pigs:
            game_world.add_collision_pairs('server.character:pig', None, pig)
            for projectile in projectile_group:
                game_world.add_collision_pairs(f'{projectile}:pig', None, pig)

    # 낙하 장애물 코코넛 k = 박자
    game_world.add_collision_pairs('server.character:coconut', server.character, None)

    coconut_positions = [
        (9, 20, 1),
        (32, 23, 2),
        (45, 15, 1),
        (48, 17, 2),
        (58, 14, 2),
        (59, 21, 1),
        (60, 14, 1),
    ]

    for i, j, k in coconut_positions:
        coconuts = [Coconut(i, j, k)]
        game_world.add_objects(coconuts, 2)
        for coconut in coconuts:
            game_world.add_collision_pairs('server.character:coconut', None, coconut)

    # 회복 아이템 k = 힐량
    game_world.add_collision_pairs('server.character:heal', server.character, None)

    heal = Heal(39, 19, 4)
    game_world.add_object(heal, 2)
    game_world.add_collision_pairs('server.character:heal', None, heal)

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

