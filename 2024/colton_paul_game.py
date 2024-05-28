import pygame
import sys
import time
def main():
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    FPS = 60
    # Set up the window
    window_width = 800
    window_height = 600
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Rectangles Screensaver")

    # Load images
    image2 = pygame.image.load("images/tom.jpeg")
    image1 = pygame.image.load("images/jerry.jpeg")

    # Scale images to match rectangle size
    image1 = pygame.transform.scale(image1, (100, 100))
    image2 = pygame.transform.scale(image2, (100, 100))

    # Rectangle properties
    rect1 = pygame.Rect(100, 100, 100, 100)
    rect2 = pygame.Rect(200, 200, 100, 100)
    rect2_speed = [10, 10]  # Speed of movement
    rect1_speed = [0, 0]
    score = 0
    score_timer = pygame.time.get_ticks()

    white = (255, 255, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    font = pygame.font.SysFont("comicsansms", 30)
    GAME_OVER_FONT = pygame.font.SysFont("comicsans", 100)


    def game_over(score):
        draw_text = GAME_OVER_FONT.render("Game Over", 1, BLACK)
        window.blit(
            draw_text,
            (
                window_width // 2 - draw_text.get_width() // 2,
                window_height // 2 - draw_text.get_height() // 2,
            ),
        )
        pygame.display.update()
        pygame.time.delay(5000)
        return score


    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            rect1 = rect1.move(-10, 0)
        if keys[pygame.K_RIGHT]:
            rect1 = rect1.move(10, 0)
        if keys[pygame.K_UP]:
            rect1 = rect1.move(0, -10)
        if keys[pygame.K_DOWN]:
            rect1 = rect1.move(0, 10)

        if rect1.colliderect(rect2):
            score = game_over(score)
            return score

        rect1.left = max(0, min(rect1.left, window_width - rect1.width))
        rect1.top = max(0, min(rect1.top, window_height - rect1.height))

        # Update position of moving rectangle
        rect2 = rect2.move(rect2_speed)

        # Bounce off the edges
        if rect2.left < 0 or rect2.right > window_width:
            rect2_speed[0] = -rect2_speed[0]
        if rect2.top < 0 or rect2.bottom > window_height:
            rect2_speed[1] = -rect2_speed[1]
        if rect1.left < 0 or rect1.right > window_width:
            rect1_speed[0] = 0

        current_time = pygame.time.get_ticks()
        if current_time - score_timer >= 1000:
            score += 1
            score_timer = current_time
            rect2_speed[0]+=1
            rect2_speed[1]+=1

        # Draw images on the screen
        window.fill(WHITE)
        window.blit(image1, rect1)
        window.blit(image2, rect2)
        score_text = font.render("Score: " + str(score), True, BLACK)
        window.blit(score_text, (window_width - score_text.get_width() - 10, 10))
        clock.tick(FPS)
        pygame.display.flip()

if __name__ == "__main__":
    main()
