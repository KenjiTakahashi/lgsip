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
from PyQt4.QtCore import Qt, QRectF
from lgsip.frontend.gates.gate import DeleteGateButton


class Wire(QtGui.QGraphicsObject):
    def __init__(self, parent=None):
        super(Wire, self).__init__(parent)
        self.setZValue(-1)
        self.setFlag(self.ItemIsSelectable, True)
        self.x, self.y, self.nx, self.ny = 0, 0, 0, 0
        self.propagating = True

    def setStart(self, x, y):
        self.x, self.y = x, y

    def setEnd(self, x, y):
        self.nx, self.ny = x, y

    def boundingRect(self):
        return QRectF(self.x, self.y, self.x + self.nx, self.y + self.ny)

    def paint(self, painter, option, widget):
        pen = QtGui.QPen()
        pen.setWidth(4)
        pen.setColor(QtGui.QColor(QtGui.QPalette().mid()))
        painter.setPen(pen)
        dx = (self.nx - self.x) / 2
        dy = (self.ny - self.y) / 2
        self.path = QtGui.QPainterPath()
        self.shape = QtGui.QPainterPath()
        self.path.moveTo(self.x, self.y)
        if dx and dy:
            dx += self.x
            self.path.lineTo(dx, self.y)
            self.shape.addRect(self.x, self.y - 2, dx - self.x, 4)
            self.path.moveTo(dx, self.y)
            self.path.lineTo(dx, self.ny)
            self.shape.addRect(dx - 2, self.y - 2, 4, self.ny - self.y)
            self.path.moveTo(dx, self.ny)
        self.path.lineTo(self.nx, self.ny)
        self.shape.addRect(dx - 2, self.ny - 2, self.nx - dx, 4)
        painter.drawPath(self.path)
        if self.propagating:
            pen.setDashPattern([3, 4])
            pen.setColor(Qt.red)
            painter.setPen(pen)
            painter.drawPath(self.path)

    def shape(self):
        return self.shape

    def mousePressEvent(self, event):
        super(Wire, self).mousePressEvent(event)
        if event.button() == Qt.RightButton:
            self.deleteLater()

    def mouseMoveEvent(self, event):
        super(Wire, self).mouseMoveEvent(event)
        print(event.pos())


class _RubberBand(QtGui.QGraphicsObject):
    def __init__(self, parent=None):
        super(_RubberBand, self).__init__(parent)
        self.x, self.y, self.nx, self.ny = 0, 0, 0, 0
        self.setZValue(-2)
        self._delete = DeleteGateButton()
        self._delete.clicked.connect(self._deleteGates)
        proxy = QtGui.QGraphicsProxyWidget(self)
        proxy.setWidget(self._delete)

    def setStart(self, pos):
        self.x, self.y = pos.x(), pos.y()

    def setEnd(self, pos):
        self.nx, self.ny = pos.x(), pos.y()
        if self.ny < self.y:
            y = self.ny + 4
        else:
            y = self.ny - 20
        if self.nx < self.x:
            x = self.nx + 4
        else:
            x = self.nx - 20
        self._delete.move(x, y)

    def _deleteGates(self):
        scene = self.scene()
        for gate in scene.collidingItems(self):
            gate.deleteLater()
        scene.removeItem(self)

    def boundingRect(self):
        return QRectF(self.x, self.y, self.nx - self.x, self.ny - self.y)

    def paint(self, painter, option, widget):
        painter.setPen(Qt.NoPen)
        painter.setBrush(QtGui.QPalette().light())
        width, height = self.nx - self.x, self.ny - self.y
        painter.drawRect(self.x, self.y, width, height)


class _LgsipScene(QtGui.QGraphicsScene):
    def __init__(self, parent=None):
        super(_LgsipScene, self).__init__(parent)
        self._wire = None
        self._direction = None
        self._sender = None
        self._rubber = _RubberBand()
        self._rubber_ = False

    def dropEvent(self, event):
        data = event.mimeData()
        module = bytes(data.data('lgsip/x-modulename').data()).decode('utf-8')
        cls = bytes(data.data('lgsip/x-classname').data()).decode('utf-8')
        gate = getattr(__import__(module, globals(), locals(), cls), cls)()
        gate.setSketched(True)
        gate.wiring.connect(self.wire)
        proxy = self.addWidget(gate)
        proxy.setPos(event.scenePos())

    def wire(self, realSender, direction):
        if self._wire and self._direction != direction:
            realSender.addEndWire(self._wire, self.sender().pos())
            self._wire = None
            self._sender = None
        elif not self._wire:
            self._sender = realSender
            self._wire = Wire()
            self._sender.addStartWire(self._wire, self.sender().pos())
            self.addItem(self._wire)

    def mousePressEvent(self, event):
        button = event.button()
        if button == Qt.RightButton:
            if self._wire:
                self.removeItem(self._wire)
                self._sender.cancelWire(self._wire)
                self._wire = None
                self._sender = None
            elif self._rubber:
                self.removeItem(self._rubber)
        elif button == Qt.LeftButton:
            if not self._rubber_ and not self.itemAt(event.scenePos()):
                self.removeItem(self._rubber)
                self._rubber_ = True
                self._rubber.setStart(event.scenePos())
                self._rubber.setEnd(event.scenePos())
                self.addItem(self._rubber)
            elif self._rubber_:
                self._rubber_ = False
        super(_LgsipScene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._wire:
            pos = event.scenePos()
            self._wire.setEnd(pos.x(), pos.y())
        elif self._rubber_:
            self._rubber.setEnd(event.scenePos())
        self.update()
        super(_LgsipScene, self).mouseMoveEvent(event)


class SketchBoard(QtGui.QGraphicsView):
    def __init__(self, parent=None):
        super(SketchBoard, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        # Hope it will be fast enough or maybe we'll
        # find a better way later on.
        self.setViewportUpdateMode(self.FullViewportUpdate)
        self.setMouseTracking(True)
        self.setScene(_LgsipScene())

    def dragEnterEvent(self, event):
        data = event.mimeData()
        if(data.hasFormat('lgsip/x-classname')
        and data.hasFormat('lgsip/x-modulename')):
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        self.dragEnterEvent(event)
