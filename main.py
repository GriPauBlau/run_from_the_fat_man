import pygame
import math
import random

pygame.init()

p1_score = 0
p2_score = 0

size_x = 2 * 1280
size_y = 2 * 720
win = pygame.display.set_mode((size_x, size_y))
pygame.display.set_caption("Run from the Fat Man")

player1X = 100
player1Y = 100
baddyX = 300
baddyY = 300
player2X = 100
player2Y = 100
circle_centre_x = random.random() * size_x
circle_centre_y = random.random() * size_y
extra_centre = (circle_centre_x, circle_centre_y)
extra_radius = 10
win_circle_x = 1100
win_circle_y = 100
win_circle = (win_circle_x, win_circle_y)
vel = 20
baddyVel = 10

run = True


def draw_game():
    win.fill((0, 0, 0))
    pygame.draw.rect(win, (226, 31, 255), (player1X, player1Y, 20, 20))
    pygame.draw.rect(win, (31, 226, 255), (player2X, player2Y, 20, 20))
    pygame.draw.rect(win, (0, 250, 0), (baddyX, baddyY, 40, 40))
    pygame.draw.circle(win, (250, 0, 0), extra_centre, extra_radius)
    pygame.draw.circle(win, (255, 255, 255), win_circle, 30, 30)
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


while run:
    pygame.time.delay(100)
    h1 = distance(player1X, player1Y, baddyX, baddyY)
    h2 = distance(player2X, player2Y, baddyX, baddyY)
    # Baddy position
    if h1 < h2:
        # chase player1
        baddyX, baddyY = chase(player1X, player1Y, baddyX, baddyY)
        if run:
            print("Exit Player 1")
            p1_score -= 2
    elif h1 > h2:
        # chase player2
        baddyX, baddyY = chase(player2X, player2Y, baddyX, baddyY)
        if not run:
            p2_score -= 2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    # player position 1
    if keys[pygame.K_a] and player1X >= 20:
        player1X -= vel

    if keys[pygame.K_d] and player1X <= size_x - 40:
        player1X += vel

    if keys[pygame.K_w] and player1Y >= 20:
        player1Y -= vel

    if keys[pygame.K_s] and player1Y <= size_y - 40:
        player1Y += vel

    # player 2 position
    if keys[pygame.K_LEFT] and player2X >= 20:
        player2X -= vel

    if keys[pygame.K_RIGHT] and player2X <= size_x - 40:
        player2X += vel

    if keys[pygame.K_UP] and player2Y >= 20:
        player2Y -= vel

    if keys[pygame.K_DOWN] and player2Y <= size_y - 40:
        player2Y += vel
    draw_game()

    if abs(baddyY - player1Y) < 30 and abs(baddyX - player1X) < 30:
        run = False
    if abs(baddyY - player2Y) < 30 and abs(baddyX - player2X) < 30:
        run = False

    if distance(player1X, player1Y, circle_centre_x, circle_centre_y) < 30:
        circle_centre_x = random.random() * size_x
        circle_centre_y = random.random() * size_y
        extra_centre = (circle_centre_x, circle_centre_y)
        p1_score += 1

    if distance(player2X, player2Y, circle_centre_x, circle_centre_y) < 30:
        circle_centre_x = random.random() * size_x
        circle_centre_y = random.random() * size_y
        extra_centre = (circle_centre_x, circle_centre_y)
        p2_score += 1

    if distance(player1X, player1Y, win_circle_x, win_circle_y) < 40 and p1_score >= 5:
        run = False
    if distance(player2X, player2Y, win_circle_x, win_circle_y) < 40 and p2_score >= 5:
        run = False
        if p1_score > p2_score:
            print("Player 1 wins!")
        elif p2_score > p1_score:
            print("Player 2 wins!")

print("p1_score: ", p1_score)
print("p2_score: ", p2_score)
pygame.quit()
