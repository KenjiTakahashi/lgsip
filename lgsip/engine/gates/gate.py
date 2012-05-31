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
from PyQt4.QtCore import QObject
from pykka.actor import ThreadingActor


class _Gate(QObject, ThreadingActor):
    def __init__(self):
        super(_Gate, self).__init__()
        self._inputs = list()
        self._wires = list()
        self.start()

    def on_receive(self, message):
        if message.get('die'):
            self.stop()
        else:
            pass

    def changeInput(self, index, value):
        try:
            self._inputs[value] = value
        except IndexError:
            raise lgsiperr.InvalidInputIndexError

    def compute(self):
        raise NotImplementedError


class Compound(QObject):
    pass
