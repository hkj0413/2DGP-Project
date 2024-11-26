import server
import character
import game_framework
import random

from pico2d import load_image, draw_rectangle, get_time, clamp
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

class Spore:
    image = None

    def __init__(self, i = 0, j = 0):
        self.x = i * 30.0 + 15.0
        self.y = j * 30.0 + 15.0
        self.base_x = i * 30.0 + 15.0
        self.sx = 0
        self.face_dir = random.randint(0, 1) * 2 - 1  # -1 or 1
        self.state = random.randint(0, 1)
        if self.state == 0:
            self.framex = random.randint(0, 1)
        elif self.state == 1:
            self.framex = random.randint(0, 3)
        self.prev_state = 0
        self.framey = self.state * 2 + 1 # 1 or 3
        self.hp = 2
        self.last_check_time = get_time()
        self.time_elapsed = 0
        self.build_behavior_tree()
        if Spore.image == None:
            Spore.image = load_image("./Mob/" + 'Spore' + ".png")

    def update(self):
        self.sx = self.x - server.background.window_left
        self.x = clamp(self.base_x - 90.0, self.x, self.base_x + 90.0)

        current_time = get_time()
        self.time_elapsed += current_time - self.last_check_time
        self.last_check_time = current_time

        if self.state != self.prev_state:
            self.bt.run()
            self.time_elapsed = 0
            self.prev_state = self.state

        elapsed_seconds = int(self.time_elapsed)
        self.time_elapsed -= elapsed_seconds

        logic_map = {
            0: self.check_zero_logic,
            1: self.check_one_logic,
            2: self.check_two_logic,
            4: self.check_four_logic,
            5: self.check_five_logic,
        }
        for _ in range(elapsed_seconds):
            if self.state in logic_map:
                logic_map[self.state]()

        if self.state == 0:
            self.framex = (self.framex + 2.0 * 1.5 * game_framework.frame_time) % 2
        elif self.state == 1:
            self.framex = (self.framex + 4.0 * 1.5 * game_framework.frame_time) % 4
            self.walk()
        elif self.state == 2 or self.state == 3:
            self.framex = 0
        elif self.state == 4:
            self.framex = self.framex + 4.0 * 1.2 * game_framework.frame_time

    def draw(self):
        if -15 <= self.sx <= 1095:
            if not self.state == 5:
                if self.face_dir == 1:
                    self.image.clip_composite_draw(int(self.framex) * 50, self.framey * 50, 50, 50, 0, 'h', self.sx,
                                                   self.y, 50, 50)
                elif self.face_dir == -1:
                    self.image.clip_composite_draw(int(self.framex) * 50, self.framey * 50, 50, 50, 0, '', self.sx,
                                                   self.y, 50, 50)
                if character.RectMode:
                    draw_rectangle(*self.get_rect())

    def get_bb(self):
        return self.x - 15.0, self.y - 15.0, self.x + 15.0, self.y + 15.0

    def get_rect(self):
        return self.sx - 15.0, self.y - 15.0, self.sx + 15.0, self.y + 15.0

    def handle_collision(self, group, other):
        if group == 'server.character:spore' and not self.state == 4 and not self.state == 5:
            other.take_damage(1)

    def take_damage(self, damage):
        if self.state == 0 or self.state == 1 or self.state == 3:
            self.hp = max(0, self.hp - damage)
            if self.hp <= 0:
                self.state = 4
                self.framey = 2
                character.Character.score += 1
            else:
                self.state = 2
                self.framey = 0

    def check_state(self, s):
        if self.state == s:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def walk(self):
        self.x += 1 * self.face_dir * character.RUN_SPEED_PPS * game_framework.frame_time
        if self.x <= self.base_x - 90.0 or self.x >= self.base_x + 90:
            self.face_dir *= -1

    def check_zero_logic(self):
        if self.time_elapsed >= 4 or random.randint(1, 5) == 1:  # 4초 이상 경과했거나 랜덤 조건
            self.state = 1
            self.framey = 3
            self.time_elapsed = 0  # 시간 리셋

    def check_zero(self):
        if not self.state == 0:
            return BehaviorTree.FAIL
        return BehaviorTree.SUCCESS

    def check_one_logic(self):
        if random.randint(1, 5) == 1:
            self.state = 0
            self.framey = 1

    def check_one(self):
        if not self.state == 1:
            return BehaviorTree.FAIL
        return BehaviorTree.SUCCESS

    def check_two_logic(self):
        self.state = 1
        self.framey = 3

    def check_two(self):
        if not self.state == 2:
            return BehaviorTree.FAIL
        return BehaviorTree.SUCCESS

    def check_four_logic(self):
        if self.time_elapsed >= 2:
            self.state = 5
            self.time_elapsed = 0

    def check_four(self):
        if not self.state == 4:
            return BehaviorTree.FAIL
        return BehaviorTree.SUCCESS

    def check_five_logic(self):
        if self.time_elapsed >= 5:
            self.state = 0
            self.time_elapsed = 0
            self.framey = 1
            self.hp = 2
            self.x = self.base_x
            self.face_dir = random.randint(0, 1) * 2 - 1

    def check_five(self):
        if not self.state == 5:
            return BehaviorTree.FAIL
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        action_map = {
            0: self.check_zero,
            1: self.check_one,
            2: self.check_two,
            4: self.check_four,
            5: self.check_five,
        }

        def run_state_actions():
            action = action_map.get(self.state, lambda: BehaviorTree.FAIL)
            return action()

        self.bt = BehaviorTree(Action('spore_AI', run_state_actions))