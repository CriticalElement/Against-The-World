import pygame


class Sprite(pygame.sprite.Sprite):
    """
        This represents a base sprite. This class is never used alone - it is an abstract class that is subclassed
        by other sprites.
    """
    def __init__(self, *args):
        super(Sprite, self).__init__(*args)
        self.surface = None
        self.original_surface = None
        self.rect = None
        self.rectoff = None
        self.is_player = False
        self.is_hud = False

    def update(self, *args, **kwargs):
        self.rect = self.rectoff
