# -*- coding: utf-8 -*-
import os
import pygame

from engine.Card import Card
from engine.Constants import COLORS, VALUE_PREF, VALUES
from engine.History import History
from engine.Player import Player
from engine.Talon import Talon
from config import *


dir_path = os.path.dirname(os.path.realpath(__file__))


WIDTH, HEIGHT = 1200, 750

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Matrimony_card_game")

pygame.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


FPS = 10

LEVEL_FONT = pygame.font.SysFont("comicsans", 20)

TURN = pygame.image.load(dir_path + "/engine/assets/turn.png")


CARD_WIDTH = 60
CARD_HEIGHT = 80


class Marias:
    def __init__(self):
        # init cards
        cards: list[Card] = [Card(b, h) for b in COLORS for h in VALUES]
        self.talon: Talon = Talon(cards)
        self.talon.shuffle()
        self.player0: Player = Player(0, 'Tunta')
        self.player1: Player = Player(1, 'Punta')

        # distribute cards
        for i in range(5):
            self.player0.addcard(self.talon.popcard())

        for i in range(5):
            self.player1.addcard(self.talon.popcard())

        self.trumfcolor: str = self.talon.cards[0].color
        self.lastcard: Card = self.talon.cards[0]

        # posledni tah
        self.lastcard0: Card = None
        self.lastcard1: Card = None
        self.lasthlaska0: bool = False
        self.lasthlaska1: bool = False

        self.phase: int = 0  # 0... pripravna faze, 1...dolizany balik
        self.playerturn: int = 0

        self.player0points: int = 0  # body hracu
        self.player1points: int = 0

        self.round: int = 0
        self.history: History = History()

    def isdone(self):
        if self.player0.isdone() and self.player1.isdone():
            return True
        return False

    def firsttakes(self, card0: Card, card1: Card):

        if (card0 == None) or (card1 == None):
            return None

        if self.phase == 0:
            if (card1.color == card0.color) and (VALUE_PREF[card1.value] > VALUE_PREF[card0.value]):
                return False
            else:
                return True

        if self.phase == 1:
            if (card1.color == card0.color) and (VALUE_PREF[card1.value] > VALUE_PREF[card0.value]):
                return False
            elif (card1.color != card0.color) and (card1.color == self.trumfcolor):
                return False
            else:
                return True

    def play(self):

        if self.talon.isempty():
            self.phase = 1

        # player moves
        if self.playerturn == 0:
            # first play player 0
            self.lastcard0, self.lasthlaska0 = self.player0.play(
                self.history, self.phase, self.trumfcolor, True, None)
            # second ply player 1
            self.lastcard1, self.lasthlaska1 = self.player1.play(
                self.history, self.phase, self.trumfcolor, False, self.lastcard0)

        else:
            # second ply player 1
            self.lastcard1, self.lasthlaska1 = self.player1.play(
                self.history, self.phase, self.trumfcolor, True, None)
            # first play player 0
            self.lastcard0, self.lasthlaska0 = self.player0.play(
                self.history, self.phase, self.trumfcolor, False, self.lastcard1)

        self.round += 1

        c0 = self.lastcard0
        c1 = self.lastcard1

        # kdo bere stych
        wt = None
        if self.playerturn == 0:
            ft = self.firsttakes(c0, c1)
            if ft:
                wt = 0
            else:
                wt = 1
        else:
            ft = self.firsttakes(c1, c0)
            if ft:
                wt = 1
            else:
                wt = 0

        self.history.add(self.phase, self.lastcard0, self.lastcard1,
                         self.lasthlaska0, self.lasthlaska1, wt)

        if LOGS:
            print("********************")
            print(c0, " vs. ", c1, "wins: ", wt)
            print("********************")

        if wt == 0:
            self.player0points += c0.points + c1.points
            self.playerturn = 0

            if not self.talon.isempty():
                # prvni dolizava hrac, ktery sebral stych
                self.player0.addcard(self.talon.popcard())
                self.player1.addcard(self.talon.popcard())

            # posledni stych
            if self.isdone():
                self.player0points += 10

        else:
            self.player1points += c0.points + c1.points
            self.playerturn = 1

            if not self.talon.isempty():
                self.player1.addcard(self.talon.popcard())
                self.player0.addcard(self.talon.popcard())

            # posledni stych
            if self.isdone():
                self.player1points += 10

        if self.lasthlaska0:
            if self.lastcard0.color == self.trumfcolor:
                self.player0points += 40
            else:
                self.player0points += 20

        if self.lasthlaska1:
            if self.lastcard1.color == self.trumfcolor:
                self.player1points += 40
            else:
                self.player1points += 20

        self.lastcard0 = None
        self.lastcard1 = None
        self.lasthlaska0 = False
        self.lasthlaska1 = False


def draw_window(marias: Marias):
    #WIN.blit(SEA, (0, 0))
    WIN.fill(WHITE)

    h1 = LEVEL_FONT.render("Hrac 0: " + marias.player0.name +
                           " ::: Skore: " + str(marias.player0points), 1, BLACK)
    h2 = LEVEL_FONT.render("Hrac 1: " + marias.player1.name +
                           " ::: Skore: " + str(marias.player1points), 1, BLACK)
    h3 = LEVEL_FONT.render("Trumfy: ", 1, BLACK)

    WIN.blit(h1, (30, 30))
    WIN.blit(h2, (30, 660))
    WIN.blit(h3, (1000, 10))

    #WIN.blit(FLAG, (WIDTH - ME_SIZE, HEIGHT - ME_SIZE - 10))

    # for mine in mines:
    #    WIN.blit(ENEMY, (mine.rect.x, mine.rect.y))

    # cards of player 1 (top)
    x = 50
    y = 70
    for c in marias.player0.hand.cards:
        WIN.blit(c.picture, (x, y))
        x += 70

    # cards of player 2 (down)
    x = 50
    y = 550
    for c in marias.player1.hand.cards:
        WIN.blit(c.picture, (x, y))
        x += 70

    # draw history
    x = 50
    y = 250
    for stych in marias.history.stychy:
        c0 = stych.card0
        c1 = stych.card1

        if c0 != None:
            d = 0
            if stych.hlaska0:
                d = 20
            WIN.blit(c0.picture, (x, y-d))

        if c1 != None:
            d = 0
            if stych.hlaska1:
                d = 20
            WIN.blit(c1.picture, (x, y+120+d))

        wt = stych.wt

        if wt == 0:
            WIN.blit(TURN, (x+20, y-50))
        if wt == 1:
            WIN.blit(TURN, (x+20, y+250))

        x += 70

    WIN.blit(marias.lastcard.picture, (1000, 50))
    pygame.draw.line(WIN, BLACK, (814, 200), (814, 520), 3)

    pygame.display.update()


# hlavni smycka hry
def main():

    marias = Marias()

    clock = pygame.time.Clock()

    run = True
    firstdraw = True
    play = False

    while run:

        clock.tick(FPS)

        keys_pressed = pygame.key.get_pressed()

        # herni kolo - stridaji se tahy hracu
        if keys_pressed[pygame.K_SPACE] and not marias.isdone():
            # if not marias.isdone():
            marias.play()

        draw_window(marias)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


if __name__ == "__main__":
    main()
