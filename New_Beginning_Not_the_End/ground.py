import server

from pico2d import load_image

class Ground:
    image = None

    def __init__(self, i=0, j=0.0, k=0):
        self.x = i * 30.0 + 15.0
        self.y = j * 30.0 + 15.0
        self.framex = k
        self.sx = 0
        if Ground.image == None:
            Ground.image = load_image('Block.png')

    def update(self):
        self.sx = self.x - server.background.window_left

    def draw(self):
        if -15 <= self.sx <= 1095:
            self.image.clip_draw(self.framex * 120, 0, 120, 120, self.sx, self.y, 30, 30)

    def get_bb(self):
        return self.sx - 15.0, self.y - 15.0, self.sx + 15.0, self.y + 15.0

    def collide_jump(self):
        return self.y - 35.0

    def collide_fall(self):
        return self.y + 65.0

    def handle_collision(self, group, other):
        pass

    def handle_collision_fall(self, group, other):
        pass

    def handle_collision_jump(self, group, other):
        pass