import pygame
from pygame.locals import K_w, K_a, K_d

from sprites.groundtiles import *
from sprites.player import Player
from sprites.sprite import Sprite


# initialize the window
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Against The World')

all_sprites = pygame.sprite.Group()
ground_tiles = pygame.sprite.Group()
ground_coords = {}
for x in range(-7500, 7500, 750):
    ground_coords[x] = Ground((x, 450))
    ground_tiles.add(ground_coords[x])
    all_sprites.add(ground_coords[x])
player = Player()
all_sprites.add(player)

# game loop
clock = pygame.time.Clock()
running = True
while running:

    # window close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    key = pygame.key.get_pressed()
    if key[K_w]:
        player.jump()
    if key[K_a]:
        player.x_vel = player.x_vel - 5
        if player.x_vel < -10:
            player.x_vel = -10
    elif key[K_d]:
        player.x_vel = player.x_vel + 5
        if player.x_vel > 10:
            player.x_vel = 10

    if player.x < -7550:
        player.x = -7550
    if player.x > 7400:
        player.x = 7400

    # background
    screen.fill((135, 206, 235))

    sprite: Sprite
    for sprite in all_sprites:
        x_off = 100
        if sprite != player:
            x_off = x_off - player.x
        screen.blit(sprite.surface, sprite.rect.move(x_off, 0))

    player.update()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
