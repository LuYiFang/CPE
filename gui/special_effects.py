from random import randint
from engine.pygame_adapter import adapter


class HitSpark(adapter.collision_object()):
    def __init__(self, boss_pos, boss_size):
        super(HitSpark, self).__init__()

        self.surf, self.rect = adapter.load_image(
            './gui/static/hit_spark.png',
            center=(
                randint(boss_pos[0], boss_pos[0] + boss_size[0]),
                randint(boss_pos[1], boss_pos[1] + boss_size[0])
            )
        )
        adapter.resize(self.surf, (64, 64))

        self.flash_ms = 500

    def flash(self):
        pass