import pygame
import random
import sys
import os
from pygame.locals import *

def main():
    pygame.init()

    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Egg Hunt Game")

    #The stuff under this loads the image for the game
    RED_WIDTH, RED_HEIGHT = 50, 80
    Red = pygame.image.load(os.path.join('Assets', 'kirby.png'))
    Red = pygame.transform.scale(Red, (RED_WIDTH, RED_HEIGHT))
    Red = pygame.transform.rotate(Red, 90)
    WHITE = (255, 255, 255)

    clock = pygame.time.Clock()
    #this tells the player size, position and how fast they go
    player_size = 40
    player_pos = [WIDTH // 2, HEIGHT // 2]
    player_speed = 3.6
    #this controls the egg Variables
    egg_size = 30
    eggs = []
    for _ in range(100):
        egg = [random.randrange(WIDTH - egg_size), random.randrange(HEIGHT - egg_size)]
        eggs.append(egg)

    score = 0
    start_time = pygame.time.get_ticks()
    running = True
    #this draw's the player on the screen
    def draw_player(pos, image):
        screen.blit(image, pos)
    #draws egg's on screen
    def draw_egg(egg):
        pygame.draw.rect(screen, WHITE, (egg[0], egg[1], egg_size, egg_size))

    while running:
        clock.tick(60)
      #event caused by person pressing buttons etc
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    #keybind Functions for moving player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos[1] -= player_speed
        if keys[pygame.K_s]:
            player_pos[1] += player_speed
        if keys[pygame.K_a]:
            player_pos[0] -= player_speed
        if keys[pygame.K_d]:
            player_pos[0] += player_speed

        player_pos[0] = max(0, min(player_pos[0], WIDTH - player_size))
        player_pos[1] = max(0, min(player_pos[1], HEIGHT - player_size))
    #adds random interger between -3 and 3 next ensures that the x position is in the boundaries of the screen
        for egg in eggs:
            egg[0] += random.randint(-3, 3)
            egg[1] += random.randint(-3, 3)
            egg[0] = max(0, min(egg[0], WIDTH - egg_size))
            egg[1] = max(0, min(egg[1], HEIGHT - egg_size))
    #this part iterates though a copy of the egg list checking if the player collides and removes eggs and updates score
        for egg in eggs[:]:
            if (player_pos[0] < egg[0] + egg_size and
                player_pos[0] + player_size > egg[0] and
                player_pos[1] < egg[1] + egg_size and
                player_pos[1] + player_size > egg[1]):
                eggs.remove(egg)
                score += 1
    # fills screen then draws character player at position told by player_pos finally draws each egg
        screen.fill((0, 0, 0))
        draw_player(player_pos, Red)
        for egg in eggs:
            draw_egg(egg)
    #this code displays the score and size of it and draws it on the screen
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (WIDTH - 200, 20))
    #retrieves the time and waits till specific time to stop
        current_time = pygame.time.get_ticks()
        if current_time - start_time >= 30000:
            running = False
    #updates screen
        pygame.display.flip()
    # fills screen with black prints gameover and end score
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 72)
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()

    pygame.time.wait(3000)

    return score

if __name__ == "__main__":
    main()
