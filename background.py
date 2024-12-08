import server

from pico2d import load_image, get_canvas_width, clamp, load_music

class Background:
    image = None
    sound = None
    current_sound = None

    def __init__(self, k):
        self.frame = k
        self.cw = get_canvas_width() # 가로 3240 pixel == 108m 화면은 1080 pixel 만 출력,
        self.window_left = 0         # 세로 1200 pixel == 40m 이지만 800 pixel 만 사용 하고 출력
        if Background.image == None:
            Background.image = [load_image("./Background/" + 'Background' + " (%d)" % i + ".png") for i in range(1, 4 + 1)]
        self.w = self.image[k].w
        if Background.sound == None:
            Background.sound = [load_music("./Bgm/" + 'BGM' + " (%d)" % i + ".mp3") for i in range(1, 3 + 1)]
            for sound in Background.sound:
                sound.set_volume(12)
        self.play_sound()

    def update(self):
        self.window_left = clamp(0, int(server.character.x) - self.cw // 2, self.w - self.cw - 1)

    def draw(self):
        self.image[self.frame].clip_draw_to_origin(self.window_left, 0, self.cw, 800, 0, 0)

    def handle_event(self, event):
        pass

    def play_sound(self):
        if self.frame == 0:
            if Background.current_sound != Background.sound[0]:
                if Background.current_sound:
                    Background.current_sound.stop()
                Background.current_sound = Background.sound[0]
                Background.current_sound.repeat_play()

        elif self.frame == 1:
            if Background.current_sound != Background.sound[1]:
                if Background.current_sound:
                    Background.current_sound.stop()
                Background.current_sound = Background.sound[1]
                Background.current_sound.repeat_play()

        elif self.frame == 2 or self.frame == 3:
            if Background.current_sound != Background.sound[2]:
                if Background.current_sound:
                    Background.current_sound.stop()
                Background.current_sound = Background.sound[2]
                Background.current_sound.repeat_play()