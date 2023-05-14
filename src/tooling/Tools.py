from config import LOGS


def get_cards_of_oponent():
    return


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
