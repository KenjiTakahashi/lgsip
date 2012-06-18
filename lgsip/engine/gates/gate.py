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

from lgsip.engine import lgsiperr
from PyQt4.QtCore import QThread, pyqtSignal


class _Gate(QThread):
    inValueChanged = pyqtSignal(int, bool)
    outValueChanged = pyqtSignal(bool)

    def __init__(self):
        super(_Gate, self).__init__()
        self._inputs = list()
        self._gates = list()
        self._running = True
        self._value = False
        self.start()

    def run(self):
        while self._running:
            self.msleep(1)
            value = self.compute()
            if value != self._value:  # TODO: Test if we could for inside if
                self.outValueChanged.emit(value)
                self._value = value
            for (gate, index) in self._gates:
                gate.changeInput(index, value)

    def die(self):
        self._running = False

    def addWire(self, gate, index):
        try:
            self._gates.append((gate, index))
        except IndexError:
            raise lgsiperr.InvalidInputIndexError

    def removeWire(self, gate, index):
        try:
            self._gates.remove((gate, index))
        except IndexError:
            raise lgsiperr.InvalidInputIndexError

    def connections(self):
        return self._gates

    def changeInput(self, index, value):
        try:
            if self._inputs[index] != value:
                self._inputs[index] = value
                self.inValueChanged.emit(index, value)
        except IndexError:
            raise lgsiperr.InvalidInputIndexError

    def compute(self):
        raise NotImplementedError


class BasicGate(_Gate):
    def __init__(self, number, name):
        super(BasicGate, self).__init__()
        if name != "Not" and number < 2:
            raise lgsiperr.NotEnoughInputsError
        self._inputs += [False] * number


class IOGate(_Gate):
    pass
