import math

import pygame

from sprites.sprite import Sprite
from sprites.projectile import Projectile
from helper import *


__all__ = ('Enemy', 'StaticEnemy', 'FlyingEnemy')


class Enemy(Sprite):
    def __init__(self, shoot_delay, shoot_func, health, id_, *args, callback=lambda: None):
        super(Enemy, self).__init__(*args)
        self.shoot_func = shoot_func
        self.shoot_event = pygame.USEREVENT + 1
        pygame.USEREVENT += 1  # make sure other sprites can create events
        self.health = health
        self.id = id_
        self.callback = callback
        pygame.time.set_timer(self.shoot_event, shoot_delay)
        event_mappings[self.shoot_event] = self.shoot_func

    def update(self, screen=None):
        super(Enemy, self).update(screen)
        if self.health <= 0:
            self.surface = pygame.Surface((0, 0))
            self.rect = self.surface.get_rect()
            self.rectoff = self.rect
            pygame.cursor.execute('UPDATE enemies SET health = 0, dead = 1 WHERE id=?', (self.id,))
            pygame.conn.commit()
            event_mappings.pop(self.shoot_event, None)
            self.callback()
            self.kill()


class StaticEnemy(Enemy):
    def __init__(self, coords, health, *args, dead=False, **kwargs):
        if dead:
            Sprite.__init__(self)
            self.surface = pygame.Surface((0, 0))
            self.original_surface = self.surface
            self.rect = self.surface.get_rect()
            self.rectoff = self.rect
            self.health = 1
            self.id = args[0]
            self.shoot_event = None
            self.callback = lambda: None
            return
        super(StaticEnemy, self).__init__(3000, self.shoot, health, *args, **kwargs)
        self.surface = pygame.image.load('images/staticenemy.png')
        self.original_surface = self.surface.copy()
        self.rect = self.surface.get_rect(topleft=coords)
        print(self.rect)
        self.rectoff = self.rect
        self.projectile = None

    def shoot(self):
        if 0 < self.rect.x < 800:  # make sure enemy is shooting only when visible on the screen
            start_pos = (self.rect.x + 40 + pygame.player.x, self.rect.y + 60)
            self.projectile = Projectile('images/fireball.png', start_pos, (pygame.player.x, pygame.player.y + 50), 5)
            pygame.all_sprites.add(self.projectile)
            pygame.damaging_sprites.add(self.projectile)


class FlyingEnemy(Enemy):
    def __init__(self, coords, health, *args, dead=False, **kwargs):
        if dead:
            Sprite.__init__(self)
            self.surface = pygame.Surface((0, 0))
            self.original_surface = self.surface
            self.rect = self.surface.get_rect()
            self.rectoff = self.rect
            self.health = 1
            self.id = args[0]
            self.shoot_event = None
            self.callback = lambda: None
            self.original_rect = self.rect
            self.lifetime = 0
            return
        super(FlyingEnemy, self).__init__(3000, self.shoot, health, *args, **kwargs)
        self.surface = pygame.image.load('images/flyingenemy.png')
        self.original_surface = self.surface.copy()
        self.rect = self.surface.get_rect(topleft=coords)
        self.original_rect = self.rect
        print(self.rect)
        self.rectoff = self.rect
        self.projectile = None
        self.lifetime = 0.05  # x value for the sine function

    def shoot(self):
        if 0 < self.rect.x < 800:  # make sure enemy is shooting only when visible on the screen
            start_pos = (self.rect.x + 25 + pygame.player.x, self.rect.y + 12)
            self.projectile = Projectile('images/fireball.png', start_pos, (pygame.player.x, pygame.player.y + 50), 5)
            pygame.all_sprites.add(self.projectile)
            pygame.damaging_sprites.add(self.projectile)

    def update(self, *args, **kwargs):
        super(FlyingEnemy, self).update(*args, **kwargs)
        self.rect = self.original_rect.move(0, math.sin(self.lifetime) * 30)
        self.lifetime += 0.05
