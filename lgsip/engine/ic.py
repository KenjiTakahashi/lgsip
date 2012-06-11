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


class IC(object):
    def __init__(self, *gates):
        self._inputs = dict()
        self._outputs = dict()
        self._gates = list()
        for gate in gates:
            if isinstance(gate, BinaryInput):
                self._inputs.setdefault(
                    gate, list()
                ).extend(gate.connections())
                # gate.deleteLater()
            elif isinstance(gate, BinaryOutput):
                self._outputs.setdefault(gate, list())
            else:
                for gate_, num in gate.connections():
                    if isinstance(gate_, BinaryOutput):
                        self._outputs.setdefault(
                            gate_, list()
                        ).append((gate, 0))
                        gate.removeWire(gate_, num)
                    else:
                        self._gates.append(gate)
        print(self._inputs, 0, self._gates, 1, self._outputs)

    def addWire(self, output, gate, input):
        self._outputs[output].addWire(gate, input)

    def wire(self, index):
        return self._inputs[index]
