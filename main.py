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
        self.score = 0

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


class FatMan(pygame.sprite.Sprite):
    def __init__(self, colour):
        super(FatMan, self).__init__()
        self.colour = colour
        self.surf = pygame.image.load("ferpectament_100.png").convert()
        self.rect = self.surf.get_rect(
            # Make the position random
            center=(
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = 3

    def update(self, player1, player2):
        # calculate the distance to each player
        d1 = distance(player1.rect.centerx,
                      player1.rect.centery,
                      self.rect.centerx,
                      self.rect.centery)

        d2 = distance(player2.rect.centerx,
                      player2.rect.centery,
                      self.rect.centerx,
                      self.rect.centery)

        if d1 < d2:
            chase(self, player1, self.speed)
        else:
            chase(self, player2, self.speed)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Prize(pygame.sprite.Sprite):
    def __init__(self, colour):
        super(Prize, self).__init__()
        self.surf = pygame.image.load("red_ball3.png").convert()
        self.rect = self.surf.get_rect(
            # Make the position random
            center = (
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

        # self.surf.set_colorkey(GREEN, RLEACCEL)
        # self.mask = pygame.mask.from_surface(self.surf)


class Exit(pygame.sprite.Sprite):
    def __init__(self, colour):
        super(Exit, self).__init__()
        self.colour = colour
        self.surf = pygame.Surface((30, 30))
        self.surf.fill(self.colour)
        self.rect = self.surf.get_rect(
            # Make the position random
            center = (
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

def draw_game(player1, player2, fat_man, prize):
    # Draw a black background
    screen.fill(BLACK)

    # Draws the game players and elements
    # Player 1
    screen.blit(player1.surf, player1.rect)

    # Player 2
    screen.blit(player2.surf, player2.rect)

    # FatMan
    screen.blit(fat_man.surf, fat_man.rect)

    # Prize
    screen.blit(prize.surf, prize.rect)

    # Exit
    screen.blit(exit.surf, exit.rect)

    # Update the display
    pygame.display.flip()


def distance(x, y, a, b):
    x1 = abs(x - a)
    y1 = abs(y - b)
    h = math.sqrt(x1 ** 2 + y1 ** 2)

    return h


def chase(chaser, chased, speed):
    if chaser.rect.centerx > chased.rect.centerx:
        chaser.rect.move_ip(-speed, 0)
    if chaser.rect.centerx < chased.rect.centerx:
        chaser.rect.move_ip(speed, 0)
    if chaser.rect.centery > chased.rect.centery:
        chaser.rect.move_ip(0, -speed)
    if chaser.rect.centery < chased.rect.centery:
        chaser.rect.move_ip(0, speed)

    return chaser


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

players = pygame.sprite.Group()
players.add(player1)
players.add(player2)

# Instantiate foe
fat_man = FatMan(GREEN)

# Instantiate a prize
prize = Prize(RED)

# Instantiate an exit
exit = Exit(WHITE)

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
    fat_man.update(player1, player2)

    # Draw the new frame
    draw_game(player1, player2, fat_man, prize)

    # Check if a player collides with the prize
    if pygame.sprite.collide_rect(player1, prize):
        # If so, then remove the prize and create a new one elsewhere
        prize.kill()
        prize = Prize(RED)
        screen.blit(prize.surf, prize.rect)
        player1.score += 1

    if pygame.sprite.collide_rect(player2, prize):
        # If so, then remove the prize and create a new one elsewhere
        prize.kill()
        prize = Prize(RED)
        screen.blit(prize.surf, prize.rect)
        player2.score += 1


    screen.fill(BLACK)

    if (pygame.sprite.collide_rect(player1, exit) or\
       pygame.sprite.collide_rect(player2, exit)) and\
       (player1.score >= 5 or player2.score >= 5):
        running = False

    if pygame.sprite.collide_rect(player1, fat_man):
        # If so, then remove the prize and create a new one elsewhere
        player1.score -= 2
        player1.kill()
        running = False
        # print("players.alive? ", player2.alive())
        # if not player2.alive():
        #     running = False

    if pygame.sprite.collide_rect(player2, fat_man):
        # If so, then remove the prize and create a new one elsewhere
        player2.score -= 2
        player2.kill()
        running = False
        # if not player1.alive():
        #     running = False


if player1.score >= 5:
    print("Player 1 wins!")
elif player2.score >= 5:
    print("Player 2 wins!")

print("p1_score: ", player1.score)
print("p2_score: ", player2.score)
pygame.quit()
