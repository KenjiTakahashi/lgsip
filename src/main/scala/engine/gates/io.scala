package lgsis.engine
package gates
package io

class BinaryInput(input : Boolean) extends IOGate {
    inputs() += input

    def switch() {
        // that mess is temporary
        import scala.collection.mutable.ArrayBuffer
        val tmp = ArrayBuffer[Boolean]()
        tmp += !inputs()(0)
        inputs() = tmp
    }
    override def compute : Boolean = inputs()(0)
}

class BinaryOutput extends IOGate {
    inputs() += false

    override def compute : Boolean = inputs()(0)
}
