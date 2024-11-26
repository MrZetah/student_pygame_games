import pygame
from pygame.locals import *
import sys
import os
pygame.font.init()

def main():
    # 2 - Define constants
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (69, 64, 55)
    BROWN = (0, 255, 0)
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 800
    FPS = 60

    JUMP_HEIGHT = 20
    GRAVITY = 1
    PLAYER_VELOCITY = 6
    BULLET_VEL = 7
    MAX_BULLETS = 3
    CHARACTER_WIDTH, CHARACTER_HEIGHT = (50,65)

    # 3 - Initialize the world
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Chicken Fighters')
    clock = pygame.time.Clock()

    # Load background image
    STRTIMGE= pygame.transform.scale(pygame.image.load(
        os.path.join('Assets', 'pixelcityfirstbg.png')), (WINDOW_WIDTH, WINDOW_HEIGHT))
    background = pygame.transform.scale(pygame.image.load(
        os.path.join('Assets', 'ingameimage.png')), (WINDOW_WIDTH, WINDOW_HEIGHT))

    # Load player images
    player1_image = pygame.image.load(os.path.join('Assets', 'venom-1.png'))
    player2_image = pygame.image.load(os.path.join('Assets', 'carnage-1.png'))

    # Resize player images
    player1_image = pygame.transform.scale(player1_image, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
    player2_image = pygame.transform.scale(player2_image, (CHARACTER_WIDTH, CHARACTER_HEIGHT))

    # Load bullet image
    bullet_image = pygame.image.load(os.path.join('Assets', 'sonnyandcher.png'))
    bullet_image = pygame.transform.scale(bullet_image, (210, 100))

    # Display Instructions
    duration = 10000
    INSTRUCTIONS_FONT = pygame.font.SysFont('verdana', 26)
    start_ticks = pygame.time.get_ticks()
    should_break = False
    while pygame.time.get_ticks() - start_ticks < duration:
        if should_break:
            break
        window.blit(STRTIMGE,(0,0))
        instructions = [
        'Press enter to skip at any time',
        'To win this game you must defeat the other player',
        'Dont fall off the platforms!',
        'Use the arrows and ASWD to move',
        'Control and space bar to shoot',]
        for i, instruction in enumerate(instructions):
            draw_text = INSTRUCTIONS_FONT.render(instruction, 1, WHITE)
            window.blit(draw_text, (WINDOW_WIDTH//2 - draw_text.get_width()//2, 100 + i *50))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    should_break =True
                    break
        pygame.display.update()
    window.blit(STRTIMGE,(0,0))

    # 4 - Load assets: images, sounds, etc.

    # 5 - Initialize variables
    player1_x, player1_y = 100, WINDOW_HEIGHT - CHARACTER_HEIGHT - 10
    player2_x, player2_y = 700, WINDOW_HEIGHT - CHARACTER_HEIGHT - 10
    velocity_y1 = 0
    velocity_y2 = 0
    is_jumping1 =False
    is_jumping2 =False
    bullet1 = []
    bullet2 = []
    player1_health = 10
    player2_health = 10
    platforms=[
        pygame.Rect(0, WINDOW_HEIGHT-725, 400, 23),
        pygame.Rect(310, WINDOW_HEIGHT-575, 560, 22),
        pygame.Rect(0, WINDOW_HEIGHT-400, 350, 22),
        pygame.Rect(350, WINDOW_HEIGHT-275, 425, 22),
        pygame.Rect(50, WINDOW_HEIGHT-98, 324, 22),
        pygame.Rect(0,WINDOW_HEIGHT-5,800,22),]

    # 6 - Define functions
    def handle_bullets():
        nonlocal player1_health, player2_health
        # Handle player 1's bullets
        for b in bullet1:
            b.x += BULLET_VEL
            if player2.colliderect(b):
                player2_health -= 1
                bullet1.remove(b)
            elif b.x > WINDOW_WIDTH:
                bullet1.remove(b)
        # Handle player 2's bullets
        for b in bullet2:
            b.x -= BULLET_VEL
            if player1.colliderect(b):
                player1_health -= 1
                bullet2.remove(b)
            elif b.x < 0:
                bullet2.remove(b)

    def draw_window():
        nonlocal player1_health, player2_health
        window.blit(background, (0, 0))
        window.blit(player1_image, player1)
        window.blit(player2_image, (player2.x, player2.y))

        # Draw health bars
        health_font = pygame.font.SysFont('verdana', 30)
        player1_health_text = health_font.render(f"Player 1 Health: {player1_health}", 1, WHITE)
        player2_health_text = health_font.render(f"Player 2 Health: {player2_health}", 1, WHITE)
        window.blit(player1_health_text, (10, 10))
        window.blit(player2_health_text, (WINDOW_WIDTH - player2_health_text.get_width() - 10, 10))

        # Draw platforms
        for platform in platforms:
            pygame.draw.rect(window, GREEN, platform)

        # Draw bullets
        for b in bullet1:
            window.blit(bullet_image, (b.x, b.y))
        for b in bullet2:
            window.blit(bullet_image, (b.x, b.y))

        # Update window
        pygame.display.update()

    def handle_movement(keys_pressed, player, is_jumping, velocity_y):
    # Player 1 uses WASD keys
        if keys_pressed[pygame.K_a] and player.x - PLAYER_VELOCITY > 0:
            player.x -= PLAYER_VELOCITY
        if keys_pressed[pygame.K_d] and player.x + PLAYER_VELOCITY + player.width < WINDOW_WIDTH:
            player.x += PLAYER_VELOCITY
        if not is_jumping:
            if keys_pressed[pygame.K_w]:
                is_jumping = True
                velocity_y = -JUMP_HEIGHT
        else:
            velocity_y += GRAVITY
            player.y += velocity_y
            on_platform = False
            for platform in platforms:
                if player.colliderect(platform) and velocity_y > 0:
                    if player.y + player.height <= platform.y + 10:
                        player.y = platform.y - player.height
                        is_jumping = False
                        velocity_y = 0
                        on_platform = True
                        break
            #if on_platform:
            if not on_platform:
                is_jumping = True

            if player.y > WINDOW_HEIGHT:
                player.y = WINDOW_HEIGHT - player.height
                is_jumping = False

        return player, is_jumping, velocity_y


    def handle_movement_p2(keys_pressed, player, is_jumping, velocity_y):
        # Player 2 uses Arrow keys
        if keys_pressed[pygame.K_LEFT] and player.x - PLAYER_VELOCITY > 0:
            player.x -= PLAYER_VELOCITY
        if keys_pressed[pygame.K_RIGHT] and player.x + PLAYER_VELOCITY + player.width < WINDOW_WIDTH:
            player.x += PLAYER_VELOCITY
        if not is_jumping:
            if keys_pressed[pygame.K_UP]:
                is_jumping = True
                velocity_y = -JUMP_HEIGHT
        else:
            velocity_y += GRAVITY
            player.y += velocity_y
            on_platform = False
            for platform in platforms:
                if player.colliderect(platform) and velocity_y > 0:
                    if player.y + player.height <= platform.y + 10:
                        player.y = platform.y - player.height
                        is_jumping =  False
                        velocity_y = 0
                        on_platform = True
                        break
            #if on_platform:
            if not on_platform:
                is_jumping =True

            if player.y > WINDOW_HEIGHT:
                player.y = WINDOW_HEIGHT - player.height
                is_jumping =False

        return player, is_jumping, velocity_y

    def draw_winner(text):
        winner_font = pygame.font.SysFont('verdana', 100)
        draw_text = winner_font.render(text, 1, BLACK)
        window.blit(draw_text, (WINDOW_WIDTH / 2 - draw_text.get_width() / 2, WINDOW_HEIGHT / 2 - draw_text.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(4000)

    # 7 - Loop forever
    player1 = player1_image.get_rect()
    player1 = pygame.Rect(player1_x, player1_y, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    player2 = pygame.Rect(player2_x, player2_y, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return
                if event.key == pygame.K_LCTRL and len(bullet1) < MAX_BULLETS:
                    bullet1.append(pygame.Rect(player1.x + player1.width, player1.y + player1.height // 2 - 2, 10, 5))
                if event.key == pygame.K_SPACE and len(bullet2) < MAX_BULLETS:
                    bullet2.append(pygame.Rect(player2.x, player2.y + player2.height // 2 - 2, 10, 5))

        # Handle movement for both playerrs
        keys_pressed = pygame.key.get_pressed()
        player1, is_jumping1, velocity_y1 = handle_movement(keys_pressed, player1, is_jumping1, velocity_y1)
        player2, is_jumping2, velocity_y2 = handle_movement_p2(keys_pressed, player2, is_jumping2, velocity_y2)

        # Handle bullets
        handle_bullets()

        # Check for winner
        if player1_health <= 0:
            draw_winner("Player 2 Wins!")
            return
        if player2_health <= 0:
            draw_winner("Player 1 Wins!")
            return

        # Draw everything
        draw_window()

        clock.tick(FPS)

if __name__ == "__main__":
    main()
