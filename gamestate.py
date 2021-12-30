import pygame


pygame.init()


class GameState:
    menu = 'Menu'
    game = 'Game'

    def __init__(self):
        self.state = self.menu

    def change_state(self, new_state):
        self.state = new_state
