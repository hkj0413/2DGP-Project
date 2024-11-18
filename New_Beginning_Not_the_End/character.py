from pico2d import get_time, load_image, draw_rectangle, clamp

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

jump_velocity = 10.0
fall_velocity = 0.0
gravity = 0.5

class Idle:
    @staticmethod
    def enter(character, e):
        global Jump, d_pressed, a_pressed
        if start_event(e):
            character.face_dir = 1
        elif right_up(e):
            d_pressed = False
        elif left_up(e):
            a_pressed = False
        elif change(e):
            if a_pressed or d_pressed:
                character.state_machine.add_event(('CHANGE', 0))
        elif change_stance_z(e) and not Jump and not Fall and Character.state == 0:
            character.change_z()
        elif change_stance_x(e) and not Jump and not Fall and Character.state == 0:
            character.change_x()
        elif rc_down(e):
            if Character.stance == 0:
                Character.state = 1
                Character.speed = 1
        elif rc_up(e):
            if Character.stance == 0:
                Character.state = 0
                Character.speed = 3
        elif jump(e) and not Jump and not Fall:
            if not (Character.stance == 0 and Character.state == 1):
                Jump = True
                character.frame = 0
        elif temp_damage(e) and Character.hit_delay == 0:
            character.state_machine.add_event(('HIT', 0))
        elif dash(e) and Character.dash_cooldown == 0:
            character.state_machine.add_event(('USE_DASH', 0))

        if Character.stance == 0:
            if Character.state == 0:
                character.name = 'Idle_SG'
            elif Character.state == 1:
                character.name = 'Rc_SG'
            character.frame = clamp(0, character.frame, 14)
        elif Character.stance == 1:
            character.name = 'Idle_RF'
            character.frame = clamp(0, character.frame, 14)
        elif Character.stance == 2:
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
            if Character.stance == 0 or Character.stance == 1:
                character.frame = (character.frame + 14.0 * 1.5 * game_framework.frame_time) % 14
            elif Character.stance == 2:
                character.frame = (character.frame + 11.0 * 1.5 * game_framework.frame_time) % 11

    @staticmethod
    def draw(character):
        if Jump or Fall:
            if character.face_dir == 1:
                if Character.stance == 0:
                    character.images['Walk_SG'].clip_composite_draw(0, 0, 340, 340, 0, '',
                                                                         character.x, character.y, 170, 170)
                elif Character.stance == 1:
                    character.images['Walk_RF'].clip_composite_draw(0, 0, 340, 340, 0, '',
                                                                    character.x, character.y, 170, 170)
                elif Character.stance == 2:
                    character.images['Walk_HG'].clip_composite_draw(0, 0, 340, 340, 0, '',
                                                                    character.x, character.y, 170, 170)
            else:
                if Character.stance == 0:
                    character.images['Walk_SG'].clip_composite_draw(0, 0, 340, 340, 0, 'h',
                                                                    character.x, character.y, 170, 170)
                elif Character.stance == 1:
                    character.images['Walk_RF'].clip_composite_draw(0, 0, 340, 340, 0, 'h',
                                                                    character.x, character.y, 170, 170)
                elif Character.stance == 2:
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
        elif change_stance_z(e) and not Jump and not Fall and Character.state == 0:
            character.change_z()
        elif change_stance_x(e) and not Jump and not Fall and Character.state == 0:
            character.change_x()
        elif rc_down(e):
            if Character.stance == 0:
                Character.state = 1
                Character.speed = 1
        elif rc_up(e):
            if Character.stance == 0:
                Character.state = 0
                Character.speed = 3
        elif jump(e) and not Jump and not Fall:
            if not (Character.stance == 0 and Character.state == 1):
                Jump = True
                character.frame = 0
        elif temp_damage(e) and Character.hit_delay == 0:
            character.state_machine.add_event(('HIT', 0))
        elif dash(e) and Character.dash_cooldown == 0:
            character.state_machine.add_event(('USE_DASH', 0))

        if Character.stance == 0:
            if Character.state == 0:
                character.name = 'Walk_SG'
            elif Character.state == 1:
                character.name = 'Rc_SG'
        elif Character.stance == 1:
            character.name = 'Walk_RF'
        elif Character.stance == 2:
            character.name = 'Walk_HG'

        if Character.stance == 0 and Character.state == 1:
            character.frame = clamp(0, character.frame, 14)
        else:
            character.frame = clamp(0, character.frame, 6)

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        global Fall
        if Character.stance == 0 and Character.state == 1:
            character.frame = (character.frame + 14.0 * 1.5 * game_framework.frame_time) % 14
        elif not Jump and not Fall:
            character.frame = (character.frame + 6.0 * 2.0 * game_framework.frame_time) % 6

        character.x += Character.speed * character.face_dir * RUN_SPEED_PPS * game_framework.frame_time

        for block in game_world.collision_pairs['character:ground'][1] + game_world.collision_pairs['character:wall'][1]:
            if game_world.collide(character, block):
                character.x -= Character.speed * character.face_dir * RUN_SPEED_PPS * game_framework.frame_time
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
        if take_damage(e):
            character.wait_time = get_time()
            Character.hit_delay = 1
            if Character.stance == 0 and Character.state == 1:
                Character.hp = max(0, Character.hp - max(0, (8 - Character.shield_def)))
                if d_pressed or a_pressed:
                    if Character.stance == 0 and Character.state == 1:
                        character.state_machine.add_event(('CHANGE', 0))
            elif Character.state == 0:
                a_pressed = False
                d_pressed = False
                Jump = False
                jump_velocity = 10.0
                Fall = True
                character.frame = 0
                Character.hp = max(0, Character.hp - 8)
        elif right_down(e):
            d_pressed = True
            if Character.stance == 0 and Character.state == 1:
                character.state_machine.add_event(('CHANGE', 0))
        elif left_down(e):
            a_pressed = True
            if Character.stance == 0 and Character.state == 1:
                character.state_machine.add_event(('CHANGE', 0))
        elif rc_up(e):
            if Character.stance == 0 and Character.state == 1:
                Character.state = 0
                Character.speed = 3

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        if get_time() - character.wait_time > 0.5:
            character.state_machine.add_event(('TIME_OUT', 0))
        if Character.stance == 0 and Character.state == 1:
            character.frame = (character.frame + 14.0 * 1.5 * game_framework.frame_time) % 14

    @staticmethod
    def draw(character):
        if Character.state == 0:
            if character.face_dir == 1:
                if Character.stance == 0:
                    character.images['Hit_SG'].clip_composite_draw(0, 0, 340, 340, 0, '',
                                                                   character.x, character.y, 170, 170)
                elif Character.stance == 1:
                    character.images['Hit_RF'].clip_composite_draw(0, 0, 340, 340, 0, '',
                                                                   character.x, character.y, 170, 170)
                elif Character.stance == 2:
                    character.images['Hit_HG'].clip_composite_draw(0, 0, 340, 340, 0, '',
                                                                   character.x, character.y, 170, 170)
            else:
                if Character.stance == 0:
                    character.images['Hit_SG'].clip_composite_draw(0, 0, 340, 340, 0, 'h',
                                                                   character.x, character.y, 170, 170)
                elif Character.stance == 1:
                    character.images['Hit_RF'].clip_composite_draw(0, 0, 340, 340, 0, 'h',
                                                                   character.x, character.y, 170, 170)
                elif Character.stance == 2:
                    character.images['Hit_HG'].clip_composite_draw(0, 0, 340, 340, 0, 'h',
                                                                   character.x, character.y, 170, 170)
        else:
            if character.face_dir == 1:
                character.images[character.name].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '',
                                                                 character.x, character.y, 170, 170)
            else:
                character.images[character.name].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h',
                                                                 character.x, character.y, 170, 170)

class Dash:
    @staticmethod
    def enter(character, e):
        global Jump, jump_velocity, Fall, fall_velocity, d_pressed, a_pressed
        if use_dash(e):
            Jump = False
            jump_velocity = 10.0
            Fall = False
            fall_velocity = 0.0
            character.wait_time = get_time()
            Character.frame = 0
            Character.hit_delay = 0.3
            Character.dash_cooldown = 6
        elif right_up(e):
            d_pressed = False
        elif left_up(e):
            a_pressed = False
        elif rc_up(e):
            if Character.stance == 0 and Character.state == 1:
                Character.state = 0
                Character.speed = 3

    @staticmethod
    def exit(character, e):
        if time_out(e):
            if d_pressed or a_pressed:
                character.state_machine.add_event(('CHANGE', 0))

    @staticmethod
    def do(character):
        global Fall
        character.x += 20 * character.face_dir * RUN_SPEED_PPS * game_framework.frame_time

        for block in game_world.collision_pairs['character:ground'][1] + game_world.collision_pairs['character:wall'][1]:
            if game_world.collide(character, block):
                character.x -= 20 * character.face_dir * RUN_SPEED_PPS * game_framework.frame_time
                Fall = True
                character.state_machine.add_event(('TIME_OUT', 0))
                return

        if get_time() - character.wait_time > 0.15:
            Fall = True
            character.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(character):
        if character.face_dir == 1:
            if Character.stance == 0:
                character.images['Walk_SG'].clip_composite_draw(0, 0, 340, 340, 0, '',
                                                               character.x, character.y, 170, 170)
            elif Character.stance == 1:
                character.images['Walk_RF'].clip_composite_draw(0, 0, 340, 340, 0, '',
                                                               character.x, character.y, 170, 170)
            elif Character.stance == 2:
                character.images['Walk_HG'].clip_composite_draw(0, 0, 340, 340, 0, '',
                                                               character.x, character.y, 170, 170)
        else:
            if Character.stance == 0:
                character.images['Walk_SG'].clip_composite_draw(0, 0, 340, 340, 0, 'h',
                                                               character.x, character.y, 170, 170)
            elif Character.stance == 1:
                character.images['Walk_RF'].clip_composite_draw(0, 0, 340, 340, 0, 'h',
                                                               character.x, character.y, 170, 170)
            elif Character.stance == 2:
                character.images['Walk_HG'].clip_composite_draw(0, 0, 340, 340, 0, 'h',
                                                               character.x, character.y, 170, 170)

animation_names = ['Idle_SG', 'Walk_SG', 'Hit_SG', 'Die_SG', 'Rc_SG',
                   'Idle_RF', 'Walk_RF', 'Hit_RF', 'Die_RF',
                   'Idle_HG', 'Walk_HG', 'Hit_HG', 'Die_HG']

class Character:
    images = None
    stance = 0
    state = 0
    speed = 3
    hp = 20
    max_hp = 20
    bullet_SG = 8
    bullet_RF = 4
    max_bullet_HG = 20
    bullet_HG = max_bullet_HG
    shield_def = 1
    hit_delay = 0 # 피격 면역
    dash_cooldown = 0 # 대쉬 쿨타임 6초

    def load_images(self):
        if Character.images == None:
            Character.images = {}
            for name in animation_names:
                if name == 'Idle_SG':
                    Character.images[name] = load_image("./HKCAWS/" + name + ".png")
                elif name == 'Walk_SG':
                    Character.images[name] = load_image("./HKCAWS/" + name + ".png")
                elif name == 'Hit_SG':
                    Character.images[name] = load_image("./HKCAWS/" + name + ".png")
                elif name == 'Die_SG':
                    Character.images[name] = load_image("./HKCAWS/" + name + ".png")
                elif name == 'Rc_SG':
                    Character.images[name] = load_image("./HKCAWS/" + name + ".png")

                elif name == 'Idle_RF':
                    Character.images[name] = load_image("./R93/" + name + ".png")
                elif name == 'Walk_RF':
                    Character.images[name] = load_image("./R93/" + name + ".png")
                elif name == 'Hit_RF':
                    Character.images[name] = load_image("./R93/" + name + ".png")
                elif name == 'Die_RF':
                    Character.images[name] = load_image("./R93/" + name + ".png")

                elif name == 'Idle_HG':
                    Character.images[name] = load_image("./GSH18Mod/" + name + ".png")
                elif name == 'Walk_HG':
                    Character.images[name] = load_image("./GSH18Mod/" + name + ".png")
                elif name == 'Hit_HG':
                    Character.images[name] = load_image("./GSH18Mod/" + name + ".png")
                elif name == 'Die_HG':
                    Character.images[name] = load_image("./GSH18Mod/" + name + ".png")

    def __init__(self):
        self.x, self.y = 34, 140.0
        self.face_dir = 1
        self.frame = 0
        self.ball_count = 10
        self.load_images()
        self.name = ''
        self.delay = 0
        self.Lshift_cool = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {
                    right_down: Walk, left_down: Walk, left_up: Idle, right_up: Idle, change_stance_z: Idle, change_stance_x: Idle,
                    change: Walk, jump: Idle, rc_down: Idle, rc_up: Idle, dash: Idle, use_dash: Dash,
                    temp_damage: Idle, take_damage: Hit
                },
                Walk: {
                    right_down: Walk, left_down: Walk, right_up: Walk, left_up: Walk, change_stance_z: Walk, change_stance_x: Walk,
                    change: Idle, jump: Walk, rc_down: Walk, rc_up: Walk, dash: Walk, use_dash: Dash,
                    temp_damage: Walk, take_damage: Hit
                },
                Hit: {
                    right_down: Hit, left_down: Hit, rc_up: Hit, time_out: Idle,
                    change: Walk,
                },
                Dash: {
                    left_up: Dash, right_up: Dash, rc_up: Dash, time_out: Idle, change: Walk
                },
            }
        )

    def update(self):
        global Jump, jump_velocity, Fall, fall_velocity
        self.state_machine.update()
        self.x = clamp(17, self.x, 1063)

        if Jump:
            self.y += jump_velocity * RUN_SPEED_PPS * game_framework.frame_time
            jump_velocity -= gravity * RUN_SPEED_PPS * game_framework.frame_time
            if jump_velocity <= 0:
                Jump = False
                Fall = True
                jump_velocity = 10.0

        if Fall:
            self.y -= fall_velocity * RUN_SPEED_PPS * game_framework.frame_time
            fall_velocity += gravity * RUN_SPEED_PPS * game_framework.frame_time

        if not Character.hit_delay == 0:
            if self.delay == 0:
                self.delay = get_time()
            if get_time() - self.delay > Character.hit_delay:
                Character.hit_delay = 0
                self.delay = 0

        if not Character.dash_cooldown == 0:
            if self.Lshift_cool == 0:
                self.Lshift_cool = get_time()
            if get_time() - self.Lshift_cool > Character.dash_cooldown:
                Character.dash_cooldown = 0
                self.Lshift_cool = 0

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def change_z(self):
        if Character.stance == 0:
            Character.stance = 1
            Character.speed = 4
        elif Character.stance == 1:
            Character.stance = 2
            Character.speed = 5
        elif Character.stance == 2:
            Character.stance = 0
            Character.speed = 3

    def change_x(self):
        if Character.stance == 0:
            Character.stance = 2
            Character.speed = 5
        elif Character.stance == 1:
            Character.stance = 0
            Character.speed = 3
        elif Character.stance == 2:
            Character.stance = 1
            Character.speed = 4

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
            jump_velocity = 10.0