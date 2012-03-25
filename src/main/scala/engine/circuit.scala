package lgsis.engine

import gates.{BasicGate, IOGate}
import exceptions._
import collection.mutable.{ArrayBuffer, Map}

class Circuit {
    val wires = ArrayBuffer[(BasicGate, Int, BasicGate, Int)]()

    def addWire(iGate : BasicGate, iNumber : Int, oGate : BasicGate, oNumber : Int) {
        val wire = (iGate, iNumber, oGate, oNumber)
        if(wires.contains(wire)) throw new WireExistsException()
        wires += wire
    }
    def removeWire(iGate : BasicGate, iNumber : Int, oGate : BasicGate, oNumber : Int) {
        wires -= ((iGate, iNumber, oGate, oNumber))
    }
}

class IntegratedCircuit(circuit : Circuit) {
    val inputs = Map[IOGate, Int]()
    val outputs = Map[IOGate, Int]()

    def addInput(iGate : IOGate, iNumber : Int) {
        if(inputs.contains(iGate)) throw new IOConnectedException()
        inputs += iGate -> iNumber
    }
    def removeInput(iGate : IOGate) {
        inputs -= iGate
    }
    def addOutput(oGate : IOGate, oNumber : Int) {
        if(outputs.contains(oGate)) throw new IOConnectedException()
        outputs += oGate -> oNumber
    }
    def removeOutput(oGate : IOGate) {
        outputs -= oGate
    }
}
