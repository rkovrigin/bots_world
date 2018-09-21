from representation import *

MAGENTA = Representation(0xff, 0x00, 0xff)


class MineralRepresentation(object):
    UNKNOWN_MINERAL_COLOR = GRAY

    def set_scene(self):
        return MAGENTA

    def set_scene_transparency(self):
        if self.energy < 50:
            transparancy = 50
        elif self.energy > 255:
            transparancy = 255
        else:
            transparancy = self.energy
        return Representation(0xf4, 72, 0xd0, transparancy)

    def set_scene_bot_kind(self):
        return self.set_scene_transparency()

    def set_scene_energy(self):
        if self.energy > 255:
            transparancy = 255
        else:
            transparancy = self.energy
        return Representation(0xe5, 0x69, 0xf5, transparancy)

    def print_style(self, print_style_id=None):
        if print_style_id is None:
            return (
                self.set_scene(),
                self.set_scene_transparency(),
                self.set_scene_bot_kind(),
                self.set_scene_energy(),
            )

        if print_style_id == PRINT_STYLE_GREENRED:
            return self.set_scene()
        elif print_style_id == PRINT_STYLE_GREENRED_ENERGY:
            return self.set_scene_transparency()
        elif print_style_id == PRINT_STYLE_MULTICOLOR:
            return self.set_scene_bot_kind()
        elif print_style_id == PRINT_STYLE_ENERGY:
            return self.set_scene_energy()
        else:
            return self.UNKNOWN_MINERAL_COLOR


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
