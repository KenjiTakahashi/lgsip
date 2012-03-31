package lgsis

import engine.gates.{BinaryInput, BinaryOutput, And}
import com.coconut_palm_software.xscalawt.XScalaWT._ // just checking if we really have XS(cala)WT
import org.eclipse.swt.SWT // and SWT itself

object Placeholder {
    def main(args: Array[String]) = {
        val bi = new BinaryInput(true)
        val bi2 = new BinaryInput(false)
        val bo = new BinaryOutput()
        val and = new And(2)
        bi.addWire(and, 0)
        bi2.addWire(and, 1)
        and.addWire(bo, 0)
        println(bi.compute)
        println(bi2.compute)
        println(and.compute)
        println(bo.compute)
    }
}
