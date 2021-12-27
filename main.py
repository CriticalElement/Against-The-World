import time

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
all_sprites.add(player.left_arm)
all_sprites.add(player.right_arm)
all_sprites.add(player.left_leg)
all_sprites.add(player.right_leg)
all_sprites.add(player)
all_sprites.add(player.sword)
foot_flipped = player.left_leg.surface.copy()
foot_flipped = pygame.transform.flip(foot_flipped, True, False)
player.left_leg.surface = foot_flipped
player.right_leg.surface = foot_flipped
leg_direction = 'Right'
head_direction = 'Right'
torso_bobbing = False

current_index = 0
other_leg_index = 6
time_since_bob = time.time()

# game loop
clock = pygame.time.Clock()
running = True
while running:

    # window close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # handle movement
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
    if player.x_vel < 0:
        if head_direction != 'Left':
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
            sword_flipped = player.sword.surface.copy()
            sword_flipped = pygame.transform.flip(sword_flipped, True, False)
            player.sword.surface = sword_flipped
            player.sword_direction = 'Left'
        else:
            # walk cycle
            if current_index % 3:
                player.left_leg.surface = pygame.image.load(f'images/leg{int(current_index / 2)}.png')
                player.right_leg.surface = pygame.image.load(f'images/leg{int(other_leg_index / 2)}.png')
                current_index = current_index + 1
                other_leg_index = other_leg_index + 1
                if current_index == 24:
                    current_index = 0
                if other_leg_index == 24:
                    other_leg_index = 0
            else:
                current_index = current_index + 1
                other_leg_index = other_leg_index + 1
            if time.time() - time_since_bob > 0.1:
                # bob player up and down with walk cycle
                if player.ground_height == 355:
                    player.ground_height = 353
                else:
                    player.ground_height = 355
                time_since_bob = time.time()
    if player.x_vel > 0:
        if head_direction != 'Right':
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
        else:
            # walk cycle
            if current_index % 3:
                player.left_leg.surface = pygame.image.load(f'images/rleg{int(current_index / 2)}.png')
                player.right_leg.surface = pygame.image.load(f'images/rleg{int(other_leg_index / 2)}.png')
                current_index = current_index + 1
                other_leg_index = other_leg_index + 1
                if current_index == 24:
                    current_index = 0
                if other_leg_index == 24:
                    other_leg_index = 0
            else:
                current_index = current_index + 1
                other_leg_index = other_leg_index + 1
            if time.time() - time_since_bob > 0.1:
                # bob player up and down with walk cycle
                if player.ground_height == 355:
                    player.ground_height = 353
                else:
                    player.ground_height = 355
                time_since_bob = time.time()
    if -3 < player.x_vel < 3:
        # reset the leg animation
        if leg_direction == 'Left':
            player.left_leg.surface = pygame.image.load('images/leg0.png')
            player.right_leg.surface = pygame.image.load('images/leg0.png')
            player.ground_height = 355
        else:
            player.left_leg.surface = pygame.image.load('images/rleg0.png')
            player.right_leg.surface = pygame.image.load('images/rleg0.png')
            player.ground_height = 355

    # background
    screen.fill((135, 206, 235))

    # render all sprites
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
