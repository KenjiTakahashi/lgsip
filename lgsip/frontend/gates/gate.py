# -*- coding: utf-8 -*-
# This is a part of lgsip @ http://github.com/KenjiTakahashi/lgsip/
# Karol "Kenji Takahashi" Wozniak (C) 2012
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QSize


class Gate(QtGui.QWidget):
    def __init__(self, inputs=1, outputs=1, parent=None):
        super(Gate, self).__init__(parent)
        self.path = QtGui.QPainterPath()
        self.h = 20 + 20 * (inputs - 1)
        delta = self.h / (inputs + 1)
        for i in range(1, inputs + 1):
            self.path.addRect(0, delta * i - 2, 10, 4)
        delta = self.h / (outputs + 1)
        for i in range(1, outputs + 1):
            self.path.addRect(50, delta * i - 2, 10, 4)

    def paintEvent(self, event):
        super(Gate, self).paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QtGui.QPalette().mid())
        painter.drawPath(self.path)

    def sizeHint(self):
        return QSize(60, self.h)
