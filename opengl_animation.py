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
        QWidget)


class Helper(object):
    def __init__(self, x, y, scale):
        self.background = QBrush(QColor(255, 255, 255))
        self._x = x
        self._y = y
        self._scale = scale

    def set_scene(self, painter, map):
        for bot in map:
            if bot.predator:
                self.drawRect(painter, bot.x, bot.y, Qt.red)
            elif bot.age < 50:
                self.drawRect(painter, bot.x, bot.y, Qt.green)
            else:
                self.drawRect(painter, bot.x, bot.y, Qt.darkGreen)

    def drawRect(self, painter, x, y, color):
        painter.setBrush(color)
        painter.drawRect(x*self._scale, y*self._scale, self._scale, self._scale)

    def paint(self, painter, event, map):
        painter.fillRect(event.rect(), self.background)
        painter.save()

        self.set_scene(painter, map)
        # painter.drawText(QRect(0, self._y * self._scale, 100, 100), Qt.AlignCenter, "Bots: %s" % (len(map)))

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
        self.helper.paint(painter, event, map)
        painter.end()


class WorldWindow(QWidget):
    def __init__(self, queue, x, y, scale):
        super(WorldWindow, self).__init__()

        self.setWindowTitle("World of bots")

        helper = Helper(x, y, scale)
        openGLLabel = QLabel()
        openGLLabel.setAlignment(Qt.AlignHCenter)
        openGL = GLWidget(helper, self, queue, x, y, scale, openGLLabel)

        layout = QGridLayout()
        layout.addWidget(openGL, 0, 1)
        layout.addWidget(openGLLabel, 1, 1)
        self.setLayout(layout)

        timer = QTimer(self)
        timer.timeout.connect(openGL.animate)
        timer.start(50)


if __name__ == '__main__':

    app = QApplication(sys.argv)

    fmt = QSurfaceFormat()
    fmt.setSamples(1)
    QSurfaceFormat.setDefaultFormat(fmt)

    window = WorldWindow()
    window.show()
    sys.exit(app.exec_())
