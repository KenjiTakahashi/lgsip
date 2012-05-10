package lgsis

import engine.gates.basic._
import engine.gates.io._
import engine.Circuit
import com.coconut_palm_software.xscalawt.XScalaWT._ // just checking if we really have XS(cala)WT
import org.eclipse.swt.SWT // and SWT itself
import com.scaladudes.signal.stopDispatcher

object Main extends App {
        val circuit = new Circuit()
        val i1 = new BinaryInput(true)
        val i2 = new BinaryInput(true)
        val i3 = new BinaryInput(true)
        val i4 = new BinaryInput(true)
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
    circuit.step()
    circuit.step()
    circuit.step()
    circuit.step()
    circuit.step()
    circuit.step()
    println(o1.compute)
    println(o2.compute)
    stopDispatcher()
}
