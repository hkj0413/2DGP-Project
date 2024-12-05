import server
import game_framework
import game_world

from pico2d import load_image

from cskillsg_crack import CskillCrackSG

mob_group = ['spore', 'slime', 'pig']

class CskillCrackSGEffect:
    image = None

    def __init__(self, d):
        self.x = server.character.x
        self.y = 140
        self.sx = 0
        self.frame = 0
        self.face = d
        if CskillCrackSGEffect.image == None:
            CskillCrackSGEffect.image = [load_image("./Effect/SG/" + 'C_SG_crack' + " (%d)" % i + ".png") for i in range(1, 3 + 1)]

    def update(self):
        self.sx = self.x - server.background.window_left
        self.frame = self.frame + 19.0 * 0.8 * game_framework.frame_time

        if self.frame > 19.0:
            cskillcracksg = CskillCrackSG(self.face)
            game_world.add_object(cskillcracksg, 3)
            for mob in mob_group:
                game_world.add_collision_pairs(f'cskillcracksg:{mob}', cskillcracksg, None)
            game_world.remove_object(self)

    def draw(self):
        if 15.0 < self.frame < 19.0:
            if self.face == 1:
                self.image[2].composite_draw(0, '', self.sx + 120, self.y + 120, 380, 358)
                self.image[2].composite_draw(0, '', self.sx + 370, self.y + 120, 380, 358)
                self.image[2].composite_draw(0, '', self.sx + 620, self.y + 120, 380, 358)
                self.image[2].composite_draw(0, '', self.sx + 120, self.y + 450, 380, 358)
                self.image[2].composite_draw(0, '', self.sx + 370, self.y + 450, 380, 358)
                self.image[2].composite_draw(0, '', self.sx + 620, self.y + 450, 380, 358)
            elif self.face == -1:
                self.image[2].composite_draw(0, '', self.sx - 120, self.y + 120, 380, 358)
                self.image[2].composite_draw(0, '', self.sx - 370, self.y + 120, 380, 358)
                self.image[2].composite_draw(0, '', self.sx - 620, self.y + 120, 380, 358)
                self.image[2].composite_draw(0, '', self.sx - 120, self.y + 450, 380, 358)
                self.image[2].composite_draw(0, '', self.sx - 370, self.y + 450, 380, 358)
                self.image[2].composite_draw(0, '', self.sx - 620, self.y + 450, 380, 358)
        if 9.0 < self.frame < 19.0:
            if self.face == 1:
                self.image[1].composite_draw(0, '', self.sx + 120, self.y + 120, 380, 358)
                self.image[1].composite_draw(0, '', self.sx + 370, self.y + 120, 380, 358)
                self.image[1].composite_draw(0, '', self.sx + 620, self.y + 120, 380, 358)
                self.image[1].composite_draw(0, '', self.sx + 120, self.y + 450, 380, 358)
                self.image[1].composite_draw(0, '', self.sx + 370, self.y + 450, 380, 358)
                self.image[1].composite_draw(0, '', self.sx + 620, self.y + 450, 380, 358)
            elif self.face == -1:
                self.image[1].composite_draw(0, '', self.sx - 120, self.y + 120, 380, 358)
                self.image[1].composite_draw(0, '', self.sx - 370, self.y + 120, 380, 358)
                self.image[1].composite_draw(0, '', self.sx - 620, self.y + 120, 380, 358)
                self.image[1].composite_draw(0, '', self.sx - 120, self.y + 450, 380, 358)
                self.image[1].composite_draw(0, '', self.sx - 370, self.y + 450, 380, 358)
                self.image[1].composite_draw(0, '', self.sx - 620, self.y + 450, 380, 358)
        if 6.0 < self.frame < 19.0:
            if self.face == 1:
                self.image[0].composite_draw(0, '', self.sx + 620, self.y + 120, 380, 358)
                self.image[0].composite_draw(0, '', self.sx + 620, self.y + 450, 380, 358)
            elif self.face == -1:
                self.image[0].composite_draw(0, '', self.sx - 620, self.y + 120, 380, 358)
                self.image[0].composite_draw(0, '', self.sx - 620, self.y + 450, 380, 358)
        if 3.0 < self.frame < 19.0:
            if self.face == 1:
                self.image[0].composite_draw(0, '', self.sx + 370, self.y + 120, 380, 358)
                self.image[0].composite_draw(0, '', self.sx + 370, self.y + 450, 380, 358)
            elif self.face == -1:
                self.image[0].composite_draw(0, '', self.sx - 370, self.y + 120, 380, 358)
                self.image[0].composite_draw(0, '', self.sx - 370, self.y + 450, 380, 358)
        if self.frame < 19.0:
            if self.face == 1:
                self.image[0].composite_draw(0, '', self.sx + 120, self.y + 120, 260, 358)
                self.image[0].composite_draw(0, '', self.sx + 120, self.y + 450, 260, 358)
            elif self.face == -1:
                self.image[0].composite_draw(0, '', self.sx - 120, self.y + 120, 260, 358)
                self.image[0].composite_draw(0, '', self.sx - 120, self.y + 450, 260, 358)