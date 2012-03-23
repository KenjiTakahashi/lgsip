package lgsis.engine
package gates

import exceptions._
import collection.mutable.ArrayBuffer

abstract class Gate {
    val inputs = ArrayBuffer[Boolean]()
    var output = false

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
    def changeInput(index : Int, value : Boolean) {
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
    private def recompute() {
        val new_output = compute
        if(new_output != output) {
            output = new_output
            // notify somehow
        }
    }
}
