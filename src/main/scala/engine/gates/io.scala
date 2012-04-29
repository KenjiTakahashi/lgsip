package lgsis.engine
package gates
package io

import scala.actors._
import scala.actors.Actor._

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

case class STOP()

class Clock extends IOGate with Actor {
    inputs += false
    var timeout = 1000L
    start()

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
        if(timeout < 0) timeout = 0
    }

    override def compute : Boolean = inputs(0)
}
