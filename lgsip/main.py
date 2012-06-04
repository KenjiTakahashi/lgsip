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
from lgsip.frontend.center import LgsipTabWidget
from lgsip.frontend.treewidgets import(
    LgsipBasicGatesWidget, LgsipComplexGatesWidget
)
#from lgsip.frontend.left import LgsipBasicGatesBox


class Main(QtGui.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        widget = QtGui.QWidget()
        layout = QtGui.QHBoxLayout()
        self.basicgates = LgsipBasicGatesWidget()
        self.complexgates = LgsipComplexGatesWidget()
        self.tabs = LgsipTabWidget()
        self.tabs.addTab()
        layout.addWidget(self.basicgates)
        layout.addWidget(self.tabs)
        layout.addWidget(self.complexgates)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        #from lgsip.engine.gates.io import BinaryInput, BinaryOutput
        #from lgsip.engine.gates.basic import And
        #bi1 = BinaryInput(True)
        #bi2 = BinaryInput(True)
        #and_ = And(2)
        #bo = BinaryOutput()
        #bi1.addWire((and_, 0))
        #bi2.addWire((and_, 1))
        #and_.addWire((bo, 0))
        #from time import sleep
        #sleep(2)
        #print(bo.compute())


def run():
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("lgsip")
    main = Main()
    main.show()
    sys.exit(app.exec_())
