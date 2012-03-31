package lgsis.engine
package gates
package basic

import exceptions._

class Or(number : Int) extends Gate {
    val name = "Or"
    if(number < 2) throw new NotEnoughInputsException()
    inputs ++= new Array[Boolean](number)

    override def compute : Boolean = {
        for(input <- inputs) {
            if(input) return true
        }
        false
    }
}
