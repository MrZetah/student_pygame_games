
# Pygame Template

# 1 - import packages
import pygame
from pygame.locals import *
import sys
import os
pygame.font.init()

def main():
    #2 - Define constants
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (180, 180, 180)
    DARK_GREY = (80, 80, 80)
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 500
    FPS = 40
    pygame.display.set_caption("Saurus")

    PLAYER_SIZE = 40
    BOSS_SIZE = 40

    JUMP_HEIGHT1 = 65         # Increasing this value increases jump height, but increasing the up gravity will decrease jump height
    UP_GRAVITY1 = 5           # These variables changes the vel_y variable
    DOWN_GRAVITY1 = 4         # Tweak these two values until you get a realistic feel
    JUMP_HEIGHT2 = 65         # Increasing this value increases jump height, but increasing the up gravity will decrease jump height
    UP_GRAVITY2 = 5           # These variables changes the vel_y variable
    DOWN_GRAVITY2 = 4         # Tweak these two values until you get a realistic feel

    vel_y1 = 0                # Initially set this variable to 0. Pressing the up key will change it later
    vel_y2 = 0                # Initially set this variable to 0. Pressing the up key will change it later

    BULLET_VEL = 16           #velocity of bullets
    MAX_BULLETS = 3           #total amount of bullets available

    PLAYER_VELOCITY = 10      # This is the velocity to move side to side
    BOSS_VELOCITY = 10        # This is the velocity to move side to side

    moving_left = False
    boss_moving_left = False
    moving_right = False      # Initially set block to not move unless left or right key are pressed
    boss_moving_right = False      # Initially set block to not move unless left or right key are pressed
    game_over = False

    dino_bullets = []         #empty list of bullets used
    boss_bullets = []         #x2

    DINO_DMG = pygame.USEREVENT + 1
    BOSS_DMG = pygame.USEREVENT + 2

    dino_health = 20
    boss_health = 20
    HEALTH_FONT = pygame.font.SysFont('baskerville', 16)
    WIN_FONT = pygame.font.SysFont('baskerville', 80)


    #3 - Initialize the world
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    # Display Instructions
    duration = 10000
    INSTRUCTIONS_FONT = pygame.font.SysFont('baskerville', 30)
    start_ticks = pygame.time.get_ticks()
    should_break = False
    while pygame.time.get_ticks() - start_ticks < duration:
        if should_break:
            break
        window.fill(WHITE)
        instructions = ['Created by Yuna Gaidawirth',
        'Press enter to skip at any time',
        'Player1 uses WASD to move, and F to fire bullets',
        'Player2 uses IJKL to move, and H to fire bullets',
        'Bring your enemies health to 0 to win',
        'Press escape button to exit game at any time']
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

    DINOSAUR = pygame.image.load(os.path.join('Assets', 'dinosaur_game.png'))
    DINO = pygame.transform.rotate(pygame.transform.scale(DINOSAUR, (PLAYER_SIZE, PLAYER_SIZE)), 0)    #player
    BACKGROUND = pygame.image.load(os.path.join('Assets', 'dinogame.png'))
    GROUND = pygame.transform.rotate(pygame.transform.scale(BACKGROUND, (WINDOW_HEIGHT + 140, WINDOW_WIDTH - 200)), 0)    #background
    FLYING_DINO = pygame.image.load(os.path.join('Assets', 'image.png'))
    FLY_DINO = pygame.transform.rotate(pygame.transform.scale(FLYING_DINO, (BOSS_SIZE, BOSS_SIZE)), 0)   #boss



    #5 - Initialize variables

    dino = pygame.Rect(WINDOW_WIDTH//2 - 280, WINDOW_HEIGHT - PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)  #player rectangle

    BOSS = pygame.Rect(WINDOW_WIDTH//2 + 250, WINDOW_HEIGHT - BOSS_SIZE, BOSS_SIZE, BOSS_SIZE)


#DRAWING WINDOW ELEMENTS FUNCTION

    def draw_window(dino_bullets, boss_bullets, dino_health, boss_health):    #drawing background and player
        #window.fill(WHITE)
        window.blit(GROUND, (80, 0))
        dino_health_message = HEALTH_FONT.render("PLAYER1 HP: " + str(dino_health), 1, BLACK)
        boss_health_message = HEALTH_FONT.render("PLAYER2 HP: " + str(boss_health), 1, BLACK)

        window.blit(boss_health_message, (WINDOW_WIDTH - dino_health_message.get_width() - 10, 10))
        window.blit(dino_health_message, (10, 10))
        window.blit(DINO, dino)
        window.blit(FLY_DINO, BOSS)

        for bullet in dino_bullets:
            pygame.draw.rect(window, GREY, bullet)   #drawing the bullet

        for bullet in boss_bullets:
            pygame.draw.rect(window, DARK_GREY, bullet)   #drawing the bullet

        pygame.display.update()

#BULLET FUNCTIONS

    def handle_dino_bullets(dino_bullets, boss_health):     #movement of player bullets
        for bullet in dino_bullets:
            bullet.x += BULLET_VEL
            if BOSS.colliderect(bullet):
                pygame.event.post(pygame.event.Event(BOSS_DMG))
                boss_health -= 1
                dino_bullets.remove(bullet)
            elif bullet.x > WINDOW_WIDTH:
                dino_bullets.remove(bullet)
        return boss_health

    def handle_boss_bullets(boss_bullets, dino_health):     #movement of boss bullets
        for bullet in boss_bullets:
            bullet.x -= BULLET_VEL
            if dino.colliderect(bullet):
                pygame.event.post(pygame.event.Event(DINO_DMG))
                dino_health -= 1
                boss_bullets.remove(bullet)
            elif bullet.x < 0:
                boss_bullets.remove(bullet)
        return dino_health

#WINNER FUNCTION

    def winner(text):
        draw_winner_text = WIN_FONT.render(text, 1, BLACK)
        window.blit(draw_winner_text, (WINDOW_WIDTH/2 - draw_winner_text.get_width()/2, draw_winner_text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(5000)

#WINNER DISPLAY FUNCTION

    def handle_win(dino_health, boss_health):
        winner_message = ""
        if dino_health <= 0:
            winner_message = "Player2 Wins!"
        if boss_health <= 0:
            winner_message = "Player1 Wins!"
        if winner_message != "":
            winner(winner_message)
            return True



#CHECK FOR QUIT

    while True:
                #8 Check for and handle events
        for event in pygame.event.get():
                    #Check to see if user has quit the game
            if event.type == pygame.QUIT:
                return
                    #Press the 'q' key as an option to quit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                    #Check for other 'game' related events (collisions, key presses, mouse clicks, etc.)

#PLAYER MOVEMENT

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and dino.y == WINDOW_HEIGHT - PLAYER_SIZE:  # Check to see if player is on ground before jumping
                    vel_y1 = -JUMP_HEIGHT1                                                          # a negative value moves the player up.
            #Check left and right keys to move player side to side
                if event.key == pygame.K_a:
                    moving_left = True
                if event.key == pygame.K_d:
                    moving_right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_d:
                    moving_right = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i and BOSS.y == WINDOW_HEIGHT - BOSS_SIZE:  # Check to see if player is on ground before jumping
                    vel_y2 = -JUMP_HEIGHT2                                                           # a negative value moves the player up.
            #Check left and right keys to move player side to side
                if event.key == pygame.K_j:
                    boss_moving_left = True
                if event.key == pygame.K_l:
                    boss_moving_right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_j:
                    boss_moving_left = False
                if event.key == pygame.K_l:
                    boss_moving_right = False

#FIRING BULLETS

            if event.type == pygame.KEYDOWN:      #act of firing bullets
                if event.key == pygame.K_f and len(dino_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(dino.x + PLAYER_SIZE - 18, dino.y + 10, 10, 5)
                    dino_bullets.append(bullet)

            if event.type == pygame.KEYDOWN:      #act of firing bullets
                if event.key == pygame.K_h and len(boss_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(BOSS.x + BOSS_SIZE - 30, BOSS.y + 10, 10, 5)
                    boss_bullets.append(bullet)

#JUMPING PHYSICS

          # If the up key is pressed, the player will move up due to the y velocity being changed
        dino.y += vel_y1
        if dino.y < WINDOW_HEIGHT - PLAYER_SIZE and vel_y1 < 0:  # if the player is in the air and moving up, decrease the y velocity by the "up gravity" value
            vel_y1 += UP_GRAVITY1
        if dino.y < WINDOW_HEIGHT - PLAYER_SIZE and vel_y1 >= 0:  # if the player is in the air and moving down, increase the y velocity by the "down gravity" value
            vel_y1 += DOWN_GRAVITY1
        if dino.y >= WINDOW_HEIGHT - PLAYER_SIZE:  # When the player hits the ground, set the y velocity to 0 to stop it.
            vel_y1 = 0
            dino.y = WINDOW_HEIGHT - PLAYER_SIZE  # This line corrects for any occurence where the player moves just below the bottom of the screen in a single frame

        BOSS.y += vel_y2
        if BOSS.y < WINDOW_HEIGHT - BOSS_SIZE and vel_y2 < 0:  # if the player is in the air and moving up, decrease the y velocity by the "up gravity" value
            vel_y2 += UP_GRAVITY2
        if BOSS.y < WINDOW_HEIGHT - BOSS_SIZE and vel_y2 >= 0:  # if the player is in the air and moving down, increase the y velocity by the "down gravity" value
            vel_y2 += DOWN_GRAVITY2
        if BOSS.y >= WINDOW_HEIGHT - BOSS_SIZE:  # When the player hits the ground, set the y velocity to 0 to stop it.
            vel_y2 = 0
            BOSS.y = WINDOW_HEIGHT - BOSS_SIZE  # This line corrects for any occurence where the player moves just below the bottom of the screen in a single frame

#KEEPING PLAYER ON THE SCREEN

        if moving_left == True and dino.x > 0:
            dino.x -= PLAYER_VELOCITY
        if moving_right == True and dino.x < (WINDOW_WIDTH - PLAYER_SIZE):
            dino.x += PLAYER_VELOCITY

        if boss_moving_left == True and BOSS.x > 0:
            BOSS.x -= BOSS_VELOCITY
        if boss_moving_right == True and BOSS.x < (WINDOW_WIDTH - BOSS_SIZE):
            BOSS.x += BOSS_VELOCITY

        game_over = handle_win(dino_health, boss_health)
        if game_over:
            break

        #10 - Clear the window
        window.fill(WHITE)

#THE WINDOW ELEMENTS

        boss_health = handle_dino_bullets(dino_bullets, boss_health)
        dino_health = handle_boss_bullets(boss_bullets, dino_health)
        draw_window(dino_bullets, boss_bullets, dino_health, boss_health)

        #12 - Update the window
        pygame.display.update()

        #13 - Set frame rate to slow things down
        clock.tick(FPS)

    return



if __name__ == "__main__":
    main()
