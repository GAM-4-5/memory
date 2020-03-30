import pygame
import pygame.draw
from math import floor, modf, pi
from random import randint
import time

pygame.init()

colors = [(0,   0, 255),
          (255,   0, 0),
          (0, 255,   0),
          (100,   160,   40),
          (160,   70,   20),
          (160,   160,   40),
          (50,   100,   50),
          (60,   80,   40),
          (80,   100,   150),
          (70,   250,   220),
          (50,   100,   95),
          (30,   120,   200),
          (220,   150,   25),
          (255,   0,   0),
          (255,   0,   0),
          (255,   0,   0),
          (255,   0,   0), ]

CARD_WIDTH = 100
CARD_HEIGHT = 160

PADDING_TOP = 50
PADDING_LEFT = 50


class Card:
    x = 0
    y = 0
    alpha = 255
    color = 0
    faceUp = True
    done = False

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.alpha = 255
        self.color = color

    def Draw(self):
        r, g, b = colors[self.color]
        if not self.done:
            pygame.draw.rect(screen, (r, g, b, self.alpha) if self.faceUp else (
                42, 42, 42, self.alpha), [self.x, self.y, CARD_WIDTH, CARD_HEIGHT], 0)

    def TestCollisionSelfPoint(self, x, y):
        return x > self.x and y > self.y and x < self.x + CARD_WIDTH and y < self.y + CARD_HEIGHT

COLOR_INACTIVE = (151,175,171)
COLOR_ACTIVE = (27,246,246)


Cards = []

CARDS_ROW = 4
CARD_COLUMNS = 4
COLORS_TOTAL = floor(CARDS_ROW * CARD_COLUMNS / 2)

colorsOut = {}


def pullUniqueColor():
    i = randint(0, COLORS_TOTAL - 1)
    v = colorsOut.get(i)
    while v == 2:
        i = randint(0, COLORS_TOTAL - 1)
        v = colorsOut.get(i)
    if v == 1:
        colorsOut[i] = 2
    else:
        colorsOut[i] = 1
    return i


def findPressedCard(x, y):
    for card in Cards:
        if card.TestCollisionSelfPoint(x, y):
            return card
    return None


i = 0
for y in range(0, CARDS_ROW):
    for x in range(0, CARD_COLUMNS):
        Cards.append(Card(x * 3 / 2 * CARD_WIDTH + PADDING_LEFT, y *
                          3 / 2 * CARD_HEIGHT + PADDING_TOP, pullUniqueColor()))
        i += 0.5

SCREEN_WIDTH = floor(CARD_COLUMNS * 3 / 2 * CARD_WIDTH + PADDING_LEFT)
SCREEN_HEIGHT = floor(CARDS_ROW * 3 / 2 * CARD_HEIGHT + PADDING_TOP)

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

pygame.display.set_caption("MemoryGame")
font = pygame.font.SysFont('Comic Sans MS', 30)

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((255, 255, 255))

    for card in Cards:
        card.Draw()

    pygame.display.flip()

pygame.quit()
