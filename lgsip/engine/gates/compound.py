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

from lgsip.engine.gates.gate import BasicGate


class Nand(BasicGate):
    def __init__(self, inputs):
        super(Nand, self).__init__(inputs, "Nand")

    def compute(self):
        return not all(x for x in self._inputs)


class Nor(BasicGate):
    def __init__(self, inputs):
        super(Nor, self).__init__(inputs, "Nor")

    def compute(self):
        return not any(x for x in self._inputs)


class Xor(BasicGate):
    def __init__(self):
        super(Xor, self).__init__(2, "Xor")

    def compute(self):
        return self._inputs[0] ^ self._inputs[1]


class Xnor(BasicGate):
    def __init__(self):
        super(Xnor, self).__init__(2, "Xnor")

    def compute(self):
        return not self._inputs[0] ^ self._inputs[1]
