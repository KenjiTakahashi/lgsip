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

from lgsip.engine import lgsiperr, ic
from PyQt4.QtCore import QThread, pyqtSignal
import imp


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
            if value != self._value:
                self.outValueChanged.emit(value)
                self._value = value
            for (gate, index) in self._gates:
                try:
                    gate.changeInput(index, value)
                except lgsiperr.InvalidInputIndexError:
                    self._gates.remove((gate, index))

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
            gate.changeInput(index, False)
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
        self._extendable = True

    def addInput(self):
        if self._extendable:
            self._inputs.append(False)

    def removeInput(self):
        """Completely removes an input from the gate.

        All connections to this input stay until an update is called,
        they are then wiped.

        You cannot remove input from a gate which is non-extendable or
        if there are only 2 inputs (it makes no sense anyway).
        """
        if self._extendable and len(self._inputs) > 2:
            self._inputs.pop()


class IOGate(_Gate):
    pass


class ComplexGate(ic.IC):
    def __init__(self, name, parent=None):
        module = imp.load_source("complex_gate", name)
        module.load(self)
