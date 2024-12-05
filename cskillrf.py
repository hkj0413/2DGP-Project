import server
import game_framework
import game_world

from pico2d import load_image, load_wav, get_time

class CskillRF:
    image = None
    C_RF_1_sound = None
    def __init__(self):
        self.x = server.character.x
        self.y = server.character.y
        self.sx = 0
        self.frame = 0
        self.one = 0
        self.time = get_time()
        if CskillRF.image == None:
            CskillRF.image = [load_image("./Effect/RF/" + 'C_RF' + " (%d)" % i + ".png") for i in range(1, 6 + 1)]
        if CskillRF.C_RF_1_sound == None:
            CskillRF.C_RF_1_sound = load_wav("./Sound/C_RF_1.mp3")
            CskillRF.C_RF_1_sound.set_volume(64)


    def update(self):
        self.x = server.character.x
        self.y = server.character.y
        self.sx = self.x - server.background.window_left

        if get_time() - self.time > 10.0:
            game_world.remove_object(self)

        if self.one == 0 and get_time() - self.time > 2.0:
            CskillRF.C_RF_1_sound.play()
            self.one += 1

        self.frame = (self.frame + 6.0 * 2.0 * game_framework.frame_time) % 6

    def draw(self):
        self.image[int(self.frame)].draw(self.sx, self.y - 15, 135, 127)