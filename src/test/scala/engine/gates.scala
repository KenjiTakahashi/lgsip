import org.specs2._
import lgsis.engine.gates.basic._
import lgsis.engine.gates.io._
import lgsis.engine.Circuit

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
    trait Prepare {
        val a = new BinaryInput(false)
        val b = new BinaryInput(false)
        val out = new BinaryOutput()
        val circuit = new Circuit()
    }

    trait OrPrepare extends Prepare with mutable.Before {
        val or = new Or(2)
        circuit.addWire(a, 0, or, 0)
        circuit.addWire(b, 0, or, 1)
        circuit.addWire(or, out, 0)
        def before = {}
    }
    class OrSpec extends mutable.Specification {
        "The Or gate" should {
            "be false if all values are false" in new OrPrepare {
                circuit.step()
                out.compute must beEqualTo(false)
            }
            "be true if any value is true" in new OrPrepare {
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
    }

    trait AndPrepare extends Prepare with mutable.Before {
        val and = new And(2)
        circuit.addWire(a, 0, and, 0)
        circuit.addWire(b, 0, and, 1)
        circuit.addWire(and, out, 0)
        def before = {}
    }
    class AndSpec extends mutable.Specification {
        "The And gate" should {
            "be false if any value is false" in new AndPrepare {
                circuit.step()
                out.compute must beEqualTo(false)
            }
            "be true if all values are true" in new AndPrepare {
                a.switch()
                circuit.step()
                out.compute must beEqualTo(false)
                b.switch()
                circuit.step()
                out.compute must beEqualTo(true)
                a.switch()
                circuit.step()
                out.compute must beEqualTo(false)
            }
        }
    }
    def is = new OrSpec ^ new AndSpec
}
