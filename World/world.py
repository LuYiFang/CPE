from time import sleep
from World.level import (
    LevelBase,
    Level1,
    Level2,
)

from engine.pygame_adapter import adapter


class World:
    def __init__(self):
        self.current_difficulty = 1
        self.levels = {'Level1': Level1}
        self.current_level = Level2
        adapter.init()
        adapter.set_screen()

    def new_game(self):
        level = self.current_level()
        level.reset()
        self.count_down()
        self.run(level)

    def end_game(self):
        print('End')
        self.next_level()
        self.set_config()

    def exit(self):
        pass

    def change_difficulty(self, level):
        pass

    def next_level(self):
        pass

    def set_config(self):
        pass

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
            adapter.update_screen()
            if level.is_end():
                running = False
        self.end_game()


if __name__ == '__main__':
    world = World()
    world.new_game()
