import server
import character
import game_framework
import game_world

from pico2d import load_image

class RcskillRFEffect:
    image = None

    def __init__(self):
        self.x = character.mouse_x
        self.y = 800 - character.mouse_y
        self.sx = 0
        self.frame = 0
        if RcskillRFEffect.image == None:
            RcskillRFEffect.image = [load_image("./Effect/RF/" + 'Rc_RF' + " (%d)" % i + ".png") for i in range(1, 8 + 1)]

    def update(self):
        self.sx = self.x - server.background.window_left
        self.frame = self.frame + 8.0 * 1.5 * game_framework.frame_time
        if self.frame > 8.0:
            game_world.remove_object(self)

    def draw(self):
        if self.frame < 8.0:
            self.image[int(self.frame)].draw(self.sx + 10, self.y, 239, 141)