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
from PyQt4.QtCore import Qt
import pyclbr


class _Delegate(QtGui.QStyledItemDelegate):
    def paint(self, painter, option, index):
        if not index.parent().isValid():
            options = QtGui.QStyleOptionButton()
            options.rect = option.rect
            options.state = option.state
            style = option.widget.style()
            style.drawControl(
                QtGui.QStyle.CE_PushButtonBevel, options, painter
            )
            option.rect.setWidth(15)
            style.drawPrimitive(
                QtGui.QStyle.PE_IndicatorBranch, option, painter
            )
            painter.drawText(
                options.rect, Qt.AlignVCenter | Qt.AlignCenter,
                index.data(Qt.DisplayRole)
            )


class _LgsipGatesWidget(QtGui.QTreeWidget):
    _module = 'lgsip.frontend.gates.'

    def __init__(self, categories, parent=None):
        super(_LgsipGatesWidget, self).__init__(parent)
        self.setRootIsDecorated(False)
        self.setItemDelegate(_Delegate())
        self.setIndentation(0)
        self.setFixedWidth(110)
        self.setExpandsOnDoubleClick(False)
        self.header().close()
        self.itemClicked.connect(self._expandCollapse)
        for category in categories:
            if isinstance(category, str):
                module = self._module + category.lower()
            else:
                category, module = category
                module = self._module + module
            item = QtGui.QTreeWidgetItem([category])
            self.addTopLevelItem(item)
            g = pyclbr.readmodule(module)
            for gate in g.keys():
                if gate[0] != '_':
                    subitem = QtGui.QTreeWidgetItem()
                    item.addChild(subitem)
                    module_ = __import__(module, globals(), locals(), gate)
                    self.setItemWidget(subitem, 0, getattr(module_, gate)())
        self.expandAll()

    def _expandCollapse(self, item):
        if item.isExpanded():
            self.collapseItem(item)
        else:
            self.expandItem(item)


class LgsipBasicGatesWidget(_LgsipGatesWidget):
    def __init__(self, parent=None):
        super(LgsipBasicGatesWidget, self).__init__(
            ['IO', 'Basic', 'Compound'], parent
        )


class LgsipComplexGatesWidget(_LgsipGatesWidget):
    def __init__(self, parent=None):
        super(LgsipComplexGatesWidget, self).__init__(
            [('Built-in', 'complex')], parent
        )
        # add user-defined here (from .config/...)
