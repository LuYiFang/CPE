from World.level import (
    LevelBase,
    Level1,
    Level2,
    Level3,
)

from engine.pygame_adapter import adapter, KEYUP
from gui.menu import Menu
from gui.special_effects import CountNumber


class World:
    def __init__(self):
        self.current_difficulty = 1
        self.max_difficulty = 10
        self.levels = [Level1, Level2, Level3]
        self.max_level = len(self.levels)
        self.current_level = Level1

        adapter.init()
        adapter.set_screen()
        screen_size = adapter.get_screen_size()
        self.menu = Menu(
            screen_size.current_w, screen_size.current_h,
            self.new_game, self.change_level, self.change_difficulty, self.exit
        )
        self.countdown_event = None
        self.countdown_surf = None

    def new_game(self, *args, **kwargs):
        level = self.current_level(self.current_difficulty)
        level.reset()

        self.countdown_event, self.countdown_surf = self.set_countdown()
        self.run(level)

    def end_game(self):
        print('End')
        adapter.clean_event()
        self.next_level()
        self.show_menu()

    def exit(self):
        adapter.exit()

    def change_level(self, value, level):
        if level > self.max_level or level < 1:
            return
        self.current_level = self.levels[level-1]

    def change_difficulty(self, value, difficulty):
        if difficulty > self.max_difficulty or difficulty < 1:
            return
        self.current_difficulty = difficulty

    def next_level(self):
        pass

    def show_menu(self):
        self.menu.launch_menu(adapter.get_screen())

    def set_countdown(self):
        countdown_event = adapter.create_time_event(1000, 4)
        countdown_surf = [
            CountNumber('src/static/3.png'),
            CountNumber('src/static/2.png'),
            CountNumber('src/static/1.png'),
            CountNumber(None),
        ]
        return countdown_event, countdown_surf

    def run(self, level: LevelBase):
        running = True
        countdown_index = 0
        while running:

            if countdown_index == 0:
                adapter.allow(self.countdown_event)

            for event in adapter.get_event():
                running = adapter.exit_game(event)

                if event.type == self.countdown_event:
                    level.exclude_boss_sprites.add(self.countdown_surf[countdown_index])
                    if countdown_index != 0:
                        level.exclude_boss_sprites.remove(self.countdown_surf[countdown_index - 1])

                    adapter.update_display()

                    if countdown_index == 3:
                        adapter.allow(None)

                    countdown_index += 1

                if countdown_index >= 4:
                    level.boss_move(event, level.player)
                    level.player_move(event, level.boss)
            level.update()

            for sprite in level.exclude_boss_sprites:
                adapter.bind_screen(sprite.surf, sprite.rect)

            adapter.update_display()

            level.spark_sprites.update()
            adapter.update_screen()

            if level.is_end():
                end_background = level.end_event()
                adapter.bind_screen(end_background, (0, 0))
                adapter.update_display()

                adapter.delay(2000)
                adapter.wait()
                running = False

        self.end_game()
