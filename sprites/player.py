import pygame

from helper import *
from sprites.sprite import Sprite


class Player(Sprite):
    def __init__(self, *args):
        super(Player, self).__init__(*args)
        self.x_vel = 0
        self.y_vel = 0
        self.x = 0
        self.y = 350
        self.sword_offset_x = 0
        self.sword_offset_y = 0
        self.ground_height = 355
        self._hasjump = False
        self.is_player = True
        self.surface = pygame.image.load('images/headandtorso.png')
        self.rect = pygame.Rect(50, 350, 65, 100)
        self.rectoff = self.rect
        self.left_arm = LeftArm()
        self.right_arm = RightArm()
        self.left_leg = LeftLeg()
        self.right_leg = RightLeg()
        self.sword = Sword()
        self.sword_direction = 'Right'

    def update_coords(self):
        self.rect = self.surface.get_rect(topleft=(50, self.y))
        self.left_arm.rectoff = self.left_arm.surface.get_rect(topleft=(50, self.y + 45))
        self.right_arm.rectoff = self.right_arm.surface.get_rect(topleft=(95, self.y + 45))
        self.left_leg.rect = self.left_leg.surface.get_rect(topleft=(55, self.y + 72))
        self.right_leg.rect = self.right_leg.surface.get_rect(topleft=(75, self.y + 72))
        if self.sword_direction == 'Right':
            self.sword.rectoff = self.sword.surface.get_rect(topleft=(105, self.y + 5))
        else:
            self.sword.rectoff = self.sword.surface.get_rect(topleft=(-5, self.y + 5))

    def update(self, *args, **kwargs):
        self.x_vel = self.x_vel * cof
        self.y_vel = self.y_vel + gravity ** 2
        self.x = self.x + self.x_vel
        self.y = self.y + self.y_vel
        if self.y > self.ground_height:
            self.y = self.ground_height
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
        self.surface = pygame.image.load('images/leftarm.png')
        self.original_surface = self.surface
        self.rect = self.surface.get_rect(topleft=(40, 380))
        self.rectoff = self.rect
        self.is_player = True


class RightArm(Sprite):
    def __init__(self, *args):
        super(RightArm, self).__init__(*args)
        self.surface = pygame.image.load('images/rightarm.png')
        self.original_surface = self.surface
        self.rect = self.surface.get_rect(topleft=(70, 380))
        self.rectoff = self.rect
        self.is_player = True


class LeftLeg(Sprite):
    def __init__(self, *args):
        super(LeftLeg, self).__init__(*args)
        self.surface = pygame.image.load('images/leg0.png')
        self.rect = self.surface.get_rect(topleft=(55, 400))
        self.rectoff = self.rect
        self.is_player = True


class RightLeg(Sprite):
    def __init__(self, *args):
        super(RightLeg, self).__init__(*args)
        self.surface = pygame.image.load('images/leg0.png')
        self.rect = self.surface.get_rect(topleft=(75, 400))
        self.rectoff = self.rect
        self.is_player = True


class Sword(Sprite):
    def __init__(self, *args):
        super(Sword, self).__init__(*args)
        self.surface = pygame.image.load('images/sword.png')
        self.original_surface = self.surface
        self.rect = self.surface.get_rect(topleft=(85, 380))
        self.rectoff = self.rect
        self.is_player = True

    def update(self, screen=None):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
