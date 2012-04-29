import org.specs2._
import lgsis.engine.gates.basic._
import lgsis.engine.gates.io._
import lgsis.engine.Circuit

//class Test extends mutable.Specification {
    //"test" in {
        //val a = new BinaryInput(false)
        //val b = new BinaryInput(false)
        //val o = new BinaryOutput()
        //val c = new Circuit()
        //val r = new Or(2)
        //c.addWire(a, 0, r, 0)
        //c.addWire(b, 0, r, 1)
        //c.addWire(r, o, 0)
        //a.switch()
        //c.step()
        //o.compute must beEqualTo(true)
    //}
//}
class IOGatesTest extends mutable.Specification {
    val i = new BinaryInput(false)
    args(sequential=true)
    "The Binary Input" should {
        "be set to false" in {
            i.compute must beEqualTo(false)
        }
        "be set to true" in {
            i.switch()
            i.compute must beEqualTo(true)
        }
    }
}

class BasicGatesTest extends Specification {
    val a = new BinaryInput(false)
    val b = new BinaryInput(false)
    val out = new BinaryOutput()
    val circuit = new Circuit()

    class OrSpec extends mutable.Specification {
        val or = new Or(2)
        circuit.addWire(a, 0, or, 0)
        circuit.addWire(b, 0, or, 1)
        circuit.addWire(or, out, 0)
        "The Or gate" should {
            "be false for 2 false values" in {
                circuit.step()
                out.compute must beEqualTo(false)
            }
            "be true if any value is true" in {
                a.switch()
                circuit.step()
                out.compute must beEqualTo(true)
                b.switch()
                circuit.step()
                out.compute must beEqualTo(true)
                a.switch()
                circuit.step()
                out.compute must beEqualTo(true)
            }
        }
        circuit.removeAll()
    }
    class AndSpec extends mutable.Specification {
        val and = new And(2)
        circuit.addWire(a, 0, and, 0)
        circuit.addWire(b, 0, and, 1)
        circuit.addWire(and, out, 0)
        "The And gate" should {
            "be false if any value is false" in {
                circuit.step()
                out.compute must beEqualTo(false)
            }
        }
    }
    def is = {
        args(sequential=true)
        new AndSpec ^ new OrSpec
        //new OrSpec ^ new AndSpec
    }
}
