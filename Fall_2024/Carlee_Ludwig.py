# Snake Version 2

# 1 - import packages
import pygame
from pygame.locals import *
import sys
import random
pygame.font.init()

def main():
    #2 - Define constants
    BLACK = (204, 153, 255)
    GREEN = (0, 0, 225)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 700
    FPS = 7
    tron1_WIDTH_HEIGHT = 18
    GAP = 0
    SCORE_FONT = pygame.font.SysFont('comicsans', 40)   #Create variables with font information for text
    GAME_OVER_FONT = pygame.font.SysFont('comicsans', 100)
    direction = "DOWN"
    direction2 = "UP"

    #3 - Initialize the world
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Tron')
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
        instructions = ['Created by Carlee Ludwig',
        'Press enter to skip at any time',
        'P1-Blue, use keys W,S,A,D',
        'P2-Red, use arrow keys.',
        'Running into the wall or yourself will make you lose',
        'Avoid the line drawn by your opponent']
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

    #5 - Initialize variables
    play = False
    tron1 = []
    tron2 = []

    window_rect = window.get_rect()
    center_x, center_y = window_rect.center[0], window_rect.center[1]
    tron1_rect = pygame.Rect(center_x+200, center_y, tron1_WIDTH_HEIGHT, tron1_WIDTH_HEIGHT)
    tron2_rect = pygame.Rect(center_x-200, center_y, tron1_WIDTH_HEIGHT, tron1_WIDTH_HEIGHT)

    tron1.append(tron1_rect)
    tron2.append(tron2_rect)

    pygame.draw.rect(window, RED, tron1_rect)
    pygame.draw.rect(window, GREEN, tron2_rect)



    pygame.display.update()

    def game_over(text):
        draw_text = GAME_OVER_FONT.render(text, 1, WHITE)
        window.blit(draw_text, (WINDOW_WIDTH//2 - draw_text.get_width()//2, WINDOW_HEIGHT//2 - draw_text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(5000)


    #6 - Loop forever
    while True:

        #7 Check for and handle events
        for event in pygame.event.get():
            #Check to see if user has quit the game
            if event.type == pygame.QUIT:
                return
            #Press the 'q' key as an option to quit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_p:
                    play = not play
                #Check to see if any of the direction keys have been pressed
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                    play = True   # Start Game
                    # Set direction of Tron1
                    if event.key == pygame.K_UP and direction != 'DOWN':
                        if len(tron1) == 1:
                            direction = 'UP'
                        else:
                            if tron1[-1].x != tron1[-2].x:
                                direction = 'UP'
                    if event.key == pygame.K_DOWN and direction != 'UP':
                        if len(tron1) == 1:
                            direction = 'DOWN'
                        else:
                            if tron1[-1].x != tron1[-2].x:
                                direction = 'DOWN'
                    if event.key == pygame.K_LEFT and direction != 'RIGHT':
                        if len(tron1) == 1:
                            direction = 'LEFT'
                        else:
                            if tron1[-1].y != tron1[-2].y:
                                direction = 'LEFT'
                    if event.key == pygame.K_RIGHT and direction != 'LEFT':
                        if len(tron1) == 1:
                            direction = 'RIGHT'
                        else:
                            if tron1[-1].y != tron1[-2].y:
                                direction = 'RIGHT'

                    # Set direction of Tron2
                    if event.key == pygame.K_w and direction2 != 'DOWN':
                        if len(tron2) == 1:
                            direction2 = 'UP'
                        else:
                            if tron2[-1].x != tron2[-2].x:
                                direction2 = 'UP'
                    if event.key == pygame.K_s and direction2 != 'UP':
                        if len(tron2) == 1:
                            direction2 = 'DOWN'
                        else:
                            if tron2[-1].x != tron2[-2].x:
                                direction2 = 'DOWN'
                    if event.key == pygame.K_d and direction2 != 'LEFT':
                        if len(tron2) == 1:
                            direction2 = 'RIGHT'
                        else:
                            if tron2[-1].y != tron2[-2].y:
                                direction2 = 'RIGHT'
                    if event.key == pygame.K_a and direction2 != 'RIGHT':
                        if len(tron2) == 1:
                            direction2 = 'LEFT'

                        else:
                            if tron2[-1].y != tron2[-2].y:
                                direction2 = 'LEFT'

        #Check for other 'game' related events (collisions, key presses, mouse clicks, etc.)
        # Check to see if the head of the snake collides with a dot
        for body_square in tron1[0:-1]:
            if body_square.colliderect(tron1[-1]):
                game_over('Red Wins!!!')
                return
        for body_square in tron2[0:-1]:
            if body_square.colliderect(tron2[-1]):
                game_over('Blue Wins!!!')
                return
        for body_square in tron2:
            if body_square.colliderect(tron1[-1]):
                game_over('Blue Wins!!!')
                return
        for body_square in tron1:
            if body_square.colliderect(tron2[-1]):
                game_over('Red Wins!!!')
                return

        # Check to see if snake hits any of the walls
        if tron1[-1].x < 0 or tron1[-1].x > WINDOW_WIDTH - tron1_WIDTH_HEIGHT:
            game_over('Blue Wins!!!')
            return
        if tron1[-1].y < 0 or tron1[-1].y > WINDOW_HEIGHT - tron1_WIDTH_HEIGHT:
            game_over('Blue Wins!!!')
            return
        # Check to see if snake collides with itself
        if tron2[-1].x < 0 or tron2[-1].x > WINDOW_WIDTH - tron1_WIDTH_HEIGHT:
            game_over('Red Wins!!!')
            return
        if tron2[-1].y < 0 or tron2[-1].y > WINDOW_HEIGHT - tron1_WIDTH_HEIGHT:
            game_over('Red Wins!!!')
            return


        if play:
            #8 - Do any "per frame" actions (move objects, add or remove items)
            if direction == 'RIGHT':
                # Move Right
                tron1_rect_add = pygame.Rect(tron1[-1].x + tron1_WIDTH_HEIGHT + GAP, tron1[-1].y, tron1_WIDTH_HEIGHT, tron1_WIDTH_HEIGHT)
            if direction == 'LEFT':
                # Move LEFT
                tron1_rect_add = pygame.Rect(tron1[-1].x - tron1_WIDTH_HEIGHT - GAP, tron1[-1].y, tron1_WIDTH_HEIGHT, tron1_WIDTH_HEIGHT)
            if direction == 'UP':
                # Move UP
                tron1_rect_add = pygame.Rect(tron1[-1].x, tron1[-1].y - tron1_WIDTH_HEIGHT - GAP, tron1_WIDTH_HEIGHT, tron1_WIDTH_HEIGHT)
            if direction == 'DOWN':
                # Move UP
                tron1_rect_add = pygame.Rect(tron1[-1].x, tron1[-1].y + tron1_WIDTH_HEIGHT + GAP, tron1_WIDTH_HEIGHT, tron1_WIDTH_HEIGHT)


            tron1.append(tron1_rect_add)

            #8 - Do any "per frame" actions (move objects, add or remove items)
            if direction2 == 'RIGHT':
                # Move Right
                tron2_rect_add = pygame.Rect(tron2[-1].x + tron1_WIDTH_HEIGHT + GAP, tron2[-1].y, tron1_WIDTH_HEIGHT, tron1_WIDTH_HEIGHT)
            if direction2 == 'LEFT':
                # Move LEFT
                tron2_rect_add = pygame.Rect(tron2[-1].x - tron1_WIDTH_HEIGHT - GAP, tron2[-1].y, tron1_WIDTH_HEIGHT, tron1_WIDTH_HEIGHT)
            if direction2 == 'UP':
                # Move UP
                tron2_rect_add = pygame.Rect(tron2[-1].x, tron2[-1].y - tron1_WIDTH_HEIGHT - GAP, tron1_WIDTH_HEIGHT, tron1_WIDTH_HEIGHT)
            if direction2 == 'DOWN':
                # Move UP
                tron2_rect_add = pygame.Rect(tron2[-1].x, tron2[-1].y + tron1_WIDTH_HEIGHT + GAP, tron1_WIDTH_HEIGHT, tron1_WIDTH_HEIGHT)

            tron2.append(tron2_rect_add)

            #9 - Clear the window
            window.fill(BLACK)

            #10 - Draw all window elements

            for tron1_square in tron1:
                pygame.draw.rect(window, RED, tron1_square)
            for tron2_square in tron2:
                pygame.draw.rect(window, GREEN, tron2_square)

            #11 - Update the window
            pygame.display.update()

            #12 - Set frame rate to slow things down
            clock.tick(FPS)

if __name__ == "__main__":
    main()

