import pygame
import sys
import random
from pygame.locals import *
pygame.font.init()

def main():
    FPS = 60
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    COLOR = (20, 255, 20)
    win_width, win_height = 800, 500
    GRAVITY = 0.5
    rect_width, rect_height = 25, 50
    duration = 30000
    score = 0

    with open('highscore_henrik.txt', 'r') as file:
            high_score = int(file.read())

    GAME_OVER_FONT = pygame.font.SysFont('comicsans', 100)
    GAME_START = pygame.font.SysFont('comicsans', 30)
    INSTRUCTIONS_FONT = pygame.font.SysFont('comicsans', 20)

    pygame.init()
    window = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption('Game')
    clock = pygame.time.Clock()

    STEVE = pygame.image.load('Assets/image.png')
    STEVE = pygame.transform.scale(STEVE, (31, 60))
    window.blit(STEVE, (50, 50))

    TNT = pygame.image.load('Assets/tnt.png')
    TNT = pygame.transform.scale(TNT, (50, 50))
    window.blit(TNT, (50, 50))

    rect_x, rect_y = 150, win_height - rect_height
    RECT = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
    VEL_X, VEL_Y = 3, 0

    current_level = 1
    max_level = 2

    obstacle_width, obstacle_height = 50, 50
    obstacle_color = (255, 0, 0)
    obstacles = []

    def generate_obstacles(level):
        num_obstacles = level + 1
        obstacle_spacing = (win_width - 100) // num_obstacles
        return [
            pygame.Rect(100 + i * obstacle_spacing, win_height - obstacle_height, obstacle_width, obstacle_height)
            for i in range(num_obstacles)
        ]

    def game_over(score, high_score):
        if score >= high_score:
            with open('highscore_henrik.txt', 'w') as file:
                file.write(str(score - 1))
        draw_text = GAME_OVER_FONT.render("Game Over", 1, BLACK)
        window.blit(draw_text, (win_width//2 - draw_text.get_width()//2, win_height//2 - draw_text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(5000)
        return score

    obstacles = generate_obstacles(current_level)

    start_ticks = pygame.time.get_ticks()
    should_break = False
    while pygame.time.get_ticks() - start_ticks < duration:
        if should_break:
            break
        window.fill(BLACK)
        instructions = ['My Game by Henrik Ellickson',
        'Press the Up Arrow to jump.',
        'Jump Over the TNT Blocks to keep the score going up.',
        "The game will end if you get hit by the TNT blocks.",
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
    window.fill(WHITE)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return score
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP and rect_y == win_height - rect_height:
                    VEL_Y = -11

        VEL_Y += GRAVITY
        rect_y += VEL_Y

        if rect_y > win_height - rect_height:
            rect_y = win_height - rect_height
            VEL_Y = 0

        rect_x += VEL_X

        if rect_x + rect_width >= win_width:
            if current_level < max_level:
                current_level += 1
                rect_x = -40
                VEL_X += 1
                obstacles = generate_obstacles(current_level)
            else:
                current_level = 1
                rect_x = -40
                VEL_X = 3
                obstacles = generate_obstacles(current_level)

        score += 1
        if high_score < score:
            high_score = score

        pygame.display.set_caption (f'Score {score}       High Score {high_score}')

        player_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        if any(player_rect.colliderect(obstacle) for obstacle in obstacles):
            score = game_over(score, high_score)
            return score

        window.fill(WHITE)
        window.blit(STEVE, player_rect)
        for obstacle in obstacles:
            window.blit(TNT, obstacle)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
