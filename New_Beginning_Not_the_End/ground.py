from pico2d import load_image

class Ground:
    image = None

    def __init__(self, i=0, j=0, k=0):
        self.x = 0
        self.base_x = i * 30 + 15
        self.y = j * 30 + 15
        self.framex = k
        if Ground.image == None:
            Ground.image = load_image('Block.png')

    def update(self):
        self.x = self.base_x

    def draw(self):
        self.image.clip_draw(self.framex * 120, 0, 120, 120, self.x, self.y, 30, 30)

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15

    def collide_left(self):
        return self.x - 33

    def collide_right(self):
        return self.x + 33

    def handle_collision(self, group, other):
        pass