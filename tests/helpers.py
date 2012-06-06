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

from PyQt4.QtCore import QCoreApplication, QObject
import sys
from collections import Counter


class GateTest(QObject):
    def setUp(self):
        self.app = QCoreApplication(sys.argv)
        self._occurrences = Counter()

    def _increment(self, _, __):
        self._occurrences[self.sender()] += 1
        for limit in self._limit:
            if self._occurrences == limit:
                self.app.quit()
                break

    def _wait(self):
        self._limit = [Counter(l) for l in self._limit]
        if self._limit[0]:
            self.app.exec_()
