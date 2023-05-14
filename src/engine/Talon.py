import random
from engine import Card as c


# Class managing talon


class Talon:
    def __init__(self, cards: list[c.Card]):
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
