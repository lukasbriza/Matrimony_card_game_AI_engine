from config import LOGS
from engine.Card import Card
from engine.Constants import COLORS, VALUE_PREF, VALUES
from engine.Hand import Hand
from engine.History import History


def evaluate_wt(player_turn: int, trumf_color: str, phase: int, card0: Card, card1: Card):
    if player_turn == 1:
        ft = first_takes_resolve(trumf_color, phase, card0, card1)
        if ft:
            return 0
        else:
            return 1
    else:
        ft = first_takes_resolve(trumf_color, phase, card1, card0)
        if ft:
            return 1
        else:
            return 0


def first_takes_resolve(trumf_color: str, phase: int, card0: Card, card1: Card):
    if (card0 == None) or (card1 == None):
        return None

    if phase == 0:
        if (card1.color == card0.color) and (VALUE_PREF[card1.value] > VALUE_PREF[card0.value]):
            return False
        else:
            return True

    if phase == 1:
        if (card1.color == card0.color) and (VALUE_PREF[card1.value] > VALUE_PREF[card0.value]):
            return False
        elif (card1.color != card0.color) and (card1.color == trumf_color):
            return False
        else:
            return True


def is_hlaska(chosen_card: Card, my_hand: Hand):
    hlaska = False
    if chosen_card.value == 'svrsek':
        if my_hand.iscardpresent(chosen_card.color, 'kral'):
            hlaska = True
    return hlaska


def get_simplified_card_list(cards: list[Card]):
    result: list[list[str]] = []
    for card in cards:
        result.append([card.color, card.value])
    return result


def get_list_as_cards(cards: list[list[str]]):
    result: list[Card] = []
    for card in cards:
        result.append(Card(card[0], card[1]))
    return result


def get_cards_of_oponent(history: History, card_db: list[list[str]], cards_in_hand: list[Card]):
    stych_list = history.stychy
    cards = card_db.copy()
    hist_simplified: list[Card] = []
    for stych in stych_list:
        hist_simplified.append(stych.card0)
        hist_simplified.append(stych.card1)

    for card in cards_in_hand:
        cards.remove([card.color, card.value])

    for card in hist_simplified:
        cards.remove([card.color, card.value])
    return cards


def get_card_db():
    result: list[list[str]] = []
    for color in COLORS:
        for value in VALUES:
            result.append([color, value])
    return result


def get_all_cards_as_class():
    result: list[Card] = []
    cardList = get_card_db()

    for card in cardList:
        result.append(Card(card[0], card[1]))
    return result


def get_cards_as_class(filter: list[list[str]]):
    result: list[Card] = []
    for card in filter:
        result.append(Card(card[0], card[1]))
    return result


def print_valid_card_moves(name: str, cards_in_hand: list, valid_moves: list):
    if LOGS:
        print("************************************")
        print("Hrac:", name)
        print("Ma v ruce:")
        for c in cards_in_hand:
            print(c)
        print("Muze hrat:")
        for c in valid_moves:
            print(c)
        print("************************************")
    return
