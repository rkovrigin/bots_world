from representation import *

MAGENTA = Representation(0xff, 0x00, 0xff)


class MineralRepresentation(object):
    UNKNOWN_MINERAL_COLOR = GRAY

    def set_scene(self):
        return MAGENTA

    def set_scene_transparency(self):
        if self.quantity < 50:
            transparancy = 50
        elif self.quantity > 255:
            transparancy = 255
        else:
            transparancy = self.quantity
        return Representation(0xf4, 72, 0xd0, transparancy)

    def set_scene_bot_kind(self):
        return self.set_scene_transparency()

    def set_scene_energy(self):
        if self.quantity > 255:
            transparancy = 255
        else:
            transparancy = self.quantity
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
    def __init__(self, map, quantity=255):
        self._quantity = quantity

        self._is_active = True
        self._map = map

    @property
    def is_alive(self):
        return self._is_active

    @property
    def quantity(self):
        return self._quantity

    def die(self):
        self._is_active = False
        # print("The mineral is exhausted")

    def bite_piece(self, size):
        if not self.is_alive:
            return 0
        if size < 0:
            return 0

        bite = min(size, self._quantity)
        self._quantity -= bite

        if self._quantity <= 0:
            self.die()

        return bite

    def execute_command(self, x, y):
        if self._quantity > 0:
            self._quantity += 1
