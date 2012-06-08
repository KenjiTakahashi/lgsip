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
        self._swires = list()
        self._ewires = list()

    def addStartWire(self, wire):
        self._swires.append(wire)

    def addEndWire(self, wire):
        self._ewires.append(wire)

    def cancelWire(self, wire):
        self._swires.remove(wire)

    def deleteWires(self):
        for wire in self._swires:
            wire.deleteLater()
        for wire in self._ewires:
            wire.deleteLater()


class InWireButton(WireButton):
    def addStartWire(self, wire, pos):
        super(InWireButton, self).addStartWire(wire)
        pos += self.pos()
        wire.setStart(pos.x(), pos.y() + 2)

    def addEndWire(self, wire, pos):
        super(InWireButton, self).addEndWire(wire)
        pos += self.pos()
        wire.setEnd(pos.x(), pos.y() + 2)

    def moveWires(self, offset):
        pos = offset + self.pos()
        for wire in self._swires:
            wire.setStart(pos.x(), pos.y() + 2)
        for wire in self._ewires:
            wire.setEnd(pos.x(), pos.y() + 2)


class OutWireButton(WireButton):
    def addStartWire(self, wire, pos):
        super(OutWireButton, self).addStartWire(wire)
        pos += self.pos()
        wire.setStart(pos.x() + self.width(), pos.y() + 2)

    def addEndWire(self, wire, pos):
        super(OutWireButton, self).addEndWire(wire)
        pos += self.pos()
        wire.setEnd(pos.x() + self.width(), pos.y() + 2)

    def moveWires(self, offset):
        pos = offset + self.pos()
        for wire in self._swires:
            wire.setStart(pos.x() + self.width(), pos.y() + 2)
        for wire in self._ewires:
            wire.setEnd(pos.x() + self.width(), pos.y() + 2)


class Gate(QtGui.QWidget):
    wiring = pyqtSignal(object, int)

    def __init__(self, inputs=1, outputs=1, parent=None):
        super(Gate, self).__init__(parent)
        self._sketched = False
        self._integrated = False
        self._wires = list()
        self._wires2 = dict()
        self.setStyleSheet('background-color: transparent;')
        self.setFixedWidth(80)
        self.offset = QPoint()
        self._inbuttons = list()
        self._outbuttons = list()
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
        self.setFixedHeight(self.h)
        delta = self.h / (self._inputs + 1)
        for i in range(1, self._inputs + 1):
            try:
                button = self._inbuttons[i - 1]
            except IndexError:
                button = InWireButton(self)
                button.clicked.connect(self._wiringIn)
                self._inbuttons.append(button)
            button.move(0, delta * i - 2)
            button.show()
        delta = self.h / (self._outputs + 1)
        for i in range(1, self._outputs + 1):
            try:
                button = self._outbuttons[i - 1]
            except IndexError:
                button = OutWireButton(self)
                button.clicked.connect(self._wiringOut)
                self._outbuttons.append(button)
            button.move(60, delta * i - 2)
            button.show()

    def _drawButtons(self):
        delta = self.h / 2
        if not hasattr(self, "delete"):
            self.delete = DeleteGateButton(self)
            self.delete.clicked.connect(self._delete)
        if self._integrated:
            self.delete.move(20, delta - 16)
            if not hasattr(self, "desintegrate"):
                self.desintegrate = DesintegrateGateButton(self)
            self.desintegrate.move(20, delta - 4)
            self._buttons.add(self.desintegrate)
            self.desintegrate.show()
        else:
            self.delete.move(20, delta - 8)
        self.delete.show()

    def _drawPath(self):
        self.path = QtGui.QPainterPath()

    def _wiringIn(self):
        self.wiring.emit(self.sender(), 0)

    def _wiringOut(self):
        self.wiring.emit(self.sender(), 1)

    def _delete(self):
        for button in self._inbuttons:
            button.deleteWires()
        for button in self._outbuttons:
            button.deleteWires()
        self.deleteLater()

    def setSketched(self, val):
        self._sketched = val

    def moveWires(self, pos=None):
        if not pos:
            pos = self.pos()
        for button in self._inbuttons:
            button.moveWires(pos)
        for button in self._outbuttons:
            button.moveWires(pos)

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
            self.moveWires(newPos)

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
        self._drawWireButtons()

    def _drawWireButtons(self):
        if not hasattr(self, "addWire"):
            self.addWire = AddWireButton(self)
        self.addWire.clicked.connect(self._addWire)
        self.addWire.move(20, self.h - 16)

    def _addWire(self):
        self._inputs += 1
        self._drawWires()
        self._drawButtons()
        self._drawPath()
        self._drawWireButtons()
        self.moveWires()
        self.update()

    def _removeWire(self):
        if self._inputs > 2:
            self._inputs -= 1
            self._drawWires()
            self._drawButtons()
            self._drawPath()
            self._drawWireButtons()
            self.moveWires()
            self.update()


class InputGate(Gate):
    def __init__(self, outputs=1, parent=None):
        super(InputGate, self).__init__(0, outputs, parent)


class OutputGate(Gate):
    def __init__(self, inputs=1, parent=None):
        super(OutputGate, self).__init__(inputs, 0, parent)
