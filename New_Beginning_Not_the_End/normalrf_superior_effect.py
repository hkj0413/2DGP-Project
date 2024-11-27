import server
import game_framework
import game_world

from pico2d import load_image

class NormalRFSPEffect:
    image = None

    def __init__(self, d):
        self.x = server.character.x
        self.y = server.character.y
        self.sx = 0
        self.timer = 0
        self.temp = 0
        self.face = d
        if NormalRFSPEffect.image == None:
            NormalRFSPEffect.image = load_image("./Effect/RF/" + 'Lc_RF_superior' + " (1)" + ".png")

    def update(self):
        self.sx = self.x - server.background.window_left

        self.timer += game_framework.frame_time

        if self.timer >= 0.01:
            self.timer = 0
            self.temp += 1
            self.x += 30
            if self.temp == 16:
                game_world.remove_object(self)

    def draw(self):
        if -15 <= self.sx <= 1095:
            if self.temp < 16:
                if self.face == 1:
                    self.image.composite_draw(0, '', self.sx + 70, self.y - 10, 510, 90)
                elif self.face == -1:
                    self.image.composite_draw(0, 'h', self.sx - 70, self.y - 10, 510, 90)