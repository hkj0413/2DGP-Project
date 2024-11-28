from pico2d import load_image, load_font

from character import Character

import character

class UI:
    image_hp = None
    image_bullet = None
    image_dash = None
    image_rc_sg = None
    image_rc_hg = None

    def __init__(self):
        if UI.image_hp == None:
            self.hp_image = [load_image("./Icon/" + 'Heart' + " (%d)" % i + ".png") for i in range(1, 3 + 1)]
        if UI.image_bullet == None:
            self.bullet_image = load_image('Bullet.png')
        if UI.image_dash == None:
            self.image_dash = load_image("./Icon/" + 'All_dash' + ".png")
        if UI.image_rc_sg == None:
            self.image_rc_sg = load_image("./Icon/" + 'SG_defensive_stance' + ".png")
        if UI.image_rc_hg == None:
            self.image_rc_hg = load_image("./Icon/" + 'HG_agile_shooting' + ".png")
        self.font = load_font('ENCR10B.TTF', 20)

    def update(self):
        pass

    def draw(self):
        heart_count = int(Character.max_hp / 2)
        hx = 20
        hy = 780

        for i in range(heart_count):
            if Character.hp >= (i + 1) * 2:
                self.hp_image[0].draw(hx + i * 30, hy, 30, 30)
            elif Character.hp == (i * 2) + 1:
                self.hp_image[1].draw(hx + i * 30, hy, 30, 30)
            else:
                self.hp_image[2].draw(hx + i * 30, hy, 30, 30)

        bx = 1060
        by = 770

        self.font.draw(560, 780.0, f'Score : {Character.score}', (0, 0, 0))

        if Character.dash_cooldown == 0:
            self.image_dash.draw(124, 40, 48 ,48)

        if Character.stance == 0:
            self.image_rc_sg.draw(124 + 64 * 3, 40, 48 ,48)

            for i in range(8):
                if i < Character.bullet_SG:
                    self.bullet_image.clip_composite_draw(0, 0, 27, 50, 0, '', bx - i * 27, by, 27, 50)
                else:
                    self.bullet_image.clip_composite_draw(27, 0, 27, 50, 0, '', bx - i * 27, by, 27, 50)
            if Character.state == 1 or character.Reload_SG:
                for i in range(Character.shield_def):
                    self.bullet_image.clip_composite_draw(162, 0, 54, 50, 0, '', bx - i * 27 + 2, by - 40, 32, 30)
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
            if Character.agile_shooting_cooldown == 0:
                self.image_rc_hg.draw(124 + 64 * 3, 40, 48 ,48)

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