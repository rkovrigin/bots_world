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
            self._map[self._x, self._y] = self._min


    def sun_rate_at(self, x, y):
        return self._map[x, y]
