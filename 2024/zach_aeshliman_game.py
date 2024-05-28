# Minotaur's Labyrinth

# Modules
import pygame
import sys
import os
import random
pygame.font.init()

def game():
    # Constants
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)
    WINDOW_WIDTH, WINDOW_HEIGHT = 840, 750
    GRID_SIZE = 20
    THESEUS_HITBOX_SIZE = 20
    MINOTAUR_RUN = GRID_SIZE * 2
    FPS = 10
    MINOTAUR_HITBOX_SIZE, MINOTAUR_HEIGHT, MINOTAUR_WIDTH = 40, 40, 40
    GAME_OVER_FONT = pygame.font.SysFont('comicsans', 100)


    LABYRINTH_LAYOUT = [
        "111111111111111111111",
        "100010000010000010101",
        "101110101000111110101",
        "100010111010100010001",
        "111000001110111010111",
        "100010100000001010001",
        "101111111010111011101",
        "100010000010001000001",
        "111010101110111111101",
        "100010100000101000001",
        "101010111111101010111",
        "100000001000100010101",
        "111011101011101011101",
        "101010100000001000001",
        "101000001110101110111",
        "100011101010101000001",
        "101110101000111010111",
        "100000101010000010001",
        "111111111111111111111",
    ]

    LABYRINTH_WIDTH = len(LABYRINTH_LAYOUT[0])
    LABYRINTH_HEIGHT = len(LABYRINTH_LAYOUT)

    # Initialize pygame
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    # Assets

    # [!] Get eerie, cave-like ambience for background
    # [!] Add in minotaur roars to play at random
    MINOTAUR_IMAGE = pygame.image.load(os.path.join(
        os.path.dirname(__file__), 'images', 'minotaur_sprite.jpeg'))
    MINOTAUR_IMAGE = pygame.transform.scale(MINOTAUR_IMAGE, (MINOTAUR_WIDTH, MINOTAUR_HEIGHT))

    DEAD_MINOTAUR_IMAGE = pygame.transform.rotate(MINOTAUR_IMAGE, 180)

    THESEUS_IMAGE = pygame.image.load(os.path.join(
        os.path.dirname(__file__), 'images', 'theseus.png'))
    THESEUS_IMAGE = pygame.transform.scale(THESEUS_IMAGE, (GRID_SIZE, GRID_SIZE))

    SWORD_IMAGE = pygame.image.load(os.path.join(
        os.path.dirname(__file__), 'images', 'sword_sprite.jpeg'))
    SWORD_IMAGE = pygame.transform.scale(SWORD_IMAGE, (GRID_SIZE//2, GRID_SIZE))

    theseus_rect = THESEUS_IMAGE.get_rect()
    minotaur_rect = MINOTAUR_IMAGE.get_rect()
    sword_rect = SWORD_IMAGE.get_rect()

    # Variables
    theseus_rect.x = GRID_SIZE * 2
    theseus_rect.y = GRID_SIZE * 2
    theseus_dx, theseus_dy = 0, 0

    minotaur_rect.x = GRID_SIZE * 14
    minotaur_rect.y = GRID_SIZE * 10
    minotaur_dx, minotaur_dy = 0, 0

    sword_rect.x = 690
    sword_rect.y = 690
    sword_obtained = False

    def handle_theseus_movements(theseus_rect):

        keys = pygame.key.get_pressed()
        move_directions = pygame.Vector2(0, 0)
        if keys[pygame.K_a]:
            move_directions.x = -1
        elif keys[pygame.K_d]:
            move_directions.x = 1
        if keys[pygame.K_w]:
            move_directions.y = -1
        elif keys[pygame.K_s]:
            move_directions.y = 1

        if move_directions.length() > 0:
            move_directions.normalize_ip()

        theseus_dx, theseus_dy = move_directions.x, move_directions.y
        next_x = theseus_rect.x + theseus_dx * GRID_SIZE
        next_y = theseus_rect.y + theseus_dy * GRID_SIZE

        # Define hitbox position (center of Theseus)
        hitbox_x = next_x + GRID_SIZE // 2 - THESEUS_HITBOX_SIZE // 2
        hitbox_y = next_y + GRID_SIZE // 2 - THESEUS_HITBOX_SIZE // 2

        # Check if the hitbox is within the labyrinth bounds
        if 0 <= hitbox_x < WINDOW_WIDTH - THESEUS_HITBOX_SIZE and 0 <= hitbox_y < WINDOW_HEIGHT - THESEUS_HITBOX_SIZE:
            # Check if the hitbox collides with walls
            if not check_collision(hitbox_x, hitbox_y):
                theseus_rect.x = next_x
                theseus_rect.y = next_y

    # Function to check collision with walls
    def check_collision(x, y):
        cell_x = int(x // MINOTAUR_HITBOX_SIZE)
        cell_y = int(y // MINOTAUR_HITBOX_SIZE)
        return LABYRINTH_LAYOUT[cell_y][cell_x] == "1"

    def handle_minotaur_movements(minotaur_rect):

        next_x = minotaur_rect.x + random.choice([-MINOTAUR_RUN, 0, MINOTAUR_RUN])
        next_y = minotaur_rect.y + random.choice([-MINOTAUR_RUN, 0, MINOTAUR_RUN])

        next_cell_x = next_x // MINOTAUR_HITBOX_SIZE
        next_cell_y = next_y // MINOTAUR_HITBOX_SIZE

        if LABYRINTH_LAYOUT[next_cell_y][next_cell_x] != "1":
            minotaur_rect.x = next_x
            minotaur_rect.y = next_y

    def draw_labyrinth(window):
        for y, row in enumerate(LABYRINTH_LAYOUT):
            for x, cell in enumerate(row):
                if cell == "1":
                    pygame.draw.rect(window, WHITE, (x * MINOTAUR_HITBOX_SIZE, y * MINOTAUR_HITBOX_SIZE, MINOTAUR_HITBOX_SIZE, MINOTAUR_HITBOX_SIZE))

    def game_over_lose():
        loser_message = random.randint(1,3)
        if loser_message == 1:
            draw_text = GAME_OVER_FONT.render("u loser", 1, RED)
        elif loser_message == 2:
            draw_text = GAME_OVER_FONT.render("imagine", 1, RED)
        elif loser_message == 3:
            draw_text = GAME_OVER_FONT.render("try harder", 1, RED)
        window.blit(draw_text, (WINDOW_WIDTH//2 - draw_text.get_width()//2, WINDOW_HEIGHT//2 - draw_text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(5000)
        return

    def game_over_win():
        win_message = random.randint(1, 3)
        if win_message == 1:
            draw_text = GAME_OVER_FONT.render("congrats", 1, YELLOW)
        elif win_message == 2:
            draw_text = GAME_OVER_FONT.render("want a cookie?", 1, YELLOW)
        elif win_message == 3:
            draw_text = GAME_OVER_FONT.render("good job", 1, YELLOW)
        window.blit(draw_text, (WINDOW_WIDTH//2 - draw_text.get_width()//2, WINDOW_HEIGHT//2 - draw_text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(5000)
        return

    # Main game loop
    def main(theseus_rect, sword_rect, minotaur_rect, theseus_dx, theseus_dy, minotaur_dx, minotaur_dy, sword_obtained):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            if theseus_rect.colliderect(sword_rect):
                sword_obtained = True

            if theseus_rect.colliderect(minotaur_rect) and sword_obtained == False:
                game_over_lose()
                return
            elif theseus_rect.colliderect(minotaur_rect) and sword_obtained == True:
                game_over_win()
                return

            handle_theseus_movements(theseus_rect)
            handle_minotaur_movements(minotaur_rect)

            theseus_rect.x += theseus_dx * GRID_SIZE
            theseus_rect.y += theseus_dy * GRID_SIZE

            minotaur_rect.x += minotaur_dx
            minotaur_rect.y += minotaur_dy

            if sword_obtained == True:
                sword_rect.x = theseus_rect.x + 5
                sword_rect.y = theseus_rect.y - 15

            window.fill(BLACK)
            draw_labyrinth(window)

            theseus_draw_x = theseus_rect.x - THESEUS_HITBOX_SIZE // 2
            theseus_draw_y = theseus_rect.y - THESEUS_HITBOX_SIZE // 2

            window.blit(MINOTAUR_IMAGE, (minotaur_rect.x, minotaur_rect.y))
            window.blit(THESEUS_IMAGE, theseus_rect)
            window.blit(SWORD_IMAGE, (sword_rect.x, sword_rect.y))

            pygame.display.update()
            clock.tick(FPS)
    main(theseus_rect,sword_rect, minotaur_rect, theseus_dx, theseus_dy, minotaur_dx, minotaur_dy, sword_obtained)

if __name__ == "__main__":
    game()
