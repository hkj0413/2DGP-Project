import server
import game_framework
import game_world

from pico2d import load_image

class NormalSGEffcet:
    image = None

    def __init__(self, d):
        self.x = server.character.x
        self.y = server.character.y
        self.sx = 0
        self.framex = 0
        self.face = d
        if NormalSGEffcet.image == None:
            NormalSGEffcet.image = load_image("./Effect/" + 'Lc_SG' + ".png")

    def update(self):
        self.sx = self.x - server.background.window_left
        self.framex = self.framex + 9.0 * 1.5 * game_framework.frame_time
        if self.framex > 8.0:
            game_world.remove_object(self)

    def draw(self):
        if -15 <= self.sx <= 1095:
            if self.framex <= 8.0:
                if self.face == 1:
                    self.image.clip_composite_draw(int(self.framex) * 155, 0, 155, 157, 0, '',
                                                   self.sx + 60 + int(self.framex) * 10, self.y - 17, 155, 157)
                elif self.face == -1:
                    self.image.clip_composite_draw(int(self.framex) * 155, 0, 155, 157, 0, 'h',
                                                   self.sx - 60 - int(self.framex) * 10, self.y - 17, 155, 157)