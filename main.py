import sys
from PyQt5.QtWidgets import QApplication
from animate_example import Qwidget
from world import World
from queue import Queue
from threading import Thread

DEFAULT_UNIV_X = 200
DEFAULT_UNIV_Y = 100
BOTS_AT_BEGINNING = 100
SCALE = 5

def main():
    queue = Queue(maxsize=100)
    app = QApplication(sys.argv)
    widget = Qwidget(queue, DEFAULT_UNIV_X, DEFAULT_UNIV_Y, SCALE)
    world = World(queue, DEFAULT_UNIV_X, DEFAULT_UNIV_Y, BOTS_AT_BEGINNING)

    world.start()
    app.exec_()

if __name__ == "__main__":
    main()
