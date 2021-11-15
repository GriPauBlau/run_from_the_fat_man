# A game with pygame

import pygame
import math
import random

# Import pygame.locals for easier access to key coordinates

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_RIGHT,
    K_LEFT,
    K_a,
    K_s,
    K_d,
    K_w,
    K_ESCAPE,
    KEYDOWN,
    QUIT
    )


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
extra_radius = 30

# Winning circle
win_circle_x = 1100
win_circle_y = 100
win_circle = (win_circle_x, win_circle_y)

running = True


# Definition of functions for the game
class Player(pygame.sprite.Sprite):
    def __init__(self, colour, movement_keys):
        super(Player, self).__init__()
        self.colour = colour
        self.surf = pygame.Surface((20, 20))
        self.surf.fill(self.colour)
        self.movement_keys = movement_keys
        self.rect = self.surf.get_rect(
            # Make the position random
            center=(
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self, keys):
        if keys[self.movement_keys['up']]:
            self.rect.move_ip(0, -5)
        if keys[self.movement_keys['down']]:
            self.rect.move_ip(0, 5)
        if keys[self.movement_keys['left']]:
            self.rect.move_ip(-5, 0)
        if keys[self.movement_keys['right']]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Baddy(pygame.sprite.Sprite):
    def __init__(self, colour):
        super(Baddy, self).__init__()
        self.colour = colour
        self.surf = pygame.Surface((40, 40))
        self.surf.fill(self.colour)
        self.rect = self.surf.get_rect(
            # Make the position random
            center=(
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
            )
        )


class Prize(pygame.sprite.Sprite):
    def __init__(self, colour):
        super(Prize, self).__init__()
        # self.colour = colour
        # self.surf = pygame.Surface((20, 20))
        self.surf = pygame.image.load("red_ball3.png").convert()
        # self.surf.fill(self.colour)
        self.rect = self.surf.get_rect(
            # Make the position random
            center = (
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

        # self.surf.set_colorkey(GREEN, RLEACCEL)
        # self.mask = pygame.mask.from_surface(self.surf)


def draw_game(player1, player2, baddy, prize):
    # Draw a black background
    screen.fill(BLACK)

    # Draws the game players and elements
    # Player 1
    screen.blit(player1.surf, player1.rect)

    # Player 2
    screen.blit(player2.surf, player2.rect)

    # Baddy
    screen.blit(baddy.surf, baddy.rect)

    # Prize
    screen.blit(prize.surf, prize.rect)

    # Exit
    # pygame.draw.circle(screen, WHITE, win_circle, 30, 30)

    # Update the display
    pygame.display.flip()


# def distance(x, y, a, b):
#     x1 = abs(x - a)
#     y1 = abs(y - b)
#     h = math.sqrt(x1 ** 2 + y1 ** 2)
#     return h


# def chase(x, y, chaser_x, chaser_y):
#     if chaser_x < x - 10:
#         chaser_x += baddyVel
#         draw_game()
#     elif chaser_x > x + 10:
#         draw_game()
#         chaser_x -= baddyVel
#     elif chaser_y < y - 10:
#         chaser_y += baddyVel
#     elif chaser_y > y + 10:
#         chaser_y -= baddyVel

#     return chaser_x, chaser_y

# Instantiate players
player1 = Player(PINK,
                 {'up': K_w,
                  'down': K_s,
                  'left': K_a,
                  'right': K_d})

player2 = Player(LIGHT_BLUE,
                 {'up': K_UP,
                  'down': K_DOWN,
                  'left': K_LEFT,
                  'right': K_RIGHT})

# Instantiate foe
baddy = Baddy(GREEN)

# Instantiate a prize
prize = Prize(RED)

# Main game loop ----
while running:
    pygame.time.delay(10)

    # Manage quitting the game
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False


    # Capture keys that get pressed
    keys = pygame.key.get_pressed()

    # Update the position of the players
    player1.update(keys)
    player2.update(keys)

    # Draw the new frame
    draw_game(player1, player2, baddy, prize)

    # Check if any enemies have collided with the player
    if pygame.sprite.collide_rect(player2, prize):
        # If so, then remove the player and stop the loop
        prize.kill()
        prize = Prize(RED)
        screen.blit(prize.surf, prize.rect)
        # running = False

    screen.fill(BLACK)

    # h1 = distance(player1X, player1Y, baddyX, baddyY)
    # h2 = distance(player2X, player2Y, baddyX, baddyY)

    # # Baddy position
    # if h1 < h2:
    #     # chase player1
    #     baddyX, baddyY = chase(player1X, player1Y, baddyX, baddyY)
    # elif h1 > h2:
    #     # chase player2
    #     baddyX, baddyY = chase(player2X, player2Y, baddyX, baddyY)
    # if abs(baddyY - player1Y) < 30 and abs(baddyX - player1X) < 30:
    #     running = False
    # if abs(baddyY - player2Y) < 30 and abs(baddyX - player2X) < 30:
    #     running = False

    # if distance(player1X, player1Y, circle_centre_x, circle_centre_y) < 30:
    #     circle_centre_x = random.random() * SCREEN_WIDTH
    #     circle_centre_y = random.random() * SCREEN_HEIGHT
    #     extra_centre = (circle_centre_x, circle_centre_y)
    #     p1_score += 1

    # if distance(player2X, player2Y, circle_centre_x, circle_centre_y) < 30:
    #     circle_centre_x = random.random() * SCREEN_WIDTH
    #     circle_centre_y = random.random() * SCREEN_HEIGHT
    #     extra_centre = (circle_centre_x, circle_centre_y)
    #     p2_score += 1

    # if distance(player1X, player1Y, win_circle_x, win_circle_y) < 40 and p1_score >= 5:
    #     running = False

    # if distance(player2X, player2Y, win_circle_x, win_circle_y) < 40 and p2_score >= 5:
    #     running = False


if p1_score > p2_score and (p2_score >= 5 or p1_score >=5):
    print("Player 1 wins!")
elif p2_score > p1_score and (p2_score >= 5 or p1_score >=5):
    print("Player 2 wins!")

print("p1_score: ", p1_score)
print("p2_score: ", p2_score)
pygame.quit()
