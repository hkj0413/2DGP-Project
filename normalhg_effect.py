import server
import game_framework
import game_world

from pico2d import load_image

class NormalHGEffect:
    image = None

    def __init__(self, d):
        self.x = server.character.x + 18 * d
        self.y = server.character.y
        self.sx = 0
        self.timer = 0
        self.temp = 0
        self.face = d
        if NormalHGEffect.image == None:
            NormalHGEffect.image = load_image("./Effect/HG/" + 'Lc_HG' + " (1)" + ".png")

    def update(self):
        self.sx = self.x - server.background.window_left

        self.timer += game_framework.frame_time

        if self.timer >= 0.01:
            self.timer = 0
            self.temp += 1
            self.x += 10 * self.face
            if self.temp == 36:
                game_world.remove_object(self)

    def draw(self):
        if self.temp < 36:
            if self.face == 1:
                self.image.composite_draw(0, '', self.sx + 15, self.y - 10, 30, 27)
            elif self.face == -1:
                self.image.composite_draw(0, 'h', self.sx - 15, self.y - 10, 30, 27)