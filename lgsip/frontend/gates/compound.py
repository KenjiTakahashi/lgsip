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

from lgsip.frontend.gates import basic
from lgsip.engine.gates import compound
from PyQt4.QtCore import QPointF
from PyQt4 import QtGui


class Nand(basic.And):
    def _doGate(self, inputs):
        self._gate = compound.Nand(inputs)

    def _drawPath(self):
        super(Nand, self)._drawPath()
        self.path.addEllipse(60, self.h / 2 - 5, 10, 10)


class Nor(basic.Or):
    def _doGate(self, inputs):
        self._gate = compound.Nor(inputs)

    def _drawPath(self):
        super(Nor, self)._drawPath()
        self.path.addEllipse(60, self.h / 2 - 5, 10, 10)


class Xor(basic.Or):
    def __init__(self, parent=None):
        super(Xor, self).__init__(2, parent=parent)

    def _doGate(self, _):
        self._gate = compound.Xor()

    def _wireButtons(self):
        return False

    def _drawPath(self):
        super(Xor, self)._drawPath()
        self.path2 = QtGui.QPainterPath()
        self.path2.moveTo(10, 0)
        self.path2.quadTo(QPointF(20, self.h / 2), QPointF(10, self.h))

    def paintEvent(self, event):
        super(Xor, self).paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen(QtGui.QPalette().mid(), 2)
        painter.strokePath(self.path2, pen)


class Xnor(Xor):
    def __init__(self, parent=None):
        super(Xnor, self).__init__(parent)

    def _doGate(self, _):
        self._gate = compound.Xnor()

    def _wireButtons(self):
        return False

    def _drawPath(self):
        super(Xnor, self)._drawPath()
        self.path.addEllipse(60, self.h / 2 - 5, 10, 10)
