from pico2d import load_image

class Ground:
    image = None

    def __init__(self, i=0, j=0.0, k=0):
        self.x = 0
        self.base_x = i * 30 + 15
        self.y = j * 30.0 + 15.0
        self.framex = k
        if Ground.image == None:
            Ground.image = load_image('Block.png')

    def update(self):
        self.x = self.base_x

    def draw(self):
        self.image.clip_draw(self.framex * 120, 0, 120, 120, self.x, self.y, 30, 30)

    def get_bb(self):
        return self.x - 15, self.y - 15.0, self.x + 15, self.y + 15.0

    def collide_jump(self):
        return self.y - 35

    def collide_fall(self):
        return self.y + 65

    def handle_collision(self, group, other):
        pass

    def handle_collision_fall(self, group, other):
        pass

    def handle_collision_jump(self, group, other):
        pass