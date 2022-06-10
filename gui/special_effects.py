from random import randint
from time import time
from engine.pygame_adapter import adapter


class HitSpark(adapter.collision_object()):
    def __init__(self, boss_pos, boss_size):
        super(HitSpark, self).__init__()

        pos_x = randint(boss_pos[0], boss_pos[0] + boss_size[0])
        pos_y = randint(boss_pos[1], boss_pos[1] + boss_size[1])
        size = 64

        self.surf, self.rect = adapter.load_image(
            'src/static/hit_spark.png',
            topleft=(
                pos_x,
                pos_y
            ),
        )
        self.surf = adapter.resize(self.surf, (size, size))
        self.flash_ms = 200 / 1000
        self.timer = time()

    def update(self):
        if time() - self.timer >= self.flash_ms:
            self.kill()


class CountNumber(adapter.collision_object()):
    def __init__(self, img_url):
        super(CountNumber, self).__init__()
        size = 256
        screen_w, screen_h = adapter.get_screen_x_y()
        middle_x = screen_w / 2 - size / 2
        middle_y = screen_h / 2 - size / 2

        if img_url is None:
            self.surf, self.rect = adapter.create_surface((0, 0))
        else:
            self.surf, self.rect = adapter.load_image(
                img_url,
                topleft=(middle_x, middle_y)
            )
            self.surf = adapter.resize(self.surf, (size, size))

    def kill(self):
        self.kill()
