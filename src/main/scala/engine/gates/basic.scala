package lgsis.engine
package gates
package basic

class And(number : Int) extends BasicGate(number, "And") {
    override def compute : Boolean = inputs().forall(x => x)
}

class Nand(number : Int) extends BasicGate(number, "Nand") {
    override def compute : Boolean = inputs().forall(x => !x)
}

class Or(number : Int) extends BasicGate(number, "Or") {
    override def compute : Boolean = inputs().contains(true)
}

class Nor(number : Int) extends BasicGate(number, "Nor") {
    override def compute : Boolean = !inputs().contains(true)
}

class Xor extends BasicGate(2, "Xor") {
    override def compute : Boolean = inputs()(0) ^ inputs()(1)
}

class Xnor extends BasicGate(2, "Xnor") {
    override def compute : Boolean = !(inputs()(0) ^ inputs()(1))
}

class Not extends BasicGate(1, "Not") {
    override def compute : Boolean = !inputs()(0)
}
