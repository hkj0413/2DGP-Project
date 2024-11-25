import server
import character

from pico2d import load_image, draw_rectangle

class Ladder:
    image = None

    def __init__(self, i=0, j=0.0, k=0, l=0):
        self.x = i * 30.0 + 15.0
        self.y = j * 30.0 + 15.0
        self.framex = k
        self.framey = l
        self.sx = 0
        if Ladder.image == None:
            Ladder.image = load_image('Block.png')

    def update(self):
        self.sx = self.x - server.background.window_left

    def draw(self):
        if -15 <= self.sx <= 1095:
            self.image.clip_draw(self.framex * 120, self.framey * 120, 120, 120, self.sx, self.y, 30, 30)
        if character.RectMode:
            draw_rectangle(*self.get_rect())

    def get_bb(self):
        return self.x - 15.0, self.y - 15.0, self.x + 15.0, self.y + 15.0

    def get_rect(self):
        return self.sx - 15.0, self.y - 15.0, self.sx + 15.0, self.y + 15.0

    def handle_collision(self, group, other):
        pass