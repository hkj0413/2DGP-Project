from pico2d import get_time, load_image, load_font, draw_rectangle

from ball import Ball

import game_world
import game_framework

from state_machine import start_event, right_down, left_up, left_down, right_up, space_down, StateMachine, time_out

PIXEL_PER_METER = (30.0 / 1)  # 30 pixel 1 m
RUN_SPEED_KMPH = 30.0           # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

class Idle:
    @staticmethod
    def enter(character, e):
        if start_event(e):
            character.face_dir = 1
        elif right_down(e) or left_up(e):
            character.face_dir = -1
        elif left_down(e) or right_up(e):
            character.face_dir = 1

        character.frame = 0
        character.action = 14
        character.wait_time = get_time()

    @staticmethod
    def exit(character, e):
        if space_down(e):
            character.fire_ball()

    @staticmethod
    def do(character):
        character.frame = (character.frame + character.action * ACTION_PER_TIME * game_framework.frame_time) % character.action

    @staticmethod
    def draw(character):
        if character.face_dir == 1:
            character.images['Idle'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '',character.x, character.y, 170, 170)
        else:
            character.images['Idle'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h',character.x, character.y, 170, 170)

class Walk:
    @staticmethod
    def enter(character, e):
        if right_down(e) or left_up(e):
            character.dir, character.face_dir = 1, 1
        elif left_down(e) or right_up(e):
            character.dir, character.face_dir= -1, -1

        character.action = 6

    @staticmethod
    def exit(character, e):
        if space_down(e):
            character.fire_ball()

    @staticmethod
    def do(character):
        character.frame = (character.frame + character.action * ACTION_PER_TIME*game_framework.frame_time) % character.action
        character.x += character.dir * RUN_SPEED_PPS * game_framework.frame_time
        pass

    @staticmethod
    def draw(character):
        if character.face_dir == 1:
            character.images['Walk'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '', character.x, character.y, 170, 170)
        else:
            character.images['Walk'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h', character.x, character.y, 170, 170)

animation_names = ['Idle', 'Walk']

class Character:
    images = None

    def load_images(self):
        if Character.images == None:
            Character.images = {}
            for name in animation_names:
                if name == 'Idle':
                    Character.images[name] = load_image("./HKCAWS/" + name + ".png")
                elif name == 'Walk':
                    Character.images[name] = load_image("./HKCAWS/" + name + ".png")

    def __init__(self):
        self.x, self.y = 400, 90
        self.face_dir = 1
        self.ball_count = 10
        self.load_images()
        self.font = load_font('ENCR10B.TTF', 16)
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Walk, left_down: Walk, left_up: Walk, right_up: Walk, space_down: Idle},
                Walk: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Walk},
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x - 10, self.y + 50, f'{self.ball_count:02d}', (255, 255, 0))
        draw_rectangle(*self.get_bb())

    def fire_ball(self):
        if self.ball_count > 0:
            self.ball_count -= 1
            ball = Ball(self.x, self.y, self.face_dir * 10)
            game_world.add_object(ball)
            game_world.add_collision_pairs('zombie:ball', None, ball)

    def get_bb(self):
        return self.x - 17, self.y - 50, self.x + 17, self.y + 18

    def handle_collision(self, group, other):
        if group == 'character:ball':
            self.ball_count += 1
        elif group == 'character:zombie':
            game_framework.running = False