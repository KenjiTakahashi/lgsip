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

from lgsip.frontend.gates.gate import BasicGate
from lgsip.engine.gates import basic
from PyQt4 import QtGui
from PyQt4.QtCore import QPointF


class And(BasicGate):
    def __init__(self, inputs=2, parent=None):
        super(And, self).__init__(inputs, 1, parent)
        self._gate.inValueChanged.connect(self.setInPropagating)
        self._gate.outValueChanged.connect(self.setOutPropagating)

    def _doGate(self, inputs):
        self._gate = basic.And(inputs)

    def _drawPath(self):
        super(And, self)._drawPath()
        self.path.moveTo(40, self.h / 2)
        self.path.arcTo(20, 0, 40, self.h, -90, 180)
        self.path.addRect(20, 0, 20, self.h)


class Or(BasicGate):
    def __init__(self, inputs=2, parent=None):
        super(Or, self). __init__(inputs, 1, parent)
        self._gate.inValueChanged.connect(self.setInPropagating)
        self._gate.outValueChanged.connect(self.setOutPropagating)

    def _doGate(self, inputs):
        self._gate = basic.Or(inputs)

    def _drawPath(self):
        super(Or, self)._drawPath()
        self.path.moveTo(15, 0)
        self.path.quadTo(QPointF(25, self.h / 2), QPointF(15, self.h))
        self.path.quadTo(QPointF(45, self.h + 2), QPointF(60, self.h / 2 + 2))
        self.path.lineTo(60, self.h / 2 - 2)
        self.path.quadTo(QPointF(45, -2), QPointF(15, 0))


class Not(BasicGate):
    def __init__(self, parent=None):
        super(Not, self). __init__(1, 1, parent)
        self._gate.inValueChanged.connect(self.setInPropagating)
        self._gate.outValueChanged.connect(self.setOutPropagating)

    def _doGate(self, _):
        self._gate = basic.Not()

    def _drawPath(self):
        super(Not, self)._drawPath()
        self.path.addPolygon(QtGui.QPolygonF([
            QPointF(20, 0), QPointF(60, self.h / 2 - 2),
            QPointF(60, self.h / 2 + 2), QPointF(20, self.h)
        ]))
        self.path.addEllipse(60, self.h / 2 - 5, 10, 10)
