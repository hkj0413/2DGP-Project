import server
import character
import game_framework
import random

from pico2d import load_image, draw_rectangle, get_time
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

class Spore:
    image = None

    def __init__(self, i = 0, j = 0):
        self.x = i * 30.0 + 15.0
        self.y = j * 30.0 + 15.0
        self.base_x = i * 30.0 + 15.0
        self.sx = 0
        self.framex = 0
        self.framey = 3
        self.face_dir = random.randint(0, 1) * 2 - 1 # -1 or 1
        self.hp = 2
        if Spore.image == None:
            Spore.image = load_image("./Mob/" + 'Spore' + ".png")

    def update(self):
        # self.bt.run()
        self.sx = self.x - server.background.window_left

    def draw(self):
        if -15 <= self.sx <= 1095:
            if self.face_dir == 1:
                self.image.clip_composite_draw(self.framex * 50, self.framey * 50, 50, 50, 0, '', self.sx, self.y, 50,
                                               50)
            elif self.face_dir == -1:
                self.image.clip_composite_draw(self.framex * 50, self.framey * 50, 50, 50, 0, 'h', self.sx, self.y, 50,
                                               50)
            if character.RectMode:
                draw_rectangle(*self.get_rect())

    def get_bb(self):
        return self.x - 15.0, self.y - 15.0, self.x + 15.0, self.y + 15.0

    def get_rect(self):
        return self.sx - 15.0, self.y - 15.0, self.sx + 15.0, self.y + 15.0

    def handle_collision(self, group, other):
        if group == 'server.character:spore':
            other.take_damage(1)

    def move_1st(self):
        pass

    def move_2nd(self):
        pass

    def move_3rd(self):
        pass

    def build_behavior_tree(self):
        # a1 = Action('move')

        root = None
        self.bt = BehaviorTree(root)
        pass