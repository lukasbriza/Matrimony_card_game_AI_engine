from engine.Stych import Stych


class History:
    def __init__(self):
        self.stychy = []

    def add(self, phase, card0, card1, hlaska0, hlaska1, wt):
        self.stychy.append(Stych(phase, card0, card1, hlaska0, hlaska1, wt))

    def getlast(self):
        return self.stychy[-1]
