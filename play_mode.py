from pico2d import *

import game_framework
import game_world
import guide_mode
import server

from ground import Ground
from wall import Wall
from ladder import Ladder
from portal import Portal
from character import Character
from ui import UI
from coconut import Coconut
from heal import Heal
from more_hp import MoreHP
from enhance import Enhance
from diamond import Diamond

from background import Background
from spore import Spore
from slime import Slime
from pig import Pig
from stonegolem import Stonegolem

character_created = False

stage = 3

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.push_mode(guide_mode)
        else:
            server.character.handle_event(event)

projectile_group = [
        'normalsg1', 'normalsg2', 'normalsg3', 'normalrf', 'normalrfsp', 'normalhg', 'reloadrf', 'rcskillrf', 'eskillhg',
        'rcskillhg', 'qskillsg', 'qskillstunsg', 'qskillrf', 'cskillstunsg', 'cskillsg', 'eskillsg1', 'eskillsg2', 'eskillsg3',
        'qskillboomhg', 'cskillhg', 'rcskillsg'
                        ]

stage_data = {
    1: {
        'ladder_positions': [
            (range(3, 18), 39),
            (range(9, 16), 82),
            (range(3, 12), 95),
            (range(13, 22), 95),
            (range(8, 17), 106),
            (range(18, 26), 106),
        ],

        'wall_positions': [
            (range(18, 23), 49),
            (range(3, 12), 29),
            (range(9, 27), 83),
            (range(9, 22), 93),
        ],

        'floor_positions': [
            (2, range(65, 68)),
            (1, range(0, 30)),
            (1, range(35, 44)),
            (1, range(50, 57)),
            (1, range(62, 85)),
            (1, range(94, 108)),
            (0, range(0, 30)),
            (0, range(35, 44)),
            (0, range(50, 57)),
            (0, range(62, 85)),
            (0, range(94, 108)),
        ],

        'ground_positions': [
            (26, range(105, 108)),
            (22, range(88, 106)),
            (21, range(72, 80)),
            (18, range(38, 41)),
            (18, range(69, 70)),
            (17, range(96, 107)),
            (16, range(46, 48)),
            (16, range(82, 83)),
            (15, range(66, 67)),
            (14, range(41, 45)),
            (13, range(13, 21)),
            (12, range(26, 30)),
            (12, range(69, 70)),
            (12, range(76, 79)),
            (12, range(95, 106)),
            (11, range(2, 4)),
            (9, range(6, 8)),
            (8, range(82, 84)),
            (8, range(93, 94)),
            (7, range(11, 16)),
            (7, range(96, 107)),
            (6, range(71, 80)),
            (5, range(19, 26)),
            (3, range(65, 68)),
            (2, range(0, 30)),
            (2, range(35, 44)),
            (2, range(50, 57)),
            (2, range(62, 65)),
            (2, range(68, 85)),
            (2, range(94, 108)),
        ],

        'spore_positions': [
            (7, 3),
            (11, 3),
            (13, 3),
            (17, 3),
            (25, 3),
            (22, 6),
            (16, 14),
            (74, 7),
            (76, 7),
            (80, 3),
            (99, 8),
            (100, 8),
            (101, 8),
            (102, 8),
            (103, 8),
        ],

        'slime_positions': [
            (9, 3),
            (16, 3),
            (39, 3),
            (75, 7),
            (79, 3),
            (98, 13),
            (99, 13),
            (100,13),
            (101, 13),
            (102, 13),
        ],

        'pig_positions': [
            (17, 14),
            (40, 3),
            (53, 3),
            (71, 3),
            (73, 3),
            (99, 18),
            (100, 18),
            (101, 18),
            (102, 18),
            (103, 18),
        ],

        'coconut_positions': [
        (9, 20, 1),
        (32, 23, 2),
        (45, 15, 1),
        (48, 17, 2),
        (58, 14, 2),
        (59, 24, 1),
        (60, 14, 4),
        (66, 24, 3),
        (69, 24, 2),
        (80, 24, 5),
        ],

        'heal_positions': [
        (39, 19, 4),
        (76, 22, 4),
        (79, 22, 4),
        (91, 9, 4),
        ],
    },

    2: {
        'floor_positions': [
            (1, range(0, 36)),
            (0, range(0, 36)),
        ],

        'ground_positions': [
            (14, range(32, 36)),
            (11, range(24, 28)),
            (8, range(16, 20)),
            (5, range(8, 12)),
            (2, range(0, 36)),
        ],
    },

    3: {
        'floor_positions': [
            (1, range(0, 36)),
            (0, range(0, 36)),
        ],

        'ground_positions': [
            (10, range(0, 5)),
            (8, range(12, 24)),
            (5, range(27, 30)),
            (5, range(6, 9)),
            (2, range(0, 36)),
        ],

        'spore_positions': [
            (10, 3),
            (13, 3),
            (16, 3),
            (19, 3),
            (22, 3),
            (25, 3),
        ],
    },
}

def clear_collision_pairs():
    game_world.collision_pairs.clear()

def change_stage(stage_number):
    global stage

    all_objects = game_world.get_all_objects()

    for obj in all_objects:
        if obj != server.character:
            game_world.remove_object(obj)

    clear_collision_pairs()

    stage = stage_number

    init(stage_number)

def init(stage):
    global character, character_created

    if stage == 1:
        stage_info = stage_data[stage]

        # 캐릭터
        if not character_created:
            server.character = Character()
            game_world.add_object(server.character, 1)
            character_created = True

        # UI
        ui = UI()
        game_world.add_object(ui, 3)

        server.background = Background(0)
        game_world.add_object(server.background, 0)

        # 사다리
        game_world.add_collision_pairs('server.character:ladder', server.character, None)

        for i_range, j in stage_info['ladder_positions']:
            ladders = [Ladder(j, i, 4) for i in i_range]
            game_world.add_objects(ladders, 0)
            for ladder in ladders:
                game_world.add_collision_pairs('server.character:ladder', None, ladder)

        # a, d 판정만 있는 블럭
        game_world.add_collision_pairs('server.character:wall', server.character, None)

        for i_range, j in stage_info['wall_positions']:
            walls = [Wall(j, i, 3) for i in i_range]
            game_world.add_objects(walls, 0)
            for wall in walls:
                game_world.add_collision_pairs('server.character:wall', None, wall)

        # a, d 판정만 있는 바닥
        for j, i_range in stage_info['floor_positions']:
            walls = [Wall(i, j, 1) for i in i_range]
            game_world.add_objects(walls, 0)
            for wall in walls:
                game_world.add_collision_pairs('server.character:wall', None, wall)

        # a, d, 점프, 추락 판정이 있는 블럭
        game_world.add_collision_pairs('server.character:ground', server.character, None)

        for j, i_range in stage_info['ground_positions']:
            grounds = [Ground(i, j, 2) for i in i_range]
            game_world.add_objects(grounds, 0)
            for ground in grounds:
                game_world.add_collision_pairs('server.character:ground', None, ground)

        # 포탈
        game_world.add_collision_pairs('server.character:portal', server.character, None)

        portal = Portal(105, 4, 0)
        game_world.add_object(portal, 0)
        game_world.add_collision_pairs('server.character:portal', None, portal)

        # 몹 스포아
        game_world.add_collision_pairs('server.character:spore', server.character, None)

        for i, j in stage_info['spore_positions']:
            spores = [Spore(i, j)]
            game_world.add_objects(spores, 2)
            for spore in spores:
                game_world.add_collision_pairs('server.character:spore', None, spore)
                for projectile in projectile_group:
                    game_world.add_collision_pairs(f'{projectile}:spore', None, spore)

        # 몹 슬라임
        game_world.add_collision_pairs('server.character:slime', server.character, None)

        for i, j in stage_info['slime_positions']:
            slimes = [Slime(i, j)]
            game_world.add_objects(slimes, 2)
            for slime in slimes:
                game_world.add_collision_pairs('server.character:slime', None, slime)
                for projectile in projectile_group:
                    game_world.add_collision_pairs(f'{projectile}:slime', None, slime)

        # 몹 돼지
        game_world.add_collision_pairs('server.character:pig', server.character, None)

        for i, j in stage_info['pig_positions']:
            pigs = [Pig(i, j)]
            game_world.add_objects(pigs, 2)
            for pig in pigs:
                game_world.add_collision_pairs('server.character:pig', None, pig)
                for projectile in projectile_group:
                    game_world.add_collision_pairs(f'{projectile}:pig', None, pig)

        # 낙하 장애물 코코넛 k = 박자
        game_world.add_collision_pairs('server.character:coconut', server.character, None)

        for i, j, k in stage_info['coconut_positions']:
            coconuts = [Coconut(i, j, k)]
            game_world.add_objects(coconuts, 2)
            for coconut in coconuts:
                game_world.add_collision_pairs('server.character:coconut', None, coconut)

        # 회복 아이템 k = 힐량
        game_world.add_collision_pairs('server.character:heal', server.character, None)


        for i, j, k in stage_info['heal_positions']:
            heals = [Heal(i, j, k)]
            game_world.add_objects(heals, 2)
            for heal in heals:
                game_world.add_collision_pairs('server.character:heal', None, heal)

        # 최대 체력 증가 아이템
        game_world.add_collision_pairs('server.character:morehp', server.character, None)

        morehp = MoreHP(73, 22)
        game_world.add_object(morehp, 2)
        game_world.add_collision_pairs('server.character:morehp', None, morehp)

        # 캐릭터 강화 아이템
        game_world.add_collision_pairs('server.character:enhance', server.character, None)

        enhance = Enhance(90, 23)
        game_world.add_object(enhance, 2)
        game_world.add_collision_pairs('server.character:enhance', None, enhance)

        # 다이아 몬드 아이템
        game_world.add_collision_pairs('server.character:diamond', server.character, None)

        diamond = Diamond(100, 3)
        game_world.add_object(diamond, 2)
        game_world.add_collision_pairs('server.character:diamond', None, diamond)

    elif stage == 2:
        stage_info = stage_data[stage]

        # 캐릭터
        if not character_created:
            server.character = Character()
            game_world.add_object(server.character, 1)
            character_created = True

        # UI
        ui = UI()
        game_world.add_object(ui, 3)

        server.background = Background(1)
        game_world.add_object(server.background, 0)

        game_world.add_collision_pairs('server.character:ladder', server.character, None)

        # a, d 판정만 있는 바닥
        game_world.add_collision_pairs('server.character:wall', server.character, None)

        for j, i_range in stage_info['floor_positions']:
            walls = [Wall(i, j, 1) for i in i_range]
            game_world.add_objects(walls, 0)
            for wall in walls:
                game_world.add_collision_pairs('server.character:wall', None, wall)

        # a, d, 점프, 추락 판정이 있는 블럭
        game_world.add_collision_pairs('server.character:ground', server.character, None)

        for j, i_range in stage_info['ground_positions']:
            grounds = [Ground(i, j, 2) for i in i_range]
            game_world.add_objects(grounds, 0)
            for ground in grounds:
                game_world.add_collision_pairs('server.character:ground', None, ground)

        # 포탈
        game_world.add_collision_pairs('server.character:portal', server.character, None)

        portal = Portal(34, 16, 0)
        game_world.add_object(portal, 0)
        game_world.add_collision_pairs('server.character:portal', None, portal)

    elif stage == 3:
        stage_info = stage_data[stage]

        # 캐릭터
        if not character_created:
            server.character = Character()
            game_world.add_object(server.character, 1)
            character_created = True

        # UI
        ui = UI()
        game_world.add_object(ui, 3)

        server.background = Background(1)
        game_world.add_object(server.background, 0)

        game_world.add_collision_pairs('server.character:ladder', server.character, None)

        # a, d 판정만 있는 바닥
        game_world.add_collision_pairs('server.character:wall', server.character, None)

        for j, i_range in stage_info['floor_positions']:
            walls = [Wall(i, j, 1) for i in i_range]
            game_world.add_objects(walls, 0)
            for wall in walls:
                game_world.add_collision_pairs('server.character:wall', None, wall)

        # a, d, 점프, 추락 판정이 있는 블럭
        game_world.add_collision_pairs('server.character:ground', server.character, None)

        for j, i_range in stage_info['ground_positions']:
            grounds = [Ground(i, j, 2) for i in i_range]
            game_world.add_objects(grounds, 0)
            for ground in grounds:
                game_world.add_collision_pairs('server.character:ground', None, ground)

        # 포탈
        game_world.add_collision_pairs('server.character:portal', server.character, None)

        portal = Portal(34, 4, 1)
        game_world.add_object(portal, 0)
        game_world.add_collision_pairs('server.character:portal', None, portal)

        # 보스 골렘
        game_world.add_collision_pairs('server.character:stonegolem', server.character, None)
        game_world.add_collision_pairs('server.character:stonegolemattack', server.character, None)
        game_world.add_collision_pairs('server.character:stonegolemskill', server.character, None)

        stonegolem = Stonegolem(18, 6)
        game_world.add_object(stonegolem, 0)
        game_world.add_collision_pairs('server.character:stonegolem', None, stonegolem)
        for projectile in projectile_group:
            game_world.add_collision_pairs(f'{projectile}:stonegolem', None, stonegolem)

        # 몹 스포아
        game_world.add_collision_pairs('server.character:spore', server.character, None)

        for i, j in stage_info['spore_positions']:
            spores = [Spore(i, j)]
            game_world.add_objects(spores, 2)
            for spore in spores:
                game_world.add_collision_pairs('server.character:spore', None, spore)
                for projectile in projectile_group:
                    game_world.add_collision_pairs(f'{projectile}:spore', None, spore)

        # 회복 아이템 k = 힐량
        game_world.add_collision_pairs('server.character:heal', server.character, None)

        heals = [Heal(2, 11, 4)]
        game_world.add_objects(heals, 2)
        for heal in heals:
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