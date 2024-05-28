# Pygame Template

# 1 - import packages
import pygame
from pygame.locals import *
import sys
pygame.font.init()
lives = 3

def main(lives):
    #2 - Define constants
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    ORANGE = (255, 165, 0)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    PURPLE = (160, 32, 240)

    VEL_X = 10
    VEL_Y = 10
    WINDOW_WIDTH = 1440
    WINDOW_HEIGHT = 760
    FPS = 30
    fake_loco = 0
    real_loco = 0
    WORLDS = 4
    lives = lives

    SCORE_FONT = pygame.font.SysFont('comicsans', 20)

    background = pygame.Rect((0,0), (1440, 760))

    player = pygame.Rect((10, 639), (40, 40))

    prize = pygame.Rect((1400, 660), (40, 40))

    prize2 = pygame.Rect((200, 660), (40, 40))

    floor = pygame.Rect((0, 700), (0, 700))


    #3 - Initialize the world
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    player_width, player_height = 40, 60

    GAME_OVER_FONT = pygame.font.SysFont('comicsans', 100)

    player_x, player_y = 10, 680

    floor_width, floor_height = 1440, 80
    floor_x, floor_y = 0, 700

    win_block_width, win_block_height = 40, 40
    win_block_x, win_block_y = 1400, 660

    win_block2_width, win_block2_height = 40, 40
    win_block2_x, win_block2_y = 200, 660

    bird_width, bird_height = 250, 230
    bird_x, bird_y = 200, 200

    worm_width, worm_height = 150, 230
    worm_x, worm_y = 200, 200

    bat_width, bat_height = 160, 100
    bat_x, bat_y = 200, 200


    ###### World 1 Objects ######

    bird_1 = pygame.Rect((200, 100), (250, 230))
    bird_2 = pygame.Rect((450, 100), (250, 230))
    bird_3 = pygame.Rect((700, 100), (250, 230))
    bird_4 = pygame.Rect((950, 100), (250, 230))

    ###### World 2 Objects ######

    worm_1 = pygame.Rect((200, 700), (worm_width, worm_height))
    worm_2 = pygame.Rect((450, 700), (worm_width, worm_height))
    worm_3 = pygame.Rect((700, 700), (worm_width, worm_height))
    worm_4 = pygame.Rect((950, 700), (worm_width, worm_height))

    ###### World 3 Objects ######

    bat_1 = pygame.Rect((250, 0), (bat_width, bat_height))
    bat_2 = pygame.Rect((500, 0), (bat_width, bat_height))
    bat_3 = pygame.Rect((750, 0), (bat_width, bat_height))
    bat_4 = pygame.Rect((1000, 0), (bat_width, bat_height))
    worm_5 = pygame.Rect((1250, 800), (worm_width, worm_height))

    #4 - Load assets: images, sounds, etc.

    suit_man = pygame.image.load('images/suit_man.png')
    suit_man = pygame.transform.scale(suit_man, (player_width, player_height))

    trophy = pygame.image.load('images/trophy.png')
    trophy = pygame.transform.scale(trophy, (win_block_width, win_block_height))

    grass_floor = pygame.image.load('images/grass_floor.png')
    grass_floor = pygame.transform.scale(grass_floor, (floor_width, floor_height))

    sand_floor = pygame.image.load('images/sand.png')
    sand_floor = pygame.transform.scale(sand_floor, (floor_width, floor_height))

    stone_floor = pygame.image.load('images/stone.png')
    stone_floor = pygame.transform.scale(stone_floor,(floor_width, floor_height))

    hell_floor = pygame.image.load('images/hell_floor.png')
    hell_floor = pygame.transform.scale(hell_floor,(floor_width, floor_height))

    sky = pygame.image.load('images/sky.png')
    sky = pygame.transform.scale(sky, (WINDOW_WIDTH, WINDOW_HEIGHT))

    desert = pygame.image.load('images/desert.png')
    desert = pygame.transform.scale(desert, (WINDOW_WIDTH, WINDOW_HEIGHT))

    cave = pygame.image.load('images/cave.png')
    cave = pygame.transform.scale(cave, (WINDOW_WIDTH, WINDOW_HEIGHT))

    hell = pygame.image.load('images/hell.png')
    hell = pygame.transform.scale(hell, (WINDOW_WIDTH, WINDOW_HEIGHT))

    bird = pygame.image.load('images/bird.png')
    bird = pygame.transform.scale(bird, (bird_width, bird_height))

    worm = pygame.image.load('images/worm.png')
    worm = pygame.transform.scale(worm, (worm_width, worm_height))

    bat = pygame.image.load('images/bat.png')
    bat = pygame.transform.scale(bat, (bat_width, bat_height))

    #5 - Initialize variables
    def game_win():
        draw_text = GAME_OVER_FONT.render("You Won!", 1, WHITE)
        window.blit(draw_text, (WINDOW_WIDTH//2 - draw_text.get_width()//2, WINDOW_HEIGHT//2 - draw_text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(5000)
        return

    def game_lost(lives):
        draw_text = GAME_OVER_FONT.render("You Lose.", 1, BLACK)
        window.blit(draw_text, (WINDOW_WIDTH//2 - draw_text.get_width()//2, WINDOW_HEIGHT//2 - draw_text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(3000)
        lives -= 1
        if lives > 0:
            main(lives)
        else:
            return

    def under_world(lives):
        window.fill(BLACK)
        window.blit(hell, background)
        window.blit(suit_man, player)
        window.blit(hell_floor, floor)
        window.blit(trophy, prize2)
        score_text = SCORE_FONT.render("lives: " + str(lives), 1, WHITE)
        window.blit(score_text, (10, 10))
        if player.colliderect(prize2):
            game_win()
            return False

    def world_1(lives):
        global bird_1_drop
        window.fill(BLACK)
        window.blit(sky, background)
        window.blit(suit_man, player)
        window.blit(grass_floor, floor)
        window.blit(bird, bird_1)
        window.blit(bird, bird_2)
        window.blit(bird, bird_3)
        window.blit(bird, bird_4)
        score_text = SCORE_FONT.render("lives: " + str(lives), 1, WHITE)
        window.blit(score_text, (10, 10))
        if bird_1.colliderect(player):
            game_lost(lives)
            return False
        if bird_2.colliderect(player):
            game_lost(lives)
            return False
        if bird_3.colliderect(player):
            game_lost(lives)
            return False
        if bird_4.colliderect(player):
            game_lost(lives)
            return False

        if real_loco > 30:
            bird_1.y += 10
            bird_1.x += 10

        if real_loco > 60:
            bird_2.y += 10
            bird_2.x += 10

        if real_loco > 80:
            bird_3.y += 10
            bird_3.x += 10

        if real_loco > 100:
            bird_4.y += 10
            bird_4.x += 10


    def world_2(lives):
        window.fill(BLACK)
        window.blit(desert, background)
        window.blit(suit_man, player)
        window.blit(sand_floor, floor)
        window.blit(worm, worm_1)
        window.blit(worm, worm_2)
        window.blit(worm, worm_3)
        window.blit(worm, worm_4)
        score_text = SCORE_FONT.render("lives: " + str(lives), 1, WHITE)
        window.blit(score_text, (10, 10))
        if worm_1.colliderect(player):
            game_lost(lives)
            return False
        if worm_2.colliderect(player):
            game_lost(lives)
            return False
        if worm_3.colliderect(player):
            game_lost(lives)
            return False
        if worm_4.colliderect(player):
            game_lost(lives)
            return False

        if real_loco > 153:
            worm_1.y -= 30

        if real_loco > 180:
            worm_2.y -= 30

        if real_loco > 200:
            worm_3.y -= 30

        if real_loco > 230:
            worm_4.y -= 30

    def world_3(lives):
        window.fill(BLACK)
        window.blit(cave, background)
        window.blit(suit_man, player)
        window.blit(stone_floor, floor)
        window.blit(trophy, prize)
        window.blit(bat, bat_1)
        window.blit(bat, bat_2)
        window.blit(bat, bat_3)
        window.blit(bat, bat_4)
        window.blit(worm, worm_5)
        score_text = SCORE_FONT.render("lives: " + str(lives), 1, WHITE)
        window.blit(score_text, (10, 10))
        if bat_1.colliderect(player):
            game_lost(lives)
            return False
        if bat_2.colliderect(player):
            game_lost(lives)
            return False
        if bat_3.colliderect(player):
            game_lost(lives)
            return False
        if bat_4.colliderect(player):
            game_lost(lives)
            return False
        if worm_5.colliderect(player):
            game_lost(lives)
            return False
        if player.colliderect(prize):
            game_win()
            return False
        if real_loco > 300:
            bat_1.y += 40

        if real_loco > 340:
            bat_2.y += 30

        if real_loco > 350:
            bat_3.y += 30

        if real_loco > 394:
            bat_4.y += 30

        if real_loco > 408:
            worm_5.y -= 40

    keep_playing = None
    #6 - Loop forever
    while True:  #  main game loop
        if real_loco < 0:
            keep_playing = under_world(lives)
            if keep_playing == False:
                return

        elif real_loco < 140:
            keep_playing = world_1(lives)
            if keep_playing == False:
                return

        elif real_loco > 140 and real_loco < 287:
            keep_playing = world_2(lives)
            if keep_playing == False:
                return

        elif real_loco > 287:
            keep_playing = world_3(lives)
            if keep_playing == False:
                return

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and player.x < WINDOW_WIDTH*WORLDS:
            player.x += VEL_X
            player.x = player.x % WINDOW_WIDTH
            real_loco += 1

        if keys[pygame.K_LEFT]:
            player.x -= VEL_X
            player.x = player.x % WINDOW_WIDTH
            real_loco -= 1


            #Check for other 'game' related events (collisions, key presses, mouse clicks, etc.)


        #8 - Do any "per frame" actions (move objects, add or remove items)

        #9 - Clear the window



        #10 - Draw all window elements

        #11 - Update the window
        pygame.display.update()

        #12 - Set frame rate to slow things down
        clock.tick(FPS)

if __name__ == "__main__":
    main(lives)
