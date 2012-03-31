package lgsis

import engine.gates.basic._
import engine.gates.io._
import com.coconut_palm_software.xscalawt.XScalaWT._ // just checking if we really have XS(cala)WT
import org.eclipse.swt.SWT // and SWT itself

object Main {
    def main(args: Array[String]) = {
        val bi = new BinaryInput(true)
        val bi2 = new BinaryInput(true)
        val bi3 = new BinaryInput(false)
        val bi4 = new BinaryInput(false)
        val bo = new BinaryOutput()
        val and = new And(2)
        val or = new Or(2)
        bi.addWire(and, 0)
        bi2.addWire(or, 0)
        bi4.addWire(or, 1)
        or.addWire(and, 1)
        and.addWire(bo, 0)
        println(and.compute)
        println(or.compute)
        println(bo.compute)
    }
}
