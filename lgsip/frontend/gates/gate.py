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
from PyQt4.QtCore import Qt, QSize, QPointF, QPoint, pyqtSignal


class _LgsipGateButton(QtGui.QPushButton):
    def __init__(self, parent=None):
        super(_LgsipGateButton, self).__init__(parent)
        self.path = QtGui.QPainterPath()
        self.path.setFillRule(Qt.WindingFill)
        self.setFlat(True)
        self.setFixedSize(QSize(16, 16))

    def paintEvent(self, event):
        super(_LgsipGateButton, self).paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color)
        painter.drawPath(self.path)


class RemoveWireButton(_LgsipGateButton):
    def __init__(self, parent=None):
        super(RemoveWireButton, self).__init__(parent)
        self.path.addRect(3, 6, 10, 4)
        self.color = QtGui.QColor(160, 0, 0)


class AddWireButton(_LgsipGateButton):
    def __init__(self, parent=None):
        super(AddWireButton, self).__init__(parent)
        self.path.addRect(3, 6, 10, 4)
        self.path.addRect(6, 3, 4, 10)
        self.color = QtGui.QColor(0, 160, 0)


class DeleteGateButton(_LgsipGateButton):
    def __init__(self, parent=None):
        super(DeleteGateButton, self).__init__(parent)
        self.path.addPolygon(QtGui.QPolygonF([
            QPointF(3, 5), QPointF(5, 3), QPointF(13, 11), QPointF(11, 13)
        ]))
        self.path.addPolygon(QtGui.QPolygonF([
            QPointF(3, 11), QPointF(5, 13), QPointF(13, 5), QPointF(11, 3)
        ]))
        self.color = QtGui.QColor(0, 0, 160)


class DesintegrateGateButton(_LgsipGateButton):
    def __init__(self, parent=None):
        super(DesintegrateGateButton, self).__init__(parent)
        self.path.addPolygon(QtGui.QPolygonF([
            QPointF(3, 8), QPointF(6, 3), QPointF(8, 5),
            QPointF(5, 8), QPointF(8, 13), QPointF(6, 13)
        ]))
        self.path.addPolygon(QtGui.QPolygonF([
            QPointF(8, 5), QPointF(10, 3), QPointF(13, 8),
            QPointF(10, 13), QPointF(8, 13), QPointF(11, 8)
        ]))
        self.color = QtGui.QColor(0, 0, 160)


class WireButton(_LgsipGateButton):
    def __init__(self, parent=None):
        super(WireButton, self).__init__(parent)
        self.setFixedSize(QSize(20, 4))
        self.path.addRect(0, 0, 20, 4)
        self.color = QtGui.QPalette().mid()


class Gate(QtGui.QWidget):
    wiring = pyqtSignal(int, int, int)

    def __init__(self, inputs=1, outputs=1, parent=None):
        super(Gate, self).__init__(parent)
        self._sketched = False
        self._integrated = False
        self._wires = list()
        self.setStyleSheet('background-color: transparent;')
        self.setFixedWidth(80)
        self.offset = QPoint()
        self._buttons = set()
        self._inputs = inputs
        self._outputs = outputs
        self._drawWires()
        self._drawButtons()
        self._drawPath()

    def _drawWires(self):
        if self._inputs:
            self.h = 24 + 24 * (self._inputs - 1)
        elif self._outputs:
            self.h = 24 + 24 * (self._outputs - 1)
        else:  # this should never happen
            self.h = 40
        delta = self.h / (self._inputs + 1)
        for i in range(1, self._inputs + 1):
            button = WireButton(self)
            button.move(0, delta * i - 2)
            button.clicked.connect(self._wiringIn)
            self._buttons.add(button)
        delta = self.h / (self._outputs + 1)
        for i in range(1, self._outputs + 1):
            button = WireButton(self)
            button.move(60, delta * i - 2)
            button.clicked.connect(self._wiringOut)
            self._buttons.add(button)

    def _drawButtons(self):
        delta = self.h / 2
        self.delete = DeleteGateButton(self)
        self._buttons.add(self.delete)
        if self._integrated:
            self.delete.move(20, delta - 16)
            self.desintegrate = DesintegrateGateButton(self)
            self.desintegrate.move(20, delta - 4)
            self._buttons.add(self.desintegrate)
        else:
            self.delete.move(20, delta - 8)

    def _drawPath(self):
        self.path = QtGui.QPainterPath()

    def _wiringIn(self):
        pos = self.sender().pos()
        self.wiring.emit(0, pos.y() + 2, 0)

    def _wiringOut(self):
        pos = self.sender().pos()
        self.wiring.emit(80, pos.y() + 2, 1)

    def setSketched(self, val):
        self._sketched = val

    def appendWire(self, wire, inOut, pos):
        self._wires.append((wire, inOut, pos))

    def removeWire(self, wire, inOut):
        for wire, inOut, pos in self._wires:
            if wire == wire and inOut == inOut:
                self._wires.remove((wire, inOut, pos))

    def paintEvent(self, event):
        super(Gate, self).paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QtGui.QPalette().mid())
        painter.drawPath(self.path)

    def mousePressEvent(self, event):
        if self._sketched:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self._sketched:
            newPos = self.mapToParent(event.pos() - self.offset)
            self.move(newPos)
            for wire, inOut, (x, y) in self._wires:
                if inOut:
                    wire.setLine(x + newPos.x(), y + newPos.y())
                else:
                    wire.setStart(x + newPos.x(), y + newPos.y())

    def mouseReleaseEvent(self, event):
        self.offset = QPoint()

    def sizeHint(self):
        return QSize(80, self.h)


class BasicGate(Gate):
    def __init__(self, inputs=2, outputs=1, parent=None):
        super(BasicGate, self).__init__(inputs, outputs, parent)
        self.removeWire = RemoveWireButton(self)
        self.removeWire.clicked.connect(self._removeWire)
        self.removeWire.move(20, -2)
        self.addWire = AddWireButton(self)
        self.addWire.clicked.connect(self._addWire)
        self.addWire.move(20, self.h - 16)

    def _addWire(self):
        self._inputs += 1
        while self._buttons:
            button = self._buttons.pop()
            button.deleteLater()
        self._drawWires()
        self._drawButtons()
        self._drawPath()
        self.update()

    def _removeWire(self):
        if self._inputs > 2:
            self._inputs -= 1
            while self._buttons:
                button = self._buttons.pop()
                button.deleteLater()
            self._drawWires()
            self._drawButtons()
            self._drawPath()
            self.update()


class InputGate(Gate):
    def __init__(self, outputs=1, parent=None):
        super(InputGate, self).__init__(0, outputs, parent)


class OutputGate(Gate):
    def __init__(self, inputs=1, parent=None):
        super(OutputGate, self).__init__(inputs, 0, parent)
