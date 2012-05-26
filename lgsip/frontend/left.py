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

from PyQt4 import QtGui
import pyclbr


class LgsipBasicGatesBox(QtGui.QTreeWidget):
    """It's hacky, but we'll change it later"""
    _module = 'lgsip.frontend.gates.'

    def __init__(self, parent=None):
        super(LgsipBasicGatesBox, self).__init__(parent)
        self.setRootIsDecorated(False)
        self.setFixedWidth(110)
        self.header().close()
        for category in ['IO', 'Basic']:
            item = QtGui.QTreeWidgetItem()
            self.addTopLevelItem(item)
            #self.setItemWidget(item, 0, QtGui.QPushButton(category, self))
            module = self._module + category.lower()
            g = pyclbr.readmodule(module)
            for gate in g.keys():
                subitem = QtGui.QTreeWidgetItem()
                item.addChild(subitem)
                module_ = __import__(module, globals(), locals(), gate)
                self.setItemWidget(subitem, 0, getattr(module_, gate)())
        self.expandAll()
