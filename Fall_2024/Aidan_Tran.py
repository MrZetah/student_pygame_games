# 1 - import packages
import pygame
from pygame.locals import *
import sys
import random

pygame.font.init()

def main():
    # 2 - Define constants
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 750
    FPS = 60

    # Game settings
    PADDLE_WIDTH = 90
    PADDLE_HEIGHT = 15
    PADDLE_SPEED = 8
    BALL_SIZE = 10
    BALL_SPEED = 4
    BRICK_WIDTH = 100
    BRICK_HEIGHT = 50
    BRICK_ROWS = 5
    BRICK_COLS = 9
    BRICK_PADDING = 10
    LIVES = 3

    # 3 - Initialize the world
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    # Set up fonts
    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)

    # Game variables
    paddle_x = (WINDOW_WIDTH - PADDLE_WIDTH) // 2
    paddle_y = WINDOW_HEIGHT - 30  # Position the paddle near the bottom of the window
    ball_x, ball_y = paddle_x + PADDLE_WIDTH // 2, WINDOW_HEIGHT // 2
    ball_dx, ball_dy = BALL_SPEED, -BALL_SPEED
    bricks = [[True] * BRICK_COLS for _ in range(BRICK_ROWS)]
    score = 0
    lives = LIVES

    # Load ball image
    ball_image = pygame.image.load("Assets/Nathanpic.jpg")  # Replace with your image path
    ball_image = pygame.transform.scale(ball_image, (BALL_SIZE * 2, BALL_SIZE * 2))

    # Function to draw the bricks
    def draw_bricks():
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                if bricks[row][col]:
                    brick_x = col * (BRICK_WIDTH + BRICK_PADDING) + BRICK_PADDING
                    brick_y = row * (BRICK_HEIGHT + BRICK_PADDING) + BRICK_PADDING
                    pygame.draw.rect(window, BLUE, (brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))

    # Game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return score

        # Move paddle
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and paddle_x > 0:
            paddle_x -= PADDLE_SPEED
        if keys[K_RIGHT] and paddle_x < WINDOW_WIDTH - PADDLE_WIDTH:
            paddle_x += PADDLE_SPEED

        # Move ball
        ball_x += ball_dx
        ball_y += ball_dy

        # Ball collision with walls
        if ball_x <= 0 or ball_x >= WINDOW_WIDTH - BALL_SIZE:
            ball_dx *= -1
        if ball_y <= 0:
            ball_dy *= -1

        # Ball collision with paddle
        if (paddle_x <= ball_x <= paddle_x + PADDLE_WIDTH and
            paddle_y <= ball_y + BALL_SIZE <= paddle_y + PADDLE_HEIGHT):
            ball_dy *= -1

        # Ball collision with bricks
        brick_hit = False
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                if bricks[row][col]:
                    brick_x = col * (BRICK_WIDTH + BRICK_PADDING) + BRICK_PADDING
                    brick_y = row * (BRICK_HEIGHT + BRICK_PADDING) + BRICK_PADDING
                    if (brick_x <= ball_x <= brick_x + BRICK_WIDTH and
                        brick_y <= ball_y <= brick_y + BRICK_HEIGHT):
                        bricks[row][col] = False
                        score += 1
                        ball_dy *= -1
                        brick_hit = True
                        break
            if brick_hit:
                break

        # Ball falls below the paddle (lose a life)
        if ball_y >= WINDOW_HEIGHT:
            lives -= 1
            ball_x, ball_y = paddle_x + PADDLE_WIDTH // 2, WINDOW_HEIGHT // 2
            ball_dx, ball_dy = BALL_SPEED * random.choice([-1, 1]), -BALL_SPEED

        # Check for game over or win
        if lives <= 0:
            window.fill(BLACK)
            text = LARGE_FONT.render("Game Over", True, RED)
            window.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            return score
        if score == BRICK_ROWS * BRICK_COLS:
            window.fill(BLACK)
            text = LARGE_FONT.render("You Win!", True, RED)
            window.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            return score

        # Clear the window
        window.fill(BLACK)

        # Draw all game elements
        pygame.draw.rect(window, WHITE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        window.blit(ball_image, (int(ball_x) - BALL_SIZE, int(ball_y) - BALL_SIZE))
        draw_bricks()

        # Display score and lives
        score_text = FONT.render(f"Score: {score}", True, WHITE)
        lives_text = FONT.render(f"Lives: {lives}", True, WHITE)
        window.blit(score_text, (5, 5))
        window.blit(lives_text, (WINDOW_WIDTH - 100, 5))

        # Update the window
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
