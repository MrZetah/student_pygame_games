import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Constants
FPS = 60
Wind_Hei, Wind_Leng = 500, 800
Bla = (0, 0, 0)
Whi = (255, 255, 255)
Red = (255, 0, 0)
Blue = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player Attributes
cha_x, cha_y = 375, 220
cha_wid, cha_hei = 30, 25
cha_sped, rot_sped = 3, 5
ang = 0
player_health = 10

# Bullet Attributes
bul_sped = 5
bullets = []

# Enemy Attributes
enemies = []
enemy_rects = []
enemy_bullets = []
spawn_timer = 0



# Utility Functions
def calculate_angle(source_x, source_y, target_x, target_y):
    # Calculate angle between two points.
    return math.degrees(math.atan2(target_y - source_y, target_x - source_x))

def spawn_enemy():
    # Spawn a new enemy.
    enemy_type = random.choice([1, 2])
    x = random.randint(50, Wind_Leng - 50)
    y = random.randint(50, Wind_Hei - 50)
    health = 2 if enemy_type == 1 else 3
    return {"x": x, "y": y, "type": enemy_type, "health": health, "shoot_cooldown": 0}

def clamp(value, min_val, max_val):
    # Clamp a value between min and max.
    return max(min_val, min(value, max_val))

# Main Game Loop
def main():
        # Load Images
    try:
        Player = pygame.image.load('Assets/Gun_Guy_Ship.png.png')
        Enemy1 = pygame.image.load('Assets/Big_Rawr_Enemy_With_PewPew.png.png')
        Enemy2 = pygame.image.load('Assets/Big_Rawr_Enemy.png.png')
    except pygame.error as e:
        print(f"Error: Could not load an image. {e}")
        sys.exit()

    # Initialize Window
    window = pygame.display.set_mode((Wind_Leng, Wind_Hei))
    pygame.display.set_caption("Survive")
    pygame.display.update()
    clock = pygame.time.Clock()

    global cha_x, cha_y, ang, player_health, spawn_timer
    duration = 10000
    INSTRUCTIONS_FONT = pygame.font.SysFont('comicsans', 20)
    start_ticks = pygame.time.get_ticks()
    should_break = False
    while pygame.time.get_ticks() - start_ticks < duration:
        if should_break:
            break
        window.fill(WHITE)
        instructions = ['Created by Marcus Brown',
        'Press enter to skip at any time',
        'Use left/right arrow keys to rotate player',
        'Use w and s key to move forward and back',
        'Use space bar to fire bullets',
        'Survive as long as possible']
        for i, instruction in enumerate(instructions):
            draw_text = INSTRUCTIONS_FONT.render(instruction, 1, BLACK)
            window.blit(draw_text, (Wind_Leng//2 - draw_text.get_width()//2, 100 + i *50))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    should_break = True
                    break
        pygame.display.update()
    window.fill(BLACK)
    running = True
    char = pygame.Rect(cha_x, cha_y, cha_wid, cha_hei)

    # Time
    start_time = pygame.time.get_ticks()
    font = pygame.font.SysFont('comicsans', 20)


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullet_x = cha_x + cha_wid // 2
                bullet_y = cha_y + cha_hei // 2
                bullets.append({"x": bullet_x, "y": bullet_y, "angle": ang + 90})

        # Handle Key Presses
        keys = pygame.key.get_pressed()
        '''
        if keys[pygame.K_SPACE]:
            bullet_x = cha_x + cha_wid // 2
            bullet_y = cha_y + cha_hei // 2
            bullets.append({"x": bullet_x, "y": bullet_y, "angle": ang + 90})
        '''
        if keys[pygame.K_LEFT]:
            ang += rot_sped
        if keys[pygame.K_RIGHT]:
            ang -= rot_sped
        if keys[pygame.K_w]:
            cha_x += cha_sped * math.cos(math.radians(ang + 90))
            cha_y -= cha_sped * math.sin(math.radians(ang + 90))
        if keys[pygame.K_s]:
            cha_x -= cha_sped * math.cos(math.radians(ang + 90))
            cha_y += cha_sped * math.sin(math.radians(ang + 90))

        # Keep Player Within Bounds
        cha_x = clamp(cha_x, 0, Wind_Leng - cha_wid)
        cha_y = clamp(cha_y, 0, Wind_Hei - cha_hei)
        char.topleft = (cha_x, cha_y)

        # Rotate Player
        rotated_player = pygame.transform.rotate(Player, ang)
        rotated_rect = rotated_player.get_rect(center=char.center)




        # Update Bullets
        for bullet in bullets[:]:
            bullet["x"] += bul_sped * math.cos(math.radians(bullet["angle"]))
            bullet["y"] -= bul_sped * math.sin(math.radians(bullet["angle"]))
            if bullet["x"] < 0 or bullet["x"] > Wind_Leng or bullet["y"] < 0 or bullet["y"] > Wind_Hei:
                bullets.remove(bullet)

        # Spawn New Enemies
        spawn_timer -= 1
        if spawn_timer <= 0:
            spawn_timer = random.randint(100, 180)  # Spawn interval
            enemies.append(spawn_enemy())

        # Update Enemies
        for enemy in enemies[:]:
            angle_to_player = calculate_angle(enemy["x"], enemy["y"], cha_x, cha_y)
            if enemy["type"] == 1:
                if enemy["shoot_cooldown"] <= 0:
                    # Type 1 enemy shoots at player
                    enemy_bullets.append({"x": enemy["x"], "y": enemy["y"], "angle": angle_to_player})
                    enemy["shoot_cooldown"] = random.randint(90, 150)
                else:
                    enemy["shoot_cooldown"] -= 1
            else:  # Type 2 enemies move slowly toward the player
                enemy["x"] += 1.5 * math.cos(math.radians(angle_to_player))
                enemy["y"] += 1.5 * math.sin(math.radians(angle_to_player))

            # Check for Bullet Collision
            for bullet in bullets[:]:
                if pygame.Rect(bullet["x"], bullet["y"], 5, 5).colliderect(
                        pygame.Rect(enemy["x"], enemy["y"], 38, -90)):
                    enemy["health"] -= 1
                    bullets.remove(bullet)
                    if enemy["health"] <= 0:
                        enemies.remove(enemy)

            # Check for Collision with Player
            if pygame.Rect(enemy["x"], enemy["y"], 30, 30).colliderect(char):
                player_health -= 2 if enemy["type"] == 2 else 1
                player_health = clamp(player_health, 0, 10)
                enemies.remove(enemy)
                if player_health <= 0:
                    print("Game Over!")
                    running = False

        # Update Enemy Bullets
        for bullet in enemy_bullets[:]:
            bullet["x"] += bul_sped * math.cos(math.radians(bullet["angle"]))
            bullet["y"] += bul_sped * math.sin(math.radians(bullet["angle"]))
            if pygame.Rect(bullet["x"], bullet["y"], 5, 5).colliderect(char):
                player_health -= 1
                player_health = clamp(player_health, 0, 10)
                enemy_bullets.remove(bullet)
                if player_health <= 0:
                    print("Game Over!")
                    running = False
            elif bullet["x"] < 0 or bullet["x"] > Wind_Leng or bullet["y"] < 0 or bullet["y"] > Wind_Hei:
                enemy_bullets.remove(bullet)

        # Render Everything
        window.fill(Whi)
        window.blit(rotated_player, rotated_rect.topleft)

         # Timer
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        timer_text = font.render(f'Time: {elapsed_time}', True, Bla)
        window.blit(timer_text, (Wind_Leng - 100, 10))


        # Draw Player Bullets
        for bullet in bullets:
            pygame.draw.rect(window, Bla, (bullet["x"], bullet["y"], 5, 5))


        # Draw Enemies
        for enemy in enemies:
            angle_to_player = calculate_angle(enemy["x"], enemy["y"], cha_x, cha_y)
            enemy_image = Enemy1 if enemy["type"] == 1 else Enemy2
            rotated_enemy = pygame.transform.rotate(enemy_image, -angle_to_player)
            enemy_rect = rotated_enemy.get_rect(center=(enemy["x"], enemy["y"]))
            window.blit(rotated_enemy, enemy_rect.topleft)



        # Draw Enemy Bullets
        for bullet in enemy_bullets:
            pygame.draw.rect(window, Red, (bullet["x"], bullet["y"], 5, 5))

        # Display Player Health
        font = pygame.font.SysFont('comicsans', 20)
        health_text = font.render(f'Health: {player_health}', True, Bla)
        window.blit(health_text, (10, 10))


        pygame.display.update()
        clock.tick(FPS)

    pygame.time.delay(3000)
    return round(elapsed_time)

if __name__ == "__main__":
    main()


'''
Asteroids type game

        Player = pygame.image.load('/Users/brownmar001/Library/CloudStorage/OneDrive-rocori.k12.mn.us/Python/Unit 8/Gun_Guy_Ship.png.png')
        Enemy1 = pygame.image.load('/Users/brownmar001/Library/CloudStorage/OneDrive-rocori.k12.mn.us/Python/Unit 8/Big_Rawr_Enemy_With_PewPew.png.png')
        Enemy2 = pygame.image.load('/Users/brownmar001/Library/CloudStorage/OneDrive-rocori.k12.mn.us/Python/Unit 8/Big_Rawr_Enemy.png.png')
'''
