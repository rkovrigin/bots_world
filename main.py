import sys
from PyQt5.QtWidgets import QApplication
from animate_example import Qwidget
from world import World

DEFAULT_UNIV_X = 200
DEFAULT_UNIV_Y = 100
BOTS_AT_BEGINNING = 10
SCALE = 5

def main():
    app = QApplication(sys.argv)
    widget = Qwidget(DEFAULT_UNIV_X, DEFAULT_UNIV_Y, SCALE)
    world = World(DEFAULT_UNIV_X, DEFAULT_UNIV_Y, SCALE)
    app.exec_()

if __name__ == "__main__":
    main()
