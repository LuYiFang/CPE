from characters.base import Character
from engine.pygame_adapter import (
    adapter,
    k,
)


class Player(Character):
    def __init__(self, attack_power=1, heal_rate=1, hp=50):
        super().__init__(hp=hp, attack_power=attack_power, heal_rate=heal_rate)
        self.surf, self.rect = adapter.create_surface((0, 0))
        adapter.resize(self.surf, (128, 128))
        self.rect.topleft = (150, 50)

        screen_size = adapter.get_screen_size()
        width, height = 300, 20
        hp_x = screen_size.current_w / 2 - width / 2
        hp_y = screen_size.current_h / 15 * 14

        self.hp_rect_tmp = self.set_hp_bar_tmp((hp_x, hp_y), (width, height))
        self.update_hp_tmp()

    def attack(self, event, target, attack_key=k.K_RETURN):
        if event.type != k.KEYUP:
            return None
        if event.key == attack_key:
            target.hp -= self.attack_power
            spark = target.be_hit()
            return spark

    def die(self):
        print('You die')

    def recover(self, event, recover_key=k.K_c):
        if event.type != k.KEYUP:
            return None
        if event.key == recover_key:
            self.hp += self.heal_rate
            if self.hp > self.full_hp:
                self.hp = self.full_hp
            return True
