import numpy as np
import matplotlib.pyplot as plt

EMPTY = 0
BOT = 1
BOT_VEGAN = 2
BOT_PREDATOR = 3
BOTS = [BOT, BOT_VEGAN, BOT_PREDATOR]

class Map(object):
    _N = None
    _M = None
    _map = None
    _plt = None

    def __init__(self, n, m):
        self._N = n
        self._M = m
        self._map = np.zeros((self._N, self._M))

    def is_empty(self, x, y):
        if self._map[x][y] == EMPTY:
            return True

    def addBot(self, x, y):
        self._map[x][y] = BOT

    def show(self):
        plt.imshow(self._map, cmap='Greys')
        plt.show()

    def showBots(self, bots):
        for i in range(self._N):
            for j in range(self._M):
                self._map[i][j] = EMPTY
        for bot in bots:
            self._map[bot.x][bot.y] = BOT

        self.show()

    def print_2d(self):
        print self._map

    def print_manual(self):
        for i in range(self._N):
            for j in range(self._M):
                print self._map[i][j],
            print ''

    def at(self, x, y):
        return self._map[x][y]
