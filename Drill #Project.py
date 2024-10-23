from pico2d import *

WIDTH, HEIGHT = 1080, 800
x, y = 34, 140.0

position = 0
state = 0
shield_enhance = 1
handgun_max_bullet = 20
handgun_attack_speed = 12

MoveRight = True
Walking = False
Attack = False
AttackRight = True
Hit = False
Reload_shotgun = False
Reload_rifle = False
Reload_handgun = False
Jump = False
Fall = False
Die = False
Dash = False

changing = False
change_time = 0

attack_time = 0
attack_delay = 0

hit_delay = 0

reload_time = 0

die_time = 0      # 120 2초 (60 FPS)

dash_cooldown = 0 # 360 6초 (60 FPS)
move = 0

jump_velocity = 0.0
fall_velocity = 0.0
gravity = 0.5

d_pressed = False
a_pressed = False

BG_WIDTH, BG_HEIGHT = 3240, 1200
ox = 0
dx = 0
xpos = 0

class Background:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = load_image('1stage.png')

    def update(self, dx):
        global ox
        ox += dx

        if ox < 0:
            ox = 0
        if ox > BG_WIDTH - WIDTH:
            ox = BG_WIDTH - WIDTH

        self.x = ox

    def draw(self):
        self.image.clip_draw(self.x, self.y, WIDTH, HEIGHT, WIDTH // 2, HEIGHT // 2)

class Grass:
    image = None

    def __init__(self, i = 0, j = 0):
        self.base_x = i * 30 + 15
        self.y  = j * 30 + 15
        if Grass.image == None:
            Grass.image = load_image('grass.png')

    def update(self):
        self.x = self.base_x - ox

    def draw(self):
        self.image.draw(self.x, self.y, 30, 30)

class Ground:
    image = None

    def __init__(self, i = 0, j = 0):
        self.base_x = i * 30 + 15
        self.y  = j * 30 + 15
        if Ground.image == None:
            Ground.image = load_image('ground.png')

    def update(self):
        self.x = self.base_x - ox

    def draw(self):
        self.image.draw(self.x, self.y, 30, 30)

class Draw_Character:
    image_Hp = None
    image_Bullet = None

    def __init__(self):
        self.framex = 0
        self.temp = 0
        self.roll = 60
        self.Hp = 20                                                 # 현재 체력
        self.max_Hp = 20                                             # 최대 체력
        if Draw_Character.image_Hp == None:
            self.Hp_image = load_image('Hp.png')                     # 체력 그림
        self.Bullet_shotgun = 8                                      # 샷건 총알 개수
        self.Bullet_rifle = 4                                        # 라이플 총알 개수
        self.Bullet_handgun = handgun_max_bullet                     # 핸드건 총알 개수
        if Draw_Character.image_Bullet == None:                      # 총알 그림
            self.Bullet_image = load_image('Bullet.png')

        self.images = {                                              # 이미지 미리 로드 하기
            "wait_shotgun": load_image('HKCAWS_wait.png'),
            "wait_rifle": load_image('R93_wait.png'),
            "wait_handgun": load_image('GSH18Mod_wait.png'),
            "move_shotgun": load_image('HKCAWS_move.png'),
            "move_rifle": load_image('R93_move.png'),
            "move_handgun": load_image('GSH18Mod_move.png'),
            "attack_shotgun": load_image('HKCAWS_attack.png'),
            "attack_rifle": load_image('R93_attack.png'),
            "attack_handgun": load_image('GSH18Mod_attack.png'),
            "damage_shotgun": load_image('HKCAWS_damage.png'),
            "damage_rifle": load_image('R93_damage.png'),
            "damage_handgun": load_image('GSH18Mod_damage.png'),
            "reload_shotgun": load_image('HKCAWS_reload.png'),
            "reload_handgun": load_image('GSH18Mod_reload.png'),
            "shield_shotgun": load_image('HKCAWS_shield.png'),
            "die_shotgun": load_image('HKCAWS_die.png'),
            "die_rifle": load_image('R93_die.png'),
            "die_handgun": load_image('GSH18Mod_die.png'),
            "ultimate_1_shotgun": load_image('HKCAWS_ultimate_1.png'),
            "ultimate_2_shotgun": load_image('HKCAWS_ultimate_2.png'),
        }

        self.image = self.images["wait_shotgun"]                     # 기본 캐릭터 그림

    def update(self):
        global MoveRight, Walking, changing, change_time, Attack, attack_time, attack_delay, Hit, hit_delay, Reload_shotgun, Reload_rifle, Reload_handgun, reload_time
        global Die, die_time, x, y, dx, ox, xpos, Jump, jump_velocity, Fall, fall_velocity, a_pressed, d_pressed, state, Dash, dash_cooldown
        self.temp += 1
        if Die:
            if die_time == 180:
                self.temp = 0
                self.framex = 0
            if not position == 2:
                if die_time > 129:
                    if self.temp % 3 == 0:
                        if position == 0:
                            self.framex = (self.framex + 1) % 18
                            self.image = self.images["die_shotgun"]    # 샷건 사망
                        elif position == 1:
                            self.framex = (self.framex + 1) % 18
                            self.image = self.images["die_rifle"]      # 라이플 사망
                else:
                    self.framex = 18
            elif position == 2:
                if die_time > 80:
                    if self.temp % 5 == 0:
                        self.framex = (self.framex + 1) % 21
                        self.image = self.images["die_handgun"]        # 핸드건 사망
                else:
                    self.framex = 21

        elif Reload_shotgun:
            if reload_time == 80:
                self.temp = 0
                self.framex = 0
            if self.temp % 5 == 0:
                self.framex = (self.framex + 1) % 16
                self.image = self.images["reload_shotgun"]

        elif Reload_rifle:
            if reload_time > 30 or 20 >= reload_time > 10:
                self.framex = 0
                self.image = self.images["attack_rifle"]
            elif 30 >= reload_time > 20:
                self.framex = 1
            else:
                self.framex = 0
                self.image = self.images["move_rifle"]

        elif Reload_handgun:
            if reload_time == 30:
                self.temp = 0
                self.framex = 0
                self.roll = 60
            if self.temp % 4 == 0:
                self.framex = (self.framex + 1) % 10
                if self.roll >= 0:
                    self.roll -= 15
                self.image = self.images["reload_handgun"]

        elif Hit:
            if position == 0 and state == 1:
                if self.temp % 3 == 0:
                    self.framex = (self.framex + 1) % 14
                    self.image = self.images["shield_shotgun"]           # 샷건 방패 들기 피격
            else:
                self.framex = 0
                if position == 0:
                    self.image = self.images["damage_shotgun"]           # 샷건 피격
                elif position == 1:
                    self.image = self.images["damage_rifle"]             # 라이플 피격
                elif position == 2:
                    self.image = self.images["damage_handgun"]           # 핸드건 피격

        elif Attack:
            if attack_time == 15:
                self.temp = 0
                self.framex = 0
            if self.temp % 4 == 0:
                if position == 0:
                    self.framex = (self.framex + 1) % 15
                    self.image = self.images["attack_shotgun"]           # 샷건 공격
                elif position == 1:
                    self.framex = (self.framex + 1) % 7
                    self.image = self.images["attack_rifle"]             # 라이플 공격
                elif position == 2:
                    self.framex = (self.framex + 1) % 5
                    self.image = self.images["attack_handgun"]           # 핸드건 공격

        elif not Walking:
            if Jump or Fall or Dash:
                self.framex = 0
                if position == 0:
                    self.image = self.images["move_shotgun"]             # 샷건 점프, 추락, 대쉬
                elif position == 1:
                    self.image = self.images["move_rifle"]               # 라이플 점프, 추락, 대쉬
                elif position == 2:
                    self.image = self.images["move_handgun"]             # 핸드건 점프, 추락, 대쉬
            else:
                if self.temp % 3 == 0:
                    if position == 0:
                        if state == 0:
                            self.framex = (self.framex + 1) % 14
                            self.image = self.images["wait_shotgun"]     # 샷건 대기
                        elif state == 1:
                            self.framex = (self.framex + 1) % 14
                            self.image = self.images["shield_shotgun"]   # 샷건 방패 들기 대기
                    elif position == 1:
                        self.framex = (self.framex + 1) % 14
                        self.image = self.images["wait_rifle"]           # 라이플 대기
                    elif position == 2:
                        self.framex = (self.framex + 1) % 11
                        self.image = self.images["wait_handgun"]         # 핸드건 대기

        elif Walking:
            if Jump or Fall or Dash:
                self.framex = 0
                if position == 0:
                    self.image = self.images["move_shotgun"]             # 샷건 점프, 추락 이동, 대쉬
                elif position == 1:
                    self.image = self.images["move_rifle"]               # 라이플 점프, 추락 이동, 대쉬
                elif position == 2:
                    self.image = self.images["move_handgun"]             # 핸드건 점프, 추락 이동, 대쉬
            else:
                if position == 0 and state == 1:
                    if self.temp % 3 == 0:
                        self.framex = (self.framex + 1) % 14
                        self.image = self.images["shield_shotgun"]       # 샷건 방패 들기 이동
                else:
                    if self.temp % 4 == 0:
                        self.framex = (self.framex + 1) % 6
                        if position == 0 and state == 0:
                            self.image = self.images["move_shotgun"]     # 샷건 이동
                        elif position == 1:
                            self.image = self.images["move_rifle"]       # 라이플 이동
                        elif position == 2:
                            self.image = self.images["move_handgun"]     # 핸드건 이동

        if changing:                     # 폼 체인지 중에는 그림이 그려 지지 않아서 깜빡임 구현
            change_time -= 1
            if change_time <= 0:
                changing = False

        if Attack:
            attack_time -= 1
            if attack_time <= 0:
                Attack = False
                if position == 0:
                    attack_delay = 30                      # 샷건 공격 속도 0.5초 (60 FPS)
                elif position == 1:
                    attack_delay = 60                      # 라이플 공격 속도 1초 (60 FPS)
                elif position == 2:
                    attack_delay = handgun_attack_speed    # 권총 공격 속도 0.2초 (60 FPS)
        if not attack_delay == 0:                          # 공격 속도 attack_delay == 0 이 되기 전까지 공격 불가
            attack_delay -= 1
            if attack_delay <= 0:
                attack_delay = 0

        if not hit_delay == 0:                              # 피격 면역 hit_delay == 0 이 되기 전까지 무적
            hit_delay -= 1
            if hit_delay <= 0:
                Hit = False
                hit_delay = 0

        dx = 0

        if MoveRight and Walking:
            if x > 580 and not ox == BG_WIDTH - WIDTH:                                 # 오른쪽 으로 캐릭터 제외 모든 객체 이동
                if position == 0 and state == 0 and not Reload_shotgun and not Attack:
                    if check_collide(world):
                        dx = 0
                    else:
                        dx = 3
                        if check_collide_ad(world, 3) and not Jump and not Fall:
                            Fall = True
                elif position == 0 and (state == 1 or Reload_shotgun):
                    if check_collide(world):
                        dx = 0
                    else:
                        dx = 1
                        if check_collide_ad(world, 1) and not Jump and not Fall:
                            Fall = True
                elif position == 1 and state == 0 and not Reload_rifle:
                    if check_collide(world):
                        dx = 0
                    else:
                        dx = 4
                        if check_collide_ad(world, 4) and not Jump and not Fall:
                            Fall = True
                elif position == 2:
                    if check_collide(world):
                        dx = 0
                    else:
                        dx = 5
                        if check_collide_ad(world, 5) and not Jump and not Fall:
                            Fall = True
            else:                                                                      # 오른쪽 으로 캐릭터 이동
                if position == 0 and state == 0 and not Reload_shotgun and not Attack: # 샷건 이동 속도, 방패를 들지 않을 경우
                    x += 3
                    if check_collide(world):
                        x += -3
                    elif check_collide_ad(world, 3) and not Jump and not Fall:
                        Fall = True
                elif position == 0 and (state == 1 or Reload_shotgun):                 # 샷건 이동 속도, 방패를 들거나 장전 중일 경우
                    x += 1
                    if check_collide(world):
                        x += -1
                    elif check_collide_ad(world, 1) and not Jump and not Fall:
                        Fall = True
                elif position == 1 and state == 0 and not Reload_rifle:                # 라이플 이동 속도, 저격 스킬을 사용 중이 아닐 경우
                    x += 4
                    if check_collide(world):
                        x += -4
                    elif check_collide_ad(world, 4) and not Jump and not Fall:
                        Fall = True
                elif position == 2:                                                    # 핸드건 이동 속도
                    x += 5
                    if check_collide(world):
                        x += -5
                    elif check_collide_ad(world, 5) and not Jump and not Fall:
                        Fall = True

        elif not MoveRight and Walking:
            if x < 500 and not ox == 0:                                                # 왼쪽 으로 캐릭터 제외 모든 객체 이동
                if position == 0 and state == 0 and not Reload_shotgun and not Attack:
                    if check_collide(world):
                        dx = 0
                    else:
                        dx = -3
                        if check_collide_ad(world, 3) and not Jump and not Fall:
                            Fall = True
                elif position == 0 and (state == 1 or Reload_shotgun):
                    if check_collide(world):
                        dx = 0
                    else:
                        dx = -1
                        if check_collide_ad(world, 1) and not Jump and not Fall:
                            Fall = True
                elif position == 1 and state == 0 and not Reload_rifle:
                    if check_collide(world):
                        dx = 0
                    else:
                        dx = -4
                        if check_collide_ad(world, 4) and not Jump and not Fall:
                            Fall = True
                elif position == 2:
                    if check_collide(world):
                        dx = 0
                    else:
                        dx = -5
                        if check_collide_ad(world, 5) and not Jump and not Fall:
                            Fall = True
            else:                                                                      # 왼쪽 으로 캐릭터 이동
                if position == 0 and state == 0 and not Reload_shotgun and not Attack: # 샷건 이동 속도, 방패를 들지 않을 경우
                    x += -3
                    if check_collide(world):
                        x += 3
                    elif check_collide_ad(world, 3) and not Jump and not Fall:
                        Fall = True
                elif position == 0 and (state == 1 or Reload_shotgun):                 # 샷건 이동 속도, 방패를 들거나 장전 중일 경우
                    x += -1
                    if check_collide(world):
                        x += 1
                    elif check_collide_ad(world, 1) and not Jump and not Fall:
                        Fall = True
                elif position == 1 and state == 0 and not Reload_rifle:                # 라이플 이동 속도, 저격 스킬을 사용 중이 아닐 경우
                    x += -4
                    if check_collide(world):
                        x += 4
                    elif check_collide_ad(world, 4) and not Jump and not Fall:
                        Fall = True
                elif position == 2:                                                    # 핸드건 이동 속도
                    x += -5
                    if check_collide(world):
                        x += 5
                    elif check_collide_ad(world, 5) and not Jump and not Fall:
                        Fall = True

        if Dash:
            if dash_cooldown <= 350:
                Dash = False
                Fall = True
                if move == 0:
                    x += -20
                elif move == 1:
                    x += 20

            if x > 580 and not ox == BG_WIDTH - WIDTH and move == 0:
                if check_collide(world):
                    dx = 0
                    x += -20
                    Dash = False
                    Fall = True
                else:
                    dx = 20
            elif move == 0:
                x += 20
                if check_collide(world):
                    x += -20
                    Dash = False
                    Fall = True
            elif x < 500 and not ox == 0 and move == 1:
                if check_collide(world):
                    dx = 0
                    x += 20
                    Dash = False
                    Fall = True
                else:
                    dx = -20
            elif move == 1:
                x += -20
                if check_collide(world):
                    x += 20
                    Dash = False
                    Fall = True

        if not dash_cooldown == 0:
            dash_cooldown -= 1
            if dash_cooldown <= 0:
                dash_cooldown = 0

        if Reload_shotgun:
            reload_time -= 1
            if reload_time <= 0:
                Reload_shotgun = False
                self.Bullet_shotgun = 8

        if Reload_rifle:
            reload_time -= 1
            if reload_time == 30:
                jump_velocity = 6.0
                Fall = False
                fall_velocity = 0.0
                if not Jump:
                    Jump = True
            elif 30 >= reload_time >= 10:
                if x > 580 and not ox == BG_WIDTH - WIDTH and MoveRight:
                    if check_collide(world):
                        dx = 0
                        x += -8
                    else:
                        dx = 8
                elif MoveRight:
                    x += 8
                    if check_collide(world):
                        x += -8
                elif x < 500 and not ox == 0 and not MoveRight:
                    if check_collide(world):
                        dx = 0
                        x += 8
                    else:
                        dx = -8
                elif not MoveRight:
                    x += -8
                    if check_collide(world):
                        x += 8
            elif reload_time == 10:
                if MoveRight:
                    x += -8
                elif not MoveRight:
                    x += 8
            elif reload_time <= 0:
                Reload_rifle = False
                if a_pressed:
                    MoveRight = False
                elif d_pressed:
                    MoveRight = True
                else:
                    MoveRight = not MoveRight
                self.Bullet_rifle = 4

        if Reload_handgun:
            reload_time -= 1
            if reload_time <= 0:
                Reload_handgun = False
                self.Bullet_handgun = handgun_max_bullet

        xpos += dx

        if x < 34:                                                # 화면 왼쪽 경계 이동 불가
            x = 34
        if x > WIDTH - 34:                                        # 화면 오른쪽 경계 이동 불가
            x = WIDTH - 34

        if Jump:
            y += jump_velocity                                    # 점프 가속도
            jump_velocity -= gravity
            if jump_velocity <= 0.0:
                y += jump_velocity
                Jump = False
                Fall = True
                jump_velocity = 10.0
            elif check_collide_jump(Grass):
                y = bottom_o - 18
                Jump = False
                Fall = True
                jump_velocity = 10.0

        if Fall:
            y -= fall_velocity                                    # 추락 가속도
            fall_velocity += gravity
            if check_collide_fall(Grass):
                y = top_o + 50
                Fall = False
                fall_velocity = 0.0
            elif y < -68:
                Fall = False
                Die = True
                die_time = 180
                fall_velocity = 0.0

        if Die:
            if die_time == 180:                                   # 사망 시간
                Walking = False
                Attack = False
                Reload_shotgun = False
                Reload_shotgun = False
                Hit = False
                Jump = False
                Fall = False
                a_pressed = False
                d_pressed = False
                state = 0
                change_time = 0
                attack_time = 0
                attack_delay = 0
                hit_delay = 0
                reload_time = 0
                jump_velocity = 0.0
                fall_velocity = 0.0
            die_time -= 1
            if die_time <= 0:
                MoveRight = True
                Die = False
                x = 34
                y = 140.0
                ox -= xpos
                for o in world:
                    o.x -= xpos
                xpos = 0
                if self.Hp == 0:
                    self.Hp = self.max_Hp
                    self.Bullet_shotgun = 8
                    self.Bullet_rifle = 4
                    self.Bullet_handgun = handgun_max_bullet
                die_time = 180

    def draw(self):
        if not changing:
            if Die:
                if position == 0:        # 샷건
                    if MoveRight:        # 오른쪽 사망 그림
                        self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, '', x - 48, y, 170, 170)
                    elif not MoveRight:  # 왼쪽 사망 그림
                        self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, 'h', x + 48, y, 170, 170)
                elif position == 1:      # 라이플
                    if MoveRight:        # 오른쪽 사망 그림
                        self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, '', x - 11, y, 170, 170)
                    elif not MoveRight:  # 왼쪽 사망 그림
                        self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, 'h', x + 11, y, 170, 170)
                elif position == 2:      # 핸드건
                    if MoveRight:        # 오른쪽 사망 그림
                        self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, '', x, y, 170, 170)
                    elif not MoveRight:  # 왼쪽 사망 그림
                        self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, 'h', x, y, 170, 170)

            elif Attack:
                if AttackRight:          # 오른쪽 공격 그림
                    self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, '', x, y, 170, 170)
                elif not AttackRight:    # 왼쪽 공격 그림
                    self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, 'h', x, y, 170, 170)
            elif Reload_rifle:
                if MoveRight:            # 오른쪽 라이플 장전
                    self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, 'h', x, y, 170, 170)
                elif not MoveRight:      # 왼쪽 라이플 장전
                    self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, '', x, y, 170, 170)
            elif Reload_handgun:
                if MoveRight:            # 오른쪽 핸드건 장전
                    self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, '', x + self.roll, y, 170, 170)
                elif not MoveRight:      # 왼쪽 핸드건 장전
                    self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, 'h', x - self.roll, y, 170, 170)
            else:
                if MoveRight:            # 오른쪽 그 외 전부
                    self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, '', x, y, 170, 170)
                elif not MoveRight:      # 왼쪽 그 외 전부
                    self.image.clip_composite_draw(self.framex * 340, 0, 340, 340, 0, 'h', x, y, 170, 170)

    def take_damage(self, damage):
        global Walking, a_pressed, d_pressed, Hit, hit_delay, Jump, jump_velocity, Fall, Die, die_time
        if hit_delay == 0:
            if position == 0 and (state == 1 or Reload_shotgun):
                self.Hp -= max(damage - shield_enhance, 0) # 데미지 가 감소량 보다 작을 경우 0의 피해를 받음
            else:
                self.Hp -= damage
                Jump = False
                jump_velocity = 10.0
                Fall = True
                Walking = False
                a_pressed = False
                d_pressed = False
            Hit = True
            hit_delay = 30                                 # 0.5초 무적 (60 FPS)
            if self.Hp <= 0:
                self.Hp = 0
                Die =  True
                die_time = 180
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
        heart_count = int(self.max_Hp / 2)          # 하트 개수 = 최대 체력 / 2
        hx = 20
        hy = 780

        for i in range(heart_count):
            if self.Hp >= (i + 1) * 2:              # 하트 1개당 체력2일 경우 한칸 그림
                self.Hp_image.clip_composite_draw(0, 0, 120, 360, 0, '', hx + i * 30, hy, 30, 90)
            elif self.Hp == (i * 2) + 1:            # 하트 1개당 체력1일 경우 반칸 그림
                self.Hp_image.clip_composite_draw(120, 0, 120, 360, 0, '', hx + i * 30, hy, 30, 90)
            else:                                   # 하트 1개당 체력0일 경우 빈칸 그림
                self.Hp_image.clip_composite_draw(240, 0, 120, 360, 0, '', hx + i * 30, hy, 30, 90)

    def show_Bullet(self):
        bx = 1060
        by = 770

        if not changing:
            if position == 0:
                for i in range(8):                  # 샷건 최대 총알
                    if i < self.Bullet_shotgun:     # 샷건 현재 총알 수 만큼 그리고 없으면 빈칸
                        self.Bullet_image.clip_composite_draw(0, 0, 27, 50, 0, '', bx - i * 27, by, 27, 50)
                    else:
                        self.Bullet_image.clip_composite_draw(27, 0, 27, 50, 0, '', bx - i * 27, by, 27, 50)
            elif position == 1:
                for i in range(4):                  # 라이플 최대 총알
                    if i < self.Bullet_rifle:       # 라이플 현재 총알 수 만큼 그리고 없으면 빈칸
                        self.Bullet_image.clip_composite_draw(54, 0, 27, 50, 0, '', bx - i * 27, by, 27, 50)
                    else:
                        self.Bullet_image.clip_composite_draw(81, 0, 27, 50, 0, '', bx - i * 27, by, 27, 50)
            elif position == 2:
                for i in range(handgun_max_bullet): # 핸드건 최대 총알
                    if i < self.Bullet_handgun:     # 핸드건 최대 총알 수 만큼 그리고 없으면 빈칸
                        if i >= 20:
                            self.Bullet_image.clip_composite_draw(108, 0, 27, 50, 0, '', bx - (i - 20) * 28 , by - 56, 27, 50)
                        elif i >= 10:
                            self.Bullet_image.clip_composite_draw(108, 0, 27, 50, 0, '', bx - (i - 10) * 28 , by - 28, 27, 50)
                        else:
                            self.Bullet_image.clip_composite_draw(108, 0, 27, 50, 0, '', bx - i * 28, by, 27, 50)
                    else:
                        if i >= 20:
                            self.Bullet_image.clip_composite_draw(136, 0, 27, 50, 0, '', bx - (i - 20) * 28 , by - 56, 27, 50)
                        elif i >= 10:
                            self.Bullet_image.clip_composite_draw(136, 0, 27, 50, 0, '', bx - (i - 10) * 28, by - 28, 27, 50)
                        else:
                            self.Bullet_image.clip_composite_draw(136, 0, 27, 50, 0, '', bx - i * 28, by, 27, 50)

def handle_events():
    global running, MoveRight, Walking, Attack, AttackRight, attack_delay, position, state, Reload_shotgun, Reload_rifle, Reload_handgun,reload_time
    global Hit, hit_delay, Jump, jump_velocity, Fall, fall_velocity, changing, change_time, attack_time, a_pressed, d_pressed, Dash, dash_cooldown, move
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False

        # Esc 누를시 게임 종료
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

        if not Die:
            # d 누를시 오른쪽 으로 이동, a를 누르는 중에 눌러도 오른쪽 으로 이동
            if event.type == SDL_KEYDOWN and event.key == SDLK_d:
                if not Reload_rifle:
                    MoveRight = True
                Walking = True
                d_pressed = True
                Hit = False

            # d 손 땔시 오른쪽 이동 멈춤
            elif event.type == SDL_KEYUP and event.key == SDLK_d:
                d_pressed = False
                Hit = False
                if a_pressed:       # a키를 누르 면서 d를 땔시 다시 왼쪽 으로 이동
                    MoveRight = False
                if not a_pressed:   # 아닌 경우 멈춤
                    Walking = False

            # a 누를시 왼쪽 으로 이동, d를 누르는 중에 눌러도 왼쪽 으로 이동
            elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
                if not Reload_rifle:
                    MoveRight = False
                Walking = True
                a_pressed = True
                Hit = False

            # a 손 땔시 왼쪽 이동 멈춤
            elif event.type == SDL_KEYUP and event.key == SDLK_a:
                a_pressed = False
                Hit = False
                if d_pressed:       # d키를 누르 면서 a를 땔시 다시 오른쪽 으로 이동
                    MoveRight = True
                if not d_pressed:   # 아닌 경우 멈춤
                    Walking = False

            # space 누를시 점프
            elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE and not Jump and not Fall and not state == 1 and not Dash:
                Jump = True
                jump_velocity = 10.0
                Hit = False

            # r 누를시 샷건 재장전
            elif event.type == SDL_KEYDOWN and event.key == SDLK_r and not Attack and position == 0 and not Reload_shotgun and character.Bullet_shotgun == 0:
                Hit = False
                Reload_shotgun = True
                reload_time = 80

            # r 누를시 라이플 재장전
            elif event.type == SDL_KEYDOWN and event.key == SDLK_r and not Attack and position == 1 and not Reload_rifle and character.Bullet_rifle == 0:
                Hit = False
                Reload_rifle = True
                MoveRight = not MoveRight
                reload_time = 40
                hit_delay = 30

            # r 누를시 핸드건 재장전
            elif event.type == SDL_KEYDOWN and event.key == SDLK_r and not Attack and position == 2 and not Reload_handgun and character.Bullet_handgun == 0:
                Hit = False
                Reload_handgun = True
                reload_time = 30

            # shift 누를시 대쉬
            elif event.type == SDL_KEYDOWN and event.key == SDLK_LSHIFT and dash_cooldown == 0 and reload_time <= 10:
                Dash = True
                attack_delay = 2   # 타이밍 맞추면 평캔 가능
                Jump = False
                jump_velocity = 0.0
                Fall = False
                fall_velocity = 0.0
                state = 0
                dash_cooldown = 360
                hit_delay = 30
                if MoveRight:
                    move = 0
                elif not MoveRight:
                    move = 1

            # 샷건 -> 라이플 -> 핸드건 -> 샷건 폼 체인지, 스킬 사용, 공격, 재장전, 점프, 피격 중에는 불가능
            elif (
                    event.type == SDL_KEYDOWN and event.key == SDLK_z and state == 0 and not Attack and not Reload_shotgun and
                    not Reload_rifle and not Jump and not Fall and hit_delay == 0
            ):
                if position == 2:
                    position = 0
                else:
                    position += 1
                changing = True
                change_time = 3

            # 샷건 -> 핸드건 -> 라이플 -> 샷건 폼 체인지, 스킬 사용, 공격, 재장전, 점프, 피격 중에는 불가능
            elif (
                    event.type == SDL_KEYDOWN and event.key == SDLK_x and state == 0 and not Attack and not Reload_shotgun and
                    not Reload_rifle and not Jump and not Fall and hit_delay == 0
            ):
                if position == 0:
                    position = 2
                else:
                    position -= 1
                changing = True
                change_time = 3

            # 마우스 좌클릭 공격 (라이플 은 이동, 점프, 추락 중에 공격 불가), attack_delay == 공격 속도
            elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT and not Attack and attack_delay == 0:
                mouse_x, mouse_y = event.x, event.y
                Hit = False
                if position == 0 and state == 1:  # 샷건이 방패를 들고 있을 경우
                    if mouse_x < x:               # 캐릭터 보다 왼쪽 좌클릭 시 공격은 못 하지만 왼쪽 을 바라 봄
                        MoveRight = False
                    elif mouse_x > x:             # 캐릭터 보다 오른쪽 좌클릭 시 공격은 못 하지만 오른쪽 을 바라 봄
                        MoveRight = True

                elif (  # 나머지 경우
                        (position == 0 and state == 0 and character.Bullet_shotgun > 0) or
                        (position == 1 and not Walking and not Jump and not Fall and character.Bullet_rifle > 0) or
                        (position == 2 and state == 0 and character.Bullet_handgun > 0)
                ):
                    if position == 0:             # 샷건 총알 감소
                        character.Bullet_shotgun -= 1
                    elif position == 1:           # 라이플 총알 감소
                        character.Bullet_rifle -= 1
                    elif position == 2:           # 핸드건 총알 감소
                        character.Bullet_handgun -= 1

                    Attack = True
                    attack_time = 15              # 공격 모션 시간

                    if mouse_x < x:               # 캐릭터 보다 왼쪽 좌클릭 시 왼쪽 공격, 오른쪽 이동 중 에는 왼쪽 공격후 오른쪽 을 다시 바라 봄
                        AttackRight = False
                        if not Walking:           # 이동 중 공격이 아니면 공격 후 왼쪽 을 바라 봄
                            MoveRight = False
                    elif mouse_x > x:             # 캐릭터 보다 오른쪽 좌클릭 시 오른쪽 공격, 왼쪽 이동 중 에는 오른쪽 공격후 왼쪽 을 다시 바라 봄
                        AttackRight = True
                        if not Walking:           # 이동 중 공격이 아니면 공격 후 오른쪽 을 바라 봄
                            MoveRight = True

            # 샷건 일때 우클릭 중 일시 방패를 듬
            elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_RIGHT and not Attack and position == 0 and state == 0:
                state = 1

            # 샷건 일때 우클릭 땔시 방패를 내림
            elif event.type == SDL_MOUSEBUTTONUP and event.button == SDL_BUTTON_RIGHT and position == 0 and state == 1:
                state = 0

            # t 누를시 hp - 4
            elif event.type == SDL_KEYDOWN and event.key == SDLK_t:
                character.take_damage(8)

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

def check_collide(object):
    for o in object:
        if collide(x, y, o):
            return True
    return False

def collide(cx, cy, o):
    left_c, right_c = cx - 17, cx + 17

    top_c, bottom_c = cy + 18.0, cy - 50.0

    left_o, right_o = o.x - 15, o.x + 15

    top_o, bottom_o = o.y + 15, o.y - 15

    # 사각 충돌 체크
    if left_c < right_o and bottom_c < top_o and right_c > left_o and top_c > bottom_o:
        # print(f"캐릭터 좌표: ({left_c}, {right_c}), ({top_c}, {bottom_c})")
        # print(f"객체 좌표: ({left_o}, {right_o}), ({top_o}, {bottom_o})")
        return True
    return False

def check_collide_ad(object, speed):
    for o in object:
        if collide_ad(x, y, o, object, speed):
            return True
    return False

def collide_ad(cx, cy, o, object, speed):
    left_c, right_c = cx - 17, cx + 17

    top_c, bottom_c = cy + 18.0, cy - 50.0

    left_o, right_o = o.x - 25, o.x + 25

    top_o, bottom_o = o.y + 15, o.y - 15

    # 오른 쪽에 바닥이 있으면 안 떨어짐
    if MoveRight:
        if left_c > right_o > left_c - speed * 2 and bottom_c == top_o:
            if any(o2.x - 15 <= left_c <= o2.x + 15 and bottom_c == o2.y + 15 for o2 in object if o2 != o):
                return False
            return True

    # 왼 쪽에 바닥이 있으면 안 떨어짐
    elif not MoveRight:
        if right_c < left_o < right_c + speed * 2 and bottom_c == top_o:
            if any(o2.x - 15 <= right_c <= o2.x + 15 and bottom_c == o2.y + 15 for o2 in object if o2 != o):
                return False
            return True
    return False

def check_collide_jump(object):
    check_object = [o for o in world if isinstance(o, object)]
    for o in check_object:
        if collide_jump(x, y, o):
            return True
    return False

def collide_jump(cx, cy, o):
    global bottom_o
    left_c, right_c = cx - 17, cx + 17

    top_c, bottom_c = cy + 18.0, cy - 50.0

    left_o, right_o = o.x - 15, o.x + 15

    top_o, bottom_o = o.y + 15, o.y - 15

    # 천장에 캐릭터 머리가 부딫힘
    if left_c < right_o and top_c > bottom_o and right_c > left_o and top_c - jump_velocity < bottom_o:
        return True, bottom_o
    return False

def check_collide_fall(object):
    check_object = [o for o in world if isinstance(o, object)]
    for o in check_object:
        if collide_fall(x, y, o):
            return True
    return False

def collide_fall(cx, cy, o):
    global top_o
    left_c, right_c = cx - 17, cx + 17

    top_c, bottom_c = cy + 18.0, cy - 50.0

    left_o, right_o = o.x - 15, o.x + 15

    top_o, bottom_o = o.y + 15, o.y - 15

    # 바닥에 캐릭터 가 닿음
    if left_c < right_o and bottom_c < top_o and right_c > left_o and bottom_c + fall_velocity > top_o:
        return True, top_o
    return False

def update_world():
    background.update(dx)
    for o in world:
        o.update()
    character.update()

def render_world():
    clear_canvas()
    background.draw()
    for o in world:
        o.draw()
    character.draw()
    character.show_Hp()
    character.show_Bullet()
    update_canvas()

def reset_world():
    global running, grass, ground, character, world, background

    running = True
    world = []

    background = Background()

    grass = [Grass(i, 6) for i in range(18, 23 + 1)]
    world += grass

    grass = [Grass(i, 3) for i in range(10, 27 + 1) if (i < 16 or i > 20)]
    world += grass

    grass = [Grass(i, 2) for i in range(0, 108 + 1) if
             (i < 10 or i > 15) and (i < 21 or i > 27) and (i < 30 or i > 33) and (i < 44 or i > 49)]
    world += grass

    ground = [Ground(i, 2) for i in range(10, 27 + 1) if (i < 16 or i > 20)]
    world += ground

    for j in range(0, 1 + 1):
        ground = [Ground(i, j) for i in range(0, 108 + 1) if (i < 30 or i > 33) and (i < 44 or i > 49)]
        world += ground

    character = Draw_Character()

open_canvas(WIDTH, HEIGHT)

reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)

close_canvas()