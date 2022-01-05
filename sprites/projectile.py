import math

import pygame

from sprites.sprite import Sprite


__all__ = ('Projectile', )


class Projectile(Sprite):
    def __init__(self, image, start_pos, end_pos, speed, *args):
        super(Projectile, self).__init__(*args)
        self.speed = speed
        self.movements = 0
        self.surface = pygame.image.load(image)
        self.rect = self.surface.get_rect(topleft=start_pos)
        self.original_rect = self.rect
        end_pos_x, end_pos_y = end_pos
        start_pos_x, start_pos_y = start_pos
        self.angle = math.atan2(end_pos_y - start_pos_y, end_pos_x - start_pos_x)
        rotated = pygame.transform.rotate(self.surface, self.angle * 4)
        self.surface = rotated
        self.rect = self.surface.get_rect(center=self.rect.center)
        self.rectoff = self.rect

    def update(self, screen=None):
        super(Projectile, self).update(screen)
        run = math.cos(self.angle) * self.speed * self.movements
        rise = math.sin(self.angle) * self.speed * self.movements
        self.rect = self.original_rect.move(run, rise)
        self.movements = self.movements + 1
        if self.movements == 200:
            self.kill()
            pygame.all_sprites.remove(self)
