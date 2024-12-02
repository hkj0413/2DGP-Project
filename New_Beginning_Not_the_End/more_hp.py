import server
import character
import game_world

from pico2d import load_image, draw_rectangle

class MoreHP:
    image = None

    def __init__(self, i=0, j=0.0):
        self.x = i * 30.0 + 15.0
        self.y = j * 30.0 + 15.0
        self.sx = 0
        if MoreHP.image == None:
            MoreHP.image = load_image("./Item/" + 'More_Hp' + ".png")

    def update(self):
        self.sx = self.x - server.background.window_left

    def draw(self):
        if -30 <= self.sx <= 1080 + 30:
            self.image.draw(self.sx, self.y + 10, 50, 50)
            if character.RectMode:
                draw_rectangle(*self.get_rect())

    def get_bb(self):
        return self.x - 30.0, self.y - 15, self.x + 30.0, self.y + 45.0

    def get_rect(self):
        return self.sx - 30.0, self.y - 15, self.sx + 30.0, self.y + 45.0

    def handle_collision(self, group, other):
        if group == 'server.character:morehp':
            other.take_more_hp()
            game_world.remove_object(self)