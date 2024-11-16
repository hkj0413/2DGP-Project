from sdl2 import *

def start_event(e):
    return e[0] == 'START'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a

def change_stance_z(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_z

def change_stance_x(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_x

def jump(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def die(e):
    return e[0] == 'DIE'

def time_out(e):
    return e[0] == 'TIME_OUT'

class StateMachine:
    def __init__(self, o):
        self.o = o
        self.event_que = []

    def start(self, state):
        self.cur_state = state
        print(f'Enter into {state}')
        self.cur_state.enter(self.o, ('START', 0))

    def add_event(self, e):
        self.event_que.append(e)

    def set_transitions(self, transitions):
        self.transitions = transitions

    def update(self):
        self.cur_state.do(self.o)
        if self.event_que:
            event = self.event_que.pop(0)
            self.handle_event(event)

    def draw(self):
        self.cur_state.draw(self.o)

    def handle_event(self, e):
        for event, next_state in self.transitions[self.cur_state].items():
            if event(e):
                print(f'Exit from {self.cur_state}')
                self.cur_state.exit(self.o, e)
                self.cur_state = next_state
                print(f'Enter into {self.cur_state}')
                self.cur_state.enter(self.o, e)
                return