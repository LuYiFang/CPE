from abc import ABC, abstractmethod

from engine.pygame_adapter import adapter


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

        self.hp_color = (32, 230, 91, 90)
        self.hp_back_color = (255, 255, 255)
        self.hp_border_color = (17, 125, 50, 49)
        # self.hp_rect, self.inner_pos = self.set_hp_bar()

        self.hp_rect_tmp = self.set_hp_bar_tmp()

    # def set_hp_bar(self, pos=(100, 10), size=(300, 20)):
        # TODO: something below should not static?
    #     hp_rect = adapter.create_rect(*pos, *size)
    #     inner_pos = (hp_rect.topleft[0] + 1, hp_rect.topleft[1] + 1)
    #     adapter.draw(self.hp_back_color, *hp_rect.topleft, *hp_rect.size)
    #     adapter.draw(self.hp_border_color, *hp_rect.topleft, *hp_rect.size, 1)
    #     return hp_rect, inner_pos
    #
    # def update_hp_bar(self):
    #     progress = self.hp / self.full_hp
    #     width = (self.hp_rect.size[0] - 2) * progress
    #     height = self.hp_rect.size[1] - 2
    #     inner_size = (width, height)
    #     adapter.draw_hp_bar(
    #         self.inner_pos,
    #         inner_size,
    #         self.hp_color,
    #     )

    def set_hp_bar_tmp(self, pos=(100, 10), size=(300, 20)):
        return adapter.create_rect(*pos, *size)

    def update_hp_tmp(self):
        # self.hp_rect_tmp.midbottom = self.rect.centerx, self.rect.top
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

