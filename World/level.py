from abc import ABC, abstractmethod
from characters.boss import Boss
from characters.player import Player
from engine.pygame_adapter import adapter, KEYUP, K_RETURN

import inspect


class LevelAbstract(ABC):
    @abstractmethod
    def boss_move(self, *args, **kwargs):
        pass

    @abstractmethod
    def player_move(self, *args, **kwargs):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def is_end(self):
        pass


class LevelBase(LevelAbstract):
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.default_rate = 5
        self.default_hp = 100
        self.level = int(self.__class__.__name__[5:])

        self.boss = Boss(
            attack_speed=self.count_attack_speed(),
            recover_speed=self.count_recover_speed(),
            attack_power=self.count_attack_power(),
            heal_rate=self.count_recover_power(),
            hp=self.count_hp(),
        )

        self.player = Player(
            attack_power=2,
            heal_rate=1,
            hp=50,
        )
        self.spark_sprites = adapter.create_group()
        self.exclude_boss_sprites = adapter.create_group()
        self.exclude_boss_sprites.add(self.player)

    def count_hp(self):
        return self.default_hp + self.level * 0.5

    def count_attack_speed(self):
        return pow(self.difficulty, 1.5)

    def count_recover_speed(self):
        return pow(self.difficulty, 1.5)

    def count_attack_power(self):
        difficulty_power = self.default_rate * self.difficulty * 0.5
        level_addition = self.level * 0.5
        return self.default_rate + difficulty_power + level_addition

    def count_recover_power(self):
        difficulty_power = self.default_rate * self.difficulty * 0.5
        level_addition = self.level * 0.5
        return self.default_rate + difficulty_power + level_addition

    def boss_move(self, *args, **kwargs):
        pass

    def player_move(self, event, target):
        spark = self.player.attack(event, target)
        if spark is not None:
            self.spark_sprites.add(spark)
            self.exclude_boss_sprites.add(spark)

    def reset(self):
        self.player.reset()
        self.boss.reset()

    def is_end(self):
        return self.player.is_dead() or self.boss.is_dead()

    def end_event(self):
        screen_size = adapter.get_screen_x_y()
        img_url = 'src/static/you_die.png'

        if self.boss.is_dead():
            img_url = 'src/static/you_win.png'
        end_background, _ = adapter.load_image(img_url)
        end_background = adapter.resize(end_background, screen_size)
        return end_background

    def update(self):
        self.player.update()
        self.boss.update()

    @staticmethod
    def match_time(t, speed):
        time_interval = 10 - speed
        if 10 >= time_interval or time_interval <= 0:
            return False
        return t % time_interval == 0


class Level1(LevelBase):
    def __init__(self, difficulty):
        super().__init__(difficulty)


class Level2(LevelBase):
    def __init__(self, difficulty):
        super().__init__(difficulty)

    def boss_move(self, event, target):
        self.boss.attack(event, target)

    def player_move(self, event, target):
        super(Level2, self).player_move(event, target)
        self.player.recover(event)


class Level3(Level2):
    def boss_move(self, event, target):
        super(Level3, self).boss_move(event, target)
        self.boss.recover(event)
