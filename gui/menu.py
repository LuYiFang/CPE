from engine.pygame_adapter import adapter, THEME_SOLARIZED


class Menu:
    def __init__(self, width, height, play_func, level_change_func, diff_change_func, exit_func):
        self.menu = adapter.create_menu('Break Keyboard', width, height, theme=THEME_SOLARIZED)

        self.menu.add.button('Play', play_func, 1)
        levels = [(f'Level {i}', i) for i in range(1, 6)]
        self.menu.add.selector('Level', levels, onchange=level_change_func)
        difficulties = [(str(i), i) for i in range(1, 11)]
        self.menu.add.selector('Difficulty', difficulties, onchange=diff_change_func)
        self.menu.add.button('Quit', exit_func)

    def launch_menu(self, surf):
        self.menu.mainloop(surf)
