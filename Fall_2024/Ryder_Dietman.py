# Pygame Template

# 1 - import packages
import pygame
from pygame.locals import *
import sys
import time
pygame.font.init()

def main():
    #2 - Define constants
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    WINDOW_WIDTH = 405
    WINDOW_HEIGHT = 700
    FPS = 100
    SCORE_FONT = pygame.font.SysFont('comicsans', 20)
    GAME_OVER_FONT = pygame.font.SysFont('comicsans', 50)


    J_WIDTH,J_HEIGHT=100,60
    K_WIDTH,K_HEIGHT=100,60
    F_WIDTH,F_HEIGHT=120,67
    D_WIDTH,D_HEIGHT=100,60

    D_RECT_WIDTH,D_RECT_HEIGHT=90,60
    F_RECT_WIDTH,F_RECT_HEIGHT=92,67
    J_RECT_WIDTH,J_RECT_HEIGHT=95,60
    K_RECT_WIDTH,K_RECT_HEIGHT=94,60

    game_ticks = pygame.time.get_ticks()

    #3 - Initialize the world
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    # Display Instructions
    duration = 10000
    INSTRUCTIONS_FONT = pygame.font.SysFont('comicsans', 20)
    start_ticks = pygame.time.get_ticks()
    should_break = False
    while pygame.time.get_ticks() - start_ticks < duration:
        if should_break:
            break
        window.fill(WHITE)
        instructions = ['Created by Ryder Dietman',
        'Tap the keys to the beat of the song.']
        for i, instruction in enumerate(instructions):
            draw_text = INSTRUCTIONS_FONT.render(instruction, 1, BLACK)
            window.blit(draw_text, (WINDOW_WIDTH//2 - draw_text.get_width()//2, 100 + i *50))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    should_break = True
                    break
        pygame.display.update()
    window.fill(WHITE)

    #4 - Load assets: images, sounds, etc.
    pygame.mixer.pre_init(frequency=22050, size=-16, channels=2)
    song_file = 'Assets/spotifydown.com - Twinkle Twinkle Little Star-[AudioTrimmer.com].mp3'
    pygame.mixer.music.load(song_file)  # Load the song
    pygame.mixer.music.play(-1)

    d_key=pygame.image.load('Assets/Screenshot_2024-11-06_at_11.46.49_AM-removebg-preview.png')
    d_key=pygame.transform.scale(d_key,(D_WIDTH,D_HEIGHT))

    f_key=pygame.image.load('Assets/Screenshot_2024-11-06_at_11.36.09_AM-removebg-preview.png')
    f_key=pygame.transform.scale(f_key,(F_WIDTH,F_HEIGHT))

    j_key=pygame.image.load('Assets/Screenshot_2024-11-06_at_10.55.56_AM-removebg-preview.png')
    j_key=pygame.transform.scale(j_key,(J_WIDTH,J_HEIGHT))

    k_key=pygame.image.load('Assets/Screenshot_2024-11-06_at_10.56.03_AM-removebg-preview.png')
    k_key=pygame.transform.scale(k_key,(K_WIDTH,K_HEIGHT))


    #5 - Initialize variables
    d_Rect =  pygame.Rect(0, 0, D_RECT_WIDTH, D_RECT_HEIGHT)
    f_Rect = pygame.Rect(90, 0, F_RECT_WIDTH, F_RECT_HEIGHT)
    j_Rect = pygame.Rect(200, 0, J_RECT_WIDTH, J_RECT_HEIGHT)
    k_Rect = pygame.Rect(301, 0, K_RECT_WIDTH, K_RECT_HEIGHT)

    score=0

    static_keys = {
        'd': pygame.Rect(0, 600, D_WIDTH, D_HEIGHT),
        'f': pygame.Rect(90, 597, F_WIDTH, F_HEIGHT),
        'j': pygame.Rect(200, 600, J_WIDTH, J_HEIGHT),
        'k': pygame.Rect(301, 600, K_WIDTH, K_HEIGHT)
    }

    class myRect(pygame.Rect):
        def __init__(self, left, top, width, height, time, key_type):
            super().__init__(left, top, width, height)
            self.time=time
            self.key_type = key_type
            self.active=False
            self.clicked=False

    def key_rect(key_type, time):
        if key_type == 'd':
            return myRect(0, -100, D_WIDTH, D_HEIGHT, time, key_type)
        if key_type == 'f':
            return myRect(90, -100, F_WIDTH, F_HEIGHT, time, key_type)
        if key_type == 'j':
            return myRect(200, -100, J_WIDTH, J_HEIGHT, time, key_type)
        if key_type == 'k':
            return myRect(301, -100, K_WIDTH, K_HEIGHT, time, key_type)

    falling_keys = [
    key_rect('d', 280), key_rect('f', 832), key_rect('j', 1513), key_rect('f', 2237),
    key_rect('d', 2958), key_rect('k', 3610), key_rect('f', 4349), key_rect('j', 5613),
    key_rect('d', 6314), key_rect('j', 7035), key_rect('f', 7721), key_rect('k', 8392),
    key_rect('d', 9028), key_rect('f', 9727), key_rect('j', 11175), key_rect('d', 11814),
    key_rect('k', 12455), key_rect('f', 13132), key_rect('j', 13840), key_rect('d', 14511),
    key_rect('k', 15150), key_rect('f', 16578), key_rect('j', 17215), key_rect('d', 17838),
    key_rect('f', 18580), key_rect('k', 19277), key_rect('d', 20028), key_rect('f', 20717),
    key_rect('j', 22040), key_rect('d', 22728), key_rect('k', 23319), key_rect('f', 24008),
    key_rect('j', 24772), key_rect('d', 25463), key_rect('k', 26108), key_rect('f', 27417),
    key_rect('j', 28165), key_rect('d', 28795), key_rect('k', 29503), key_rect('f', 30216),
    key_rect('j', 30877), key_rect('d', 31588)
]

    #6 - Define functions
    def falling_objects():
        for key in falling_keys:
            if key.time < pygame.time.get_ticks() - start_ticks:
                key.y += 1
            if key.key_type == 'd':
                window.blit(d_key, key)
            elif key.key_type == 'f':
                window.blit(f_key, key)
            elif key.key_type == 'j':
                window.blit(j_key, key)
            elif key.key_type == 'k':
                window.blit(k_key, key)
            if key.y > 500:
                key.active = True

    def game_over():
        window.fill(WHITE)
        draw_text = GAME_OVER_FONT.render("Game Over", 1, BLACK)
        score_text = SCORE_FONT.render("Score: " + str(score), 1, BLACK)
        window.blit(score_text, (150, 400))
        window.blit(draw_text, (WINDOW_WIDTH//2 - draw_text.get_width()//2, WINDOW_HEIGHT//2 - draw_text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(4000)

    start_ticks = pygame.time.get_ticks()
    #7 - Loop forever
    while True:
        if pygame.time.get_ticks() - game_ticks > 44*1000:  # If 41 seconds have passed
            game_over()
            pygame.mixer.music.pause()
            return score
        #8 Check for and handle events
        for event in pygame.event.get():
            #Check to see if user has quit the game
            if event.type == pygame.QUIT:
                pygame.mixer.music.pause()
                return score
            #Press the 'q' key as an option to quit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.mixer.music.pause()
                    return score
                for each_key in falling_keys:
                    if event.key == pygame.K_d and each_key.key_type == 'd' and each_key.active == True:
                        add = (10 - abs(each_key.y - static_keys['k'].y))
                        if add > 0:
                            score += add
                        falling_keys.remove(each_key)
                    elif event.key == pygame.K_f and each_key.key_type == 'f' and each_key.active == True:
                        add = (10 - abs(each_key.y - static_keys['k'].y))
                        if add > 0:
                            score += add
                        falling_keys.remove(each_key)
                    elif event.key == pygame.K_j and each_key.key_type == 'j' and each_key.active == True:
                        add = (10 - abs(each_key.y - static_keys['k'].y))
                        if add > 0:
                            score += add
                        falling_keys.remove(each_key)
                    elif event.key == pygame.K_k and each_key.key_type == 'k' and each_key.active == True:
                        add = (10 - abs(each_key.y - static_keys['k'].y))
                        if add > 0:
                            score += add
                        falling_keys.remove(each_key)
            #Check for other 'game' related events (collisions, key presses, mouse clicks, etc.)


        #9 - Do any "per frame" actions (move objects, add or remove items)

        #10 - Clear the window
        window.fill(WHITE)

        #11 - Draw all window elements
        for key in static_keys.values():
            if key == static_keys['d']:
                window.blit(d_key, key)
            elif key == static_keys['f']:
                window.blit(f_key, key)
            elif key == static_keys['j']:
                window.blit(j_key, key)
            elif key == static_keys['k']:
                window.blit(k_key, key)
        falling_objects()
        score_text = SCORE_FONT.render("Score: " + str(score), 1, BLACK)
        window.blit(score_text, (150, 10))
        #12 - Update the window
        pygame.display.update()

        #13 - Set frame rate to slow things down
        clock.tick(FPS)


if __name__ == "__main__":
    main()


