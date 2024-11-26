# 1 - import packages
import pygame
from pygame.locals import *
import sys
import random
pygame.font.init()
pygame.display.set_caption("Space Escape")

def main():
    #2 - Define constants
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 550
    VEL = 15
    SPACESHIP_VEL = 12
    FPS = 60
    SPACESHIP_WIDTH = 90
    SPACESHIP_HEIGHT = 75
    GAME_OVER_FONT = pygame.font.SysFont('comicsans', 100)
    SCORE_FONT = pygame.font.SysFont('comicsans', 20)

    #3 - Initialize the world
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    window_rect = window.get_rect()

    # Display Instructions
    duration = 100000
    INSTRUCTIONS_FONT = pygame.font.SysFont('comicsans', 20)
    start_ticks = pygame.time.get_ticks()
    should_break = False
    while pygame.time.get_ticks() - start_ticks < duration:
        if should_break:
            break
        window.fill(WHITE)
        instructions = ['Created by Eric Hernandez',
        'Press enter to skip the instructions.',
        'Use the Up and Down arrow keys to move the spaceship.',
        'You die if you collide with the meteors or aliens.',
        'Try to get a high score.',
        'Press q to quit at any time.']
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
    SPACESHIP = pygame.image.load('Assets/spaceship_red.png')
    SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
        SPACESHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

    SPACE = pygame.image.load('Assets/Space2.png')
    SPACE = pygame.transform.scale(SPACE, (WINDOW_WIDTH, WINDOW_HEIGHT))

    large_obstacle = pygame.image.load("Assets/Meteor.png")
    large_obstacle = pygame.transform.scale(large_obstacle, (200, 50))

    small_obstacle = pygame.image.load("Assets/Alien.png")
    small_obstacle = pygame.transform.scale(small_obstacle, (40, 70))

    #5 - Initialize variables
    obstacles = []
    score = 0
    frames = 0
    moving_up = False
    moving_down = False
    spaceship_rect = SPACESHIP.get_rect()
    spaceship_rect.x = 20
    spaceship_rect.y = WINDOW_HEIGHT - SPACESHIP_HEIGHT - 245

    #5.5 Create functions
    def game_over():
        draw_text = GAME_OVER_FONT.render("Game Over", 1, WHITE)
        window.blit(draw_text, (WINDOW_WIDTH//2 - draw_text.get_width()//2, WINDOW_HEIGHT//2 - draw_text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(5000)


    def add_obstacle():
                                # x,   y,   w,  h
        obstacle_1 = pygame.Rect(800, 50, 200, 50)
        obstacle_2 = pygame.Rect(870, 130, 40, 70)
        obstacle_3 = pygame.Rect(800, 250, 200, 50)
        obstacle_4 = pygame.Rect(870, 330, 40, 70)
        obstacle_5 = pygame.Rect(800, 450, 200, 50)
        x = random.randint(0,4)
        if x == 0:
            return obstacle_1
        elif x == 1:
            return obstacle_2
        elif x == 2:
            return obstacle_3
        elif x == 3:
            return obstacle_4
        else:
            return obstacle_5

    #6 - Loop forever
    while True:

        #7 Check for and handle events
        for event in pygame.event.get():
            #Check to see if user has quit the game
            if event.type == pygame.QUIT:
                return score
            #Press the 'q' key as an option to quit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return score
            #Check left and right keys to move spaceship side to side
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    moving_up = True
                if event.key == pygame.K_DOWN:
                    moving_down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    moving_up = False
                if event.key == pygame.K_DOWN:
                    moving_down = False

        #8 - Do any "per frame" actions (move objects, add or remove items)
        frames += 1
        if frames > random.randint(20, max(30, 100-score)):
            obstacles.append(add_obstacle())
            frames = 0

        if moving_up == True and spaceship_rect.y > 10:
            spaceship_rect.y -= SPACESHIP_VEL
        if moving_down == True and spaceship_rect.y < 450:
            spaceship_rect.y += SPACESHIP_VEL

        for obstacle in obstacles:
            if spaceship_rect.colliderect(obstacle):
                game_over()
                return score

        #9 - Clear the window
        window.fill(BLACK)
        window.blit(SPACE, window_rect)

        #10 - Draw all window elements
        for obstacle in obstacles:
            obstacle.x -= VEL
            if obstacle.width == 40:
                window.blit(small_obstacle, obstacle)
            if obstacle.width == 200:
                window.blit(large_obstacle, obstacle)
            if obstacle.x < -200:
                score += 1
                obstacles.remove(obstacle)

        window.blit(SPACESHIP, spaceship_rect)
        score_text = SCORE_FONT.render("Score: " + str(score), 1, WHITE)
        window.blit(score_text, (10, 10))

        #11 - Update the window
        pygame.display.update()

        #12 - Set frame rate to slow things down
        clock.tick(FPS)

if __name__ == "__main__":
    main()



