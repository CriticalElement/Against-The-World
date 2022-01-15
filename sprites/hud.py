import time
import os

import pygame

from sprites.sprite import Sprite


__all__ = ('HealthHeart', 'UpdraftIcon', 'DashIcon')


filled_heart = pygame.image.load('images/filledheart.png')
heart = pygame.image.load('images/heart.png')
updraft = pygame.image.load('images/updraft.png')
dash = pygame.image.load('images/dash.png')
font = pygame.font.Font(os.path.abspath('misc/C&C Red Alert [INET].ttf'), 30)


class HealthHeart(Sprite):
    def __init__(self, filled, pos, *args):
        super(HealthHeart, self).__init__(*args)
        self.surface = filled_heart if filled else heart
        self.rect = self.surface.get_rect(topleft=pos)
        self.rectoff = self.rect
        self.is_hud = True

    def update(self, filled):
        super(HealthHeart, self).update()
        self.surface = filled_heart if filled else heart


class UpdraftIcon(Sprite):
    def __init__(self, unlocked, use_time, *args):
        super(UpdraftIcon, self).__init__(*args)
        self.text = None
        self.update_icon(unlocked, use_time)
        self.rect = self.surface.get_rect(topleft=(7, 50))
        self.rectoff = self.rect

    def update_icon(self, unlocked, use_time):
        self.surface = updraft.copy() if unlocked else pygame.Surface((0, 0))
        self.original_surface = self.surface
        if (time_until_use := time.time() - use_time) > 5:
            text = 'Q'
        else:
            text = str(5 - int(time_until_use))
        self.text = font.render(text, True, (255, 255, 255))
        self.surface.blit(self.text, (20, 10))

    def update(self, unlocked, use_time):
        self.update_icon(unlocked, use_time)


class DashIcon(Sprite):
    def __init__(self, unlocked, use_time, *args):
        super(DashIcon, self).__init__(*args)
        self.text = None
        self.update_icon(unlocked, use_time)
        self.rect = self.surface.get_rect(topleft=(7, 90))
        self.rectoff = self.rect

    def update_icon(self, unlocked, use_time):
        self.surface = dash.copy() if unlocked else pygame.Surface((0, 0))
        self.original_surface = self.surface
        if (time_until_use := time.time() - use_time) > 5:
            text = 'E'
        else:
            text = str(5 - int(time_until_use))
        self.text = font.render(text, True, (255, 255, 255))
        self.surface.blit(self.text, (20, 10))

    def update(self, unlocked, use_time):
        self.update_icon(unlocked, use_time)
