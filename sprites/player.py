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
        self.surface = pygame.image.load('images/headandtorso.png').convert()
        self.surface.set_colorkey((99, 99, 99))
        self.rect = pygame.Rect(50, 350, 65, 100)
        self.left_arm = LeftArm()
        self.right_arm = RightArm()
        self.left_leg = LeftLeg()
        self.right_leg = RightLeg()

    def update_coords(self):
        self.rect = self.surface.get_rect(topleft=(50, self.y))
        self.left_arm.rect = self.left_arm.surface.get_rect(topleft=(50, self.y + 45))
        self.right_arm.rect = self.right_arm.surface.get_rect(topleft=(95, self.y + 45))
        self.left_leg.rect = self.left_leg.surface.get_rect(topleft=(55, self.y + 80))
        self.right_leg.rect = self.right_leg.surface.get_rect(topleft=(75, self.y + 80))

    def update(self, *args, **kwargs):
        self.x_vel = self.x_vel * cof
        self.y_vel = self.y_vel + gravity ** 2
        self.x = self.x + self.x_vel
        self.y = self.y + self.y_vel
        if self.y > 355:
            self.y = 355
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
        self.surface = pygame.image.load('images/rightarm.png').convert()
        self.surface.set_colorkey((99, 99, 99))
        self.rect = self.surface.get_rect(topleft=(70, 380))
        self.is_player = True


class LeftLeg(Sprite):
    def __init__(self, *args):
        super(LeftLeg, self).__init__(*args)
        self.surface = pygame.image.load('images/leg.png').convert()
        self.surface.set_colorkey((99, 99, 99))
        self.rect = self.surface.get_rect(topleft=(55, 400))
        self.is_player = True


class RightLeg(Sprite):
    def __init__(self, *args):
        super(RightLeg, self).__init__(*args)
        self.surface = pygame.image.load('images/leg.png').convert()
        self.surface.set_colorkey((99, 99, 99))
        self.rect = self.surface.get_rect(topleft=(75, 400))
        self.is_player = True
