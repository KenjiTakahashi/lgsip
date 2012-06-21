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

from lgsip.engine.gates.io import BinaryInput, BinaryOutput
from collections import OrderedDict
from PyQt4.QtCore import QObject, pyqtSignal


class IC(QObject):
    inValueChanged = pyqtSignal(int, bool)
    outValueChanged = pyqtSignal(int, bool)

    def __init__(self, *gates):
        super(IC, self).__init__()
        self._inputs_ = OrderedDict()
        self._outputs_ = OrderedDict()
        self._gates = list()
        for gate in gates:
            if isinstance(gate, BinaryInput):
                conn = gate.connections()
                self._inputs_.setdefault(gate, list()).extend(conn)
                for g, i in conn:
                    g.changeInput(i, False)
            elif isinstance(gate, BinaryOutput):
                self._outputs_.setdefault(gate, list())
            else:
                for gate_, num in gate.connections():
                    if isinstance(gate_, BinaryOutput):
                        self._outputs_.setdefault(
                            gate_, list()
                        ).append((gate, 0))
                        gate.removeWire(gate_, num)
                    self._gates.append(gate)
        self._inputs = list()
        self._outputs = list()
        for gate, conn in self._inputs_.items():
            self._inputs.append(conn)
            for conn_, _ in conn:
                conn_.inValueChanged.connect(self._inValueChanged)
            gate.die()
            gate.wait()
        for gate, conn in self._outputs_.items():
            self._outputs.append(conn)
            for conn_, _ in conn:
                conn_.outValueChanged.connect(self._outValueChanged)
            gate.die()
            gate.wait()

    def _inValueChanged(self, i, value):
        index = -1
        for _i, _input in enumerate(self._inputs):
            if (self.sender(), i) in _input:
                index = _i
                break
        if index != -1:
            self.inValueChanged.emit(index, value)

    def _outValueChanged(self, _, value):
        index = -1
        for _i, _output in enumerate(self._outputs):
            if (self.sender(), 0) in _output:
                index = _i
                break
        if index != -1:
            self.outValueChanged.emit(index, value)

    def addWire(self, gate, output, input):
        for _output in self._outputs[output]:
            _output.addWire(gate, input)

    def wire(self, index):
        return self._inputs[index]

    def die(self):
        for gate in self._gates:
            gate.die()

    def wait(self):
        for gate in self._gates:
            gate.wait()
