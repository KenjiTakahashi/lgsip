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
from PyQt4.QtCore import Qt, QSize, QPointF, QMimeData, QPoint, pyqtSignal


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


class Gate(QtGui.QWidget):
    wiring = pyqtSignal()

    def __init__(self, inputs=1, outputs=1, parent=None):
        super(Gate, self).__init__(parent)
        self._sketched = False
        self.offset = QPoint()
        self.path = QtGui.QPainterPath()
        self.h = 24 + 24 * (inputs - 1)
        delta = self.h / (inputs + 1)
        for i in range(1, inputs + 1):
            location = delta * i - 2
            self.path.addRect(0, location, 10, 4)
            button = QtGui.QPushButton(self)  # roll our own here
            button.setFixedSize(16, 16)
            button.move(0, location - 6)
            button.clicked.connect(self.wiring)
        delta = self.h / (outputs + 1)
        for i in range(1, outputs + 1):
            location = delta * i - 2
            self.path.addRect(50, location, 10, 4)
            button = QtGui.QPushButton(self)  # roll our own here, too
            button.setFixedSize(16, 16)
            button.move(50, location - 6)
            button.clicked.connect(self.wiring)
        self.setFixedWidth(60)

    def setSketched(self, val):
        self._sketched = val

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
        else:
            drag = QtGui.QDrag(self)
            data = QMimeData()
            data.setData('lgsip/x-classname', type(self).__name__)
            data.setData('lgsip/x-modulename', type(self).__module__)
            drag.setMimeData(data)
            pixmap = QtGui.QPixmap(self.size())
            pixmap.fill(Qt.transparent)
            self.render(pixmap, flags=QtGui.QWidget.DrawChildren)
            drag.setPixmap(pixmap)
            drag.exec_()

    def mouseMoveEvent(self, event):
        if self._sketched:
            self.move(self.mapToParent(event.pos() - self.offset))

    def mouseReleaseEvent(self, event):
        self.offset = QPoint()

    def sizeHint(self):
        return QSize(60, self.h)


class BasicGate(Gate):
    def __init__(self, inputs=1, outputs=1, parent=None):
        super(BasicGate, self).__init__(inputs, outputs, parent)
        self.removeWire = RemoveWireButton(self)
        self.removeWire.move(10, -2)
        delta = self.h / 2
        self.delete = DeleteGateButton(self)  # move it to Gate
        self.delete.move(10, delta - 16)
        self.desintegrate = DesintegrateGateButton(self)
        self.desintegrate.move(10, delta - 4)
        self.addWire = AddWireButton(self)
        self.addWire.move(10, self.h - 16)
