import pygame
import os
import random
import time

def game():
    # Initialize pygame
    pygame.font.init()

    # Constants
    WIDTH, HEIGHT = 1440, 900
    WINDOW_WIDTH, WINDOW_HEIGHT = 720, 900
    FPS = 50
    VEL = 8
    PLAYER_WIDTH, PLAYER_HEIGHT = 150, 15
    RECT_WIDTH, RECT_HEIGHT = 15, 15
    BOX_WIDTH, BOX_HEIGHT = 30, 15
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 100, 100)

    # Load assets
    WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("BREAKOUT")
    SCORE_FONT = pygame.font.SysFont("times_new_roman", 60)
    GAME_OVER_FONT = pygame.font.SysFont("times_new_roman", 60)
    YOU_WIN_FONT = pygame.font.SysFont("times_new_roman", 100)
    GAME_OVER_IMAGE = pygame.image.load(os.path.join("images", "game_over.png"))
    START_IMAGE = pygame.image.load(os.path.join("images", "start_screen.png"))
    BACKGROUND_IMAGE = pygame.image.load(os.path.join("images", "space.png"))
    BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))
    window = pygame.Rect(360, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    game_over_screen = pygame.transform.scale(GAME_OVER_IMAGE, (WIDTH, HEIGHT))
    start = pygame.transform.scale(START_IMAGE, (WIDTH, HEIGHT))

    def start_screen():
        WIN.blit(start, (0, 0))
        pygame.display.update()
        time.sleep(3)

    def you_win(score):
        WIN.blit(game_over_screen, (0, 0))
        draw_text = GAME_OVER_FONT.render("You Win! Final Score: "+str(score), 1, WHITE)
        WIN.blit(draw_text, (555, 470))
        pygame.display.update()
        time.sleep(3)

    def game_over(score):
        WIN.blit(game_over_screen, (0, 0))
        draw_text = GAME_OVER_FONT.render("Final Score: "+str(score), 1, WHITE)
        WIN.blit(draw_text, (555, 470))
        pygame.display.update()
        time.sleep(3)
        return score

    def draw_background():
        WIN.blit(BACKGROUND, (0, 0))
        pygame.draw.rect(WIN, BLACK, window)

    def player_handle_movement(keys_pressed, player):
        if (keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]) and player.x > 360:  # left
            player.x -= VEL
        if (keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]) and player.x < 926:  # right
            player.x += VEL

    def main():
        VEL_X, VEL_Y = -5, -5  # Ensure these variables are accessible within the function
        ball_color = WHITE
        player_x, player_y = 660, 870
        rect_x, rect_y = 660, 433
        score = 0
        bounce_count = 0
        score_requirement = 15
        score_needed = 0
        run = True
        lines = 15 ##########################################################
        boxes = []
        box_x, box_y = 369, 0

        player = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
        clock = pygame.time.Clock()

        # Initialize box color outside the loop
        box_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

        start_screen()

        while run:
            keys_pressed = pygame.key.get_pressed()

            if len(boxes) == 0:  # Refill boxes if none are left
                box_x, box_y = 369, 0
                for _ in range(lines):
                    for _ in range(22):
                        uno_boxo = pygame.Rect(box_x, box_y, BOX_WIDTH, BOX_HEIGHT)
                        boxes.append(uno_boxo)
                        box_x += 32
                    box_x = 369
                    box_y += 17

            rect1 = pygame.Rect((rect_x, rect_y, RECT_WIDTH, RECT_HEIGHT))
            clock.tick(FPS)

            for box in boxes[:]:  # Iterate over a copy of the list
                if box.colliderect(rect1):
                    bounce = random.randint(1, 3)
                    boxes.remove(box)
                    score += 1
                    score_needed+=1
                    if score_needed > 25:  # Increase the velocity when score exceeds 75
                        if VEL_X>0:
                            VEL_X = int(VEL_X + 2)
                        elif VEL_X<0:
                            VEL_X = int(VEL_X - 2)
                        if VEL_Y>0:
                            VEL_Y = int(VEL_Y + 2)
                        elif VEL_X<0:
                            VEL_Y = int(VEL_Y - 2)
                        score_needed = 0

                    if bounce == 1:
                        VEL_X = -VEL_X

                    elif bounce == 2:
                        VEL_Y = -VEL_Y

                    elif bounce == 3:
                        VEL_X = -VEL_X
                        VEL_Y = -VEL_Y

                    box_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            if rect1.x < 362 or rect1.x > 1063:
                VEL_X = -VEL_X
            if rect1.y < 4 or rect1.y > 910:
                VEL_Y = -VEL_Y
                if rect1.y > 910:
                    run = False

            if rect1.colliderect(player):
                VEL_Y = -VEL_Y
                bounce_count += 1
                if VEL_X > 0 and (keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]):
                    VEL_X = -VEL_X
                elif VEL_X < 0 and (keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]):
                    VEL_X = -VEL_X

            if len(boxes) == 0:
                you_win(score)
                break

            #if bounce_count == 5 and score < score_requirement:
            #    lines += 1
             #   bounce_count = 0
             #   score_requirement += 15

            rect_x += VEL_X
            rect_y += VEL_Y

            player_handle_movement(keys_pressed, player)
            draw_background()
            score_text = SCORE_FONT.render("Score: " + str(score), 1, WHITE)

            for box in boxes:
                pygame.draw.rect(WIN, box_color, box)

            pygame.draw.rect(WIN, WHITE, player)
            pygame.draw.rect(WIN, ball_color, rect1)
            WIN.blit(score_text, (10, 10))
            pygame.display.update()
            if keys_pressed[pygame.K_q]:
                    break
        score = game_over(score)
        return score
    score = main()
    return score

if __name__ == "__main__":
    game()

