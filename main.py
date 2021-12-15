import pygame
import random
import math

from pygame import mixer

# initialise pygame
pygame.init()
running = True

# colors

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 255)

# creating the screen for game

screen = pygame.display.set_mode((800, 600))
# background
background = pygame.image.load("background.jpg")
# welcome_img =pygame.image.load("start.jpg")

# backgroun sound
mixer.music.load("background_song.mp3")
mixer.music.play(-1)

# title and icons

pygame.display.set_caption("Space_Invaders")
icon = pygame.image.load("rocket1.png")
pygame.display.set_icon(icon)  # adding icon on the title bar of softonic icon

# playes
playerimg = pygame.image.load("spaceship.png")
playerx = 370  # x_axis value
playery = 480  # y_axis value
playerx_change = 0
playery_change = 0

# enemy

enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load("enemy2.png"))
    enemyx.append(random.randint(0, 735))  # x_axis value
    enemyy.append(random.randint(50, 150))  # y_axis value
    enemyx_change.append(0.3)
    enemyy_change.append(10)

# bullet

# ready = you cant see the bullet on screen
# fire  = bullet is in the state of motion  and we can  see
bulletimg = pygame.image.load("bullet.png")
bulletx = 0  # x_axis value
bullety = 480  # because spaceship is at 480 pixel position at the starting
bulletx_change = 0
bullety_change = 1
bullet_state = "ready"

# score

score_value = 0
font = pygame.font.Font('justBubble.ttf', 32)
textx = 10
texty = 10

# game Over text

gameOver_text = pygame.font.Font('justBubble.ttf', 80)


def game_over():
    last_call = gameOver_text.render(" GAME OVER ", True, red)
    screen.blit(last_call, (200, 240))


def showscore(x, y):
    score = font.render("Score :" + str(score_value), True, white)
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerimg, (x, y))  # blit() function is used to draw something on screen


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))  # blit() function is used to draw something on screen


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (
        x + 16,
        y + 10))  # we add 16 so that our bullet appears o the centre of spaceship not on the corners of spaceship


def iscollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2)))
    if distance < 27:
        return True
    else:
        return False


# welcome
def screen_score(text, color, x, y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, [x, y])

    # start  =pygame.image.load("start.jpg")

    # welcome_page


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # whenever the quit button is press we simply out from our while loop
            running = False
        # Now we will check whether which key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerx_change = +0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":  # first it check whether the bullet is already on screen or not , if it already on screen than it won't fire again until it com back in ready state
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletx = playerx  # so that our bullet do not foloow aour space ship
                    fire_bullet(bulletx, bullety)
        # now if we put off the fingure from the keys then it will chane like the way given below
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerx_change = 0
            if event.key == pygame.K_RIGHT:
                playerx_change = 0

    screen.fill(black)
    # backgroun image
    screen.blit(background, (0, 0))

    # checking for boundries of spaceship  ,so it dien't go out of boundries
    playerx += playerx_change

    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736
    # bullet movement
    if bullety < 0:
        bullety = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change
    # checking for boundries for enemy spaceship , so that it doesn't go ut of the biundries

    for i in range(num_of_enemies):

        # game Over

        if enemyy[i] > 400:
            for j in range(num_of_enemies):
                enemyy[j] = 2000

            game_over()
            # running  = False

            break
        enemyx[i] += enemyx_change[i]

        if enemyx[i] <= 0:
            enemyx_change[i] = 0.3
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx_change[i] = -0.3
            enemyy[i] += enemyy_change[i]
        # checking for collion
        collision = iscollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bullety = 480
            bullet_state = "ready"
            score_value += 10

            # print(score)
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(50, 150)

        enemy(enemyx[i], enemyy[i], i)

    player(playerx,
           playery)  # should be called after screen.fill method otherwise  ,our player won't be visible
    showscore(textx, texty)

    pygame.display.update()  # add to update display otherwise screen won't update



pygame.quit()
