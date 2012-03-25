package lgsis.engine
package gates

class BinaryInput(new_value : Boolean) extends IOGate {
    var value = new_value
    def switch(new_value : Boolean) {
        value = new_value
    }
    override def compute : Boolean = value
}
