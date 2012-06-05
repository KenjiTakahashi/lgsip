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

from lgsip.engine.gates import io, basic


class TestBinaryInput(object):
    def test_should_be_false_when_set_to_false(self):
        self.i = io.BinaryInput(False)
        assert self.i.compute() == False

    def test_should_be_true_when_switched_from_false(self):
        self.i = io.BinaryInput(False)
        self.i.switch()
        assert self.i.compute() == True

    def test_should_be_true_when_set_to_true(self):
        self.i = io.BinaryInput(True)
        assert self.i.compute() == True

    def test_should_be_false_when_switch_from_true(self):
        self.i = io.BinaryInput(True)
        self.i.switch()
        assert self.i.compute() == False

    def tearDown(self):
        self.i.die()
        self.i.wait()


from PyQt4.QtCore import QCoreApplication

import sys
app = QCoreApplication(sys.argv)


class TestAnd(object):
    def setUp(self):
        self._count = 0
        self.a = basic.And(2)
        self.a.valueChanged.connect(self._increment)

    def _increment(self, _, __):
        self._count += 1
        print(self._count)
        if self._count == self._limit:
            app.quit()

    def _wait(self):
        if self._limit > 0:
            app.exec_()

    def _prepare(self, i1, i2):
        self.i1 = io.BinaryInput(i1)
        self.i2 = io.BinaryInput(i2)
        self.i1.addWire(self.a, 0)
        self.i2.addWire(self.a, 1)
        self.i1.valueChanged.connect(self._increment)
        self.i2.valueChanged.connect(self._increment)

    def test_should_be_false_when_first_value_is_false(self):
        self._prepare(False, True)
        self._limit = 0
        self._wait()
        assert self.a.compute() == False

    def test_should_be_false_when_second_value_is_false(self):
        self._prepare(True, False)
        self._limit = 0
        self._wait()
        assert self.a.compute() == False

    def test_should_be_false_when_both_values_are_false(self):
        self._prepare(False, False)
        self._limit = 0
        self._wait()
        assert self.a.compute() == False

    def test_should_be_true_when_both_values_are_true(self):
        self._prepare(True, True)
        self._limit = 2
        self._wait()
        assert self.a.compute() == True

    def tearDown(self):
        self.i1.die()
        self.i2.die()
        self.a.die()
        self.i1.wait()
        self.i2.wait()
        self.a.wait()
