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


class DisintegrateGateButton(_LgsipGateButton):
    def __init__(self, parent=None):
        super(DisintegrateGateButton, self).__init__(parent)
        self.path.addPolygon(QtGui.QPolygonF([
            QPointF(7, 3), QPointF(3, 8), QPointF(7, 13)
        ]))
        self.path.addPolygon(QtGui.QPolygonF([
            QPointF(9, 3), QPointF(13, 8), QPointF(9, 13)
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
        self.propagating = False

    def addStartWire(self, wire, gate=None):
        self._swires.append(wire)
        if gate:
            self.parent().connect(self, wire._endParent, gate, False)

    def addEndWire(self, wire, gate=None):
        """Adds a wire that ends in this input/output.

        Args:
            wire: a reference to the wire
            gate: source gate (where the wire has started)
        """
        self._ewires.append(wire)
        if gate:
            self.parent().connect(wire._startParent, self, gate, True)

    def cancelWire(self, wire):
        self._swires.remove(wire)

    def setPropagating(self, value):
        self.propagating = value
        if value:
            self.color = Qt.red
        else:
            self.color = QtGui.QPalette().mid()
        for wire in self._ewires:
            wire.setPropagating(value)
        self.update()

    def deleteWires(self):
        for wire in self._swires:
            wire._startParent.parent().disconnect(
                wire._startParent, wire._endParent
            )
            wire.deleteLater()
        self.deleteEWires()

    def deleteEWires(self):
        for wire in self._ewires:
            wire._startParent.parent().disconnect(
                wire._startParent, wire._endParent
            )
            wire.deleteLater()


class InWireButton(WireButton):
    def addStartWire(self, wire, pos, gate=None):
        super(InWireButton, self).addStartWire(wire, gate)
        pos += self.pos()
        wire.setStart(pos.x(), pos.y() + 2)

    def addEndWire(self, wire, pos, gate=None):
        super(InWireButton, self).addEndWire(wire, gate)
        pos += self.pos()
        wire.setEnd(pos.x(), pos.y() + 2)

    def moveWires(self, offset):
        pos = offset + self.pos()
        for wire in self._swires:
            wire.setStart(pos.x(), pos.y() + 2)
        for wire in self._ewires:
            wire.setEnd(pos.x(), pos.y() + 2)


class OutWireButton(WireButton):
    def addStartWire(self, wire, pos, gate=None):
        super(OutWireButton, self).addStartWire(wire, gate)
        pos += self.pos()
        wire.setStart(pos.x() + self.width(), pos.y() + 2)

    def addEndWire(self, wire, pos, gate=None):
        super(OutWireButton, self).addEndWire(wire, gate)
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

    def __init__(self, inputs=1, outputs=1, parent=None, integrated=False):
        super(Gate, self).__init__(parent)
        self._integrated = integrated
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

    def calculateHeight(self):
        """Returns gate height, calculated basing on the number of
        inputs/outputs.

        Specific gate implementation could reimplement this method
        to provide a different calculation algorithm.
        It should return a valid height, i.e. an integer greater than 0.
        """
        if self._inputs:
            h = 24 + 24 * (self._inputs - 1)
        elif self._outputs:
            h = 24 + 24 * (self._outputs - 1)
        else:  # this should never happen
            h = 40
        return h

    def _drawWires(self):
        self.h = self.calculateHeight()
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
            self.delete.clicked.connect(self.deleteLater)
        if self._integrated:
            self.delete.move(20, delta - 16)
            if not hasattr(self, "desintegrate"):
                self.disintegrate = DisintegrateGateButton(self)
            self.disintegrate.move(20, delta - 4)
            self.disintegrate.show()
        else:
            self.delete.move(20, delta - 8)
        self.delete.show()

    def _drawPath(self):
        self.path = QtGui.QPainterPath()

    def _wiringIn(self):
        self.wiring.emit(self.sender(), 0)

    def _wiringOut(self):
        self.wiring.emit(self.sender(), 1)

    def deleteLater(self):
        for button in self._inbuttons:
            button.deleteWires()
        for button in self._outbuttons:
            button.deleteWires()
        super(Gate, self).deleteLater()

    def setInPropagating(self, i, value):
        self._inbuttons[i].setPropagating(value)

    def setOutPropagating(self, i, value):
        self._outbuttons[i].setPropagating(value)

    def connect(self, sender, wire, gate, flag):
        if flag:
            gate._gate.addWire(
                self._gate, self._inbuttons.index(wire),
                gate._outbuttons.index(sender)
            )
        else:
            self._gate.addWire(
                gate._gate, gate._inbuttons.index(wire),
                self._outbuttons.index(sender)
            )

    def disconnect(self, sender, wire):
        gate = wire.parent()
        self._gate.removeWire(
            gate._gate, gate._inbuttons.index(wire),
            self._outbuttons.index(sender)
        )

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
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
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
        if self._wireButtons():
            self.removeWire = RemoveWireButton(self)
            self.removeWire.clicked.connect(self._removeWire)
            self.removeWire.move(20, -2)
            self._drawWireButtons()
        self._doGate(inputs)

    def _doGate(self, inputs):
        raise NotImplementedError

    def _wireButtons(self):
        raise NotImplementedError

    def _drawWireButtons(self):
        if not hasattr(self, "addWire"):
            self.addWire = AddWireButton(self)
        self.addWire.clicked.connect(self._addWire)
        self.addWire.move(20, self.h - 16)

    def _addWire(self):
        self._inputs += 1
        self._gate.addInput()
        self._drawWires()
        self._drawButtons()
        self._drawPath()
        self._drawWireButtons()
        self.moveWires()
        self.update()

    def _removeWire(self):
        if self._inputs > 2:
            self._inputs -= 1
            self._gate.removeInput()
            self._inbuttons.pop().deleteEWires()
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


import os
import imp
from lgsip.engine.ic import IC


class ComplexGate(Gate):
    def __init__(self, name, pixmap=False, parent=None):
        if not os.path.isfile(name):
            raise Exception
        self._intname = name
        module = imp.load_source("complex_gate", name)
        (name, inputs, outputs, gates) = module.load()
        self.name = name
        super(ComplexGate, self).__init__(inputs, outputs, parent, True)
        self._gate = IC(*gates)
        self._gate.inValueChanged.connect(self.setInPropagating)
        self._gate.outValueChanged.connect(self.setOutPropagating)
        if not pixmap:
            for i, conn in enumerate(self._gate._outputs):
                for conn_, _ in conn:
                    if conn_.compute():
                        self.setOutPropagating(i, True)

    def _drawPath(self):
        super(ComplexGate, self)._drawPath()
        self.path.addRect(20, 0, 40, self.h)

    def paintEvent(self, event):
        super(ComplexGate, self).paintEvent(event)
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen(QtGui.QPalette().dark())
        painter.setPen(pen)
        painter.drawText(36, 30, 30, 20, 0, self.name)
