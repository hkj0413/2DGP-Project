from random import randint

from pico2d import *
import random

WIDTH, HEIGHT = 1080, 800
x, y = 40, 110
position = 0
state = 0
MoveRight = True
Walking = False
Attack = False
AttackRight = True

changing = False
change_time = 0

attack_time = 0
attack_delay = 0

d_pressed = False
a_pressed = False

BG_WIDTH, BG_HEIGHT = 2060, 1200
bg_x = 0
bg_y = 0

class Background:
    def __init__(self):
        self.image = load_image('1stage.png')

    def update(self, dx):
        global bg_x
        bg_x += dx

        if bg_x < 0:
            bg_x = 0
        if bg_x > BG_WIDTH - WIDTH:
            bg_x = BG_WIDTH - WIDTH

    def draw(self):
        self.image.clip_draw(bg_x, bg_y, WIDTH, HEIGHT, WIDTH // 2, HEIGHT // 2)

class Grass:
    def __init__(self, i = 0):
        self.x = i * 30 + 15
        self.image = load_image('grass.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, 45, 30, 30)

class Ground:
    def __init__(self, i = 0):
        self.x = i * 30 + 15
        self.image = load_image('ground.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, 15, 30, 30)

class Draw_Character:
    def __init__(self):
        self.framex = 0
        self.temp = 0
        self.image = load_image('HKCAWS_wait.png')
        self.Hp = 20
        self.max_Hp = 20
        self.Hp_image = load_image('Hp.png')

    def update(self):
        global changing, change_time, Attack, attack_time, attack_delay
        self.temp += 1
        if Attack:
            if attack_time == 15:
                self.framex = 0
            if self.temp % 4 == 0:
                if position == 0:
                    self.framex = (self.framex + 1) % 15
                    self.image = load_image('HKCAWS_attack.png')
                elif position == 1:
                    self.framex = (self.framex + 1) % 7
                    self.image = load_image('R93_attack.png')
                elif position == 2:
                    self.framex = (self.framex + 1) % 5
                    self.image = load_image('GSH18Mod_attack.png')
        elif not Walking:
            if self.temp % 3 == 0:
                if position == 0:
                    self.framex = (self.framex + 1) % 14
                    self.image = load_image('HKCAWS_wait.png')
                elif position == 1:
                    self.framex = (self.framex + 1) % 14
                    self.image = load_image('R93_wait.png')
                elif position == 2:
                    self.framex = (self.framex + 1) % 11
                    self.image = load_image('GSH18Mod_wait.png')
        elif Walking:
            if self.temp % 4 == 0:
                self.framex = (self.framex + 1) % 6
                if position == 0:
                    self.image = load_image('HKCAWS_move.png')
                elif position == 1:
                    self.image = load_image('R93_move.png')
                elif position == 2:
                    self.image = load_image('GSH18Mod_move.png')
        if changing:
            change_time -= 1
            if change_time <= 0:
                changing = False
        if Attack:
            attack_time -= 1
            if attack_time <= 0:
                Attack = False
                if position == 0:
                    attack_delay = 16
                elif position == 1:
                    attack_delay = 15
                elif position == 2:
                    attack_delay = 6
        if not attack_delay == 0:
            if attack_delay > 1:
                attack_delay -= 1
            elif attack_delay == 1:
                attack_delay = 0

    def draw(self):
        if changing:
            pass
        else:
            if MoveRight and not Walking and not Attack:
                self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, '', x, y, 170, 170)
            elif not MoveRight and not Walking and not Attack:
                self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, 'h', x, y, 170, 170)
            elif MoveRight and Walking and not Attack:
                self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, '', x, y, 170, 170)
            elif not MoveRight and Walking and not Attack:
                self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, 'h', x, y, 170, 170)
            elif AttackRight and Attack:
                self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, '', x, y, 170, 170)
            elif not AttackRight and Attack:
                self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, 'h', x, y, 170, 170)

    def take_damage(self, damage):
        self.Hp -= damage
        if self.Hp <= 0:
            self.Hp = 0
        self.show_Hp()

    def heal(self, healpack):
        self.Hp += healpack
        if self.Hp > self.max_Hp:
            self.Hp = self.max_Hp
        self.show_Hp()

    def plus_max_Hp(self, plusHp):
        self.max_Hp += plusHp
        self.Hp += plusHp
        self.show_Hp()

    def show_Hp(self):
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


def handle_events():
    global running, MoveRight, Walking, Attack, AttackRight, position, changing, change_time, attack_time, a_pressed, d_pressed, mouse_x, mouse_y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_d:
            MoveRight = True
            Walking = True
            d_pressed = True
        elif event.type == SDL_KEYUP and event.key == SDLK_d:
            d_pressed = False
            if not a_pressed:
                Walking = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
            MoveRight = False
            Walking = True
            a_pressed = True
        elif event.type == SDL_KEYUP and event.key == SDLK_a:
            a_pressed = False
            if not d_pressed:
                Walking = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_z:
            if position == 2:
                position = 0
            else:
                position += 1
            changing = True
            change_time = 2
        elif event.type == SDL_KEYDOWN and event.key == SDLK_x:
            if position == 0:
                position = 2
            else:
                position -= 1
            changing = True
            change_time = 2
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT and not Attack and attack_delay == 0:
            mouse_x, mouse_y = event.x, event.y
            if not (position == 1 and Walking):
                if not Attack and attack_delay == 0:
                    Attack = True
                    attack_time = 15

                if mouse_x < x:
                    AttackRight = False
                    if not Walking:
                        MoveRight = False
                elif mouse_x > x:
                    AttackRight = True
                    if not Walking:
                        MoveRight = True
        elif event.type == SDL_KEYDOWN and event.key == SDLK_t:
            character.take_damage(4)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_y:
            character.heal(1)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_u:
            character.plus_max_Hp(4)

def update_world():
    global x, y
    dx = 0
    if MoveRight and Walking:
        if position == 0 and state == 0:
            dx = 3
        elif position == 1 and state == 0:
            dx = 4
        elif position == 2:
            dx = 5
        x += dx
    elif not MoveRight and Walking:
        if position == 0 and state == 0:
            dx = -3
        elif position == 1 and state == 0:
            dx = -4
        elif position == 2:
            dx = -5
        x += dx

    background.update(dx)

    for o in world:
        o.update()

def render_world():
    clear_canvas()
    background.draw()
    for o in world:
        o.draw()
    character.show_Hp()
    update_canvas()

def reset_world():
    global running, grass, ground, character, world, background

    running = True
    world = []

    background = Background()

    ground = [Ground(i) for i in range(0, 35 + 1)]
    world += ground

    grass = [Grass(i) for i in range(0, 35 + 1)]
    world += grass

    character = Draw_Character()
    world.append(character)

open_canvas(WIDTH, HEIGHT)

reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)

close_canvas()