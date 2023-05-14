from engine.Card import Card


class Stych:
    def __init__(self, phase: int, card0: Card, card1: Card, hlaska0, hlaska1, wt):
        self.card0 = card0
        self.card1 = card1
        self.cards = [card0, card1]
        self.hlaska0 = hlaska0  # true/false, if hlaska appeared
        self.hlaska1 = hlaska1
        self.hlasky = [hlaska0, hlaska1]  # for access through list
        self.wt = wt  # who took
        self.phase = phase
