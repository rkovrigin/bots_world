from threading import Thread

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import random
import sys

from bot import Bot
from world import World


class UniverseView(QGraphicsView):
    def __init__(self, x, y, scale):
        QGraphicsView.__init__(self)
        self._x = x
        self._y = y
        self._scale = scale
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.drawUniverse(x, y)

    def drawUniverse(self, rows, columns):
        self.scene.setSceneRect(QRectF(0, 0, rows*self._scale, columns*self._scale))

        for x in range(rows):
            self.scene.addLine(x*self._scale, 0, x*self._scale, columns*self._scale, QPen(Qt.black))

        for y in range(columns):
            self.scene.addLine(0, y*self._scale, rows*self._scale, y*self._scale, QPen(Qt.black))

    def drawCellAt(self, x, y, color=Qt.black):
        item = QGraphicsRectItem(x*self._scale, y*self._scale, self._scale, self._scale)
        item.setBrush(QBrush(color))
        self.scene.addItem(item)

    def drawEnergyCellAt(self, x, y, energy):
        if energy < 10:
            color = Qt.lightGray
        elif energy < 30:
            color = Qt.yellow
        elif energy < 50:
            color = Qt.darkYellow
        elif energy < 100:
            color = Qt.red
        elif energy < 200:
            color = Qt.darkRed
        elif energy < 500:
            color = Qt.magenta
        else:
            color = Qt.black
        self.drawCellAt(x, y, color)

    def drawEnergyGrayCellAt(self, x, y, energy):
        item = QGraphicsRectItem(x*self._scale, y*self._scale, self._scale, self._scale)
        x = max(0, 255-energy)
        item.setBrush(QColor(x, x, x))
        self.scene.addItem(item)

    def clear_scene(self):
        self.scene.clear()

    def random_scene(self):
        for i in range(self._x):
            for j in range(self._y):
                if not random.randrange(100) % 2:
                    self.drawCellAt(i, j)

    def set_scene(self, map):
        for bot, x, y in map.iterate_members():
            self.drawCellAt(x, y)

    def set_scene_rainbow(self, map):
        for bot, x, y in map.iterate_members():
            #energy = max(0, 255 - bot.energy)
            #age = min(bot.age, 255)
            self.drawCellAt(x, y, QColor(150, x*256/map.x, y*256/map.y))


    def set_scene_bots(self, map):
        for bot, x, y in map.iterate_members():
            if bot.predator:
                self.drawCellAt(x, y, Qt.red)
            elif bot.age < 50:
                self.drawCellAt(x, y, Qt.green)
            else:
                self.drawCellAt(x, y, Qt.darkGreen)

        #self.drawUniverse(DEFAULT_UNIV_X, DEFAULT_UNIV_Y)

    def set_scene_energy(self, map):
        for bot, x, y in map.iterate_members():
            self.drawEnergyCellAt(x, y, bot.energy)
            #self.drawEnergyGrayCellAt(x, y, bot.energy)


class Qwidget(QWidget):
    def __init__(self, queue, x, y, scale):
        super(Qwidget, self).__init__()
        self._x = x
        self._y = y
        self._scale = scale
        # self.size = size
        self.game = None
        self.queue = queue
        # self.world = World(DEFAULT_UNIV_X, DEFAULT_UNIV_Y, BOTS_AT_BEGINNING)
        self.label = QLabel()
        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowTitle(self.tr("Game of Life"))
        self.setLayout(QVBoxLayout())

        self.comboBox = QComboBox()
        self.comboBox.currentTextChanged.connect(self.select)

        self.view = UniverseView(self._x, self._x, self._scale)
        self.layout().addWidget(self.view)

        self.item = None
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.tick)
        self.layout().addWidget(self.label)
        self.select()

    def select(self):
        self.timer.stop()
        self.tick()
        self.timer.start()

    def tick(self):
        self.view.clear_scene()
        # test = self.world.cycle()
        #self.view.set_scene(self.world._map)
        if not self.queue.empty():
            map = self.queue.get()
            self.view.set_scene_bots(map)
        else:
            print("Queue is empty")
        # self.view.set_scene_rainbow(self.world._map)
        # self.view.set_scene_energy(self.world._map)
        # self.label.setText(test)