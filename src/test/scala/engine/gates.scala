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

    trait NandPrepare extends Prepare with mutable.Before {
        val nand = new Nand(2)
        circuit.addWire(a, 0, nand, 0)
        circuit.addWire(b, 0, nand, 1)
        circuit.addWire(nand, out, 0)
        def before = {}
    }
    class NandSpec extends mutable.Specification {
        "The Nand gate" should {
            "be false if any value is true" in new NandPrepare {
                a.switch()
                circuit.step()
                out.compute should beEqualTo(false)
                b.switch()
                circuit.step()
                out.compute should beEqualTo(false)
                a.switch()
                circuit.step()
                out.compute should beEqualTo(false)
            }
            "be true if all values are false" in new NandPrepare {
                circuit.step()
                out.compute should beEqualTo(true)
            }
        }
    }

    trait NorPrepare extends Prepare with mutable.Before {
        val nor = new Nor(2)
        circuit.addWire(a, 0, nor, 0)
        circuit.addWire(b, 0, nor, 1)
        circuit.addWire(nor, out, 0)
        def before = {}
    }
    class NorSpec extends mutable.Specification {
        "The Nor gate" should {
            "be true if all values are false" in new NorPrepare {
                circuit.step()
                out.compute should beEqualTo(true)
            }
            "be false if any value is true" in new NorPrepare {
                a.switch()
                circuit.step()
                out.compute should beEqualTo(false)
                b.switch()
                circuit.step()
                out.compute should beEqualTo(false)
                a.switch()
                circuit.step()
                out.compute should beEqualTo(false)
            }
        }
    }

    trait XorPrepare extends Prepare with mutable.Before {
        val xor = new Xor()
        circuit.addWire(a, 0, xor, 0)
        circuit.addWire(b, 0, xor, 1)
        circuit.addWire(xor, out, 0)
        def before = {}
    }
    class XorSpec extends mutable.Specification {
        "The Xor gate" should {
            "be false if both values are false" in new XorPrepare {
                circuit.step()
                out.compute should beEqualTo(false)
            }
            "be false if both values are true" in new XorPrepare {
                a.switch()
                b.switch()
                circuit.step()
                out.compute should beEqualTo(false)
            }
            "be true if one value is true and the other is false" in new XorPrepare {
                a.switch()
                circuit.step()
                out.compute should beEqualTo(true)
                a.switch()
                b.switch()
                out.compute should beEqualTo(true)
            }
        }
    }

    trait XnorPrepare extends Prepare with mutable.Before {
        var xnor = new Xnor()
        circuit.addWire(a, 0, xnor, 0)
        circuit.addWire(b, 0, xnor, 1)
        circuit.addWire(xnor, out, 0)
        def before = {}
    }
    class XnorSpec extends mutable.Specification {
        "The Xnor gate" should {
            "be true if both values are false" in new XnorPrepare {
                circuit.step()
                out.compute should beEqualTo(true)
            }
            "be true if both values are true" in new XnorPrepare {
                a.switch()
                b.switch()
                circuit.step()
                out.compute should beEqualTo(true)
            }
            "be false if one value in true and the other is false" in new XnorPrepare {
                a.switch()
                circuit.step()
                out.compute should beEqualTo(false)
                a.switch()
                b.switch()
                circuit.step()
                out.compute should beEqualTo(false)
            }
        }
    }

    trait NotPrepare extends Prepare with mutable.Before {
        var not = new Not()
        circuit.addWire(a, 0, not, 0)
        circuit.addWire(not, out, 0)
        def before = {}
    }
    class NotSpec extends mutable.Specification {
        "The Not gate" should {
            "be true if value is false" in new NotPrepare {
                circuit.step()
                out.compute should beEqualTo(true)
            }
            "be false if value is true" in new NotPrepare {
                a.switch()
                circuit.step()
                out.compute should beEqualTo(false)
            }
        }
    }

    def is = new OrSpec ^ new AndSpec ^ new NandSpec ^ new NorSpec
}
