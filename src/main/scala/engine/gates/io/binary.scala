package lgsis.engine
package gates

class BinaryInput(new_value : Boolean) extends IOGate {
    output = new_value

    def switch() {
        output = !output
        recompute()
    }
    override def compute : Boolean = output
}

class BinaryOutput extends IOGate {
    inputs += false

    override def compute : Boolean = inputs(0)
}
