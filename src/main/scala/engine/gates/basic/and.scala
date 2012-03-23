package lgsis.engine
package gates

import exceptions._

class And(number : Int) extends Gate {
    val name = "And"
    if(number < 2) throw new NotEnoughInputsException()
    inputs ++= new Array[Boolean](number)

    override def compute : Boolean = {
        for(input <- inputs) {
            if(!input) return false
        }
        true
    }
}
