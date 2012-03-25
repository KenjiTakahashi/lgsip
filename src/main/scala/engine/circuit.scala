package lgsis.engine

import gates.Gate
import exceptions._
import collection.mutable.ArrayBuffer

class Circuit {
    val wires = ArrayBuffer[(Gate, Int, Gate, Int)]()
    def addWire(iGate : Gate, iNumber : Int, oGate : Gate, oNumber : Int) {
        val wire = (iGate, iNumber, oGate, oNumber)
        if(wires.contains(wire)) throw new WireExistsException()
        wires += wire
    }
    def removeWire(iGate : Gate, iNumber : Int, oGate : Gate, oNumber : Int) {
        wires -= ((iGate, iNumber, oGate, oNumber))
    }
}

class IntegratedCircuit(circuit : Circuit) {
    val inputs = ArrayBuffer[(Gate, Int)]()
    val outputs = ArrayBuffer[(Gate, Int)]()

    def addInput(iGate : Gate, iNumber : Int) {
    }
    def removeInput(iGate : Gate) {
    }
}
