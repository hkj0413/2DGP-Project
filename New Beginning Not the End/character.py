from numpy import character
from pico2d import get_time, load_image, load_font, draw_rectangle, clamp

from ball import Ball

import game_world
import game_framework

from state_machine import *

PIXEL_PER_METER = (30.0 / 1)  # 30 pixel 1 m
RUN_SPEED_KMPH = 10.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Idle:
    @staticmethod
    def enter(character, e):
        if start_event(e):
            character.face_dir = 1
        elif right_down(e) or left_up(e):
            character.face_dir = -1
        elif left_down(e) or right_up(e):
            character.face_dir = 1

        if character.stance == 0:
            character.name = 'Idle_SG'
        elif character.stance == 1:
            character.name = 'Idle_RF'
        elif character.stance == 2:
            character.name = 'Idle_HG'

        character.frame = 0
        character.wait_time = get_time()

    @staticmethod
    def exit(character, e):
        if change_stance_z(e):
            character.change_z()
        elif change_stance_x(e):
            character.change_x()
        elif space_down(e):
            character.fire_ball()

    @staticmethod
    def do(character):
        if character.stance == 0 or character.stance == 1:
            character.frame = (character.frame + 14.0 * 1.5 * game_framework.frame_time) % 14
        elif character.stance == 2:
            character.frame = (character.frame + 11.0 * 1.5 * game_framework.frame_time) % 11

    @staticmethod
    def draw(character):
        if character.face_dir == 1:
            character.images[character.name].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '',
                                                                 character.x, character.y, 170, 170)
        else:
            character.images[character.name].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h',
                                                                 character.x, character.y, 170, 170)
class Walk:
    @staticmethod
    def enter(character, e):
        if right_down(e) or left_up(e):
            character.face_dir = 1
        elif left_down(e) or right_up(e):
            character.face_dir= -1

        if character.stance == 0:
            character.name = 'Walk_SG'
        elif character.stance == 1:
            character.name = 'Walk_RF'
        elif character.stance == 2:
            character.name = 'Walk_HG'

        character.frame = 0

    @staticmethod
    def exit(character, e):
        if change_stance_z(e):
            character.change_z()
        elif change_stance_x(e):
            character.change_x()
        elif space_down(e):
            character.fire_ball()

    @staticmethod
    def do(character):
        character.frame = (character.frame + 6.0 * 2.0 * game_framework.frame_time) % 6
        character.x += character.speed * character.face_dir * RUN_SPEED_PPS * game_framework.frame_time
        pass

    @staticmethod
    def draw(character):
        if character.face_dir == 1:
            character.images[character.name].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '',
                                                                 character.x, character.y, 170, 170)
        else:
            character.images[character.name].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h',
                                                                 character.x, character.y, 170, 170)

animation_names = ['Idle_SG', 'Idle_RF', 'Idle_HG', 'Walk_SG', 'Walk_RF', 'Walk_HG']

class Character:
    images = None

    def load_images(self):
        if Character.images == None:
            Character.images = {}
            for name in animation_names:
                if name == 'Idle_SG':
                    Character.images[name] = load_image("./HKCAWS/" + name + ".png")
                elif name == 'Idle_RF':
                    Character.images[name] = load_image("./R93/" + name + ".png")
                elif name == 'Idle_HG':
                    Character.images[name] = load_image("./GSH18Mod/" + name + ".png")
                elif name == 'Walk_SG':
                    Character.images[name] = load_image("./HKCAWS/" + name + ".png")
                elif name == 'Walk_RF':
                    Character.images[name] = load_image("./R93/" + name + ".png")
                elif name == 'Walk_HG':
                    Character.images[name] = load_image("./GSH18Mod/" + name + ".png")

    def __init__(self):
        self.x, self.y = 400, 90
        self.stance = 0
        self.face_dir = 1
        self.speed = 3
        self.ball_count = 10
        self.load_images()
        self.name = ''
        self.font = load_font('ENCR10B.TTF', 16)
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {
                    right_down: Walk, left_down: Walk, left_up: Walk, right_up: Walk, change_stance_z: Idle, change_stance_x: Idle,
                    space_down: Idle
                },
                Walk: {
                    right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, change_stance_z: Walk, change_stance_x: Walk,
                    space_down: Walk
                },
            }
        )

    def update(self):
        self.state_machine.update()
        self.x = clamp(17, self.x, 1063)

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x - 10, self.y + 50, f'{self.ball_count:02d}', (255, 255, 0))
        draw_rectangle(*self.get_bb())

    def change_z(self):
        if self.stance == 0:
            self.stance = 1
            self.speed = 4
        elif self.stance == 1:
            self.stance = 2
            self.speed = 5
        elif self.stance == 2:
            self.stance = 0
            self.speed = 3

    def change_x(self):
        if self.stance == 0:
            self.stance = 2
            self.speed = 5
        elif self.stance == 1:
            self.stance = 0
            self.speed = 3
        elif self.stance == 2:
            self.stance = 1
            self.speed = 4

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