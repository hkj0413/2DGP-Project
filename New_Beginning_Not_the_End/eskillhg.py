import server
import character
import game_framework
import game_world
import random

from pico2d import load_image ,draw_rectangle

class EskillHG:
    image = None

    def __init__(self, d):
        self.x = server.character.x + 18 * d
        self.y = server.character.y + random.randint(-5 , 5)
        self.sx = 0
        self.damage = server.character.damage_HG
        self.timer = 0
        self.temp = 0
        self.face = d
        if EskillHG.image == None:
            EskillHG.image = load_image("./Effect/HG/" + 'Lc_HG' + " (1)" + ".png")

    def update(self):
        self.sx = self.x - server.background.window_left

        self.timer += game_framework.frame_time

        if self.timer >= 0.01:
            self.timer = 0
            self.temp += 1
            self.x += 10 * self.face
            if self.temp == 36:
                game_world.remove_object(self)

    def draw(self):
        if self.temp < 36:
            if self.face == 1:
                self.image.composite_draw(0, '', self.sx + 15, self.y - 10, 30, 27)
            elif self.face == -1:
                self.image.composite_draw(0, 'h', self.sx - 15, self.y - 10, 30, 27)
            if character.God:
                draw_rectangle(*self.get_rect())

    def get_bb(self):
        if self.face == 1:
            return self.x, self.y - 30.0, self.x + 30.0, self.y + 10.0
        elif self.face == -1:
            return self.x - 30.0, self.y - 30.0, self.x, self.y + 10.0

    def get_rect(self):
        if self.face == 1:
            return self.sx, self.y - 30.0, self.sx + 30.0, self.y + 10.0
        elif self.face == -1:
            return self.sx - 30.0, self.y - 30.0, self.sx, self.y + 10.0

    def handle_collision(self, group, other):
        mob_group = ['spore', 'slime', 'pig']
        for mob in mob_group:
            if group == f'eskillhg:{mob}':
                other.take_damage(self.damage)
