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
from PyQt4.QtCore import Qt, QSize, QMimeData
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
        else:
            pixmap = index.data(666)
            painter.drawPixmap(10, option.rect.y() + 10, pixmap)

    def sizeHint(self, option, index):
        size = super(_Delegate, self).sizeHint(option, index)
        if not index.parent().isValid():
            return size
        return QSize(size.width(), index.data(666).height() + 20)


class _LgsipGatesWidget(QtGui.QTreeWidget):
    _module = 'lgsip.frontend.gates.'

    def __init__(self, categories, parent=None):
        super(_LgsipGatesWidget, self).__init__(parent)
        self.setRootIsDecorated(False)
        self.setItemDelegate(_Delegate())
        self.setIndentation(0)
        self.setFixedWidth(110)
        self.setExpandsOnDoubleClick(False)
        self.setDragDropMode(self.DragOnly)
        self.header().close()
        self.itemClicked.connect(self._expandCollapse)
        for name, id in categories:
            module = self._module + id.lower()
            item = QtGui.QTreeWidgetItem([name])
            self.addTopLevelItem(item)
            g = pyclbr.readmodule(module)
            for gate in g.keys():
                if gate[0] != '_':
                    subitem = QtGui.QTreeWidgetItem()
                    item.addChild(subitem)
                    module_ = __import__(module, globals(), locals(), gate)
                    widget = getattr(module_, gate)()
                    pixmap = self.createPixmap(widget)
                    subitem.setData(0, 666, pixmap)
                    subitem.setData(0, 667, gate)
                    subitem.setData(0, 668, module)
        self.expandAll()

    def createPixmap(self, widget):
        pixmap = QtGui.QPixmap(widget.sizeHint())
        pixmap.fill(Qt.transparent)
        widget.render(pixmap, flags=QtGui.QWidget.DrawChildren)
        widget._gate.die()
        return pixmap

    def _expandCollapse(self, item):
        if item.isExpanded():
            self.collapseItem(item)
        else:
            self.expandItem(item)

    def startDrag(self, actions):
        index = self.currentIndex()
        if index.parent().isValid():
            data = QMimeData()
            filename = index.data(669)
            if filename:
                data.setData('lgsip/x-filename', filename)
            else:
                data.setData('lgsip/x-classname', index.data(667))
                data.setData('lgsip/x-modulename', index.data(668))
            drag = QtGui.QDrag(self)
            drag.setMimeData(data)
            drag.setPixmap(index.data(666))
            drag.start(Qt.CopyAction)


class LgsipBasicGatesWidget(_LgsipGatesWidget):
    def __init__(self, parent=None):
        super(LgsipBasicGatesWidget, self).__init__(
            [
                (QtGui.QApplication.translate('main', 'IO'), 'IO'),
                (QtGui.QApplication.translate('main', 'Basic'), 'Basic'),
                (QtGui.QApplication.translate('main', 'Compound'), 'Compound'),
            ], parent
        )


from os import listdir
from os.path import isfile, join, dirname, normpath
from lgsip.frontend.gates.gate import ComplexGate


class LgsipComplexGatesWidget(_LgsipGatesWidget):
    def __init__(self, parent=None):
        super(LgsipComplexGatesWidget, self).__init__([], parent)
        item = QtGui.QTreeWidgetItem([self.tr("Built-in")])
        self.addTopLevelItem(item)
        path = normpath(join(dirname(__file__), "..", "engine/gates/complex"))
        for gate in [f for f in listdir(path)
            if isfile(join(path, f)) and f[-6:] == '.lgsip'
        ]:
            subitem = QtGui.QTreeWidgetItem()
            item.addChild(subitem)
            filename = join(path, gate)
            pixmap = self.createPixmap(ComplexGate(filename, True))
            subitem.setData(0, 666, pixmap)
            subitem.setData(0, 669, filename)
        item = QtGui.QTreeWidgetItem([self.tr("User-defined")])
        self.addTopLevelItem(item)
        self.expandAll()
