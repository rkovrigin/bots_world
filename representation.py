from collections import namedtuple

NO_TRANSPARENCY = 255
TRANSPARENT = 0
MAX_VALUE = 255


class Representation(object):
    def __init__(self, r, g, b, alpha=TRANSPARENT):
        self.r = r
        self.g = g
        self.b = b
        self._increase = 10
        self._decrease = 10

    def increaseRed(self, amount=10):
        self.r = min(self.r + amount, MAX_VALUE)
        self.g = max(self.g - self._decrease, 0)
        self.b = max(self.b - self._decrease, 0)

    def increaseGreen(self, amount=10):
        self.r = max(self.r - self._decrease, 0)
        self.g = min(self.g + amount, MAX_VALUE)
        self.b = max(self.b - self._decrease, 0)

    def increaseBlue(self, amount=10):
        self.r = max(self.r - self._decrease, 0)
        self.g = max(self.g - self._decrease, 0)
        self.b = min(self.b + amount, MAX_VALUE)


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

PRINT_STYLE_RGB = 0
PRINT_STYLE_MAX_COLOR_VALUE = 1
PRINT_STYLE_ENERGY = 2
PRINT_STYLE_NO_COLOR = 3

Cell = namedtuple('Cell', ["red", "green", "blue", "energy", "kind"])