import server

from pico2d import load_image, get_canvas_width, clamp

class Background:
    def __init__(self):
        self.image = load_image('1stage.png')
        self.cw = get_canvas_width()
        self.w = self.image.w
        self.window_left = 0

    def update(self):
        self.window_left = clamp(0, int(server.character.x) - self.cw // 2, self.w - self.cw - 1)

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, 0, self.cw, 800, 0, 0)

    def handle_event(self, event):
        pass