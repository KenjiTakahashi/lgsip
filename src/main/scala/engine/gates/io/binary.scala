package lgsis.engine
package gates
package io

class BinaryInput(new_value : Boolean) extends Gate {
    output = new_value

    def switch() {
        output = !output
        recompute()
    }
    override def compute : Boolean = output
}

class BinaryOutput extends Gate {
    inputs += false
    
    override def compute : Boolean = inputs(0)
}
