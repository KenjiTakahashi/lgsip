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
from PyQt4.QtCore import Qt
from lgsip.frontend.gates.wire import Wire


class _LgsipScene(QtGui.QGraphicsScene):
    def __init__(self, parent=None):
        super(_LgsipScene, self).__init__(parent)
        self._wire = None
        self._direction = None

    def dropEvent(self, event):
        data = event.mimeData()
        module = bytes(data.data('lgsip/x-modulename').data()).decode('utf-8')
        cls = bytes(data.data('lgsip/x-classname').data()).decode('utf-8')
        gate = getattr(__import__(module, globals(), locals(), cls), cls)()
        gate.setSketched(True)
        gate.wiring.connect(self.wire)
        proxy = self.addWidget(gate)
        proxy.setPos(event.scenePos())

    def wire(self, x, y, direction):
        if self._wire and self._direction != direction:
            pos = self.sender().pos()
            self._wire.setLine(pos.x() + x, pos.y() + y)
            self._wire = None
        elif not self._wire:
            self._direction = direction
            pos = self.sender().pos()
            self._wire = Wire(pos.x() + x, pos.y() + y)
            self.addItem(self._wire)

    def mousePressEvent(self, event):
        if self._wire and event.button() == Qt.RightButton:
            self.removeItem(self._wire)
            self._wire = None
        else:
            super(_LgsipScene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._wire:
            pos = event.scenePos()
            self._wire.setLine(pos.x(), pos.y())
            self.update()


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
