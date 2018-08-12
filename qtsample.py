import random
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

DEFAULT_UNIV_X = 10
DEFAULT_UNIV_Y = 10
SCALE = 30

class UniverseView(QGraphicsView):
    def __init__(self):
        QGraphicsView.__init__(self)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.drawUniverse(DEFAULT_UNIV_X, DEFAULT_UNIV_Y)

    def drawUniverse(self, rows, columns):
        """Draw the universe grid.
        """
        self.scene.setSceneRect(QRectF(0, 0, rows*SCALE, columns*SCALE))

        # draw vertical lines
        for x in range(rows):
            self.scene.addLine(x*SCALE, 0, x*SCALE, columns, QPen(Qt.black))

        # draw horrizontal lines
        for y in range(columns):
            self.scene.addLine(0, y*SCALE, rows, y*SCALE, QPen(Qt.black))

    def drawCellAt(self, x, y):
        """Fill the cell at grid location (x, y)
        """
        item = QGraphicsRectItem(x*SCALE, y*SCALE, SCALE, SCALE)
        item.setBrush(QBrush(Qt.black))
        self.scene.addItem(item)

    def clearScene(self):
        """Clear the scene.
        """
        # self.scene.clear()

    def random_scene(self):
        self.clearScene()
        for i in range(DEFAULT_UNIV_X):
            for j in range(DEFAULT_UNIV_Y):
                if not random.randrange(100) %2:
                    self.drawCellAt(i,j)


class GameOfLifeApp(QDialog):
    """Main Dialog window for GameOfLife
    """

    def __init__(self, parent=None):
        super(GameOfLifeApp, self).__init__(parent)
        # Qt Graphics view where the whole action happens
        self.universeView = UniverseView()
        self.setGeometry(0,0,400, 400)

        # set the window layout
        layout = QVBoxLayout()
        layout.addWidget(self.universeView)

        self.patternBox = QComboBox()
        self.universeView.random_scene()
        self.setLayout(layout)

        self.setWindowTitle('Bots')

app = QApplication(sys.argv)
gol = GameOfLifeApp()
gol.show()
app.exec_()

print("hello")