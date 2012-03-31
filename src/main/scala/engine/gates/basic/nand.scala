package lgsis.engine
package gates
package basic

class Nand(number : Int) extends BasicGate(number, "Nand") {
    override def compute : Boolean = {
        for(input <- inputs) {
            if(input) return false
        }
        true
    }
}
