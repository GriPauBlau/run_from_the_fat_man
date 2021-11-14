# A game with pygame

import pygame
import math
import random

pygame.init()

# Define colours for the game
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (226, 31, 255)
LIGHT_BLUE = (31, 226, 255)
GREEN = (0, 250, 0)
RED = (250, 0, 0)


# Define screen size
SCREEN_WIDTH = 2 * 1280
SCREEN_HEIGHT = 2 * 720

# Set up screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Add the name of the game on the window top banner
pygame.display.set_caption("Run from the Fat Man")

# Initiate game variables
# Scores
p1_score = 0
p2_score = 0

# Player definitions
# Player 1
player1X = 100
player1Y = 100
P1Vel = 20

# Player 2
player2X = 100
player2Y = 100
P2Vel = 20

# Baddy
baddyX = 300
baddyY = 300
baddyVel = 10

# Prize
circle_centre_x = random.random() * SCREEN_WIDTH
circle_centre_y = random.random() * SCREEN_HEIGHT
extra_centre = (circle_centre_x, circle_centre_y)
extra_radius = 10

# Winning circle
win_circle_x = 1100
win_circle_y = 100
win_circle = (win_circle_x, win_circle_y)

running = True

# Definition of functions for the game
def draw_game():
    # Draw a black background
    screen.fill(BLACK)
    # Draw a surface
    surf = pygame.Surface((150, 150))
    surf.fill(WHITE)
    # rect = surf.get_rect()
    screen.blit(surf, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    pygame.display.flip()

    # Draws the game players and elements
    pygame.draw.rect(screen, PINK, (player1X, player1Y, 20, 20))
    pygame.draw.rect(screen, LIGHT_BLUE, (player2X, player2Y, 20, 20))
    pygame.draw.rect(screen, GREEN, (baddyX, baddyY, 40, 40))
    pygame.draw.circle(screen, RED, extra_centre, extra_radius)
    pygame.draw.circle(screen, WHITE, win_circle, 30, 30)
    pygame.display.update()


def distance(x, y, a, b):
    x1 = abs(x - a)
    y1 = abs(y - b)
    h = math.sqrt(x1 ** 2 + y1 ** 2)
    return h


def chase(x, y, chaser_x, chaser_y):
    if chaser_x < x - 10:
        chaser_x += baddyVel
        draw_game()
    elif chaser_x > x + 10:
        draw_game()
        chaser_x -= baddyVel
    elif chaser_y < y - 10:
        chaser_y += baddyVel
    elif chaser_y > y + 10:
        chaser_y -= baddyVel

    return chaser_x, chaser_y


# Main game loop ----
while running:
    pygame.time.delay(100)
    h1 = distance(player1X, player1Y, baddyX, baddyY)
    h2 = distance(player2X, player2Y, baddyX, baddyY)
    # Baddy position
    if h1 < h2:
        # chase player1
        baddyX, baddyY = chase(player1X, player1Y, baddyX, baddyY)
        # if running:
        #     print("Exit Player 1")
        #     p1_score -= 2
    elif h1 > h2:
        # chase player2
        baddyX, baddyY = chase(player2X, player2Y, baddyX, baddyY)
        # if not running:
        #     p2_score -= 2

    # Manage quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    keys = pygame.key.get_pressed()

    # player position 1
    if keys[pygame.K_a] and player1X >= 20:
        player1X -= P1Vel

    if keys[pygame.K_d] and player1X <= SCREEN_WIDTH - 40:
        player1X += P1Vel

    if keys[pygame.K_w] and player1Y >= 20:
        player1Y -= P1Vel

    if keys[pygame.K_s] and player1Y <= SCREEN_HEIGHT - 40:
        player1Y += P1Vel

    # player 2 position
    if keys[pygame.K_LEFT] and player2X >= 20:
        player2X -= P2Vel

    if keys[pygame.K_RIGHT] and player2X <= SCREEN_WIDTH - 40:
        player2X += P2Vel

    if keys[pygame.K_UP] and player2Y >= 20:
        player2Y -= P2Vel

    if keys[pygame.K_DOWN] and player2Y <= SCREEN_HEIGHT - 40:
        player2Y += P2Vel
    draw_game()

    if abs(baddyY - player1Y) < 30 and abs(baddyX - player1X) < 30:
        running = False
    if abs(baddyY - player2Y) < 30 and abs(baddyX - player2X) < 30:
        running = False

    if distance(player1X, player1Y, circle_centre_x, circle_centre_y) < 30:
        circle_centre_x = random.random() * SCREEN_WIDTH
        circle_centre_y = random.random() * SCREEN_HEIGHT
        extra_centre = (circle_centre_x, circle_centre_y)
        p1_score += 1

    if distance(player2X, player2Y, circle_centre_x, circle_centre_y) < 30:
        circle_centre_x = random.random() * SCREEN_WIDTH
        circle_centre_y = random.random() * SCREEN_HEIGHT
        extra_centre = (circle_centre_x, circle_centre_y)
        p2_score += 1

    if distance(player1X, player1Y, win_circle_x, win_circle_y) < 40 and p1_score >= 5:
        running = False

    if distance(player2X, player2Y, win_circle_x, win_circle_y) < 40 and p2_score >= 5:
        running = False

if p1_score > p2_score and (p2_score >= 5 or p1_score >=5):
    print("Player 1 wins!")
elif p2_score > p1_score and (p2_score >= 5 or p1_score >=5):
    print("Player 2 wins!")

print("p1_score: ", p1_score)
print("p2_score: ", p2_score)
pygame.quit()
