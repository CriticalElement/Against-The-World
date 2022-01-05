import pygame

from sprites.sprite import Sprite
from sprites.projectile import Projectile
from helper import *


__all__ = ('Enemy', 'StaticEnemy')


class Enemy(Sprite):
    def __init__(self, shoot_delay, shoot_func, health, *args):
        super(Enemy, self).__init__(*args)
        self.shoot_func = shoot_func
        self.shoot_event = pygame.USEREVENT + 1
        self.health = health
        pygame.time.set_timer(self.shoot_event, shoot_delay)
        event_mappings[self.shoot_event] = self.shoot_func

    def update(self, screen=None):
        super(Enemy, self).update(screen)
        if self.health <= 0:
            self.surface = pygame.Surface((0, 0))
            self.rect = self.surface.get_rect()
            self.rectoff = self.rect
            del event_mappings[self.shoot_event]
            self.kill()


class StaticEnemy(Enemy):
    def __init__(self, coords, dead=False, *args):
        if dead:
            Sprite.__init__(self)
            self.surface = pygame.Surface((0, 0))
            self.original_surface = self.surface
            self.rect = self.surface.get_rect()
            self.rectoff = self.rect
            return
        super(StaticEnemy, self).__init__(3000, self.shoot, 50, *args)
        self.surface = pygame.image.load('images/staticenemy1.png')
        self.original_surface = self.surface.copy()
        self.rect = self.surface.get_rect(topleft=coords)
        print(self.rect)
        self.rectoff = self.rect
        self.projectile = None

    def shoot(self):
        start_pos = (self.rect.x + 40 + pygame.player.x, self.rect.y + 60)
        self.projectile = Projectile('images/fireball.png', start_pos, (pygame.player.x, pygame.player.y + 50),
                                     5)
        pygame.all_sprites.add(self.projectile)
