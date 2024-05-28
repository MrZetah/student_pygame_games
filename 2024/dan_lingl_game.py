# Write your code here :-)
# 1 - import packages
import pygame
from pygame.locals import *
import sys
import random
import os
import math
pygame.font.init()


def main():
    #2 - Define constants
    #FPS/Colors
    FPS = 30
    BLACK = (0,0,0)
    RED = (255, 0, 0)

    #Window Stuff
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 720

    #Enviroment
    GROUND = 625
    BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Background.jpeg')), (WINDOW_WIDTH, WINDOW_HEIGHT))
    #Original Dimensions = 309 x 163
    OBSTABCLE_WIDTH = 75
    OBSTABCLE_HEIGHT = 25
    GROUND_OBSTACLE_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Gorund_Obstacle.png')), (OBSTABCLE_WIDTH, OBSTABCLE_HEIGHT))
    SKY_OBSTACLE_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Sky_Obstacle.png')), (OBSTABCLE_WIDTH, OBSTABCLE_HEIGHT))
    GROUND_OBSTACLE_X, GROUND_OBSTACLE_Y = WINDOW_WIDTH, GROUND - 50
    SKY_OBSTACLE_X, SKY_OBSTACLE_Y = WINDOW_WIDTH, GROUND - 200


    #Player Stuff
    PLAYER_WIDTH = 75
    PLAYER_HEIGHT = 150
    START_X = 100
    START_Y = GROUND - PLAYER_HEIGHT

    #Movement Stuff
    VEL_X = 15
    JUMP_HEIGHT = 30
    UP_GRAVITY = 5
    DOWN_GRAVITY = 2
    VELOCITY = 10

    GAME_OVER_FONT = pygame.font.SysFont('comicsans', 100)


    #3 - Initialize the world



    #4 - Load assets: images, sounds, etc.

    #5 - Initialize variables
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    scroll = 0
    tiles = math.ceil(WINDOW_WIDTH / BACKGROUND.get_width()) + 1
    clock = pygame.time.Clock()
    player_image = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Player_Standin.png')), (PLAYER_WIDTH, PLAYER_HEIGHT))
    player_rect = player_image.get_rect()
    player_rect.x = START_X
    player_rect.y = START_Y
    ground_obstacle = GROUND_OBSTACLE_IMAGE.get_rect()
    ground_obstacle.x = GROUND_OBSTACLE_X
    ground_obstacle.y = GROUND_OBSTACLE_Y
    sky_obstacle = SKY_OBSTACLE_IMAGE.get_rect()
    sky_obstacle.x = SKY_OBSTACLE_X
    sky_obstacle.y = SKY_OBSTACLE_Y
    vel_y = 0
    keys_pressed = pygame.key.get_pressed()
    frames = 0
    ground_obstacles = []
    sky_obstacles = []
    font=pygame.freetype.SysFont(None, 34)
    font.origin=True


    #5.5 Functions

    def player_move(keys_pressed, player_rect):
        if keys_pressed[pygame.K_a] and player_rect.x - VEL_X > 0:
                player_rect.x -= VEL_X
        if keys_pressed[pygame.K_d] and player_rect.x + VEL_X + player_rect.width < WINDOW_WIDTH:
                player_rect.x += VEL_X

    def add_ground_obstacle(GROUND_OBSTACLE_IMAGE):
        x = random.randint(0,1)
        ground_obstacle = GROUND_OBSTACLE_IMAGE.get_rect()
        ground_obstacle.x = GROUND_OBSTACLE_X
        ground_obstacle.y = GROUND_OBSTACLE_Y

        return ground_obstacle

    def add_sky_obstacle(SKY_OBSTACLE_IMAGE):
        sky_obstacle = SKY_OBSTACLE_IMAGE.get_rect()
        sky_obstacle.x = SKY_OBSTACLE_X
        sky_obstacle.y = SKY_OBSTACLE_Y

        return sky_obstacle

    def add_obstacle():
        obstacle_1 = pygame.Rect(15, -100, 200, 50)
        obstacle_2 = pygame.Rect(240, -100, 200, 50)
        obstacle_3 = pygame.Rect(175, -100, 100, 25)
        x = random.randint(0,2)
        if x == 0:
            return obstacle_1
        elif x == 1:
            return obstacle_2
        else:
            return obstacle_3

    def game_over(minutes, seconds, millis):
        window.blit(BACKGROUND, (0, 0))
        draw_text = GAME_OVER_FONT.render("Game Over", 1, BLACK)
        #print_score = font.render(f'You Survived + {out}')
        window.blit(draw_text, (WINDOW_WIDTH//2 - draw_text.get_width()//2, WINDOW_HEIGHT//2 - draw_text.get_height()//2))
        #window.blit(print_score, (WINDOW_WIDTH//2 - draw_text.get_width()//2, WINDOW_HEIGHT//2 - draw_text.get_height()//2 - draw_text.get_height()//2))
        pygame.display.update()
        score = round(minutes + seconds/60 + millis/60000, 5)
        pygame.time.delay(5000)
        return score

    #6 - Loop forever
    while True:
        #Scroll the Screen
        i = 0
        while(i < tiles):
            window.blit(BACKGROUND, (BACKGROUND.get_width()*i + scroll, 0))
            i += 1
            # FRAME FOR SCROLLING
            scroll -= 6

            # RESET THE SCROLL FRAME
            if abs(scroll) > BACKGROUND.get_width():
                scroll = 0

        #7 Check for and handle events
        for event in pygame.event.get():
            #Check to see if user has quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #Press the 'q' key as an option to quit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            #Check for other 'game' related events (collisions, key presses, mouse clicks, etc.)
                if event.key == pygame.K_w and player_rect.y == GROUND - player_rect.height:  # Check to see if player is on ground before jumping
                    vel_y = -JUMP_HEIGHT


        #8 - Do any "per frame" actions (move objects, add or remove items)
        #Timer
        ticks = pygame.time.get_ticks()
        millis = ticks%1000
        seconds = int(ticks/1000 % 60)
        minutes = int(ticks/60000 % 24)
        out = '{minutes:02d}:{seconds:02d}:{millis}'.format(minutes=minutes, millis=millis, seconds=seconds)
        score = minutes + seconds/60 + millis/60000
        font.render_to(window, (100, 100), out, pygame.Color(RED))

        #Jump Physics
        player_rect.y += vel_y
        if player_rect.y < GROUND - player_rect.height and vel_y < 0:  # if the player is in the air and moving up, decrease the y velocity by the "up gravity" value
            vel_y += UP_GRAVITY
        if player_rect.y < GROUND - player_rect.height and vel_y >= 0:  # if the player is in the air and moving down, increase the y velocity by the "down gravity" value
            vel_y += DOWN_GRAVITY
        if player_rect.y >= GROUND - player_rect.height:  # When the player hits the ground, set the y velocity to 0 to stop it.
            vel_y = 0
            player_rect.y = GROUND - player_rect.height  # This line corrects for any occurence where the player moves just below the bottom of the screen in a si

        #Obsticles
        frames += 1
        x = random.randint(0,1)
        if frames > random.randint(45, 100):
            if x == 0:
                ground_obstacles.append(add_ground_obstacle(GROUND_OBSTACLE_IMAGE))
                frames = 0
            else:
                sky_obstacles.append(add_sky_obstacle(SKY_OBSTACLE_IMAGE))
                frames = 0

        for obstacle in ground_obstacles:
            if player_rect.colliderect(obstacle):
                score = game_over(minutes, seconds, millis)
                print(score)
                return score

        for obstacle in sky_obstacles:
            if player_rect.colliderect(obstacle):
                game_over(minutes, seconds, millis)
                print(score)
                return score

        keys_pressed = pygame.key.get_pressed()
        player_move(keys_pressed, player_rect)


        #9 - Clear the window

        #10 - Draw all window elements


        for obstacle in ground_obstacles:
            obstacle.x -= VELOCITY
            window.blit(GROUND_OBSTACLE_IMAGE, obstacle)

            if obstacle.x + obstacle.width < 0:
                ground_obstacles.remove(obstacle)

        for obstacle in sky_obstacles:
            obstacle.x -= VELOCITY
            window.blit(SKY_OBSTACLE_IMAGE, obstacle)

            if obstacle.x + obstacle.width < 0:
                sky_obstacles.remove(obstacle)



        window.blit(player_image, player_rect)


        #11 - Update the window
        pygame.display.update()

        #12 - Set frame rate to slow things down
        clock.tick(FPS)

if __name__ == "__main__":
    main()
