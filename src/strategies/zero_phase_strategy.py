from engine.Card import Card
from engine.Constants import COLORS, VALUES
from engine.Hand import Hand
from engine.History import History
from tooling.Tools import compare_cards, get_all_cards_as_class, is_cer, is_kul, is_lis, is_zal

import random


def zero_phase_strategy(
        strategy: list[float],
        my_hand: Hand,
        valid_moves: list[Card],
        history: History,
        trumf_color: str,
        first: bool,
        opCard
):
    global card_to_play
    global possible_cards
    possible_cards = None
    card_to_play = None

    # Hardcoded rules
    #####################################################
    # If I had "svrsek" and "kral" in same color play "svrsek"?
    svrsek_val = VALUES[-3]
    kral_val = VALUES[-2]

    for color in COLORS:
        is_svrsek_present = my_hand.iscardpresent(color, svrsek_val)
        is_kral_present = my_hand.iscardpresent(color, kral_val)

        # succes scenario
        if is_svrsek_present and is_kral_present:
            card_to_play = Card(color, svrsek_val)
            break

    # play eso if you can
    for move in valid_moves:
        if move.value == "eso":
            card_to_play = move

    # play rule regardless of strategy
    if card_to_play != None:
        for valid_move in valid_moves:
            if valid_move.color == card_to_play.color and valid_move.value == card_to_play.value:
                return card_to_play

    #####################################################
    # Translate strategy
    # Common strategy (0-1)
    common = strategy[0:2]
    # For attack strategy (2-6)
    attack = strategy[2:7]
    # For defense strategy (7-8)
    defense = strategy[7:]
    #####################################################
    # Common
    index = valued_draw(common)

    if index == 0:
        possible_cards = common_strategy0(valid_moves, my_hand)
    if index == 1:
        if possible_cards != None:
            possible_cards = common_strategy1(possible_cards, my_hand)

    # Attacking
    if first:
        index2 = valued_draw(attack)

        if index2 == 0:
            if possible_cards != None:
                card_to_play = get_lowest_card(possible_cards)
            else:
                card_to_play = get_lowest_card(valid_moves)
        if index2 == 1:
            if possible_cards != None:
                card_to_play = get_highest_card(possible_cards)
            else:
                card_to_play = get_highest_card(valid_moves)
        if index2 == 2:
            if possible_cards != None:
                card_to_play = get_lowest_col_chance_of_oponent(
                    history, my_hand, opCard, possible_cards)
            else:
                card_to_play = get_lowest_col_chance_of_oponent(
                    history, my_hand, opCard, valid_moves)
        if index2 == 3:
            if possible_cards != None:
                card_to_play = get_highest_col_chance_of_oponent(
                    history, my_hand, opCard, possible_cards)
            else:
                card_to_play = get_highest_col_chance_of_oponent(
                    history, my_hand, opCard, valid_moves)

        if index2 == 4:
            if possible_cards != None:
                card_to_play = combine_highest_card_and_op_lowest_chance(
                    possible_cards, history, my_hand, opCard)
            else:
                card_to_play = combine_highest_card_and_op_lowest_chance(
                    valid_moves, history, my_hand, opCard)

        if card_to_play == None:
            return random.choice(valid_moves)
        return card_to_play

    # Defending
    else:
        index3 = valued_draw(defense)

        if index3 == 0:
            if possible_cards:
                card_to_play = get_lowest_card(possible_cards)
            else:
                card_to_play = get_lowest_card(valid_moves)
        if index3 == 1:
            if possible_cards:
                card_to_play = get_highest_card(possible_cards)
            else:
                card_to_play = get_highest_card(valid_moves)

        if card_to_play == None:
            return random.choice(valid_moves)
        return card_to_play


#########################################################
def common_strategy0(valid_moves: list[Card], my_hand: Hand,):
    svrsek_val = VALUES[-3]
    kral_val = VALUES[-2]

    # Save "svrsek" and "kral" else return NONE
    forbiden_moves: list[Card] = []

    for card in my_hand.cards:
        if card.value == svrsek_val or card.value == kral_val:
            forbiden_moves.append(card)

    # Filter forbiden moves from avaliable choices
    eligible_moves = valid_moves.copy()
    for move in valid_moves:
        for f_move in forbiden_moves:
            if compare_cards(move, f_move):
                eligible_moves.remove(f_move)

    return eligible_moves


def common_strategy1(valid_moves: list[Card], my_hand: Hand):
    eso_val = VALUES[-1]
    desitka_val = VALUES[-5]

    # Save "eso" and "desitky" else return NONE
    forbiden_moves: list[Card] = []

    for card in my_hand.cards:
        if card.value == eso_val or card.value == desitka_val:
            forbiden_moves.append(card)

    # Filter forbiden moves from avaliable choices
    eligible_moves = valid_moves.copy()
    for move in valid_moves:
        for f_move in forbiden_moves:
            if compare_cards(move, f_move):
                eligible_moves.remove(f_move)

    return eligible_moves
#########################################################


def get_highest_card(valid_moves: list[Card]):
    play_card = None

    for move in valid_moves:
        if play_card == None:
            play_card = move
        if move.value > play_card.value:
            play_card = move

    return play_card


def get_lowest_card(valid_moves: list[Card]):
    play_card = None

    for move in valid_moves:
        if play_card == None:
            play_card = move
        if move.value < play_card.value:
            play_card = move

    return play_card


def get_lowest_col_chance_of_oponent(history: History, my_hand: Hand, opCard: Card, valid_moves: list[Card]):
    cer_in_game, lis_in_game, zal_in_game, kul_in_game = assign_chances(
        opCard, history, my_hand)

    ls = [[COLORS[0], cer_in_game], [COLORS[1], lis_in_game],
          [COLORS[2], zal_in_game], [COLORS[3], kul_in_game]]

    def takeSecond(elem: list):
        return elem[1]

    ls.sort(key=takeSecond)

    c0 = find_valid(ls[0], valid_moves)
    c1 = find_valid(ls[1], valid_moves)
    c2 = find_valid(ls[2], valid_moves)
    c3 = find_valid(ls[3], valid_moves)

    if c0:
        return c0
    if c1:
        return c1
    if c2:
        return c2
    return c3


def get_highest_col_chance_of_oponent(history: History, my_hand: Hand, opCard: Card, valid_moves: list[Card]):
    cer_in_game, lis_in_game, zal_in_game, kul_in_game = assign_chances(
        opCard, history, my_hand)

    ls = [[COLORS[0], cer_in_game], [COLORS[1], lis_in_game],
          [COLORS[2], zal_in_game], [COLORS[3], kul_in_game]]

    def takeSecond(elem: list):
        return elem[1]

    ls.sort(key=takeSecond, reverse=True)

    c0 = find_valid(ls[0], valid_moves)
    c1 = find_valid(ls[1], valid_moves)
    c2 = find_valid(ls[2], valid_moves)
    c3 = find_valid(ls[3], valid_moves)

    if c0:
        return c0
    if c1:
        return c1
    if c2:
        return c2
    return c3


def find_valid(col: str, valid_moves: list[Card]):
    res = None
    for move in valid_moves:
        if col == move.color:
            res = move
            break
    return res


def combine_highest_card_and_op_lowest_chance(valid_moves: list[Card], history: History, my_hand: Hand, opCard: Card):
    cer_in_game, lis_in_game, zal_in_game, kul_in_game = assign_chances(
        opCard, history, my_hand)

    ls = [[COLORS[0], cer_in_game], [COLORS[1], lis_in_game],
          [COLORS[2], zal_in_game], [COLORS[3], kul_in_game]]

    def takeSecond(elem: list):
        return elem[1]

    ls.sort(key=takeSecond)
    play_card = None

    for move in valid_moves:
        if ls[0] == move.color and play_card == None:
            play_card = move
        if ls[0] == move.color and play_card != None and move.value < play_card.value:
            play_card = move

    if play_card == None:
        for move in valid_moves:
            if ls[1] == move.color and play_card == None:
                play_card = move
            if ls[1] == move.color and play_card != None and move.value < play_card.value:
                play_card = move

    if play_card == None:
        for move in valid_moves:
            if ls[2] == move.color and play_card == None:
                play_card = move
            if ls[2] == move.color and play_card != None and move.value < play_card.value:
                play_card = move

    if play_card == None:
        for move in valid_moves:
            if ls[3] == move.color and play_card == None:
                play_card = move
            if ls[3] == move.color and play_card != None and move.value < play_card.value:
                play_card = move
    return play_card


def assign_chances(opCard: Card, history: History, my_hand: Hand):
    known_cer = 0
    known_lis = 0
    known_zal = 0
    known_kul = 0

    all_cards = get_all_cards_as_class()
    n_cer = len(list(filter(is_cer, all_cards)))
    n_lis = len(list(filter(is_lis, all_cards)))
    n_zal = len(list(filter(is_zal, all_cards)))
    n_kul = len(list(filter(is_kul, all_cards)))

    def resolve(col: str):
        nonlocal known_cer
        nonlocal known_lis
        nonlocal known_zal
        nonlocal known_kul
        if col == COLORS[0]:
            known_cer = known_cer + 1
        if col == COLORS[1]:
            known_lis = known_lis + 1
        if col == COLORS[2]:
            known_zal = known_zal + 1
        if col == COLORS[3]:
            known_kul = known_kul + 1

    for stych in history.stychy:
        resolve(stych.card0.color)
        resolve(stych.card1.color)

    for card in my_hand.cards:
        resolve(card.color)

    if opCard != None:
        resolve(opCard.color)

    cer_in_game = n_cer - known_cer
    lis_in_game = n_lis - known_lis
    zal_in_game = n_zal - known_zal
    kul_in_game = n_kul - known_kul

    return cer_in_game, lis_in_game, zal_in_game, kul_in_game


def if_eso_retrurn_trumf_eso(valid_moves: list[Card], opCard: Card, trumf_color: str):
    global card_to_play
    if opCard.value == "desitka" or opCard.value == "eso":
        card_to_play = None
        for move in valid_moves:
            if move.color == trumf_color and move.value == "eso":
                card_to_play = move

    return card_to_play


def valued_draw(values: list[float]):
    sum_of_values = sum(values)
    normalized_values = [v / sum_of_values for v in values]
    cumulative_sum = 0
    edges = []

    for value in normalized_values:
        cumulative_sum = cumulative_sum + value
        edges.append(cumulative_sum)

    draw_number = random.random()
    for i, v in enumerate(edges):
        if draw_number < v:
            return i
