from representation import *


class Mineral(MineralRepresentation):
    def __init__(self, map, energy=255):
        self._energy = energy
        self._commands = []

        self._is_active = True
        self._map = map

    @property
    def is_alive(self):
        return self._is_active

    @property
    def energy(self):
        return self._energy

    def die(self):
        self._is_active = False
        # print("The mineral is exhausted")

    def bite_piece(self, size):
        if not self.is_alive:
            return 0
        if size < 0:
            return 0

        bite = min(size, self._energy)
        self._energy -= bite

        if self._energy <= 0:
            self.die()

        return bite

    def execute_command(self, x, y):
        if self._energy > 0:
            self._energy += 1
