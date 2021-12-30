import os

import pygame


__all__ = ('UIElement', 'Button')


# https://www.dafont.com/c-c-red-alert-inet.font
font = pygame.font.Font(os.path.abspath('misc/C&C Red Alert [INET].ttf'), 50)


class UIElement(pygame.sprite.Sprite):
    def __init__(self, coords, text='', image='', *args):
        super(UIElement, self).__init__(*args)
        if text:
            self.surface = font.render(text, False, (255, 255, 255)).convert_alpha()
        elif image:
            self.surface = pygame.image.load(image)
        self.rect = self.surface.get_rect(center=coords)


class Button(UIElement):
    def __init__(self, callback, *args):
        super(Button, self).__init__(*args)
        self.callback = callback

    def update(self, event):
        if event and event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()
