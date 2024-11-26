import server
import character
import game_framework
import game_world

from pico2d import draw_rectangle

class NormalSG3:

    def __init__(self, d):
        self.x = server.character.x
        self.y = server.character.y
        self.sx = 0
        self.framex = 0
        self.face = d

    def update(self):
        self.sx = self.x - server.background.window_left
        self.framex = self.framex + 9.0 * 1.5 * game_framework.frame_time
        if self.framex > 4.0:
            game_world.remove_object(self)

    def draw(self):
        if -15 <= self.sx <= 1095:
            if character.RectMode:
                draw_rectangle(*self.get_rect())

    def get_bb(self):
        if self.face == 1:
            return self.x + 121 + 17, self.y - 49.0, self.x + 180 + 17.0, self.y + 19.0
        elif self.face == -1:
            return self.x - 180.0 - 17.0, self.y - 49.0, self.x - 121 - 17, self.y + 19.0

    def get_rect(self):
        if self.face == 1:
            return self.sx + 121 + 17, self.y - 49.0, self.sx + 180 + 17.0, self.y + 19.0
        elif self.face == -1:
            return self.sx - 180.0 - 17.0, self.y - 49.0, self.sx - 121 - 17, self.y + 19.0

    def handle_collision(self, group, other):
        if group == 'normalsg3:spore':
            other.take_damage(1)