import pygame
import sys
import csv
import Devin_Barnum
import Henrik_Ellickson
import Jailyn_Alvarado
import Gabe_Fredin
import Autumn_Kron
import Allie_Wehlage
import Ben_Kritzeck
import Aidan_Tran
import Nathan_Ruhland
import Maveric_Peterson
import Marcus_Brown
import Yuna_Gaidawirth
import Ryder_Dietman
import Eric_Hernandez
import Carlee_Ludwig

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 700, 800
column_1 = 200
column_2 = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.Font(None, 30)
font1 = pygame.font.Font(None, 50)
# Menu options
menu_options = ['Gabe Fredin', 'Flappy Bird', 'Jailyn Maze', 'Block Battle', 'Brick Breaker',
                'Cookie', 'SIMON', 'Platformer Battle', 'Henrik Ellickson', 'Fart Man',
                'Marcus Brown', 'Dino Shoot Out', 'Two Week Party', 'Space Escape', 'Tron']
selected_option = 0

def reset_screen():
    SCREEN_WIDTH, SCREEN_HEIGHT = 700, 900
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Menu")


def draw_menu(high_scores):
    screen.fill(WHITE)
    # Draw Game Heading
    game_heading = font1.render("Select Game", True, BLUE)
    game_heading_rect = game_heading.get_rect(center=(column_1, 50))
    screen.blit(game_heading, game_heading_rect)
    # Draw Game Names
    for index, option in enumerate(menu_options):
        color = RED if index == selected_option else BLACK
        text = font.render(option, True, color)
        text_rect = text.get_rect(center=(column_1, 100 + index * 40))
        screen.blit(text, text_rect)
    # Draw High Score Heading
    score_heading = font1.render("High Score", True, BLUE)
    score_heading_rect = score_heading.get_rect(center=(column_2, 50))
    screen.blit(score_heading, score_heading_rect)
    # Draw High Scores
    for index, score in enumerate(high_scores):
        color = RED if index == selected_option else BLACK
        text = font.render(str(score), True, color)
        text_rect = text.get_rect(center=(column_2, 100 + index * 40))
        screen.blit(text, text_rect)

    pygame.display.update()

def load_scores():
    filename = 'high_scores_all_games.csv'
    data_list = []
    with open(filename, mode='r', newline='', encoding="utf-8-sig") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data_list.append(row[0])
    return data_list

def load_play_attempts():
    filename = 'play_attempts.csv'
    play_count = []
    with open(filename, mode='r', newline='', encoding="utf-8-sig") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            play_count.append(int(row[0]))
    print(play_count)
    return play_count

def write_scores_to_csv(high_scores, filename):
    with open(filename, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        for item in high_scores:
            csv_writer.writerow([item])

def write_play_attempts_to_csv(play_count, filename):
    with open(filename, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        for item in play_count:
            csv_writer.writerow([item])


def main():
    high_scores = load_scores()
    play_attempts = load_play_attempts()
    global selected_option
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                write_scores_to_csv(high_scores, 'high_scores_all_games.csv')
                write_play_attempts_to_csv(play_attempts, 'play_attempts.csv')
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    print(f"{menu_options[selected_option]} selected")

                    # Call the corresponding function here
                    if selected_option == 0:
                        play_attempts[0] += 1
                        score = Gabe_Fredin.main()
                        if score > int(high_scores[selected_option]):
                            high_scores[selected_option] = score
                            write_scores_to_csv(high_scores, 'high_scores_all_games.csv')
                        reset_screen()

                    elif selected_option == 1:
                        play_attempts[1] += 1
                        score = Autumn_Kron.main()
                        if score > int(high_scores[selected_option]):
                            high_scores[selected_option] = score
                            write_scores_to_csv(high_scores, 'high_scores_all_games.csv')
                        reset_screen()

                    elif selected_option == 2:
                        play_attempts[2] += 1
                        Allie_Wehlage.main()
                        reset_screen()

                    elif selected_option == 3:
                        play_attempts[3] += 1
                        score = Ben_Kritzeck.main()
                        if score > int(high_scores[selected_option]):
                            high_scores[selected_option] = score
                            write_scores_to_csv(high_scores, 'high_scores_all_games.csv')
                        reset_screen()

                    elif selected_option == 4:
                        play_attempts[4] += 1
                        score = Aidan_Tran.main()
                        if score > float(high_scores[selected_option]):
                            high_scores[selected_option] = round(score, 5)
                            write_scores_to_csv(high_scores, 'high_scores_all_games.csv')
                        reset_screen()


                    elif selected_option == 5:
                        play_attempts[5] += 1
                        Nathan_Ruhland.main()
                        reset_screen()

                    elif selected_option == 6:
                        play_attempts[6] += 1
                        score = Devin_Barnum.main()
                        if score > int(high_scores[selected_option]):
                            high_scores[selected_option] = score
                            write_scores_to_csv(high_scores, 'high_scores_all_games.csv')
                        reset_screen()

                    elif selected_option == 7:
                        play_attempts[7] += 1
                        Jailyn_Alvarado.main()
                        reset_screen()

                    elif selected_option == 8:
                        play_attempts[8] += 1
                        score = Henrik_Ellickson.main()
                        if score > int(high_scores[selected_option]):
                            high_scores[selected_option] = score
                            write_scores_to_csv(high_scores, 'high_scores_all_games.csv')
                        reset_screen()

                    elif selected_option == 9:
                        play_attempts[9] += 1
                        Maveric_Peterson.main()
                        reset_screen()

                    elif selected_option == 10:
                        play_attempts[10] += 1
                        score = Marcus_Brown.main()
                        if score > int(high_scores[selected_option]):
                            high_scores[selected_option] = score
                            write_scores_to_csv(high_scores, 'high_scores_all_games.csv')
                        reset_screen()

                    elif selected_option == 11:
                        play_attempts[11] += 1
                        Yuna_Gaidawirth.main()
                        reset_screen()

                    elif selected_option == 12:
                        play_attempts[12] += 1
                        score = Ryder_Dietman.main()
                        if score > int(high_scores[selected_option]):
                            high_scores[selected_option] = score
                            write_scores_to_csv(high_scores, 'high_scores_all_games.csv')
                        reset_screen()

                    elif selected_option == 13:
                        play_attempts[13] += 1
                        score = Eric_Hernandez.main()
                        if score > int(high_scores[selected_option]):
                            high_scores[selected_option] = score
                            write_scores_to_csv(high_scores, 'high_scores_all_games.csv')
                        reset_screen()

                    elif selected_option == 14:
                        play_attempts[14] += 1
                        Carlee_Ludwig.main()
                        reset_screen()


        draw_menu(high_scores)
        clock.tick(10)

if __name__ == "__main__":
    main()
