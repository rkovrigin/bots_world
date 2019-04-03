import math
import numpy as np

NO_GRADIENT = 0

class SunMap(object):
    __slots__ = ["_x", "_y", "_min", "_max", "_map"]

    def __init__(self, x, y, min, max):
        self._x = x
        self._y = y
        self._min = min
        self._max = max
        self._map = np.empty([x, y], dtype=int)
        self.set_sun()

    def set_sun(self):
        if self._max > self._min:
            step = (self._max - self._min) / self._y
            rate = step
            for y in range(self._y):
                for x in range(self._x):
                    self._map[x, y] = np.floor(rate)
                rate += step
        elif self._min > self._max:
            step = (self._min - self._max) / self._y
            rate = step
            for y in reversed(range(self._y)):
                for x in range(self._x):
                    self._map[x, y] = np.floor(rate)
                rate += step
        else:
            for y in reversed(range(self._y)):
                for x in range(self._x):
                    self._map[x, y] = self._min


    def sun_rate_at(self, x, y):
        return self._map[x, y]


class PoisonMap():
    __slots__ = ["_x", "_n", "_map"]

    def __init__(self, x, n=9):
        self._x = x
        self._n = n
        self._map = np.zeros([x], dtype=int)
        self.set_poison()

    def set_poison(self):
        step = self._x // self._n

        power = -1
        level = 0
        for i in range(0, math.ceil(self._n//2 + 1) * step, step):
            for j in range(i, i+step):
                self._map[j] = level
            for j in range(self._x-i-1, self._x-i-step-1, -1):
                self._map[j] = level
            power += 1
            level = 10**power

        print(self._map)