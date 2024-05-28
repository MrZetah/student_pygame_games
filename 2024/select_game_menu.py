import pygame
import sys
import csv
import race_car_game
import snakeV2
import thaddeus_zaborowski_game
import axel_bruns_game
import carson_crosby_game
import colton_hern_game
import colton_paul_game
import dan_lingl_game
import john_schelonka_game
import owen_hoepner_game
import zach_aeshliman_game

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.Font(None, 40)
font1 = pygame.font.Font(None, 50)
# Menu options
menu_options = ['Axel Bruns', 'Carson Crosby', 'Colton Hern', 'Colton Paul', 'Daniel Lingl', 'John Schelonka', 'Owen Hoepner', 'Thaddeus Zaborowski', 'Snake Game', 'Zachary Aeshliman']
selected_option = 0

def reset_screen():
    SCREEN_WIDTH, SCREEN_HEIGHT = 900, 700
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Menu")


def draw_menu(high_scores):
    screen.fill(WHITE)
    # Draw Game Heading
    game_heading = font1.render("Select Game", True, BLUE)
    game_heading_rect = game_heading.get_rect(center=(SCREEN_WIDTH // 5, 50))
    screen.blit(game_heading, game_heading_rect)
    # Draw Game Names
    for index, option in enumerate(menu_options):
        color = RED if index == selected_option else BLACK
        text = font.render(option, True, color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 5, 100 + index * 50))
        screen.blit(text, text_rect)
    # Draw High Score Heading
    score_heading = font1.render("High Score", True, BLUE)
    score_heading_rect = score_heading.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(score_heading, score_heading_rect)
    # Draw High Scores
    for index, score in enumerate(high_scores):
        color = RED if index == selected_option else BLACK
        text = font.render(str(score), True, color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 100 + index * 50))
        screen.blit(text, text_rect)

    pygame.display.update()

def load_scores():
    filename = 'high_scores.csv'
    data_list = []
    with open(filename, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data_list.append(row[0])
    return data_list

def write_scores_to_csv(high_scores, filename):
    with open(filename, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        for item in high_scores:
            csv_writer.writerow([item])

def main():
    high_scores = load_scores()
    global selected_option
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                write_scores_to_csv(high_scores, 'high_scores.csv')
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
                        axel_bruns_game.main(3)
                        reset_screen()

                    elif selected_option == 1:
                        score = carson_crosby_game.game()
                        if score > int(high_scores[selected_option]):
                            high_scores[selected_option] = score
                            write_scores_to_csv(high_scores, 'high_scores.csv')
                            reset_screen()

                    elif selected_option == 2:
                        colton_hern_game.game()
                        reset_screen()

                    elif selected_option == 3:
                        score = colton_paul_game.main()
                        if score > int(high_scores[selected_option]):
                            high_scores[selected_option] = score
                            write_scores_to_csv(high_scores, 'high_scores.csv')
                            reset_screen()

                    elif selected_option == 4:
                        score = dan_lingl_game.main()
                        if score > float(high_scores[selected_option]):
                            high_scores[selected_option] = round(score, 5)
                            write_scores_to_csv(high_scores, 'high_scores.csv')
                            reset_screen()


                    elif selected_option == 5:
                        score = john_schelonka_game.main()
                        if score > int(high_scores[selected_option]):
                            high_scores[selected_option] = score
                            write_scores_to_csv(high_scores, 'high_scores.csv')
                            reset_screen()

                    elif selected_option == 6:
                        owen_hoepner_game.main()
                        reset_screen()

                    elif selected_option == 7:
                        score = thaddeus_zaborowski_game.main()
                        if score > int(high_scores[selected_option]):
                            high_scores[selected_option] = score
                            write_scores_to_csv(high_scores, 'high_scores.csv')
                            reset_screen()

                    elif selected_option == 8:
                        score = snakeV2.main()
                        if score > int(high_scores[selected_option]):
                            high_scores[selected_option] = score
                            write_scores_to_csv(high_scores, 'high_scores.csv')
                            reset_screen()

                    elif selected_option == 9:
                        zach_aeshliman_game.game()
                        reset_screen()

                    #elif selected_option == 10:
                        #pass # Function for Game 11



        draw_menu(high_scores)
        clock.tick(10)

if __name__ == "__main__":
    main()
