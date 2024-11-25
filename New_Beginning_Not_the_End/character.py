from pico2d import get_time, load_image, draw_rectangle, clamp

import game_world
import game_framework
import server
import ground

from state_machine import *

PIXEL_PER_METER = (30.0 / 1)  # 30 pixel 1 m
RUN_SPEED_KMPH = 10.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

a_pressed = False
d_pressed = False
w_pressed = False
s_pressed = False
Move = False
Jump = False
Fall = False
Climb = False
Attack = False
attacking = False
Reload_SG = False
Reload_RF = False
rrf = False
Reload_HG = False

jump_velocity = 10.0
fall_velocity = 0.0
gravity = 0.5
mouse_x, mouse_y = 0, 0
screen_left = 0
screen_right = 1080

RectMode = False

class Idle:
    @staticmethod
    def enter(character, e):
        global Jump, d_pressed, a_pressed, attacking, Reload_SG, Reload_HG, s_pressed, w_pressed, RectMode
        if start_event(e):
            character.face_dir = 1
        elif right_up(e):
            d_pressed = False
        elif left_up(e):
            a_pressed = False
        elif walk(e):
            if a_pressed or d_pressed:
                character.state_machine.add_event(('WALK', 0))
        elif on_down(e):
            w_pressed = True
        elif on_up(e):
            w_pressed = False
        elif under_down(e):
            s_pressed = True
        elif under_up(e):
            s_pressed = False
        elif change_stance_z(e) and not Jump and not Fall and not Attack and Character.state == 0 and not Reload_SG and not Reload_HG:
            character.change_z()
        elif change_stance_x(e) and not Jump and not Fall and not Attack and Character.state == 0 and not Reload_SG and not Reload_HG:
            character.change_x()
        elif lc_down(e):
            attacking = True
        elif lc_up(e):
            attacking = False
        elif rc_down(e):
            if Character.stance == 0:
                Character.state = 1
                Character.speed = 1
        elif rc_up(e):
            if Character.stance == 0:
                Character.state = 0
                if not Reload_SG:
                    Character.speed = 3
        elif jump(e) and not Jump and not Fall:
            if Character.stance == 0 and Character.state == 0:
                Jump = True
                if not Attack and not Reload_SG:
                    character.frame = 0
            elif Character.stance == 1 and Character.state == 0:
                if not Attack:
                    Jump = True
                    character.frame = 0
            elif Character.stance == 2:
                Jump = True
                if not Attack and not Reload_HG:
                    character.frame = 0
        elif temp_damage(e) and Character.hit_delay == 0:
            Character.damage = 8
            character.state_machine.add_event(('HIT', 0))
        elif dash(e) and Character.dash_cooldown == 0 and not Reload_SG and not Reload_HG:
            character.state_machine.add_event(('USE_DASH', 0))
        elif reload(e):
            if Character.stance == 0 and Character.bullet_SG == 0 and Character.state <= 1:
                if not Reload_SG:
                    Reload_SG = True
                    Character.speed = 1
                    character.frame = 0
                    character.reload_time = get_time()
            elif Character.stance == 1 and Character.bullet_RF == 0 and Character.state == 0:
                if s_pressed:
                    character.state_machine.add_event(('RF_RELOAD_S', 0))
                elif not s_pressed:
                    character.state_machine.add_event(('RF_RELOAD', 0))
            elif Character.stance == 2 and Character.bullet_HG == 0 and Character.state == 0:
                if not Reload_HG:
                    Reload_HG = True
                    Character.speed = 7
                    character.frame = 0
                    Character.hit_delay = 0.5
                    character.reload_time = get_time()

        elif temp_more(e):
            Character.max_hp += 2
        elif temp_heal(e):
            Character.hp = min(Character.hp + 1, Character.max_hp)
        elif temp_bullet(e):
            Character.bullet_SG = 0
            Character.bullet_RF = 0
            Character.bullet_HG = 0
        elif temp_reset_cool(e):
            Character.dash_cooldown = 0
            character.Lshift_cool = 0
        elif temp_rectmode(e):
           RectMode = not RectMode

        if Character.stance == 0 and not Reload_SG:
            if Character.state == 0:
                if character.name != 'Idle_SG':
                    character.name = 'Idle_SG'
            elif Character.state == 1:
                if character.name != 'Rc_SG':
                    character.name = 'Rc_SG'
            character.frame = clamp(0, character.frame, 13)
        elif Character.stance == 0 and Reload_SG:
            if character.name != 'Reload_SG':
                character.name = 'Reload_SG'
        elif Character.stance == 1:
            if character.name != 'Idle_RF':
                character.name = 'Idle_RF'
            character.frame = clamp(0, character.frame, 13)
        elif Character.stance == 2 and not Reload_HG:
            if character.name != 'Idle_HG':
                character.name = 'Idle_HG'
            character.frame = clamp(0, character.frame, 10)
        elif Character.stance == 2 and Reload_HG:
            if character.name != 'Reload_HG':
                character.name = 'Reload_HG'

    @staticmethod
    def exit(character, e):
        if right_down(e):
            character.face_dir = 1
        elif left_down(e):
            character.face_dir = -1

    @staticmethod
    def do(character):
        global Move, mouse_x
        if Attack:
            if character.frame == 0:
                if character.x > 1080:
                    mouse_x += character.x - 1080 // 2
                if mouse_x > character.x:
                    character.attack_dir = 1
                    character.face_dir = 1
                elif mouse_x< character.x:
                    character.attack_dir = -1
                    character.face_dir = -1
            if Character.stance == 0:
                character.frame = (character.frame + 15.0 * 0.8 * game_framework.frame_time) % 15
            elif Character.stance == 1:
                character.frame = (character.frame + 7.0 * 2.0 * game_framework.frame_time) % 7
            elif Character.stance == 2:
                character.frame = (character.frame + 5.0 * 3.0 * game_framework.frame_time) % 5

        elif Reload_SG:
            character.frame = (character.frame + 16.0 * 0.7 * game_framework.frame_time) % 16

        elif Reload_HG:
            character.frame = (character.frame + 10.0 * 1.8 * game_framework.frame_time) % 10

        elif not Jump and not Fall:
            if Move:
                Move = False
            if Character.stance == 0 or Character.stance == 1:
                character.frame = (character.frame + 14.0 * 1.5 * game_framework.frame_time) % 14
            elif Character.stance == 2:
                character.frame = (character.frame + 11.0 * 1.5 * game_framework.frame_time) % 11

        if Climb:
            if w_pressed and not s_pressed:
                if not Move:
                    Move = True
                character.y += Character.speed * RUN_SPEED_PPS * game_framework.frame_time / 2
                for block in game_world.collision_pairs['server.character:ground'][1]:
                    if screen_left - 15 <= block.x <= screen_right + 15:
                        if game_world.collide(character, block):
                            character.y -= Character.speed * RUN_SPEED_PPS * game_framework.frame_time / 2
                            return
            elif s_pressed and not w_pressed:
                if not Move:
                    Move = True
                character.y -= Character.speed * RUN_SPEED_PPS * game_framework.frame_time / 2
                for block in game_world.collision_pairs['server.character:ground'][1]:
                    if screen_left - 15 <= block.x <= screen_right + 15:
                        if game_world.collide(character, block):
                            character.y += Character.speed * RUN_SPEED_PPS * game_framework.frame_time / 2
                            return

    @staticmethod
    def draw(character):
        if Attack:
            if character.attack_dir == 1:
                if Character.stance == 0:
                    character.images['Attack_SG'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '',
                                                                      character.sx, character.y, 170, 170)
                elif Character.stance == 1:
                    character.images['Attack_RF'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '',
                                                                      character.sx, character.y, 170, 170)
                elif Character.stance == 2:
                    character.images['Attack_HG'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '',
                                                                      character.sx, character.y, 170, 170)
            elif character.attack_dir == -1:
                if Character.stance == 0:
                    character.images['Attack_SG'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h',
                                                                      character.sx, character.y, 170, 170)
                elif Character.stance == 1:
                    character.images['Attack_RF'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h',
                                                                      character.sx, character.y, 170, 170)
                elif Character.stance == 2:
                    character.images['Attack_HG'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h',
                                                                      character.sx, character.y, 170, 170)
        elif Reload_SG:
            if character.face_dir == 1:
                character.images[character.name].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '',
                                                                  character.sx, character.y, 170, 170)
            elif character.face_dir == -1:
                character.images[character.name].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h',
                                                                  character.sx, character.y, 170, 170)
        elif Reload_HG:
            if character.face_dir == 1:
                if 0 <= int(character.frame) <= 4:
                    roll = 60 - int(character.frame) * 15
                else:
                    roll = -15
                character.images[character.name].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '',
                                                                     character.sx + roll, character.y, 170, 170)

            elif character.face_dir == -1:
                if 0 <= int(character.frame) <= 4:
                    roll = 60 - int(character.frame) * 15
                else:
                    roll = -15
                character.images[character.name].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h',
                                                                     character.sx - roll, character.y, 170, 170)

        elif Jump or Fall:
            if character.face_dir == 1:
                if Character.stance == 0:
                    character.images['Walk_SG'].clip_composite_draw(0, 0, 340, 340, 0, '',
                                                                         character.sx, character.y, 170, 170)
                elif Character.stance == 1:
                    character.images['Walk_RF'].clip_composite_draw(0, 0, 340, 340, 0, '',
                                                                    character.sx, character.y, 170, 170)
                elif Character.stance == 2:
                    character.images['Walk_HG'].clip_composite_draw(0, 0, 340, 340, 0, '',
                                                                    character.sx, character.y, 170, 170)
            elif character.face_dir == -1:
                if Character.stance == 0:
                    character.images['Walk_SG'].clip_composite_draw(0, 0, 340, 340, 0, 'h',
                                                                    character.sx, character.y, 170, 170)
                elif Character.stance == 1:
                    character.images['Walk_RF'].clip_composite_draw(0, 0, 340, 340, 0, 'h',
                                                                    character.sx, character.y, 170, 170)
                elif Character.stance == 2:
                    character.images['Walk_HG'].clip_composite_draw(0, 0, 340, 340, 0, 'h',
                                                                    character.sx, character.y, 170, 170)
        else:
            if character.face_dir == 1:
                character.images[character.name].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '',
                                                                     character.sx, character.y, 170, 170)
            elif character.face_dir == -1:
                character.images[character.name].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h',
                                                                     character.sx, character.y, 170, 170)
class Walk:
    @staticmethod
    def enter(character, e):
        global a_pressed, d_pressed, Jump, attacking, Reload_SG, Reload_HG, s_pressed, w_pressed, RectMode
        if right_down(e):
            d_pressed = True
            character.face_dir = 1
        elif right_up(e):
            d_pressed = False
            if a_pressed:
                character.face_dir = -1
            elif not a_pressed:
                character.state_machine.add_event(('IDLE', 0))
        elif left_down(e):
            a_pressed = True
            character.face_dir = -1
        elif left_up(e):
            a_pressed = False
            if d_pressed:
                character.face_dir = 1
            elif not d_pressed:
                character.state_machine.add_event(('IDLE', 0))
        elif on_down(e):
            w_pressed = True
        elif on_up(e):
            w_pressed = False
            if not d_pressed and not a_pressed and not s_pressed and Climb:
                character.state_machine.add_event(('IDLE', 0))
        elif under_down(e):
            s_pressed = True
        elif under_up(e):
            s_pressed = False
            if not d_pressed and not a_pressed and not w_pressed and Climb:
                character.state_machine.add_event(('IDLE', 0))
        elif change_stance_z(e) and not Jump and not Fall and not Attack and Character.state == 0 and not Reload_SG and not Reload_HG:
            character.change_z()
        elif change_stance_x(e) and not Jump and not Fall and not Attack and Character.state == 0 and not Reload_SG and not Reload_HG:
            character.change_x()
        elif lc_down(e):
            attacking = True
        elif lc_up(e):
            attacking = False
        elif rc_down(e):
            if Character.stance == 0:
                Character.state = 1
                Character.speed = 1
        elif rc_up(e):
            if Character.stance == 0:
                Character.state = 0
                if not Reload_SG:
                    Character.speed = 3
        elif jump(e) and not Jump and not Fall:
            if Character.stance == 0 and Character.state == 0:
                Jump = True
                if not Attack and not Reload_SG:
                    character.frame = 0
            elif Character.stance == 1 and Character.state == 0:
                if not Attack:
                    Jump = True
                    character.frame = 0
            elif Character.stance == 2:
                Jump = True
                if not Attack and not Reload_HG:
                    character.frame = 0
        elif temp_damage(e) and Character.hit_delay == 0:
            Character.damage = 8
            character.state_machine.add_event(('HIT', 0))
        elif dash(e) and Character.dash_cooldown == 0 and not Reload_SG and not Reload_HG:
            character.state_machine.add_event(('USE_DASH', 0))
        elif reload(e):
            if Character.stance == 0 and Character.bullet_SG == 0 and Character.state <= 1:
                if not Reload_SG:
                    Reload_SG = True
                    Character.speed = 1
                    character.frame = 0
                    character.reload_time = get_time()
            elif Character.stance == 1 and Character.bullet_RF == 0 and Character.state == 0:
                if s_pressed:
                    character.state_machine.add_event(('RF_RELOAD_S', 0))
                elif not s_pressed:
                    character.state_machine.add_event(('RF_RELOAD', 0))
            elif Character.stance == 2 and Character.bullet_HG == 0 and Character.state == 0:
                if not Reload_HG:
                    Reload_HG = True
                    Character.speed = 7
                    character.frame = 0
                    Character.hit_delay = 0.5
                    character.reload_time = get_time()

        elif temp_more(e):
            Character.max_hp += 2
        elif temp_heal(e):
            Character.hp = min(Character.hp + 1, Character.max_hp)
        elif temp_bullet(e):
            Character.bullet_SG = 0
            Character.bullet_RF = 0
            Character.bullet_HG = 0
        elif temp_reset_cool(e):
            Character.dash_cooldown = 0
            character.Lshift_cool = 0
        elif temp_rectmode(e):
           RectMode = not RectMode

        if Character.stance == 0 and not Reload_SG:
            if Character.state == 0:
                if character.name != 'Walk_SG':
                    character.name = 'Walk_SG'
            elif Character.state == 1:
                if character.name != 'Rc_SG':
                    character.name = 'Rc_SG'
        elif Character.stance == 0 and Reload_SG:
            if character.name != 'Reload_SG':
                character.name = 'Reload_SG'
        elif Character.stance == 1:
            if character.name != 'Walk_RF':
                character.name = 'Walk_RF'
        elif Character.stance == 2 and not Reload_HG:
            if character.name != 'Walk_HG':
                character.name = 'Walk_HG'
        elif Character.stance == 2 and Reload_HG:
            if character.name != 'Reload_HG':
                character.name = 'Reload_HG'

        if Character.stance == 0 and Character.state == 1:
            character.frame = clamp(0, character.frame, 13)
        else:
            character.frame = clamp(0, character.frame, 5)

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        global Fall, Move, mouse_x, Climb
        if not Move:
            Move = True

        if Attack:
            if character.frame == 0 and not Character.stance == 1:
                if character.x > 1080:
                    mouse_x += character.x - 1080 // 2
                if mouse_x > character.x:
                    character.attack_dir = 1
                elif mouse_x < character.x:
                    character.attack_dir = -1
            if Character.stance == 0:
                character.frame = (character.frame + 15.0 * 0.8 * game_framework.frame_time) % 15
            elif Character.stance == 1:
                character.frame = (character.frame + 7.0 * 2.0 * game_framework.frame_time) % 7
            elif Character.stance == 2:
                character.frame = (character.frame + 5.0 * 3.0 * game_framework.frame_time) % 5

        elif Reload_SG:
            character.frame = (character.frame + 16.0 * 0.7 * game_framework.frame_time) % 16

        elif Reload_HG:
            character.frame = (character.frame + 10.0 * 1.8 * game_framework.frame_time) % 10

        else:
            if Character.stance == 0 and Character.state == 1:
                character.frame = (character.frame + 14.0 * 1.5 * game_framework.frame_time) % 14
            elif not Jump and not Fall:
                character.frame = (character.frame + 6.0 * 2.0 * game_framework.frame_time) % 6

        if Climb:
            if w_pressed and not s_pressed:
                character.y += Character.speed * RUN_SPEED_PPS * game_framework.frame_time / 2
                for block in game_world.collision_pairs['server.character:ground'][1]:
                    if screen_left - 15 <= block.x <= screen_right + 15:
                        if game_world.collide(character, block):
                            character.y -= Character.speed * RUN_SPEED_PPS * game_framework.frame_time / 2
                            return
            elif s_pressed and not w_pressed:
                character.y -= Character.speed * RUN_SPEED_PPS * game_framework.frame_time / 2
                for block in game_world.collision_pairs['server.character:ground'][1]:
                    if screen_left - 15 <= block.x <= screen_right + 15:
                        if game_world.collide(character, block):
                            character.y += Character.speed * RUN_SPEED_PPS * game_framework.frame_time / 2
                            return

        if d_pressed or a_pressed:
            if Character.stance == 0:
                if not Attack:
                    character.x += Character.speed * character.face_dir * RUN_SPEED_PPS * game_framework.frame_time
            elif Character.stance == 1:
                if Character.state == 0 and not Attack:
                    character.x += Character.speed * character.face_dir * RUN_SPEED_PPS * game_framework.frame_time
            elif Character.stance == 2:
                if not Character.state == 1:
                    character.x += Character.speed * character.face_dir * RUN_SPEED_PPS * game_framework.frame_time

            for block in game_world.collision_pairs['server.character:ground'][1] + game_world.collision_pairs['server.character:wall'][1]:
                if screen_left - 15 <= block.x <= screen_right + 15:
                    if game_world.collide(character, block):
                        character.x -= Character.speed * character.face_dir * RUN_SPEED_PPS * game_framework.frame_time
                        return

            ground_objects = game_world.collision_pairs['server.character:ground'][1]
            for block in ground_objects:
                if screen_left - 15 <= block.x <= screen_right + 15:
                    if game_world.collide_ad(character, block, ground_objects):
                        Fall = True
                        print('collide_ad')
                        return

            for block in game_world.collision_pairs['server.character:ladder'][1]:
                if screen_left - 15 <= block.x <= screen_right + 15:
                    if game_world.collide_ladder(character, block):
                        Fall = True
                        Climb = False
                        print('collide_ladder')
                        return

    @staticmethod
    def draw(character):
        if Attack:
            if character.attack_dir == 1:
                if Character.stance == 0:
                    character.images['Attack_SG'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '',
                                                                      character.sx, character.y, 170, 170)
                elif Character.stance == 1:
                    character.images['Attack_RF'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '',
                                                                      character.sx, character.y, 170, 170)
                elif Character.stance == 2:
                    character.images['Attack_HG'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '',
                                                                      character.sx, character.y, 170, 170)
            elif character.attack_dir == -1:
                if Character.stance == 0:
                    character.images['Attack_SG'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h',
                                                                      character.sx, character.y, 170, 170)
                elif Character.stance == 1:
                    character.images['Attack_RF'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h',
                                                                      character.sx, character.y, 170, 170)
                elif Character.stance == 2:
                    character.images['Attack_HG'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h',
                                                                      character.sx, character.y, 170, 170)
        elif Reload_SG:
            if character.face_dir == 1:
                character.images[character.name].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '',
                                                                  character.sx, character.y, 170, 170)
            elif character.face_dir == -1:
                character.images[character.name].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h',
                                                                  character.sx, character.y, 170, 170)
        elif Reload_HG:
            if character.face_dir == 1:
                if 0 <= int(character.frame) <= 4:
                    roll = 60 - int(character.frame) * 15
                else:
                    roll = -15
                character.images[character.name].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '',
                                                                     character.sx + roll, character.y, 170, 170)
            elif character.face_dir == -1:
                if 0 <= int(character.frame) <= 4:
                    roll = 60 - int(character.frame) * 15
                else:
                    roll = -15
                character.images[character.name].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h',
                                                                     character.sx - roll, character.y, 170, 170)

        else:
            if character.face_dir == 1:
                character.images[character.name].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '',
                                                                     character.sx, character.y, 170, 170)
            elif character.face_dir == -1:
                character.images[character.name].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h',
                                                                     character.sx, character.y, 170, 170)

class Hit:
    @staticmethod
    def enter(character, e):
        global a_pressed, d_pressed, Jump, jump_velocity, Fall, attacking, s_pressed, w_pressed
        if take_hit(e):
            if Character.stance == 0 and (Character.state == 1 or Reload_SG):
                Character.hp = max(0, Character.hp - max(0, (Character.damage - Character.shield_def)))
                if Character.hp == 0:
                    Character.speed = 3
                    character.state_machine.add_event(('DIE', 0))
                elif a_pressed or d_pressed:
                    character.state_machine.add_event(('WALK', 0))
            elif Character.state == 0:
                a_pressed = False
                d_pressed = False
                if Climb:
                    w_pressed = False
                    s_pressed = False
                Jump = False
                jump_velocity = 10.0
                Fall = True
                if not Attack:
                    character.frame = 0
                Character.hp = max(0, Character.hp - Character.damage)
                if Character.hp == 0:
                    Character.score -= 100
                    character.state_machine.add_event(('DIE', 0))
            character.wait_time = get_time()
            Character.hit_delay = 1
        elif lc_down(e):
            attacking = True
        elif lc_up(e):
            attacking = False
        elif right_down(e):
            d_pressed = True
            if Character.stance == 0 and Character.state == 1:
                character.state_machine.add_event(('WALK', 0))
        elif left_down(e):
            a_pressed = True
            if Character.stance == 0 and Character.state == 1:
                character.state_machine.add_event(('WALK', 0))
        elif on_down(e):
            w_pressed = True
        elif on_up(e):
            w_pressed = False
        elif under_down(e):
            s_pressed = True
        elif under_up(e):
            s_pressed = False
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
        if Attack:
            if Character.stance == 0:
                character.frame = (character.frame + 15.0 * 0.8 * game_framework.frame_time) % 15
            elif Character.stance == 1:
                character.frame = (character.frame + 7.0 * 2.0 * game_framework.frame_time) % 7
            elif Character.stance == 2:
                character.frame = (character.frame + 5.0 * 3.0 * game_framework.frame_time) % 5
        elif Reload_SG:
            character.frame = (character.frame + 16.0 * 1.0 * game_framework.frame_time) % 16
        else:
            if Character.stance == 0 and Character.state == 1:
                character.frame = (character.frame + 14.0 * 1.5 * game_framework.frame_time) % 14

    @staticmethod
    def draw(character):
        if Attack:
            if character.attack_dir == 1:
                if Character.stance == 0:
                    character.images['Attack_SG'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '',
                                                                      character.sx, character.y, 170, 170)
                elif Character.stance == 1:
                    character.images['Attack_RF'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '',
                                                                      character.sx, character.y, 170, 170)
                elif Character.stance == 2:
                    character.images['Attack_HG'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '',
                                                                      character.sx, character.y, 170, 170)
            elif character.attack_dir == -1:
                if Character.stance == 0:
                    character.images['Attack_SG'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h',
                                                                      character.sx, character.y, 170, 170)
                elif Character.stance == 1:
                    character.images['Attack_RF'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h',
                                                                      character.sx, character.y, 170, 170)
                elif Character.stance == 2:
                    character.images['Attack_HG'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h',
                                                                      character.sx, character.y, 170, 170)
        elif Character.state == 0 and not Reload_SG and not Reload_HG:
            if character.face_dir == 1:
                if Character.stance == 0:
                    character.images['Hit_SG'].clip_composite_draw(0, 0, 340, 340, 0, '',
                                                                   character.sx, character.y, 170, 170)
                elif Character.stance == 1:
                    character.images['Hit_RF'].clip_composite_draw(0, 0, 340, 340, 0, '',
                                                                   character.sx, character.y, 170, 170)
                elif Character.stance == 2:
                    character.images['Hit_HG'].clip_composite_draw(0, 0, 340, 340, 0, '',
                                                                   character.sx, character.y, 170, 170)
            elif character.face_dir == -1:
                if Character.stance == 0:
                    character.images['Hit_SG'].clip_composite_draw(0, 0, 340, 340, 0, 'h',
                                                                   character.sx, character.y, 170, 170)
                elif Character.stance == 1:
                    character.images['Hit_RF'].clip_composite_draw(0, 0, 340, 340, 0, 'h',
                                                                   character.sx, character.y, 170, 170)
                elif Character.stance == 2:
                    character.images['Hit_HG'].clip_composite_draw(0, 0, 340, 340, 0, 'h',
                                                                   character.sx, character.y, 170, 170)
        else:
            if character.face_dir == 1:
                character.images[character.name].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '',
                                                                 character.sx, character.y, 170, 170)
            elif character.face_dir == -1:
                character.images[character.name].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h',
                                                                 character.sx, character.y, 170, 170)

class Die:
    @staticmethod
    def enter(character, e):
        global a_pressed, d_pressed, Jump, jump_velocity, Fall, fall_velocity, Attack, attacking, Move, s_pressed, w_pressed
        global Reload_SG, Reload_RF, rrf, Reload_HG, Climb
        if die(e):
            Move = False
            Jump = False
            Fall = False
            Climb = False
            Attack = False
            attacking = False
            a_pressed = False
            d_pressed = False
            w_pressed = False
            s_pressed = False
            Reload_SG = False
            Reload_RF = False
            rrf = False
            Reload_HG = False
            jump_velocity = 10.0
            fall_velocity = 0.0
            character.frame = 0
            Character.state = 0
            Character.attack_delay = 0
            character.attack_cool = 0
            character.attack_time = 0
            character.hit_cool = 0
            character.reload_time = 0
            character.wait_time = get_time()

    @staticmethod
    def exit(character, e):
        if time_out(e):
            character.x, character.y = 34, 140.0
            server.background.window_left = 0
            Character.hit_delay = 1
            if Character.stance == 0:
                Character.speed = 3
            elif Character.stance == 1:
                Character.speed = 4
            elif Character.stance == 2:
                Character.speed = 5
            if Character.hp == 0:
                Character.hp = Character.max_hp
                Character.bullet_SG = 8
                Character.bullet_RF = 4
                Character.bullet_HG = Character.max_bullet_HG

    @staticmethod
    def do(character):
        if get_time() - character.wait_time > 3:
            character.state_machine.add_event(('TIME_OUT', 0))
        if Character.stance == 0 or Character.stance == 1:
            character.frame = character.frame + 18.0 * 1.0 * game_framework.frame_time
        elif Character.stance == 2:
            character.frame = character.frame + 21.0 * 0.6 * game_framework.frame_time

    @staticmethod
    def draw(character):
        if character.face_dir == 1:
            if Character.stance == 0:
                character.images['Die_SG'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '',
                                                               character.sx - 48, character.y, 170, 170)
            elif Character.stance == 1:
                character.images['Die_RF'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '',
                                                               character.sx - 11, character.y, 170, 170)
            elif Character.stance == 2:
                character.images['Die_HG'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, '',
                                                               character.sx, character.y, 170, 170)
        elif character.face_dir == -1:
            if Character.stance == 0:
                character.images['Die_SG'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h',
                                                               character.sx + 48, character.y, 170, 170)
            elif Character.stance == 1:
                character.images['Die_RF'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h',
                                                               character.sx + 11, character.y, 170, 170)
            elif Character.stance == 2:
                character.images['Die_HG'].clip_composite_draw(int(character.frame) * 340, 0, 340, 340, 0, 'h',
                                                               character.sx, character.y, 170, 170)

class Dash:
    @staticmethod
    def enter(character, e):
        global Jump, jump_velocity, Fall, fall_velocity, d_pressed, a_pressed, attacking, s_pressed, w_pressed, Climb
        if use_dash(e):
            Jump = False
            jump_velocity = 10.0
            Fall = False
            fall_velocity = 0.0
            Climb = False
            character.wait_time = get_time()
            Character.hit_delay = 0.3
            Character.dash_cooldown = 6
            if not Attack:
                Character.frame = 0
                Character.attack_delay = 0
                character.attack_cool = 0
                character.attack_time = 0
        elif right_up(e):
            d_pressed = False
        elif left_up(e):
            a_pressed = False
        elif on_up(e):
            w_pressed = False
        elif under_up(e):
            s_pressed = False
        elif lc_up(e):
            attacking = False
        elif rc_up(e):
            if Character.stance == 0 and Character.state == 1:
                Character.state = 0
                Character.speed = 3

    @staticmethod
    def exit(character, e):
        global Reload_RF
        if time_out(e):
            if d_pressed or a_pressed:
                character.state_machine.add_event(('WALK', 0))

    @staticmethod
    def do(character):
        global Fall
        if Attack:
            if Character.stance == 0:
                character.frame = (character.frame + 15.0 * 0.8 * game_framework.frame_time) % 15
            elif Character.stance == 1:
                character.frame = (character.frame + 7.0 * 2.0 * game_framework.frame_time) % 7
            elif Character.stance == 2:
                character.frame = (character.frame + 5.0 * 3.0 * game_framework.frame_time) % 5

        character.x += 20 * character.face_dir * RUN_SPEED_PPS * game_framework.frame_time

        for block in game_world.collision_pairs['server.character:ground'][1] + game_world.collision_pairs['server.character:wall'][1]:
            if screen_left - 15 <= block.x <= screen_right + 15:
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
                                                               character.sx, character.y, 170, 170)
            elif Character.stance == 1:
                character.images['Walk_RF'].clip_composite_draw(0, 0, 340, 340, 0, '',
                                                               character.sx, character.y, 170, 170)
            elif Character.stance == 2:
                character.images['Walk_HG'].clip_composite_draw(0, 0, 340, 340, 0, '',
                                                               character.sx, character.y, 170, 170)
        elif character.face_dir == -1:
            if Character.stance == 0:
                character.images['Walk_SG'].clip_composite_draw(0, 0, 340, 340, 0, 'h',
                                                               character.sx, character.y, 170, 170)
            elif Character.stance == 1:
                character.images['Walk_RF'].clip_composite_draw(0, 0, 340, 340, 0, 'h',
                                                               character.sx, character.y, 170, 170)
            elif Character.stance == 2:
                character.images['Walk_HG'].clip_composite_draw(0, 0, 340, 340, 0, 'h',
                                                               character.sx, character.y, 170, 170)

class RRF:
    @staticmethod
    def enter(character, e):
        global d_pressed, a_pressed, attacking, Reload_RF, rrf, s_pressed, w_pressed
        if rf_reload(e) and not Reload_RF:
            Reload_RF = True
            character.wait_time = get_time()
            rrf = False
            character.name = 'Attack_RF'
            character.frame = 0
        elif right_up(e):
            d_pressed = False
        elif left_up(e):
            a_pressed = False
        elif on_up(e):
            w_pressed = False
        elif under_up(e):
            s_pressed = False
        elif lc_up(e):
            attacking = False

    @staticmethod
    def exit(character, e):
        global Fall, Reload_RF
        if time_out(e):
            Fall = True
            Reload_RF = False
            Character.bullet_RF = 4
            Character.hit_delay = 0.1
            if d_pressed or a_pressed:
                character.state_machine.add_event(('WALK', 0))

    @staticmethod
    def do(character):
        global Jump, jump_velocity, Fall, fall_velocity, Reload_RF, rrf

        if get_time() - character.wait_time > 0.4:
            character.state_machine.add_event(('TIME_OUT', 0))

        elif get_time() - character.wait_time > 0.35:
            character.name = 'Walk_RF'

        elif get_time() - character.wait_time > 0.25:
            character.frame = 0

        if get_time() - character.wait_time > 0.15:
            if not rrf:
                Jump = True
                jump_velocity = 6.0
                Fall = False
                fall_velocity = 0.0
                rrf = True
                character.frame = 1
            character.x -= 8 * character.face_dir * RUN_SPEED_PPS * game_framework.frame_time

        for block in game_world.collision_pairs['server.character:ground'][1] + game_world.collision_pairs['server.character:wall'][1]:
            if screen_left - 15 <= block.x <= screen_right + 15:
                if game_world.collide(character, block):
                    character.x += 8 * character.face_dir * RUN_SPEED_PPS * game_framework.frame_time
                    Fall = True
                    return

    @staticmethod
    def draw(character):
        if character.face_dir == 1:
            character.images[character.name].clip_composite_draw(character.frame * 340, 0, 340, 340, 0, '',
                                                                 character.sx, character.y, 170, 170)
        elif character.face_dir == -1:
            character.images[character.name].clip_composite_draw(character.frame * 340, 0, 340, 340, 0, 'h',
                                                                 character.sx, character.y, 170, 170)

class RsRF:
    @staticmethod
    def enter(character, e):
        global d_pressed, a_pressed, attacking, Reload_RF, rrf, s_pressed, w_pressed
        if rf_reload_s(e) and not Reload_RF:
            Reload_RF = True
            character.wait_time = get_time()
            rrf = False
            character.name = 'Attack_RF'
            character.frame = 0
        elif right_up(e):
            d_pressed = False
        elif left_up(e):
            a_pressed = False
        elif on_up(e):
            w_pressed = False
        elif under_up(e):
            s_pressed = False
        elif lc_up(e):
            attacking = False

    @staticmethod
    def exit(character, e):
        global Fall, Reload_RF
        if time_out(e):
            Fall = True
            Reload_RF = False
            Character.bullet_RF = 4
            Character.hit_delay = 0.1
            if d_pressed or a_pressed:
                character.state_machine.add_event(('WALK', 0))

    @staticmethod
    def do(character):
        global Jump, jump_velocity, Fall, fall_velocity, Reload_RF, rrf

        if get_time() - character.wait_time > 0.4:
            character.state_machine.add_event(('TIME_OUT', 0))

        elif get_time() - character.wait_time > 0.35:
            character.name = 'Walk_RF'

        elif get_time() - character.wait_time > 0.25:
            character.frame = 0

        elif get_time() - character.wait_time > 0.15:
            if not rrf:
                Jump = True
                jump_velocity = 6.0
                Fall = False
                fall_velocity = 0.0
                rrf = True
                character.frame = 1

    @staticmethod
    def draw(character):
        if character.face_dir == 1:
            character.images[character.name].clip_composite_draw(character.frame * 340, 0, 340, 340, 0, '',
                                                                 character.sx, character.y, 170, 170)
        elif character.face_dir == -1:
            character.images[character.name].clip_composite_draw(character.frame * 340, 0, 340, 340, 0, 'h',
                                                                 character.sx, character.y, 170, 170)

animation_names = ['Idle_SG', 'Walk_SG', 'Hit_SG', 'Die_SG', 'Attack_SG', 'Reload_SG', 'Rc_SG',
                   'Idle_RF', 'Walk_RF', 'Hit_RF', 'Die_RF', 'Attack_RF',
                   'Idle_HG', 'Walk_HG', 'Hit_HG', 'Die_HG', 'Attack_HG', 'Reload_HG',]

class Character:
    images = None
    stance = 0
    state = 0
    speed = 3
    hp = 20
    max_hp = 20
    score = 0
    damage = 0
    bullet_SG = 8
    bullet_RF = 4
    max_bullet_HG = 20
    bullet_HG = max_bullet_HG
    shield_def = 1 # 방어 태세 방어도
    hit_delay = 0 # 피격 면역
    attack_delay = 0 # 공격 속도
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
                elif name == 'Attack_SG':
                    Character.images[name] = load_image("./HKCAWS/" + name + ".png")
                elif name == 'Reload_SG':
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
                elif name == 'Attack_RF':
                    Character.images[name] = load_image("./R93/" + name + ".png")

                elif name == 'Idle_HG':
                    Character.images[name] = load_image("./GSH18Mod/" + name + ".png")
                elif name == 'Walk_HG':
                    Character.images[name] = load_image("./GSH18Mod/" + name + ".png")
                elif name == 'Hit_HG':
                    Character.images[name] = load_image("./GSH18Mod/" + name + ".png")
                elif name == 'Die_HG':
                    Character.images[name] = load_image("./GSH18Mod/" + name + ".png")
                elif name == 'Attack_HG':
                    Character.images[name] = load_image("./GSH18Mod/" + name + ".png")
                elif name == 'Reload_HG':
                    Character.images[name] = load_image("./GSH18Mod/" + name + ".png")

    def __init__(self):
        self.x, self.y = 34.0, 140.0
        self.face_dir = 1
        self.attack_dir = 1
        self.frame = 0
        self.sx = 0
        self.load_images()
        self.name = ''
        self.hit_cool = 0
        self.attack_cool = 0
        self.attack_time = 0
        self.reload_time = 0
        self.Lshift_cool = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {
                    right_down: Walk, left_down: Walk, left_up: Idle, right_up: Idle, change_stance_z: Idle, change_stance_x: Idle,
                    walk: Walk, jump: Idle, rc_down: Idle, rc_up: Idle, dash: Idle, use_dash: Dash, lc_down: Idle, lc_up: Idle,
                    reload: Idle, rf_reload: RRF, idle: Idle, under_down: Idle, under_up: Idle, rf_reload_s: RsRF,
                    on_up: Idle, on_down: Idle,
                    temp_damage: Idle, take_hit: Hit, die: Die,
                    temp_more: Idle, temp_heal: Idle, temp_bullet: Idle, temp_reset_cool: Idle, temp_rectmode: Idle,
                },
                Walk: {
                    right_down: Walk, left_down: Walk, right_up: Walk, left_up: Walk, change_stance_z: Walk, change_stance_x: Walk,
                    idle: Idle, jump: Walk, rc_down: Walk, rc_up: Walk, dash: Walk, use_dash: Dash, lc_down: Walk, lc_up: Walk,
                    reload: Walk, rf_reload: RRF, walk: Walk, under_down: Walk, under_up: Walk, rf_reload_s: RsRF,
                    on_up: Walk, on_down: Walk,
                    temp_damage: Walk, take_hit: Hit, die: Die,
                    temp_more: Walk, temp_heal: Walk, temp_bullet: Walk, temp_reset_cool: Walk, temp_rectmode: Walk,
                },
                Hit: {
                    right_down: Hit, left_down: Hit, on_down: Hit, under_down: Hit, under_up: Hit, rc_up: Hit, lc_down: Hit, lc_up: Hit,
                    time_out: Idle, walk: Walk, die: Die
                },
                Die: {
                    time_out: Idle
                },
                Dash: {
                    left_up: Dash, right_up: Dash, on_up: Dash, under_up: Dash, rc_up: Dash, lc_up: Dash,
                    time_out: Idle, walk: Walk
                },
                RRF: {
                    left_up: RRF, right_up: RRF, on_up: RRF, under_up: RRF, lc_up: RRF,
                    time_out: Idle, walk: Walk
                },
                RsRF: {
                    left_up: RsRF, right_up: RsRF, on_up: RsRF, under_up: RsRF, lc_up: RsRF,
                    time_out: Idle, walk: Walk
                },
            }
        )

    def update(self):
        global Jump, jump_velocity, Fall, fall_velocity, Attack, Move, screen_left, screen_right, Reload_SG, Reload_HG
        self.state_machine.update()
        self.x = clamp(17.0, self.x, server.background.w - 17.0)
        self.sx = self.x - server.background.window_left
        screen_left = server.background.window_left
        screen_right = server.background.window_left + 1080

        if Jump:
            if not Move:
                Move = True
            self.y += jump_velocity * RUN_SPEED_PPS * game_framework.frame_time
            jump_velocity -= gravity * RUN_SPEED_PPS * game_framework.frame_time
            if jump_velocity <= 0:
                Jump = False
                Fall = True
                jump_velocity = 10.0

        if Fall:
            self.y -= fall_velocity * RUN_SPEED_PPS * game_framework.frame_time
            fall_velocity += gravity * RUN_SPEED_PPS * game_framework.frame_time
            if self.y < -68:
                Move = False
                Fall = False
                fall_velocity = 0.0
                self.state_machine.add_event(('DIE', 0))

        if attacking and not Attack:
            if Character.attack_delay == 0:
                if Character.stance == 0 and Character.bullet_SG > 0:
                    if self.attack_time == 0:
                        self.attack_time = get_time()
                        self.frame = 0
                        Character.bullet_SG -= 1
                        Attack = True
                elif Character.stance == 1 and not Move and Character.bullet_RF > 0:
                    if self.attack_time == 0:
                        self.attack_time = get_time()
                        self.frame = 0
                        Character.bullet_RF -= 1
                        Attack = True
                elif Character.stance == 2 and Character.bullet_HG > 0:
                    if self.attack_time == 0:
                        self.attack_time = get_time()
                        self.frame = 0
                        Character.bullet_HG -= 1
                        Attack = True
        if Attack:
            if Character.stance == 0:
                if get_time() - self.attack_time > 0.5:
                    Character.attack_delay = 0.5
                    self.attack_time = 0
                    self.frame = 0
                    Attack = False
            elif Character.stance == 1:
                if get_time() - self.attack_time > 0.4:
                    Character.attack_delay = 1
                    self.attack_time = 0
                    self.frame = 0
                    Attack = False
            elif Character.stance == 2:
                if get_time() - self.attack_time > 0.3:
                    Character.attack_delay = 0.2
                    self.attack_time = 0
                    self.frame = 0
                    Attack = False

        if Reload_SG:
            if get_time() - self.reload_time > 1.5:
                self.reload_time = 0
                if Character.state == 0:
                    Character.speed = 3
                elif Character.state == 1:
                    Character.speed = 1
                Character.bullet_SG = 8
                Reload_SG = False
                if d_pressed or a_pressed:
                    self.state_machine.add_event(('WALK', 0))
                else:
                    self.state_machine.add_event(('IDLE', 0))

        if Reload_HG:
            if get_time() - self.reload_time > 0.5:
                self.reload_time = 0
                Character.speed = 5
                Character.bullet_HG = Character.max_bullet_HG
                Reload_HG = False
                if d_pressed or a_pressed:
                    self.state_machine.add_event(('WALK', 0))
                else:
                    self.state_machine.add_event(('IDLE', 0))

        if not Character.hit_delay == 0:
            if self.hit_cool == 0:
                self.hit_cool = get_time()
            if get_time() - self.hit_cool > Character.hit_delay:
                Character.hit_delay = 0
                self.hit_cool = 0

        if not Character.attack_delay == 0:
            if self.attack_cool == 0:
                self.attack_cool = get_time()
            if get_time() - self.attack_cool > Character.attack_delay:
                Character.attack_delay = 0
                self.attack_cool = 0

        if not Character.dash_cooldown == 0:
            if self.Lshift_cool == 0:
                self.Lshift_cool = get_time()
            if get_time() - self.Lshift_cool > Character.dash_cooldown:
                Character.dash_cooldown = 0
                self.Lshift_cool = 0

    def handle_event(self, event):
        global mouse_x, mouse_y
        self.state_machine.add_event(('INPUT', event))
        if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT or (event.type == SDL_MOUSEMOTION and attacking):
            mouse_x, mouse_y = event.x, event.y

    def draw(self):
        self.state_machine.draw()
        if RectMode:
            draw_rectangle(*self.get_rect())

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
        return self.x - 17.0, self.y - 49.0, self.x + 17.0, self.y + 19.0

    def get_rect(self):
        return self.sx - 17.0, self.y - 49.0, self.sx + 17.0, self.y + 19.0

    def handle_collision(self, group, other):
        global Fall, fall_velocity, Climb
        if group == 'server.character:ladder':
            if not Climb:
                Climb = True
            if Fall:
                Fall = False
                fall_velocity = 0.0

    def handle_collision_fall(self, group, other):
        global Fall, fall_velocity
        if group == 'server.character:ground' and Fall:
            self.y = ground.Ground.collide_fall(other)
            Fall = False
            fall_velocity = 0.0

    def handle_collision_jump(self, group, other):
        global Jump, jump_velocity, Fall
        if group == 'server.character:ground' and Jump:
            self.y = ground.Ground.collide_jump(other)
            Jump = False
            Fall = True
            jump_velocity = 10.0

    def take_damage(self, damage):
        if Character.hit_delay == 0:
            Character.damage = damage
            self.state_machine.add_event(('HIT', 0))

    def take_heal(self, heal):
        Character.hp = min(Character.hp + heal, Character.max_hp)