from pico2d import get_time, load_image, load_font, draw_rectangle, clamp

import game_world
import game_framework
import ground

from state_machine import *

PIXEL_PER_METER = (30.0 / 1)  # 30 pixel 1 m
RUN_SPEED_KMPH = 10.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

a_pressed = False
d_pressed = False
Jump = False
Fall = False

jump_velocity = 8.5
fall_velocity = 0.0
gravity = 0.1

class Idle:
    @staticmethod
    def enter(character, e):
        global Jump
        if start_event(e):
            character.face_dir = 1
        elif change_stance_z(e) and not Jump and not Fall:
            character.change_z()
        elif change_stance_x(e) and not Jump and not Fall:
            character.change_x()
        elif jump(e) and not Jump and not Fall:
            Jump = True
            character.frame = 0

        if character.stance == 0:
            character.name = 'Idle_SG'
            character.frame = clamp(0, character.frame, 14)
        elif character.stance == 1:
            character.name = 'Idle_RF'
            character.frame = clamp(0, character.frame, 14)
        elif character.stance == 2:
            character.name = 'Idle_HG'
            character.frame = clamp(0, character.frame, 11)

        character.wait_time = get_time()

    @staticmethod
    def exit(character, e):
        if right_down(e):
            character.face_dir = 1
        elif left_down(e):
            character.face_dir = -1

    @staticmethod
    def do(character):
        if not Jump and not Fall:
            if character.stance == 0 or character.stance == 1:
                character.frame = (character.frame + 14.0 * 1.5 * game_framework.frame_time) % 14
            elif character.stance == 2:
                character.frame = (character.frame + 11.0 * 1.5 * game_framework.frame_time) % 11

    @staticmethod
    def draw(character):
        if Jump or Fall:
            if character.face_dir == 1:
                if character.stance == 0:
                    character.images['Walk_SG'].clip_composite_draw(0, 0, 340, 340, 0, '',
                                                                         character.x, character.y, 170, 170)
                elif character.stance == 1:
                    character.images['Walk_RF'].clip_composite_draw(0, 0, 340, 340, 0, '',
                                                                    character.x, character.y, 170, 170)
                elif character.stance == 2:
                    character.images['Walk_HG'].clip_composite_draw(0, 0, 340, 340, 0, '',
                                                                    character.x, character.y, 170, 170)
            else:
                if character.stance == 0:
                    character.images['Walk_SG'].clip_composite_draw(0, 0, 340, 340, 0, 'h',
                                                                    character.x, character.y, 170, 170)
                elif character.stance == 1:
                    character.images['Walk_RF'].clip_composite_draw(0, 0, 340, 340, 0, 'h',
                                                                    character.x, character.y, 170, 170)
                elif character.stance == 2:
                    character.images['Walk_HG'].clip_composite_draw(0, 0, 340, 340, 0, 'h',
                                                                    character.x, character.y, 170, 170)
        else:
            if character.face_dir == 1:
                character.images[character.name].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '',
                                                                     character.x, character.y, 170, 170)
            else:
                character.images[character.name].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h',
                                                                     character.x, character.y, 170, 170)
class Walk:
    @staticmethod
    def enter(character, e):
        global a_pressed, d_pressed, Jump
        if right_down(e):
            d_pressed = True
            character.face_dir = 1
        elif right_up(e):
            d_pressed = False
            if a_pressed:
                character.face_dir = -1
            elif not a_pressed:
                character.state_machine.add_event(('CHANGE', 0))
        elif left_down(e):
            a_pressed = True
            character.face_dir = -1
        elif left_up(e):
            a_pressed = False
            if d_pressed:
                character.face_dir = 1
            elif not d_pressed:
                character.state_machine.add_event(('CHANGE', 0))
        elif change_stance_z(e) and not Jump and not Fall:
            character.change_z()
        elif change_stance_x(e) and not Jump and not Fall:
            character.change_x()
        elif jump(e) and not Jump and not Fall:
            Jump = True
            character.frame = 0

        if character.stance == 0:
            character.name = 'Walk_SG'
        elif character.stance == 1:
            character.name = 'Walk_RF'
        elif character.stance == 2:
            character.name = 'Walk_HG'

        character.frame = clamp(0, character.frame, 6)

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        global Fall
        if not Jump and not Fall:
            character.frame = (character.frame + 6.0 * 2.0 * game_framework.frame_time) % 6

        character.x += character.speed * character.face_dir * RUN_SPEED_PPS * game_framework.frame_time

        for block in game_world.collision_pairs['character:ground'][1] + game_world.collision_pairs['character:wall'][1]:
            if game_world.collide(character, block):
                character.x -= character.speed * character.face_dir * RUN_SPEED_PPS * game_framework.frame_time
                return

        ground_objects = game_world.collision_pairs['character:ground'][1]
        for block in ground_objects:
            if game_world.collide_ad(character, block, ground_objects):
                Fall = True
                print('collide_ad')
                return

    @staticmethod
    def draw(character):
        if character.face_dir == 1:
            character.images[character.name].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '',
                                                                 character.x, character.y, 170, 170)
        else:
            character.images[character.name].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h',
                                                                 character.x, character.y, 170, 170)

class Hit:
    @staticmethod
    def enter(character, e):
        global a_pressed, d_pressed, Jump, jump_velocity, Fall
        Jump = False
        jump_velocity = 8.5
        Fall = True
        character.wait_time = get_time()
        character.frame = 0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        if get_time() - character.wait_time > 1:
            character.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(character):
        if character.face_dir == 1:
            if character.stance == 0:
                character.images['Die_SG'].clip_composite_draw(1 * 340, 0, 340, 340, 0, '',
                                                                character.x - 48, character.y, 170, 170)
            elif character.stance == 1:
                character.images['Die_RF'].clip_composite_draw(1 * 340, 0, 340, 340, 0, '',
                                                                character.x - 11, character.y, 170, 170)
            elif character.stance == 2:
                character.images['Die_HG'].clip_composite_draw(2 * 340, 0, 340, 340, 0, '',
                                                                character.x, character.y, 170, 170)
        else:
            if character.stance == 0:
                character.images['Die_SG'].clip_composite_draw(1 * 340, 0, 340, 340, 0, 'h',
                                                                     character.x + 48, character.y, 170, 170)
            elif character.stance == 1:
                character.images['Die_RF'].clip_composite_draw(1 * 340, 0, 340, 340, 0, 'h',
                                                                     character.x + 11, character.y, 170, 170)
            elif character.stance == 2:
                character.images['Die_HG'].clip_composite_draw(2 * 340, 0, 340, 340, 0, 'h',
                                                                     character.x, character.y, 170, 170)

animation_names = ['Idle_SG', 'Idle_RF', 'Idle_HG',
                   'Walk_SG', 'Walk_RF', 'Walk_HG',
                   'Die_SG', 'Die_RF', 'Die_HG']

class Character:
    images = None
    image_Hp = None
    image_Bullet = None

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
                elif name == 'Die_SG':
                    Character.images[name] = load_image("./HKCAWS/" + name + ".png")
                elif name == 'Die_RF':
                    Character.images[name] = load_image("./R93/" + name + ".png")
                elif name == 'Die_HG':
                    Character.images[name] = load_image("./GSH18Mod/" + name + ".png")

    def __init__(self):
        self.x, self.y = 34, 140.0
        self.stance = 0
        self.face_dir = 1
        self.speed = 3
        self.frame = 0
        self.ball_count = 10
        self.load_images()
        self.name = ''
        self.font = load_font('ENCR10B.TTF', 16)
        self.Hp = 20
        self.max_Hp = 20
        if Character.image_Hp == None:
            self.Hp_image = load_image('Hp.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {
                    right_down: Walk, left_down: Walk, left_up: Walk, right_up: Walk, change_stance_z: Idle, change_stance_x: Idle,
                    jump: Idle,
                    temp_damage: Hit
                },
                Walk: {
                    right_down: Walk, left_down: Walk, right_up: Walk, left_up: Walk, change_stance_z: Walk, change_stance_x: Walk,
                    change: Idle, jump: Walk,
                    temp_damage: Hit
                },
                Hit: {
                    time_out: Idle
                },
            }
        )

    def update(self):
        global Jump, jump_velocity, Fall, fall_velocity
        self.state_machine.update()
        self.x = clamp(17, self.x, 1063)

        if Jump:
            self.y += jump_velocity * RUN_SPEED_PPS * game_framework.frame_time
            jump_velocity -= gravity
            if jump_velocity <= 0:
                Jump = False
                Fall = True
                jump_velocity = 8.5

        if Fall:
            self.y -= fall_velocity * RUN_SPEED_PPS * game_framework.frame_time
            fall_velocity += gravity

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x - 10, self.y + 50.0, f'{self.ball_count:02d}', (255, 255, 0))
        draw_rectangle(*self.get_bb())

        heart_count = int(self.max_Hp / 2)
        hx = 20
        hy = 780

        for i in range(heart_count):
            if self.Hp >= (i + 1) * 2:
                self.Hp_image.clip_composite_draw(0, 0, 120, 360, 0, '', hx + i * 30, hy, 30, 90)
            elif self.Hp == (i * 2) + 1:
                self.Hp_image.clip_composite_draw(120, 0, 120, 360, 0, '', hx + i * 30, hy, 30, 90)
            else:
                self.Hp_image.clip_composite_draw(240, 0, 120, 360, 0, '', hx + i * 30, hy, 30, 90)

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

    def get_bb(self):
        return self.x - 17, self.y - 49.0, self.x + 17, self.y + 19.0

    def handle_collision(self, group, other):
        pass

    def handle_collision_fall(self, group, other):
        global Fall, fall_velocity
        if group == 'character:ground' and Fall:
            self.y = ground.Ground.collide_fall(other)
            Fall = False
            fall_velocity = 0.0

    def handle_collision_jump(self, group, other):
        global Jump, jump_velocity, Fall
        if group == 'character:ground' and Jump:
            self.y = ground.Ground.collide_jump(other)
            Jump = False
            Fall = True
            jump_velocity = 8.5