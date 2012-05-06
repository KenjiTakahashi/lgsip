package lgsis.engine

import gates.{BasicGate, IOGate}
import exceptions._
import scala.collection.mutable.{Set, Map, ArrayBuffer}
import com.scaladudes.signal.connect
import scala.actors._

class Circuit extends Actor {
    val wires = Map[BasicGate, Map[BasicGate, Int]]()
    val inputs = Map[(IOGate, Int), ArrayBuffer[(BasicGate, Int)]]()
    val outputs = Map[BasicGate, ArrayBuffer[(IOGate, Int)]]()
    var currentGates = Set[BasicGate]()

    case class STOP()

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
                outputs(gate).foreach {case (g, n) => g.changeInput(n, value)}
            } catch {
                case _: NoSuchElementException =>
            }
        }
        currentGates = currentGates_
    }
    def stepInputs(gate : IOGate, values : ArrayBuffer[Boolean]) {
        for(index <- values.indices) {
            try {
                inputs((gate, index)).foreach {
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
    def addWire(
        iGate : IOGate, iNumber : Int, oGate : BasicGate, oNumber : Int
    ) {
        val iWire = (iGate, iNumber)
        val oWire = (oGate, oNumber)
        if(inputs.contains(iWire)) {
            if(inputs(iWire).contains(oWire)) {
                throw new WireExistsException()
            } else {
                inputs(iWire) = ArrayBuffer[(BasicGate, Int)]()
            }
        } else {
            inputs(iWire) = ArrayBuffer[(BasicGate, Int)]()
        }
        connect[iGate.ValueChanged] {
            case iGate.ValueChanged(i) => stepInputs(iGate, i)
        }
        inputs(iWire) += oWire
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
        if(outputs.contains(iGate) && outputs(iGate).contains(wire)) {
            throw new WireExistsException()
        } else {
            outputs(iGate) = ArrayBuffer[(IOGate, Int)]()
        }
        outputs(iGate) += wire
    }
    def addWire(iGate :IOGate, oCircuit : Circuit, oNumber : Int) {
    }
    def addWire(iGate : BasicGate, oCircuit : Circuit, oNumber : Int) {
    }
    def addWire(
        iCircuit : Circuit, iNumber : Int, oCIrcuit : Circuit, oNumber : Int
    ) {
    }
    def addWire(
        iCircuit : Circuit, iNumber : Int, oGate : BasicGate, oNumber : Int
    ) {
    }
    def addWire(
        iCircuit : Circuit, iNumber : Int, oGate : IOGate, oNumber : Int
    ) {
    }
    def removeAll() {
        wires.clear()
        inputs.clear()
        outputs.clear()
        currentGates.clear()
    }
}
