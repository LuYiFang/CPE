import sys
import pygame
from pygame.locals import (
    KEYDOWN,
    KEYUP,
    K_ESCAPE,
    QUIT,
    RLEACCEL,
    K_RETURN,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_c,
)
import pygame_menu
from pygame_menu.themes import THEME_SOLARIZED
from engine.base import GameFrameworkBase


class PygameAdapter(GameFrameworkBase):
    def __init__(self):
        self.screen = None
        self.screen_rgb = None

    def init(self):
        pygame.init()

    def set_screen(self, width=800, height=600, rgb=(255, 255, 255)):
        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill(rgb)
        self.screen_rgb = rgb

    def update_screen(self):
        self.screen.fill(self.screen_rgb)

    def get_screen(self):
        return self.screen

    def get_screen_size(self):
        return pygame.display.Info()

    def get_event(self):
        return pygame.event.get()

    def get_key_press(self):
        return pygame.key.get_pressed()

    def exit_game(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return False
        elif event.type == QUIT:
            self.exit()
        return True

    def create_surface(self, size, rgb=(255, 255, 255)):
        surf = pygame.Surface(size)
        surf.fill(rgb)
        return surf, surf.get_rect()

    def draw(self, rgb, x, y, width, height, *args):
        pygame.draw.rect(self.screen, rgb, (x, y, width, height), *args)

    def create_rect(self, *args):
        return pygame.Rect(*args)

    # def draw_hp_bar(self, inner_pos, inner_size, health_color):
    #     # pygame.draw.rect(self.screen, back_color, (*pos, *size))
    #     # pygame.draw.rect(self.screen, border_color, (*pos, *size), 1)
    #     # inner_pos = (pos[0] + 1, pos[1] + 1)
    #     rect = (round(inner_pos[0]), round(inner_pos[1]), round(inner_size[0]), round(inner_size[1]))
    #     self.draw(health_color, *rect)
    #     # pygame.draw.rect(self.screen, health_color, rect)

    def draw_health_bar(self, pos, size, borderC, backC, healthC, progress):
        pygame.draw.rect(self.screen, backC, (*pos, *size))
        pygame.draw.rect(self.screen, borderC, (*pos, *size), 1)
        innerPos = (pos[0] + 1, pos[1] + 1)
        innerSize = ((size[0] - 2) * progress, size[1] - 2)
        rect = (round(innerPos[0]), round(innerPos[1]), round(innerSize[0]), round(innerSize[1]))
        pygame.draw.rect(self.screen, healthC, rect)

    def load_image(self, path, rgb=(255, 255, 255), **kwargs):
        surf = pygame.image.load(path).convert()
        surf.set_colorkey(rgb, RLEACCEL)
        return surf, surf.get_rect(**kwargs)

    def resize(self, surface, size):
        return pygame.transform.scale(surface, size)

    def delay(self, ms):
        pygame.time.delay(ms)

    def update_display(self):
        # pygame.display.flip()
        pygame.display.update()

    def bind_screen(self, sub_object, rect, *args):
        self.screen.blit(sub_object, rect, *args)

    def collision_object(self):
        return pygame.sprite.Sprite

    def create_group(self):
        return pygame.sprite.Group()

    def add_group(self, group, items):
        for i in items:
            group.add(i)

    def create_time_event(self, ms):
        event_id = pygame.USEREVENT + 1
        pygame.time.set_timer(event_id, ms)
        return event_id

    def game_speed(self, frame_rate):
        clock = pygame.time.Clock()
        clock.tick(frame_rate)

    def get_ticks(self):
        pygame.time.get_ticks()

    def create_menu(self, title, width, height, **kwargs):
        return pygame_menu.Menu(title, width, height, **kwargs)

    def menu_exit(self):
        pygame_menu.events.EXIT

    def exit(self):
        pygame.quit()
        sys.exit()


adapter = PygameAdapter()
