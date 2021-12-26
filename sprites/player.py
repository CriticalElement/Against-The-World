import pygame

from constants import *
from sprites.sprite import Sprite


class Player(Sprite):
    def __init__(self, *args):
        super(Player, self).__init__(*args)
        self.x_vel = 0
        self.y_vel = 0
        self.x = 0
        self.y = 350
        self._hasjump = False
        self.is_player = True
        self.surface = pygame.Surface((50, 100))
        self.surface.fill((255, 255, 255))
        self.rect = self.surface.get_rect(topleft=(50, 350))
        self.left_arm = LeftArm()
        self.right_arm = RightArm()

    def update_coords(self):
        self.rect = self.surface.get_rect(topleft=(50, self.y))
        self.left_arm.rect = self.left_arm.surface.get_rect(topleft=(40, self.y + 30))
        self.right_arm.rect = self.right_arm.surface.get_rect(topleft=(95, self.y + 30))

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


class LeftArm(Sprite):
    def __init__(self, *args):
        super(LeftArm, self).__init__(*args)
        self.surface = pygame.image.load('images/leftarm.png').convert()
        self.surface.set_colorkey((99, 99, 99))
        self.rect = self.surface.get_rect(topleft=(40, 380))
        self.is_player = True


class RightArm(Sprite):
    def __init__(self, *args):
        super(RightArm, self).__init__(*args)
        self.surface = pygame.Surface((15, 24))
        self.surface.fill((255, 0, 0))
        self.rect = self.surface.get_rect(topleft=(70, 380))
        self.is_player = True
