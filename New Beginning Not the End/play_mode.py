import random

from pico2d import *

import game_framework

import game_world
from grass import Grass
from character import Character
from ball import Ball
from zombie import Zombie

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
    global character, balls, zombies

    grass = Grass()
    game_world.add_object(grass, 0)

    character = Character()
    game_world.add_object(character, 1)

    balls = [Ball(random.randint(100, 980), 60, 0) for _ in range(30)]
    game_world.add_objects(balls, 1)

    zombies = [Zombie() for _ in range(5)]
    game_world.add_objects(zombies, 1)

    game_world.add_collision_pairs('character:ball', character, None)
    for ball in balls:
        game_world.add_collision_pairs('character:ball', None, ball)

    game_world.add_collision_pairs('character:zombie', character, None)

    for zombie in zombies:
        game_world.add_collision_pairs('character:zombie', None, zombie)
        game_world.add_collision_pairs('zombie:ball', zombie, None)

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

