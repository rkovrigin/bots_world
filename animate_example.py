from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import random
import sys
from world import World
from map import BOT, EMPTY

DEFAULT_UNIV_X = 100
DEFAULT_UNIV_Y = 60
SCALE = 8


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

    def drawCellAt(self, x, y, color=Qt.black):
        # if random.randrange(2) == 0:
        #     color = Qt.black
        # else:
        #     color = Qt.red
        item = QGraphicsRectItem(x*SCALE, y*SCALE, SCALE, SCALE)
        item.setBrush(QBrush(color))
        self.scene.addItem(item)

    def clearScene(self):
        self.scene.clear()

    def random_scene(self):
        for i in range(DEFAULT_UNIV_X):
            for j in range(DEFAULT_UNIV_Y):
                if not random.randrange(100) % 2:
                    self.drawCellAt(i,j)

    def set_scene(self, map):
        for x in range(map._N):
            for y in range(map._M):
                if map.at(x,y) == BOT:
                    self.drawCellAt(x, y)

    def set_scene_bots(self, bots):
        for bot in bots:
            if bot.age < 15:
                self.drawCellAt(bot.x, bot.y, Qt.green)
            elif bot._max_age - bot.age <= 20:
                self.drawCellAt(bot.x, bot.y, Qt.gray)
            else:
                self.drawCellAt(bot.x, bot.y)

class Qwidget(QWidget):

    def __init__(self):
        super(Qwidget, self).__init__()
        # self.size = size
        self.game = None
        self.world = World(DEFAULT_UNIV_X, DEFAULT_UNIV_Y, 100)
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
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.tick)
        self.select()

    def select(self):
        self.timer.stop()
        self.tick()
        self.timer.start()

    def tick(self):
        self.view.clearScene()
        self.world.cycle()
        # self.view.set_scene(self.world._map)
        self.view.set_scene_bots(self.world._bots)

app = QApplication(sys.argv)
# gol = GameOfLifeApp()
# gol.show()

w = Qwidget()
app.exec_()