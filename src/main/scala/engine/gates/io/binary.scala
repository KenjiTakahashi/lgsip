package lgsis.engine
package gates

class BinaryInput(new_value : Boolean) extends IOGate {
    var value = new_value
    def switch() {
        value = !value
    }
    override def compute : Boolean = value
}
