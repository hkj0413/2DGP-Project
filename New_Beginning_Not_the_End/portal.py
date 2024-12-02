import server
import character

from pico2d import load_image, draw_rectangle

class Portal:
    image = None

    def __init__(self, i=0.0, j=0.0):
        self.x = i * 30.0 + 15.0
        self.y = j * 30.0 + 15.0
        self.sx = 0
        if Portal.image == None:
            Portal.image = load_image("./Block/" + 'Block' + " (15)" + ".png")

    def update(self):
        self.sx = self.x - server.background.window_left

    def draw(self):
        if -45 <= self.sx <= 1080 + 45:
            self.image.draw(self.sx, self.y, 90, 90)
            if character.God:
                draw_rectangle(*self.get_rect())

    def get_bb(self):
        return self.x - 45.0, self.y - 45.0, self.x + 45.0, self.y + 45.0

    def get_rect(self):
        return self.sx - 45.0, self.y - 45.0, self.sx + 45.0, self.y + 45.0

    def handle_collision(self, group, other):
        pass