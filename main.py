import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Title and icon
pygame.display.set_caption('POP - Space Invaders')
icon = pygame.image.load('images/main-pic.jpg')
pygame.display.set_icon(icon)

# Adding background image
background = pygame.image.load('images/background-image.jpg')

# Adding background music
mixer.music.load('audio/background.mp3')
mixer.music.set_volume(0.05)
mixer.music.play(-1)

# Adding score to the game window
score_value = 0
font = pygame.font.SysFont("freesansbold.ttf", 32)
scoreX = 10
scoreY = 10

# Game-Over font
game_over_font = pygame.font.SysFont("freesansbold.ttf", 64)

# Adding player image
player_ship = pygame.image.load('images/space_ship.png')
playerX = 370
playerY = 500
playerX_change = 0

# Adding enemy image
enemy_ship = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 3

for i in range(num_of_enemies):
    enemy_ship.append(pygame.image.load('images/enemy_ship.png'))
    enemyX.append(random.randint(64, 800 - 64))
    enemyY.append(random.randint(30, 70))
    enemyX_change.append(0.5)
    enemyY_change.append(20)

# Adding bullet
bullet_icon = pygame.image.load('images/bullet.png')
bulletX = playerX
bulletY = playerY
bulletX_change = 0
bulletY_change = 2
bullet_state = 'ready'


def player(x, y):
    screen.blit(player_ship, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_ship[i], (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_icon, (x + 15, y + 15))


def display_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_display():
    game_over_text = game_over_font.render("GAME OVER!!!", True, (255, 255, 255))
    screen.blit(game_over_text, (200, 255))


def isCollision(x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    return distance < 40


# Game Loop
running = True
while running:

    # To keep the background color
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # To loop all the events in the game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Moving the player with the LEFT and RIGHT keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 1.5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bulletX = playerX
                    bullet(bulletX, bulletY)
                    bullet_sound = mixer.Sound('audio/laser.wav')
                    bullet_sound.play()
                    bullet_sound.set_volume(0.1)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Boundary checks for player
    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX > (800 - 64):
        playerX = 800 - 64

    # player ship
    player(playerX, playerY)

    # enemy_ship
    for i in range(num_of_enemies):
        # Check if Game Over
        if enemyY[i] > 500:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_display()
            break

        # Boundary checks for enemy
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= (800 - 64):
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        enemyX[i] += enemyX_change[i]

        enemy(enemyX[i], enemyY[i], i)

        # Checking for collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # explosion_sound
            explosion_sound = mixer.Sound('audio/explosion.wav')
            explosion_sound.set_volume(0.05)
            explosion_sound.play()

            bulletY = playerY
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(64, 800 - 64)
            enemyY[i] = random.randint(30, 70)

    # Bullet movement
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = 'ready'

    if bullet_state == 'fire':
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # display score
    display_score(scoreX, scoreY)

    # To always update the display
    pygame.display.update()
