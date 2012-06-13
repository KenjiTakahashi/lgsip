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

from lgsip.frontend.gates.gate import InputGate, OutputGate
from PyQt4 import QtGui
from PyQt4.QtCore import Qt, pyqtSignal


class _SwitchButton(QtGui.QPushButton):
    def __init__(self, parent=None):
        super(_SwitchButton, self).__init__(parent)
        self.setCheckable(True)
        self.setFixedSize(18, 18)
        self.move(38, 3)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        if self.isChecked():
            painter.setBrush(QtGui.QBrush(QtGui.QColor(160, 0, 0)))
        else:
            painter.setBrush(QtGui.QPalette().light())
        painter.drawRect(0, 0, self.width(), self.height())


class BinaryInput(InputGate):
    switched = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(BinaryInput, self).__init__(parent=parent)
        self.path.addRect(20, 0, 40, self.h)
        self._switch = _SwitchButton(self)
        self._switch.clicked.connect(self._switched)

    def _switched(self):
        self.switched.emit(self._switch.isChecked())


class BinaryOutput(OutputGate):
    def __init__(self, parent=None):
        super(BinaryOutput, self).__init__(parent=parent)
        self.path.addRect(20, 0, 40, self.h)
        self._switch = _SwitchButton(self)
        self._switch.setEnabled(False)

    def switch(self, value=None):
        if not value:
            value = not self._switch.isChecked()
        self._switch.setChecked(value)


class Clock(InputGate):
    def __init__(self, parent=None):
        super(Clock, self).__init__(parent=parent)
        self.path.addRect(20, 0, 40, self.h)
        self.time = QtGui.QLineEdit(self)
        self.time.setFixedSize(18, 18)
        self.time.move(38, 3)
