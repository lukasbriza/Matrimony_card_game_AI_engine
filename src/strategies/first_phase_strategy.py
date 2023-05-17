from engine.Card import Card
from engine.Hand import Hand
from tooling.Tools import evaluate_wt
import copy


class GameState():
    def __init__(self, id: int):
        self.id: int = id
        self.player_cards: list[Card] = None
        self.player_points: int = 0
        self.player_played: Card = None

        self.enemy_cards: list[Card] = None
        self.enemy_points: int = 0
        self.enemy_played: Card = None

        self.playerturn = 0

    def is_done(self):
        if len(self.player_cards) == 0 and len(self.enemy_cards):
            return True
        return False

    def is_cardpresent(self, cards: list[Card], col, val):
        for c in cards:
            if c.color == col and c.value == val:
                return True
        return False

    def is_hlaska(self, cards: list[Card], chosen_card: Card):
        hlaska = False
        if chosen_card.value == "svrsek":
            if self.is_cardpresent(cards, chosen_card.color, "kral"):
                hlaska = True
        return hlaska


class StrategyDicision():
    def __init__(self):
        self.player_wins = 0
        self.enemy_wins = 0


def first_phase_strategy(
        oponent_cards: list[Card],
        my_cards: list[Card],
        first: bool,
        trumf_color: str
):
    global strategy
    ########################################################################################
    # Generate first level of gamestates
    root_nodes: list[GameState] = get_root_nodes(
        oponent_cards, my_cards, first, trumf_color)

    root_copy: list[GameState] = []
    for node in root_nodes:
        state = GameState(node.id)
        state.enemy_cards = node.enemy_cards
        state.enemy_points = node.enemy_points
        state.enemy_played = node.enemy_played
        state.player_cards = node.player_cards
        state.player_played = node.player_played
        state.player_points = node.player_points
        state.playerturn = node.playerturn
        root_copy.append(state)
    ########################################################################################
    # Get all posible moves
    evaluated_list = recursive_state_generation(root_copy, trumf_color)
    ########################################################################################
    # Build dictionary for decision
    evaluation_dict: dict[str, StrategyDicision] = {}
    for state in evaluated_list:

        if (str(state.id) in evaluation_dict) == False:
            new_dictionary = StrategyDicision()
            evaluation_dict[str(state.id)] = new_dictionary

        if state.player_points > state.enemy_points:
            evaluation_dict[str(state.id)].player_wins = evaluation_dict[str(
                state.id)].player_wins + 1
        if state.player_points < state.enemy_points:
            evaluation_dict[str(state.id)].enemy_wins = evaluation_dict[str(
                state.id)].enemy_wins + 1
    ########################################################################################
    #
    strategy = 0
    gap = 0
    for key in evaluation_dict:
        new_gap = evaluation_dict[key].player_wins - \
            evaluation_dict[key].enemy_wins
        if new_gap > gap:
            strategy = int(key)

    return root_nodes[strategy].player_played


def get_root_nodes(
    oponent_cards: list[Card],
    my_cards: list[Card],
    first: bool,
    trumf_color: str
):
    hand0 = Hand()
    hand0.cards = my_cards

    hand1 = Hand()
    hand1.cards = oponent_cards

    root_nodes: list[GameState] = []
    id = 0
    if first:
        valid0 = hand0.validcardmoves(None, 1, trumf_color)

        for card0 in valid0:
            valid1 = hand1.validcardmoves(card0, 1, trumf_color)
            for card1 in valid1:
                state, hlaska0, hlaska1 = process_game_state(
                    0, hand0, hand1, card0, card1, id)

                # Evaluate players
                wt = None
                wt = evaluate_wt(state.playerturn,
                                 trumf_color, 1, card0, card1)
                evaluate_move(wt, state, hlaska0, hlaska1, trumf_color)

                root_nodes.append(state)
                id = id + 1
    else:
        valid1 = hand1.validcardmoves(None, 1, trumf_color)
        for card1 in valid1:
            valid0 = hand0.validcardmoves(card1, 1, trumf_color)
            for card0 in valid0:
                state, hlaska0, hlaska1 = process_game_state(
                    1, hand0, hand1, card0, card1, id)

                # Evaluate players
                wt = None
                wt = evaluate_wt(state.playerturn,
                                 trumf_color, 1, card0, card1)
                evaluate_move(wt, state, hlaska0, hlaska1, trumf_color)

                root_nodes.append(state)
                id = id + 1
    return root_nodes


def process_game_state(playerturn: int, hand0: Hand, hand1: Hand, card0: Card, card1: Card, id: int):
    state = GameState(id)
    state.playerturn = playerturn

    # Player game state
    player_hand = hand0.cards.copy()
    state.player_played = card0
    hlaska0 = state.is_hlaska(player_hand, card0)
    player_hand.remove(card0)
    state.player_cards = player_hand

    # Enemy game state
    enemy_hand = hand1.cards.copy()
    state.enemy_played = card1
    hlaska1 = state.is_hlaska(enemy_hand, card1)
    enemy_hand.remove(card1)
    state.enemy_cards = enemy_hand

    return state, hlaska0, hlaska1


def recursive_state_generation(game_states: list[GameState], trumf_color: str):
    #######################################################
    # break recursive rule
    counter = 0
    for state in game_states:
        if len(state.enemy_cards) == 0 and len(state.player_cards) == 0:
            counter = counter + 1
    if counter == len(game_states):
        return game_states.copy()
    #######################################################
    new_states: list[GameState] = []

    for state in game_states:
        # Reset played card
        state.enemy_played = None
        state.player_played = None

        # Play first flow
        if state.playerturn == 1:
            # Player
            hand0 = Hand()
            hand0.cards = state.player_cards.copy()
            valid0 = hand0.validcardmoves(None, 1, trumf_color)

            # Enemy
            hand1 = Hand()
            hand1.cards = state.enemy_cards

            for card0 in valid0:
                valid1 = hand1.validcardmoves(card0, 1, trumf_color)
                for card1 in valid1:
                    new_state, hlaska0, hlaska1 = process_game_state(
                        state.playerturn, hand0, hand1, card0, card1, state.id)
                    new_state.player_points = state.player_points
                    new_state.enemy_points = state.enemy_points

                    # Evaluate players
                    wt = None
                    wt = evaluate_wt(new_state.playerturn,
                                     trumf_color, 1, card0, card1)
                    evaluate_move(wt, new_state, hlaska0, hlaska1, trumf_color)

                    # Add new state to list of variants
                    new_states.append(new_state)

        # Play second flow
        else:
            # Player
            hand0 = Hand()
            hand0.cards = state.player_cards.copy()

            # Enemy
            hand1 = Hand()
            hand1.cards = state.enemy_cards
            valid1 = hand1.validcardmoves(None, 1, trumf_color)

            for card1 in valid1:
                valid0 = hand0.validcardmoves(card1, 1, trumf_color)
                for card0 in valid0:
                    new_state, hlaska0, hlaska1 = process_game_state(
                        state.playerturn, hand0, hand1, card0, card1, state.id)
                    new_state.player_points = state.player_points
                    new_state.enemy_points = state.enemy_points

                    # Evaluate players
                    wt = None
                    wt = evaluate_wt(new_state.playerturn,
                                     trumf_color, 1, card0, card1)
                    evaluate_move(wt, new_state, hlaska0, hlaska1, trumf_color)

                    # Add new state to list of variants
                    new_states.append(new_state)

    return recursive_state_generation(new_states, trumf_color)


def evaluate_move(
    wt: int,
    state: GameState,
    hlaska0: bool,
    hlaska1: bool,
    trumf_color: str
):
    if wt == 0:
        state.player_points = state.player_points + \
            state.player_played.points + state.enemy_played.points
        state.playerturn = 0

        if state.is_done():
            state.player_points = state.player_points + 10
    else:
        state.enemy_points = state.enemy_points + \
            state.player_played.points + state.enemy_played.points
        state.playerturn = 1

        if state.is_done():
            state.enemy_points = state.enemy_points + 10

    if hlaska0:
        if state.player_played.color == trumf_color:
            state.player_points = state.player_points + 40
        else:
            state.player_points = state.player_points + 20
    if hlaska1:
        if state.enemy_played.color == trumf_color:
            state.enemy_points = state.enemy_points + 40
        else:
            state.enemy_points = state.enemy_points + 20

    return
