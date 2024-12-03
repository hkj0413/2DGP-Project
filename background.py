import server

from pico2d import load_image, get_canvas_width, clamp

class Background:
    image = None

    def __init__(self, k):
        self.frame = k
        self.cw = get_canvas_width() # 가로 3240 pixel == 108m 화면은 1080 pixel 만 출력,
        self.window_left = 0         # 세로 1200 pixel == 40m 이지만 800 pixel 만 사용 하고 출력
        if Background.image == None:
            Background.image = [load_image("./Background/" + 'Background' + " (%d)" % i + ".png") for i in range(1, 2 + 1)]
        self.w = self.image[k].w

    def update(self):
        self.window_left = clamp(0, int(server.character.x) - self.cw // 2, self.w - self.cw - 1)

    def draw(self):
        self.image[self.frame].clip_draw_to_origin(self.window_left, 0, self.cw, 800, 0, 0)

    def handle_event(self, event):
        pass