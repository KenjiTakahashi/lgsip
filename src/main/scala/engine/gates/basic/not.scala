package lgsis.engine
package gates
package basic

class Not extends Gate {
    inputs += false

    override def compute : Boolean = {
        return !inputs(0)
    }
}
