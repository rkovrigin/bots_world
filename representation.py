from PyQt5.QtGui import QColor

NO_TRANSPARENCY = 255


class Representation(object):
    def __init__(self, r, g, b, alpha=NO_TRANSPARENCY):
        self._color = QColor(r, g, b, alpha)

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
GRAY = GREY = Representation(0x7a, 0x7a, 0x7a)

PRINT_STYLE_GREENRED = 0
PRINT_STYLE_GREENRED_ENERGY = 1
PRINT_STYLE_MULTICOLOR = 2
PRINT_STYLE_ENERGY = 3
PRINT_STYLE_NO_COLOR = 4
PRINT_STYLE_NO_DRAWING = 5
