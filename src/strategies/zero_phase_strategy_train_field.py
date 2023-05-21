import numpy as np
import random
from deap import base, creator, tools, algorithms
import matplotlib.pyplot as plt
from engine.Hand import Hand
from engine.History import History

from engine.Player import Player
from engine.Talon import Talon

from engine.Card import Card
from engine.Constants import COLORS, VALUES
from strategies.zero_phase_strategy import zero_phase_strategy
from tooling.Tools import evaluate_wt, first_takes_resolve, is_hlaska, print_valid_card_moves

CXPB = 0.5  # crossover chance
MUTPB = 0.2  # mutation chance
NGEN = 20
POPULATION_SIZE = 100
STRATEGY_SIZE = 10


def plotStats(mean, maximum):
    fig, ax = plt.subplots()
    ax.plot(range(NGEN+1), mean, label="mean")     # 0.tá generace zvlášť
    ax.plot(range(NGEN+1), maximum, label="max")
    ax.legend()
    plt.show()


def evaluationFunction(individual: list[int], p: list[list[int]]):
    POPULATION = p
    number_of_wins = 0

    for oponent_strategy in POPULATION:
        me_first = GameSimulation(individual, oponent_strategy)
        me_second = GameSimulation(oponent_strategy, individual)

        mf_my_result, mf_oponet_result = me_first.play()
        ms_oponent_result, ms_my_result = me_second.play()

        if mf_my_result > mf_oponet_result:
            number_of_wins = number_of_wins + 1
        if ms_my_result > ms_oponent_result:
            number_of_wins = number_of_wins + 1

    return number_of_wins,


def trainStrategy():
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("attr_init", random.random)
    toolbox.register("individual", tools.initRepeat,
                     creator.Individual, toolbox.attr_init, n=STRATEGY_SIZE)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    pop = toolbox.population(n=POPULATION_SIZE)
    toolbox.register("evaluate", evaluationFunction, p=pop)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("mutate", tools.mutUniformInt, low=0, up=1, indpb=MUTPB)

    statistics = tools.Statistics(key=lambda ind: ind.fitness.values)
    statistics.register("mean", np.mean)
    statistics.register("max", np.max)
    hof = tools.HallOfFame(2)
    finalpop, logbook = algorithms.eaSimple(
        pop, toolbox, cxpb=CXPB, mutpb=MUTPB, ngen=NGEN, stats=statistics, halloffame=hof)
    mean, maximum = logbook.select("mean", "max")

    plotStats(mean, maximum)
    print(hof[0])


class TrainPlayer:
    def __init__(self, num: int, name: str, strategy: list[float]):
        self.num = num
        self.name = name
        self.strategy = strategy
        self.hand = Hand()

    def isdone(self):
        if self.hand.isempty():
            return True
        return False

    def addcard(self, card):
        self.hand.addcard(card)

    def play(self, history: History, phase: int, trumfcolor: str, first=True, opcard=None):
        if not self.isdone():
            hlaska = False

            if first:
                # play first
                cm = self.hand.validcardmoves(None, phase, trumfcolor)
                print_valid_card_moves(self.name, self.hand.cards, cm)

                card = zero_phase_strategy(
                    self.strategy, self.hand.cards, cm, history, trumfcolor, first, opcard)
                hlaska = is_hlaska(card, self.hand)
                self.hand.removecard(card.color, card.value)

                return card, hlaska
            else:
                # play second
                cm = self.hand.validcardmoves(opcard, phase, trumfcolor)
                print_valid_card_moves(self.name, self.hand.cards, cm)

                card = zero_phase_strategy(
                    self.strategy, self.hand.cards, cm, history, trumfcolor, first, opcard)
                hlaska = is_hlaska(card, self.hand)
                self.hand.removecard(card.color, card.value)

                return card, hlaska

        return None, False


class GameSimulation:
    def __init__(self, strategy0: list[float], strategy1: list[float]):
        cards: list[Card] = [Card(b, h) for b in COLORS for h in VALUES]
        self.talon: Talon = Talon(cards)
        self.talon.shuffle()

        self.player0: Player = Player(0, "strategy0")
        self.player1: Player = Player(1, "strategy1")

        # distribute cards
        for i in range(5):
            self.player0.addcard(self.talon.popcard())

        for i in range(5):
            self.player1.addcard(self.talon.popcard())

        self.trumfcolor: str = self.talon.cards[0].color
        self.lastcard: Card = self.talon.cards[0]

        # posledni tah
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
            # End game
            return self.player0points, self.player1points

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

        wt = None
        wt = evaluate_wt(self.playerturn, self.trumfcolor, self.phase, c0, c1)

        self.history.add(self.phase, self.lastcard0, self.lastcard1,
                         self.lasthlaska0, self.lasthlaska1, wt)

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

        # loop till talon is empty
        return self.play()
