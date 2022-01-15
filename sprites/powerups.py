import math

import pygame

from sprites.sprite import Sprite


__all__ = ('Powerup', 'UpdraftPowerup', 'DashPowerup')


class Powerup(Sprite):
    def __init__(self, coords, image, callback, *args):
        super(Powerup, self).__init__(*args)
        self.surface = pygame.image.load(image)
        self.callback = callback
        self.rect = self.surface.get_rect(topleft=coords)
        self.original_rect = self.rect
        self.rectoff = self.rect
        self.lifetime = 0.07  # number that counts the number of frames the powerup has been active for, for sine wave

    def collect(self):
        self.callback()
        self.kill()

    def update(self, *args, **kwargs):
        super(Powerup, self).update(*args, **kwargs)
        self.rect = self.original_rect.move(0, math.sin(self.lifetime) * 30)  # float up and down
        self.lifetime += 0.07


class UpdraftPowerup(Powerup):
    def __init__(self, coords, *args):
        super(UpdraftPowerup, self).__init__(coords, 'images/updraft.png', *args)


class DashPowerup(Powerup):
    def __init__(self, coords, *args):
        super(DashPowerup, self).__init__(coords, 'images/dash.png', *args)
