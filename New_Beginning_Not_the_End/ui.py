from pico2d import load_image, load_font
from character import Character

class UI:
    image_hp = None
    image_bullet = None

    def __init__(self):
        if UI.image_hp == None:
            self.hp_image = load_image('Hp.png')
        if UI.image_bullet == None:
            self.bullet_image = load_image('Bullet.png')
        self.font = load_font('ENCR10B.TTF', 16)

    def update(self):
        pass

    def draw(self):
        heart_count = int(Character.max_hp / 2)
        hx = 20
        hy = 780

        for i in range(heart_count):
            if Character.hp >= (i + 1) * 2:
                self.hp_image.clip_composite_draw(0, 0, 120, 360, 0, '', hx + i * 30, hy, 30, 90)
            elif Character.hp == (i * 2) + 1:
                self.hp_image.clip_composite_draw(120, 0, 120, 360, 0, '', hx + i * 30, hy, 30, 90)
            else:
                self.hp_image.clip_composite_draw(240, 0, 120, 360, 0, '', hx + i * 30, hy, 30, 90)

        bx = 1060
        by = 770

        if Character.stance == 0:
            for i in range(8):
                if i < Character.bullet_SG:
                    self.bullet_image.clip_composite_draw(0, 0, 27, 50, 0, '', bx - i * 27, by, 27, 50)
                else:
                    self.bullet_image.clip_composite_draw(27, 0, 27, 50, 0, '', bx - i * 27, by, 27, 50)
            #if state == 1 or Reload_shotgun:
                #for i in range(shield_enhance):
                    #self.Bullet_image.clip_composite_draw(162, 0, 54, 50, 0, '', bx - i * 27 + 2, by - 40, 32, 30)
        elif Character.stance == 1:
            for i in range(4):
                if i < Character.bullet_RF:
                    self.bullet_image.clip_composite_draw(54, 0, 27, 50, 0, '', bx - i * 27, by, 27, 50)
                else:
                    self.bullet_image.clip_composite_draw(81, 0, 27, 50, 0, '', bx - i * 27, by, 27, 50)
            #if state == 1:
                #for i in range(snipe_bullet):
                    #self.Bullet_image.clip_composite_draw(216, 0, 54, 50, 0, '', bx - i * 39 + 11, by - 55, 69, 60)
        elif Character.stance == 2:
            for i in range(Character.max_bullet_HG):
                if i < Character.bullet_HG:
                    if i >= 20:
                        self.bullet_image.clip_composite_draw(108, 0, 27, 50, 0, '', bx - (i - 20) * 28, by - 56,
                                                              27, 50)
                    elif i >= 10:
                        self.bullet_image.clip_composite_draw(108, 0, 27, 50, 0, '', bx - (i - 10) * 28, by - 28,
                                                              27, 50)
                    else:
                        self.bullet_image.clip_composite_draw(108, 0, 27, 50, 0, '', bx - i * 28, by, 27, 50)
                else:
                    if i >= 20:
                        self.bullet_image.clip_composite_draw(136, 0, 27, 50, 0, '', bx - (i - 20) * 28, by - 56,
                                                              27, 50)
                    elif i >= 10:
                        self.bullet_image.clip_composite_draw(136, 0, 27, 50, 0, '', bx - (i - 10) * 28, by - 28,
                                                              27, 50)
                    else:
                        self.bullet_image.clip_composite_draw(136, 0, 27, 50, 0, '', bx - i * 28, by, 27, 50)

        self.font.draw(300, 40.0, 'Dash ', (0, 0, 175))
        if Character.dash_cooldown == 0:
            self.font.draw(350, 40.0, 'on', (0, 155, 0))
        elif not Character.dash_cooldown == 0:
            self.font.draw(350, 40.0, 'off', (205, 0, 0))