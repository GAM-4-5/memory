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

TIME_TILL_TURN = 5

done = False
clock = pygame.time.Clock()

gameStarted = False
startTime = 0

CARD_PUT_DOWN_TIME = 3

card1up = None
card2up = None
cardsSolved = 0
cardPutDownTime = CARD_PUT_DOWN_TIME
lastCard = None
puttingDown = False
errors = 0
endTime = 0

def SaveHighScore(name):
    print(name)

while not done:
    if TIME_TILL_TURN > 0:
        clock.tick(1)
        TIME_TILL_TURN -= 1
    elif not gameStarted:
        clock.tick(30)
        gameStarted = True
        for card in Cards:
            card.faceUp = False
        startTime = time.time()
    else:
        clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((255, 255, 255))

    x, y = pygame.mouse.get_pos()
    pressed, _, _ = pygame.mouse.get_pressed()
    if gameStarted:
        if cardsSolved == COLORS_TOTAL:
            if endTime == 0:
                endTime = time.time()
            d = floor(endTime - startTime)
            timeFromStart = font.render(str(d), False, (0, 0, 0))
            screen.blit(timeFromStart, (SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2))
            errorsSprite = font.render(str(errors), False, (230, 0, 0))
            screen.blit(errorsSprite, (SCREEN_WIDTH / 2 + 50, SCREEN_HEIGHT / 2))
        else:
            d = floor((time.time()) - startTime)
            timeFromStart = font.render(str(d), False, (0, 0, 0))
            screen.blit(timeFromStart, (SCREEN_WIDTH / 2 - 50, 0))
            errorsSprite = font.render(str(errors), False, (230, 0, 0))
            screen.blit(errorsSprite, (SCREEN_WIDTH / 2 + 50, 0))

            if time.time() > cardPutDownTime and puttingDown:
                if card1up != None:
                    card1up.faceUp = False
                if card2up != None:
                    card2up.faceUp = False
                card1up = None
                card2up = None
                puttingDown = False

            if pressed:
                card = findPressedCard(x, y)
                if card != None and card != lastCard:
                    card.faceUp = True

                    if card1up == None:
                        card1up = card
                    elif card2up == None:
                        card2up = card
                        if card1up.color == card2up.color:
                            card1up.done = True
                            card2up.done = True
                            cardsSolved += 1
                            card1up = None
                            card2up = None
                        else:
                            cardPutDownTime = CARD_PUT_DOWN_TIME + time.time()
                            puttingDown = True
                            errors += 1
                    else:
                        puttingDown = False

                        card1up.faceUp = False
                        card2up.faceUp = False

                        card1up = card
                        card2up = None
                lastCard = card
    else:
        timeTillStart = font.render(str(TIME_TILL_TURN), False, (0, 0, 0))
        screen.blit(timeTillStart, (0, 0))
    
    for card in Cards:
        card.Draw()

    pygame.display.flip()

pygame.quit()
