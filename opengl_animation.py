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
from PyQt5.QtGui import (QBrush, QColor, QFont, QLinearGradient, QPainter,
        QPen, QSurfaceFormat)
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QOpenGLWidget,
                             QWidget, QPushButton, QCheckBox, QGroupBox, QRadioButton, QVBoxLayout)

from bot import Bot_short_info, BOT_PREDATOR_KIND, BOT_VEGAN_KIND, BOT_MINERAL_KIND
from mineral import Mineral_short_info

PRINT_STYLE = {
    0 : "Green/Red",
    1 : "Green/Red energy",
    2 : "No color",
    3 : "Multicolor",
    4 : "Energy",
}


class Helper(object):
    def __init__(self, x, y, scale):
        self.background = QBrush(QColor(255, 255, 255))
        self._x = x
        self._y = y
        self._scale = scale

    def set_scene(self, painter, map):
        for member in map:
            if isinstance(member, Bot_short_info):
                if member.kind == BOT_PREDATOR_KIND:
                    self.drawRect(painter, member.x, member.y, Qt.red)
                elif member.kind == BOT_VEGAN_KIND:
                    self.drawRect(painter, member.x, member.y, Qt.green)
                elif member.kind == BOT_MINERAL_KIND:
                    self.drawRect(painter, member.x, member.y, Qt.blue)
                else:
                    raise Exception("No such bot kind")
            elif isinstance(member, Mineral_short_info):
                self.drawRect(painter, member.x, member.y, Qt.magenta)
            else:
                raise Exception("No such kind of object %r" % member)

    def set_scene_transparency(self, painter, map):
        for member in map:
            if isinstance(member, Bot_short_info):
                if member.energy > 255:
                    transparancy = 255
                elif member.energy < 100:
                    transparancy = 100
                else:
                    transparancy = member.energy

                if member.kind == BOT_PREDATOR_KIND:
                    color = QColor(255, 0, 0, transparancy)
                elif member.kind == BOT_VEGAN_KIND:
                    color = QColor(0, 255, 0, transparancy)
                elif member.kind == BOT_MINERAL_KIND:
                    color = QColor(0, 0, 255, transparancy)
            elif isinstance(member, Mineral_short_info):
                if member.quantity < 50:
                    transparancy = 50
                elif member.quantity > 255:
                    transparancy = 255
                else:
                    transparancy = member.quantity
                color = QColor(0xf4, 72, 0xd0, transparancy)

            self.drawRect(painter, member.x, member.y, color)

    def set_scene_bot_kind(self, painter, map):
        for member in map:
            if isinstance(member, Bot_short_info):
                if member.energy > 255:
                    transparancy = 255
                elif member.energy < 100:
                    transparancy = 100
                else:
                    transparancy = member.energy

                r = (member.color & BOT_PREDATOR_KIND) >> 16
                g = (member.color & BOT_VEGAN_KIND) >> 8
                b = member.color & BOT_MINERAL_KIND

                color = QColor(r, g, b, 200)

            elif isinstance(member, Mineral_short_info):
                if member.quantity < 50:
                    transparancy = 50
                elif member.quantity > 255:
                    transparancy = 255
                else:
                    transparancy = member.quantity
                color = QColor(0xf4, 72, 0xd0, transparancy)

            self.drawRect(painter, member.x, member.y, color)

    def set_scene_no_color(self, painter, map):
        for member in map:
            self.drawRect(painter, member.x, member.y, None)

    def set_scene_energy(self, painter, map):
        for member in map:
            if isinstance(member, Bot_short_info):
                if member.energy > 255:
                    transparancy = 255
                else:
                    transparancy = member.energy

                color = QColor(255, 255-transparancy, 0, transparancy)
            elif isinstance(member, Mineral_short_info):
                if member.quantity > 255:
                    transparancy = 255
                else:
                    transparancy = member.quantity
                color = QColor(0xe5, 0x69, 0xf5, transparancy)
            self.drawRect(painter, member.x, member.y, color)


    def drawRect(self, painter, x, y, color):
        if color is not None:
            painter.setBrush(color)
        painter.drawRect(x*self._scale, y*self._scale, self._scale, self._scale)

    def paint(self, painter, event, map, print_style):
        painter.fillRect(event.rect(), self.background)
        painter.save()

        if print_style == PRINT_STYLE[0]:
            self.set_scene(painter, map)
        elif print_style == PRINT_STYLE[1]:
            self.set_scene_transparency(painter, map)
        elif print_style == PRINT_STYLE[2]:
            self.set_scene_no_color(painter, map)
        elif print_style == PRINT_STYLE[3]:
            self.set_scene_bot_kind(painter, map)
        elif print_style == PRINT_STYLE[4]:
            self.set_scene_energy(painter, map)

        painter.restore()


class GLWidget(QOpenGLWidget):
    def __init__(self, helper, parent, queue, x, y, scale, label):
        super(GLWidget, self).__init__(parent)

        self.helper = helper
        self.elapsed = 0
        self._x = x
        self._y = y
        self._scale = scale
        self._queue = queue
        self._label = label
        self._print_style = PRINT_STYLE[0]
        self.setFixedSize(x*scale, y*scale)
        self.setAutoFillBackground(False)

    def animate(self):
        self.elapsed = (self.elapsed + self.sender().interval()) % 1000
        self.update()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        map = self._queue.get()
        self._label.setText("Frames: %d; Bots: %d" % (self._queue.qsize(), len(map)))
        self.helper.paint(painter, event, map, self._print_style)
        painter.end()


class WorldWindow(QWidget):
    def __init__(self, queue, x, y, scale):
        super(WorldWindow, self).__init__()

        self.setWindowTitle("World of bots")

        helper = Helper(x, y, scale)
        openGLLabel = QLabel()
        openGLLabel.setAlignment(Qt.AlignHCenter)
        self.openGL = GLWidget(helper, self, queue, x, y, scale, openGLLabel)

        layout = QGridLayout()
        layout.addWidget(self.openGL, 0, 1)
        layout.addWidget(openGLLabel, 1, 1)
        self.setLayout(layout)

        self.button_box = self.createRadioButtonGroup()
        layout.addWidget(self.button_box)

        timer = QTimer(self)
        timer.timeout.connect(self.openGL.animate)
        timer.start(1)

    def createRadioButtonGroup(self):
        groupBox = QGroupBox("View style")

        self.radioGreenRed = QRadioButton("Green/Red/Blue")
        self.radioGreenRed.toggled.connect(self.radioButtonColor)

        self.radioGreenRedEnergy = QRadioButton("Green/Red/Blue energy")
        self.radioGreenRedEnergy.toggled.connect(self.radioButtonColor)

        self.radioNoColor = QRadioButton("No color")
        self.radioNoColor.toggled.connect(self.radioButtonColor)

        self.radioMultiColor = QRadioButton("Multicolor")
        self.radioMultiColor.toggled.connect(self.radioButtonColor)

        self.radioEnergy = QRadioButton("Energy")
        self.radioEnergy.toggled.connect(self.radioButtonColor)

        self.radioGreenRed.setChecked(True)
        vbox = QVBoxLayout()
        vbox.addWidget(self.radioGreenRed)
        vbox.addWidget(self.radioGreenRedEnergy)
        vbox.addWidget(self.radioNoColor)
        vbox.addWidget(self.radioMultiColor)
        vbox.addWidget(self.radioEnergy)
        groupBox.setLayout(vbox)

        return groupBox

    def radioButtonColor(self, checked=True):
        if not checked:
            return

        if self.radioGreenRed.isChecked():
            self.openGL._print_style = PRINT_STYLE[0]
        elif self.radioGreenRedEnergy.isChecked():
            self.openGL._print_style = PRINT_STYLE[1]
        elif self.radioNoColor.isChecked():
            self.openGL._print_style = PRINT_STYLE[2]
        elif self.radioMultiColor.isChecked():
            self.openGL._print_style = PRINT_STYLE[3]
        elif self.radioEnergy.isChecked():
            self.openGL._print_style = PRINT_STYLE[4]
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
