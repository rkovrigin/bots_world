import sys
import time

from PyQt5.QtGui import QSurfaceFormat
from PyQt5.QtWidgets import QApplication
from animate_example import Qwidget
from opengl_animation import WorldWindow
from world import World
from queue import Queue
from threading import Thread, Event

DEFAULT_UNIV_X = 200
DEFAULT_UNIV_Y = 100
BOTS_AT_BEGINNING = 100
SCALE = 6

def main():
    queue = Queue(maxsize=1000)
    event = Event()
    world = World(queue, DEFAULT_UNIV_X, DEFAULT_UNIV_Y, BOTS_AT_BEGINNING, event=event)

    world.start()
    while queue.empty():
        time.sleep(1)

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
    event.set()
    world.join()


if __name__ == "__main__":
    main()
