from pico2d import *

import random

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
Reload_rifle_s = False
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

die_time = 0       # 180 3초 (60 FPS)

dash_cooldown = 0  # 360 6초 (60 FPS)

target_down_cooldown = 0 # 1200 20초 (60 FPS)

bullet_time_cooldown = 0 # 600 10초 (60 FPS)

move = 0
snipe = 2
snipe_bullet = snipe
snipe_size = 45
spree = 0

jump_velocity = 0.0
fall_velocity = 0.0
gravity = 0.5

d_pressed = False
a_pressed = False
s_pressed =  False
lc_pressed = False

BG_WIDTH, BG_HEIGHT = 3240, 1200
ox = 0
dx = 0
xpos = 0
mouse_x = 0
mouse_y = 0

mob_damage = 0

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

class Block:
    image = None

    def __init__(self, i = 0, j = 0, k = 0):
        self.base_x = i * 30 + 15
        self.y  = j * 30 + 15
        self.framex = k
        if Block.image == None:
            Block.image = load_image('Block.png')

    def update(self):
        self.x = self.base_x - ox

    def draw(self):
        self.image.clip_draw(self.framex * 120, 0, 120, 120, self.x, self.y, 30, 30)

class Spore:
    image = None

    def __init__(self, i = 0, j = 0):
        self.x = 0
        self.base_x = i * 30 + 15
        self.y  = j * 30 + 15
        self.fx = i * 30 + 15
        self.fy = j * 30 + 15
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0
        self.framex = 0
        self.damage = 1
        self.state = random.randint(0, 1)
        if self.state == 0:
            self.framey = 3
        elif self.state == 1:
            self.framey = 1
        self.temp = 0
        self.move = 0
        self.stun = 0
        self.rand = random.randint(1, 2)
        if self.rand == 1:
            self.moveright = True
        elif self.rand == 2:
            self.moveright = False
        self.hp = 2
        if Spore.image == None:
            Spore.image = load_image('Spore.png')

    def update(self):
        self.temp += 1
        if self.state == 0:
            if self.temp % 8 == 0:
                self.framex = (self.framex + 1) % 4
                self.rand = random.randint(1, 20)
                if self.rand == 20:
                    self.state = 1
                    self.framex = 0
                    self.framey = 1
                    self.temp = 0
                if self.moveright:
                    self.move -= 3
                elif not self.moveright:
                    self.move += 3
                if (self.move > 90 and not self.moveright) or (self.move < -90 and self.moveright) or self.rand == 19:
                    self.moveright = not self.moveright

        elif self.state == 1:
            if self.temp % 70 == 0 and self.framex % 2 == 0:
                self.rand = random.randint(1, 5)
                if self.rand == 5 or self.temp == 210:
                    self.state = 0
                    self.framex = 0
                    self.framey = 3
                    self.temp = 0
                self.framex = (self.framex + 1) % 2
            elif self.temp % 10 == 0 and self.framex % 2 == 1:
                self.framex = (self.framex + 1) % 2

        elif self.state == 2:
            if self.temp == 30:
                if self.stun > 0:
                    self.state = 5
                else:
                    self.state = 1
                    self.framey = 1
                    self.temp = 0

        elif self.state == 3:
            if self.temp % 8 == 0 and self.temp < 32:
                self.framex = (self.framex + 1) % 4
            elif self.temp >= 100:
                self.framex = 4
                self.state = 4
                self.temp = 0
            elif self.temp >= 32:
                self.framex = 3

        elif self.state == 4:
            if self.temp == 300:
                self.framex = 0
                self.framey = 1
                self.temp = 0
                self.move = 0
                self.state = 1
                self.hp = 2
                self.rand = random.randint(1, 2)
                if self.rand == 1:
                    self.moveright = True
                elif self.rand == 2:
                    self.moveright = False
                self.base_x = self.fx
                self.y = self.fy

        elif self.state == 5:
            if not self.framex == 0:
                self.framex = 0
            if not self.framey == 0:
                self.framey = 0

        if not self.stun == 0:
            self.stun -= 1
            if self.stun <= 0:
                self.stun = 0
                if not self.state == 2 and not self.state == 3 and not self.state == 4:
                    self.state = 1
                    self.framey = 1
                    self.temp = 0
                elif self.state == 2:
                    self.state = 2

        self.x = self.base_x - ox + self.move
        self.left = self.x - 15
        self.right = self.x + 15
        self.top = self.y + 15
        self.bottom = self.y - 15

    def draw(self):
        if self.moveright:
            self.image.clip_composite_draw(self.framex * 50, self.framey * 50, 50, 50, 0, '', self.x, self.y, 50, 50)
        else:
            self.image.clip_composite_draw(self.framex * 50, self.framey * 50, 50, 50, 0, 'h', self.x, self.y, 50, 50)

    def take_damage(self, damage):
        self.hp -= damage
        self.temp = 0
        self.framex = 0
        self.framey = 0
        self.state = 2
        if self.hp <= 0:
            self.framey = 2
            self.state = 3
            self.hp = 0
            self.stun = 0

    def take_stun(self, time):
        self.stun = time

class Slime:
    image = None

    def __init__(self, i = 0, j = 0):
        self.x = 0
        self.base_x = i * 30 + 15
        self.y  = j * 30 + 40
        self.fx = i * 30 + 15
        self.fy = j * 30 + 40
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0
        self.framex = 0
        self.damage = 1
        self.state = random.randint(0, 1)
        if self.state == 0:
            self.framey = 3
        elif self.state == 1:
            self.framey = 1
        self.temp = 0
        self.move = 0
        self.stun = 0
        self.rand = random.randint(1, 2)
        if self.rand == 1:
            self.moveright = True
        elif self.rand == 2:
            self.moveright = False
        self.hp = 3
        if Slime.image == None:
            Slime.image = load_image('Slime.png')

    def update(self):
        self.temp += 1
        if self.state == 0:
            if self.temp % 7 == 0:
                self.framex = (self.framex + 1) % 7
                self.rand = random.randint(1, 20)
                if self.rand == 20:
                    self.state = 1
                    self.framex = 0
                    self.framey = 1
                    self.temp = 0
                if self.moveright:
                    self.move -= 4
                elif not self.moveright:
                    self.move += 4
                if (self.move > 120 and not self.moveright) or (self.move < -120 and self.moveright) or self.rand == 19:
                    self.moveright = not self.moveright

        elif self.state == 1:
            if self.temp % 36 == 0:
                self.rand = random.randint(1, 5)
            if self.temp % 10 == 0:
                if self.rand == 5 or self.temp == 180:
                    self.state = 0
                    self.framex = 0
                    self.framey = 3
                    self.temp = 0
                self.framex = (self.framex + 1) % 3

        elif self.state == 2:
            if self.temp == 30:
                if self.stun > 0:
                    self.state = 5
                else:
                    self.state = 1
                    self.framey = 1

        elif self.state == 3:
            if self.temp % 10 == 0 and self.temp < 40:
                self.framex = (self.framex + 1) % 4
            elif self.temp >= 100:
                self.framex = 4
                self.state = 4
                self.temp = 0
            elif self.temp >= 40:
                self.framex = 3

        elif self.state == 4:
            if self.temp == 300:
                self.framex = 0
                self.framey = 1
                self.temp = 0
                self.move = 0
                self.state = 1
                self.hp = 3
                self.rand = random.randint(1, 2)
                if self.rand == 1:
                    self.moveright = True
                elif self.rand == 2:
                    self.moveright = False
                self.base_x = self.fx
                self.y = self.fy

        elif self.state == 5:
            if not self.framex == 0:
                self.framex = 0
            if not self.framey == 0:
                self.framey = 0

        if not self.stun == 0:
            self.stun -= 1
            if self.stun <= 0:
                self.stun = 0
                if not self.state == 2 and not self.state == 3 and not self.state == 4:
                    self.state = 1
                    self.framey = 1
                    self.temp = 0
                elif self.state == 2:
                    self.state = 2

        self.x = self.base_x - ox + self.move
        self.left = self.x - 25
        self.right = self.x + 25
        self.top = self.y + 20
        self.bottom = self.y - 20

    def draw(self):
        if self.moveright:
            self.image.clip_composite_draw(self.framex * 70, self.framey * 85, 70, 85, 0, '', self.x + 10, self.y, 70, 85)
        else:
            self.image.clip_composite_draw(self.framex * 70, self.framey * 85, 70, 85, 0, 'h', self.x - 10, self.y, 70, 85)

    def take_damage(self, damage):
        self.hp -= damage
        self.temp = 0
        self.framex = 0
        self.framey = 0
        self.state = 2
        if self.hp <= 0:
            self.framey = 2
            self.state = 3
            self.hp = 0
            self.stun = 0

    def take_stun(self, time):
        self.stun = time

class Pig:
    image = None

    def __init__(self, i = 0, j = 0):
        self.x = 0
        self.base_x = i * 30 + 15
        self.y  = j * 30 + 25
        self.fx = i * 30 + 15
        self.fy = j * 30 + 25
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0
        self.framex = 0
        self.damage = 2
        self.state = random.randint(0, 1)
        if self.state == 0:
            self.framey = 3
        elif self.state == 1:
            self.framey = 1
        self.temp = 0
        self.move = 0
        self.stun = 0
        self.rand = random.randint(1, 2)
        if self.rand == 1:
            self.moveright = True
        elif self.rand == 2:
            self.moveright = False
        self.hp = 4
        if Pig.image == None:
            Pig.image = load_image('Pig.png')

    def update(self):
        self.temp += 1
        if self.state == 0:
            if self.temp % 8 == 0:
                self.framex = (self.framex + 1) % 3
                self.rand = random.randint(1, 20)
                if self.rand == 20:
                    self.state = 1
                    self.framex = 0
                    self.framey = 1
                    self.temp = 0
                if self.moveright:
                    self.move -= 2
                elif not self.moveright:
                    self.move += 2
                if (self.move > 60 and not self.moveright) or (self.move < -60 and self.moveright) or self.rand == 19:
                    self.moveright = not self.moveright

        elif self.state == 1:
            if self.temp % 60 == 0 and self.framex % 2 == 0:
                self.rand = random.randint(1, 5)
                if self.rand == 5 or self.temp == 180:
                    self.state = 0
                    self.framex = 0
                    self.framey = 3
                    self.temp = 0
                self.framex = (self.framex + 1) % 2
            elif self.temp % 20 == 0 and self.framex % 2 == 1:
                self.framex = (self.framex + 1) % 2

        elif self.state == 2:
            if self.temp == 30:
                self.framey = 1
                if self.stun > 0:
                    self.state = 5
                else:
                    self.state = 1

        elif self.state == 3:
            if self.temp % 8 == 0 and self.temp < 24:
                self.framex = (self.framex + 1) % 3
            elif self.temp >= 100:
                self.framex = 4
                self.state = 4
                self.temp = 0
            elif self.temp >= 32:
                self.framex = 3

        elif self.state == 4:
            if self.temp == 300:
                self.framex = 0
                self.framey = 1
                self.temp = 0
                self.move = 0
                self.state = 1
                self.hp = 4
                self.rand = random.randint(1, 2)
                if self.rand == 1:
                    self.moveright = True
                elif self.rand == 2:
                    self.moveright = False
                self.base_x = self.fx
                self.y = self.fy

        elif self.state == 5:
            if not self.framex == 0:
                self.framex = 0
            if not self.framey == 0:
                self.framey = 0

        if not self.stun == 0:
            self.stun -= 1
            if self.stun <= 0:
                self.stun = 0
                if not self.state == 2 and not self.state == 3 and not self.state == 4:
                    self.state = 1
                    self.framey = 1
                    self.temp = 0
                elif self.state == 2:
                    self.state = 2

        self.x = self.base_x - ox + self.move
        self.left = self.x - 30
        self.right = self.x + 30
        self.top = self.y + 25
        self.bottom = self.y - 25

    def draw(self):
        if self.moveright:
            self.image.clip_composite_draw(self.framex * 70, self.framey * 60, 70, 60, 0, '', self.x, self.y, 70, 60)
        else:
            self.image.clip_composite_draw(self.framex * 70, self.framey * 60, 70, 60, 0, 'h', self.x, self.y, 70, 60)

    def take_damage(self, damage):
        self.hp -= damage
        self.temp = 0
        self.framex = 0
        self.framey = 0
        self.state = 2
        if self.hp <= 0:
            self.framey = 2
            self.state = 3
            self.hp = 0
            self.stun = 0

    def take_stun(self, time):
        self.stun = time

class Obstacle:
    image = None

    def __init__(self, i=0, j=0.0, k=0, l=0):
        self.x = 0
        self.base_x = i * 30 + 15
        self.y = j * 30.0 + 15.0
        self.fy = j * 30.0 + 15.0
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0
        self.damage = 1
        self.temp = l
        self.state = 11
        self.gravity = 0.0
        self.framex = k
        if Obstacle.image == None:
            Obstacle.image = load_image('Coconut.png')

    def update(self):
        if self.state == 10:
            self.y -= self.gravity
            self.gravity += 0.25
            if self.y < -10:
                self.state = 11
                self.gravity = 0.0

        elif self.state == 11:
            self.temp += 1
            if self.temp == 180:
                self.state = 10
                self.temp = 0
                self.y = self.fy

        self.x = self.base_x - ox
        self.left = self.x - 10
        self.right = self.x + 10
        self.top = self.y + 5.0
        self.bottom = self.y - 5.0

    def draw(self):
        if self.state == 10:
            self.image.clip_draw(self.framex * 50, 0, 50, 50, self.x + 12, self.y + 12.0, 50, 50)

class Projectile:
    images = None

    def __init__(self, p):
        self.x = x
        self.y = y
        self.fx = x
        self.fy = y
        self.framex = 0
        self.temp = 0
        self.type = p
        self.count = 0
        if AttackRight:
            self.attackright = True
        elif not AttackRight:
            self.attackright = False
        if MoveRight:
            self.moveright = True
        elif not MoveRight:
            self.moveright = False
        if self.images == None:
            self.images = {
                "Lc_shotgun": load_image('HKCAWS_Lc.png'),
                "Lc_rifle": load_image('R93_Lc.png'),
                "Lc_rifle_enhance": load_image('R93_Lc_enhance.png'),
                "Lc_rifle_effect": load_image('R93_Lc_effect.png'),
                "Rc_rifle": load_image('R93_Rc.png'),
                "Reload_rifle_effect": load_image('R93_reload_effect.png'),
                "Lc_handgun": load_image('GSH18Mod_Lc.png'),
                "Lc_handgun_effect": load_image('GSH18Mod_Lc_effect.png'),
                "Dash_effect": load_image('Dash_effect.png'),
            }
        self.image = self.images["Lc_shotgun"]

    def update(self):
        global projectile
        self.temp += 1
        # 샷건 기본 공격
        if self.type == "lc_shotgun":                 # 샷건 기본 공격 사거리 9칸 / 0 ~ 68
            if self.temp == 1:
                self.image = self.images["Lc_shotgun"]
            if self.temp <= 15:
                for m in mob:
                    if m.state == 0 or m.state == 1 or m.state == 5:
                        if self.attackright:
                            if self.x <= m.left <= self.x + 60 and self.y + 18 >= m.bottom and self.y - 50 <= m.top:
                                m.take_damage(3)
                            elif self.x + 60 < m.left <= self.x + 120 and self.y + 18 >= m.bottom and self.y - 50 <= m.top:
                                m.take_damage(2)
                            elif self.x + 120 < m.left <= self.x + 180 and self.y + 18 >= m.bottom and self.y - 50 <= m.top:
                                m.take_damage(1)
                        elif not self.attackright:
                            if self.x - 60 <= m.right <= self.x and self.y + 18 >= m.bottom and self.y - 50 <= m.top:
                                m.take_damage(3)
                            elif self.x - 120 < m.right <= self.x - 60 and self.y + 18 >= m.bottom and self.y - 50 <= m.top:
                                m.take_damage(2)
                            elif self.x - 180 < m.right <= self.x - 120 and self.y + 18 >= m.bottom and self.y - 50 <= m.top:
                                m.take_damage(1)
            if self.temp % 5 == 0:
                self.framex = (self.framex + 1) % 9
            if self.temp == 45:
                projectile.remove(self)

        # 라이플 기본 공격
        elif self.type == "lc_rifle":                 # 라이플 기본 공격 사거리 24칸, 29칸 / 25 ~ 55, 20 ~ 60
            if self.temp == 1:
                self.image = self.images["Lc_rifle"]
            if self.attackright:
                self.fx += 20
            elif not self.attackright:
                self.fx -= 20
            if self.temp == 24 or self.count >= 4:
                projectile.remove(self)
            for m in mob:
                if m.state == 0 or m.state == 1 or m.state == 5:
                    if self.attackright:
                        if self.fx + 70 <= m.right and self.fx + 240 >= m.left and self.fy + 5 >= m.bottom and self.fy - 25 <= m.top:
                            m.take_damage(4)
                            self.count += 1
                    elif not self.attackright:
                        if self.fx - 240  <= m.right and self.fx - 70 >= m.left and self.fy + 5 >= m.bottom and self.fy - 25 <= m.top:
                            m.take_damage(4)
                            self.count += 1

        # 라이플 기본 공격 강화
        elif self.type == "lc_rifle_enhance":
            if self.temp == 1:
                self.image = self.images["Lc_rifle_enhance"]
            if self.temp % 4 == 0:
                self.framex = (self.framex + 1) % 4
            if self.attackright:
                self.fx += 30
            elif not self.attackright:
                self.fx -= 30
            if self.temp == 16 or self.count >= 6:
                projectile.remove(self)
            for m in mob:
                if m.state == 0 or m.state == 1 or m.state == 5:
                    if self.attackright:
                        if self.fx + 70 <= m.right and self.fx + 580 >= m.left and self.fy + 10 >= m.bottom and self.fy - 30 <= m.top:
                            m.take_damage(6)
                            self.count += 1
                    elif not self.attackright:
                        if self.fx - 580  <= m.right and self.fx - 70 >= m.left and self.fy + 10 >= m.bottom and self.fy - 30 <= m.top:
                            m.take_damage(6)
                            self.count += 1

        # 라이플 기본 공격 이펙트
        elif self.type == "lc_rifle_effect":
            if x > 580 and not ox == BG_WIDTH - WIDTH and MoveRight and Walking:
                self.x += -4
            elif x < 500 and not ox == 0 and not MoveRight and Walking:
                self.x += 4
            if x > 580 and not ox == BG_WIDTH - WIDTH and move == 0 and Dash:
                self.x += -20
            elif x < 500 and not ox == 0 and move == 1 and Dash:
                self.x += 20
            if self.temp == 1:
                self.image = self.images["Lc_rifle_effect"]
            if self.temp % 4 == 0:
                self.framex = (self.framex + 1) % 12
            if self.temp == 48:
                projectile.remove(self)

        # 라이플 타겟 다운 범위
        elif self.type == "rc_rifle":
            self.x = mouse_x
            self.y = 800 - mouse_y
            if self.temp == 1:
                self.count = 140
                self.image = self.images["Rc_rifle"]
            if self.temp <= 21 and  self.temp % 3 == 0:
                self.count -= 20
            if not state == 1:
                projectile.remove(self)

        # 라이플 장전 투망
        elif self.type == "reload_rifle_effect":
            if self.temp == 1:
                self.image = self.images["Reload_rifle_effect"]
            if self.moveright:
                self.fx -= 12
            elif not self.moveright:
                self.fx += 12
            if self.temp == 20 or self.count >= 1:
                projectile.remove(self)
            for m in mob:
                if m.state == 0 or m.state == 1 or m.state == 5:
                    if not self.moveright:
                        if self.fx + 90 <= m.right and self.fx + 122 >= m.left and self.fy + 10 >= m.bottom and self.fy - 30 <= m.top:
                            m.take_damage(0)
                            m.take_stun(120)
                            self.count += 1
                    elif self.moveright:
                        if self.fx - 122  <= m.right and self.fx - 90 >= m.left and self.fy + 10 >= m.bottom and self.fy - 30 <= m.top:
                            m.take_damage(0)
                            m.take_stun(120)
                            self.count += 1

        # 핸드건 기본 공격
        elif self.type == "lc_handgun":               # 핸드건 기본 공격 사거리 12칸 / 20 ~ 60
            if self.temp == 1:
                self.image = self.images["Lc_handgun"]
            if self.attackright:
                self.fx += 10
            elif not self.attackright:
                self.fx -= 10
            if self.temp == 36 or self.count >= 1:
                projectile.remove(self)
            for m in mob:
                if m.state == 0 or m.state == 1 or m.state == 5:
                    if self.attackright:
                        if self.fx <= m.right and self.fx + 30 >= m.left and self.fy + 10 >= m.bottom and self.fy - 30 <= m.top:
                            m.take_damage(1)
                            self.count += 1
                    elif not self.attackright:
                        if self.fx - 30 <= m.right and self.fx >= m.left and self.fy + 10 >= m.bottom and self.fy - 30 <= m.top:
                            m.take_damage(1)
                            self.count += 1

        # 핸드건 기본 공격 이펙트
        elif self.type == "lc_handgun_effect":
            if x > 580 and not ox == BG_WIDTH - WIDTH and MoveRight and Walking:
                self.x += -5
            elif x < 500 and not ox == 0 and not MoveRight and Walking:
                self.x += 5
            if x > 580 and not ox == BG_WIDTH - WIDTH and move == 0 and Dash:
                self.x += -20
            elif x < 500 and not ox == 0 and move == 1 and Dash:
                self.x += 20
            if self.temp == 1:
                self.image = self.images["Lc_handgun_effect"]
            if self.temp % 5 == 0:
                self.framex = (self.framex + 1) % 4
            if self.temp == 20:
                projectile.remove(self)

        # 대쉬 이펙트
        elif self.type == "dash_effect":
            if x > 580 and not ox == BG_WIDTH - WIDTH and move == 0:
                self.x += -40
            elif x < 500 and not ox == 0 and move == 1:
                self.x += 40
            if self.temp == 1:
                self.image = self.images["Dash_effect"]
            if self.temp == 10:
                projectile.remove(self)

    def draw(self):
        if self.type == "lc_shotgun":
            if self.attackright:
                self.image.clip_composite_draw(self.framex * 155, 0, 155, 157, 0, '', self.x + 70 + self.framex * 10, self.y - 17, 155, 157)
            elif not self.attackright:
                self.image.clip_composite_draw(self.framex * 155, 0, 155, 157, 0, 'h', self.x - 70 - self.framex * 10, self.y - 17, 155, 157)
        elif self.type == "lc_rifle":
            if self.attackright:
                self.image.clip_composite_draw(0, 0, 170, 70, 0, '', self.fx + 70, self.fy - 20, 170, 70)
            elif not self.attackright:
                self.image.clip_composite_draw(0, 0, 170, 70, 0, 'h', self.fx + 70, self.fy - 20, 170, 70)
        elif self.type == "lc_rifle_enhance":
            if self.attackright:
                self.image.clip_composite_draw(self.framex * 510, 0, 510, 113, 0, '', self.fx + 70, self.fy - 10, 510, 90)
            elif not self.attackright:
                self.image.clip_composite_draw(self.framex * 510, 0, 510, 113, 0, 'h', self.fx + 70, self.fy - 10, 510, 90)
        elif self.type == "lc_rifle_effect":
            if self.attackright:
                self.image.clip_composite_draw(self.framex * 67, 0, 67, 63, 0, '', self.x + 75, self.y - 10, 67, 63)
            elif not self.attackright:
                self.image.clip_composite_draw(self.framex * 67, 0, 67, 63, 0, 'h', self.x - 75, self.y - 10, 67, 63)
        elif self.type == "rc_rifle":
            self.image.clip_composite_draw(0, 0, 256, 256, 0, '', self.x, self.y, 64 + self.count, 64 + self.count)
        elif self.type == "reload_rifle_effect":
            if not self.moveright:
                self.image.clip_composite_draw(0, 0, 129, 207, 0, 'h', self.fx + 80, self.fy - 10, 33, 52)
            elif self.moveright:
                self.image.clip_composite_draw(0, 0, 129, 207, 0, '', self.fx + 80, self.fy - 10, 33, 52)
        elif self.type == "lc_handgun":
            if self.attackright:
                self.image.clip_composite_draw(0, 0, 10, 9, 0, '', self.fx, self.fy - 20, 30, 27)
            elif not self.attackright:
                self.image.clip_composite_draw(0, 0, 10, 9, 0, 'h', self.fx, self.fy - 20, 30, 27)
        elif self.type == "lc_handgun_effect":
            if self.attackright:
                self.image.clip_composite_draw(self.framex * 123, 0, 123, 125, 0, '', self.x + 36, self.y - 17, 62, 63)
            elif not self.attackright:
                self.image.clip_composite_draw(self.framex * 123, 0, 123, 125, 0, 'h', self.x - 36, self.y - 17, 62, 63)
        elif self.type == "dash_effect":
            if self.moveright:
                self.image.clip_composite_draw(self.framex * 66, 0, 66, 128, 0, 'h', self.x, self.y - 17, 66, 128)
            elif not self.moveright:
                self.image.clip_composite_draw(self.framex * 66, 0, 66, 128, 0, '', self.x, self.y - 17, 66, 128)

class Character:
    image_Hp = None
    image_Bullet = None

    def __init__(self):
        self.framex = 0
        self.temp = 0
        self.roll = 60
        self.Hp = 20                                                 # 현재 체력
        self.max_Hp = 20                                             # 최대 체력
        if Character.image_Hp == None:
            self.Hp_image = load_image('Hp.png')                     # 체력 그림
        self.Bullet_shotgun = 8                                      # 샷건 총알 개수
        self.Bullet_rifle = 4                                        # 라이플 총알 개수
        self.Bullet_handgun = handgun_max_bullet                     # 핸드건 총알 개수
        if Character.image_Bullet == None:                           # 총알 그림
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
            "spree_handgun": load_image('GSH18Mod_spree.png'),
            "ultimate_1_shotgun": load_image('HKCAWS_ultimate_1.png'),
            "ultimate_2_shotgun": load_image('HKCAWS_ultimate_2.png'),
        }
        self.image = self.images["wait_shotgun"]                     # 기본 캐릭터 그림

    def update(self):
        global MoveRight, Walking, changing, change_time, Attack, attack_time, attack_delay, Reload_shotgun, Reload_rifle, Reload_handgun, reload_time
        global Die, die_time, x, y, dx, ox, xpos, Jump, jump_velocity, Fall, fall_velocity, a_pressed, d_pressed, state, Hit, hit_delay
        global Dash, dash_cooldown, projectile, spree, bullet_time_cooldown, lc_pressed, s_pressed, Reload_rifle_s, target_down_cooldown
        self.temp += 1
        if Die:
            if die_time == 180:
                self.temp = 0
                self.framex = 0
                if position == 0:
                    self.image = self.images["die_shotgun"]
                elif position == 1:
                    self.image = self.images["die_rifle"]
                elif position == 2:
                    self.image = self.images["die_handgun"]
            if not position == 2:
                if die_time > 129:
                    if self.temp % 3 == 0:
                        if position == 0:
                            self.framex = (self.framex + 1) % 18       # 샷건 사망
                        elif position == 1:
                            self.framex = (self.framex + 1) % 18       # 라이플 사망
                else:
                    self.framex = 18
            elif position == 2:
                if die_time > 80:
                    if self.temp % 5 == 0:
                        self.framex = (self.framex + 1) % 21           # 핸드건 사망
                else:
                    self.framex = 21

        elif Reload_shotgun:
            if reload_time == 80:
                self.temp = 0
                self.framex = 0
                self.image = self.images["reload_shotgun"]
            if self.temp % 5 == 0:
                self.framex = (self.framex + 1) % 16

        elif Reload_rifle or Reload_rifle_s:
            if reload_time == 30:
                self.image = self.images["attack_rifle"]
            elif reload_time == 10:
                self.image = self.images["move_rifle"]
            if reload_time > 30 or 20 >= reload_time > 10:
                self.framex = 0
            elif 30 >= reload_time > 20:
                self.framex = 1
            else:
                self.framex = 0

        elif Reload_handgun:
            if reload_time == 30:
                self.temp = 0
                self.framex = 0
                self.roll = 60
                self.image = self.images["reload_handgun"]
            if self.temp % 4 == 0:
                self.framex = (self.framex + 1) % 10
                if self.roll >= 0:
                    self.roll -= 15

        elif position == 2 and state == 1:
            if self.image != self.images["spree_handgun"]:  # 핸드건 난사
                self.image = self.images["spree_handgun"]
                self.temp = 0
            if self.temp % 3 == 0:
                self.framex = (self.framex + 1) % 7
            if spree <= 0:
                state = 0
                self.Bullet_handgun = 0
                bullet_time_cooldown = 600
            if self.temp % 8 == 0:
                projectile += [Projectile("lc_handgun")]
                projectile += [Projectile("lc_handgun_effect")]
                spree -= 1
            if self.temp % 8 == 4:
                projectile += [Projectile("lc_handgun")]
                spree -= 1

        elif Hit:
            if hit_delay == 59:
                if position == 0:
                    self.image = self.images["damage_shotgun"]
                elif position == 1:
                    self.image = self.images["damage_rifle"]
                elif position == 2 and state == 0:
                    self.image = self.images["damage_handgun"]
            if position == 0 and state == 1:
                if self.image != self.images["shield_shotgun"]:
                    self.image = self.images["shield_shotgun"]
                if self.temp % 3 == 0:
                    self.framex = (self.framex + 1) % 14                    # 샷건 방패 들기 피격
            elif position == 1 and state == 1:
                if self.image != self.images["wait_rifle"]:                 # 라이플 저격 피격
                    self.image = self.images["wait_rifle"]
                if self.temp % 4 == 0:
                    self.framex = (self.framex + 1) % 14
            else:
                self.framex = 0                                             # 샷건, 라이플, 핸드건 피격

        elif Attack:
            if attack_time == 15:
                self.temp = 0
                self.framex = 0
                if position == 0:
                    self.image = self.images["attack_shotgun"]
                elif position == 1:
                    self.image = self.images["attack_rifle"]
                elif position == 2:
                    self.image = self.images["attack_handgun"]
            if self.temp % 4 == 0:
                if position == 0:
                    self.framex = (self.framex + 1) % 15                    # 샷건 공격
                elif position == 1:
                    self.framex = (self.framex + 1) % 7                     # 라이플 공격
                elif position == 2:
                    self.framex = (self.framex + 1) % 5                     # 핸드건 공격

        elif not Walking or (position == 1 and state == 1):
            if Jump or Fall or Dash:
                self.framex = 0
                if self.image != self.images["move_shotgun"] and position == 0:
                    self.image = self.images["move_shotgun"]                # 샷건 점프, 추락, 대쉬
                elif self.image != self.images["move_rifle"] and position == 1:
                    self.image = self.images["move_rifle"]                  # 라이플 점프, 추락, 대쉬
                elif self.image != self.images["move_handgun"] and position == 2:
                    self.image = self.images["move_handgun"]                # 핸드건 점프, 추락, 대쉬
            else:
                if self.temp % 4 == 0:
                    if position == 0:
                        if state == 0:
                            self.framex = (self.framex + 1) % 14
                            if self.image != self.images["wait_shotgun"]:   # 샷건 대기
                                self.image = self.images["wait_shotgun"]
                        elif state == 1:
                            self.framex = (self.framex + 1) % 14
                            if self.image != self.images["shield_shotgun"]: # 샷건 방패 들기 대기
                                self.image = self.images["shield_shotgun"]
                    elif position == 1:
                        self.framex = (self.framex + 1) % 14
                        if self.image != self.images["wait_rifle"]:         # 라이플 대기
                            self.image = self.images["wait_rifle"]
                    elif position == 2:
                        self.framex = (self.framex + 1) % 11
                        if self.image != self.images["wait_handgun"]:       # 핸드건 대기
                            self.image = self.images["wait_handgun"]

        elif Walking:
            if Jump or Fall or Dash:
                self.framex = 0
                if position == 0:
                    if self.image != self.images["move_shotgun"]:           # 샷건 점프, 추락 이동, 대쉬
                        self.image = self.images["move_shotgun"]
                elif position == 1:
                    if self.image != self.images["move_rifle"]:             # 라이플 점프, 추락 이동, 대쉬
                        self.image = self.images["move_rifle"]
                elif position == 2:
                    if self.image != self.images["move_handgun"]:           # 핸드건 점프, 추락 이동, 대쉬
                        self.image = self.images["move_handgun"]
            else:
                if position == 0 and state == 1:
                    if self.temp % 3 == 0:
                        self.framex = (self.framex + 1) % 14
                        if self.image != self.images["shield_shotgun"]:     # 샷건 방패 들기 이동
                            self.image = self.images["shield_shotgun"]
                else:
                    if self.temp % 4 == 0:
                        self.framex = (self.framex + 1) % 6
                        if position == 0 and state == 0:
                            if self.image != self.images["move_shotgun"]:   # 샷건 이동
                                self.image = self.images["move_shotgun"]
                        elif position == 1:
                            if self.image != self.images["move_rifle"]:     # 라이플 이동
                                self.image = self.images["move_rifle"]
                        elif position == 2:
                            if self.image != self.images["move_handgun"]:   # 핸드건 이동
                                self.image = self.images["move_handgun"]

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

        if Die:
            if die_time == 180:                                   # 사망 시간
                Walking = False
                Attack = False
                Reload_shotgun = False
                Reload_rifle = False
                Reload_rifle_s = False
                Reload_handgun = False
                Hit = False
                Jump = False
                Fall = False
                a_pressed = False
                d_pressed = False
                s_pressed = False
                lc_pressed = False
                change_time = 0
                attack_time = 0
                attack_delay = 0
                hit_delay = 0
                reload_time = 0
                jump_velocity = 0.0
                fall_velocity = 0.0
                if state == 1:
                    if position == 1:
                        target_down_cooldown = 1200
                    elif position == 2:
                        bullet_time_cooldown = 600
                state = 0
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
                hit_delay = 60
                if self.Hp == 0:
                    self.Hp = self.max_Hp
                    self.Bullet_shotgun = 8
                    self.Bullet_rifle = 4
                    self.Bullet_handgun = handgun_max_bullet

        if check_collide_mob():
            self.take_damage(mob_damage)

        if not hit_delay == 0:                                                         # 피격 면역 hit_delay == 0 이 되기 전까지 무적
            hit_delay -= 1
            if hit_delay <= 30 and Hit:
                Hit = False
            elif hit_delay <= 0:
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
                elif position == 2 and Reload_handgun:
                    if check_collide(world):
                        dx = 0
                        x += -2
                    else:
                        dx = 7
                        if check_collide_ad(world, 7) and not Jump and not Fall:
                            Fall = True
                elif position == 2 and not state == 1:
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
                elif position == 2 and Reload_handgun:                                 # 핸드건 장전 이동 속도
                    x += 7
                    if check_collide(world):
                        x += -7
                    elif check_collide_ad(world, 7) and not Jump and not Fall:
                        Fall = True
                elif position == 2 and not state == 1:                                 # 핸드건 이동 속도
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
                elif position == 2 and Reload_handgun:
                    if check_collide(world):
                        dx = 0
                        x += 2
                    else:
                        dx = -7
                        if check_collide_ad(world, 7) and not Jump and not Fall:
                            Fall = True
                elif position == 2 and not state == 1:
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
                elif position == 2 and Reload_handgun:                                 # 핸드건 장전 이동 속도
                    x += -7
                    if check_collide(world):
                        x += 7
                    elif check_collide_ad(world, 7) and not Jump and not Fall:
                        Fall = True
                elif position == 2 and not state == 1:                                 # 핸드건 이동 속도
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
                projectile += [Projectile("reload_rifle_effect")]
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

        if Reload_rifle_s:
            reload_time -= 1
            if reload_time == 30:
                jump_velocity = 6.0
                Fall = False
                fall_velocity = 0.0
                if not Jump:
                    Jump = True
                projectile += [Projectile("reload_rifle_effect")]
            elif reload_time <= 0:
                Reload_rifle_s = False
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
            elif check_collide_jump(Block):
                y = bottom_o - 18
                Jump = False
                Fall = True
                jump_velocity = 10.0

        if Fall:
            y -= fall_velocity                                    # 추락 가속도
            fall_velocity += gravity
            if check_collide_fall(Block):
                y = top_o + 50
                Fall = False
                fall_velocity = 0.0
            elif y < -68:
                Fall = False
                Die = True
                die_time = 180
                fall_velocity = 0.0

        if not target_down_cooldown == 0:
            target_down_cooldown -= 1
            if target_down_cooldown <= 0:
                target_down_cooldown = 0

        if not bullet_time_cooldown == 0:
            bullet_time_cooldown -= 1
            if bullet_time_cooldown <= 0:
                bullet_time_cooldown = 0

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
            elif Reload_rifle or Reload_rifle_s:
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
        global Walking, a_pressed, d_pressed, s_pressed, Hit, hit_delay, Jump, jump_velocity, Fall, Die, die_time
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
                s_pressed = False
            if self.Hp <= 0:
                self.Hp = 0
                Die =  True
                die_time = 180
            elif self.Hp > 0:
                Hit = True
                hit_delay = 60                             # 1초 무적 (60 FPS)
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
                if state == 1 or Reload_shotgun:
                    for i in range(shield_enhance): # 샷건 방어도
                        self.Bullet_image.clip_composite_draw(162, 0, 54, 50, 0, '', bx - i * 27 + 2, by - 40, 32, 30)
            elif position == 1:
                for i in range(4):                  # 라이플 최대 총알
                    if i < self.Bullet_rifle:       # 라이플 현재 총알 수 만큼 그리고 없으면 빈칸
                        self.Bullet_image.clip_composite_draw(54, 0, 27, 50, 0, '', bx - i * 27, by, 27, 50)
                    else:
                        self.Bullet_image.clip_composite_draw(81, 0, 27, 50, 0, '', bx - i * 27, by, 27, 50)
                if state == 1:
                    for i in range(snipe_bullet):   # 타겟 다운 최대 총알
                        self.Bullet_image.clip_composite_draw(216, 0, 54, 50, 0, '', bx - i * 39 + 11, by - 55, 69, 60)
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
    global Hit, hit_delay, Jump, jump_velocity, Fall, fall_velocity, changing, change_time, attack_time, a_pressed, d_pressed, s_pressed
    global Dash, dash_cooldown, move, mouse_x, mouse_y, lc_pressed, projectile, bullet_time_cooldown, spree, Reload_rifle_s, snipe_bullet, target_down_cooldown
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
                if not Reload_rifle and not (position == 2 and state == 1):
                    MoveRight = True
                Walking = True
                d_pressed = True
                Hit = False

            # d 손 땔시 오른쪽 이동 멈춤
            elif event.type == SDL_KEYUP and event.key == SDLK_d:
                d_pressed = False
                if a_pressed and not (position == 2 and state == 1): # a키를 누르 면서 d를 땔시 다시 왼쪽 으로 이동
                    MoveRight = False
                if not a_pressed:   # 아닌 경우 멈춤
                    Walking = False

            # a 누를시 왼쪽 으로 이동, d를 누르는 중에 눌러도 왼쪽 으로 이동
            elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
                if not Reload_rifle and not (position == 2 and state == 1):
                    MoveRight = False
                Walking = True
                a_pressed = True
                Hit = False

            # a 손 땔시 왼쪽 이동 멈춤
            elif event.type == SDL_KEYUP and event.key == SDLK_a:
                a_pressed = False
                if d_pressed and not (position == 2 and state == 1): # d키를 누르 면서 a를 땔시 다시 오른쪽 으로 이동
                    MoveRight = True
                if not d_pressed:   # 아닌 경우 멈춤
                    Walking = False

            elif event.type == SDL_KEYDOWN and event.key == SDLK_s:
                s_pressed = True

            elif event.type == SDL_KEYUP and event.key == SDLK_s:
                s_pressed = False

            # space 누를시 점프
            elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE and not Jump and not Fall and not (position == 0 and state == 1) and not Dash:
                Jump = True
                jump_velocity = 10.0
                Hit = False

            # r 누를시 샷건 재장전
            elif event.type == SDL_KEYDOWN and event.key == SDLK_r and not Attack and position == 0 and not Reload_shotgun and character.Bullet_shotgun == 0:
                Hit = False
                Reload_shotgun = True
                reload_time = 80

            # r 누를시 라이플 재장전
            elif event.type == SDL_KEYDOWN and event.key == SDLK_r and not Attack and position == 1 and not Reload_rifle and not Reload_rifle_s and s_pressed and character.Bullet_rifle == 0:
                Hit = False
                Reload_rifle_s = True
                MoveRight = not MoveRight
                reload_time = 40
                hit_delay = 30

            # r 누를시 라이플 재장전
            elif event.type == SDL_KEYDOWN and event.key == SDLK_r and not Attack and position == 1 and not Reload_rifle and not Reload_rifle_s and character.Bullet_rifle == 0:
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
                hit_delay = 30

            # shift 누를시 대쉬
            elif event.type == SDL_KEYDOWN and event.key == SDLK_LSHIFT and dash_cooldown == 0 and reload_time <= 10:
                Dash = True
                attack_delay = 2   # 타이밍 맞추면 평캔 가능
                Jump = False
                jump_velocity = 0.0
                Fall = False
                fall_velocity = 0.0
                dash_cooldown = 360
                hit_delay = 30
                if MoveRight:
                    move = 0
                elif not MoveRight:
                    move = 1
                if position == 0:
                    if state == 1:
                        state = 0
                elif position == 1:
                    if state == 1:
                        state = 0
                        snipe_bullet = snipe
                        target_down_cooldown = 1200
                elif position == 2:
                    if state == 1:
                        state = 0
                        character.Bullet_handgun = spree // 2
                        spree = 0
                        bullet_time_cooldown = 600
                projectile += [Projectile("dash_effect")]

            # 샷건 -> 라이플 -> 핸드건 -> 샷건 폼 체인지, 스킬 사용, 공격, 재장전, 점프, 피격 중에는 불가능
            elif (
                    event.type == SDL_KEYDOWN and event.key == SDLK_z and state == 0 and not Attack and not Reload_shotgun and
                    not Reload_rifle and not Reload_handgun and not Jump and not Fall and hit_delay <= 30
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
                    not Reload_rifle and not Reload_handgun and not Jump and not Fall and hit_delay <= 30
            ):
                if position == 0:
                    position = 2
                else:
                    position -= 1
                changing = True
                change_time = 3

            # 마우스 좌클릭 공격
            elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
                mouse_x, mouse_y = event.x, event.y
                lc_pressed = True

            # 마우스 좌클릭 을 때기 전까지 계속 공격
            elif event.type == SDL_MOUSEBUTTONUP and event.button == SDL_BUTTON_LEFT:
                lc_pressed = False

            # 만약 마우스 위치가 바껴서 공격 방향도 바뀌 는지 확인
            elif event.type == SDL_MOUSEMOTION and (lc_pressed or position == 1 and state == 1):
                mouse_x, mouse_y = event.x, event.y

            # 샷건 일때 우클릭 중 일시 방패를 듬
            elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_RIGHT and not Attack and position == 0 and state == 0:
                state = 1

            # 샷건 일때 우클릭 땔시 방패를 내림
            elif event.type == SDL_MOUSEBUTTONUP and event.button == SDL_BUTTON_RIGHT and position == 0 and state == 1:
                state = 0

            elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_RIGHT and not Attack and position == 1 and state == 0 and target_down_cooldown == 0:
                mouse_x, mouse_y = event.x, event.y
                state = 1
                projectile += [Projectile("rc_rifle")]
                if mouse_x < x:
                    AttackRight = False
                    MoveRight = False
                elif mouse_x > x:
                    AttackRight = True
                    MoveRight = True

            elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_RIGHT and not Attack and position == 2 and state == 0 and bullet_time_cooldown == 0 and not Reload_handgun:
                mouse_x, mouse_y = event.x, event.y
                state = 1
                spree = character.Bullet_handgun * 2
                if mouse_x < x:
                    AttackRight = False
                    MoveRight = False
                elif mouse_x > x:
                    AttackRight = True
                    MoveRight = True

            # t 누를시 hp - 8
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

            # f 누를시 모든 쿨타임 초기화
            elif event.type == SDL_KEYDOWN and event.key == SDLK_f:
                dash_cooldown = 0
                target_down_cooldown = 0
                bullet_time_cooldown = 0

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
    check_object = [o for o in world if isinstance(o, object) and o.framex == 1]
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
    check_object = [o for o in world if isinstance(o, object) and o.framex == 1]
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

def check_collide_mob():
    if not Die and hit_delay == 0:
        for m in mob:
            if not m.state == 3 and not m.state == 4:
                if collide_mob(x, y, m):
                    return True
    return False

def collide_mob(cx, cy, m):
    global mob_damage
    left_c, right_c = cx - 17, cx + 17

    top_c, bottom_c = cy + 18.0, cy - 50.0

    if left_c < m.right and bottom_c < m.top and right_c > m.left and top_c > m.bottom:
        mob_damage = m.damage
        # print(f"캐릭터 좌표: ({left_c}, {right_c}), ({top_c}, {bottom_c})")
        # print(f"객체 좌표: ({m.left}, {m.right}), ({m.top}, {m.bottom})")
        return True
    return False

def attacking():
    global MoveRight, AttackRight, Attack, attack_delay, attack_time, Hit, projectile, state, snipe, snipe_bullet, target_down_cooldown
    if lc_pressed and not Attack and attack_delay == 0: # 공격 (라이플 은 이동, 점프, 추락 중에 공격 불가), attack_delay == 공격 속도
        if position == 0 and state == 1:  # 샷건이 방패를 들고 있을 경우
            if mouse_x < x:  # 캐릭터 보다 왼쪽 좌클릭 시 공격은 못 하지만 왼쪽 을 바라 봄
                MoveRight = False
            elif mouse_x > x:  # 캐릭터 보다 오른쪽 좌클릭 시 공격은 못 하지만 오른쪽 을 바라 봄
                MoveRight = True
        elif position == 1 and state == 1:  # 라이플 타겟 다운 중
            if mouse_x < x:  # 캐릭터 보다 왼쪽 좌클릭 시 왼쪽 을 바라 보며 사격
                AttackRight = False
                MoveRight = False
            elif mouse_x > x:  # 캐릭터 보다 오른쪽 좌클릭 시 오른쪽 을 바라 보며 사격
                AttackRight = True
                MoveRight = True

            Attack = True
            attack_time = 15

            if snipe_bullet > 0:
                snipe_bullet -= 1
                projectile += [Projectile("lc_rifle_enhance")]
                projectile += [Projectile("lc_rifle_effect")]
                if snipe_bullet == 0:
                    state = 0
                    snipe_bullet = snipe
                    target_down_cooldown = 1200

        elif position == 2 and state == 1:  # 핸드건 쌍권총 난사 중
            if mouse_x < x:  # 캐릭터 보다 왼쪽 좌클릭 시 왼쪽 으로 공격 방향 전환
                AttackRight = False
                MoveRight = False
            elif mouse_x > x:  # 캐릭터 보다 오른쪽 좌클릭 시 오른쪽 으로 공격 방향 전환
                AttackRight = True
                MoveRight = True

        elif (  # 나머지 경우
                (position == 0 and state == 0 and character.Bullet_shotgun > 0) or
                (position == 1 and not Walking and not Jump and not Fall and character.Bullet_rifle > 0) or
                (position == 2 and state == 0 and character.Bullet_handgun > 0)
        ):
            if mouse_x < x:  # 캐릭터 보다 왼쪽 좌클릭 시 왼쪽 공격, 오른쪽 이동 중 에는 왼쪽 공격후 오른쪽 을 다시 바라 봄
                AttackRight = False
                if not Walking:  # 이동 중 공격이 아니면 공격 후 왼쪽 을 바라 봄
                    MoveRight = False
            elif mouse_x > x:  # 캐릭터 보다 오른쪽 좌클릭 시 오른쪽 공격, 왼쪽 이동 중 에는 오른쪽 공격후 왼쪽 을 다시 바라 봄
                AttackRight = True
                if not Walking:  # 이동 중 공격이 아니면 공격 후 오른쪽 을 바라 봄
                    MoveRight = True

            if position == 0:  # 샷건 총알 감소
                Hit = False
                character.Bullet_shotgun -= 1
                projectile += [Projectile("lc_shotgun")]
            elif position == 1:  # 라이플 총알 감소
                Hit = False
                character.Bullet_rifle -= 1
                if character.Bullet_rifle > 0:
                    projectile += [Projectile("lc_rifle")]
                else:
                    projectile += [Projectile("lc_rifle_enhance")]
                projectile += [Projectile("lc_rifle_effect")]
            elif position == 2:  # 핸드건 총알 감소
                Hit = False
                character.Bullet_handgun -= 1
                projectile += [Projectile("lc_handgun")]
                projectile += [Projectile("lc_handgun_effect")]

            Attack = True
            attack_time = 15  # 공격 모션 시간

def update_world():
    background.update(dx)
    for o in world:
        o.update()
    attacking()
    for p in projectile:
        p.update()
    for m in mob:
        m.update()
    character.update()

def render_world():
    clear_canvas()
    background.draw()
    for o in world:
        o.draw()
    character.draw()
    for m in mob:
        m.draw()
    for p in projectile:
        p.draw()
    character.show_Hp()
    character.show_Bullet()
    update_canvas()

def reset_world():
    global running, grass, ground, character, world, background, mob, projectile

    running = True
    world = []
    mob = []
    projectile = []

    background = Background()

    plank_positions = [
        (range(3, 12), 29),
    ]

    for i_range, j in plank_positions:
        world += [Block(j, i, 2) for i in i_range]

    grass_positions = [
        (13, range(13, 21)),
        (12, range(26, 30)),
        (11, range(2, 4)),
        (9, range(6, 8)),
        (7, range(11, 16)),
        (5, range(19, 26)),
        (2, range(0, 30)),
        (2, range(34, 44)),
        (2, range(50, 109)),
    ]

    for j, i_range in grass_positions:
        world += [Block(i, j, 1) for i in i_range]

    ground_positions = [
        (1, range(0, 30)),
        (1, range(34, 44)),
        (1, range(50, 109)),
        (0, range(0, 30)),
        (0, range(34, 44)),
        (0, range(50, 109)),
    ]

    for j, i_range in ground_positions:
        world += [Block(i, j, 0) for i in i_range]

    # world +=[Block(9, 2, 2)]

    mob += [Spore(7, 3)]
    mob += [Slime(9, 3)]
    mob += [Spore(11, 3)]
    mob += [Spore(13, 3)]
    mob += [Spore(17, 3)]
    mob += [Spore(22, 6)]
    mob += [Spore(16, 14)]
    mob += [Pig(18, 14)]

    mob += [Obstacle(9, 20, 0, 0)]
    mob += [Obstacle(32, 25, 0, 90)]

    character = Character()

open_canvas(WIDTH, HEIGHT)

reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)

close_canvas()