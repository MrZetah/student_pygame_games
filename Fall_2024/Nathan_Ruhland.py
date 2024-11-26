import pygame
from pygame.locals import *
import sys
pygame.font.init()

def main():
    # 2 - Define constants
    GOLD = (255, 215, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    WINDOW_WIDTH = 640
    WINDOW_HEIGHT = 480
    OVEN_HEIGHT = 100
    OVEN_WIDTH = 100
    FPS = 60
    VEL = 5
    COOKIE_WIDTH = 40
    COOKIE_HEIGHT = 40
    JUMP_HEIGHT = 100005  # Tweak for jump height
    UP_GRAVITY = 1    # Upward gravity when jumping
    DOWN_GRAVITY = .10034 # Downward gravity for falling
    vel_y = 0.3        # Vertical velocity
    PLAYER_VELOCITY = 10
    moving_left = False
    moving_right = False
    WINNER_FONT = pygame.font.SysFont('comicsans', 100)

    # 3 - Initialize the world
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    # 4 - Load assets: images, sounds, etc.
    COOKIE = pygame.image.load('Assets/cookie.jpeg')
    OVEN = pygame.image.load('Assets/oven.jpeg')
    OVEN = pygame.transform.scale(OVEN, (OVEN_HEIGHT, OVEN_WIDTH))
    oven_rect = OVEN.get_rect()
    COOKIE = pygame.transform.scale(COOKIE, (COOKIE_HEIGHT, COOKIE_WIDTH))
    cookie_rect = COOKIE.get_rect()
    cookie_rect.midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT)

    # 5 - Initialize variables
    platform_1 = pygame.Rect(0, 290, 150, 5)
    platform_2 = pygame.Rect(500, 390, 150, 5)
    platform_3 = pygame.Rect (550, 190, 150, 5)
    winner_stand = pygame.Rect(10, 100, 150, 5)

    def game_over():
        draw_text = WINNER_FONT.render("YOU WIN", 1, BLACK)
        window.blit(draw_text, (WINDOW_WIDTH//2 - draw_text.get_width()//2, WINDOW_HEIGHT//2 - draw_text.get_height()//2))
        pygame.display.update()
        return

    duration = 10000
    INSTRUCTIONS_FONT = pygame.font.SysFont('comicsans', 20)
    start_ticks = pygame.time.get_ticks()
    should_break = False
    while pygame.time.get_ticks() - start_ticks < duration:
        if should_break:
            break
        window.fill(WHITE)
        instructions = ['Created by Nathan Ruhland',
        'Press enter to skip at any time',
        'Use the wasd keys to get the cookie to the oven']
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

    # 7 - Loop forever
    while True:
        # 8 - Check for and handle events
        for event in pygame.event.get():
            # Check to see if user has quit the game
            if event.type == pygame.QUIT:
                return

        # 9 - Do any "per frame" actions (move objects, add or remove items)
        cookie_rect.y += vel_y

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and cookie_rect.y == WINDOW_HEIGHT - COOKIE_HEIGHT:  # Check if player is on the ground
                vel_y = -JUMP_HEIGHT

        # Gravity logic
        if cookie_rect.y < WINDOW_HEIGHT - COOKIE_HEIGHT and vel_y < 0:  # If the player is in the air and moving up, decrease the y velocity by the "up gravity"
            vel_y += UP_GRAVITY
        if cookie_rect.y < WINDOW_HEIGHT - COOKIE_HEIGHT and vel_y >= 0:  # If the player is falling, increase the y velocity by the "down gravity"
            vel_y += DOWN_GRAVITY

        # Collision detection with platform_1
        if cookie_rect.colliderect(platform_1) and vel_y >= 0:  # Check if falling down and colliding with platform_1
            vel_y = 0
            cookie_rect.y = platform_1.top - COOKIE_HEIGHT

        if cookie_rect.colliderect(platform_2) and vel_y >= 0:
            vel_y = 0
            cookie_rect.y = platform_2.top - COOKIE_HEIGHT

        if cookie_rect.colliderect(platform_3) and vel_y >= 0:
            vel_y = 0
            cookie_rect.y = platform_3.top - COOKIE_HEIGHT
        if cookie_rect.colliderect(winner_stand) and vel_y >= 0:
            vel_y = 0
            cookie_rect.y = winner_stand.top - COOKIE_HEIGHT

                   # Position the cookie just above the platform
        # If the cookie is on the ground (window bottom), stop downward movement
        if cookie_rect.y >= WINDOW_HEIGHT - COOKIE_HEIGHT:
            vel_y = 0
            cookie_rect.y = WINDOW_HEIGHT - COOKIE_HEIGHT  # Correct position if the cookie goes below the screen

        # Movement controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s] and cookie_rect.y < WINDOW_HEIGHT - COOKIE_HEIGHT:
            cookie_rect.y += VEL
        if keys[pygame.K_w] and cookie_rect.y > 0:
            cookie_rect.y -= VEL
        if keys[pygame.K_d] and cookie_rect.x < WINDOW_WIDTH - COOKIE_WIDTH:
            cookie_rect.x += VEL
        if keys[pygame.K_a] and cookie_rect.x > 0:
            cookie_rect.x -= VEL

        # 10 - Clear the window
        window.fill(WHITE)

        # 11 - Draw all window elements
        pygame.draw.rect(window, BLACK, platform_1)
        pygame.draw.rect(window, BLACK, platform_2)
        pygame.draw.rect(window, BLACK, platform_3)
        pygame.draw.rect(window, GOLD, winner_stand)
        window.blit(COOKIE, cookie_rect)
        window.blit(OVEN, oven_rect)
        # 12 - Update the window
        pygame.display.update()
        if cookie_rect.colliderect(oven_rect):
            game_over()
            pygame.time.delay(3000)
            return


        # 13 - Set frame rate to slow things down
        clock.tick(FPS)

if __name__ == "__main__":
    main()
