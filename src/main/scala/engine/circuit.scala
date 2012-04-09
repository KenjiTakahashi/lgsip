package lgsis.engine

import gates.{BasicGate, IOGate}
import exceptions._
import scala.collection.mutable.{Set, Map, ArrayBuffer}
import commons.properties.Observable.observe

class Circuit {
    val wires = Map[BasicGate, Map[BasicGate, Int]]()
    .withDefaultValue(Map[BasicGate, Int]())
    val inputs = Map[(IOGate, Int), ArrayBuffer[(BasicGate, Int)]]()
    .withDefaultValue(ArrayBuffer[(BasicGate, Int)]())
    val outputs = Map[BasicGate, ArrayBuffer[(IOGate, Int)]]()
    .withDefaultValue(ArrayBuffer[(IOGate, Int)]())
    var currentGates = Set[BasicGate]()

    def step() {
        val currentGates_ = Set[BasicGate]()
        for(gate <- currentGates) {
            val value = gate.compute
            for((g, n) <- wires(gate)) {
                g.changeInput(n, value)
                // notify to the GUI
            }
            try {
                outputs(gate).foreach {case (g, n) => g.changeInput(n, value)}
            } catch {
                case _: NoSuchElementException =>
            }
            //println(gate)
            //println(gate.inputs())
            currentGates_ ++= wires(gate).keys
        }
        currentGates = currentGates_
    }
    def stepInputs(gate : IOGate, values : ArrayBuffer[Boolean]) {
        for(index <- values.indices) {
            try {
                inputs((gate, index)).foreach {
                    case (g, n) => g.changeInput(n, values(index))
                }
            } catch {
                case _: NoSuchElementException =>
            }
        }
    }
    def addWire(iGate : IOGate, iNumber : Int, oGate : BasicGate, oNumber : Int) {
        val iWire = (iGate, iNumber)
        val oWire = (oGate, oNumber)
        if(inputs.contains(iWire) && inputs(iWire).contains(oWire)) {
            throw new WireExistsException()
        }
        observe(iGate.inputs) {values => stepInputs(iGate, values)}
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
        }
        outputs(iGate) += wire
    }
}
