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

from tests.helpers import GateTest
from lgsip.engine.gates import io, basic, compound


class TestSimpleCircuit(GateTest):
    def _prepare(self, i1, i2, i3):
        self.i1 = io.BinaryInput(i1)
        self.i2 = io.BinaryInput(i2)
        self.i3 = io.BinaryInput(i3)
        self.a1 = basic.And(2)
        self.a2 = basic.And(2)
        self.o = basic.Or(2)
        self.n = basic.Not()
        self.i1.valueChanged.connect(self._increment)
        self.i2.valueChanged.connect(self._increment)
        self.i3.valueChanged.connect(self._increment)
        self.a1.valueChanged.connect(self._increment)
        self.a2.valueChanged.connect(self._increment)
        self.o.valueChanged.connect(self._increment)
        self.n.valueChanged.connect(self._increment)
        self.i1.addWire(self.a1, 0)
        self.i2.addWire(self.n, 0)
        self.n.addWire(self.a1, 1)
        self.i2.addWire(self.a2, 0)
        self.i3.addWire(self.a2, 1)
        self.a1.addWire(self.o, 0)
        self.a2.addWire(self.o, 1)

    def test_should_be_true_when_values_are_true_true_true(self):
        self._prepare(True, True, True)
        self._limit = [
            [self.n, self.a1, self.o, self.a2, self.a2],
            [self.n, self.a1, self.a1, self.a1, self.o,
            self.o, self.o, self.a2, self.a2]
        ]
        self._wait()
        assert self.o.compute() == True

    def test_should_be_true_when_values_are_false_true_true(self):
        self._prepare(False, True, True)
        self._limit = [
            [self.n, self.a2, self.a2, self.o],
            [self.a1, self.n, self.a1, self.a2, self.a2, self.o]
        ]
        self._wait()
        assert self.o.compute() == True

    def test_should_be_true_when_values_are_true_false_true(self):
        self._prepare(True, False, True)
        self._limit = [
            [self.a1, self.a1, self.a2, self.o]
        ]
        self._wait()
        assert self.o.compute() == True

    def test_should_be_false_when_values_are_false_false_true(self):
        self._prepare(False, False, True)
        self._limit = [
            [self.a1, self.a2]
        ]
        self._wait()
        assert self.o.compute() == False

    def test_should_be_false_when_values_are_true_true_false(self):
        self._prepare(True, True, False)
        self._limit = [
            [self.a1, self.n, self.a2],
            [self.a1, self.n, self.a1, self.o, self.a1, self.o, self.a2]
        ]
        self._wait()
        assert self.o.compute() == False

    def test_should_be_false_when_values_are_false_true_false(self):
        self._prepare(False, True, False)
        self._limit = [
            [self.n, self.a2],
            [self.a1, self.n, self.a1, self.a2]
        ]
        self._wait()
        assert self.o.compute() == False

    def test_should_be_true_when_values_are_true_false_false(self):
        self._prepare(True, False, False)
        self._limit = [
            [self.a1, self.a1, self.o]
        ]
        self._wait()
        assert self.o.compute() == True

    def test_should_be_false_when_values_are_false_false_false(self):
        self._prepare(False, False, False)
        self._limit = [
            [self.a1]
        ]
        self._wait()
        assert self.o.compute() == False

    def tearDown(self):
        self.i1.die()
        self.i2.die()
        self.i3.die()
        self.a1.die()
        self.a2.die()
        self.o.die()
        self.n.die()
        self.i1.wait()
        self.i2.wait()
        self.i3.wait()
        self.a1.wait()
        self.a2.wait()
        self.o.wait()
        self.n.wait()


class TestJKLatch(GateTest):
    def _prepare(self, i1, i2, i3):
        self.j = io.BinaryInput(i1)
        self.c = io.BinaryInput(i2)
        self.k = io.BinaryInput(i3)
        self.a1 = basic.And(3)
        self.a2 = basic.And(3)
        self.n1 = compound.Nor(2)
        self.n2 = compound.Nor(2)
        self.j.addWire(self.a1, 1)
        self.k.addWire(self.a2, 1)
        self.c.addWire(self.a1, 2)
        self.c.addWire(self.a2, 2)
        self.a1.addWire(self.n1, 0)
        self.a2.addWire(self.n2, 0)
        self.n1.addWire(self.a1, 0)
        self.n2.addWire(self.a2, 0)
        self.n1.addWire(self.n2, 1)
        self.n2.addWire(self.n1, 1)
        self.a1.valueChanged.connect(self._increment)
        self.a2.valueChanged.connect(self._increment)
        self.n1.valueChanged.connect(self._increment)
        self.n2.valueChanged.connect(self._increment)

    #def test_cyclic(self):
        #self._prepare(True, True, True)
        #begin = [self.a1, self.a1, self.a2, self.a2]
        #first_list = begin + [self.a1, self.n2]
        #second_list = begin + [self.a2, self.n1]
        #self._limit = [first_list, second_list]
        #self._wait()
        #first = self.n1.compute() == False and self.n2.compute() == True
        #second = self.n1.compute() == True and self.n2.compute() == False
        #assert first or second
        #first_list += [self.a1, self.n1]
        #second_list += [self.a2, self.n2]
        #self._limit = [first_list, second_list]
        #self._wait()
        #if first:
            #assert self.n1.compute() == True and self.n2.compute() == False
        #else:
            #assert self.n1.compute() == False and self.n2.compute() == True

    def tearDown(self):
        self.j.die()
        self.k.die()
        self.c.die()
        self.a1.die()
        self.a2.die()
        self.n1.die()
        self.n2.die()
        self.j.wait()
        self.k.wait()
        self.c.wait()
        self.a1.wait()
        self.a2.wait()
        self.n1.wait()
        self.n2.wait()


from lgsip.engine.ic import IC


class TestIC(GateTest):
    def _prepare(self, i1, i2, i3):
        self.i1 = io.BinaryInput(i1)
        self.i2 = io.BinaryInput(i2)
        self.i3 = io.BinaryInput(i3)
        self.a1 = basic.And(2)
        self.a2 = basic.And(2)
        self.o = basic.Or(2)
        self.n = basic.Not()
        self.i1.valueChanged.connect(self._increment)
        self.i2.valueChanged.connect(self._increment)
        self.i3.valueChanged.connect(self._increment)
        self.a1.valueChanged.connect(self._increment)
        self.a2.valueChanged.connect(self._increment)
        self.o.valueChanged.connect(self._increment)
        self.n.valueChanged.connect(self._increment)
        self.i1.addWire(self.a1, 0)
        self.i2.addWire(self.n, 0)
        self.n.addWire(self.a1, 1)
        self.i2.addWire(self.a2, 0)
        self.i3.addWire(self.a2, 1)
        self.a1.addWire(self.o, 0)
        self.a2.addWire(self.o, 1)

    def test_IC(self):
        self._prepare(False, False, False)
        self.out = io.BinaryOutput()
        self.o.addWire(self.out, 0)
        ic = IC(
            self.i1, self.i2, self.i3, self.a1, self.a2, self.o, self.n, self.o
        )
        assert False

    def tearDown(self):
        self.i1.die()
        self.i2.die()
        self.i3.die()
        self.a1.die()
        self.a2.die()
        self.o.die()
        self.n.die()
        self.out.die()
        self.i1.wait()
        self.i2.wait()
        self.i3.wait()
        self.a1.wait()
        self.a2.wait()
        self.o.wait()
        self.n.wait()
        self.out.wait()
