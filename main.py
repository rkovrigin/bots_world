import sys
import time

from PyQt5.QtGui import QSurfaceFormat
from PyQt5.QtWidgets import QApplication
from animate_example import Qwidget
from opengl_animation import WorldWindow
from world import World
from queue import Queue
from threading import Thread

DEFAULT_UNIV_X = 60
DEFAULT_UNIV_Y = 30
BOTS_AT_BEGINNING = 60
MINERALS_AT_BEGINNING = 100
SCALE = 10

exit_flag = 0


def main():
    queue = Queue(maxsize=1)
    world = World(queue, DEFAULT_UNIV_X, DEFAULT_UNIV_Y, BOTS_AT_BEGINNING, MINERALS_AT_BEGINNING)

    world.start()

    # app = QApplication(sys.argv)
    # widget = Qwidget(queue, DEFAULT_UNIV_X, DEFAULT_UNIV_Y, SCALE)
    # app.exec_()
    # # print(queue.qsize())

    app = QApplication(sys.argv)

    fmt = QSurfaceFormat()
    fmt.setSamples(4)
    QSurfaceFormat.setDefaultFormat(fmt)

    window = WorldWindow(queue, DEFAULT_UNIV_X, DEFAULT_UNIV_Y, SCALE)
    window.show()

    app.exec_()

    world.finish_him()
    world.join()


if __name__ == "__main__":
    main()
