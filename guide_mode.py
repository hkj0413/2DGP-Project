from pico2d import clear_canvas, update_canvas, get_events
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_1, SDLK_2, SDLK_3, SDLK_RETURN

import game_framework
import game_world
from mainguide import Mainguide

def init():
    global guide
    guide = Mainguide()
    game_world.add_object(guide, 4)

def finish():
    game_world.remove_object(guide)

def update():
   pass

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RETURN:
            game_framework.pop_mode()

def pause():
    pass

def resume():
    pass