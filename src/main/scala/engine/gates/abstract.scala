package lgsis.engine
package gates

import collection.mutable.ArrayBuffer

abstract class Gate {
    val inputs = ArrayBuffer[Boolean]()
    var output = false

    def addInputs(number : Int) {
        if(number < 1) return // throw exception
        inputs ++= new Array[Boolean](number)
        recompute()
    }
    def removeInputs(number : Int) {
        if(number < 1) return // throw exception
        if(inputs.size - number < 2) return // as above
        inputs.trimEnd(number)
        recompute()
    }
    def changeInput(index : Int, value : Boolean) {
        inputs(index) = value // need to catch exception here
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
