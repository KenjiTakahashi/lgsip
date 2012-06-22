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
from PyQt4.QtCore import Qt, QRectF, QPointF
from lgsip.frontend.gates.gate import DeleteGateButton, _LgsipGateButton
from uuid import uuid4
import imp


class Wire(QtGui.QGraphicsObject):
    def __init__(self, propagating=False, parent=None):
        super(Wire, self).__init__(parent)
        self.setZValue(-1)
        self.setFlag(self.ItemIsSelectable, True)
        self.x, self.y, self.nx, self.ny = 0, 0, 0, 0
        self._propagating = propagating
        self._startParent = None
        self._endParent = None

    def setStart(self, x, y):
        self.x, self.y = x, y

    def setEnd(self, x, y):
        self.nx, self.ny = x, y

    def setStartParent(self, parent):
        self._startParent = parent

    def setEndParent(self, parent):
        self._endParent = parent

    def setPropagating(self, value):
        self._propagating = value

    def boundingRect(self):
        return QRectF(self.x, self.y, self.x + self.nx, self.y + self.ny)

    def paint(self, painter, option, widget):
        pen = QtGui.QPen()
        pen.setWidth(4)
        pen.setColor(QtGui.QColor(QtGui.QPalette().mid()))
        painter.setPen(pen)
        dx = (self.nx - self.x) / 2
        dy = (self.ny - self.y) / 2
        self.path = QtGui.QPainterPath()
        self.shape = QtGui.QPainterPath()
        self.path.moveTo(self.x, self.y)
        if dx and dy:
            dx += self.x
            self.path.lineTo(dx, self.y)
            self.shape.addRect(self.x, self.y - 2, dx - self.x, 4)
            self.path.moveTo(dx, self.y)
            self.path.lineTo(dx, self.ny)
            self.shape.addRect(dx - 2, self.y - 2, 4, self.ny - self.y)
            self.path.moveTo(dx, self.ny)
        self.path.lineTo(self.nx, self.ny)
        self.shape.addRect(dx - 2, self.ny - 2, self.nx - dx, 4)
        painter.drawPath(self.path)
        if self._propagating:
            pen.setDashPattern([3, 4])
            pen.setColor(Qt.red)
            painter.setPen(pen)
            painter.drawPath(self.path)

    def shape(self):
        return self.shape

    def mousePressEvent(self, event):
        super(Wire, self).mousePressEvent(event)
        if event.button() == Qt.RightButton:
            if self._endParent:
                self._startParent.parent().disconnect(self._endParent)
            self.deleteLater()

    def mouseMoveEvent(self, event):
        super(Wire, self).mouseMoveEvent(event)
        print(event.pos())


class IntegrateGateButton(_LgsipGateButton):
    def __init__(self, parent=None):
        super(IntegrateGateButton, self).__init__(parent)
        self.path.addPolygon(QtGui.QPolygonF([
            QPointF(3, 3), QPointF(7, 8), QPointF(3, 13)
        ]))
        self.path.addPolygon(QtGui.QPolygonF([
            QPointF(13, 3), QPointF(9, 8), QPointF(13, 13)
        ]))
        self.color = QtGui.QColor(0, 0, 160)


class _RubberBand(QtGui.QGraphicsObject):
    def __init__(self, parent=None):
        super(_RubberBand, self).__init__(parent)
        self.x, self.y, self.nx, self.ny = 0, 0, 0, 0
        self.setZValue(-2)
        self._delete = DeleteGateButton()
        self._delete.clicked.connect(self._deleteGates)
        self._integrate = IntegrateGateButton()
        proxy = QtGui.QGraphicsProxyWidget(self)
        proxy.setWidget(self._delete)
        proxy2 = QtGui.QGraphicsProxyWidget(self)
        proxy2.setWidget(self._integrate)

    def setStart(self, pos):
        self.x, self.y = pos.x(), pos.y()

    def setEnd(self, pos):
        self.nx, self.ny = pos.x(), pos.y()
        if self.ny < self.y:
            y = self.ny + 4
        else:
            y = self.ny - 20
        if self.nx < self.x:
            x = self.nx + 4
            x2 = x + 20
        else:
            x = self.nx - 20
            x2 = x - 20
        self._delete.move(x, y)
        self._integrate.move(x2, y)

    def _deleteGates(self):
        scene = self.scene()
        for gate in scene.collidingItems(self):
            gate.deleteLater()
        scene.removeItem(self)

    def boundingRect(self):
        return QRectF(self.x, self.y, self.nx - self.x, self.ny - self.y)

    def paint(self, painter, option, widget):
        painter.setPen(Qt.NoPen)
        painter.setBrush(QtGui.QPalette().light())
        width, height = self.nx - self.x, self.ny - self.y
        painter.drawRect(self.x, self.y, width, height)


class _LgsipScene(QtGui.QGraphicsScene):
    def __init__(self, parent=None):
        super(_LgsipScene, self).__init__(parent)
        self._wire = None
        self._direction = None
        self._sender = None
        self._rubber = _RubberBand()
        self._rubber_ = False

    def clean(self):
        for item in self.items():
            try:
                widget = item.widget()._gate
            except AttributeError:
                pass
            else:
                widget.die()
                widget.wait()
            finally:
                item.deleteLater()

    def dropEvent(self, event):
        data = event.mimeData()
        filename = data.data('lgsip/x-filename')
        if filename:
            from lgsip.frontend.gates.gate import ComplexGate
            gate = ComplexGate(bytes(filename).decode('utf-8'))
        else:
            module = bytes(
                data.data('lgsip/x-modulename').data()
            ).decode('utf-8')
            cls = bytes(data.data('lgsip/x-classname').data()).decode('utf-8')
            gate = getattr(__import__(module, globals(), locals(), cls), cls)()
        gate.wiring.connect(self.wire)
        proxy = self.addWidget(gate)
        proxy.setPos(event.scenePos())

    def wire(self, realSender, direction):
        if self._wire and self._direction != direction:
            if not direction:
                realSender.addEndWire(
                    self._wire, self.sender().pos(), self._sender.parent()
                )
                self._wire.setEndParent(realSender)
            else:
                realSender.addStartWire(
                    self._wire, self.sender().pos(), self._sender.parent()
                )
                self._wire.setStartParent(realSender)
            self._wire = None
            self._sender = None
        elif not self._wire:
            self._direction = direction
            self._sender = realSender
            self._wire = Wire(self._sender.propagating)
            if direction:
                self._sender.addStartWire(self._wire, self.sender().pos())
                self._wire.setStartParent(self._sender)
            else:
                self._sender.addEndWire(self._wire, self.sender().pos())
                self._wire.setEndParent(self._sender)
            self.addItem(self._wire)

    def mousePressEvent(self, event):
        button = event.button()
        if button == Qt.RightButton:
            if self._wire:
                self.removeItem(self._wire)
                self._sender.cancelWire(self._wire)
                self._wire = None
                self._sender = None
            elif self._rubber:
                self.removeItem(self._rubber)
        elif button == Qt.LeftButton:
            if(
                not self._rubber_ and
                not self.itemAt(event.scenePos()) and
                not self._wire
            ):
                self.removeItem(self._rubber)
                self._rubber_ = True
                self._rubber.setStart(event.scenePos())
                self._rubber.setEnd(event.scenePos())
                self.addItem(self._rubber)
            elif self._rubber_:
                self._rubber_ = False
        super(_LgsipScene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._wire:
            pos = event.scenePos()
            if self._direction:
                self._wire.setEnd(pos.x(), pos.y())
            else:
                self._wire.setStart(pos.x(), pos.y())
        elif self._rubber_:
            self._rubber.setEnd(event.scenePos())
        self.update()
        super(_LgsipScene, self).mouseMoveEvent(event)


class SketchBoard(QtGui.QGraphicsView):
    def __init__(self, parent=None):
        super(SketchBoard, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        # Hope it will be fast enough or maybe we'll
        # find a better way later on.
        self.setViewportUpdateMode(self.FullViewportUpdate)
        self.setMouseTracking(True)
        self.setScene(_LgsipScene())

    def save(self):
        dialog = QtGui.QFileDialog(
            self, self.tr("Save circuit"),
            filter=self.tr("Circuit files (*.lgsip)")
        )
        dialog.setFileMode(dialog.AnyFile)
        result = dialog.exec_()
        if result:
            filename = dialog.selectedFiles()[0]
            if filename[-6:] != ".lgsip":
                filename += ".lgsip"

            def a(widget):
                name = widget.__class__.__name__
                if name == 'BinaryInput':
                    return widget._switch.isChecked()
                elif name == 'Clock':
                    text = widget.time.text()
                    return text and text or 1000
                elif name == 'ComplexGate':
                    return "'{0}'".format(widget._intname)
                elif name in ['And', 'Or', 'Nand', 'Nor']:
                    return len(widget._inbuttons)
                else:
                    return ""
            with open(filename, 'w') as f:
                uuids = dict()
                wires = dict()
                f.write("from PyQt4.QtCore import QPointF, QPoint\n")
                f.write("from lgsip.frontend.sketchboard import Wire\n")
                f.write("from lgsip.frontend.gates.io import ")
                f.write("BinaryInput, BinaryOutput, Clock\n")
                f.write("from lgsip.frontend.gates.basic import ")
                f.write("And, Or, Not\n")
                f.write("from lgsip.frontend.gates.compound import ")
                f.write("Nor, Nand, Xor, Xnor\n")
                f.write("from lgsip.frontend.gates.gate import ComplexGate\n")
                f.write("def load(self):\n")
                for item in self.items():
                    try:
                        widget = item.widget()
                        uuid = "g{0}".format(uuid4().int)
                        uuids[widget] = uuid
                        f.write("    {0} = {1}({2})\n".format(
                            uuid, widget.__class__.__name__, a(widget)
                        ))
                        f.write("    p = self.addWidget({0})\n".format(uuid))
                        pos = item.scenePos()
                        f.write("    p.setPos(QPointF({0}, {1}))\n".format(
                            pos.x(), pos.y()
                        ))
                    except AttributeError:
                        wires[item._startParent] = item._endParent
                for sParent, eParent in wires.items():
                    uuid = "w{0}".format(uuid4().int)
                    startParent = uuids[sParent.parent()]
                    endParent = uuids[eParent.parent()]
                    f.write("    {0} = Wire()\n".format(uuid))
                    f.write("    {0}.setStartParent({1})\n".format(
                        uuid, startParent)
                    )
                    f.write("    {0}.setEndParent({1})\n".format(
                        uuid, endParent
                    ))
                    f.write("    self.addItem({0})\n".format(uuid))
                    pos = sParent.parent().pos()
                    f.write("    {0}._outbuttons[{1}]".format(
                        startParent,
                        sParent.parent()._outbuttons.index(sParent)
                    ))
                    f.write(".addStartWire({0}, QPoint({1}, {2}))\n".format(
                        uuid, pos.x(), pos.y()
                    ))
                    pos = eParent.parent().pos()
                    f.write("    {0}._inbuttons[{1}]".format(
                        endParent, eParent.parent()._inbuttons.index(eParent)
                    ))
                    f.write(".addEndWire({0}, QPoint({1}, {2}), {3})\n".format(
                        uuid, pos.x(), pos.y(), startParent
                    ))

    def load(self):
        dialog = QtGui.QFileDialog(
            self, self.tr("Load circuit"),
            filter=self.tr("Circuit files (*.lgsip)")
        )
        dialog.setFileMode(dialog.ExistingFile)
        result = dialog.exec_()
        if result:
            filename = dialog.selectedFiles()[0]
            module = imp.load_source("circuit", filename)
            scene = self.scene()
            scene.clean()
            module.load(scene)

    def dragEnterEvent(self, event):
        data = event.mimeData()
        if(data.hasFormat('lgsip/x-classname')
        and data.hasFormat('lgsip/x-modulename')
        or data.hasFormat('lgsip/x-filename')):
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        self.dragEnterEvent(event)
