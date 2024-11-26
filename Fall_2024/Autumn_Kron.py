# Write your code here :-)
# Pygame Template

# 1 - import packages
import pygame
from pygame.locals import *
import sys
import random
import time
pygame.font.init()
pygame.init()

def main():
    #2 - Define constants
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    WINDOW_WIDTH = 640
    WINDOW_HEIGHT = 480
    FPS = 30
    counter = 0

    BLUE = (0, 0, 255)
    PLAYER_SIZE = 30
    JUMP_HEIGHT = 20
    UP_GRAVITY = 4
    DOWN_GRAVITY = 4
    vel_y = 0
    PLAYER_VELOCITY = 6
    pipe_list = []

    GREEN = (0, 225,0)
    TOP_PIPE_WIDTH, TOP_PIPE_HEIGHT = 40, 340
    BOTTOM_PIPE_WIDTH, BOTTOM_PIPE_HEIGHT = 40, 340
    VEL = 3

    MY_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(MY_EVENT, 1500)
    counter = 0

    score_counter = -130
    score = score_counter//60
    SCORE_FONT = pygame.font.SysFont('comicsans', 20)


    GAME_OVER_FONT = pygame.font.SysFont('comicsans', 100)

    #3 - Initialize the world
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    # Display Instructions

    duration = 10000
    INSTRUCTIONS_FONT = pygame.font.SysFont('comicsans', 20)
    start_ticks = pygame.time.get_ticks()
    should_break = False
    while pygame.time.get_ticks() - start_ticks < duration:
        if should_break:
            break
        window.fill(WHITE)
        instructions = ['Created by Autumn Kron',
        'Press enter to skip at any time',
        'Try to not let your bird hit the pipes or the edges',
        'Press the space bar to move the bird']
        for i, instruction in enumerate(instructions):
            draw_text = INSTRUCTIONS_FONT.render(instruction, 1, BLACK)
            window.blit(draw_text, (WINDOW_WIDTH//2 - draw_text.get_width()//2, 100 + i *50))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    should_break = True
                    break
        pygame.display.update()
    window.fill(BLACK)

    #4 - Load assets: images, sounds, etc.
    player_1 = pygame.image.load('Assets/bird.png')
    player_1 = pygame.transform.scale(player_1,(50,55))

    BACKGROUND = pygame.transform.scale( pygame.image.load ('Assets/background.png'), (WINDOW_WIDTH, WINDOW_HEIGHT))


    TOP_PIPE_IMAGE = pygame.image.load('Assets/tube_1.png')
    TOP_PIPE_IMAGE = pygame.transform.rotate(pygame.transform.scale(TOP_PIPE_IMAGE, (TOP_PIPE_WIDTH, TOP_PIPE_HEIGHT)),0)
    BOTTOM_PIPE_IMAGE = pygame.image.load('Assets/tube_1.png')
    BOTTOM_PIPE_IMAGE = pygame.transform.rotate(pygame.transform.scale(BOTTOM_PIPE_IMAGE, (BOTTOM_PIPE_WIDTH, BOTTOM_PIPE_HEIGHT)), 180)

   #5 - Initialize variables
    play = False
    window_rect = window.get_rect()
    center_x, center_y = window_rect.center[1], window_rect.center[1]
    player = pygame.Rect(center_x, center_y,PLAYER_SIZE, PLAYER_SIZE)




    def game_over():
        draw_text = GAME_OVER_FONT.render("Game Over", 1, WHITE)
        window.blit(draw_text, (WINDOW_WIDTH//2 - draw_text.get_width()//2, WINDOW_HEIGHT//2 - draw_text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(5000)



    #6 - Define functions


    #7 - Loop forever
    while True:

        #8 Check for and handle events
        for event in pygame.event.get():
            #Check to see if user has quit the game
            if event.type == pygame.QUIT:
                return score

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return score
                if event.key == pygame.K_p:
                    play = not play
                if event.key in [pygame.K_SPACE]:
                    play = True   # Start Game
            #Check for other 'game' related events (collisions, key presses, mouse clicks, etc.)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    vel_y = -JUMP_HEIGHT

        if player.y < 0 or player.y + PLAYER_SIZE == WINDOW_HEIGHT:
            game_over()
            return score
        for pipes in pipe_list:
            if player.colliderect(pipes[0]) or player.colliderect(pipes[1]):
                game_over()
                return score


        window.fill(BLACK)

        #9 - Do any "per frame" actions (move objects, add or remove items)

        if score_counter < 0:
            score = 0
        if play:
            player.y += vel_y
            if player.y < WINDOW_HEIGHT - PLAYER_SIZE and vel_y < 0 :
                vel_y += UP_GRAVITY
            if player.y < WINDOW_HEIGHT - PLAYER_SIZE and vel_y >= 0:
                vel_y += DOWN_GRAVITY
            if player.y >= WINDOW_HEIGHT - PLAYER_SIZE:
                vel_y = 0
                player.y = WINDOW_HEIGHT - PLAYER_SIZE


            #tube
            if counter > 60:

                TOP_PIPE_X, TOP_PIPE_Y = 640, random.randint(-300,-30)
                BOTTOM_Y = TOP_PIPE_Y + 480
                BOTTOM_PIPE_X, BOTTOM_PIPE_Y = 640, BOTTOM_Y

                TOP_PIPE_RECT = pygame.Rect((TOP_PIPE_X, TOP_PIPE_Y, TOP_PIPE_WIDTH, TOP_PIPE_HEIGHT))
                BOTTOM_PIPE_RECT = pygame.Rect((BOTTOM_PIPE_X, BOTTOM_PIPE_Y, BOTTOM_PIPE_WIDTH, BOTTOM_PIPE_HEIGHT))

                pipe_list.append((TOP_PIPE_RECT, BOTTOM_PIPE_RECT))


                counter = 0
            #was 200
            if score_counter > 70:
                score = score_counter // 65


            for items in pipe_list:
                items[0].x -= VEL
                items[1].x -= VEL



        #10 - Clear the window
        window.fill(BLACK)
        window.blit(BACKGROUND, (0,0))
        #11 - Draw all window elements
        for pipes in pipe_list:
            pygame.draw.rect(window, GREEN, pipes[0])
            pygame.draw.rect(window, GREEN, pipes[1])

            window.blit(TOP_PIPE_IMAGE, pipes[0])
            window.blit(BOTTOM_PIPE_IMAGE, pipes[1])

        score_text = SCORE_FONT.render("Score: " + str(score), 1, WHITE)
        window.blit(score_text, (10, 10))
        window.blit(player_1, (player.x-9, player.y-10, player.width, player.height))


        #12 - Update the window
        pygame.display.update()

        #13 - Set frame rate to slow things down
        clock.tick(FPS)
        counter += 1
        score_counter +=1




if __name__ == "__main__":
    main()


