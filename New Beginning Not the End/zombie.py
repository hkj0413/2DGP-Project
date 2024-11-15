import random
import game_framework
import game_world

from pico2d import *

PIXEL_PER_METER = (30.0 / 1)    # 30 pixel 1 m
RUN_SPEED_KMPH = 10.0           # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

animation_names = ['Walk', 'Attack']

class Zombie:
    images = None

    def load_images(self):
        if Zombie.images == None:
            Zombie.images = {}
            for name in animation_names:
                if name == 'Walk':
                    Zombie.images[name] = [load_image("./zombie/"+ name + " (%d)" % i + ".png") for i in range(1, 10 + 1)]
                elif name == 'Attack':
                    Zombie.images[name] = [load_image("./zombie/" + name + " (%d)" % i + ".png") for i in range(1, 8 + 1)]

    def __init__(self):
        self.x, self.y = random.randint(600, 1000), 150
        self.load_images()
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1,1])
        self.hp = 2


    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x > 1000:
            self.dir = -1
        elif self.x < 600:
            self.dir = 1
        self.x = clamp(600, self.x, 1000)
        pass


    def draw(self):
        if self.dir < 0:
            if self.hp == 2:
                Zombie.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 200, 200)
            elif self.hp == 1:
                Zombie.images['Attack'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
        else:
            if self.hp == 2:
                Zombie.images['Walk'][int(self.frame)].draw(self.x, self.y, 200, 200)
            elif self.hp == 1:
                Zombie.images['Attack'][int(self.frame)].draw(self.x, self.y, 100, 100)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def get_bb(self):
        return self.x - self.hp * 35, self.y - self.hp * 50, self.x + self.hp * 35, self.y + self.hp * 50

    def handle_collision(self, group, other):
        global FRAMES_PER_ACTION
        if group == 'zombie:ball':
            self.hp -= 1
            self.y -= 50
            self.frame = 0
            FRAMES_PER_ACTION = 8.0
            if self.hp <= 0:
                game_world.remove_object(self)


