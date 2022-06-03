from time import time
from characters.base import Character
from engine.pygame_adapter import (
    adapter,
)
from gui.special_effects import HitSpark


class Boss(Character):
    def __init__(self, attack_speed, recover_speed, attack_power=1, heal_rate=1):
        super().__init__(hp=100, attack_power=attack_power, heal_rate=heal_rate)
        self.attack_speed = attack_speed
        self.recover_speed = recover_speed

        screen_size = adapter.get_screen_size()
        width = 300
        middle_x = screen_size.current_w / 2 - width / 2

        self.surf, self.rect = adapter.load_image(
            '../gui/static/boss_normal.png',
            center=(
                screen_size.current_w / 2,
                screen_size.current_h / 2
            ),
        )

        self.surf_hurt, self.rect_hurt = adapter.load_image(
            '../gui/static/boss_hit.png',
            center=(
                screen_size.current_w / 2,
                screen_size.current_h / 2
            ),
        )

        self.attack_event_id = adapter.create_time_event(
            self.speed_to_ms(self.attack_speed)
        )

        self.hp_color = (250, 140, 22, 98)
        self.hp_border_color = (227, 88, 9, 89)
        # self.hp_rect, self.inner_pos = self.set_hp_bar()
        # self.update_hp_bar()

        self.hp_rect_tmp = self.set_hp_bar_tmp((middle_x, 10), (width, 20))
        self.update_hp_tmp()

        self.is_hit = False
        self.timer = time()

    def speed_to_ms(self, speed):
        return round(1000 / speed)

    def attack(self, event, target):
        if event.type == self.attack_event_id:
            target.hp -= self.attack_power

    def be_hit(self):
        spark = HitSpark(self.rect.topleft, self.rect.size)
        self.is_hit = True
        self.timer = time()
        return spark

    def blink(self):
        adapter.bind_screen(self.surf_hurt, self.rect_hurt)
        if time() - self.timer >= 500 / 1000:
            self.is_hit = False

    def update(self):
        super().update()
        if not self.is_hit:
            adapter.bind_screen(self.surf, self.rect)
        else:
            self.blink()

    def die(self):
        print('You win')

    def recover(self):
        pass
