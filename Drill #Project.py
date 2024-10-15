from random import randint

from pico2d import *
import random

WIDTH, HEIGHT = 1080, 800
x, y = 40, 110

position = 0
state = 0
shield_enhance = 1

MoveRight = True
Walking = False
Attack = False
AttackRight = True
Hit = False
Reload = False
Jump = False
Fall = False

changing = False
change_time = 0

attack_time = 0
attack_delay = 0

hit_delay = 0

reload_time = 0

jump_velocity = 0.0
fall_velocity = 0.0
gravity = 0.5

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
    image = None

    def __init__(self, i = 0):
        self.x = i * 30 + 15
        if Grass.image == None:
            Grass.image = load_image('grass.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, 45, 30, 30)

class Ground:
    image = None

    def __init__(self, i = 0):
        self.x = i * 30 + 15
        if Ground.image == None:
            Ground.image = load_image('ground.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, 15, 30, 30)

class Draw_Character:
    image_Hp = None
    image_Bullet_shotgun = None
    image_Bullet_rifle = None
    image_Bullet_handgun = None

    def __init__(self):
        self.framex = 0
        self.temp = 0
        self.image = load_image('HKCAWS_wait.png')                   # 기본 캐릭터 그림
        self.Hp = 20                                                 # 현재 체력
        self.max_Hp = 20                                             # 최대 체력
        if Draw_Character.image_Hp == None:
            self.Hp_image = load_image('Hp.png')                     # 체력 그림
        self.Bullet_shotgun = 7                                      # 샷건 총알 개수
        if Draw_Character.image_Bullet_shotgun == None:
            self.Bullet_shotgun_image = load_image('5.56mm.png')     # 샷건 총알 그림
        self.Bullet_rifle = 12                                       # 라이플 총알 개수
        if Draw_Character.image_Bullet_rifle == None:
            self.Bullet_rifle_image = load_image('7.62mm.png')       # 라이플 총알 그림
        self.Bullet_handgun = 20                                     # 핸드건 총알 개수
        if Draw_Character.image_Bullet_handgun == None:
            self.Bullet_handgun_image = load_image('9mm.png')        # 핸드건 총알 그림

    def update(self):
        global changing, change_time, Attack, attack_time, attack_delay, Hit, hit_delay, Reload, reload_time

        self.temp += 1
        if Reload:
            if reload_time == 80:
                self.framex = 0
            if self.temp % 5 == 0:
                if position == 0:
                    self.framex = (self.framex + 1) % 16
                    self.image = load_image('HKCAWS_reload.png')
        elif Hit:
            if position == 0 and state == 1:
                if self.temp % 3 == 0:
                    self.framex = (self.framex + 1) % 14
                    self.image = load_image('HKCAWS_shield.png')         # 샷건 방패 들기 피격
            else:
                self.framex = 0
                if position == 0:
                    self.image = load_image('HKCAWS_damage.png')         # 샷건 피격
                elif position == 1:
                    self.image = load_image('R93_damage.png')            # 라이플 피격
                elif position == 2: \
                    self.image = load_image('GSH18Mod_damage.png')       # 핸드건 피격
        elif Attack:
            if attack_time == 15:
                self.framex = 0
            if self.temp % 4 == 0:
                if position == 0:
                    self.framex = (self.framex + 1) % 15
                    self.image = load_image('HKCAWS_attack.png')         # 샷건 공격
                elif position == 1:
                    self.framex = (self.framex + 1) % 7
                    self.image = load_image('R93_attack.png')            # 라이플 공격
                elif position == 2:
                    self.framex = (self.framex + 1) % 5
                    self.image = load_image('GSH18Mod_attack.png')       # 핸드건 공격
        elif not Walking:
            if Jump or Fall:
                self.framex = 0
                if position == 0:
                    self.image = load_image('HKCAWS_move.png')           # 샷건 점프, 추락
                elif position == 1:
                    self.image = load_image('R93_move.png')              # 라이플 점프, 추락
                elif position == 2:
                    self.image = load_image('GSH18Mod_move.png')         # 핸드건 점프, 추락
            else:
                if self.temp % 3 == 0:
                    if position == 0:
                        if state == 0:
                            self.framex = (self.framex + 1) % 14
                            self.image = load_image('HKCAWS_wait.png')   # 샷건 대기
                        elif state == 1:
                            self.framex = (self.framex + 1) % 14
                            self.image = load_image('HKCAWS_shield.png') # 샷건 방패 들기 대기
                    elif position == 1:
                        self.framex = (self.framex + 1) % 14
                        self.image = load_image('R93_wait.png')          # 라이플 대기
                    elif position == 2:
                        self.framex = (self.framex + 1) % 11
                        self.image = load_image('GSH18Mod_wait.png')     # 핸드건 대기
        elif Walking:
            if Jump or Fall:
                self.framex = 0
                if position == 0:
                    self.image = load_image('HKCAWS_move.png')           # 샷건 점프, 추락 이동
                elif position == 1:
                    self.image = load_image('R93_move.png')              # 라이플 점프, 추락 이동
                elif position == 2:
                    self.image = load_image('GSH18Mod_move.png')         # 핸드건 점프, 추락 이동
            else:
                if position == 0 and state == 1:
                    if self.temp % 3 == 0:
                        self.framex = (self.framex + 1) % 14
                        self.image = load_image('HKCAWS_shield.png')     # 샷건 방패 들기 이동
                else:
                    if self.temp % 4 == 0:
                        self.framex = (self.framex + 1) % 6
                        if position == 0 and state == 0:
                            self.image = load_image('HKCAWS_move.png')   # 샷건 이동
                        elif position == 1:
                            self.image = load_image('R93_move.png')      # 라이플 이동
                        elif position == 2:
                            self.image = load_image('GSH18Mod_move.png') # 핸드건 이동
        if changing:                     # 폼 체인지 중에는 그림이 그려 지지 않아서 깜빡임 구현
            change_time -= 1
            if change_time <= 0:
                changing = False
        if Attack:
            attack_time -= 1
            if attack_time <= 0:
                Attack = False
                if position == 0:
                    attack_delay = 30    # 샷건 공격 속도 0.5초 (60 FPS)
                elif position == 1:
                    attack_delay = 60    # 라이플 공격 속도 1초 (60 FPS)
                elif position == 2:
                    attack_delay = 12    # 권총 공격 속도 0.2초 (60 FPS)
        if not attack_delay == 0:        # 공격 속도 attack_delay == 0 이 되기 전까지 공격 불가
            if attack_delay > 1:
                attack_delay -= 1
            elif attack_delay == 1:
                attack_delay = 0
        if Hit:
            if not hit_delay == 0:       # 피격 면역 hit_delay == 0 이 되기 전까지 무적
                if hit_delay > 1:
                    hit_delay -= 1
                elif hit_delay == 1:
                    Hit = False
                    hit_delay = 0
        if Reload:
            reload_time -= 1
            if reload_time <= 0:
                Reload = False
                if position == 0:
                    self.Bullet_shotgun = 7
                elif position == 1:
                    self.Bullet_rifle = 12
                elif position == 2:
                    self.Bullet_handgun = 20

    def draw(self):
        if not changing:
            if Reload:
                if MoveRight:            # 오른쪽 장전 그림
                    self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, '', x, y, 170, 170)
                elif not MoveRight:      # 왼쪽 장전 그림
                    self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, 'h', x, y, 170, 170)
            elif Hit:
                if MoveRight:            # 오른쪽 피격 그림
                    self.image.clip_composite_draw(0, 0, 340, 340, 0, '', x, y, 170, 170)
                elif not MoveRight:      # 왼쪽 피격 그림
                    self.image.clip_composite_draw(0, 0, 340, 340, 0, 'h', x, y, 170, 170)
            elif Attack:
                if AttackRight:          # 오른쪽 공격 그림
                    self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, '', x, y, 170, 170)
                elif not AttackRight:    # 왼쪽 공격 그림
                    self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, 'h', x, y, 170, 170)
            elif Walking:
                if MoveRight:            # 오른쪽 이동 그림 (점프, 추락 포함)
                    self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, '', x, y, 170, 170)
                elif not MoveRight:      # 왼쪽 이동 그림 (점프, 추락 포함)
                    self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, 'h', x, y, 170, 170)
            else:
                if MoveRight:            # 오른쪽 대기 그림 (점프, 추락 포함)
                    self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, '', x, y, 170, 170)
                elif not MoveRight:      # 왼쪽 대기 그림 (점프, 추락 포함)
                    self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, 'h', x, y, 170, 170)

    def take_damage(self, damage):
        global Hit, hit_delay
        if not Hit and hit_delay == 0:
            if position == 0 and (state == 1 or Reload):
                self.Hp -= max(damage - shield_enhance, 0) # 데미지 가 감소량 보다 작을 경우 0의 피해를 받음
            else:
                self.Hp -= damage
            Hit = True
            hit_delay = 30               # 0.5초 무적 (60 FPS)
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
        heart_count = int(self.max_Hp / 2)         # 하트 개수 = 최대 체력 / 2
        hx = 20
        hy = 780

        for i in range(heart_count):
            if self.Hp >= (i + 1) * 2:             # 하트 1개당 체력2일 경우 한칸 그림
                self.Hp_image.clip_composite_draw(0, 0, 120, 360, 0, '', hx + i * 30, hy, 30, 90)
            elif self.Hp == (i * 2) + 1:           # 하트 1개당 체력1일 경우 반칸 그림
                self.Hp_image.clip_composite_draw(120, 0, 120, 360, 0, '', hx + i * 30, hy, 30, 90)
            else:                                  # 하트 1개당 체력0일 경우 빈칸 그림
                self.Hp_image.clip_composite_draw(240, 0, 120, 360, 0, '', hx + i * 30, hy, 30, 90)

    def show_Bullet(self):
        global changing
        bx = 1060
        by = 770

        if not changing:
            if position == 0:
                for i in range(7):                 # 샷건 최대 총알
                    if i < self.Bullet_shotgun:    # 샷건 현재 총알 수 만큼 그리고 없으면 빈칸
                        self.Bullet_shotgun_image.clip_composite_draw(0, 0, 27, 49, 0, '', bx - i * 27, by, 27, 49)
                    else:
                        self.Bullet_shotgun_image.clip_composite_draw(27, 0, 27, 49, 0, '', bx - i * 27, by, 27, 49)
            elif position == 1:
                for i in range(12):                # 라이플 최대 총알
                    if i < self.Bullet_rifle:      # 라이플 현재 총알 수 만큼 그리고 없으면 빈칸
                        self.Bullet_rifle_image.clip_composite_draw(0, 0, 27, 59, 0, '', bx - i * 27, by - 10, 27, 59)
                    else:
                        self.Bullet_rifle_image.clip_composite_draw(27, 0, 27, 59, 0, '', bx - i * 27, by - 10, 27, 59)
            elif position == 2:
                for i in range(20):                # 핸드건 최대 총알
                    if i < self.Bullet_handgun:    # 핸드건 최대 총알 수 만큼 그리고 없으면 빈칸
                        self.Bullet_handgun_image.clip_composite_draw(0, 0, 28, 28, 0, '', bx - i * 28, by + 11, 28, 28)
                    else:
                        self.Bullet_handgun_image.clip_composite_draw(28, 0, 28, 28, 0, '', bx - i * 28, by + 11, 28, 28)

def handle_events():
    global running, MoveRight, Walking, Attack, AttackRight, position, state, Reload, reload_time, Jump, jump_velocity
    global changing, change_time, attack_time, a_pressed, d_pressed
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False

        # Esc 누를시 게임 종료
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

        # d 누를시 오른쪽 으로 이동, a를 누르는 중에 눌러도 오른쪽 으로 이동
        elif event.type == SDL_KEYDOWN and event.key == SDLK_d:
            MoveRight = True
            Walking = True
            d_pressed = True

        # d 손 땔시 오른쪽 이동 멈춤
        elif event.type == SDL_KEYUP and event.key == SDLK_d:
            d_pressed = False
            if a_pressed:     # a키를 누르 면서 d를 땔시 다시 왼쪽 으로 이동
                MoveRight = False
            if not a_pressed: # 아닌 경우 멈춤
                Walking = False

        # a 누를시 왼쪽 으로 이동, d를 누르는 중에 눌러도 왼쪽 으로 이동
        elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
            MoveRight = False
            Walking = True
            a_pressed = True

        # a 손 땔시 왼쪽 이동 멈춤
        elif event.type == SDL_KEYUP and event.key == SDLK_a:
            a_pressed = False
            if d_pressed:     # d키를 누르 면서 a를 땔시 다시 오른쪽 으로 이동
                MoveRight = True
            if not d_pressed: # 아닌 경우 멈춤
                Walking = False

        # space 누를시 점프
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE and not Jump:
            Jump = True
            jump_velocity = 10.0

        # r 누를시 재장전
        elif event.type == SDL_KEYDOWN and event.key == SDLK_r and not Attack and not Reload:
            if position == 0 and character.Bullet_shotgun == 0:
                Reload = True
                reload_time = 80

        # 샷건 -> 라이플 -> 핸드건 -> 샷건 폼 체인지, 스킬 사용, 공격, 재장전, 점프 중에는 불가능
        elif event.type == SDL_KEYDOWN and event.key == SDLK_z and state == 0 and not Attack and not Reload:
            if position == 2:
                position = 0
            else:
                position += 1
            changing = True
            change_time = 3

        # 샷건 -> 핸드건 -> 라이플 -> 샷건 폼 체인지, 스킬 사용, 공격, 재장전, 점프 중에는 불가능
        elif event.type == SDL_KEYDOWN and event.key == SDLK_x and state == 0 and not Attack and not Reload:
            if position == 0:
                position = 2
            else:
                position -= 1
            changing = True
            change_time = 3

        # 마우스 좌클릭 공격 (라이플 은 이동, 점프, 추락 중에 공격 불가), attack_delay == 공격 속도
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT and not Attack and attack_delay == 0:
            mouse_x, mouse_y = event.x, event.y
            if position == 0 and state == 1: # 샷건이 방패를 들고 있을 경우
                if mouse_x < x:              # 캐릭터 보다 왼쪽 좌클릭 시 공격은 못 하지만 왼쪽 을 바라 봄
                    MoveRight = False
                elif mouse_x > x:            # 캐릭터 보다 오른쪽 좌클릭 시 공격은 못 하지만 오른쪽 을 바라 봄
                    MoveRight = True

            elif (                           # 나머지 경우
                    (position == 0 and state == 0 and character.Bullet_shotgun > 0) or
                    (position == 1 and not Walking and not Jump and not Fall and character.Bullet_rifle > 0) or
                    (position == 2 and state == 0 and character.Bullet_handgun > 0)
            ):
                if position == 0:    # 샷건 총알 감소
                    character.Bullet_shotgun -= 1
                elif position == 1:  # 라이플 총알 감소
                    character.Bullet_rifle -= 1
                elif position == 2:  # 핸드건 총알 감소
                    character.Bullet_handgun -= 1

                Attack = True
                attack_time = 15     # 공격 모션 시간

                if mouse_x < x:      # 캐릭터 보다 왼쪽 좌클릭 시 왼쪽 공격, 오른쪽 이동 중 에는 왼쪽 공격후 오른쪽 을 다시 바라 봄
                    AttackRight = False
                    if not Walking:  # 이동 중 공격이 아니면 공격 후 왼쪽 을 바라 봄
                        MoveRight = False
                elif mouse_x > x:    # 캐릭터 보다 오른쪽 좌클릭 시 오른쪽 공격, 왼쪽 이동 중 에는 오른쪽 공격후 왼쪽 을 다시 바라 봄
                    AttackRight = True
                    if not Walking:  # 이동 중 공격이 아니면 공격 후 오른쪽 을 바라 봄
                        MoveRight = True

        # 샷건 일때 우클릭 중 일시 방패를 듬
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_RIGHT and not Attack and position == 0 and state == 0:
            state = 1

        # 샷건 일때 우클릭 땔시 방패를 내림
        elif event.type == SDL_MOUSEBUTTONUP and event.button == SDL_BUTTON_RIGHT and position == 0 and state == 1:
            state = 0

        # t 누를시 hp - 4
        elif event.type == SDL_KEYDOWN and event.key == SDLK_t:
            character.take_damage(4)

        # y 누를시 hp + 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_y:
            character.heal(1)

        # u 누를시 max hp + 4
        elif event.type == SDL_KEYDOWN and event.key == SDLK_u:
            character.plus_max_Hp(4)

        # i 누를시 모든 탄창 비우기
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            character.Bullet_shotgun = 0
            character.Bullet_rifle = 0
            character.Bullet_handgun = 0

def update_world():
    global x, y, Jump, jump_velocity, Fall, fall_velocity
    dx = 0
    if MoveRight and Walking:                               # 오른쪽 으로 이동
        if position == 0 and state == 0 and not Reload:     # 샷건 이동 속도, 방패를 들지 않을 경우
            dx = 3
        elif position == 0 and (state == 1 or Reload):      # 샷건 이동 속도, 방패를 들거나 장전 중일 경우
            dx = 1
        elif position == 1 and state == 0:                  # 라이플 이동 속도, 저격 스킬을 사용 중이 아닐 경우
            dx = 4
        elif position == 2:                                 # 핸드건 이동 속도
            dx = 5
        x += dx
    elif not MoveRight and Walking:                         # 왼쪽 으로 이동
        if position == 0 and state == 0 and not Reload:     # 샷건 이동 속도, 방패를 들지 않을 경우
            dx = -3
        elif position == 0 and (state == 1 or Reload):      # 샷건 이동 속도, 방패를 들거나 장전 중일 경우
            dx = -1
        elif position == 1 and state == 0:                  # 라이플 이동 속도, 저격 스킬을 사용 중이 아닐 경우
            dx = -4
        elif position == 2:                                 # 핸드건 이동 속도
            dx = -5
        x += dx

    if x < 34:                                               # 화면 왼쪽 경계 이동 불가
        x = 34
    elif x > WIDTH - 34:                                     # 화면 오른쪽 경계 이동 불가
        x = WIDTH - 34

    if not jump_velocity == 0.0:
        if jump_velocity > 0.5:
            y += jump_velocity
            jump_velocity -= gravity
        elif jump_velocity == 0.5:
            y += jump_velocity
            Jump = False
            Fall = True
            jump_velocity = 0.0
            fall_velocity = 0.5

    if not fall_velocity == 0.0:
        if fall_velocity < 10.0:
            y -= fall_velocity
            fall_velocity += gravity
        elif fall_velocity == 10.0:
            y -= fall_velocity
            Fall = False
            fall_velocity = 0.0

    background.update(dx)

    for o in world:
        o.update()

def render_world():
    clear_canvas()
    background.draw()
    for o in world:
        o.draw()
    character.show_Hp()
    character.show_Bullet()
    update_canvas()

def reset_world():
    global running, grass, ground, character, world, background

    running = True
    world = []

    background = Background()

    ground = [Ground(i) for i in range(0, 35 + 1) if not 30 <= i <= 33]
    world += ground

    grass = [Grass(i) for i in range(0, 35 + 1) if not 30 <= i <= 33]
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