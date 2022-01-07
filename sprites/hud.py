import pygame

from sprites.sprite import Sprite


__all__ = ('HealthHeart',)


filled_heart = pygame.image.load('images/filledheart.png')
heart = pygame.image.load('images/heart.png')


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
