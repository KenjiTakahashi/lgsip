package lgsis.engine
package gates
package basic

class Xnor extends BasicGate(2, "Xnor") {
    override def compute : Boolean = {
        (!inputs(0) || inputs(1)) && (inputs(0) || !inputs(1))
    }
}
