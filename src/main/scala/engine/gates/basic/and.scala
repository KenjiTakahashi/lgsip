package lgsis.engine
package gates
package basic

import exceptions._

class And(number : Int) extends BasicGate(number, "And") {
    override def compute : Boolean = {
        for(input <- inputs) {
            if(!input) return false
        }
        true
    }
}
