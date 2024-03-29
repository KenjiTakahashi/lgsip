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
from PyQt4.QtCore import Qt, QPointF, QSize, pyqtSignal
from lgsip.frontend.sketchboard import SketchBoard


class _LgsipPushButton(QtGui.QPushButton):
    def __init__(self, parent=None):
        super(_LgsipPushButton, self).__init__(parent)
        self.path = QtGui.QPainterPath()
        self.path.setFillRule(Qt.WindingFill)

    def paintEvent(self, event):
        super(_LgsipPushButton, self).paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QtGui.QPalette().mid())
        painter.drawPath(self.path)

    def sizeHint(self):
        return QSize(24, 24)


class PlayPausePushButton(_LgsipPushButton):
    bclicked = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(PlayPausePushButton, self).__init__(parent)
        self.playPath = QtGui.QPainterPath()
        self.playPath.addPolygon(QtGui.QPolygonF(
            [QPointF(7, 7), QPointF(7, 17), QPointF(17, 12)])
        )
        self.pausePath = QtGui.QPainterPath()
        self.pausePath.addRoundedRect(7, 7, 4, 10, 60, 20, Qt.RelativeSize)
        self.pausePath.addRoundedRect(13, 7, 4, 10, 60, 20, Qt.RelativeSize)
        self.path = self.pausePath
        self.clicked.connect(self._clicked)

    def _clicked(self):
        value = self.path == self.playPath
        if value:
            self.path = self.pausePath
        else:
            self.path = self.playPath
        self.update()
        self.bclicked.emit(value)


class AddPushButton(_LgsipPushButton):
    def __init__(self, parent=None):
        super(AddPushButton, self).__init__(parent)
        self.path.addRoundedRect(9, 14, 16, 6, 20, 60, Qt.RelativeSize)
        self.path.addRoundedRect(14, 9, 6, 16, 60, 20, Qt.RelativeSize)

    def sizeHint(self):
        return QSize(34, 34)


class ClosePushButton(_LgsipPushButton):
    def __init__(self, parent=None):
        super(ClosePushButton, self).__init__(parent)
        self.path.addRoundedRect(7, 10, 10, 4, 20, 60, Qt.RelativeSize)
        self.path.addRoundedRect(10, 7, 4, 10, 60, 20, Qt.RelativeSize)

    def paintEvent(self, event):
        super(_LgsipPushButton, self).paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QtGui.QPalette().mid())
        transform = QtGui.QTransform()
        transform.translate(12, -5)
        transform.rotate(45)
        painter.setTransform(transform)
        painter.drawPath(self.path)


class SavePushButton(_LgsipPushButton):
    def __init__(self, parent=None):
        super(SavePushButton, self).__init__(parent)
        self.path.addPolygon(QtGui.QPolygonF([
            QPointF(12, 17), QPointF(7, 12), QPointF(10, 12), QPointF(10, 7),
            QPointF(14, 7), QPointF(14, 12), QPointF(17, 12)
        ]))


class LoadPushButton(_LgsipPushButton):
    def __init__(self, parent=None):
        super(LoadPushButton, self).__init__(parent)
        self.path.addPolygon(QtGui.QPolygonF([
            QPointF(12, 7), QPointF(17, 12), QPointF(14, 12),
            QPointF(14, 17), QPointF(10, 17), QPointF(10, 12), QPointF(7, 12)
        ]))


class _LgsipTabBarButtons(QtGui.QWidget):
    closeClicked = pyqtSignal(QtGui.QWidget)

    def __init__(self, widget, parent=None):
        super(_LgsipTabBarButtons, self).__init__(parent)
        self.widget = widget
        self.start = PlayPausePushButton()
        self.close = ClosePushButton()
        self.close.clicked.connect(self._closeClicked)
        self.save = SavePushButton()
        self.load = LoadPushButton()
        layout = QtGui.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.load)
        layout.addWidget(self.save)
        layout.addWidget(self.start)
        layout.addWidget(self.close)
        self.setLayout(layout)

    def _closeClicked(self):
        self.closeClicked.emit(self.widget)


class LgsipTabWidget(QtGui.QTabWidget):
    _number = 1

    def __init__(self, parent=None):
        super(LgsipTabWidget, self).__init__(parent)
        add = AddPushButton()
        add.clicked.connect(self.addTab)
        self.setCornerWidget(add, Qt.TopLeftCorner)

    def addTab(self, *name):
        if len(name) > 0 and type(name[0]) == str:
            name = name[0]
        else:
            name = "Circuit " + str(self._number)
            self._number += 1
        widget = SketchBoard()
        index = super(LgsipTabWidget, self).addTab(widget, name)
        buttons = _LgsipTabBarButtons(widget)
        buttons.closeClicked.connect(self.removeTab)
        buttons.load.clicked.connect(widget.load)
        buttons.save.clicked.connect(widget.save)
        buttons.start.bclicked.connect(widget.pause)
        self.tabBar().setTabButton(index, QtGui.QTabBar.RightSide, buttons)
        self.setCurrentIndex(index)

    def removeTab(self, widget):
        if self.count() > 1:
            super(LgsipTabWidget, self).removeTab(self.indexOf(widget))
