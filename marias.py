# -*- coding: utf-8 -*-

import os
import pygame
import random

from functools import cmp_to_key

dir_path = os.path.dirname(os.path.realpath(__file__))

WIDTH, HEIGHT = 1200, 750

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Lizany Marias")

pygame.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


FPS = 10

LEVEL_FONT = pygame.font.SysFont("comicsans", 20)

# nacteni karet

CER_SEDMA = pygame.image.load(dir_path + "/assets/cer_sedma.png")
CER_OSMA = pygame.image.load(dir_path + "/assets/cer_osma.png")
CER_DEVITKA = pygame.image.load(dir_path + "/assets/cer_devitka.png")
CER_DESITKA = pygame.image.load(dir_path + "/assets/cer_desitka.png")
CER_SPODEK = pygame.image.load(dir_path + "/assets/cer_spodek.png")
CER_SVRSEK = pygame.image.load(dir_path + "/assets/cer_svrsek.png")
CER_KRAL = pygame.image.load(dir_path + "/assets/cer_kral.png")
CER_ESO = pygame.image.load(dir_path + "/assets/cer_eso.png")

ZAL_SEDMA = pygame.image.load(dir_path + "/assets/zal_sedma.png")
ZAL_OSMA = pygame.image.load(dir_path + "/assets/zal_osma.png")
ZAL_DEVITKA = pygame.image.load(dir_path + "/assets/zal_devitka.png")
ZAL_DESITKA = pygame.image.load(dir_path + "/assets/zal_desitka.png")
ZAL_SPODEK = pygame.image.load(dir_path + "/assets/zal_spodek.png")
ZAL_SVRSEK = pygame.image.load(dir_path + "/assets/zal_svrsek.png")
ZAL_KRAL = pygame.image.load(dir_path + "/assets/zal_kral.png")
ZAL_ESO = pygame.image.load(dir_path + "/assets/zal_eso.png")

LIS_SEDMA = pygame.image.load(dir_path + "/assets/lis_sedma.png")
LIS_OSMA = pygame.image.load(dir_path + "/assets/lis_osma.png")
LIS_DEVITKA = pygame.image.load(dir_path + "/assets/lis_devitka.png")
LIS_DESITKA = pygame.image.load(dir_path + "/assets/lis_desitka.png")
LIS_SPODEK = pygame.image.load(dir_path + "/assets/lis_spodek.png")
LIS_SVRSEK = pygame.image.load(dir_path + "/assets/lis_svrsek.png")
LIS_KRAL = pygame.image.load(dir_path + "/assets/lis_kral.png")
LIS_ESO = pygame.image.load(dir_path + "/assets/lis_eso.png")

KUL_SEDMA = pygame.image.load(dir_path + "/assets/kul_sedma.png")
KUL_OSMA = pygame.image.load(dir_path + "/assets/kul_osma.png")
KUL_DEVITKA = pygame.image.load(dir_path + "/assets/kul_devitka.png")
KUL_DESITKA = pygame.image.load(dir_path + "/assets/kul_desitka.png")
KUL_SPODEK = pygame.image.load(dir_path + "/assets/kul_spodek.png")
KUL_SVRSEK = pygame.image.load(dir_path + "/assets/kul_svrsek.png")
KUL_KRAL = pygame.image.load(dir_path + "/assets/kul_kral.png")
KUL_ESO = pygame.image.load(dir_path + "/assets/kul_eso.png")

TURN = pygame.image.load(dir_path + "/assets/turn.png")


CARD_WIDTH = 60
CARD_HEIGHT = 80


COLORS = ['cer', 'lis', 'zal', 'kul']
VALUES = ['sedma', 'osma', 'devitka', 'desitka',
          'spodek', 'svrsek', 'kral', 'eso']
COLOR_PREF = {'kul': 1, 'zal': 2, 'lis': 3, 'cer': 4}
VALUE_PREF = {'sedma': 7, 'osma': 8, 'devitka': 9,
              'spodek': 10, 'svrsek': 11, 'kral': 12,
              'desitka': 13, 'eso': 14}


# trida karty
class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value
        self.picture = None
        self.points = 0

        if value == 'desitka' or value == 'eso':
            self.points = 10

        # adds picture to a card
        if color == 'cer' and value == 'sedma':
            self.picture = CER_SEDMA
        if color == 'cer' and value == 'osma':
            self.picture = CER_OSMA
        if color == 'cer' and value == 'devitka':
            self.picture = CER_DEVITKA
        if color == 'cer' and value == 'desitka':
            self.picture = CER_DESITKA
        if color == 'cer' and value == 'spodek':
            self.picture = CER_SPODEK
        if color == 'cer' and value == 'svrsek':
            self.picture = CER_SVRSEK
        if color == 'cer' and value == 'kral':
            self.picture = CER_KRAL
        if color == 'cer' and value == 'eso':
            self.picture = CER_ESO

        if color == 'zal' and value == 'sedma':
            self.picture = ZAL_SEDMA
        if color == 'zal' and value == 'osma':
            self.picture = ZAL_OSMA
        if color == 'zal' and value == 'devitka':
            self.picture = ZAL_DEVITKA
        if color == 'zal' and value == 'desitka':
            self.picture = ZAL_DESITKA
        if color == 'zal' and value == 'spodek':
            self.picture = ZAL_SPODEK
        if color == 'zal' and value == 'svrsek':
            self.picture = ZAL_SVRSEK
        if color == 'zal' and value == 'kral':
            self.picture = ZAL_KRAL
        if color == 'zal' and value == 'eso':
            self.picture = ZAL_ESO

        if color == 'lis' and value == 'sedma':
            self.picture = LIS_SEDMA
        if color == 'lis' and value == 'osma':
            self.picture = LIS_OSMA
        if color == 'lis' and value == 'devitka':
            self.picture = LIS_DEVITKA
        if color == 'lis' and value == 'desitka':
            self.picture = LIS_DESITKA
        if color == 'lis' and value == 'spodek':
            self.picture = LIS_SPODEK
        if color == 'lis' and value == 'svrsek':
            self.picture = LIS_SVRSEK
        if color == 'lis' and value == 'kral':
            self.picture = LIS_KRAL
        if color == 'lis' and value == 'eso':
            self.picture = LIS_ESO

        if color == 'kul' and value == 'sedma':
            self.picture = KUL_SEDMA
        if color == 'kul' and value == 'osma':
            self.picture = KUL_OSMA
        if color == 'kul' and value == 'devitka':
            self.picture = KUL_DEVITKA
        if color == 'kul' and value == 'desitka':
            self.picture = KUL_DESITKA
        if color == 'kul' and value == 'spodek':
            self.picture = KUL_SPODEK
        if color == 'kul' and value == 'svrsek':
            self.picture = KUL_SVRSEK
        if color == 'kul' and value == 'kral':
            self.picture = KUL_KRAL
        if color == 'kul' and value == 'eso':
            self.picture = KUL_ESO

    def __repr__(self):
        return "Card:" + self.color + ' ' + self.value

    def __str__(self):
        return self.color + ' ' + self.value


class Stych:
    def __init__(self, phase, card0, card1, hlaska0, hlaska1, wt):
        self.card0 = card0
        self.card1 = card1
        self.cards = [card0, card1]
        self.hlaska0 = hlaska0  # true/assets/false, pokud karta byla hlaska
        self.hlaska1 = hlaska1
        self.hlasky = [hlaska0, hlaska1]  # pro pristupn skrze pole
        self.wt = wt  # who took
        self.phase = phase


class History:
    def __init__(self):
        self.stychy = []

    def add(self, phase, card0, card1, hlaska0, hlaska1, wt):
        self.stychy.append(Stych(phase, card0, card1, hlaska0, hlaska1, wt))

    def getlast(self):
        return self.stychy[-1]

# trida spravujici talon


class Talon:
    def __init__(self, cards):
        self.cards = cards

    def shuffle(self):
        random.shuffle(self.cards)

    def isempty(self):
        if len(self.cards) == 0:
            return True
        return False

    def popcard(self):
        if not self.isempty():
            return self.cards.pop()
        return None

# trida spravujici karty v ruce


class Hand:
    def __init__(self):
        self.cards = []

    def __cmpcards__(self, card1, card2):

        c1_color_pref = COLOR_PREF[card1.color]
        c2_color_pref = COLOR_PREF[card2.color]
        c1_value_pref = VALUE_PREF[card1.value]
        c2_value_pref = VALUE_PREF[card2.value]

        if c1_color_pref < c2_color_pref:
            return 1
        elif c1_color_pref == c2_color_pref:
            if c1_value_pref < c2_value_pref:
                return 1
            elif c1_value_pref == c2_value_pref:
                return 0
            else:
                return -1
        else:
            return -1

    def sort(self):
        self.cards = sorted(self.cards, key=cmp_to_key(self.__cmpcards__))

    def addcard(self, card):
        self.cards.append(card)
        # neefektivni - tridi se pri kazdem liznuti karty
        self.sort()

    def isempty(self):
        if len(self.cards) == 0:
            return True
        return False

    def iscardpresent(self, col, val):
        for c in self.cards:
            if c.color == col and c.value == val:
                return True
        return False

    # vraci vsechny karty dane barvy
    def getcardscol(self, col):
        l = []
        for c in self.cards:
            if c.color == col:
                l.append(c)
        return l

    # vraci vsechny karty dane barvy vyssi nez value
    def getcardshigher(self, col, val):
        l = []
        for c in self.cards:
            if c.color == col and VALUE_PREF[c.value] > VALUE_PREF[val]:
                l.append(c)
        return l

    # vraci vsechny karty dane hodnoty

    def getcardsval(self, val):
        l = []
        for c in self.cards:
            if c.value == val:
                l.append(c)
        return l

    def removecard(self, col, val):
        index = -1
        if self.iscardpresent(col, val):
            for i in range(len(self.cards)):
                if (self.cards[i].color == col) and (self.cards[i].value == val):
                    index = i
                    break
        if index >= 0:
            del self.cards[i]

    def disp(self):
        for c in self.cards:
            c.disp()

    # returns valid card moves to opcard

    def validcardmoves(self, opcard, phase, trumfcolor):
        # opcard.disp()
        # print("---")
        # print(phase)
        # print(trumfcolor)
        # print("---")

        if self.isempty():
            return []

        cardmoves = self.cards.copy()

        if opcard != None:

            cardmoves = self.getcardshigher(opcard.color, opcard.value)

            if len(cardmoves) == 0:
                # hrac nema zadne vyssi karty dane barvy
                # alespon chceme karty stejne barvy
                cardmoves = self.getcardscol(opcard.color)

                if len(cardmoves) == 0:
                    # hrac nema karty v barve protihracovy karty
                    if phase == 1:
                        # v prvni fazi muzeme hrat cokoli, pokud nemame barvu
                        # ve druhe fazi, kdyz nemame, musime trumfovat
                        cardmoves = self.getcardscol(trumfcolor)
                        if len(cardmoves) == 0:
                            cardmoves = self.cards.copy()
                    else:
                        cardmoves = self.cards.copy()

        # vyhozeni kralu z moznych tahu, kdyz mame i svrska
        # musime hrat svrska prvniho
        svrsci = self.getcardsval('svrsek')
        for s in svrsci:
            index = -1
            for i in range(len(cardmoves)):
                if cardmoves[i].color == s.color and cardmoves[i].value == 'kral':
                    index = i
                    break

            if index >= 0:
                del cardmoves[i]

        return cardmoves

    # vybere nahodnou kartu
    def chooserandom(self, cardlist):
        # print(cardlist)
        return random.choice(cardlist)


# trida hrace
class Player:
    def __init__(self, num, name):
        self.num = num
        self.name = name
        self.hand = Hand()

    def isdone(self):
        if self.hand.isempty():
            return True
        return False

    def addcard(self, card):
        self.hand.addcard(card)

    def play(self, history, phase, trumfcolor, first=True, opcard=None):
        if not self.isdone():
            hlaska = False

            if first:
                cm = self.hand.validcardmoves(None, phase, trumfcolor)

                # tisk validnich tahu
                print("====================================")
                print("Hrac:", self.name, "===============")
                print("------ Ma v ruce:")
                for c in self.hand.cards:
                    print(c)
                print("------ Muze hrat")
                for c in cm:
                    print(c)

                c = self.hand.chooserandom(self.hand.cards)

                if c.value == 'svrsek':
                    if self.hand.iscardpresent(c.color, 'kral'):
                        hlaska = True

                self.hand.removecard(c.color, c.value)

                return c, hlaska
            else:
                # hraje jako druhy
                cm = self.hand.validcardmoves(opcard, phase, trumfcolor)

                # tisk validnich tahu
                print("====================================")
                print("Hrac:", self.name, "===============")
                print("------ Ma v ruce:")
                for c in self.hand.cards:
                    print(c)
                print("------ Muze hrat")
                for c in cm:
                    print(c)

                c = self.hand.chooserandom(cm)

                if c.value == 'svrsek':
                    if self.hand.iscardpresent(c.color, 'kral'):
                        hlaska = True

                self.hand.removecard(c.color, c.value)

                return c, hlaska

        return None, False

  # trida spravujici hru


class Marias:
    def __init__(self):
        # init karet
        cards = [Card(b, h) for b in COLORS for h in VALUES]
        self.talon = Talon(cards)
        self.talon.shuffle()
        # print(self.talon.cards)
        self.player0 = Player(0, 'Tunta')
        self.player1 = Player(1, 'Punta')

        # rozdej
        for i in range(5):
            self.player0.addcard(self.talon.popcard())

        for i in range(5):
            self.player1.addcard(self.talon.popcard())

        self.trumfcolor = self.talon.cards[0].color
        self.lastcard = self.talon.cards[0]

        # posledni tah
        self.lastcard0 = None
        self.lastcard1 = None
        self.lasthlaska0 = False
        self.lasthlaska1 = False

        self.phase = 0  # 0... pripravna faze, 1...dolizany balik
        self.playerturn = 0

        self.player0points = 0  # body hracu
        self.player1points = 0

        self.round = 0
        self.history = History()

    def isdone(self):
        if self.player0.isdone() and self.player1.isdone():
            return True
        return False

    def firsttakes(self, card0, card1):

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

        # tahy hracu
        if self.playerturn == 0:
            self.lastcard0, self.lasthlaska0 = self.player0.play(
                self.history, self.phase, self.trumfcolor, True, None)
            self.lastcard1, self.lasthlaska1 = self.player1.play(
                self.history, self.phase, self.trumfcolor, False, self.lastcard0)

        else:
            self.lastcard1, self.lasthlaska1 = self.player1.play(
                self.history, self.phase, self.trumfcolor, True, None)
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

        # print("********************")
        #print(c0, " vs. ", c1, "wins: ", wt)
        # print("********************")

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


def draw_window(marias):
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
