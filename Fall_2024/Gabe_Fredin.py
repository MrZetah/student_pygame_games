import pygame
import sys
import random

def main():
    pygame.init()

    # set up the display
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Platformer Game')

    # define colors
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    PURPLE = (50, 51, 103)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    kid = pygame.image.load('Assets/lekid.jpeg')
    basketball_img = pygame.image.load('Assets/basketball.jpeg')
    bb_img = pygame.transform.scale(basketball_img, (30, 30))
    sky = pygame.image.load('Assets/lebron.webp')
    sky_img = pygame.transform.scale(sky, (800, 600))
    score = 0


    #frame rate
    clock = pygame.time.Clock()


    # Display Instructions
    duration = 10000
    INSTRUCTIONS_FONT = pygame.font.SysFont('comicsans', 20)
    SCORE_FONT = pygame.font.SysFont('Comic Sans MS', 30)
    start_ticks = pygame.time.get_ticks()
    should_break = False
    while pygame.time.get_ticks() - start_ticks < duration:
        if should_break:
            break
        screen.fill(WHITE)
        instructions = ['Created by Gabriel Fredin',
        'Press enter to move on',
        'Get LeChild to the top',
        'Press arrows to move left and right.',
        'Press Up arrow to Jump.']
        for i, instruction in enumerate(instructions):
            draw_text = INSTRUCTIONS_FONT.render(instruction, 1, BLACK)
            screen.blit(draw_text, (screen_width//2 - draw_text.get_width()//2, 100 + i *50))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    should_break = True
                    break
        pygame.display.update()


    # define some variables
    player_width = 50
    player_height = 50
    player_x = 100
    player_y = screen_height - player_height - 10 #540
    player_vel_x = 0
    player_vel_y = 0
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    gravity = 1.2
    jump_strength = -15
    on_ground = False
    kid_img = pygame.transform.scale(kid, (player_width, player_height))



    basketballs = [
        pygame.Rect(135, 450, 30, 30),
        pygame.Rect(280, 320, 30, 30),
        pygame.Rect(670, 310, 30, 30),
        pygame.Rect(290, 100, 30, 30),
        pygame.Rect(50, 300, 30, 30),
        pygame.Rect(195, 200, 30, 30),
        pygame.Rect(500, 200, 30, 30)]



    # create platforms (x, y, width, height)
    platforms = [
        pygame.Rect(50, 500, 200, 20),
        pygame.Rect(250, 430, 200, 20),
        pygame.Rect(470, 350, 200, 20),
        pygame.Rect(200, 270, 200, 20),
        pygame.Rect(450, 110, 170, 20),
        pygame.Rect(260, 160, 100, 20)]

    # Finish line (left, top, width, height)
    finish_line = pygame.Rect(screen_width - 200, 0, 20, 110)

    # Font for text
    font = pygame.font.SysFont(None, 110)

    # Function to draw text for when won
    def draw_text(text, font, color, x, y):
        img = font.render(text, True, color)
        screen.blit(img, (x, y))


    # Main game loop
    running = True
    while running:
        screen.fill(WHITE)

        # Draw score
        score_text = SCORE_FONT.render("Score: " + str(score), 1, (0, 0, 0))
        screen.blit(score_text, (10, 8))


        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return score
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and on_ground:
                    player_vel_y = jump_strength
                    on_ground = False

            '''
            if keys[pygame.K_UP] and on_ground:
                    player_vel_y = jump_strength
                    on_ground = False
            '''
        # list of basketballs, puts where placed
        collected_bbs = []
        for bb in basketballs:
            if player_rect.colliderect(bb):
                collected_bbs.append(bb)


        # if basketball collected, dissapear, score +1
        for bb in collected_bbs:
            basketballs.remove(bb)
            score += 1


        # Key press handling for player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_vel_x = -5
        elif keys[pygame.K_RIGHT]:
            player_vel_x = 5
        else:
            player_vel_x = 0



        # calculate gravity
        player_vel_y += gravity
        player_x += player_vel_x
        player_y += player_vel_y

        # Check collision with platforms
        on_ground = False
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for platform in platforms:
            if player_rect.colliderect(platform) and player_vel_y >= 0:
                player_y = platform.top - player_height
                player_vel_y = 0
                on_ground = True

        # Prevent the player from falling below the screen
        if player_y > screen_height - player_height:
            player_y = screen_height - player_height
            player_vel_y = 0
            on_ground = True

        #Prevent from right
        if player_x > screen_width - player_width:
            player_x = screen_width - player_width
            player_vel_x = 0
            player_vel_y = 0


        #Prevent from left
        if player_x < 0:
            player_x = 0
            player_vel_x = 0
            player_vel_y = 0



        # Check if player has reached the finish line
        if player_rect.colliderect(finish_line):
            draw_text("You Win!", font, PURPLE, screen_width // 3, screen_height // 3)
            pygame.display.update()
            pygame.time.wait(4000)
            running = False
            return score



        #Draw background image
        screen.blit(sky_img, (0,0))

        # Draw platforms
        for platform in platforms:
            pygame.draw.rect(screen, PURPLE, platform)

        # Draw the finish line
        pygame.draw.rect(screen, BLACK, finish_line)

        # Draw basketballs
        for bb in basketballs:
            screen.blit(bb_img, bb)

        # Draw the player
        screen.blit(kid_img, (player_x, player_y))


        # Update the display

        pygame.display.update()

        # Set the frame rate
        clock.tick(60)

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

