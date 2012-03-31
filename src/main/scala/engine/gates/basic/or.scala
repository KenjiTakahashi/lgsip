package lgsis.engine
package gates
package basic

import exceptions._

class Or(number : Int) extends BasicGate(number, "Or") {
    override def compute : Boolean = {
        for(input <- inputs) {
            if(input) return true
        }
        false
    }
}
