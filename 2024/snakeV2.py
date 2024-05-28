# Snake Version 2

# 1 - import packages
import pygame
from pygame.locals import *
import sys
import random
pygame.font.init()

def main():
    #2 - Define constants
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 700
    FPS = 20
    SNAKE_WIDTH_HEIGHT = 18
    GAP = 1
    DOT_SIZE = SNAKE_WIDTH_HEIGHT
    SCORE_FONT = pygame.font.SysFont('comicsans', 20)   #Create variables with font information for text
    GAME_OVER_FONT = pygame.font.SysFont('comicsans', 100)
    INSTRUCTIONS_FONT = pygame.font.SysFont('comicsans', 20)
    duration = 10000

    #3 - Initialize the world
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()

    # Display Instructions
    start_ticks = pygame.time.get_ticks()
    should_break = False
    while pygame.time.get_ticks() - start_ticks < duration:
        if should_break:
            break
        window.fill(WHITE)
        instructions = ['Created by Mr. Zetah',
        'Press any arrow key to begin.',
        'Use the arrow keys to move the snake.',
        'Collect as many dots as possible.',
        'You die if you hit the edge of the screen or the snake collides with itself.',
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
    window.fill(BLACK)

    #5 - Initialize variables
    play = False
    score = 0
    snake_length = 6
    snake = []
    window_rect = window.get_rect()
    center_x, center_y = window_rect.center[0], window_rect.center[1]
    snake_rect = pygame.Rect(center_x, center_y, SNAKE_WIDTH_HEIGHT, SNAKE_WIDTH_HEIGHT)
    snake.append(snake_rect)
    pygame.draw.rect(window, GREEN, snake_rect)
    direction = ''
    dot_x = random.randint(0, WINDOW_WIDTH - DOT_SIZE)
    dot_y = random.randint(0, WINDOW_HEIGHT - DOT_SIZE)
    dot_rect = pygame.Rect(dot_x, dot_y, DOT_SIZE, DOT_SIZE)
    pygame.display.update()

    def game_over():
        draw_text = GAME_OVER_FONT.render("Game Over", 1, WHITE)
        window.blit(draw_text, (WINDOW_WIDTH//2 - draw_text.get_width()//2, WINDOW_HEIGHT//2 - draw_text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(5000)
        return

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
                if event.key == pygame.K_p:
                    play = not play
                #Check to see if any of the direction keys have been pressed
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    play = True   # Start Game
                    # Set direction of snake
                    if event.key == pygame.K_UP and direction != 'DOWN':
                        if len(snake) == 1:
                            direction = 'UP'
                        else:
                            if snake[-1].x != snake[-2].x:
                                direction = 'UP'
                    if event.key == pygame.K_DOWN and direction != 'UP':
                        if len(snake) == 1:
                            direction = 'DOWN'
                        else:
                            if snake[-1].x != snake[-2].x:
                                direction = 'DOWN'
                    if event.key == pygame.K_LEFT and direction != 'RIGHT':
                        if len(snake) == 1:
                            direction = 'LEFT'
                        else:
                            if snake[-1].y != snake[-2].y:
                                direction = 'LEFT'
                    if event.key == pygame.K_RIGHT and direction != 'LEFT':
                        if len(snake) == 1:
                            direction = 'RIGHT'
                        else:
                            if snake[-1].y != snake[-2].y:
                                direction = 'RIGHT'

        #Check for other 'game' related events (collisions, key presses, mouse clicks, etc.)
        # Check to see if the head of the snake collides with a dot
        if dot_rect.colliderect(snake[-1]):
            dot_x = random.randint(0, WINDOW_WIDTH - DOT_SIZE)
            dot_y = random.randint(0, WINDOW_HEIGHT - DOT_SIZE)
            score += 1
            snake_length += 1

        # Check to see if snake hits any of the walls
        if snake[-1].x < 0 or snake[-1].x > WINDOW_WIDTH - SNAKE_WIDTH_HEIGHT:
            draw_text = GAME_OVER_FONT.render("Game Over", 1, WHITE)
            window.blit(draw_text, (WINDOW_WIDTH//2 - draw_text.get_width()//2, WINDOW_HEIGHT//2 - draw_text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            return score
        if snake[-1].y < 0 or snake[-1].y > WINDOW_HEIGHT - SNAKE_WIDTH_HEIGHT:
            draw_text = GAME_OVER_FONT.render("Game Over", 1, WHITE)
            window.blit(draw_text, (WINDOW_WIDTH//2 - draw_text.get_width()//2, WINDOW_HEIGHT//2 - draw_text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            return score
        # Check to see if snake collides with itself
        for snake_square in snake[:-2]:
            if snake[-1].colliderect(snake_square):
                draw_text = GAME_OVER_FONT.render("Game Over", 1, WHITE)
                window.blit(draw_text, (WINDOW_WIDTH//2 - draw_text.get_width()//2, WINDOW_HEIGHT//2 - draw_text.get_height()//2))
                pygame.display.update()
                pygame.time.delay(5000)
                return score

        if play:
            #8 - Do any "per frame" actions (move objects, add or remove items)
            if direction == 'RIGHT':
                # Move Right
                snake_rect_add = pygame.Rect(snake[-1].x + SNAKE_WIDTH_HEIGHT + GAP, snake[-1].y, SNAKE_WIDTH_HEIGHT, SNAKE_WIDTH_HEIGHT)
            if direction == 'LEFT':
                # Move LEFT
                snake_rect_add = pygame.Rect(snake[-1].x - SNAKE_WIDTH_HEIGHT - GAP, snake[-1].y, SNAKE_WIDTH_HEIGHT, SNAKE_WIDTH_HEIGHT)
            if direction == 'UP':
                # Move UP
                snake_rect_add = pygame.Rect(snake[-1].x, snake[-1].y - SNAKE_WIDTH_HEIGHT - GAP, SNAKE_WIDTH_HEIGHT, SNAKE_WIDTH_HEIGHT)
            if direction == 'DOWN':
                # Move UP
                snake_rect_add = pygame.Rect(snake[-1].x, snake[-1].y + SNAKE_WIDTH_HEIGHT + GAP, SNAKE_WIDTH_HEIGHT, SNAKE_WIDTH_HEIGHT)

            snake.append(snake_rect_add)
            if len(snake) > snake_length:
                del snake[0]

            #9 - Clear the window
            window.fill(BLACK)

            #10 - Draw all window elements
            dot_rect = pygame.Rect(dot_x, dot_y, DOT_SIZE, DOT_SIZE)
            for snake_square in snake:
                pygame.draw.rect(window, GREEN, snake_square)
            pygame.draw.rect(window, RED, dot_rect)
            score_text = SCORE_FONT.render("Score: " + str(score), 1, WHITE)
            window.blit(score_text, (10, 10))
            #11 - Update the window
            pygame.display.update()

            #12 - Set frame rate to slow things down
            clock.tick(FPS)

if __name__ == "__main__":
    main()
