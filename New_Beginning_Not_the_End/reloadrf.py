import server
import character
import game_framework
import game_world

from pico2d import load_image, draw_rectangle


class ReloadRF:
    image = None

    def __init__(self, d):
        self.x = server.character.x
        self.y = server.character.y
        self.sx = 0
        self.timer = 0
        self.temp = 0
        self.face = d
        if ReloadRF.image == None:
            ReloadRF.image = load_image("./Effect/RF/" + 'R_RF' + " (1)" + ".png")

    def update(self):
        self.sx = self.x - server.background.window_left

        self.timer += game_framework.frame_time

        if self.timer >= 0.01:
            self.timer = 0
            self.temp += 1
            self.x += 12 * self.face
            if self.temp == 20:
                game_world.remove_object(self)

    def draw(self):
        if self.temp < 20:
            if self.face == 1:
                self.image.composite_draw(0, 'h', self.sx + 80, self.y - 10, 33, 52)
            elif self.face == -1:
                self.image.composite_draw(0, '', self.sx - 80, self.y - 10, 33, 52)
            if character.RectMode:
                draw_rectangle(*self.get_rect())

    def get_count(self):
        self.count += 1
        return

    def get_bb(self):
        if self.face == 1:
            return self.x + 60.0, self.y - 30.0, self.x + 92.0, self.y + 10.0
        elif self.face == -1:
            return self.x - 92.0, self.y - 30.0, self.x - 60.0, self.y + 10.0

    def get_rect(self):
        if self.face == 1:
            return self.sx + 60.0, self.y - 30.0, self.sx + 92.0, self.y + 10.0
        elif self.face == -1:
            return self.sx - 92.0, self.y - 30.0, self.sx - 60.0, self.y + 10.0

    def handle_collision(self, group, other):
        if group == 'reloadrf:spore':
            other.take_stun(2)