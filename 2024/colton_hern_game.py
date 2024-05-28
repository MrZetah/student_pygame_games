import pygame

def game():

    pygame.init()

    WIDTH, HEIGHT = 1100, 750
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("The Game")

    HEALTH_FONT = pygame.font.SysFont("comicsans", 21)
    PLAYER_HEALTH_FONT = pygame.font.SysFont("times_new_roman", 50)
    WINNER_FONT = pygame.font.SysFont('calibri', 140)

    ENEMY_HIT = pygame.USEREVENT + 1
    PLAYER_HIT = pygame.USEREVENT + 2
    DOOR_ADVANCE = pygame.USEREVENT + 3
    PINK_HIT = pygame.USEREVENT + 4
    GREEN_HIT = pygame.USEREVENT + 5
    GREEN_HIT = pygame.USEREVENT + 6

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    SILVER = (192, 192, 192)
    RED = (255, 0, 0)
    AQUA = (0, 255, 255)
    BLUE = (0, 100, 255)

    PLAYER_WIDTH, PLAYER_HEIGHT = 75, 75

    BAD_WIDTH, BAD_HEIGHT = 70, 70

    PINK_SLIME_WIDTH, PINK_SLIME_HEIGHT = 32*2, 26*2

    GREEN_SLIME_WIDTH, GREEN_SLIME_HEIGHT = 32*2, 32*2

    DASH_DISTANCE = 135

    ATTACK_WIDTH, ATTACK_HEIGHT = 50, 50

    CHARACTER_IMAGE = pygame.image.load("images/plage_doctor.png")
    CHARACTER_IMAGE = pygame.transform.scale(CHARACTER_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT))

    VEL = 6
    ATTACK_VEL = 7

    MAX_ATTACKS = 2

    FPS = 60

    FIREBALL_PIC = pygame.transform.scale(
        pygame.image.load("images/fire.gif"), (ATTACK_HEIGHT, ATTACK_HEIGHT)
    )

    BAD_GUY = pygame.transform.scale(
        pygame.image.load("images/blob.gif"), (BAD_WIDTH, BAD_HEIGHT))

    PINK_SLIME = pygame.transform.scale(
        pygame.image.load("images/slime.png"), (PINK_SLIME_WIDTH, PINK_SLIME_HEIGHT))

    GREEN_SLIME = pygame.transform.scale(
        pygame.image.load("images/funny_slime.gif"), (GREEN_SLIME_WIDTH, GREEN_SLIME_HEIGHT))

    BAD_GUY_GHOST = pygame.transform.scale(
        pygame.image.load("images/ghost.gif"), (BAD_WIDTH, BAD_HEIGHT)
    )

    ENTRANCE = pygame.transform.scale(
        pygame.image.load("images/door.png"), (54, 160)
    )

    CHEST = pygame.transform.scale(
        pygame.image.load("images/tresure.png"), (50, 50)
    )

    BACKGROUND = pygame.transform.scale(
        pygame.image.load("images/tile.png"), (WIDTH * 2, HEIGHT)
    )

    END_SCREEN = pygame.transform.scale(
        pygame.image.load("images/end_screen.png"), (WIDTH//2, HEIGHT)
    )

    FLOOR = pygame.transform.scale(
        pygame.image.load("images/floor_block.png"), (50, 50)
    )

    def endgame():
        game_over = pygame.Rect(WIDTH//4, 0, END_SCREEN.get_width(), END_SCREEN.get_height())
        over = "You Won!!!"
        winner = WINNER_FONT.render(over, 1, BLUE)
        WIN.fill(BLACK)
        WIN.blit(END_SCREEN, game_over)
        WIN.blit(winner, (WIDTH//2 - winner.get_width()//2, HEIGHT - winner.get_height()))
        pygame.display.update()
        pygame.time.delay(3000)
        return

    def draw_winner(winner_text):
        draw_text = WINNER_FONT.render(winner_text, 1, RED)
        WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
        pygame.display.update()

    def screen_shift(wall, yep, floor, door):
        if yep < 176:
            wall.x -= VEL
        if yep < 176:
            door.x -= VEL

    def handle_attack(
        attack,
        attacks_up,
        attacks_down,
        attacks_left,
        attacks_right,
        pink_slime,
        green_slime,
        enemy,):
        for attack in attacks_right:
            attack.x += ATTACK_VEL
            if enemy.colliderect(attack):
                pygame.event.post(pygame.event.Event(ENEMY_HIT))
                attacks_right.remove(attack)
            if pink_slime.colliderect(attack):
                pygame.event.post(pygame.event.Event(PINK_HIT))
                attacks_right.remove(attack)
            if green_slime.colliderect(attack):
                pygame.event.post(pygame.event.Event(GREEN_HIT))
                attacks_right.remove(attack)
            elif attack.x > WIDTH:
                attacks_right.remove(attack)

        for attack in attacks_left:
            attack.x -= ATTACK_VEL
            if enemy.colliderect(attack):
                pygame.event.post(pygame.event.Event(ENEMY_HIT))
                attacks_left.remove(attack)
            if pink_slime.colliderect(attack):
                pygame.event.post(pygame.event.Event(PINK_HIT))
                attacks_left.remove(attack)
            if green_slime.colliderect(attack):
                pygame.event.post(pygame.event.Event(GREEN_HIT))
                attacks_left.remove(attack)
            elif attack.x < 0:
                attacks_left.remove(attack)

        for attack in attacks_up:
            attack.y -= ATTACK_VEL
            if enemy.colliderect(attack):
                pygame.event.post(pygame.event.Event(ENEMY_HIT))
                attacks_up.remove(attack)
            if pink_slime.colliderect(attack):
                pygame.event.post(pygame.event.Event(PINK_HIT))
                attacks_up.remove(attack)
            if green_slime.colliderect(attack):
                pygame.event.post(pygame.event.Event(GREEN_HIT))
                attacks_up.remove(attack)
            elif attack.y < 0:
                attacks_up.remove(attack)

        for attack in attacks_down:
            attack.y += ATTACK_VEL
            if enemy.colliderect(attack):
                pygame.event.post(pygame.event.Event(ENEMY_HIT))
                attacks_down.remove(attack)
            if pink_slime.colliderect(attack):
                pygame.event.post(pygame.event.Event(PINK_HIT))
                attacks_down.remove(attack)
            if green_slime.colliderect(attack):
                pygame.event.post(pygame.event.Event(GREEN_HIT))
                attacks_down.remove(attack)
            elif attack.y > HEIGHT:
                attacks_down.remove(attack)

    def dash(event, keys_pressed, dashes, player, time, floor):
        if event.type == pygame.KEYDOWN:
            if (
                keys_pressed[pygame.K_a]
                and player.x + player.width > floor.width
                and event.key == pygame.K_RSHIFT
                and player.x - DASH_DISTANCE > floor.width
                and len(dashes) < 1
                and player.x + DASH_DISTANCE > floor.width
            ):  # Left
                for i in range(16):
                    player.x -= i
                dashes.append("")
                time = 0
            if (
                keys_pressed[pygame.K_d]
                and player.x + player.width < WIDTH - floor.width
                and event.key == pygame.K_RSHIFT
                and len(dashes) < 1
                and player.x + player.width + DASH_DISTANCE < WIDTH - floor.width
            ):  # Right
                player.x += VEL
                for i in range(16):
                    player.x += i
                dashes.append("")
                time = 0
            if (
                keys_pressed[pygame.K_w]
                and player.y - DASH_DISTANCE > floor.height
                and event.key == pygame.K_RSHIFT
                and len(dashes) < 1
                and player.y + player.height + DASH_DISTANCE > floor.height
            ):  # Up
                for i in range(16):
                    player.y -= i
                dashes.append("")
                time = 0
            if (
                keys_pressed[pygame.K_s]
                and event.key == pygame.K_RSHIFT
                and player.y + player.height < HEIGHT - floor.height
                and len(dashes) < 1
                and player.y + player.height + DASH_DISTANCE < HEIGHT - floor.height
            ):
                for i in range(16):
                    player.y += i
                dashes.append("")
                time = 0

            if len(dashes) >= 1 and time >= FPS//2:
                dashes.remove("")
        return time

    def enemies_Y(enemy, time, floor, BAD_VEL_X, BAD_VEL_Y):

        if enemy.x < floor.width:
            BAD_VEL_X = -BAD_VEL_X
            # print(1)

        if enemy.y < floor.height:
            BAD_VEL_Y = -BAD_VEL_Y
            # print(2)
        if enemy.x > (WIDTH - enemy.width - floor.width):
            BAD_VEL_X = -BAD_VEL_X
            # print(3)
        if enemy.y > (HEIGHT - enemy.height - floor.height):
            BAD_VEL_Y = -BAD_VEL_Y
            # print(4)

        enemy.x += BAD_VEL_X
        enemy.y += BAD_VEL_Y

        return BAD_VEL_Y

    def enemies_X(enemy, time, floor, BAD_VEL_X, BAD_VEL_Y):

        if enemy.x < floor.width:
            BAD_VEL_X = -BAD_VEL_X
            # print(1)
        if enemy.y < floor.height:
            BAD_VEL_Y = -BAD_VEL_Y
            # print(2)
        if enemy.x + enemy.width > WIDTH - floor.width:
            BAD_VEL_X = -BAD_VEL_X
            # print(3)
        if enemy.y > (HEIGHT - enemy.height - floor.height):
            BAD_VEL_Y = -BAD_VEL_Y
            # print(4)

        enemy.x += BAD_VEL_X
        enemy.y += BAD_VEL_Y

        return BAD_VEL_X

    def pink_slime_X(pink_slime, time, floor, PINK_SPRINTER_VEL_X, PINK_SPRINTER_VEL_Y):

        if pink_slime.x < floor.width:
            PINK_SPRINTER_VEL_X = -PINK_SPRINTER_VEL_X
            # print(1)
        if pink_slime.y < floor.height:
            PINK_SPRINTER_VEL_Y = -PINK_SPRINTER_VEL_Y
            # print(2)
        if pink_slime.x + pink_slime.width > WIDTH - floor.width:
            PINK_SPRINTER_VEL_X = -PINK_SPRINTER_VEL_X
            # print(3)
        if pink_slime.y > (HEIGHT - pink_slime.height - floor.height):
            PINK_SPRINTER_VEL_Y = -PINK_SPRINTER_VEL_Y
            # print(4)

        pink_slime.x += PINK_SPRINTER_VEL_X
        pink_slime.y += PINK_SPRINTER_VEL_Y

        return PINK_SPRINTER_VEL_X

    def pink_slime_Y(pink_slime, time, floor, PINK_SPRINTER_VEL_X, PINK_SPRINTER_VEL_Y):

        if pink_slime.x < floor.width:
            PINK_SPRINTER_VEL_X = -PINK_SPRINTER_VEL_X
            # print(1)
        if pink_slime.y < floor.height:
            PINK_SPRINTER_VEL_Y = -PINK_SPRINTER_VEL_Y
            # print(2)
        if pink_slime.x + pink_slime.width > WIDTH - floor.width:
            PINK_SPRINTER_VEL_X = -PINK_SPRINTER_VEL_X
            # print(3)
        if pink_slime.y > (HEIGHT - pink_slime.height - floor.height):
            PINK_SPRINTER_VEL_Y = -PINK_SPRINTER_VEL_Y
            # print(4)

        pink_slime.x += PINK_SPRINTER_VEL_X
        pink_slime.y += PINK_SPRINTER_VEL_Y

        return PINK_SPRINTER_VEL_Y

    def green_slime_Y(green_slime, time, floor, GREEN_SPRINTER_VEL_X, GREEN_SPRINTER_VEL_Y):

        if green_slime.x < floor.width:
            GREEN_SPRINTER_VEL_X = -GREEN_SPRINTER_VEL_X
            # print(1)
        if green_slime.y < floor.height:
            GREEN_SPRINTER_VEL_Y = -GREEN_SPRINTER_VEL_Y
            # print(2)
        if green_slime.x + green_slime.width > WIDTH - floor.width:
            GREEN_SPRINTER_VEL_X = -GREEN_SPRINTER_VEL_X
            # print(3)
        if green_slime.y > (HEIGHT - green_slime.height - floor.height):
            GREEN_SPRINTER_VEL_Y = -GREEN_SPRINTER_VEL_Y
            # print(4)

        green_slime.x += GREEN_SPRINTER_VEL_X
        green_slime.y += GREEN_SPRINTER_VEL_Y

        return GREEN_SPRINTER_VEL_Y

    def green_slime_X(green_slime, time, floor, GREEN_SPRINTER_VEL_X, GREEN_SPRINTER_VEL_Y):

        if green_slime.x < floor.width:
            GREEN_SPRINTER_VEL_X = -GREEN_SPRINTER_VEL_X
            # print(1)
        if green_slime.y < floor.height:
            GREEN_SPRINTER_VEL_Y = -GREEN_SPRINTER_VEL_Y
            # print(2)
        if green_slime.x + green_slime.width > WIDTH - floor.width:
            GREEN_SPRINTER_VEL_X = -GREEN_SPRINTER_VEL_X
            # print(3)
        if green_slime.y > (HEIGHT - green_slime.height - floor.height):
            GREEN_SPRINTER_VEL_Y = -GREEN_SPRINTER_VEL_Y
            # print(4)

        green_slime.x += GREEN_SPRINTER_VEL_X
        green_slime.y += GREEN_SPRINTER_VEL_Y

        return GREEN_SPRINTER_VEL_X

    def draw_window(
        wall,
        floor,
        player,
        enemy,
        pink_slime,
        green_slime,
        door,
        yep,
        boi,
        bruh,
        exp,
        attack,
        attacks_up,
        attacks_down,
        attacks_left,
        attacks_right,
        ENEMY_HEALTH,
        PLAYER_HEALTH,
        PINK_HEALTH,
        GREEN_HEALTH,
        tresure
    ):

        WIN.blit(BACKGROUND, wall)

        draw_borders(floor)
        player_health_text = PLAYER_HEALTH_FONT.render(f"Health: {str(PLAYER_HEALTH)}", 1, AQUA)
        WIN.blit(player_health_text, (10, 0))
        if ENEMY_HEALTH > 0:
            enemy_health_text = HEALTH_FONT.render(f"Health: {str(ENEMY_HEALTH)} / 5", 1, RED)
            WIN.blit(enemy_health_text,
                (
                    enemy.x - ATTACK_HEIGHT // 2,
                    enemy.y - enemy.height // 2,
                    ATTACK_HEIGHT,
                    ATTACK_WIDTH,),)
            WIN.blit(BAD_GUY, (enemy.x, enemy.y))
        else:
            WIN.blit(BAD_GUY_GHOST, (enemy.x, enemy.y))

        if yep >= 175 and PINK_HEALTH > 0:
            pink_health_text = HEALTH_FONT.render(f"Health: {str(PINK_HEALTH)} / 5", 1, RED)
            WIN.blit(pink_health_text,
                (
                    pink_slime.x - ATTACK_HEIGHT // 2,
                    pink_slime.y - pink_slime.height // 2,
                    ATTACK_HEIGHT,
                    ATTACK_WIDTH,),)
            WIN.blit(PINK_SLIME, (pink_slime.x, pink_slime.y))
        else:
            WIN.blit(BAD_GUY_GHOST, (pink_slime.x, pink_slime.y))


        if yep >= 175 and GREEN_HEALTH > 0:
            green_health_text = HEALTH_FONT.render(f"Health: {str(GREEN_HEALTH)} / 5", 1, RED)
            WIN.blit(green_health_text,
                (
                    green_slime.x - ATTACK_HEIGHT // 2,
                    green_slime.y - green_slime.height // 2,
                    ATTACK_HEIGHT,
                    ATTACK_WIDTH,),)
            WIN.blit(GREEN_SLIME, (green_slime.x, green_slime.y))
        else:
            WIN.blit(BAD_GUY_GHOST, (green_slime.x, green_slime.y))


        if exp + boi + bruh == 3:
            WIN.blit(CHEST, (tresure.x, tresure.y))

        WIN.blit(CHARACTER_IMAGE, (player.x - 10, player.y))

        WIN.blit(ENTRANCE, (door.x, door.y))

        for attack in attacks_up:
            WIN.blit(FIREBALL_PIC, attack)

        for attack in attacks_down:
            WIN.blit(FIREBALL_PIC, attack)

        for attack in attacks_left:
            WIN.blit(FIREBALL_PIC, attack)

        for attack in attacks_right:
            WIN.blit(FIREBALL_PIC, attack)

        pygame.display.update()

    def draw_borders(floor):
        for i in range((WIDTH) // floor.width):
            WIN.blit(FLOOR, ((0 + (i * floor.width), floor.y)))
        for a in range((WIDTH) // floor.width):
            WIN.blit(FLOOR, ((0 + (a * floor.width), 0)))
        for b in range(HEIGHT // floor.height):
            WIN.blit(FLOOR, ((0, 0 + (b * floor.height))))
        for b in range(6):
            WIN.blit(FLOOR, (((WIDTH - floor.width), 0 + (b * floor.height))))
        for b in range(6):
            WIN.blit(
                FLOOR,(((
                            WIDTH - (floor.width),
                            (HEIGHT // 2)
                            + floor.height
                            + (floor.height // 2)
                            + (b * floor.height),))),)

    def player_movement(player, keys_pressed, floor):
        if keys_pressed[pygame.K_a] and player.x > floor.width:  # Left
            player.x -= VEL

        if (
            keys_pressed[pygame.K_d] and player.x + player.width < WIDTH - floor.width
        ):  # Right
            player.x += VEL

        if keys_pressed[pygame.K_w] and player.y > floor.height:  # Up
            player.y -= VEL

        if (
            keys_pressed[pygame.K_s] and player.y + player.height < HEIGHT - floor.height
        ):  # Down
            player.y += VEL

    def positioning_pink(pink_slime):
        pink_slime = pygame.Rect(WIDTH - (WIDTH // 5), HEIGHT - HEIGHT // 3, PINK_SLIME_WIDTH, PINK_SLIME_HEIGHT)

        return pink_slime

    def positioning_green(green_slime):
        green_slime = pygame.Rect(WIDTH - (WIDTH // 5),HEIGHT // 3, GREEN_SLIME_WIDTH, GREEN_SLIME_HEIGHT)

        return green_slime

    def positioning_tresure(tresure, floor):
        tresure = pygame.Rect(WIDTH - floor.width - tresure.width, HEIGHT//2, 50, 50)

        return tresure

    def main():
        time = 0

        exp = 0

        yep = 0

        tick = 0

        boi = 0

        bruh = 0
        wall = pygame.Rect(0, 0, BACKGROUND.get_width(), BACKGROUND.get_height())
        player = pygame.Rect(WIDTH // 5, HEIGHT // 2, PLAYER_WIDTH - 10, PLAYER_HEIGHT)
        floor = pygame.Rect(0, HEIGHT - 50, FLOOR.get_width(), FLOOR.get_height())
        door = pygame.Rect(
            WIDTH - ENTRANCE.get_width(),
            (HEIGHT // 2) - (ENTRANCE.get_height() // 2),
            ENTRANCE.get_width(),
            ENTRANCE.get_height(),)
        enemy = pygame.Rect(WIDTH - (WIDTH // 4), HEIGHT // 2, BAD_WIDTH, BAD_HEIGHT)
        tresure = pygame.Rect(-50, -50, 50, 50)

        pink_slime = pygame.Rect(-100, -100, PINK_SLIME_WIDTH, PINK_SLIME_HEIGHT)
        green_slime = pygame.Rect(-100, -100, GREEN_SLIME_WIDTH, GREEN_SLIME_HEIGHT)

        dashes = []

        attacks_down = []
        attacks_up = []
        attacks_left = []
        attacks_right = []

        attack = ""

        ENEMY_HEALTH = 5
        PLAYER_HEALTH = 5
        PINK_HEALTH = 5
        GREEN_HEALTH = 5

        BAD_VEL_X = 3.5
        BAD_VEL_Y = 3.5

        PINK_SPRINTER_VEL_X = -4.5
        PINK_SPRINTER_VEL_Y = -4.5

        GREEN_SPRINTER_VEL_X = 4.5
        GREEN_SPRINTER_VEL_Y = 4.5

        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run == False
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and len(attacks_left) < MAX_ATTACKS:  # Left
                        attack = pygame.Rect(
                            player.x - player.width - 5,
                            player.y + player.height // 2 - ATTACK_HEIGHT // 2,
                            ATTACK_HEIGHT,
                            ATTACK_WIDTH,
                        )
                        attacks_left.append(attack)

                    if (
                        event.key == pygame.K_RIGHT and len(attacks_right) < MAX_ATTACKS
                    ):  # Right
                        attack = pygame.Rect(
                            player.x + player.width + 5,
                            player.y + player.height // 2 - ATTACK_HEIGHT // 2,
                            ATTACK_HEIGHT,
                            ATTACK_WIDTH,
                        )
                        attacks_right.append(attack)

                    if event.key == pygame.K_UP and len(attacks_up) < MAX_ATTACKS:  # Up
                        attack = pygame.Rect(
                            player.x + player.width // 2 - ATTACK_HEIGHT // 2,
                            player.y - player.height - 5,
                            ATTACK_HEIGHT,
                            ATTACK_WIDTH,
                        )
                        attacks_up.append(attack)

                    if event.key == pygame.K_DOWN and len(attacks_down) < MAX_ATTACKS:  # Down
                        attack = pygame.Rect(
                            player.x + player.width // 2 - ATTACK_HEIGHT // 2,
                            player.y + player.height + 5,
                            ATTACK_HEIGHT,
                            ATTACK_WIDTH,
                        )
                        attacks_down.append(attack)

                if event.type == ENEMY_HIT:
                    ENEMY_HEALTH -= 1

                if event.type == PINK_HIT:
                    PINK_HEALTH -= 1

                if event.type == GREEN_HIT:
                    GREEN_HEALTH -= 1

                if PINK_HEALTH <= 0 and boi <= 0:
                    boi += 1

                if GREEN_HEALTH <= 0 and bruh <= 0:
                    bruh += 1

                if ENEMY_HEALTH <= 0 and exp <= 0:
                    exp += 1

                if event.type == PLAYER_HIT and time > 30:
                    PLAYER_HEALTH -= 1
                    time = 0

                if event.type == DOOR_ADVANCE and exp == 1:
                    yep += 1
                    screen_shift(wall, yep, floor, door)

            if exp >= 1 and yep >= 175 and tick <= 0:
                pink_slime = positioning_pink(pink_slime)
                green_slime = positioning_green(green_slime)
                tick += 1

            if exp + boi + bruh == 3 and tresure.x < 0:
                tresure = positioning_tresure(tresure, floor)

            if player.colliderect(enemy):
                pygame.event.post(pygame.event.Event(PLAYER_HIT))

            if player.colliderect(pink_slime):
                pygame.event.post(pygame.event.Event(PLAYER_HIT))

            if player.colliderect(green_slime):
                pygame.event.post(pygame.event.Event(PLAYER_HIT))

            if player.colliderect(door):
                pygame.event.post(pygame.event.Event(DOOR_ADVANCE))

            if player.colliderect(tresure) and exp + boi + bruh == 3:
                endgame()
                return


            if PLAYER_HEALTH <= 0:
                winner_text = "Game Over"
                draw_winner(winner_text)
                run == False
                pygame.time.delay(2000)
                return

            keys_pressed = pygame.key.get_pressed()

            time = dash(event, keys_pressed, dashes, player, time, floor)

            player_movement(player, keys_pressed, floor)

            BAD_VEL_X = enemies_X(enemy, time, floor, BAD_VEL_X, BAD_VEL_Y)
            BAD_VEL_Y = enemies_Y(enemy, time, floor, BAD_VEL_X, BAD_VEL_Y)

            PINK_SPRINTER_VEL_X = pink_slime_X(pink_slime, time, floor, PINK_SPRINTER_VEL_X, PINK_SPRINTER_VEL_Y)
            PINK_SPRINTER_VEL_Y = pink_slime_Y(pink_slime, time, floor, PINK_SPRINTER_VEL_X, PINK_SPRINTER_VEL_Y)

            GREEN_SPRINTER_VEL_X = green_slime_X(green_slime, time, floor, GREEN_SPRINTER_VEL_X, GREEN_SPRINTER_VEL_Y)
            GREEN_SPRINTER_VEL_Y = green_slime_Y(green_slime, time, floor, GREEN_SPRINTER_VEL_X, GREEN_SPRINTER_VEL_Y)

            handle_attack(
                attack,
                attacks_up,
                attacks_down,
                attacks_left,
                attacks_right,
                pink_slime,
                green_slime,
                enemy,
            )

            draw_window(
                wall,
                floor,
                player,
                enemy,
                pink_slime,
                green_slime,
                door,
                yep,
                boi,
                bruh,
                exp,
                attack,
                attacks_up,
                attacks_down,
                attacks_left,
                attacks_right,
                ENEMY_HEALTH,
                PLAYER_HEALTH,
                PINK_HEALTH,
                GREEN_HEALTH,
                tresure
            )

            time += 1

    main()

if __name__ == "__main__":
    game()
