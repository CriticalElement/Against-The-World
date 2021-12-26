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
all_sprites.add(player.left_arm)
all_sprites.add(player.right_arm)
all_sprites.add(player.left_leg)
all_sprites.add(player.right_leg)

foot_flipped = player.left_leg.surface.copy()
foot_flipped = pygame.transform.flip(foot_flipped, True, False)
player.left_leg.surface = foot_flipped
player.right_leg.surface = foot_flipped
leg_direction = 'Right'
head_direction = 'Right'

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

    if 0 < player.x_vel < 1:
        player.x_vel = 0
    if -1 < player.x_vel < 0:
        player.x_vel = 0
    if player.x < -7550:
        player.x = -7550
    if player.x > 7400:
        player.x = 7400

    # sprite flipping
    if player.x_vel < 0 and head_direction != 'Left':
        # moving to the left
        head_flipped = player.surface.copy()
        head_flipped = pygame.transform.flip(head_flipped, True, False)
        player.surface = head_flipped
        foot_flipped = player.left_leg.surface.copy()
        foot_flipped = pygame.transform.flip(foot_flipped, True, False)
        player.left_leg.surface = foot_flipped
        player.right_leg.surface = foot_flipped
        leg_direction = 'Left'
        head_direction = 'Left'
    if player.x_vel > 0 and leg_direction != 'Right':
        # moving to the right
        foot_flipped = player.left_leg.surface.copy()
        foot_flipped = pygame.transform.flip(foot_flipped, True, False)
        player.left_leg.surface = foot_flipped
        player.right_leg.surface = foot_flipped
        head_flipped = player.surface.copy()
        head_flipped = pygame.transform.flip(head_flipped, True, False)
        player.surface = head_flipped
        head_direction = 'Right'
        leg_direction = 'Right'

    # background
    screen.fill((135, 206, 235))

    sprite: Sprite
    for sprite in all_sprites:
        x_off = 100
        if not sprite.is_player:
            x_off = x_off - player.x
        screen.blit(sprite.surface, sprite.rect.move(x_off, 0))

    player.update()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
