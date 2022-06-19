import sys
import pygame
import pygame.locals as k
import pygame_menu
from pygame_menu.themes import THEME_SOLARIZED
from engine.base import GameFrameworkBase
import gui.color as theme


class PygameAdapter(GameFrameworkBase):
    def __init__(self):
        self.screen = None
        self.screen_rgb = None
        self.text_font = None
        self.event_count = 1

    def init(self):
        pygame.init()
        pygame.font.init()
        self.text_font = pygame.font.SysFont('Segoe UI', 34)
        self.text_font.bold = True

    def set_screen(self, width=800, height=600, rgb=theme.WHITE):
        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill(rgb)
        self.screen_rgb = rgb

    def update_screen(self):
        self.screen.fill(self.screen_rgb)

    def get_screen(self):
        return self.screen

    def get_screen_size(self):
        return pygame.display.Info()

    def get_screen_x_y(self):
        screen_size = self.get_screen_size()
        return screen_size.current_w, screen_size.current_h

    def get_event(self):
        return pygame.event.get()

    def get_key_press(self):
        return pygame.key.get_pressed()

    def exit_game(self, event):
        if event.type == k.KEYDOWN:
            if event.key == k.K_ESCAPE:
                return False
        elif event.type == k.QUIT:
            self.exit()
        return True

    def create_surface(self, size, rgb=theme.WHITE):
        surf = pygame.Surface(size)
        surf.fill(rgb)
        return surf, surf.get_rect()

    def draw(self, rgb, x, y, width, height, *args):
        pygame.draw.rect(self.screen, rgb, (x, y, width, height), *args)

    def create_rect(self, *args):
        return pygame.Rect(*args)

    def draw_health_bar(self, pos, size, borderC, backC, healthC, progress):
        pygame.draw.rect(self.screen, backC, (*pos, *size))
        pygame.draw.rect(self.screen, borderC, (*pos, *size), 1)
        innerPos = (pos[0] + 1, pos[1] + 1)
        innerSize = ((size[0] - 2) * progress, size[1] - 2)
        rect = (round(innerPos[0]), round(innerPos[1]), round(innerSize[0]), round(innerSize[1]))
        pygame.draw.rect(self.screen, healthC, rect)

    def load_image(self, path, rgb=theme.WHITE, **kwargs):
        surf = pygame.image.load(path).convert()
        surf.set_colorkey(rgb, k.RLEACCEL)
        return surf, surf.get_rect(**kwargs)

    def resize(self, surface, size):
        return pygame.transform.scale(surface, size)

    def delay(self, ms):
        pygame.time.delay(ms)

    def wait(self):
        return pygame.event.wait()

    def update_display(self, *args):
        # pygame.display.flip()
        pygame.display.update(*args)

    def bind_screen(self, sub_object, rect, *args):
        self.screen.blit(sub_object, rect, *args)

    def collision_object(self):
        return pygame.sprite.Sprite

    def create_group(self):
        return pygame.sprite.Group()

    def add_group(self, group, items):
        for i in items:
            group.add(i)

    def get_usable_event_id(self):
        event_id = pygame.USEREVENT + self.event_count % 10
        self.event_count += 1
        return event_id

    def create_time_event(self, ms, *args):
        event_id = self.get_usable_event_id()
        pygame.time.set_timer(event_id, ms, *args)
        return event_id

    def game_speed(self, frame_rate):
        clock = pygame.time.Clock()
        clock.tick(frame_rate)

    def get_ticks(self):
        pygame.time.get_ticks()

    def create_menu(self, title, width, height, **kwargs):
        return pygame_menu.Menu(title, width, height, **kwargs)

    def menu_exit(self):
        return pygame_menu.events.EXIT

    def exit(self):
        pygame.quit()
        sys.exit()

    def clean_event(self):
        pygame.event.clear()

    def block(self, type=None):
        pygame.event.set_blocked(type)

    def allow(self, type=None):
        pygame.event.set_allowed(type)

    def create_event_type(self):
        return pygame.event.custom_type()

    def create_event(self, *args):
        return pygame.event.Event(*args)

    def post_event(self, *args):
        return pygame.event.post(*args)

    def create_text(self, text, color=theme.TEXT):
        return self.text_font.render(text, False, color)


adapter = PygameAdapter()
