
from typing import Union
from config import LOGS
from engine.AI_Player import AI_Player
from engine.Card import Card
from engine.Constants import COLORS, VALUES
from engine.History import History
from engine.Player import Player
from engine.Talon import Talon
from tooling.Tools import evaluate_wt, first_takes_resolve

playerUnion = Union[Player, AI_Player]


class Marias:
    def __init__(
        self,
        player0: playerUnion = Player(0, 'Tunta'),
        player1: playerUnion = AI_Player(1, 'Ja')
    ):
        # init cards
        cards: list[Card] = [Card(b, h) for b in COLORS for h in VALUES]
        self.talon: Talon = Talon(cards)
        self.talon.shuffle()
        self.player0: playerUnion = player0
        self.player1: playerUnion = player1

        # distribute cards
        for i in range(5):
            self.player0.addcard(self.talon.popcard())

        for i in range(5):
            self.player1.addcard(self.talon.popcard())

        self.trumfcolor: str = self.talon.cards[0].color
        self.lastcard: Card = self.talon.cards[0]

        # last move
        self.lastcard0: Card = None
        self.lastcard1: Card = None
        self.lasthlaska0: bool = False
        self.lasthlaska1: bool = False

        # 0... prepare phase, 1...talon is out of cards
        self.phase: int = 0
        self.playerturn: int = 0

        # player points
        self.player0points: int = 0
        self.player1points: int = 0

        self.round: int = 0
        self.history: History = History()

    def isdone(self):
        if self.player0.isdone() and self.player1.isdone():
            return True
        return False

    def firsttakes(self, card0: Card, card1: Card):
        return first_takes_resolve(self.trumfcolor, self.phase, card0, card1)

    def play(self):

        if self.talon.isempty():
            self.phase = 1
        print(self.phase)
        # player moves
        if self.playerturn == 0:
            # first play player 0
            self.lastcard0, self.lasthlaska0 = self.player0.play(
                self.history, self.phase, self.trumfcolor, True, None)
            # second play player 1
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

        # who take stych
        wt = None
        wt = evaluate_wt(self.playerturn, self.trumfcolor, self.phase, c0, c1)

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
                # fist take card who had stych
                self.player0.addcard(self.talon.popcard())
                self.player1.addcard(self.talon.popcard())

            # last stych
            if self.isdone():
                self.player0points += 10

        else:
            self.player1points += c0.points + c1.points
            self.playerturn = 1

            if not self.talon.isempty():
                self.player1.addcard(self.talon.popcard())
                self.player0.addcard(self.talon.popcard())

            # last stych
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
