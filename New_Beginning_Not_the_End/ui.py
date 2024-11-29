from pico2d import load_image, load_font

from character import Character

import character

class UI:
    image_hp = None
    image_bullet = None
    image_dash = None
    image_rc_sg = None
    image_rc_rf = None
    image_rc_hg = None

    def __init__(self):
        if UI.image_hp == None:
            self.hp_image = [load_image("./Icon/" + 'Heart' + " (%d)" % i + ".png") for i in range(1, 3 + 1)]
        if UI.image_bullet == None:
            self.bullet_image = [load_image("./Icon/" + 'Bullet' + " (%d)" % i + ".png") for i in range(1, 8 + 1)]
        if UI.image_dash == None:
            self.image_dash = load_image("./Icon/" + 'All_dash' + ".png")
        if UI.image_rc_sg == None:
            self.image_rc_sg = load_image("./Icon/" + 'SG_defensive_stance' + ".png")
        if UI.image_rc_rf == None:
            self.image_rc_rf = load_image("./Icon/" + 'RF_target_down' + ".png")
        if UI.image_rc_hg == None:
            self.image_rc_hg = load_image("./Icon/" + 'HG_agile_shooting' + ".png")
        #self.font = load_font('ENCR10B.TTF', 20)

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

        #self.font.draw(560, 780.0, f'Score : {Character.score}', (0, 0, 0))

        if Character.dash_cooldown == 0:
            self.image_dash.draw(124, 40, 48 ,48)

        if Character.stance == 0:
            self.image_rc_sg.draw(124 + 64 * 3, 40, 48 ,48)

            for i in range(8):
                if i < Character.bullet_SG:
                    self.bullet_image[0].draw(bx - i * 27, by, 27, 50)
                else:
                    self.bullet_image[1].draw(bx - i * 27, by, 27, 50)
            if Character.state == 1 or character.Reload_SG:
                for i in range(Character.shield_def):
                    self.bullet_image[6].draw(bx - i * 27, by - 40, 25, 30)
        elif Character.stance == 1:
            if Character.target_down_cooldwon == 0:
                self.image_rc_rf.draw(124 + 64 * 3, 40, 48 ,48)

            for i in range(4):
                if i < Character.bullet_RF:
                    self.bullet_image[2].draw(bx - i * 27, by)
                else:
                    self.bullet_image[3].draw(bx - i * 27, by)
            if Character.state == 1:
                for i in range(Character.target_down_bullet):
                    self.bullet_image[7].draw(bx - i * 39 , by - 40, 33, 30)
                self.bullet_image[7].draw(character.mouse_x, 800 - character.mouse_y, 120 - Character.target_down_size,
                                          120 - Character.target_down_size)
        elif Character.stance == 2:
            if Character.agile_shooting_cooldown == 0:
                self.image_rc_hg.draw(124 + 64 * 3, 40, 48 ,48)

            for i in range(Character.max_bullet_HG):
                if i < Character.bullet_HG:
                    if i >= 20:
                        self.bullet_image[4].draw(bx - (i - 20) * 27, by - 44)
                    elif i >= 10:
                        self.bullet_image[4].draw(bx - (i - 10) * 27, by - 17)
                    else:
                        self.bullet_image[4].draw(bx - i * 27, by + 10)
                else:
                    if i >= 20:
                        self.bullet_image[5].draw(bx - (i - 20) * 27, by - 44)
                    elif i >= 10:
                        self.bullet_image[5].draw(bx - (i - 10) * 27, by - 17)
                    else:
                        self.bullet_image[5].draw(bx - i * 27, by + 10)