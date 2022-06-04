from World.level import (
    LevelBase,
    Level1,
    Level2,
)

from engine.pygame_adapter import adapter
from gui.menu import Menu


class World:
    def __init__(self):
        self.current_difficulty = 1
        self.max_difficulty = 10
        self.levels = [Level1, Level2]
        self.max_level = len(self.levels)
        self.current_level = Level1
        adapter.init()
        adapter.set_screen()
        screen_size = adapter.get_screen_size()
        self.menu = Menu(
            screen_size.current_w, screen_size.current_h,
            self.new_game, self.change_level, self.change_difficulty, self.exit
        )

    def new_game(self, *args, **kwargs):
        level = self.current_level()
        level.reset()

        self.count_down()
        self.run(level)

    def end_game(self):
        print('End')
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

    def count_down(self):
        pass
        # for i in reversed(range(1, 4)):
        #     print(i)
        #     sleep(1)

    def run(self, level: LevelBase):
        running = True
        while running:

            for event in adapter.get_event():
                running = adapter.exit_game(event)
                level.boss_move(event, level.player)

                level.player_move(event, level.boss)
            level.update()

            for sprite in level.exclude_boss_sprites:
                adapter.bind_screen(sprite.surf, sprite.rect)

            adapter.update_display()

            level.spark_sprites.update()
            adapter.update_screen()

            if level.is_end():
                running = False
        self.end_game()


if __name__ == '__main__':
    world = World()
    world.show_menu()
