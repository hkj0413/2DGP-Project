import server
import game_framework
import game_world
import math
import random

from pico2d import load_image

class CskillHGEffect:
    image = None

    def __init__(self):
        self.x = server.character.x
        self.y = server.character.y
        self.sx = 0
        self.timer = 0
        self.temp = 0
        self.angle = random.uniform(0, 360)
        self.speed = 10
        self.dx = math.cos(math.radians(self.angle)) * self.speed
        self.dy = math.sin(math.radians(self.angle)) * self.speed
        if CskillHGEffect.image == None:
            CskillHGEffect.image = load_image("./Effect/HG/" + 'Lc_HG' + " (1)" + ".png")

    def update(self):
        self.sx = self.x - server.background.window_left

        self.timer += game_framework.frame_time

        if self.timer >= 0.01:
            self.timer = 0
            self.temp += 1
            self.x += self.dx
            self.y += self.dy
            if self.temp == 16:
                game_world.remove_object(self)

    def draw(self):
        if self.temp < 16:
            self.image.draw(self.sx, self.y - 10, 30, 27)