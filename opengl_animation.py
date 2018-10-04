#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2015 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


import sys
import math
import random

from PyQt5.QtCore import QPointF, QRect, QRectF, Qt, QTimer
from PyQt5.QtGui import QBrush, QColor, QFont, QLinearGradient, QPainter, QPen, QSurfaceFormat
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QOpenGLWidget, QWidget
from PyQt5.QtWidgets import QPushButton, QCheckBox, QGroupBox, QRadioButton, QVBoxLayout

import config
from representation import PRINT_STYLE_GREENRED, PRINT_STYLE_GREENRED_ENERGY, PRINT_STYLE_NO_COLOR, \
    PRINT_STYLE_MULTICOLOR, PRINT_STYLE_ENERGY, PRINT_STYLE_NO_DRAWING


class GLWidget(QOpenGLWidget):
    def __init__(self, parent, queue, x, y, scale):
        super(GLWidget, self).__init__(parent)

        self.elapsed = 0
        self._x = x
        self._y = y
        self._scale = scale
        self._queue = queue
        self._parent = parent
        self._print_style = PRINT_STYLE_GREENRED
        self.setFixedSize(x*scale, y*scale)
        self.setAutoFillBackground(False)
        self.background = QBrush(QColor(255, 255, 255))
        self._members = None
        self._click_x = None
        self._click_y = None

    def animate(self):
        self.elapsed = (self.elapsed + self.sender().interval()) % 1000
        self.update()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self._members = self._queue.get()
        fps = 666
        self._parent.openGLLabel.setText("Frames: %d; Bots: %d; FPS: %f" % (self._queue.qsize(), len(self._members), fps))
        self.paint(painter, event, self._members)
        painter.end()

    def drawRect(self, painter, x, y):
        painter.drawRect(x*self._scale, y*self._scale, self._scale, self._scale)

    def paint(self, painter, event, members):
        painter.fillRect(event.rect(), self.background)
        painter.save()

        if config.DRAWING_STYLE == PRINT_STYLE_NO_COLOR:
            for repr, x, y, energy, commands in members:
                self.drawRect(painter, x, y)
        elif config.DRAWING_STYLE != PRINT_STYLE_NO_DRAWING:
            for repr, x, y, energy in members:
                if x < 0 or x >= 200 or y < 0 or y >= 200:
                    print("OUT OF MAP: [%d:%d] {%d}" % (x, y, energy))
                #if type(repr) in (list, tuple):
                painter.setBrush(repr.color)
                #else:
                #    painter.setBrush(repr.color)
                self.drawRect(painter, x, y)

                if x == self._click_x and y == self._click_y:
                    self._parent.openGLLabel_commands.setText("Coordinates [%d:%d]; Energy {%d}" % (x, y, energy))

                # if x == self._click_x and y == self._click_y and len(commands) > 0:
                #     print_pattern = (("%d " * 8) + "\n")*8
                #     text = print_pattern % tuple(commands)
                #     text += "Energy %d" % energy
                #     self._parent.openGLLabel_commands.setText("%d %d" % (x, y))
                #     self._click_x = None
                #     self._click_y = None

        painter.restore()

    def mousePressEvent(self, event):
        self._click_x = int(event.localPos().x() // self._scale)
        self._click_y = int(event.localPos().y() // self._scale)


class WorldWindow(QWidget):
    def __init__(self, queue, x, y, scale):
        super(WorldWindow, self).__init__()

        self.setWindowTitle("World of bots")

        self.openGLLabel = QLabel()
        self.openGLLabel_commands = QLabel()
        self.openGLLabel.setAlignment(Qt.AlignHCenter)
        self.openGLLabel.setAlignment(Qt.AlignLeft)
        self.openGL = GLWidget(self, queue, x, y, scale)

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

        timer = QTimer(self)
        timer.timeout.connect(self.openGL.animate)
        timer.start(1)

    def create_radio_button_group(self):
        groupBox = QGroupBox("View style")

        self.radioGreenRed = QRadioButton("Green/Red/Blue")
        self.radioGreenRed.toggled.connect(self.radio_button_color_is_checked)

        self.radioGreenRedEnergy = QRadioButton("Green/Red/Blue energy")
        self.radioGreenRedEnergy.toggled.connect(self.radio_button_color_is_checked)

        self.radioNoColor = QRadioButton("No color")
        self.radioNoColor.toggled.connect(self.radio_button_color_is_checked)

        self.radioMultiColor = QRadioButton("Multicolor")
        self.radioMultiColor.toggled.connect(self.radio_button_color_is_checked)

        self.radioEnergy = QRadioButton("Energy")
        self.radioEnergy.toggled.connect(self.radio_button_color_is_checked)

        self.noDrawing = QRadioButton("No drawing")
        self.noDrawing.toggled.connect(self.radio_button_color_is_checked)

        if config.DRAWING_STYLE == PRINT_STYLE_GREENRED:
            self.radioGreenRed.setChecked(True)
        elif config.DRAWING_STYLE == PRINT_STYLE_GREENRED_ENERGY:
            self.radioGreenRedEnergy.setChecked(True)
        elif config.DRAWING_STYLE == PRINT_STYLE_NO_COLOR:
            self.radioNoColor.setChecked(True)
        elif config.DRAWING_STYLE == PRINT_STYLE_MULTICOLOR:
            self.radioMultiColor.setChecked(True)
        elif config.DRAWING_STYLE == PRINT_STYLE_ENERGY:
            self.radioEnergy.setChecked(True)
        elif config.DRAWING_STYLE == PRINT_STYLE_NO_DRAWING:
            self.noDrawing.setChecked(True)
        else:
            raise Exception("config.DRAWING_STYLE is set incorrectly")

        vbox = QVBoxLayout()
        vbox.addWidget(self.radioGreenRed)
        vbox.addWidget(self.radioGreenRedEnergy)
        vbox.addWidget(self.radioMultiColor)
        vbox.addWidget(self.radioEnergy)
        vbox.addWidget(self.radioNoColor)
        vbox.addWidget(self.noDrawing)
        groupBox.setLayout(vbox)

        return groupBox

    def radio_button_color_is_checked(self, checked=True):
        if not checked:
            return

        if self.radioGreenRed.isChecked():
            config.DRAWING_STYLE = PRINT_STYLE_GREENRED
        elif self.radioGreenRedEnergy.isChecked():
            config.DRAWING_STYLE = PRINT_STYLE_GREENRED_ENERGY
        elif self.radioNoColor.isChecked():
            config.DRAWING_STYLE = PRINT_STYLE_NO_COLOR
        elif self.radioMultiColor.isChecked():
            config.DRAWING_STYLE = PRINT_STYLE_MULTICOLOR
        elif self.radioEnergy.isChecked():
            config.DRAWING_STYLE = PRINT_STYLE_ENERGY
        elif self.noDrawing.isChecked():
            config.DRAWING_STYLE = PRINT_STYLE_NO_DRAWING
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
