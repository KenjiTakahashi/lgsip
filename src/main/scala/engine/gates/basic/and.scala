package lgsis.engine
package gates
package basic

class And(number : Int) extends BasicGate(number, "And") {
    override def compute : Boolean = {
        for(input <- inputs) {
            if(!input) return false
        }
        true
    }
}
