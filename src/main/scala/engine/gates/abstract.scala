package lgsis.engine
package gates

import exceptions._
import collection.mutable.ArrayBuffer
import com.scaladudes.signal.{Signal, SignalEmitter}

abstract class Gate {
    val inputs = ArrayBuffer[Boolean]()

    def addInputs(number : Int) {
        if(number < 1) throw new NegativeNumOfInputsException()
        inputs ++= new Array[Boolean](number)
    }
    def removeInputs(number : Int) {
        if(number < 1) throw new NegativeNumOfInputsException()
        if(inputs.size - number < 2) throw new NotEnoughInputsException()
        inputs.trimEnd(number)
    }
    def changeInput(index : Int, value : Boolean) {
        try {
            inputs(index) = value
        } catch {
            case _: IndexOutOfBoundsException => {
                throw new InvalidInputIndexException()
            }
        }
    }
    def compute : Boolean
}

abstract class BasicGate(number : Int, name : String) extends Gate {
    if(name != "Not" && number < 2) throw new NotEnoughInputsException()
    inputs ++= new Array[Boolean](number)
}

abstract class IOGate extends Gate with SignalEmitter {
    case class ValueChanged(value : ArrayBuffer[Boolean]) extends Signal
}
