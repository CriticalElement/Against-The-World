import math

import pygame

from sprites.sprite import Sprite


__all__ = ('Projectile', 'Laserbeam', 'LaserbeamWarning')


fireball_sfx = pygame.mixer.Sound('sfx/fireball.wav')


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
        if end_pos_x > start_pos_x:
            # if the target is behind the staring position - flip the fireball so it is "upright"
            rotated = pygame.transform.rotate(self.surface, math.degrees(self.angle) - 180)  # offset for default image
            rotated = pygame.transform.flip(rotated, False, True)
        else:
            rotated = pygame.transform.rotate(self.surface, -math.degrees(self.angle) - 180)  # offset for default image
        self.surface = rotated
        self.rect = self.surface.get_rect(center=self.rect.center)
        self.rectoff = self.rect
        fireball_sfx.play()

    def update(self, screen=None):
        super(Projectile, self).update(screen)
        run = math.cos(self.angle) * self.speed * self.movements
        rise = math.sin(self.angle) * self.speed * self.movements
        self.rect = self.original_rect.move(run, rise)
        self.movements = self.movements + 1
        if self.movements == 150:
            self.kill()

    def kill(self):
        pygame.all_sprites.remove(self)
        pygame.damaging_sprites.remove(self)
        super(Projectile, self).kill()


class Laserbeam(Sprite):
    def __init__(self, sideways, xpos, warning, *args):
        super(Laserbeam, self).__init__(*args)
        self.movements = 0
        self.surface = pygame.image.load('images/laserbeam.png')
        self.warning = warning
        self.sideways = sideways
        if sideways:
            self.surface = pygame.transform.rotate(self.surface, 90)
            coords = (xpos - 1300, 330)
        else:
            coords = (xpos, -1200)
        self.rect = self.surface.get_rect(topleft=coords)
        self.rectoff = self.rect
        self.original_rect = self.rect

    def update(self, *args, **kwargs):
        super(Laserbeam, self).update(*args, **kwargs)
        if self.sideways:
            self.rect = self.original_rect.move(60 * self.movements, 0)
        else:
            self.rect = self.original_rect.move(0, 20 * self.movements)
        self.movements += 1
        if self.movements == 120:
            pygame.all_sprites.remove(self)
            pygame.damaging_sprites.remove(self)
            self.kill()
        elif self.movements == 10:
            pygame.all_sprites.remove(self.warning)
            self.warning.kill()


class LaserbeamWarning(Sprite):
    def __init__(self, coords, sideways, *args):
        super(LaserbeamWarning, self).__init__(*args)
        self.lifetime = 0
        self.sideways = sideways
        self.surface = pygame.image.load('images/warning.png')
        self.rect = self.surface.get_rect(topleft=coords)
        self.rectoff = self.rect

    def update(self, *args, **kwargs):
        super(LaserbeamWarning, self).update(*args, **kwargs)
        self.lifetime += 1
        if self.lifetime == 50:
            laser_beam = Laserbeam(self.sideways, self.rect.x - 30, self)
            pygame.damaging_sprites.add(laser_beam)
            pygame.all_sprites.add(laser_beam)
