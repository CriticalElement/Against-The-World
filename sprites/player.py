import pygame

from constants import *
from sprites.sprite import Sprite


class Player(Sprite):
    def __init__(self, *args):
        super(Player, self).__init__(*args)
        self.x_vel = 0
        self.y_vel = 0
        self.x = 100
        self.y = 200
        self._hasjump = False
        self.surface = pygame.Surface((50, 100))
        self.surface.fill((255, 255, 255))
        self.rect = self.surface.get_rect(topleft=(50, 200))

    def update_coords(self):
        self.rect = self.surface.get_rect(topleft=(50, self.y))

    def update(self, *args, **kwargs):
        self.x_vel = self.x_vel * cof
        self.y_vel = self.y_vel + gravity ** 2
        self.x = self.x + self.x_vel
        self.y = self.y + self.y_vel
        if self.y > 350:
            self.y = 350
            self.y_vel = 0
            self._hasjump = True
        self.update_coords()

    def jump(self):
        if self._hasjump:
            self.y_vel = self.y_vel - 15
            self._hasjump = False
            self.update_coords()
