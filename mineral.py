from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from representation import *


class Mineral(object):
    _max_energy = 300

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

    @energy.setter
    def energy(self, energy):
        self._energy = energy
        if self._energy > self._max_energy:
            self._energy = self._max_energy

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
        if not self.is_alive:
            self._map.remove_candidate(x, y, self)
            return

        if self.energy <= 0:
            self.die()

        return
        # self.energy += 1
        if not self._map._wrapper_y:
            # self._map.move_mineral(x, y, x, y + 1)
            # pass
            if self._map.at(x, y+1) is not Mineral:
                self._map.move_mineral(x, y, x, y + 1)
                # self._map._map_minerals.move(x, y, x, y+1)

    def represent_itself(self, representation_no):
        if representation_no == PRINT_STYLE_RGB:
                return QColor(0xf4, 72, 0xd0, 255)
        elif representation_no == PRINT_STYLE_MAX_COLOR_VALUE:
                return QColor(0xf4, 72, 0xd0, 255)
        elif representation_no == PRINT_STYLE_NO_COLOR:
                return None
        elif representation_no == PRINT_STYLE_ENERGY:
                return QColor(0xf4, 72, 0xd0, 255)
