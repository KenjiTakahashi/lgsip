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
    def __init__(self):
        super(_Gate, self).__init__()
        self._inputs = list()
        self._gates = list()
        self._changed = False
        #self._output = False
        self._running = True
        self.start()

    def run(self):
        while self._running:
            self.msleep(1)
            #if self._changed:
            for (gate, index) in self._gates:
                gate.changeInput(index, self.compute())
                #_newOutput = self.compute()
                #if _newOutput != self._output:
                    #self._output = _newOutput
                    #for (gate, index) in self._gates:
                        #gate.changeInput(index, self._output)

    def die(self):
        self._running = False

    def addWire(self, gate):
        self._gates.append(gate)

    def changeInput(self, index, value):
        try:
            #self._inputs[index] = value
            if self._inputs[index] != value:
                self._inputs[index] = value
                self._changed = True
        except IndexError:
            print(1)
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
    valueChanged = pyqtSignal(list)