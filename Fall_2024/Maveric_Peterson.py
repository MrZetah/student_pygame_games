import pygame
from pygame.locals import *
import sys
pygame.font.init()

def main():
    #2 - Define constants
    FARTMANPATH = 'Assets/fart man-1.png.png'
    FARTMAN = pygame.image.load(FARTMANPATH)
    FARTWALK1 = pygame.image.load('Assets/fart man-2.png.png') #
    FARTWALK2 = pygame.image.load('Assets/fartWalk2.png.png') #
    BFARTWALK1 = pygame.image.load('Assets/backWalk1.png.png') #
    BFARTWALK2 = pygame.image.load('Assets/backWalk2.png.png') #
    FARTJUMP = pygame.image.load('Assets/FARTJUMP.png.png') #
    FARTFALL = pygame.image.load('Assets/FARTFALL.png.png') #
    GOOM = pygame.image.load('Assets/goon.png.png') #
    DEADGOOM = pygame.image.load('Assets/deadGuy.png.png') #
    DEADFART = pygame.image.load('Assets/DEADFARTMAN.png.png') #
    NOTHING = pygame.image.load('Assets/nothing.png.png')
    WHALE = pygame.image.load('Assets/WHALE.png.png')
    RFARTJUMP = pygame.image.load('Assets/RFATJUMP.png.png')
    LFARTFALL = pygame.image.load('Assets/LFARTFALL.png.png')
    WHALE2 = pygame.image.load('Assets/WHALE2.png.png')
    DEADWHALE = pygame.image.load('Assets/DWHALE.png.png')
    MARTIN = pygame.image.load('Assets/MARTIN.png.png')
    BULLETT = pygame.image.load('Assets/Bullet.png.png')
    MART2LIVES= pygame.image.load('Assets/2livesleftMART.png.png')
    MART1LIFE = pygame.image.load('Assets/MARTONELIVELEFT.png.png')
    DEADMART = pygame.image.load('Assets/DEADMARTIN.png.png')
    SPAGET = pygame.image.load('Assets/SPAGETTI.png')
    MOVE = 10
    GRAV = 1  # gravity acceleration
    UPJUMP = -20  # how high
    NEWS = 2 # How much inertia works (momentum decay)
    BLACK = (0, 0, 0)
    GRAVBLUE = (255, 145, 242)
    LTBLUE = (0, 255, 255)
    YELLOW = (255, 255, 0)
    BLUE = (0, 0, 255)
    ORANGE = (255, 128, 0)
    PURPLE = (128, 0, 255)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)
    BROWN = (180, 82, 0)
    TAN =(255, 210, 145)
    RED = (255, 0, 0)
    WINH = 600
    WINW = 1100
    FPS = 60
    OBLUE = (0, 166, 255) # o means other
    WMOVE = 3
    RRED =(255, 86, 44)
    GOLD = (255, 182, 0)
    x = 0

    FONT = pygame.font.SysFont('Arial', 20)
    BADMOVE = 3
    DEAD = False
    # # # ## # #

    # THIS IS A NOTE TO MYSELF, MAKE A MAIN MENU AND MAKE AN ENDLESS MODE WHERE YOU STAY IN THE SAME STAGE AND ENEMIES KEEP COMING!!!!! ###



    # Modify the main game loop

    # Declare the list to hold the bullets
    bullets = []

    # Function to shoot bullets
    def shoot_bullet():
        # Create a bullet at Martin's position, moving towards the player
        bullet = pygame.Rect(martRect.x + martRect.width, martRect.y + martRect.height // 2, 3, 3)
        bullets.append(bullet)

    # # ## ## # ### # # ## #
    def game_over():

        INSTRUCTIONS_FONT = pygame.font.SysFont('Arial', 20)
        draw_text = INSTRUCTIONS_FONT.render("Game Over", 100, BLACK)
        WIN.blit(draw_text, (WINW//2 - draw_text.get_width()//2, WINH//2 - draw_text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(5000)
        WIN.fill(BLACK)
        return

    INSTRUCTIONS_FONT = pygame.font.SysFont('Arial', 40)
    FOONT = pygame.font.SysFont('Arial', 45)
    #3 - Initialize the world
    pygame.init()
    WIN = pygame.display.set_mode((WINW, WINH))
    clock = pygame.time.Clock()
    # Display Instructions
    duration = 10000
    INSTRUCTIONS_FONT = pygame.font.SysFont('Arial', 20)
    start_ticks = pygame.time.get_ticks()
    should_break = False
    while pygame.time.get_ticks() - start_ticks < duration:
        if should_break:
            break
        WIN.fill(WHITE)
        instructions = ['Created by Maveric Peterson',
        'Press enter to skip at any time',
        'WASD to move, your name is Fart Man',
        'Your really good at farting',
        'an evil guy named martin stole your spagetii-o\'s',
        'YOU HAVE TO STOP HIM FROM EATING THEM',
        'E to use your special if you have a power up']
        for i, instruction in enumerate(instructions):
            draw_text = INSTRUCTIONS_FONT.render(instruction, 1, BLACK)
            WIN.blit(draw_text, (WINW//2 - draw_text.get_width()//2, 100 + i *50))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    should_break = True
                    break
        pygame.display.update()
    WIN.fill(BLACK)
    #4 - Initialize variables
    stage = 1
    upMove = 0  # Vertical speed of the player
    isJumping = False
    gravity = True
    newtonL = False  # Inertia (misspelled)
    newtonR = False
    falling = False
    downing = False
    goingDown = True
    onTop = False
    poop = True # sorry there just had to be a varible nammed poop, it has nothing to do with poop,
    downTime = False # poop is there for platform jumping stuff
    WHALEP = WHALE
    wPic = False
    news = NEWS
    downFrame = 0
    llastY = 0
    llastX = 0
    spedOmart = 120
    walk_frame = 0
    badGuyH = 60
    badGuyW = 96
    lives = 1
    whaleFrames = 0
    crackFrames = 0
    marMove = 2
    lastY = 0  # To track the last y position to detect downward movement
    # p means player #
    player = pygame.Rect(9, -60, 91, 96)
    ground = pygame.Rect(0, WINH - 150, WINW, 1000)
    martRect = pygame.Rect(970, ground.y - player.height, 91, 96)
    badGuyrect = pygame.Rect(700, ground.y - badGuyH, badGuyW, badGuyH)
    badGuyrect2 = pygame.Rect(1100, ground.y - badGuyH, badGuyW, badGuyH)
    spaRect = pygame.Rect(400, 50, 462, 600)
    baad = [spaRect]
    fakerect = pygame.Rect(1100, 10000 - 96, 1, 1)
    bb = [badGuyrect, badGuyrect2]
    marFrames = 0
    bbpopped = []
    badFlyrect = pygame.Rect(1000, 100, 300, 170)
    badFlyrect2 = pygame.Rect(800, 300, 300, 170)
    bb2 = [badFlyrect, badFlyrect2]
    bb2popped = []
    footZone = pygame.Rect(player.x + 10, player.y + player.height + 200, player.width - 20, 40)
    platJump = False
    platform = pygame.Rect(170, player.height + 200, 500, 20)
    platformGrav = pygame.Rect(170, player.height + 200 + 2000, 500, 20 + 200000)
    mart = [martRect]
    beans = False
    time = True
    win = False
    lastpX = 0
    lastpY = 0
    swip = True
    MARTPIC = MARTIN
    martLives = 3
    # Velocity variables
    x_velocity = 0  # Horizontal velocity (momentum)
    horizontal_acceleration = MOVE  # Speed at which the player moves when a key is pressed

    # Walking animation frame counter
    Rwalk_frame = 0
    Rwalking = False  # Is the player moving right
    Lwalking = False
    martLive = True
    # Frame delay for alternating walk images (e.g., 10 frames delay)
    frame_delay = 10
    current_frame = 0  # Counter for frames before switching images

    #  # for whale movement

    #6 - Define functions

    #7 - Loop forever
    while True:
        if DEAD == True:
            game_over()
            return
        #8 Check for and handle events
        for event in pygame.event.get():
            #Check to see if user has quit the game
            if event.type == pygame.QUIT:
                return
            #Press the 'q' key as an option to quit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return
                if event.key == pygame.K_w and not isJumping:
                    upMove = UPJUMP  # Set the upward velocity
                    isJumping = True  # Player starts jumping
                    if onTop:
                        platJump = True

            if event.type == pygame.KEYUP:
                pass  # We don't need to handle key releases here since we're using momentum

        #9 - Do any "per frame" actions (move objects, add or remove items)

        if player.y + player.height < ground.y and gravity:
            player.y += GRAV
            GRAV += 1

        if isJumping:  # Apply gravity and jumping if the player is jumping
            upMove += GRAV  # Increase downward velocity due to gravity
            player.y += upMove  # Update the player's vertical position

            # Check if player is falling

        if lastY < player.y:  # If lastY is greater than current y, player is falling
            falling = True
          # Update lastY to the current position to track movement
        lastY = player.y
        if player.y + player.height > ground.y:
            player.y = ground.y - player.height

        if player.y == ground.y - player.height:
            GRAV = 1
            gravity = False
            isJumping = False
            falling = False  # Reset falling when player lands on the ground

        # Horizontal movement with momentum
        keys = pygame.key.get_pressed()  # if you want the keys held
        if keys[pygame.K_s]:
            downing = True
            downTime = True


        if keys[pygame.K_d]:
            x_velocity = horizontal_acceleration
            Rwalking = True  # Player is moving right
        elif keys[pygame.K_a]:
            x_velocity = -horizontal_acceleration
            Lwalking = True  # Player is moving left
        else:
            # Apply inertia (gradually slow down if no key is pressed)
            if x_velocity > 0:
                x_velocity -= news  # Slow down to the left
            elif x_velocity < 0:
                x_velocity += news  # Slow down to the right

            # Stop completely if velocity is very small
            if abs(x_velocity) < 0.5:
                x_velocity = 0
                Lwalking = False  # Player is not moving anymore
                Rwalking = False

        player.x += x_velocity  # Apply horizontal velocity

        # Change the walk_frame if the player is walking
        if Rwalking or Lwalking:
            current_frame += 1

        # Only change the image after a certain number of frames (frame delay)
        if current_frame >= frame_delay:
            walk_frame += 1
            current_frame = 0  # Reset the frame counter
        if llastY == player.y:
            falling = False
        # Alternate between FARTWALK1 and FARTWALK2 for walking animation
        if falling and Lwalking:
            current_image = LFARTFALL
        elif falling == True:
            current_image = FARTFALL
        elif Rwalking and not isJumping and not falling:
            if walk_frame % 2 == 0:
                current_image = FARTWALK1
            else:
                current_image = FARTWALK2
        elif Lwalking and not isJumping and not falling:
            if walk_frame % 2 == 0:
                current_image = BFARTWALK1
            else:
                current_image = BFARTWALK2
        elif isJumping and Lwalking and not falling:
            current_image = RFARTJUMP

        elif isJumping and Rwalking and not falling:
            current_image = FARTJUMP
        elif isJumping:
            current_image = FARTJUMP

        else:
            current_image = FARTMAN  # When not moving, show the standing image
        for i in range((len(bb))):
            bad = bb[(i - 1)]
            bad.x -= BADMOVE
            if bad.x < 0:
                BADMOVE = -BADMOVE
            if bad.x > WINW + bad.width:
                BADMOVE = -BADMOVE
            if footZone.colliderect(bad) and player.colliderect(bad):
                bbpopped.append(bad)
                bb.pop(i - 1)
                lives += 1
            elif player.colliderect(bad):
                lives -= 1
            WIN.blit(GOOM, bad)
        footZone.x = player.x + 10
        footZone.y = player.y + player.height - 20

        if lives <= 0:
            DEAD = True
        for i in range(len(bbpopped)):
            bad = bbpopped[(i - 1)]
            bad.y += 5
            bad.x -= 5
            if bad.y > WINH + 500:
                bbpopped.pop(i - 1)
        if player.x > WINW + player.width + 20 and swip:
            stage += 1
            player.x = 0 - player.width
            if stage == 4:
                player.y = ground.y + player.height
        if player.x < 0 - player.width - 1 and swip:
            stage -= 1
            if stage == 3:
                ground.y = WINH - 150
                player.y = ground.y + player.height
            player.x = WINW + player.width + 19
        if stage > 1:
            bb = []
        if stage == 2:
            for i in range(len(bb2)):
                bad = bb2[(i - 1)]
                bad.x += WMOVE
                if bad.x > 500:
                    WMOVE = -WMOVE
                if bad.x < WINW:
                    WMOVE = -WMOVE
                if footZone.colliderect(bad) and player.colliderect(bad):
                    bb2popped.append(bad)
                    bb2.pop(i - 1)
                    lives += 1
                elif player.colliderect(bad):
                    lives -= 1
                whaleFrames += 1
        lastpY = player.y
        lastpX = player.x
        if martLive and stage == 3:
            if player.x >= WINW:
                player.x = llastX - player.width
        if stage == 3:
            if player.x > WINW:
                pass
            if footZone.colliderect(martRect) and player.colliderect(martRect) and martLives > 1:
                martLives -= 1
                lives += 1
                player.y = -1000
                player.x = 96
                martRect.x = 970
                marFrames = 0
                if martLives == 2:
                    marMove = 4
                if martLives == 1:
                    marMove = 8
                bullets = []
            elif footZone.colliderect(martRect) and player.colliderect(martRect) and martLives == 1:
                martLives -= 1
                lives += 1000000
                bullets = []
            elif player.colliderect(martRect):
                    lives -= 100



                # Handle platform interaction

        if stage == 2 and player.y + player.height <= platform.y and not downing and platform.x + platform.width >= player.x and player.x > platform.x - player.width and poop:
            onTop = True
            player.y = llastY

            upMove = 0
            gravity = False
            isJumping = False
            falling = False

        elif onTop and not (platform.x + platform.width >= player.x and player.x > platform.x - player.width) and player.y < (player.y * 2.5):
            gravity = True
            isJumping = True
            falling = True
            onTop = False
        if onTop and player.y < platform.y - player.height:
            player.y += 1
        if onTop and platJump:
            upMove = UPJUMP  # Set the upward velocity
            isJumping = True  # Player starts jumping
            onTop = False
            poop = False
            crackFrames += 1
        else:
            poop = True
        if crackFrames == 10:
            platJump = False
            crackFrames = 0
        if not onTop and llastY == player.y and stage == 2 and player.y + player.height == ground.y and downing:
            gravity = True
            isJumping = True
            falling = True
            onTop = False


        if downing:
            # If player is holding down 'S', allow them to fall through the platform
            player.y += GRAV  # Continue falling through platform when pressing 'S'
            GRAV += 1  # Increase gravity if the player is falling through
            onTop = False
        llastY = player.y
        llastX = player.x
        if downTime:
            downFrame += 1
            if downFrame == 20:
                downTime = False
                downing = False
                downFrame = 0

        stage == 3




        if martLives == 3:
            spedOmart = 64
        if martLives == 2:
            spedOmart = 32
        if martLives == 1:
            spedOmart = 16
            bullet.x -= 3


        if stage == 3:
            for mar in mart:
                if martLives > 0:
                    mar.x -= marMove
                    marFrames += 1
                    if marFrames % spedOmart == 0:
                        marMove = -marMove
                    if not beans and marFrames % (spedOmart // 2) == 0:
                        shoot_bullet()
                    if marFrames % spedOmart == 0:
                        beans = not beans
                else:
                    mar.x -= 5
                    mar.y += 5
                    martLive = False
                if mar.x > 1000:
                    mart.pop(mar)
        for bullet in bullets:
            bullet.x -= 5

            # Check for collision with player
            if player.colliderect(bullet):
                lives -= 1  # Reduce lives when bullet hits the player

            # Remove the bullet if it goes off the screen
            if bullet.x < 0:
                bullets.remove(bullet)

        for bad in baad:
            if player.colliderect(bad) and stage == 4:
                win = True

        #10 - Clear the window ##### # # above put per frame actions
        if stage == 1:
            WIN.fill(LTBLUE)
        if stage == 2:
            WIN.fill(OBLUE)
        if stage == 3:
            WIN.fill(RRED)
        if stage == 4:
            WIN.fill(LTBLUE)
            ground.y = WINH - 40
            bullets = []
        #11 - Draw all window elements
        if stage == 4:
            for bad in baad:
                WIN.blit(SPAGET, bad)
        for bullet in bullets:
            WIN.blit(BULLETT, bullet)
        if stage == 2:
            pygame.draw.rect(WIN, GRAVBLUE, platformGrav)
        pygame.draw.rect(WIN, BROWN, ground)
        if DEAD:
            current_image = DEADFART
        WIN.blit(current_image, player)
        for bad in bb:
            WIN.blit(GOOM, bad)
        for bad in bbpopped:
            WIN.blit(DEADGOOM, bad)
        if stage == 2:
            pygame.draw.rect(WIN, TAN, platform)
        if whaleFrames % 5 == 0:
            wPic = not wPic
        if wPic:
            WHALEP = WHALE
        else:
            WHALEP = WHALE2
        if stage == 2:
            for bad in bb2:
                for b in bad:
                    WIN.blit(WHALEP, bad)
        for i in range(len(bb2popped)):
            bad = bb2popped[(i - 1)]
            bad.y += 5
            bad.x -= 5
            if bad.y > WINH + 500:
                bb2popped.pop(i - 1)
            WIN.blit(DEADWHALE, bad)
        if martLives == 3:
            MARTPIC = MARTIN
        if martLives == 2:
            MARTPIC = MART2LIVES
        if martLives == 1:
            MARTPIC = MART1LIFE
        if martLives == 0:
            MARTPIC = DEADMART
        if stage == 3:
            for i in range(len(mart)):
                bad = mart[i - 1]
                WIN.blit(MARTPIC, bad)
                # pygame.draw.rect(WIN, GREEN, bad)
        if stage == 4:
            swip = False
        # # # un comment these to see fart man's hitbox # # #
        #pygame.draw.rect(WIN, RED, player)
        #pygame.draw.rect(WIN, GREEN, footZone)

        if stage == 2:
            draw_text = INSTRUCTIONS_FONT.render('Uh oh, Martin is messing up the gravity!', 500, BLACK)
            WIN.blit(draw_text, (300, 100))
        '''
        if win:
            draw_text = INSTRUCTIONS_FONT.render(f'TRUE', 500, GREEN)
            WIN.blit(draw_text, (WINW//2 - draw_text.get_width()//2, WINH//2 - draw_text.get_height()//2))
        else:
            draw_text = INSTRUCTIONS_FONT.render('FALSE', 500, RED)
            WIN.blit(draw_text, (WINW//2 - draw_text.get_width()//2, WINH//2 - draw_text.get_height()//2))
           '''

        if win:
            carbs = FOONT.render("YOU WON, YOU SAVED THE SPAGETT-O'S!!", 100, BLACK)
            WIN.blit(carbs, (WINW//2 - carbs.get_width()//2, WINH//2 - carbs.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            return

        ##### put stuff that are on every stage ABOVE here #####
        #if stage == 1:
           # bb.append(turd)

        #12 - Update the window
        pygame.display.update()

        #13 - Set frame rate to slow things down
        clock.tick(FPS)




if __name__ == "__main__":
    main()
# chipoliaoili
