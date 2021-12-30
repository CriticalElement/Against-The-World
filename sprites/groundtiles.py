import pygame

from sprites.sprite import Sprite

__all__ = ('GroundTile', 'Ground')


class GroundTile(Sprite):
    def __init__(self, img, coords, *args):
        super(GroundTile, self).__init__(*args)
        self.surface = img
        self.rect = self.surface.get_rect(topleft=coords)
        self.rectoff = self.rect


class Ground(GroundTile):
    def __init__(self, coords, *args):
        ground_img = pygame.image.load('images/ground.png').convert()
        super(Ground, self).__init__(ground_img, coords, *args)
