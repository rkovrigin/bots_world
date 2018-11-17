from PyQt5.QtGui import QColor
import config

NO_TRANSPARENCY = 255
TRANSPARENT = 0


class Representation(object):
    def __init__(self, r, g, b, alpha=TRANSPARENT):
        self._color = QColor(r, g, b, alpha)
        self._increase = 10
        self._decrease = 10

    def increaseRed(self, amount=10):
        self._color.setRed(min(self.color.red() + amount, 255))
        self._color.setGreen(max(self.color.green() - self._decrease, 0))
        self._color.setBlue(max(self.color.blue() - self._decrease, 0))

    def increaseGreen(self, amount=10):
        self._color.setRed(max(self.color.red() - self._decrease, 0))
        self._color.setGreen(min(self.color.green() + amount, 255))
        self._color.setBlue(max(self.color.blue() - self._decrease, 0))

    def increaseBlue(self, amount=10):
        self._color.setRed(max(self.color.red() - self._decrease, 0))
        self._color.setGreen(max(self.color.green() - self._decrease, 0))
        self._color.setBlue(min(self.color.blue() + amount, 255))

    def setAlpha(self, alpha):
        self._color.setAlpha(alpha)

    @property
    def color(self):
        return self._color


RED = Representation(0xff, 0, 0)
BLUE = Representation(0x00, 0x00, 0xff)
GREEN = Representation(0x00, 0xff, 0x00)
YELLOW = Representation(0xff, 0xd5, 0)
ORANGE = Representation(0xff, 0x91, 0)
LIGHT_BLUE = Representation(0x00, 0xff, 0xff)
PURPLE = Representation(0xb7, 0x00, 0xff)
GRAY = GREY = UNKNOWN_BOT_COLOR = Representation(0x7a, 0x7a, 0x7a)
MAGENTA = Representation(0xff, 0x00, 0xff, 100)
UNKNOWN_MINERAL_COLOR = Representation(0xff, 0x00, 0xff, 50)

BOT_PREDATOR_KIND = 0xff0000
BOT_VEGAN_KIND    = 0x003400
BOT_MINERAL_KIND  = 0x000080

PRINT_STYLE_GREENRED = 0
PRINT_STYLE_GREENRED_ENERGY = 1
PRINT_STYLE_MULTICOLOR = 2
PRINT_STYLE_ENERGY = 3
PRINT_STYLE_NO_COLOR = 4
PRINT_STYLE_NO_DRAWING = 5


class MineralRepresentation(object):

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

    def print_style(self):
        if config.DRAWING_STYLE == PRINT_STYLE_GREENRED:
            return self.set_scene()
        elif config.DRAWING_STYLE == PRINT_STYLE_GREENRED_ENERGY:
            return self.set_scene_transparency()
        elif config.DRAWING_STYLE == PRINT_STYLE_MULTICOLOR:
            return self.set_scene_bot_kind()
        elif config.DRAWING_STYLE == PRINT_STYLE_ENERGY:
            return self.set_scene_energy()
        else:
            return UNKNOWN_MINERAL_COLOR


class BotRepresentation(object):
    def set_scene(self):
        self._color.setAlpha(200)
        return self._color
        # if self.kind == BOT_PREDATOR_KIND:
        #     return RED
        # elif self.kind == BOT_VEGAN_KIND:
        #     return GREEN
        # elif self.kind == BOT_MINERAL_KIND:
        #     return BLUE
        # else:
        #     return UNKNOWN_MINERAL_COLOR

    def set_scene_transparency(self):
        if self.energy > 255:
            transparancy = 255
        elif self.energy > 0 and self.energy < 100:
            transparancy = 100
        else:
            transparancy = self.energy

        if self.kind == BOT_PREDATOR_KIND:
            return Representation(255, 0, 0, transparancy)
        elif self.kind == BOT_VEGAN_KIND:
            return Representation(0, 255, 0, transparancy)
        elif self.kind == BOT_MINERAL_KIND:
            return Representation(0, 0, 255, transparancy)
        else:
            return UNKNOWN_BOT_COLOR

    def set_scene_bot_kind(self):
        if self.bitmap == BOT_PREDATOR_KIND:
            return RED
        elif self.bitmap == BOT_MINERAL_KIND:
            return BLUE
        elif self.bitmap == BOT_VEGAN_KIND:
            return GREEN
        elif self.bitmap == BOT_PREDATOR_KIND | BOT_VEGAN_KIND:
            return YELLOW
        elif self.bitmap == BOT_PREDATOR_KIND | BOT_MINERAL_KIND:
            return ORANGE
        elif self.bitmap == BOT_VEGAN_KIND | BOT_MINERAL_KIND:
            return LIGHT_BLUE
        elif self.bitmap == BOT_PREDATOR_KIND | BOT_MINERAL_KIND | BOT_VEGAN_KIND:
            return PURPLE
        else:
            return UNKNOWN_BOT_COLOR

    def set_scene_energy(self):
        if self.energy <= 0:
            energy = 0
        else:
            energy = self.energy
        return Representation(255, 255-energy, 0, energy)

    def print_style(self, print_style_id=None):
        if config.DRAWING_STYLE == PRINT_STYLE_GREENRED:
            return self.set_scene()
        elif config.DRAWING_STYLE == PRINT_STYLE_GREENRED_ENERGY:
            return self.set_scene_transparency()
        elif config.DRAWING_STYLE == PRINT_STYLE_MULTICOLOR:
            return self.set_scene_bot_kind()
        elif config.DRAWING_STYLE == PRINT_STYLE_ENERGY:
            return self.set_scene_energy()
        else:
            return UNKNOWN_BOT_COLOR