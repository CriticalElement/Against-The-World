import pygame


pygame.init()


class GameState:
    menu = 'Menu'
    game = 'Game'
    pause = 'Pause'
    game_over = 'Game Over'
    win = 'End'

    def __init__(self, events):
        self.state = self.menu
        self.events = events

    def change_state(self, new_state):
        self.state = new_state
        self.events = []
