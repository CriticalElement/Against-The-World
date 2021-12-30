import pygame

from sprites.sprite import Sprite


__all__ = ('StaticEnemy',)


class StaticEnemy(Sprite):
    def __init__(self, coords, *args):
        super(StaticEnemy, self).__init__(*args)
        self.surface = pygame.image.load('images/staticenemy1.png')
        self.rect = self.surface.get_rect(topleft=coords)
        self.rectoff = self.rect
