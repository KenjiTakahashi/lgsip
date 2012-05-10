import org.specs2._
import lgsis.engine.gates.basic._
import lgsis.engine.gates.io._
import lgsis.engine.Circuit

class CircuitTest extends mutable.Specification {
    def ASimpleCircuit(
        v1 : Boolean, v2 : Boolean, v3 : Boolean
    ) : (Circuit, BinaryOutput) = {
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
        "return true for (true, true, true)" in {
            val (circuit, o) = ASimpleCircuit(true, true, true)
            circuit.step()
            circuit.step()
            o.compute should beEqualTo(true)
        }
        "return true for (true, true, false)" in {
            val (circuit, o) = ASimpleCircuit(true, true, false)
            circuit.step()
            circuit.step()
            o.compute should beEqualTo(true)
        }
        "return true for (true, false, true)" in {
            val (circuit, o) = ASimpleCircuit(true, false, true)
            circuit.step()
            circuit.step()
            o.compute should beEqualTo(true)
        }
        "return false for (true, false, false)" in {
            val (circuit, o) = ASimpleCircuit(true, false, false)
            circuit.step()
            circuit.step()
            o.compute should beEqualTo(true)
        }
        "return false for (false, true, true)" in {
            val (circuit, o) = ASimpleCircuit(false, true, true)
            circuit.step()
            circuit.step()
            o.compute should beEqualTo(true)
        }
        "return false for (false, true, false)" in {
            val (circuit, o) = ASimpleCircuit(false, true, false)
            circuit.step()
            circuit.step()
            o.compute should beEqualTo(true)
        }
        "return true for (false, false, true)" in {
            val (circuit, o) = ASimpleCircuit(false, false, true)
            circuit.step()
            circuit.step()
            o.compute should beEqualTo(true)
        }
        "return false for (false, false, false)" in {
            val (circuit, o) = ASimpleCircuit(false, false, false)
            circuit.step()
            circuit.step()
            o.compute should beEqualTo(true)
        }
    }

    def ASophisticatedCircuit(
        v1 : Boolean, v2 : Boolean, v3 : Boolean, v4 : Boolean
    ) : (Circuit, (BinaryOutput, BinaryOutput)) = {
        val circuit = new Circuit()
        val i1 = new BinaryInput(v1)
        val i2 = new BinaryInput(v2)
        val i3 = new BinaryInput(v3)
        val i4 = new BinaryInput(v4)
        val nor = new Nor(2)
        val not1 = new Not()
        val not2 = new Not()
        val or1 = new Or(2)
        val or2 = new Or(2)
        val and1 = new And(2)
        val and2 = new And(2)
        val and3 = new And(2)
        val o1 = new BinaryOutput()
        val o2 = new BinaryOutput()
        circuit.addWire(i1, 0, not1, 0)
        circuit.addWire(i1, 0, nor, 0)
        circuit.addWire(i2, 0, nor, 1)
        circuit.addWire(i2, 0, and1, 1)
        circuit.addWire(i3, 0, not2, 0)
        circuit.addWire(i3, 0, or1, 0)
        circuit.addWire(i4, 0, or1, 1)
        circuit.addWire(i4, 0, and3, 1)
        circuit.addWire(not1, and1, 0)
        circuit.addWire(nor, and2, 0)
        circuit.addWire(or1, and2, 1)
        circuit.addWire(and1, or2, 0)
        circuit.addWire(not2, and3, 0)
        circuit.addWire(and3, or2, 1)
        circuit.addWire(and2, o1, 0)
        circuit.addWire(or2, o2, 0)
        return (circuit, (o1, o2))
    }

    "A Sophisticated Circuit" should {
        "return (false, false) for (true, true, true, true)" in {
            val (circuit, (o1, o2)) = ASophisticatedCircuit(
                true, true, true, true
            )
            circuit.step()
            circuit.step()
            o1.compute should beEqualTo(false)
            o2.compute should beEqualTo(false)
        }
        "return (false, true) for (false, true, true, true)" in {
            val (circuit, (o1, o2)) = ASophisticatedCircuit(
                false, true, true, true
            )
            circuit.step()
            circuit.step()
            o1.compute should beEqualTo(false)
            o2.compute should beEqualTo(true)
        }
        "return (false, false) for (true, false, true, true)" in {
            val (circuit, (o1, o2)) = ASophisticatedCircuit(
                true, false, true, true
            )
            circuit.step()
            circuit.step()
            o1.compute should beEqualTo(false)
            o2.compute should beEqualTo(false)
        }
        "return (true, false) for (false, false, true, true)" in {
            val (circuit, (o1, o2)) = ASophisticatedCircuit(
                false, false, true, true
            )
            circuit.step()
            circuit.step()
            o1.compute should beEqualTo(true)
            o2.compute should beEqualTo(false)
        }
        "return (false, true) for (true, true, false, true)" in {
            val (circuit, (o1, o2)) = ASophisticatedCircuit(
                true, true, false, true
            )
            circuit.step()
            circuit.step()
            o1.compute should beEqualTo(false)
            o2.compute should beEqualTo(true)
        }
        "return (false, true) for (false, true, false, true)" in {
            val (circuit, (o1, o2)) = ASophisticatedCircuit(
                false, true, false, true
            )
            circuit.step()
            circuit.step()
            o1.compute should beEqualTo(false)
            o2.compute should beEqualTo(true)
        }
        "return (false, true) for (true, false, false, true)" in {
            val (circuit, (o1, o2)) = ASophisticatedCircuit(
                true, false, false, true
            )
            circuit.step()
            circuit.step()
            o1.compute should beEqualTo(false)
            o2.compute should beEqualTo(true)
        }
        "return (true, true) for (false, false, false, true)" in {
            val (circuit, (o1, o2)) = ASophisticatedCircuit(
                false, false, false, true
            )
            circuit.step()
            circuit.step()
            o1.compute should beEqualTo(true)
            o2.compute should beEqualTo(true)
        }
        "return (false, false) for (true, false, false, false)" in {
            val (circuit, (o1, o2)) = ASophisticatedCircuit(
                true, false, false, false
            )
            circuit.step()
            circuit.step()
            o1.compute should beEqualTo(false)
            o2.compute should beEqualTo(false)
        }
        "return (false, true) for (true, false, false, true)" in {
            val (circuit, (o1, o2)) = ASophisticatedCircuit(
                true, false, false, true
            )
            circuit.step()
            circuit.step()
            o1.compute should beEqualTo(false)
            o2.compute should beEqualTo(true)
        }
        "return (false, false) for (true, false, true, false)" in {
            val (circuit, (o1, o2)) = ASophisticatedCircuit(
                true, false, true, false
            )
            circuit.step()
            circuit.step()
            o1.compute should beEqualTo(false)
            o2.compute should beEqualTo(false)
        }
        "return (true, false) for (false, false, true, false)" in {
            val (circuit, (o1, o2)) = ASophisticatedCircuit(
                false, false, true, false
            )
            circuit.step()
            circuit.step()
            o1.compute should beEqualTo(true)
            o2.compute should beEqualTo(false)
        }
        "return (true, false) for (false, false, true, true)" in {
            val (circuit, (o1, o2)) = ASophisticatedCircuit(
                false, false, true, true
            )
            circuit.step()
            circuit.step()
            o1.compute should beEqualTo(true)
            o2.compute should beEqualTo(false)
        }
        "return (false, true) for (false, true, false, false)" in {
            val (circuit, (o1, o2)) = ASophisticatedCircuit(
                false, true, false, false
            )
            circuit.step()
            circuit.step()
            o1.compute should beEqualTo(false)
            o2.compute should beEqualTo(true)
        }
        "return (false, false) for (true, false, false, false)" in {
            val (circuit, (o1, o2)) = ASophisticatedCircuit(
                true, false, false, false
            )
            circuit.step()
            circuit.step()
            o1.compute should beEqualTo(false)
            o2.compute should beEqualTo(false)
        }
        "return (false, false) for (false, false, false, false)" in {
            val (circuit, (o1, o2)) = ASophisticatedCircuit(
                false, false, false, false
            )
            circuit.step()
            circuit.step()
            o1.compute should beEqualTo(false)
            o2.compute should beEqualTo(false)
        }
    }
}
