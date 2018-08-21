from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import random
import sys

from bot import Bot
from world import World

DEFAULT_UNIV_X = 100
DEFAULT_UNIV_Y = 100
BOTS_AT_BEGINNING = 100
SCALE = 5


class UniverseView(QGraphicsView):
    def __init__(self):
        QGraphicsView.__init__(self)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.drawUniverse(DEFAULT_UNIV_X, DEFAULT_UNIV_Y)

    def drawUniverse(self, rows, columns):
        self.scene.setSceneRect(QRectF(0, 0, rows*SCALE, columns*SCALE))

        for x in range(rows):
            self.scene.addLine(x*SCALE, 0, x*SCALE, columns*SCALE, QPen(Qt.black))

        for y in range(columns):
            self.scene.addLine(0, y*SCALE, rows*SCALE, y*SCALE, QPen(Qt.black))

    def drawCellAt(self, x, y, color=Qt.black, energy=None):
        item = QGraphicsRectItem(x*SCALE, y*SCALE, SCALE, SCALE)
        if energy is None:
            item.setBrush(QBrush(color))
        else:
            x = max(0, 255-energy)
            item.setBrush(QColor(x, x, x))
        self.scene.addItem(item)

    def clear_scene(self):
        self.scene.clear()

    def random_scene(self):
        for i in range(DEFAULT_UNIV_X):
            for j in range(DEFAULT_UNIV_Y):
                if not random.randrange(100) % 2:
                    self.drawCellAt(i, j)

    def set_scene(self, map):
        for bot, x, y in map.iterate_members(Bot):
            self.drawCellAt(x, y)

    def set_scene_bots(self, map):
        for bot, x, y in map.iterate_members(Bot):
            if bot.predator:
                self.drawCellAt(x, y, Qt.red)
            elif bot.age < 50:
                self.drawCellAt(x, y, Qt.green)
            else:
                self.drawCellAt(x, y, Qt.darkGreen)

        #self.drawUniverse(DEFAULT_UNIV_X, DEFAULT_UNIV_Y)

    def set_scene_energy(self, map):
        for bot, x, y in map.iterate_members(Bot):
            # energy = bot.energy

            # color = Qt.gray
            # if energy < 10:
            #     color = Qt.lightGray
            # elif energy < 30:
            #     color = Qt.yellow
            # elif energy < 50:
            #     color = Qt.darkYellow
            # elif energy < 100:
            #     color = Qt.red
            # elif energy < 200:
            #     color = Qt.darkRed
            # elif energy < 500:
            #     color = Qt.magenta
            # else:
            #     color = Qt.black
            # self.drawCellAt(x, y, color)

            self.drawCellAt(x, y, energy=bot.energy)


class Qwidget(QWidget):

    def __init__(self):
        super(Qwidget, self).__init__()
        # self.size = size
        self.game = None
        self.world = World(DEFAULT_UNIV_X, DEFAULT_UNIV_Y, BOTS_AT_BEGINNING)
        self.label = QLabel()
        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowTitle(self.tr("Game of Life"))
        self.setLayout(QVBoxLayout())

        self.comboBox = QComboBox()
        self.comboBox.currentTextChanged.connect(self.select)

        self.view = UniverseView()
        self.layout().addWidget(self.view)

        self.item = None
        self.timer = QTimer()
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.tick)
        self.layout().addWidget(self.label)
        self.select()

    def select(self):
        self.timer.stop()
        self.tick()
        self.timer.start()

    def tick(self):
        # self.view.clear_scene()
        test = self.world.cycle()
        # self.view.set_scene(self.world._map)
        # self.view.set_scene_bots(self.world._map)
        self.label.setText(test)
        # self.view.set_scene_energy(self.world._map)

app = QApplication(sys.argv)
# gol = GameOfLifeApp()
# gol.show()

w = Qwidget()
app.exec_()