import numpy as np

NO_GRADIENT = 0
MAX_UP = 1
MAX_DOWN = 2

class SunMap(object):
    __slots__ = ["_x", "_y", "_min", "_max", "_gradient", "_map"]

    def __init__(self, x, y, min, max, gradient=MAX_UP):
        self._x = x
        self._y = y
        self._min = min
        self._max = max
        self._gradient = gradient
        self._map = np.empty([x, y], dtype=int)
        self.set_sun()

    def set_sun(self):
        step = self._y // (self._max - self._min)
        sun_rate = self._min
        i = 0

        if self._gradient == MAX_DOWN:
            for y in range(self._y):
                for x in range(self._x):
                    self._map[x, y] = sun_rate
                i = (i + 1) % 6
                if i == 0:
                    sun_rate += step
        elif self._gradient == MAX_UP:
            for y in reversed(range(self._y)):
                for x in range(self._x):
                    self._map[x, y] = sun_rate
                i = (i + 1) % 6
                if i == 0:
                    sun_rate += step
        elif self._gradient == NO_GRADIENT:
            self._map[self._x, self._y] = (self._max - self._min)//2

    def sun_rate_at(self, x, y):
        return self._map[x, y]
