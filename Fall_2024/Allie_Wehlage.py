import pygame
from pygame.locals import *
import random
pygame.font.init()

def main():
    # Initialize Pygame
    pygame.init()
    # Constants
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 650
    CELL_SIZE = 40
    MAZE_WIDTH = SCREEN_WIDTH // CELL_SIZE
    MAZE_HEIGHT = (SCREEN_HEIGHT - 50) // CELL_SIZE
    WHITE = (255, 255, 255)
    BLACK = (25, 15, 192)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    GRAY = (187, 15, 192)
    def display_instructions(screen):
        # Display Intructions
        duration = 10000
        INSTRUCTIONS_FONT = pygame.font.SysFont('comicsans', 20)
        start_ticks = pygame.time.get_ticks()
        should_break = False
        while pygame.time.get_ticks() - start_ticks < duration :
            if should_break:
                break
            screen.fill(WHITE)
            instructions = ['Created by Allie Wehlage',
            'Press enter to skip',
            'Get passed Jailyn and escape the maze']
            for i, instruction in enumerate(instructions):
                draw_text = INSTRUCTIONS_FONT.render(instruction, 1, BLACK)
                screen.blit(draw_text, (SCREEN_WIDTH//2 - draw_text.get_width()//2, 100 + i *50))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        should_break = True
                        break
            pygame.display.update()
        screen.fill(BLACK)


    def create_maze():
        maze = [[0] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]
        # Randomly add obstacles
        for _ in range(200):
            x = random.randint(0, MAZE_WIDTH - 1)
            y = random.randint(0, MAZE_HEIGHT - 1)
            maze[y][x] = 1
        # Set endpoint
        maze[MAZE_HEIGHT - 1][MAZE_WIDTH - 1] = 2
        return maze
    def draw_maze(screen, maze, jailyn):
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                if maze[y][x] == 1:
                    pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    screen.blit(jailyn, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif maze[y][x] == 2:
                    pygame.draw.rect(screen, GRAY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    class Player:
        def __init__(self):
            self.x = 0
            self.y = 0
        def move(self, dx, dy, maze):
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT and maze[new_y][new_x] != 1:
                self.x = new_x
                self.y = new_y
        def draw(self, screen):
            pygame.draw.rect(screen, GRAY, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    class Timer:
        def __init__(self, countdown_time):
            self.font = pygame.font.SysFont(None, 36)
            self.start_time = pygame.time.get_ticks()
            self.countdown_time = countdown_time  # Time in seconds
        def get_time(self):
            elapsed_time = pygame.time.get_ticks() - self.start_time
            remaining_time = self.countdown_time - elapsed_time // 1000
            if remaining_time < 0:
                remaining_time = 0
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            return f"Time: {minutes:02}:{seconds:02}"
        def draw(self, screen):
            time_text = self.font.render(self.get_time(), True, BLACK)
            screen.blit(time_text, (10, 600))
        def is_time_up(self):
            elapsed_time = pygame.time.get_ticks() - self.start_time
            remaining_time = self.countdown_time - elapsed_time // 1000
            return remaining_time <= 0

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont(None, 36)
    font2 = pygame.font.SysFont(None, 100)
    pygame.display.set_caption("Pygame window")
    display_instructions(screen)
    clock = pygame.time.Clock()
    countdown_time = 15
    timer = Timer(countdown_time)
    maze = [[0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1],
                [1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0],
                [0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1],
                [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                [1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1],
                [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0],
                [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1],
                [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                [0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0],
                [1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1],
                [1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0],
                [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 2]]
    player = Player()
    jailyn = pygame.image.load('Assets/jailyn.jpg')
    jailyn = pygame.transform.scale(jailyn, (CELL_SIZE,CELL_SIZE))
    running = True
    won = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.move(0, -1, maze)
                elif event.key == pygame.K_DOWN:
                    player.move(0, 1, maze)
                elif event.key == pygame.K_LEFT:
                    player.move(-1, 0, maze)
                elif event.key == pygame.K_RIGHT:
                    player.move(1, 0, maze)
        screen.fill(WHITE)
        draw_maze(screen, maze, jailyn)
        player.draw(screen)
        timer.draw(screen)
        if maze[player.y][player.x] == 2:
            won = True
            running = False
        if timer.is_time_up():
            running = False
        pygame.display.flip()
        clock.tick(30)
    screen.fill(WHITE)
    if won:
        time_text = font2.render('You Won!', True, RED)
        screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, SCREEN_HEIGHT // 2 - time_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        return

    else:
        time_text = font2.render('Time is up!', True, BLACK)
        screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, SCREEN_HEIGHT // 2 - time_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        return

if __name__ == "__main__":
    main()



