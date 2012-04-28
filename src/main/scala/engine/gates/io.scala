package lgsis.engine
package gates
package io

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
