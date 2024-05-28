import pygame
import random

def main():
    pygame.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Laser time")

    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    # player at
    player_width = 50
    player_height = 50
    player_x = SCREEN_WIDTH // 2 - player_width // 2
    player_y = SCREEN_HEIGHT - player_height - 20
    player_speed = 5

    # laser att
    lasers = []
    laser_width = 10
    laser_height = 30
    laser_speed = 7
    laser_frequency = 3

    score = 0

    font = pygame.font.Font(None, 36)

    clock = pygame.time.Clock()

    def draw_player(x, y):
        pygame.draw.rect(screen, WHITE, (x, y, player_width, player_height))

    def draw_lasers(lasers):
        for laser in lasers:
            pygame.draw.rect(screen, RED, (laser[0], laser[1], laser_width, laser_height))

    def show_score(score):
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 10))

    def game_over(score):
        screen.fill((0, 0, 0))
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        score_text = font.render("Your score: " + str(score), True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50))
        pygame.display.update()
        pygame.time.wait(5000) # Wait for 2 sec
        return score


    running = True
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
            player_x += player_speed

        if random.randint(0, laser_frequency) == 0:
            laser_x = random.randint(0, SCREEN_WIDTH - laser_width)
            laser_y = 0
            lasers.append([laser_x, laser_y])

        for laser in lasers:
            laser[1] += laser_speed
            if laser[1] > SCREEN_HEIGHT:
                lasers.remove(laser)
                score += 1 # Increment score when a laser passes the player

        for laser in lasers:
            if (player_x < laser[0] + laser_width and
                player_x + player_width > laser[0] and
                player_y < laser[1] + laser_height and
                player_y + player_height > laser[1]):
                score = game_over(score) # Call game over function if player hits laser
                return score
        draw_player(player_x, player_y)
        draw_lasers(lasers)
        show_score(score)

        pygame.display.update()

        clock.tick(60)

if __name__ == "__main__":
    main()

