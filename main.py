import sys
import time

from PyQt5.QtGui import QSurfaceFormat
from PyQt5.QtWidgets import QApplication
from animate_example import Qwidget
from opengl_animation import WorldWindow
from world import World
from queue import Queue
from threading import Thread

DEFAULT_UNIV_X = 100
DEFAULT_UNIV_Y = 50
BOTS_AT_BEGINNING = 800
MINERALS_AT_BEGINNING = 800
SCALE = 5

exit_flag = 0


def main():
    queue = Queue(1000)
    world = World(queue, DEFAULT_UNIV_X, DEFAULT_UNIV_Y, BOTS_AT_BEGINNING, MINERALS_AT_BEGINNING)
    # return world.run()

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
    app.exit()


    world.finish_him()
    world.join()


if __name__ == "__main__":
    main()
