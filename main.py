import time
import typing

import pygame
from pygame.locals import K_w, K_a, K_d

from helper import *
from gamestate import GameState
from sprites.groundtiles import *
from sprites.player import Player
from sprites.sprite import Sprite
from sprites.menu import *
from sprites.enemy import *
from sprites.hud import *


# initialize the window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Against The World')

events = []
game_state = GameState(events)
menu_image = UIElement((400, 150), image='images/againsttheworld.png')
play_button = Button(lambda: game_state.change_state(game_state.game), (400, 300), 'PLAY')
menu_elements = pygame.sprite.Group()
menu_elements.add(play_button)
menu_elements.add(menu_image)

all_sprites = pygame.sprite.Group()
ground_tiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
damaging_sprites = pygame.sprite.Group()
hud_sprites = pygame.sprite.Group()
health_sprites = pygame.sprite.Group()
for x in range(5):
    heart = HealthHeart(True, (x * 35 + 10, 10))
    hud_sprites.add(heart)
    health_sprites.add(heart)

ground_coords = {}
for x in range(-7500, 7500, 750):
    ground_coords[x] = Ground((x, 450))
    ground_tiles.add(ground_coords[x])
    all_sprites.add(ground_coords[x])
player = Player()
pygame.player = player
pygame.all_sprites = all_sprites
pygame.damaging_sprites = damaging_sprites
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
player.can_move_left = True
player.can_move_right = True
player_health = 5
last_hit_time = 0
player_blink_time = 0
player_blinking = False

current_index = 0
other_leg_index = 6
time_since_bob = time.time()
arm_rotations = [5, 10, 15, 20, 25, 30, 35, 40, 30, 20, 10, 0, -10, -20, -30, -40, -35, -30, -25, -20, -15, -10, -5]
arm_rotation_index = 0
is_arm_rotating = True
should_arm_rotate = True
arm_rotation_direction = 'Right'
sword_swinging = False
sword_damage = 10
hit_enemy = None
hit_time = time.time()

# TODO: randomly generate this and load this from a database
enemy_locations = [600]
for location in enemy_locations:
    enemy = StaticEnemy((location, 294))
    enemies.add(enemy)
    all_sprites.add(enemy)

# game loop
clock = pygame.time.Clock()
running = True
while running:

    # window close
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if game_state.state == 'Menu':
        screen.fill((135, 206, 235))
        element: UIElement
        for element in menu_elements:
            for event in events:
                element.update(event)
            screen.blit(element.surface, element.rect)

    if game_state.state == 'Game':
        # handle enemy collision
        if enemy := pygame.sprite.spritecollideany(player, enemies):
            if player.rect.x < enemy.rect.x:
                # player is to the left of the enemy
                player.x_vel = 0
                player.can_move_right = False
            else:
                # player is to the right of the enemy
                player.x_vel = 0
                player.can_move_left = False
        # handle damage collision
        if (collision := pygame.sprite.spritecollideany(player, damaging_sprites)) and time.time() - last_hit_time > 2:
            collision.kill()
            print('player collided')
            last_hit_time = time.time()
            player_health -= 1
            if player_health == 0:
                # TODO: implement game over screen with menu and retry options
                running = False

        time_diff = time.time() - last_hit_time if last_hit_time != 0 else 0

        def remove_flash():
            player.surface = pygame.image.load('images/headandtorso.png')
            if head_direction == 'Left':
                player.surface = pygame.transform.flip(player.surface, True, False)

        # blink the player every 0.1 seconds whenever they get hit to show an invincibility phase
        if time_diff > 2:
            remove_flash()
            player_blinking = False
        elif 0 < time_diff < 2 and time.time() - player_blink_time > 0.1:
            player_blink_time = time.time()
            if player_blinking:
                remove_flash()
                player_blinking = False
            else:
                player.surface.fill((200, 150, 150), special_flags=pygame.BLEND_RGB_ADD)
                player_blinking = True

        # handle movement
        key = pygame.key.get_pressed()
        if key[K_w]:
            player.jump()
        if key[K_a] and player.can_move_left:
            if not player.can_move_right:
                player.x_vel -= 2
            player.x_vel -= 2
            player.can_move_right = True
            if player.x_vel < -10:
                player.x_vel = -10
        elif key[K_d] and player.can_move_right:
            if not player.can_move_left:
                player.x_vel += 2
            player.x_vel += 2
            player.can_move_left = True
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

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_arm_rotating:
                    should_arm_rotate = True
                else:
                    is_arm_rotating = True
                    arm_rotation_direction = player.sword_direction
            if event.type in event_mappings:
                event_mappings[event.type]()

        if should_arm_rotate and not is_arm_rotating:
            is_arm_rotating = True
            should_arm_rotate = False

        if player.sword_direction == 'Right':
            if arm_rotation_direction == 'Left':
                is_arm_rotating = False
                should_arm_rotate = False
                arm_rotation_index = 0
                arm_rotation_direction = 'Right'
            if is_arm_rotating:
                player.right_arm.rect, player.right_arm.surface = rotate_along_pivot(player.right_arm,
                                                                                     player.right_arm.rectoff.topleft,
                                                                                     (0, 0),
                                                                                     arm_rotations[arm_rotation_index])
                player.sword.rect, player.sword.surface = rotate_along_pivot(player.sword,
                                                                             (player.sword.rectoff.x + -5,
                                                                              player.sword.rectoff.y + 35),
                                                                             (-5, 35),
                                                                             arm_rotations[arm_rotation_index])
                if arm_rotation_index == 0:
                    sword_swinging = True
                if arm_rotation_index == len(arm_rotations) - 1:
                    arm_rotation_index = 0
                    is_arm_rotating = False
                    sword_swinging = False
                else:
                    arm_rotation_index = arm_rotation_index + 1
                    if 7 < arm_rotation_index < 15:
                        enemy_collision: typing.Union[Enemy, Sprite]
                        if enemy_collision := pygame.sprite.spritecollideany(player.sword, enemies):
                            if sword_swinging:
                                enemy_collision.health -= sword_damage
                                sword_swinging = False
                                enemy_collision.surface.fill((200, 150, 150), special_flags=pygame.BLEND_RGB_ADD)
                                hit_enemy = enemy_collision
                                hit_time = time.time()
            else:
                player.right_arm.rect, player.right_arm.surface = player.right_arm.rectoff, \
                                                                  player.right_arm.original_surface
                player.sword.rect, player.sword.surface = player.sword.rectoff, player.sword.original_surface
            player.left_arm.rect, player.left_arm.surface = \
                player.left_arm.rectoff, player.left_arm.original_surface
        else:
            if arm_rotation_direction == 'Right':
                is_arm_rotating = False
                should_arm_rotate = False
                arm_rotation_index = 0
                arm_rotation_direction = 'Left'
            if is_arm_rotating:

                player.left_arm.rect, player.left_arm.surface = rotate_along_pivot(player.left_arm,
                                                                                   (player.left_arm.rectoff.x +
                                                                                    player.left_arm.rectoff.width,
                                                                                    player.left_arm.rectoff.y),
                                                                                   (player.left_arm.rectoff.width, 0),
                                                                                   -arm_rotations[arm_rotation_index])
                player.sword.rect, player.sword.surface = rotate_along_pivot(player.sword,
                                                                             (player.sword.rectoff.x + 76,
                                                                              player.sword.rectoff.y + 40),
                                                                             (76, 40),
                                                                             -arm_rotations[arm_rotation_index])
                if arm_rotation_index == 0:
                    sword_swinging = True
                if arm_rotation_index == len(arm_rotations) - 1:
                    arm_rotation_index = 0
                    is_arm_rotating = False
                    sword_swinging = False
                else:
                    arm_rotation_index = arm_rotation_index + 1
                    if 7 < arm_rotation_index < 15:
                        enemy_collision: typing.Union[Enemy, Sprite]
                        if enemy_collision := pygame.sprite.spritecollideany(player.sword, enemies):
                            if sword_swinging:
                                enemy_collision.health -= sword_damage
                                sword_swinging = False
                                enemy_collision.surface.fill((200, 150, 150), special_flags=pygame.BLEND_RGB_ADD)
                                hit_enemy = enemy_collision
                                hit_time = time.time()
            else:
                player.left_arm.rect, player.left_arm.surface = player.left_arm.rectoff, \
                                                                  player.left_arm.original_surface
                player.sword.rect, player.sword.surface = player.sword.rectoff, player.sword.original_surface
            player.right_arm.rect, player.right_arm.surface = \
                player.right_arm.rectoff, player.right_arm.original_surface
        if not is_arm_rotating:
            player.right_arm.rect, player.right_arm.surface = player.right_arm.rectoff, \
                                                              player.right_arm.original_surface
            player.sword.rect, player.sword.surface = player.sword.rectoff, player.sword.original_surface
            player.left_arm.rect, player.left_arm.surface = \
                player.left_arm.rectoff, player.left_arm.original_surface

        if hit_enemy and time.time() - hit_time > 0.2:
            hit_enemy.surface = hit_enemy.original_surface.copy()
            hit_enemy = None

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
                sword_flipped = player.sword.original_surface.copy()
                sword_flipped = pygame.transform.flip(sword_flipped, True, False)
                player.sword.original_surface = sword_flipped
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
                sword_flipped = player.sword.original_surface.copy()
                sword_flipped = pygame.transform.flip(sword_flipped, True, False)
                player.sword.original_surface = sword_flipped
                player.sword_direction = 'Right'
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
            if not sprite.is_player:
                sprite.update(screen=screen)
                sprite.rectoff = sprite.rect
                sprite.rect = sprite.surface.get_rect(topleft=(sprite.rect.x - player.x, sprite.rect.y))
            screen.blit(sprite.surface, sprite.rect)
        element: HealthHeart
        for index, element in enumerate(health_sprites, start=1):
            filled = True if index <= player_health else False
            element.update(filled)
        hud_elements: Sprite
        for hud_elements in hud_sprites:
            screen.blit(hud_elements.surface, hud_elements.rect)

        player.update()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
