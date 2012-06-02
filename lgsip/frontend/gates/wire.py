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
from PyQt4.QtCore import QRectF, Qt


class Wire(QtGui.QGraphicsObject):
    def __init__(self, x=0, y=0, propagating=False, inGate=False):
        super(Wire, self).__init__()
        self.x, self.y = x, y
        self.nx, self.ny = x, y
        self.propagating = propagating
        self.inGate = inGate

    def setLine(self, x, y):
        self.nx, self.ny = x, y

    def boundingRect(self):
        return QRectF(self.x, self.y, self.x + self.nx, self.y + self.ny)

    def paint(self, painter, option, widget):
        pen = QtGui.QPen()
        pen.setWidth(4)
        pen.setColor(QtGui.QColor(QtGui.QPalette().mid()))
        painter.setPen(pen)
        painter.drawLine(self.x, self.y, self.nx, self.ny)
        if self.propagating:
            dpen = QtGui.QPen()
            dpen.setWidth(4)
            dpen.setDashPattern([3, 4])
            dpen.setColor(Qt.red)
            painter.setPen(dpen)
            painter.drawLine(self.x, self.y, self.nx, self.ny)
