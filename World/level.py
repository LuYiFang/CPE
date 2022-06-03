from abc import ABC, abstractmethod
from characters.boss import Boss
from characters.player import Player
from engine.pygame_adapter import adapter


class LevelAbstract(ABC):
    @abstractmethod
    def boss_move(self, *args, **kwargs):
        pass

    @abstractmethod
    def player_move(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def is_end(self):
        pass


class LevelBase(LevelAbstract):
    def __init__(self):
        self.boss = Boss(attack_speed=1, recover_speed=1)
        self.player = Player()

    def boss_move(self, *args, **kwargs):
        pass

    def player_move(self, *arg, **kwargs):
        pass

    def reset(self):
        self.player.reset()
        self.boss.reset()

    def is_end(self):
        return self.player.is_dead() or self.boss.is_dead()

    def end_game(self):
        print('end game')

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
    def __init__(self):
        super().__init__()
        self.player = Player(attack_power=10)

    def boss_move(self, event, target):
        pass

    def player_move(self, event, target):
        self.player.attack(event, target)

    def reset(self):
        pass


class Level2(LevelBase):
    def __init__(self):
        super().__init__()
        self.boss = Boss(attack_power=5, recover_speed=1, attack_speed=1)

    def boss_move(self, event, target):
        self.boss.attack(event, target)

    def player_move(self, event, target):
        self.player.attack(event, target)

    def reset(self):
        pass