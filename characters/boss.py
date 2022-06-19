from time import time
from characters.base import Character
from engine.pygame_adapter import (
    adapter,
)
from gui.special_effects import HitSpark, RecoverShining
import gui.color as theme


class Boss(Character):
    def __init__(self, attack_speed, recover_speed, attack_power=1, heal_rate=1, hp=100):
        super().__init__(hp=hp, attack_power=attack_power, heal_rate=heal_rate)
        self.attack_speed = attack_speed
        self.recover_speed = recover_speed

        screen_size = adapter.get_screen_size()
        width = 300
        middle_x = screen_size.current_w / 2 - width / 2

        self.surf, self.rect = adapter.load_image(
            'src/static/boss_normal.png',
            center=(
                screen_size.current_w / 2,
                screen_size.current_h / 2
            ),
        )

        self.surf_hurt, self.rect_hurt = adapter.load_image(
            'src/static/boss_hit.png',
            center=(
                screen_size.current_w / 2,
                screen_size.current_h / 2
            ),
        )

        self.attack_event_id = adapter.create_time_event(
            self.speed_to_ms(self.attack_speed)
        )
        self.recover_event_id = adapter.create_time_event(
            self.speed_to_ms(self.recover_speed)
        )

        self.hp_color = theme.ACCENT2
        self.hp_border_color = theme.ACCENT2_DARK

        self.hp_rect_tmp = self.set_hp_bar_tmp((middle_x, 10), (width, 20))
        self.update_hp_tmp()

        self.is_hit = False
        self.timer = time()

        self.blink_rate = 200 / 1000

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
        if time() - self.timer >= self.blink_rate:
            self.is_hit = False

    def recover_special_effect(self):
        shining = RecoverShining(self.rect.topleft, self.rect.size)
        return shining

    def update(self):
        super().update()
        if not self.is_hit:
            adapter.bind_screen(self.surf, self.rect)
        else:
            self.blink()

    def die(self):
        print('You win')

    def recover(self, event):
        if event.type == self.recover_event_id:
            self.hp += self.heal_rate
            if self.hp > self.full_hp:
                self.hp = self.full_hp
            return self.recover_special_effect()

