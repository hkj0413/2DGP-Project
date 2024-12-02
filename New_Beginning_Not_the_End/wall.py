import server
import character

from pico2d import load_image, draw_rectangle

class Wall:
    image = None

    def __init__(self, i=0, j=0.0, k=0):
        self.x = i * 30.0 + 15.0
        self.y = j * 30.0 + 15.0
        self.frame = k - 1
        self.sx = 0
        if Wall.image == None:
            Wall.image = [load_image("./Block/" + 'Block' + " (%d)" % i + ".png") for i in range(1, 15 + 1)]

    def update(self):
        self.sx = self.x - server.background.window_left

    def draw(self):
        if -15 <= self.sx <= 1095:
            self.image[self.frame].draw(self.sx, self.y, 30, 30)
            if character.God:
                draw_rectangle(*self.get_rect())

    def get_bb(self):
        return self.x - 15.0, self.y - 15.0, self.x + 15.0, self.y + 15.0

    def get_rect(self):
        return self.sx - 15.0, self.y - 15.0, self.sx + 15.0, self.y + 15.0

    def handle_collision(self, group, other):
        pass
