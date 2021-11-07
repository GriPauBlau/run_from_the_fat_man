import pygame
import math

pygame.init()
win = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Run from the Fat Man")

player1X = 100
player1Y = 100
baddyX = 300
baddyY = 300
player2X = 100
player2Y = 100
extra_centre = (500, 500)
extra_radius = 20
vel = 20
baddyVel = 10
run = True

def draw_game():
    win.fill((0, 0, 0))
    pygame.draw.rect(win, (226, 31, 255), (player1X, player1Y, 20, 20))
    pygame.draw.rect(win, (31, 226, 255), (player2X, player2Y, 20, 20))
    pygame.draw.rect(win, (0, 250, 0), (baddyX, baddyY, 40, 40))
    pygame.draw.circle(win, (250, 0, 0), extra_centre, extra_radius)
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
    else:
        run = False

    return chaser_x, chaser_y


while run:
    pygame.time.delay(50)
    h1 = distance(player1X, player1Y, baddyX, baddyY)
    h2 = distance(player2X, player2Y, baddyX, baddyY)
    # Baddy position
    if h1 < h2:
        # chase player1
        baddyX, baddyY = chase(player1X, player1Y, baddyX, baddyY)
    elif h1 > h2:
        # chase player2
        if baddyX < player2X - 10:
            baddyX = baddyX + baddyVel
            draw_game()
        elif baddyX > player2X + 10:
            draw_game()
            baddyX = baddyX - baddyVel
        elif baddyY < player2Y - 10:
            baddyY = baddyY + baddyVel
        elif baddyY > player2Y + 10:
            baddyY = baddyY - baddyVel
        else:
            run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    # player position 1
    if keys[pygame.K_a]:
        player1X -= vel

    if keys[pygame.K_d]:
        player1X += vel

    if keys[pygame.K_w]:
        player1Y -= vel

    if keys[pygame.K_s]:
        player1Y += vel

    # player 2 position
    if keys[pygame.K_LEFT]:
        player2X -= vel

    if keys[pygame.K_RIGHT]:
        player2X += vel

    if keys[pygame.K_UP]:
        player2Y -= vel

    if keys[pygame.K_DOWN]:
        player2Y += vel
    draw_game()

    if abs(baddyY - player1Y) < 30 and abs(baddyX - player1X) < 30:
        run = False

    if abs(baddyY - player2Y) < 30 and abs(baddyX - player2X) < 30:
        run = False

pygame.quit()




