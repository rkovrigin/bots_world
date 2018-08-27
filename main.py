import sys
import time

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
    world = World(queue, DEFAULT_UNIV_X, DEFAULT_UNIV_Y, BOTS_AT_BEGINNING)

    world.start()
    while queue.empty():
        time.sleep(1)

    app = QApplication(sys.argv)
    widget = Qwidget(queue, DEFAULT_UNIV_X, DEFAULT_UNIV_Y, SCALE)
    app.exec_()
    # print(queue.qsize())


if __name__ == "__main__":
    main()
