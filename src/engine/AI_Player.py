from Card import Card
from Hand import Hand
from engine.History import History
from tooling.Tools import print_valid_card_moves


class AI_Player:
    def __init__(self, num, name):
        self.num = num
        self.name = name
        self.hand = Hand()

    def isdone(self):
        if self.hand.isempty():
            return True
        return False

    def addcard(self, card: Card):
        self.hand.addcard(card)

    def play(self, history: History, phase: int, trumfcolor: str, first=True, opcard=None):
        if not self.isdone():
            hlaska = False

            if first:
                # play first
                cm = self.hand.validcardmoves(None, phase, trumfcolor)

                # print valid card turns
                print_valid_card_moves(self.name, self.hand.cards, cm)

                # here strategy
                c = self.hand.chooserandom(self.hand.cards)

                if c.value == 'svrsek':
                    if self.hand.iscardpresent(c.color, 'kral'):
                        hlaska = True

                self.hand.removecard(c.color, c.value)

                return c, hlaska
            else:
                # play second
                cm = self.hand.validcardmoves(opcard, phase, trumfcolor)

                # print valid card turns
                print_valid_card_moves(self.name, self.hand.cards, cm)

                # here strategy
                c = self.hand.chooserandom(cm)

                if c.value == 'svrsek':
                    if self.hand.iscardpresent(c.color, 'kral'):
                        hlaska = True

                self.hand.removecard(c.color, c.value)

                return c, hlaska

        return None, False