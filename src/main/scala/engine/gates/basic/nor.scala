package lgsis.engine
package gates
package basic

class Nor(number : Int) extends BasicGate(number, "Nor") {
    override def compute : Boolean = {
        for(input <- inputs) {
            if(!input) return true
        }
        false
    }
}
