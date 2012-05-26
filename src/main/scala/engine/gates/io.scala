package lgsis.engine
package gates
package io

import scala.actors._

class BinaryInput(input : Boolean) extends IOGate {
    inputs += input

    def switch() {
        inputs(0) = !inputs(0)
        emit(ValueChanged(inputs))
    }
    override def compute : Boolean = inputs(0)
}

class BinaryOutput extends IOGate {
    inputs += false

    override def compute : Boolean = inputs(0)
}

class Clock(var timeout : Long = 1000L) extends IOGate with Actor {
    inputs += false
    start()

    private case class STOP()

    def act {
        loop {
            reactWithin(timeout) {
                case TIMEOUT => {
                    inputs(0) = !inputs(0)
                    emit(ValueChanged(inputs))
                }
                case STOP => exit()
            }
        }
    }

    def slower() {
        timeout += 20 // upper cap ?
    }
    def faster() {
        timeout -= 20
        if(timeout < 1) timeout = 1
    }
    def die() {
        this ! STOP
    }

    override def compute : Boolean = inputs(0)
}
