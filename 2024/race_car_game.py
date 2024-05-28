# Race Car Game

# 1 - import packages
import pygame
from pygame.locals import *
import sys
import random
pygame.font.init()


def main():
    #2 - Define constants
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 100, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    PURPLE = (255, 0, 255)
    WINDOW_WIDTH = 450
    WINDOW_HEIGHT = 700
    VELOCITY = 15
    CAR_VELOCITY = 15
    FPS = 60
    LINE_WIDTH = 8
    LINE_HEIGHT = 40
    CAR_WIDTH = 75
    CAR_HEIGHT = 150
    GAME_OVER_FONT = pygame.font.SysFont('comicsans', 100)
    INSTRUCTIONS_FONT = pygame.font.SysFont('comicsans', 20)
    duration = 10000

    #3 - Initialize the world
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Race Car Game")
    clock = pygame.time.Clock()

    # Display Instructions
    start_ticks = pygame.time.get_ticks()
    should_break = False
    while pygame.time.get_ticks() - start_ticks < duration:
        if should_break:
            break
        window.fill(WHITE)
        instructions = ['Created by Mr. Zetah',
        'Use the arrow keys to move the car.',
        'Dodge the Obstacles.',
        'Press enter to skip instructions']
        for i, instruction in enumerate(instructions):
            draw_text = INSTRUCTIONS_FONT.render(instruction, 1, BLACK)
            window.blit(draw_text, (WINDOW_WIDTH//2 - draw_text.get_width()//2, 100 + i *50))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    should_break = True
                    break
        pygame.display.update()


    #4 - Load assets: images, sounds, etc.
    race_car = pygame.image.load('images/race_car.png')
    race_car = pygame.transform.scale(race_car, (CAR_WIDTH, CAR_HEIGHT))
    #5 - Initialize variables
    road_lines = []
    obstacles = []
    frames = 0
    frames2 = 0
    obstacles = []
    moving_left = False
    moving_right = False
    line = pygame.Rect(WINDOW_WIDTH//2, -LINE_HEIGHT, LINE_WIDTH, LINE_HEIGHT)
    road_lines.append(line)
    car_rect = race_car.get_rect()
    car_rect.x = WINDOW_WIDTH//2
    car_rect.y = WINDOW_HEIGHT - CAR_HEIGHT - 20

    #5.5 Create functions
    def game_over():
        draw_text = GAME_OVER_FONT.render("Game Over", 1, WHITE)
        window.blit(draw_text, (WINDOW_WIDTH//2 - draw_text.get_width()//2, WINDOW_HEIGHT//2 - draw_text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(5000)
        return

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


    #6 - Loop forever
    while True:

        #7 Check for and handle events
        for event in pygame.event.get():
            #Check to see if user has quit the game
            if event.type == pygame.QUIT:
                return

            #Press the 'q' key as an option to quit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return

            #Check left and right keys to move car side to side
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moving_left = True
                if event.key == pygame.K_RIGHT:
                    moving_right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    moving_left = False
                if event.key == pygame.K_RIGHT:
                    moving_right = False
            #Check for other 'game' related events (collisions, key presses, mouse clicks, etc.)


        #8 - Do any "per frame" actions (move objects, add or remove items)
        frames += 1
        frames2 += 1
        if frames > 12:
            new_line = pygame.Rect(WINDOW_WIDTH//2, -LINE_HEIGHT, LINE_WIDTH, LINE_HEIGHT)
            road_lines.append(new_line)
            frames = 0
        if frames2 > random.randint(45, 100):
            obstacles.append(add_obstacle())
            frames2 = 0

        if moving_left == True and car_rect.x > 0:
            car_rect.x -= CAR_VELOCITY
        if moving_right == True and car_rect.x < (WINDOW_WIDTH - CAR_WIDTH):
            car_rect.x += CAR_VELOCITY

        for obstacle in obstacles:
            if car_rect.colliderect(obstacle):
                draw_text = GAME_OVER_FONT.render("Game Over", 1, WHITE)
                window.blit(draw_text, (WINDOW_WIDTH//2 - draw_text.get_width()//2, WINDOW_HEIGHT//2 - draw_text.get_height()//2))
                pygame.display.update()
                pygame.time.delay(3000)
                return

        #9 - Clear the window
        window.fill(BLACK)

        #10 - Draw all window elements
        for line in road_lines:
            line.y += VELOCITY
            pygame.draw.rect(window, WHITE, line)
            if line.y > WINDOW_HEIGHT:
                road_lines.remove(line)
        for obstacle in obstacles:
            obstacle.y += VELOCITY
            pygame.draw.rect(window, PURPLE, obstacle)
            if obstacle.y > WINDOW_HEIGHT:
                obstacles.remove(obstacle)

        window.blit(race_car, car_rect)
        #11 - Update the window
        pygame.display.update()

        #12 - Set frame rate to slow things down
        clock.tick(FPS)

if __name__ == "__main__":
    main()

