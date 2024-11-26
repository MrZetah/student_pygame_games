# 1 - import packages
import pygame
from pygame.locals import *
import sys
import random
import os

def main():
    pygame.font.init()
    FPS = 30
    TIMER =30
    WHITE = (255, 255, 255)
    BLACK = (0,0,0)
    RED = (255, 0, 0)
    VEL_X = -3
    VEL_Y = -6
    VEL_X1 = 3
    VEL_Y1 = -3
    VEL_X2 = 3
    VEL_Y2 = -3
    VEL_X3 = -3
    VEL_Y3 = -3
    COLOR = (20, 255, 20)
    start = 0
    summon_shield = 0
    summon_shielding = 0
    duration = 30000
    SCORE_FONT = pygame.font.SysFont('comicsans', 20)
    GAME_OVER_FONT = pygame.font.SysFont('comicsans', 100)
    GAME_START = pygame.font.SysFont('comicsans', 30)
    INSTRUCTIONS_FONT = pygame.font.SysFont('comicsans', 20)
    score = 0

    with open('highscore.txt', 'r') as file:
        high_score = int(file.read())

    win_width, win_hight = 800, 500

    pygame.init()
    window = pygame.display.set_mode((win_width, win_hight))
    pygame.display.set_caption (f'Score {score}')
    clock = pygame.time.Clock()

    BALL = pygame.image.load('Assets/box.png')
    BALL = pygame.transform.scale(BALL, (50, 50))
    window.blit(BALL, (50, 50))

    SPIKE = pygame.image.load('Assets/spike.png')
    SPIKE = pygame.transform.scale(SPIKE, (50, 50))
    window.blit(SPIKE, (50, 50))

    SHIELD = pygame.image.load('Assets/shield.png')
    SHIELD = pygame.transform.scale(SHIELD, (100, 100))
    window.blit(SHIELD, (50, 50))

    rect=[]
    rect_width, rect_height = 50, 50
    rect_x, rect_y = 700, 400
    rect_color= (8, 133, 161)
    window_rect = window.get_rect()
    center_x, center_y = window_rect.center[1], window_rect.center[0]
    RECT = pygame.Rect(center_x, center_y, rect_width, rect_height)
    rect.append(RECT)
    pygame.draw.rect(window, rect_color, RECT)

    rect_width1, rect_height1 = 50, 50
    rect_x1, rect_y1 = 100, 100
    rect_color1= (255, 255, 255)
    window_rect1 = window.get_rect()
    center_x, center_y = window_rect1.center[1], window_rect1.center[1]
    RECT1 = pygame.Rect(rect_x1, rect_y1, rect_width1, rect_height1)
    rect.append(RECT1)
    pygame.draw.rect(window, rect_color1, RECT1)

    rect_width2, rect_height2 = 50, 50
    rect_x2, rect_y2 = 428, 100
    rect_color2 = (255, 255, 255)
    window_rect2 = window.get_rect()
    center_x, center_y = window_rect.center[0], window_rect.center[1]
    RECT2 = pygame.Rect(center_x, center_y, rect_width2, rect_height2)
    rect.append(RECT2)
    pygame.draw.rect(window, rect_color2, RECT2)

    rect_width3, rect_height3 = 50, 50
    rect_x3, rect_y3 = 500, 300
    rect_color3 = (255, 255, 255)
    window_rect3 = window.get_rect()
    center_x, center_y = window_rect.center[0], window_rect.center[0]
    RECT3 = pygame.Rect(center_x, center_y, rect_width3, rect_height3)
    rect.append(RECT3)
    pygame.draw.rect(window, rect_color3, RECT3)

    rect_width4, rect_height4 = 100, 100
    rect_x4, rect_y4 = 10000, 0
    rect_color4 = (255, 255, 255)
    window_rect4 = window.get_rect()
    center_x, center_y = (1000, 1000)
    RECT4 = pygame.Rect(center_x, center_y, rect_width4, rect_height4)
    rect.append(RECT4)
    pygame.draw.rect(window, rect_color4, RECT4)


    def game_over(score, high_score):
        if score >= high_score:
            with open('highscore.txt', 'w') as file:
                file.write(str(score - 1))
        draw_text = GAME_OVER_FONT.render("Game Over", 1, WHITE)
        window.blit(draw_text, (win_width//2 - draw_text.get_width()//2, win_hight//2 - draw_text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(3000)
        return score


    start_ticks = pygame.time.get_ticks()
    should_break = False
    while pygame.time.get_ticks() - start_ticks < duration:
        if should_break:
            break
        window.fill(BLACK)
        instructions = ['Created by Ben K',
        'Press the left arrow key to move the red box up and left.',
        'Press the right arrow key to move the box down and right.',
        'Press the up arrow key to stop the block from moving.',
        "Don't get hit by the other blocks",
        'When your score goes up by 1000 you get a shield the shield will block one grey block.',
        'Press return to start.']
        for i, instruction in enumerate(instructions):
            draw_text = INSTRUCTIONS_FONT.render(instruction, 1, WHITE)
            window.blit(draw_text, (win_width//2 - draw_text.get_width()//2, 100 + i *50))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    should_break = True
                    break
        pygame.display.update()
    window.fill(BLACK)

    while True: # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                return score

        if RECT.y > win_hight - rect_height:
            RECT.y = win_hight - rect_height - 5

        if RECT.x < 0:
            VEL_X=-VEL_X

        if RECT.y < 0:
            VEL_Y=-VEL_Y

        RECT.x += VEL_X
        RECT.y += VEL_Y

        if RECT.x > win_width - rect_width:
            VEL_X=-VEL_X

        if RECT.y > win_hight - rect_height:
            VEL_Y=-VEL_Y

        RECT.x += VEL_X
        rect_y += VEL_Y
        #########
        if RECT1.x < 0:
            VEL_X1=-VEL_X1

        if RECT1.y < 0:
            VEL_Y1=-VEL_Y1

        RECT1.x += VEL_X1
        RECT1.y += VEL_Y1

        if RECT1.x > win_width - rect_width1:
            VEL_X1=-VEL_X1

        if RECT1.y > win_hight - rect_height1:
            VEL_Y1=-VEL_Y1

        RECT1.x += VEL_X1
        RECT1.y += VEL_Y1
        #######
        if RECT2.x < 0:
            VEL_X2=-VEL_X2

        if RECT2.y < 0:
            VEL_Y2=-VEL_Y2

        RECT2.x += VEL_X2
        RECT2.y += VEL_Y2

        if RECT2.x > win_width - rect_width2:
            VEL_X2=-VEL_X2

        if RECT2.y > win_hight - rect_height2:
            VEL_Y2=-VEL_Y2

        RECT2.x += VEL_X2
        RECT2.y += VEL_Y2
        ######

        if RECT3.x < 0:
            VEL_X3=-VEL_X3

        if RECT3.y < 0:
            VEL_Y3=-VEL_Y3

        RECT3.x += VEL_X3
        RECT3.y += VEL_Y3

        if RECT3.x > win_width - rect_width3:
            VEL_X3=-VEL_X3

        if RECT3.y > win_hight - rect_height3:
            VEL_Y3=-VEL_Y3

        RECT3.x += VEL_X3
        RECT3.y += VEL_Y3

        ######
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                VEL_X = 3
                VEL_Y = 6

            if event.key == pygame.K_LEFT:
                VEL_X = -3
                VEL_Y = -6

            if event.key == pygame.K_DOWN:
                summon_shield = 0

            if event.key == pygame.K_UP:
                VEL_X = 0
                VEL_Y = 0

        score += 1
        if high_score < score:
            high_score = score

        summon_shielding = score

        if summon_shielding == 1000:
            summon_shield = 1
            summon_shielding = 0

        if RECT1.colliderect(RECT) or RECT2.colliderect(RECT) or RECT3.colliderect(RECT):
            score = game_over(score, high_score)
            return score

        if RECT1.colliderect(RECT2):
            VEL_Y2=-VEL_Y2
            VEL_X2=-VEL_X2
            VEL_Y1=-VEL_Y1
            VEL_X1=-VEL_X1

        if RECT1.colliderect(RECT3):
            VEL_Y3=-VEL_Y3
            VEL_X3=-VEL_X3
            VEL_Y1=-VEL_Y1
            VEL_X1=-VEL_X1

        if RECT2.colliderect(RECT3):
            VEL_Y2=-VEL_Y2
            VEL_X2=-VEL_X2
            VEL_Y3=-VEL_Y3
            VEL_X3=-VEL_X3
 #################
        if RECT4.colliderect(RECT1):
            VEL_Y1=-VEL_Y1
            VEL_X1=-VEL_X1
            summon_shield = 0

        if RECT4.colliderect(RECT2):
            VEL_Y2=-VEL_Y2
            VEL_X2=-VEL_X2
            summon_shield = 0

        if RECT4.colliderect(RECT3):
            VEL_Y3=-VEL_Y3
            VEL_X3=-VEL_X3
            summon_shield = 0

        window.fill(BLACK)

        '''score_text = SCORE_FONT.render("Score: " + str(score), 1, WHITE)
        window.blit(score_text, (0, 0))'''

        pygame.display.set_caption (f'Score {score}       High Score {high_score}')

        if summon_shield == 1:
            RECT4.center = RECT.center
            window.blit(SHIELD, RECT4)

        if summon_shield == 0:
            RECT4.x = 1000

        window.blit(BALL, RECT)

        window.blit(SPIKE, RECT1)
        window.blit(SPIKE, RECT2)
        window.blit(SPIKE, RECT3)
        pygame.display.update()

        clock.tick (FPS)

if __name__ == "__main__":
    main()
