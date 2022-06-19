from abc import ABC, abstractmethod

from engine.pygame_adapter import adapter
import gui.color as theme


class CharacterAbstract(ABC):

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def attack(self, *arg, **kwargs):
        pass

    @abstractmethod
    def die(self):
        pass

    @abstractmethod
    def recover(self):
        pass


class Character(CharacterAbstract, adapter.collision_object()):
    def __init__(self, hp, attack_power=1, heal_rate=1, **kwargs):
        super().__init__()
        self.attack_power = attack_power
        self.heal_rate = heal_rate
        self.full_hp = hp
        self.hp = hp

        self.hp_color = theme.ACCENT1
        self.hp_back_color = theme.BACKGROUND
        self.hp_border_color = theme.ACCENT1_DARK
        self.hp_rect_tmp = self.set_hp_bar_tmp()

    def set_hp_bar_tmp(self, pos=(100, 10), size=(300, 20)):
        return adapter.create_rect(*pos, *size)

    def update_hp_tmp(self):
        adapter.draw_health_bar(
            self.hp_rect_tmp.topleft,
            self.hp_rect_tmp.size,
            self.hp_border_color, self.hp_back_color, self.hp_color,
            self.hp / self.full_hp
        )

    def reset(self):
        self.hp = self.full_hp

    def attack(self, *args, **kwargs):
        pass

    def die(self):
        pass

    def recover(self, *args, **kwargs):
        pass

    def is_dead(self):
        return self.hp <= 0

    def update(self):
        # self.update_hp_bar()
        self.update_hp_tmp()

