import random
from abc import ABC, abstractmethod
from characters.boss import Boss
from characters.player import Player
from engine.pygame_adapter import adapter, k
from gui.special_effects import HintText
import gui.images as img


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

        self.attack_keys = list('yhnujmikolp')
        self.recover_keys = list('qazwsxedcrfvtgb')
        self.attack_text_queue = []
        self.recover_text_queue = []
        self.right_title, self.left_title, self.right_text, self.left_text = self.count_hint_position()

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

    def player_move(self, event, target, attack_key=k.K_RETURN):
        spark = self.player.attack(event, target, attack_key)
        if spark is not None:
            self.spark_sprites.add(spark)
            self.exclude_boss_sprites.add(spark)

    def count_hint_position(self):
        screen_w, screen_h = adapter.get_screen_x_y()

        title_width = 160
        title_height = title_width / 2
        padding = 15
        title_y = screen_h / 15 * 11 + padding

        right_x = screen_w - padding - title_width

        right_title = (right_x, title_y, title_width, title_height)
        left_title = (padding, title_y, title_width, title_height)

        y = screen_h / 15 * 13 + 5
        x = right_x + 35
        right_text = (x, y)

        x = padding + 35
        left_text = (x, y)
        return right_title, left_title, right_text, left_text

    def hint_title(self):
        attack = HintText(img.ATTACK_HINT, *self.right_title)
        self.exclude_boss_sprites.add(attack)

        recover = HintText(img.RECOVER_HINT, *self.left_title)
        self.exclude_boss_sprites.add(recover)

    def hint(self):
        self.hint_title()

    def get_random_key(self, key_list):
        return key_list[random.randint(0, len(key_list) - 1)]

    def init_queue(self, key_list: list):
        queue = []
        for _ in range(4):
            key = self.get_random_key(key_list)
            text = adapter.create_text(key.upper())
            queue.append((key, text))
        return queue

    def update_queue(self, queue: list, key_list: list):
        target_key = self.get_random_key(key_list)
        text = adapter.create_text(target_key.upper())
        queue.pop(0)
        queue.append((target_key, text))
        return target_key

    def reset(self):
        self.player.reset()
        self.boss.reset()

    def is_end(self):
        return self.player.is_dead() or self.boss.is_dead()

    def end_event(self):
        screen_size = adapter.get_screen_x_y()
        img_url = img.YOU_DIE

        if self.boss.is_dead():
            img_url = img.YOU_WIN
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

    def hint(self):
        super().hint()
        text = adapter.create_text('Enter')
        adapter.bind_screen(text, self.right_text)


class Level2(Level1):
    def boss_move(self, event, target):
        self.boss.attack(event, target)

    def player_move(self, event, target, **kwargs):
        super(Level2, self).player_move(event, target, **kwargs)
        self.player.recover(event)

    def hint(self):
        super().hint()
        text = adapter.create_text('C')
        adapter.bind_screen(text, self.left_text)


class Level3(Level2):
    def boss_move(self, event, target):
        super(Level3, self).boss_move(event, target)
        shining = self.boss.recover(event)
        if shining is not None:
            self.spark_sprites.add(shining)
            self.exclude_boss_sprites.add(shining)


class Level4(Level3):
    def __init__(self, difficulty):
        super().__init__(difficulty)
        self.attack_text_queue = self.init_queue(self.attack_keys)

    def hint(self):
        self.hint_title()

        text = adapter.create_text('C')
        adapter.bind_screen(text, self.left_text)

        right_text = [*self.right_text]
        for _, text in self.attack_text_queue:
            adapter.bind_screen(text, right_text)
            right_text[0] += 30

    def player_move(self, event, target, **kwargs):
        attack_key = self.attack_text_queue[0][0]

        spark = self.player.attack(event, target, getattr(k, f'K_{attack_key}'))
        if spark is not None:
            self.spark_sprites.add(spark)
            self.exclude_boss_sprites.add(spark)
            self.update_queue(self.attack_text_queue, self.attack_keys)

        self.player.recover(event)


class Level5(Level4):
    def __init__(self, difficulty):
        super().__init__(difficulty)
        self.attack_text_queue = self.init_queue(self.attack_keys)
        self.recover_text_queue = self.init_queue(self.recover_keys)

    def hint(self):
        self.hint_title()

        left_text = [*self.left_text]
        for _, text in self.recover_text_queue:
            adapter.bind_screen(text, left_text)
            left_text[0] += 30

        right_text = [*self.right_text]
        for _, text in self.attack_text_queue:
            adapter.bind_screen(text, right_text)
            right_text[0] += 30

    def player_move(self, event, target, **kwargs):
        attack_key = self.attack_text_queue[0][0]
        spark = self.player.attack(event, target, getattr(k, f'K_{attack_key}'))
        if spark is not None:
            self.spark_sprites.add(spark)
            self.exclude_boss_sprites.add(spark)
            self.update_queue(self.attack_text_queue, self.attack_keys)

        recover_key = self.recover_text_queue[0][0]
        recover = self.player.recover(event, getattr(k, f'K_{recover_key}'))
        if recover is not None:
            self.update_queue(self.recover_text_queue, self.recover_keys)
