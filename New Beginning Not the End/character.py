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
FRAMES_PER_ACTION = 8

class Idle:
    @staticmethod
    def enter(character, e):
        if start_event(e):
            character.action = 3
            character.face_dir = 1
        elif right_down(e) or left_up(e):
            character.action = 2
            character.face_dir = -1
        elif left_down(e) or right_up(e):
            character.action = 3
            character.face_dir = 1

        character.frame = 0
        character.wait_time = get_time()

    @staticmethod
    def exit(character, e):
        if space_down(e):
            character.fire_ball()

    @staticmethod
    def do(character):
        character.frame = (character.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 8
        if get_time() - character.wait_time > 2:
            character.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(character):
        character.image.clip_draw(int(character.frame) * 100, character.action * 100, 100, 100, character.x, character.y)

class Sleep:
    @staticmethod
    def enter(character, e):
        if start_event(e):
            character.face_dir = 1
            character.action = 3
        character.frame = 0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 8


    @staticmethod
    def draw(character):
        if character.face_dir == 1:
            character.image.clip_composite_draw(int(character.frame) * 100, 300, 100, 100,
                                          3.141592 / 2, '', character.x - 25, character.y - 25, 100, 100)
        else:
            character.image.clip_composite_draw(int(character.frame) * 100, 200, 100, 100,
                                          -3.141592 / 2, '', character.x + 25, character.y - 25, 100, 100)


class Run:
    @staticmethod
    def enter(character, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            character.dir, character.face_dir, character.action = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            character.dir, character.face_dir, character.action = -1, -1, 0

    @staticmethod
    def exit(character, e):
        if space_down(e):
            character.fire_ball()


    @staticmethod
    def do(character):
        character.frame = (character.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 8

        character.x += character.dir * RUN_SPEED_PPS * game_framework.frame_time
        pass

    @staticmethod
    def draw(character):
        character.image.clip_draw(int(character.frame) * 100, character.action * 100, 100, 100, character.x, character.y)

class Character:

    def __init__(self):
        self.x, self.y = 400, 90
        self.face_dir = 1
        self.ball_count = 10
        self.font = load_font('ENCR10B.TTF', 16)
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, time_out: Sleep, space_down: Idle},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Run},
                Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 여기서 받을 수 있는 것만 걸러야 함. right left  등등..
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x-10, self.y + 50, f'{self.ball_count:02d}', (255, 255, 0))
        draw_rectangle(*self.get_bb())

    def fire_ball(self):
        if self.ball_count > 0:
            self.ball_count -= 1
            ball = Ball(self.x, self.y, self.face_dir*10)
            game_world.add_object(ball)
            game_world.add_collision_pairs('zombie:ball', None, ball)

    def get_bb(self):
        # fill here
        return self.x - 20, self.y - 50, self.x + 20, self.y + 50

    def handle_collision(self, group, other):
        # fill here
        if group == 'character:ball':
            self.ball_count += 1
        elif group == 'character:zombie':
            game_framework.running = False