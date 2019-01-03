import sys
import os
import math
import random
import datetime
import time

from PyQt5.QtCore import QPointF, QRect, QRectF, Qt, QTimer, QSize
from PyQt5.QtGui import QBrush, QColor, QFont, QLinearGradient, QPainter, QPen, QSurfaceFormat, QImage
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QOpenGLWidget, QWidget
from PyQt5.QtWidgets import QPushButton, QCheckBox, QGroupBox, QRadioButton, QVBoxLayout

import config
from representation import PRINT_STYLE_RGB, PRINT_STYLE_MAX_COLOR_VALUE, PRINT_STYLE_NO_COLOR, PRINT_STYLE_ENERGY, \
    PRINT_NO_DRAW


class GLWidget(QOpenGLWidget):
    def __init__(self, parent, x, y, scale):
        super(GLWidget, self).__init__(parent)

        self.elapsed = 0
        self._x = x
        self._y = y
        self._scale = scale
        self._parent = parent
        self._print_style = PRINT_STYLE_RGB
        self.setFixedSize(x*scale, y*scale)
        self.setAutoFillBackground(False)
        self.background = QBrush(QColor(255, 255, 255))
        self._members = None
        self._click_x = None
        self._click_y = None
        self.painter = QPainter()
        self.painterImg = QPainter()
        self.img = QImage(900, 450, QImage.Format_ARGB32)
        self.count = 0

    def animate(self, members):
        self._members = members
        self.elapsed = 1#(self.elapsed + self.sender().interval()) % 1000
        self.update()

    def saveImage(self):
        name = os.path.join("C:\\", "Users", "roman.kovrigin", "sandbox", "bots", "bots_world", "out", str(time.time()) + ".png")
        try:
            ret = self.img.save(name, "PNG")
            # print("Save with %s %d" % (name, ret))
        except Exception as e:
            print(e)

    def paintEvent(self, event):
        # if self.count % 10 == 0:
        self.painter.begin(self)
        self._parent.openGLLabel.setText("Day: %d" % (config.DAY, ))
        if self._members:
            self.paint(self.painter, event, self._members)
        self.painter.end()


        # self.painterImg.begin(self.img)
        # self.paint(self.painterImg, event, self._members)
        # self.painterImg.end()
        # self.saveImage()
        #
        # self.count += 1

        # if self._queue.empty():
        #     exit(0)
        # self.paintGL(self.painterImg, event, self._members)
        # self.painter.save()
        # self.painter.restore()
        # print(img.save("C:\\Users\\roman.kovrigin\\sandbox\\bots\\bots_world\\out\\1", "PNG"))

    def drawRect(self, painter, x, y):
        painter.drawRect(x*self._scale, y*self._scale, self._scale, self._scale)

    def paint(self, painter, event, members):
        if config.DRAWING_STYLE == PRINT_NO_DRAW:
            return

        painter.fillRect(event.rect(), self.background)

        if config.DRAWING_STYLE == PRINT_STYLE_NO_COLOR:
            for _, x, y in members:
                self.drawRect(painter, x, y)
        else:
            for repr, x, y in members:
                painter.setBrush(repr)
                self.drawRect(painter, x, y)
            #if x == self._elif config.DRAWING_STYLE == PRINT_STYLE_NO_COLOR:click_x and y == self._click_y:
            #    self._parent.openGLLabel_commands.setText("Coordinates [%d:%d:%d]; Energy {%d}" % (repr.red, repr.green, repr.blue, repr.energy))

    def mousePressEvent(self, event):
        self._click_x = int(event.localPos().x() // self._scale)
        self._click_y = int(event.localPos().y() // self._scale)


class WorldWindow(QWidget):
    def __init__(self, x, y, scale):
        super(WorldWindow, self).__init__()

        self.setWindowTitle("World of bots")

        self.openGLLabel = QLabel()
        self.openGLLabel_commands = QLabel()
        self.openGLLabel.setAlignment(Qt.AlignHCenter)
        self.openGLLabel.setAlignment(Qt.AlignLeft)
        self.openGL = GLWidget(self, x, y, scale)

        layout = QGridLayout()
        # layout.addWidget(self.openGL, 0, 1)
        # layout.addWidget(self.openGLLabel, 1, 1)
        # layout.addWidget(self.openGLLabel_commands, 1, 1)
        layout.addWidget(self.openGL)
        layout.addWidget(self.openGLLabel)
        layout.addWidget(self.openGLLabel_commands)
        self.setLayout(layout)

        self.button_box = self.create_radio_button_group()
        layout.addWidget(self.button_box)

        #timer = QTimer(self)
        #timer.timeout.connect(self.openGL.animate)
        #timer.start(30)

    def create_radio_button_group(self):
        groupBox = QGroupBox("View style")

        self.radioRGB = QRadioButton("RGB")
        self.radioRGB.toggled.connect(self.radio_button_color_is_checked)

        self.radioMaxColorValue = QRadioButton("Max color")
        self.radioMaxColorValue.toggled.connect(self.radio_button_color_is_checked)

        self.radioNoColor = QRadioButton("No color")
        self.radioNoColor.toggled.connect(self.radio_button_color_is_checked)

        self.radioEnergy = QRadioButton("Energy")
        self.radioEnergy.toggled.connect(self.radio_button_color_is_checked)

        self.radioNoDraw = QRadioButton("No draw")
        self.radioNoDraw.toggled.connect(self.radio_button_color_is_checked)

        if config.DRAWING_STYLE == PRINT_STYLE_RGB:
            self.radioRGB.setChecked(True)
        elif config.DRAWING_STYLE == PRINT_STYLE_MAX_COLOR_VALUE:
            self.radioMaxColorValue.setChecked(True)
        elif config.DRAWING_STYLE == PRINT_STYLE_NO_COLOR:
            self.radioNoColor.setChecked(True)
        elif config.DRAWING_STYLE == PRINT_STYLE_ENERGY:
            self.radioEnergy.setChecked(True)
        elif config.DRAWING_STYLE == PRINT_NO_DRAW:
            self.radioNoDraw.setChecked(True)
        else:
            raise Exception("config.DRAWING_STYLE is set incorrectly")

        vbox = QVBoxLayout()
        vbox.addWidget(self.radioRGB)
        vbox.addWidget(self.radioMaxColorValue)
        vbox.addWidget(self.radioEnergy)
        vbox.addWidget(self.radioNoColor)
        vbox.addWidget(self.radioNoDraw)
        groupBox.setLayout(vbox)

        return groupBox

    def radio_button_color_is_checked(self, checked=True):
        if not checked:
            return

        if self.radioRGB.isChecked():
            config.DRAWING_STYLE = PRINT_STYLE_RGB
        elif self.radioMaxColorValue.isChecked():
            config.DRAWING_STYLE = PRINT_STYLE_MAX_COLOR_VALUE
        elif self.radioNoColor.isChecked():
            config.DRAWING_STYLE = PRINT_STYLE_NO_COLOR
        elif self.radioEnergy.isChecked():
            config.DRAWING_STYLE = PRINT_STYLE_ENERGY
        elif self.radioNoDraw.isChecked():
            config.DRAWING_STYLE = PRINT_NO_DRAW
        else:
            raise Exception("No radio button is chosen")


if __name__ == '__main__':

    app = QApplication(sys.argv)

    fmt = QSurfaceFormat()
    fmt.setSamples(1)
    QSurfaceFormat.setDefaultFormat(fmt)

    window = WorldWindow()
    window.show()
    sys.exit(app.exec_())
