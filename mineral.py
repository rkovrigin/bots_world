from collections import namedtuple


Mineral_short_info = namedtuple("Mineral_short_info", ["x", "y", "is_active", "quantity"])


class Mineral(object):

    def __init__(self, map, quantity=None):
        if quantity is None:
            self._quantity = 255

        self._is_active = True
        self._map = map

    @property
    def is_active(self):
        return self._is_active

    def exhaust(self):
        self._is_active = False
        # print("The mineral is exhausted")

    def bite_piece(self, size):
        if not self.is_active:
            return 0
        if size < 0:
            return 0

        bite = min(size, self._quantity)
        self._quantity -= bite

        if self._quantity <= 0:
            self.exhaust()

        return bite

    def grow(self):
        if self._quantity > 0:
            self._quantity += 1