import sys
import time

from PyQt5.QtGui import QSurfaceFormat
from PyQt5.QtWidgets import QApplication
from animate_example import Qwidget
from opengl_animation import WorldWindow
from world import World
from queue import Queue
from threading import Thread

DEFAULT_UNIV_X = 36
DEFAULT_UNIV_Y = 10
BOTS_AT_BEGINNING = 50
MINERALS_AT_BEGINNING = 0
SCALE = 10

exit_flag = 0


def main():
    # return world.run()

    # app = QApplication(sys.argv)
    # widget = Qwidget(queue, DEFAULT_UNIV_X, DEFAULT_UNIV_Y, SCALE)
    # app.exec_()
    # # print(queue.qsize())

    app = QApplication(sys.argv)

    fmt = QSurfaceFormat()
    fmt.setSamples(4)
    QSurfaceFormat.setDefaultFormat(fmt)

    window = WorldWindow(DEFAULT_UNIV_X, DEFAULT_UNIV_Y, SCALE)


    world = World(window.openGL.animate, DEFAULT_UNIV_X, DEFAULT_UNIV_Y, BOTS_AT_BEGINNING, MINERALS_AT_BEGINNING)
    world.start()

    window.show()

    app.exec_()
    app.exit()


    world.finish_him()
    world.join()


if __name__ == "__main__":
    main()
