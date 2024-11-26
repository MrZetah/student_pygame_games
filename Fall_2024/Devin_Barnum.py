import pygame
from pygame.locals import *
import random
import time
import tkinter as tk

'''
class UsernameEntryWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Username")
        self.geometry("400x300+200+100")

        self.username = ""

        self.label = tk.Label(self, text="Enter your username:", fg='black')
        self.label.pack()

        self.entry = tk.Entry(self)
        self.entry.pack()

        self.submit_button = tk.Button(self, text="Submit", command=self.on_submit, fg='black')
        self.submit_button.pack()

    def on_submit(self):
        self.username = self.entry.get()
        if not self.username.strip():  # if username is empty use NAMELESS WEIRDO
            self.username = "Nameless Weirdo"
        self.quit()  # exit the Tkinter event loop
        self.destroy()  # DESTROY the Tkinter window

    def get_username(self):
        return self.username


def create_screen():
    window = UsernameEntryWindow()
    window.mainloop()  # start the Tkinter main loop
    return window.get_username()  # save the username after the window closes
'''

def main():
    # save the username input from the Tkinter window
    #user_input = create_screen()

    # Initialize pygame
    pygame.init()

    # Set up the game window
    WIDTH, HEIGHT = 450, 450
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("SIMON")
    SCORE_FONT = pygame.font.SysFont('copperplate', 30)
    wrong_answer_sound = pygame.mixer.Sound('Assets/wrong-answer-buzzer.mp3')
    bg = pygame.image.load('Assets/download.jpeg')
    bg_img = pygame.transform.scale(bg, (70, 70))
    '''
    # read the highscore from file
    highest_score = {'name': '', 'score': 0}
    try:
        with open('Assets/high_score.txt', 'r') as readfile:
            # read each line
            for line in readfile:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) != 2:
                    continue

                name, score = parts
                try:
                    score = int(score)
                except ValueError:
                    continue

                if score > highest_score['score']:
                    highest_score['name'] = name
                    highest_score['score'] = score
    except FileNotFoundError:
        pass

    highest_score_words = f'Highscore = {highest_score["score"]} by {highest_score["name"]}'

    # create greeting message
    greeting = f'Hello {user_input}'
    '''
    # Display Instructions for a short time
    duration = 10000
    WELCOME_FONT = pygame.font.SysFont('PT Mono', 23)
    INSTRUCTIONS_FONT = pygame.font.SysFont('comicsans', 20)
    start_ticks = pygame.time.get_ticks()
    should_break = False

    while pygame.time.get_ticks() - start_ticks < duration:
        if should_break:
            break
        window.fill((255, 255, 255))
        instructions = ['Created by Devin Barnum',
                        'Press enter to skip at any time',
                        'Use keys R, G, B, and Y to copy ',
                        'the same pattern as the one shown before']
        for i, instruction in enumerate(instructions):
            draw_text = INSTRUCTIONS_FONT.render(instruction, 1, (0, 0, 0))
            window.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, 100 + i * 50))
        '''
        hscore = INSTRUCTIONS_FONT.render(highest_score_words, 1, (0, 0, 0))
        window.blit(hscore, (WIDTH // 2 - hscore.get_width() // 2, 300))

        greet = WELCOME_FONT.render(greeting, 1, (0, 0, 0))
        window.blit(greet, (WIDTH // 2 - greet.get_width() // 2, 40))
        '''
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    should_break = True
                    break
        pygame.display.update()

    window.fill((0, 0, 0))

    COLOR_SOUNDS = {
        "red": pygame.mixer.Sound('Assets/redb.mp3'),
        "blue": pygame.mixer.Sound('Assets/blueb.mp3'),
        "green": pygame.mixer.Sound('Assets/greenb.mp3'),
        "yellow": pygame.mixer.Sound('Assets/yellowb.mp3')
    }

    COLORS = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0)
    }

    COLOR_KEYS = {
        pygame.K_r: "red",
        pygame.K_g: "green",
        pygame.K_b: "blue",
        pygame.K_y: "yellow"
    }

    rects = {
        "red": pygame.Rect(50, 100, WIDTH // 3, HEIGHT // 4),
        "green": pygame.Rect(250, 100, WIDTH // 3, HEIGHT // 4),
        "blue": pygame.Rect(50, 250, WIDTH // 3, HEIGHT // 4),
        "yellow": pygame.Rect(250, 250, WIDTH // 3, HEIGHT // 4),
    }

    font = pygame.font.Font(None, 36)

    class Game:
        def __init__(self):
            self.sequence = [random.choice(list(COLORS.keys()))]
            self.player_input = []
            self.game_over = False
            self.score = 0

        def lighten_color(self, color, factor=0.4):
            return tuple(min(int(c + (255 - c) * factor), 255) for c in color)

        def draw_window(self):
            window.fill((0, 0, 0))  # Clear the window
            for color, rect in rects.items():
                pygame.draw.rect(window, COLORS[color], rect)

            if self.game_over:
                # Display "Game Over!" if the game is over
                game_over_text = font.render("Game Over!", True, (255, 255, 255))
                window.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 220))

            score_text = SCORE_FONT.render("Score: " + str(self.score), 1, (255, 255, 255))
            window.blit(score_text, (10, 8))
            window.blit(bg_img, (270, 0))

            pygame.display.update()

        def show_sequence(self):
            base_delay = 1.0
            speed_up_factor = 0.1
            min_delay = 0.3

            delay = max(min_delay, base_delay - self.score * speed_up_factor)

            time.sleep(1)
            for color in self.sequence:
                window.fill((0, 0, 0))
                lighter_color = self.lighten_color(COLORS[color])
                rect = rects[color]
                pygame.draw.rect(window, lighter_color, rect)
                pygame.display.update()
                COLOR_SOUNDS[color].play()
                time.sleep(delay)
                window.fill((0, 0, 0))
                pygame.display.update()
                time.sleep(0.3)

        def check_input(self):
            if self.player_input != self.sequence[:len(self.player_input)]:
                self.game_over = True  # show game over when input doesn't match sequence

        def handle_input(self, event):
            if event.type == pygame.KEYDOWN:
                if event.key in COLOR_KEYS:
                    color = COLOR_KEYS[event.key]
                    self.player_input.append(color)
                    rect = rects[color]
                    lighter_color = self.lighten_color(COLORS[color])

                    pygame.draw.rect(window, lighter_color, rect)
                    pygame.display.update()
                    COLOR_SOUNDS[color].play()

                    time.sleep(0.75)

                    self.check_input()

                    if self.game_over:
                        highscore = str(self.score)
                        wrong_answer_sound.play()
                        '''
                        with open('Assets/high_score.txt', 'a') as readfile:
                            readfile.write(f"{user_input} {highscore}\n")
                        return
                        '''
                    if len(self.player_input) == len(self.sequence):
                        self.sequence.append(random.choice(list(COLORS.keys())))
                        self.player_input = []
                        self.score += 1
                        self.show_sequence()

    def game_loop():
        game = Game()
        game.show_sequence()

        while not game.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return game.score
                if event.type == pygame.KEYDOWN:
                    game.handle_input(event)

            game.draw_window()

        while game.game_over:
            return game.score
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    # run the game loop
    score = game_loop()
    pygame.time.delay(3000)
    return score

if __name__ == "__main__":
    main()
