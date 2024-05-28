import pygame
from pygame import *
import random
from random import randint

pygame.font.init()
pygame.mixer.init()

#constants
def main():
    HEIGHT = 760
    WIDTH = 1440
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    BLUE = (0,0,255)
    GREEN = (0,255,0)
    YELLOW = (255, 255, 0)
    Z_WIDTH = 200
    Z_HEIGHT = 100
    Z_X_COORD = WIDTH//2 - (Z_WIDTH//2)
    Z_Y_COORD = HEIGHT * (1/7)
    C_WIDTH = 200
    C_HEIGHT = 100
    BULLET_VEL = 10
    FPS = 60
    VEL = 5
    MAX_BULLETS = 5
    CHARACTER_HIT = pygame.USEREVENT + 1
    ZETAH_HIT = pygame.USEREVENT + 2
    BACKGROUND = pygame.transform.scale(pygame.image.load("Assets/Screenshot 2024-05-13 at 2.08.59 PM.png"), (WIDTH, HEIGHT))
    HEALTH_FONT = pygame.font.SysFont("papyrus", 45)
    TEXT_FONT = pygame.font.SysFont("papyrus", 25)
    WINNER_FONT = pygame.font.SysFont("comicsans", 100)
    INSTRUCTIONS_FONT = pygame.font.SysFont('comicsans', 20)
    duration = 10000

    #initialize external media
    megalovania = pygame.mixer.Sound("Assets/Undertale OST 100 - Megalovania.mp3")

    ZETAH_IMAGE = pygame.image.load("Assets/Screenshot 2024-05-20 at 2.06.46 PM.png")
    CHARACTER_IMAGE = pygame.image.load("Assets/IMG_5987.png")
    BULLET_PIC = pygame.image.load("Assets/Screenshot 2024-05-13 at 2.08.59 PM.png")

    ZETAH = pygame.transform.rotate(pygame.transform.scale(ZETAH_IMAGE, (Z_WIDTH, Z_HEIGHT)), 0)
    CHARACTER = pygame.transform.rotate(pygame.transform.scale(CHARACTER_IMAGE, (C_WIDTH, C_HEIGHT)), 0)
    BULLET = pygame.transform.rotate(pygame.transform.scale(BULLET_PIC, (10, 20)), 0)

    #initalize pygame
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Battle of the Zbuckets")

    start_ticks = pygame.time.get_ticks()
    should_break = False
    while pygame.time.get_ticks() - start_ticks < duration:
        if should_break:
            break
        window.fill(WHITE)
        instructions = ['Created by Owen Hoepner',
        'Press any arrow key to begin.',
        'Use the WASD to move the character. Use the arrow keys to strafe.',
        'KILL ZETAH!',
        'DO NOT LET ZETAH KILL YOU.',
        'Press enter to skip instructions',
        'Press q to quit']
        for i, instruction in enumerate(instructions):
            draw_text = INSTRUCTIONS_FONT.render(instruction, 1, BLACK)
            window.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, 100 + i *50))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    should_break = True
                    break
        pygame.display.update()
    window.fill(BLACK)

    #define functions

    def handle_bullets(zetah, zetah_bullets, character):
        for bullet in zetah_bullets:
            if zetah.x < WIDTH//2 and zetah.y > HEIGHT//2:
                bullet.x += BULLET_VEL
                bullet.y -= BULLET_VEL
            if zetah.x > WIDTH//2 and zetah.y > HEIGHT//2:
                bullet.x -= BULLET_VEL
                bullet.y -= BULLET_VEL
            if zetah.x < WIDTH//2 and zetah.y < HEIGHT//2:
                bullet.x += BULLET_VEL
                bullet.y += BULLET_VEL
            if zetah.x > WIDTH//2 and zetah.y < HEIGHT//2:
                bullet.x -= BULLET_VEL
                bullet.y += BULLET_VEL
            elif character.colliderect(bullet):
                pygame.event.post(pygame.event.Event(CHARACTER_HIT))
                zetah_bullets.remove(bullet)
            elif bullet.x > WIDTH or bullet.x < 0 or bullet.y > HEIGHT or bullet.y < 0:
                zetah_bullets.remove(bullet)

    def draw_window(character, zetah, char_health, zetah_health, zetah_bullets):
        character_text = HEALTH_FONT.render("Health: " + str(char_health), 1, BLACK)
        zetah_health_text = HEALTH_FONT.render("Health: " + str(zetah_health), 1, BLACK)

        window.blit(BACKGROUND,(0,0))
        window.blit(CHARACTER, (character.x, character.y))
        window.blit(ZETAH, (zetah.x, zetah.y))
        window.blit(character_text, (10, 10))
        window.blit(zetah_health_text, (WIDTH - zetah_health_text.get_width() - 10, 10))

        for bullet in zetah_bullets:
            pygame.draw.rect(window, BLACK, bullet)

        pygame.display.update()


    def zetah_hit(zetah, zetah_health):
        t = 0

        zetah_health -= 1

        while t < 5 * FPS:
            text_ow = TEXT_FONT.render("OW", 1, BLACK)
            window.blit(text_ow, (zetah.x+50, zetah.y+50))
            t = t + (1/FPS)

        pygame.display.update()

    def player_movement(keys_pressed, character):
        if keys_pressed[pygame.K_a] and character.x - VEL > 0:
            character.x -= VEL
        if keys_pressed[pygame.K_d] and character.x + VEL + C_WIDTH < WIDTH:
            character.x += VEL
        if keys_pressed[pygame.K_w] and character.y - VEL > 0:
            character.y -= VEL
        if keys_pressed[pygame.K_s] and character.y + VEL + C_HEIGHT < HEIGHT:
            character.y += VEL

    def draw_winner(text):
        draw_text = WINNER_FONT.render(text, 1, WHITE)
        window.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))

        pygame.display.update()
        pygame.time.delay(5000)

    def zetah_borders(zetah):
        if zetah.x + Z_WIDTH > WIDTH:
            zetah.x = WIDTH - Z_WIDTH//2
        if zetah.x - Z_WIDTH < 0:
            zetah.x = 0 + Z_WIDTH//2
        if zetah.y + Z_HEIGHT > HEIGHT:
            zetah.y = HEIGHT - Z_HEIGHT
        if zetah.y - Z_HEIGHT < 0:
            zetah.y = 0 + Z_HEIGHT

    while True:
        megalovania.play()

        zetah = pygame.Rect(Z_X_COORD, Z_Y_COORD, Z_WIDTH, Z_HEIGHT)
        character = pygame.Rect(WIDTH//2 - (C_WIDTH//2), HEIGHT * (6/7), C_WIDTH, C_HEIGHT)

        zetah_health = 10
        char_health = 10

        zetah_bullets = []

        clock = pygame.time.Clock()

        run = True
        while run:
            clock.tick(FPS)

            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        run = False
                        pygame.mixer.stop()
                        return
                    if event.key == pygame.K_LEFT and character.x - C_WIDTH//2 > 0:
                        character.x -= 100
                    if event.key == pygame.K_RIGHT and character.x + C_WIDTH * (3/2) < WIDTH:
                        character.x += 100
                    if event.key == pygame.K_DOWN and character.y + C_HEIGHT * (3/2) < HEIGHT:
                        character.y += 100
                    if event.key == pygame.K_UP and character.y - C_HEIGHT//3  > 0:
                        character.y -= 100
                    if event.key == pygame.K_LSHIFT:
                        ax = pygame.Rect(character.x, character.y - C_HEIGHT - 10, C_WIDTH, C_HEIGHT)
                        pygame.draw.rect(window, BLACK, ax)
                        if zetah.colliderect(ax):
                            pygame.event.post(pygame.event.Event(ZETAH_HIT))

                    X_MOVEMENT = {"NEXT_MOVE": randint(-100, 100)}
                    Y_MOVEMENT = {"NEXT_MOVE": randint(-100, 100)}
                    for v in X_MOVEMENT.values():
                        zetah.x = zetah.x + v
                        if len(zetah_bullets) < MAX_BULLETS:
                            bullet = pygame.Rect(zetah.x + Z_WIDTH//2 , zetah.y + Z_HEIGHT//2, 10, 5)
                            zetah_bullets.append(bullet)
                    for v in Y_MOVEMENT.values():
                        zetah.y = zetah.y + v
                        if len(zetah_bullets) < MAX_BULLETS:
                            bullet = pygame.Rect(zetah.x + Z_WIDTH//2 , zetah.y + Z_HEIGHT//2, 10, 5)
                            zetah_bullets.append(bullet)
                '''
                if zetah.colliderect(character):
                    pygame.event.post(pygame.event.Event(CHARACTER_HIT))
                '''
                if event.type == CHARACTER_HIT:
                    cooldown = 0
                    if cooldown < (5 * FPS):
                        char_health -= 1
                        cooldown += (1/FPS)
                    if cooldown > (5 * FPS):
                        cooldown = 0
                if event.type == ZETAH_HIT:
                    zetah_hit(zetah, zetah_health)
                    zetah_health -= 2
                zetah_borders(zetah)
            winner_text = ""
            if zetah_health <= 0:
                winner_text = "You Win"
            if char_health <= 0:
                winner_text = "Zetah Wins"
            if winner_text != "":
                draw_winner(winner_text)
                break

            pygame.display.update()
            keys_pressed = pygame.key.get_pressed()
            player_movement(keys_pressed, character)
            handle_bullets(zetah, zetah_bullets, character)
            draw_window(character, zetah, zetah_health, char_health, zetah_bullets)

        pygame.mixer.stop()

if __name__ == "__main__":
    main()
















