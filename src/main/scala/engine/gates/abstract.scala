package lgsis.engine
package gates

import exceptions._
import collection.mutable.ArrayBuffer

abstract class Gate {
    val inputs = ArrayBuffer[Boolean]()
    var output = false
    val wires = ArrayBuffer[(Gate, Int)]()

    def addInputs(number : Int) {
        if(number < 1) throw new NegativeNumOfInputsException()
        inputs ++= new Array[Boolean](number)
        recompute()
    }
    def removeInputs(number : Int) {
        if(number < 1) throw new NegativeNumOfInputsException()
        if(inputs.size - number < 2) throw new NotEnoughInputsException()
        inputs.trimEnd(number)
        recompute()
    }
    protected def changeInput(index : Int, value : Boolean) {
        try {
            inputs(index) = value
        } catch {
            case _: IndexOutOfBoundsException => {
                throw new InvalidInputIndexException()
            }
        }
        recompute()
    }
    def compute : Boolean
    protected def recompute() {
        output = compute
        wires.foreach{case (g, n) => g.changeInput(n, output)}
    }
    def addWire(oGate : Gate, oNumber : Int) {
        val wire = (oGate, oNumber)
        if(wires.contains(wire)) throw new WireExistsException()
        wires += wire
        recompute()
    }
    def removeWire(oGate : Gate, oNumber : Int) {
        wires -= ((oGate, oNumber))
        recompute()
    }
}

abstract class BasicGate(number : Int, name : String) extends Gate {
    if(number < 2) throw new NotEnoughInputsException()
    inputs ++= new Array[Boolean](number)
}
