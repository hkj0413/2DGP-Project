from pico2d import load_image, load_font

from character import Character

class Mainguide:
    image = None

    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 20)
        if Mainguide.image == None:
            Mainguide.image = load_image("./Background/" + 'Main_guide' + ".png")

    def update(self):
        pass

    def draw(self):
        left = 60
        right = 1020
        bottom = 200
        top = 740

        center_x = (left + right) // 2
        center_y = (bottom + top) // 2
        width = right - left
        height = top - bottom

        self.image.draw(center_x, center_y, width, height)

        self.font.draw(480.0, 720.0, f'Score : {Character.score}', (0, 0, 0))