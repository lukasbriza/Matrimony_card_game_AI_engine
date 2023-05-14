import random
from functools import cmp_to_key
from config import LOGS
from engine.Card import Card
from engine.Constants import COLOR_PREF, VALUE_PREF


# Class managing hand


class Hand:
    def __init__(self):
        self.cards: list[Card] = []

    def __cmpcards__(self, card1: Card, card2: Card):

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

    def addcard(self, card: Card):
        self.cards.append(card)
        # uneffective - sort on every card take
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

    # return all cards of specified "col" property
    def getcardscol(self, col):
        l = []
        for c in self.cards:
            if c.color == col:
                l.append(c)
        return l

    # return all cards of cololor specified in "col" an higher then property "val"
    def getcardshigher(self, col, val):
        l = []
        for c in self.cards:
            if c.color == col and VALUE_PREF[c.value] > VALUE_PREF[val]:
                l.append(c)
        return l

    # return cards of val property
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

    def validcardmoves(self, opcard: Card, phase: int, trumfcolor: str):
        # opcard.disp()
        if LOGS:
            print("---")
            print(phase)
            print(trumfcolor)
            print("---")

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

    # choose random card
    def chooserandom(self, cardlist: list[Card]):
        #print(cardlist)
        return random.choice(cardlist)
