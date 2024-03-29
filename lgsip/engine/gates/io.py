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

from lgsip.engine.gates.gate import IOGate
from PyQt4.QtCore import QTimer


class BinaryInput(IOGate):
    def __init__(self, value=False):
        super(BinaryInput, self).__init__()
        self._inputs.append(value)

    def switch(self):
        self._inputs[0] = not self._inputs[0]

    def compute(self):
        return self._inputs[0]


class BinaryOutput(IOGate):
    def __init__(self):
        super(BinaryOutput, self).__init__()
        self._inputs.append(False)

    def compute(self):
        return self._inputs[0]


class Clock(IOGate):
    def __init__(self, timeout=1000):
        super(Clock, self).__init__()
        self._inputs.append(False)
        self._timer = QTimer()
        self._timer.setInterval(timeout)
        self._timer.timeout.connect(self._timeout)
        self._timer.start()
        self.start()

    def _timeout(self):
        self._inputs[0] = not self._inputs[0]

    def setTimeout(self, timeout):
        self._timer.setInterval(timeout)

    def slower(self):
        self._timer.setInterval(self.interval() + 20)

    def faster(self):
        self._timer.setInterval(self.interval() - 20)

    def compute(self):
        return self._inputs[0]
