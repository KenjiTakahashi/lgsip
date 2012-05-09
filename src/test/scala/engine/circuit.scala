import org.specs2._
import lgsis.engine.gates.basic._
import lgsis.engine.gates.io._
import lgsis.engine.Circuit

class CircuitTest extends mutable.Specification {
    def ASimpleCircuit : (Circuit, BinaryOutput) = {
        val circuit = new Circuit()
        val i1 = new BinaryInput(true)
        val i2 = new BinaryInput(true)
        val i3 = new BinaryInput(true)
        val o = new BinaryOutput()
        val not = new Not()
        val and1 = new And(2)
        val and2 = new And(2)
        val or = new Or(2)
        circuit.addWire(i1, 0, not, 0)
        circuit.addWire(not, and1, 0)
        circuit.addWire(i2, 0, and1, 1)
        circuit.addWire(i2, 0, and2, 0)
        circuit.addWire(i3, 0, and2, 1)
        circuit.addWire(and1, or, 0)
        circuit.addWire(and2, or, 1)
        circuit.addWire(or, o, 0)
        return (circuit, o)
    }

    "A Simple Circuit" should {
        "return a proper value" in {
            val (circuit, o) = ASimpleCircuit
            circuit.step()
            o.compute should beEqualTo(false)
            circuit.step()
            o.compute should beEqualTo(true)
        }
    }
}
