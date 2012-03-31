package lgsis.engine
package gates
package basic

class Xor extends BasicGate(2, "Xor") {
    override def compute : Boolean = {
        (inputs(0) && !inputs(1)) || (!inputs(0) && inputs(1))
    }
}
