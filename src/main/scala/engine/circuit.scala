package lgsis.engine

import gates.{BasicGate, IOGate}
import gates.io.{BinaryInput, BinaryOutput}
import exceptions._
import scala.collection.mutable.{Set, Map, ArrayBuffer}
import com.scaladudes.signal.connect
import scala.actors._

class Circuit extends Actor {
    private val wires = Map[BasicGate, Map[BasicGate, Int]]()
    private val iWires = Map[(IOGate, Int), ArrayBuffer[(BasicGate, Int)]]()
    private val oWires = Map[BasicGate, ArrayBuffer[(IOGate, Int)]]()
    private var currentGates = Set[BasicGate]()
    private val inputs = ArrayBuffer[ArrayBuffer[(BasicGate, Int)]]()
    private val outputs = ArrayBuffer[BasicGate]()
    private var integrated = false

    private case class STOP()

    def act {
        loop {
            reactWithin(1) {
                case TIMEOUT => step()
                case STOP => exit()
            }
        }
    }
    def die() {
        this ! STOP
    }
    def step() {
        val currentGates_ = Set[BasicGate]()
        for(gate <- currentGates) {
            val value = gate.compute
            if(wires.contains(gate)) {
                for((g, n) <- wires(gate)) {
                    g.changeInput(n, value)
                    // notify to the GUI
                }
                currentGates_ ++= wires(gate).keys
            }
            try {
                oWires(gate).foreach {case (g, n) => g.changeInput(n, value)}
            } catch {
                case _: NoSuchElementException =>
            }
        }
        currentGates = currentGates_
    }
    private def stepInputs(gate : IOGate, values : ArrayBuffer[Boolean]) {
        for(index <- values.indices) {
            try {
                iWires((gate, index)).foreach {
                    case (g, n) => {
                        g.changeInput(n, values(index))
                        currentGates += g
                    }
                }
            } catch {
                case _: NoSuchElementException =>
            }
        }
    }
    def integrate() {
        integrated = true
        for(((g, n), a) <- iWires) {
            if(g.isInstanceOf[BinaryInput]) {
                inputs += a
                iWires -= ((g, n))
            }
        }
        for((g, a) <- oWires) {
            for(o <- a) {
                if(o.isInstanceOf[BinaryOutput]) {
                    outputs += g
                    oWires(g) -= o
                }
            }
        }
    }
    def disintegrate() {
        integrated = false
        inputs.clear()
        outputs.clear()
    }
    def addWire(
        iGate : IOGate, iNumber : Int, oGate : BasicGate, oNumber : Int
    ) {
        val iWire = (iGate, iNumber)
        val oWire = (oGate, oNumber)
        if(iWires.contains(iWire)) {
            if(iWires(iWire).contains(oWire)) {
                throw new WireExistsException()
            } else {
                iWires(iWire) = ArrayBuffer[(BasicGate, Int)]()
            }
        } else {
            iWires(iWire) = ArrayBuffer[(BasicGate, Int)]()
        }
        connect[iGate.ValueChanged] {
            case iGate.ValueChanged(i) => stepInputs(iGate, i)
        }
        iWires(iWire) += oWire
        currentGates += oGate
    }
    def addWire(iGate : BasicGate, oGate : BasicGate, oNumber : Int) {
        if(wires.contains(iGate)) {
            if(wires(iGate).contains(oGate)) {
                throw new WireExistsException()
            }
        } else {
            wires(iGate) = Map[BasicGate, Int]()
        } // WTF?! (but seems it has to be that way...)
        wires(iGate)(oGate) = oNumber
    }
    def addWire(iGate : BasicGate, oGate : IOGate, oNumber : Int) {
        val wire = (oGate, oNumber)
        if(oWires.contains(iGate) && oWires(iGate).contains(wire)) {
            throw new WireExistsException()
        } else {
            oWires(iGate) = ArrayBuffer[(IOGate, Int)]()
        }
        oWires(iGate) += wire
    }
    def addWire(
        iGate :IOGate, iNumber : Int, oCircuit : Circuit, oNumber : Int
    ) {
        for((g, n) <- oCircuit.inputs(oNumber)) {
            addWire(iGate, iNumber, g, n)
        }
    }
    def addWire(iGate : BasicGate, oCircuit : Circuit, oNumber : Int) {
        for((g, n) <- oCircuit.inputs(oNumber)) {
            addWire(iGate, g, n)
        }
    }
    def addWire(
        iCircuit : Circuit, iNumber : Int, oCircuit : Circuit, oNumber : Int
    ) {
        for((g, n) <- oCircuit.inputs(oNumber)) {
            addWire(iCircuit.outputs(iNumber), g, n)
        }
    }
    def addWire(
        iCircuit : Circuit, iNumber : Int, oGate : BasicGate, oNumber : Int
    ) {
        addWire(iCircuit.outputs(iNumber), oGate, oNumber)
    }
    def addWire(
        iCircuit : Circuit, iNumber : Int, oGate : IOGate, oNumber : Int
    ) {
        addWire(iCircuit.outputs(iNumber), oGate, oNumber)
    }
    def removeAll() {
        wires.clear()
        iWires.clear()
        oWires.clear()
        currentGates.clear()
    }
}
