import game_world
import server
import character
import game_framework
import random

from pico2d import load_image, draw_rectangle, clamp, load_wav
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

animation_names = ['Idle', 'Walk', 'Hit', 'Die']

class Stonegolem:
    images = None
    Stonegolem_sound = None

    def load_images(self):
        if Stonegolem.images == None:
            Stonegolem.images = {}
            for name in animation_names:
                if name == 'Idle':
                    Stonegolem.images[name] = [load_image("./Boss/Stonegolem/"+ name + " (%d)" % i + ".png") for i in range(1, 3 + 1)]
                elif name == 'Walk':
                    Stonegolem.images[name] = [load_image("./Boss/Stonegolem/" + name + " (%d)" % i + ".png") for i in range(1, 4 + 1)]
                elif name == 'Hit':
                    Stonegolem.images[name] = [load_image("./Boss/Stonegolem/"+ name + " (1)" + ".png")]
                elif name == 'Die':
                    Stonegolem.images[name] = [load_image("./Boss/Stonegolem/" + name + " (%d)" % i + ".png") for i in range(1, 7 + 1)]

    def __init__(self, i=0.0, j=0):
        self.x = i * 30.0 + 15.0
        self.y = j * 30.0 + 15.0
        self.base_x = i * 30.0 + 15.0
        self.sx = 0
        self.face_dir = -1
        self.state = 0
        self.frame = 0
        self.name = ''
        self.prev_state = -1
        self.load_images()
        self.hp = 100
        self.stun = 0
        self.timer = 0
        self.temp = 0
        self.delay = False
        self.attck = 0
        self.skill = 0
        self.build_behavior_tree()
        if Stonegolem.Stonegolem_sound == None:
            Stonegolem.Stonegolem_sound = load_wav("./Sound/Hitsound.mp3")
            Stonegolem.Stonegolem_sound.set_volume(8)

    def update(self):
        self.sx = self.x - server.background.window_left
        self.x = clamp(self.base_x - 390.0, self.x, self.base_x + 390.0)

        self.timer += game_framework.frame_time

        if self.timer >= 0.5:
            self.timer = 0
            self.temp += 1
            self.delay = False
            if self.state == 3:
                if not self.stun == 0:
                    self.stun -= 1
                    self.temp = 0
                else:
                    self.state = 1
                    if server.character.x < self.x:
                        self.face_dir = -1
                    elif server.character.x > self.x:
                        self.face_dir = 1

            logic_map = {
                0: self.check_zero_logic,
                1: self.check_one_logic,
                2: self.check_two_logic,
            }

            if self.state in logic_map:
                logic_map[self.state]()

        if self.state != self.prev_state:
            self.bt.run()
            self.prev_state = self.state

        if self.state == 0:
            if self.name != 'Idle':
                self.name = 'Idle'
            self.frame = (self.frame + 3.0 * 1.0 * game_framework.frame_time) % 3
        elif self.state == 1:
            if self.name != 'Walk':
                self.name = 'Walk'
            self.frame = (self.frame + 4.0 * 1.5 * game_framework.frame_time) % 4
            self.walk()
        elif self.state == 2 or self.state == 3:
            if self.name != 'Hit':
                self.name = 'Hit'
            self.frame = 0
        elif self.state == 4:
            if self.name != 'Die':
                self.name = 'Die'
            self.frame = self.frame + 7.0 * 0.75 * game_framework.frame_time
            if self.frame > 7.0:
                game_world.remove_object(self)

    def draw(self):
        if -15 <= self.sx <= 1080 + 15:
            if not self.state == 5:
                if self.state == 2 or self.state == 3:
                    if self.face_dir == 1:
                        self.images[self.name][int(self.frame)].composite_draw(0, 'h', self.sx - 15, self.y + 25, 387,
                                                                               267)
                    elif self.face_dir == -1:
                        self.images[self.name][int(self.frame)].composite_draw(0, '', self.sx + 15, self.y + 25, 387,
                                                                               267)
                else:
                    if self.face_dir == 1:
                        self.images[self.name][int(self.frame)].composite_draw(0, 'h', self.sx - 60, self.y + 25, 387,
                                                                               267)
                    elif self.face_dir == -1:
                        self.images[self.name][int(self.frame)].composite_draw(0, '', self.sx + 60, self.y + 25, 387,
                                                                               267)
                if character.God:
                    draw_rectangle(*self.get_rect())

    def get_bb(self):
        return self.x - 105.0, self.y - 105.0, self.x + 105.0, self.y + 105.0

    def get_rect(self):
        return self.sx - 105.0, self.y - 105.0, self.sx + 105.0, self.y + 105.0

    def handle_collision(self, group, other):
        if group == 'server.character:stonegolem' and (self.state == 0 or self.state == 1):
            other.take_damage(3)
        elif group == 'normalrf:stonegolem' and (self.state == 0 or self.state == 1 or self.state == 3 or self.state == 6):
            self.take_damage(other.give_damage())
            other.get_count()
        elif group == 'normalrfsp:stonegolem' and (self.state == 0 or self.state == 1 or self.state == 3 or self.state == 6):
            self.take_damage(other.give_damage())
            other.get_count()
        elif group == 'normalhg:stonegolem' and (self.state == 0 or self.state == 1 or self.state == 3 or self.state == 6):
            self.take_damage(other.give_damage())
            other.get_count()

    def take_damage(self, damage):
        if (self.state == 0 or self.state == 1 or self.state == 3 or self.state == 6) and not self.delay:
            self.hp = max(0, self.hp - damage)
            Stonegolem.Stonegolem_sound.play()
            if self.hp <= 0:
                self.state = 4
                self.frame = 0
                self.stun = 0
            else:
                self.state = 2
            self.delay = True
            self.timer = 0

    def take_stun(self, stun):
        if self.state == 0 or self.state == 1 or self.state == 2:
            self.stun += stun
            self.state = 3

    def check_state(self, s):
        if self.state == s:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def walk(self):
        self.x += 0.75 * self.face_dir * character.RUN_SPEED_PPS * game_framework.frame_time
        if self.x <= self.base_x - 390.0 or self.x >= self.base_x + 390:
            self.face_dir *= -1

    def check_zero_logic(self):
        if self.temp == 4 or random.randint(1, 5) == 1:
            self.state = 1
            self.temp = 0

    def check_zero(self):
        if not self.state == 0:
            return BehaviorTree.FAIL
        return BehaviorTree.SUCCESS

    def check_one_logic(self):
        if random.randint(1, 5) == 1:
            self.state = 0
            self.temp = 0

    def check_one(self):
        if not self.state == 1:
            return BehaviorTree.FAIL
        return BehaviorTree.SUCCESS

    def check_two_logic(self):
        if self.stun == 0:
            self.state = 1
            if server.character.x < self.x:
                self.face_dir = -1
            elif server.character.x > self.x:
                self.face_dir = 1
        else:
            self.state = 3
        self.temp = 0

    def check_two(self):
        if not self.state == 2:
            return BehaviorTree.FAIL
        return BehaviorTree.SUCCESS

    def check_three(self):
        if not self.state == 3:
            return BehaviorTree.FAIL
        return BehaviorTree.SUCCESS

    def check_four(self):
        if not self.state == 4:
            return BehaviorTree.FAIL
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        action_map = {
            0: self.check_zero,
            1: self.check_one,
            2: self.check_two,
            3: self.check_three,
            4: self.check_four,
        }

        def run_state_actions():
            action = action_map.get(self.state, lambda: BehaviorTree.FAIL)
            return action()

        self.bt = BehaviorTree(Action('stonegolem_AI', run_state_actions))