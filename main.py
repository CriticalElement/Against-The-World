import time
import typing
import random

import pygame
import sqlite3

from pygame.locals import K_w, K_a, K_d, K_SPACE, K_q, K_e, K_ESCAPE

from helper import *
from gamestate import GameState
from sprites.groundtiles import *
from sprites.player import Player
from sprites.sprite import Sprite
from sprites.menu import *
from sprites.enemy import *
from sprites.hud import *
from sprites.powerups import *


# initialize the window
screen = pygame.display.set_mode((800, 600))
pygame.screen = screen
pygame.display.set_caption('Against The World')
pygame.display.set_icon(pygame.image.load('images/sword.png'))

# connect to database
conn = sqlite3.connect('misc/database.db')
cursor = conn.cursor()

events = []
game_state = GameState(events)
menu_image = UIElement((400, 150), image='images/againsttheworld.png')
play_button = Button(lambda: game_state.change_state(game_state.game), (400, 300), 'PLAY')


def new_game():
    cursor.execute('DELETE FROM enemies')
    cursor.execute('DELETE FROM stats')
    for enemy_ in enemies.copy():
        enemies.remove(enemy_)
        all_sprites.remove(enemy_)
    conn.commit()
    start = 1200
    enemy_positions = []
    event_mappings.clear()

    for _ in range(0, 5):
        enemy_positions.append(start)
        start += random.randint(1000, 2000)
    for index_, enemy_pos in enumerate(enemy_positions):
        random_id = random.randint(1000000, 10000000)  # generate random id for selecting specific enemy with database
        killed_callback = create_updraft if index_ == 4 else lambda: None
        enemy_ = StaticEnemy((enemy_pos, 294), 50, random_id, callback=killed_callback)
        all_sprites.add(enemy_)
        enemies.add(enemy_)
        cursor.execute('INSERT INTO enemies VALUES (?, "static", ?, 294, 50, 0)', (random_id, enemy_pos))
        conn.commit()
    for _ in range(0, 3):
        enemy_positions.append(start)
        start += random.randint(1000, 2000)
    enemy_positions = enemy_positions[-3:]  # use the newly created enemy positions
    for index_, enemy_pos in enumerate(enemy_positions):
        random_id = random.randint(1000000, 10000000)
        killed_callback = create_dash if index_ == 2 else lambda: None
        enemy_ = FlyingEnemy((enemy_pos, 100), 10, random_id, callback=killed_callback)
        all_sprites.add(enemy_)
        enemies.add(enemy_)
        cursor.execute('INSERT INTO enemies VALUES (?, "flying", ?, 100, 10, 0)', (random_id, enemy_pos))
        conn.commit()
    random_id = random.randint(1000000, 10000000)
    boss_ = Boss((13000, 100), 50, random_id)
    cursor.execute('INSERT INTO enemies VALUES (?, "boss", 13000, 75, 50, 0)', (random_id,))
    all_sprites.add(boss_)
    enemies.add(boss_)
    conn.commit()
    cursor.execute('DELETE FROM stats')
    conn.commit()
    cursor.execute('INSERT INTO stats VALUES (5, 0, 0, 0, 350)')
    player.x = 0
    player.y = 350
    global updraft_unlocked, dash_unlocked, player_health
    updraft_unlocked = False
    dash_unlocked = False
    player_health = 5
    conn.commit()


def start_new_game():
    new_game()
    game_state.change_state(game_state.game)


new_game_button = Button(start_new_game, (400, 400), 'NEW GAME')


def stop():
    global running
    running = False


quit_button = Button(stop, (400, 500), 'QUIT')
menu_elements = pygame.sprite.Group()
menu_elements.add(play_button)
menu_elements.add(menu_image)
menu_elements.add(new_game_button)
menu_elements.add(quit_button)

all_sprites = pygame.sprite.Group()
ground_tiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
damaging_sprites = pygame.sprite.Group()
hud_sprites = pygame.sprite.Group()
health_sprites = pygame.sprite.Group()

ground_coords = {}
for x in range(-750, 15000, 750):
    ground_coords[x] = Ground((x, 450))
    ground_tiles.add(ground_coords[x])
    all_sprites.add(ground_coords[x])
player = Player()
pygame.player = player
pygame.all_sprites = all_sprites
pygame.damaging_sprites = damaging_sprites
pygame.cursor = cursor
pygame.conn = conn
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
is_arm_rotating = False
should_arm_rotate = False
arm_rotation_direction = 'Right'
sword_swinging = False
sword_damage = 10
hit_enemy = None
hit_time = time.time()
updraft_time = 0
dash_time = 0
is_dashing = False
updraft_unlocked = False
dash_unlocked = False
updraft_icon = UpdraftIcon(updraft_unlocked, 0)
hud_sprites.add(updraft_icon)
dash_icon = DashIcon(dash_unlocked, 0)
hud_sprites.add(dash_icon)
pause_icon = Button(lambda: game_state.change_state(game_state.pause), (785, 15), image='images/pause.png')
hud_sprites.add(pause_icon)
powerups = pygame.sprite.Group()

game_over_elements = pygame.sprite.Group()
continue_button = Button(start_new_game, (400, 300), 'TRY AGAIN')
menu_button = Button(lambda: game_state.change_state(game_state.menu), (400, 400), 'MENU')
game_over_text = UIElement((400, 100), 'GAME OVER')
game_over_elements.add(continue_button)
game_over_elements.add(game_over_text)
game_over_elements.add(menu_button)

pause_menu_elements = pygame.sprite.Group()
resume = Button(lambda: game_state.change_state(game_state.game), (400, 300), 'RESUME')
menu_pause_button = Button(lambda: game_state.change_state(game_state.menu), (400, 400), 'MENU')
pause_text = UIElement((400, 100), 'PAUSED')
pause_menu_elements.add(resume)
pause_menu_elements.add(menu_pause_button)
pause_menu_elements.add(pause_text)

win_elements = pygame.sprite.Group()
new_game_win_button = Button(start_new_game, (400, 400), 'NEW GAME')
menu_win_button = Button(lambda: game_state.change_state(game_state.menu), (400, 500), 'MENU')
win_text = UIElement((400, 100), 'YOU WIN!')
win_elements.add(new_game_win_button)
win_elements.add(menu_win_button)
win_elements.add(win_text)

sword_sfx = pygame.mixer.Sound('sfx/swordpullout.mp3')
hit_sfx = pygame.mixer.Sound('sfx/hit.wav')
player_hit_sfx = pygame.mixer.Sound('sfx/playerhit.wav')
updraft_sfx = pygame.mixer.Sound('sfx/updraft.mp3')
dash_sfx = pygame.mixer.Sound('sfx/dash.wav')
powerup_sfx = pygame.mixer.Sound('sfx/powerup.wav')


def unlock_updraft():
    global updraft_unlocked
    updraft_unlocked = True
    powerup_sfx.play()
    cursor.execute('DELETE FROM stats')
    conn.commit()
    cursor.execute('INSERT INTO stats VALUES (?, ?, ?, ?, ?)', (player_health, int(updraft_unlocked),
                                                                int(dash_unlocked), player.x, player.y))
    conn.commit()


def unlock_dash():
    global dash_unlocked
    dash_unlocked = True
    powerup_sfx.play()
    cursor.execute('DELETE FROM stats')
    conn.commit()
    cursor.execute('INSERT INTO stats VALUES (?, ?, ?, ?, ?)', (player_health, int(updraft_unlocked),
                                                                int(dash_unlocked), player.x, player.y))
    conn.commit()


def create_updraft():
    updraft_powerup = UpdraftPowerup((player.x + 200, 280), unlock_updraft)
    all_sprites.add(updraft_powerup)
    powerups.add(updraft_powerup)


def create_dash():
    dash_powerup = DashPowerup((player.x + 170, 100), unlock_dash)
    all_sprites.add(dash_powerup)
    powerups.add(dash_powerup)


for index, (id_, enemy_type, xpos, ypos, health, dead) in enumerate(cursor.execute('SELECT * FROM enemies')):
    enemy = Sprite
    if enemy_type == 'static':
        callback = create_updraft if index == 4 else lambda: None
        print(index)
        enemy = StaticEnemy((xpos, ypos), health, id_, callback=callback, dead=bool(dead))
    elif enemy_type == 'flying':
        callback = create_dash if index == 7 else lambda: None
        enemy = FlyingEnemy((xpos, ypos), health, id_, callback=callback, dead=bool(dead))
    else:
        enemy = Boss((13000, 75), 50, id_, dead=bool(dead))
    if not bool(dead):
        enemies.add(enemy)
        all_sprites.add(enemy)

for health, updraft, dash, xpos, ypos in cursor.execute('SELECT * FROM stats'):
    player_health = health
    updraft_unlocked = bool(updraft)
    dash_unlocked = bool(dash)
    player.x = xpos
    player.y = ypos

for x in range(5):
    alive = True if x <= player_health else False
    heart = HealthHeart(alive, (x * 35 + 10, 10))
    hud_sprites.add(heart)
    health_sprites.add(heart)

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
            element.update()
            for event in events:
                element.update(event)
            screen.blit(element.surface, element.rect)

    if game_state.state == 'Pause':
        screen.fill((135, 206, 235))
        element: UIElement
        for element in pause_menu_elements:
            element.update()
            for event in events:
                element.update(event)
            screen.blit(element.surface, element.rect)

    if game_state.state == 'Game Over':
        screen.fill((255, 87, 112))
        element: UIElement
        for element in game_over_elements:
            element.update()
            for event in events:
                element.update(event)
            screen.blit(element.surface, element.rect)

    if game_state.state == 'End':
        screen.fill((72, 212, 109))
        element: UIElement
        for element in win_elements:
            element.update()
            for event in events:
                element.update(event)
            screen.blit(element.surface, element.rect)

    if game_state.state == 'Game':
        # handle enemy collision
        if enemy := pygame.sprite.spritecollideany(player, enemies):
            if player.rect.y + 50 < enemy.rect.topleft[1] and isinstance(enemy, StaticEnemy):  # make sure you only land
                # on static enemies
                player.ground_height = player.y
            elif player.rect.x < enemy.rect.x:
                # player is to the left of the enemy
                if isinstance(enemy, StaticEnemy):
                    player.x_vel = 0
                    player.can_move_right = False
            else:
                # player is to the right of the enemy
                if isinstance(enemy, StaticEnemy):
                    player.x_vel = 0
                    player.can_move_left = False
        else:
            if player.ground_height < 300:
                player.ground_height = 355
        # handle damage collision
        if (collision := pygame.sprite.spritecollideany(player, damaging_sprites)) and time.time() - last_hit_time > 2\
                and not is_dashing:
            player_hit_sfx.play()
            collision.kill()
            last_hit_time = time.time()
            player_health -= 1
            cursor.execute('DELETE FROM stats')
            conn.commit()
            cursor.execute('INSERT INTO stats VALUES (?, ?, ?, ?, ?)',
                           (player_health, int(updraft_unlocked), int(dash_unlocked),
                            player.x, player.y))
            conn.commit()
            if player_health == 0:
                player_health = 5
                cursor.execute('DELETE FROM stats')
                conn.commit()
                cursor.execute('INSERT INTO stats VALUES (?, ?, ?, ?, ?)',
                               (player_health, int(updraft_unlocked), int(dash_unlocked),
                                player.x, player.y))
                conn.commit()
                game_state.change_state(game_state.game_over)
        # handle powerup collection
        powerup: typing.Union[Powerup, Sprite]
        if powerup := pygame.sprite.spritecollideany(player, powerups):
            powerup.collect()
            all_sprites.remove(powerup)
            powerups.remove(powerup)

        time_diff = time.time() - last_hit_time if last_hit_time != 0 else 0

        def remove_flash():
            player.original_surface = pygame.image.load('images/headandtorso.png')
            player.surface = player.original_surface.copy()
            if head_direction == 'Left':
                player.surface = pygame.transform.flip(player.surface, True, False)

        # blink the player every 0.1 seconds whenever they get hit to show an invincibility phase
        if time_diff > 2:
            remove_flash()
            player_blinking = False
            player_blink_time = 0
        elif 0 < time_diff < 2 and time.time() - player_blink_time > 0.1:
            player_blink_time = time.time()
            if player_blinking:
                remove_flash()
                player_blinking = False
            else:
                player.surface = player.surface.copy()
                player.surface.fill((200, 150, 150), special_flags=pygame.BLEND_RGB_ADD)
                player_blinking = True

        # handle movement
        key = pygame.key.get_pressed()
        if key[K_w] or key[K_SPACE]:
            player.jump()
        if key[K_a] and player.can_move_left:
            if not player.can_move_right:
                player.x_vel -= 2
            if not is_dashing:
                player.x_vel -= 2
            player.can_move_right = True
            if player.x_vel < -10:
                if not is_dashing:  # remove the speed limit when dashing
                    player.x_vel = -10
        elif key[K_d] and player.can_move_right:
            if not player.can_move_left:
                player.x_vel += 2
            if not is_dashing:
                player.x_vel += 2
            player.can_move_left = True
            if player.x_vel > 10:
                if not is_dashing:  # remove the speed limit when dashing
                    player.x_vel = 10
        if key[K_q] and time.time() - updraft_time > 5 and updraft_unlocked:
            player.y_vel = -25
            updraft_time = time.time()
            updraft_sfx.play()
        if key[K_e] and time.time() - dash_time > 5 and dash_unlocked:
            dash_sfx.play()
            is_dashing = True
            remove_flash()
            last_hit_time = 0
            player_blinking = False
            player_blink_time = 0
            player.surface = player.surface.copy()
            player.surface.fill((255, 255, 255, 128), special_flags=pygame.BLEND_RGBA_MULT)
            if head_direction == 'Right':
                player.x_vel = 50
            else:
                player.x_vel = -50
            dash_time = time.time()
        if key[K_ESCAPE]:
            pause_icon.callback()

        if -5 < player.x_vel < 5 and is_dashing:
            is_dashing = False
            remove_flash()
            player_blinking = False
            player_blink_time = 0

        if 0 < player.x_vel < 1:
            player.x_vel = 0
        if -1 < player.x_vel < 0:
            player.x_vel = 0
        if player.x < -800:
            player.x = -800
        if player.x > 14900:
            player.x = 14900

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not pause_icon.rect.collidepoint(event.pos):
                    if is_arm_rotating:
                        should_arm_rotate = True
                    else:
                        is_arm_rotating = True
                        arm_rotation_direction = player.sword_direction
            if event.type == pygame.MOUSEBUTTONUP and pause_icon.rect.collidepoint(event.pos):
                pause_icon.update(event)
            if event.type in event_mappings:
                event_mappings[event.type]()

        if len(enemies) == 0:
            game_state.change_state(game_state.win)

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
                    sword_sfx.play()
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
                                cursor.execute('UPDATE enemies SET health = ? WHERE id=?', (enemy_collision.health,
                                                                                            enemy_collision.id))
                                conn.commit()
                                hit_sfx.play()
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
                    sword_sfx.play()
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
                                cursor.execute('UPDATE enemies SET health = ? WHERE id=?', (enemy_collision.health,
                                                                                            enemy_collision.id))
                                conn.commit()
                                hit_sfx.play()
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
                if (timeoff := time.time() - time_since_bob) > 0.1:
                    # bob player up and down with walk cycle
                    if torso_bobbing:
                        player.ground_height -= 2
                    else:
                        player.ground_height += 2
                    torso_bobbing = not torso_bobbing
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
                    if torso_bobbing:
                        player.ground_height -= 2
                    else:
                        player.ground_height += 2
                    torso_bobbing = not torso_bobbing
                    time_since_bob = time.time()
        if -3 < player.x_vel < 3:
            # reset the leg animation
            if leg_direction == 'Left':
                player.left_leg.surface = pygame.image.load('images/leg0.png')
                player.right_leg.surface = pygame.image.load('images/leg0.png')
            else:
                player.left_leg.surface = pygame.image.load('images/rleg0.png')
                player.right_leg.surface = pygame.image.load('images/rleg0.png')
            if player.ground_height > 300:
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
        updraft_icon.update(updraft_unlocked, updraft_time)
        dash_icon.update(dash_unlocked, dash_time)

        for hud_elements in hud_sprites:
            screen.blit(hud_elements.surface, hud_elements.rect)

        player.update()

    pygame.display.flip()
    clock.tick(60)


cursor.execute('DELETE FROM stats')
conn.commit()
cursor.execute('INSERT INTO stats VALUES (?, ?, ?, ?, ?)', (player_health, int(updraft_unlocked), int(dash_unlocked),
                                                            player.x, player.y))
conn.commit()
pygame.quit()
