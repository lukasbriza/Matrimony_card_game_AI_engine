from engine.Card import Card
from engine.Hand import Hand
from engine.History import History
from strategies import first_phase_strategy as fs
from tooling.Tools import get_card_db, get_cards_as_class, get_cards_of_oponent, get_simplified_card_list, is_hlaska, print_valid_card_moves


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

    def play(self, history: History, phase: int, trumf_color: str, first=True, opcard=None):
        if not self.isdone():
            hlaska = False

            if first:
                cm = self.hand.validcardmoves(None, phase, trumf_color)
                print_valid_card_moves(self.name, self.hand.cards, cm)

                # Phase 1 strategy
                if phase == 1:
                    oponent_cards = get_cards_of_oponent(
                        history,
                        get_card_db(),
                        self.hand.cards
                    )
                    card = fs.first_phase_strategy(
                        get_cards_as_class(oponent_cards),
                        self.hand.cards,
                        True,
                        trumf_color
                    )
                    hlaska = is_hlaska(card, self.hand)
                    self.hand.removecard(card.color, card.value)
                    return card, hlaska

                c = self.hand.chooserandom(self.hand.cards)
                hlaska = is_hlaska(c, self.hand)
                self.hand.removecard(c.color, c.value)

                return c, hlaska
            else:
                cm = self.hand.validcardmoves(opcard, phase, trumf_color)
                print_valid_card_moves(self.name, self.hand.cards, cm)

                # Phase 1 strategy
                if phase == 1:
                    oponent_cards = get_cards_of_oponent(
                        history,
                        get_card_db(),
                        self.hand.cards
                    )
                    card = fs.first_phase_strategy(
                        get_cards_as_class(oponent_cards),
                        self.hand.cards,
                        False,
                        trumf_color
                    )
                    hlaska = is_hlaska(card, self.hand)
                    self.hand.removecard(card.color, card.value)
                    return card, hlaska

                c = self.hand.chooserandom(cm)
                hlaska = is_hlaska(c, self.hand)
                self.hand.removecard(c.color, c.value)

                return c, hlaska

        return None, False
