package lgsis

import engine.gates.basic._
import engine.gates.io._
import engine.Circuit
import com.coconut_palm_software.xscalawt.XScalaWT._ // just checking if we really have XS(cala)WT
import org.eclipse.swt.SWT // and SWT itself
import com.scaladudes.signal.stopDispatcher

object Main extends App {
    val a=new BinaryInput(false)
    val b=new BinaryInput(false)
    val c=new Circuit()
    val o=new BinaryOutput()
    val or=new Or(2)
    c.addWire(a, 0, or, 0)
    c.addWire(b, 0, or, 1)
    c.addWire(or, o, 0)
    c.step()
    println(o.compute)
    a.switch()
    c.step()
    println(a.compute)
    println(b.compute)
    println(o.compute)
    b.switch()
    c.step()
    println(a.compute)
    println(b.compute)
    println(o.compute)
    a.switch()
    c.step()
    println(a.compute)
    println(b.compute)
    println(o.compute)
    // sth custom
    //val b1 = new BinaryInput(true)
    //val b2 = new BinaryInput(true)
    //val and = new And(2)
    //val bo = new BinaryOutput()
    //b1.addWire(and, 0)
    //b2.addWire(and, 1)
    //and.addWire(bo, 0)
    //println(bo.compute)
    //// S-R latch
    //val s = new BinaryInput(true)
    //val r = new BinaryInput(false)
    //val nor1 = new Nor(2)
    //val nor2 = new Nor(2)
    //val q = new BinaryOutput()
    //val nq = new BinaryOutput()
    //s.addWire(nor1, 0)
    //r.addWire(nor2, 0)
    //nor1.addWire(nor2, 1)
    //nor2.addWire(nor1, 1)
    //nor1.addWire(q, 0)
    //nor2.addWire(nq, 0)
    //println(q.compute)
    //println(nq.compute)
    // J-K flip-flop (with faked clock)
    //val j = new BinaryInput(false)
    //val k = new BinaryInput(false)
    //val c = new BinaryInput(false)
    //val and1 = new And(3)
    //val and2 = new And(3)
    //val nor11 = new Nor(2)
    //val nor21 = new Nor(2)
    //val jkq = new BinaryOutput()
    //val jknq = new BinaryOutput()
    //j.addWire(and1, 0)
    //k.addWire(and2, 0)
    //c.addWire(and1, 1)
    //c.addWire(and2, 1)
    //and1.addWire(nor11, 0)
    //and2.addWire(nor21, 0)
    //nor11.addWire(nor21, 1)
    //nor11.addWire(and1, 2)
    //nor21.addWire(nor11, 1)
    //nor21.addWire(and2, 2)
    //nor11.addWire(jkq, 0)
    //nor21.addWire(jknq, 0)
    //val circ = new Circuit()
    //circ.addWire(j, 0, and1, 0)
    //circ.addWire(k, 0, and2, 0)
    //circ.addWire(c, 0, and1, 1)
    //circ.addWire(c, 0, and2, 1)
    //circ.addWire(and1, nor11, 0)
    //circ.addWire(and2, nor21, 0)
    //circ.addWire(nor11, nor21, 1)
    //circ.addWire(nor11, and1, 2)
    //circ.addWire(nor21, nor11, 1)
    //circ.addWire(nor21, and2, 2)
    //circ.addWire(nor11, jkq, 0)
    //circ.addWire(nor21, jknq, 0)
    //j.switch()
    //k.switch()
    //c.switch()
    //circ.start()
    //println(j.compute)
    //println(k.compute)
    //println(c.compute)
    //println(and1.compute)
    //println(and2.compute)
    //println(nor11.compute)
    //println(nor21.compute)
    //println(jkq.compute)
    //println(jknq.compute)
    //println("-")
    //import java.lang.Thread
    //Thread.sleep(100)
    ////circ ! Step
    //println(and1.compute)
    //println(and2.compute)
    //println(nor11.compute)
    //println(nor21.compute)
    //println(jkq.compute)
    //println(jknq.compute)
    //println("-")
    //import java.lang.Thread
    //Thread.sleep(100)
    //println(and1.compute)
    //println(and2.compute)
    //println(nor11.compute)
    //println(nor21.compute)
    //println(jkq.compute)
    //println(jknq.compute)
    //println("-")
    //println(and1.compute)
    //println(and2.compute)
    //println(nor11.compute)
    //println(nor21.compute)
    //println(jkq.compute)
    //println(jknq.compute)
    //println("-")
    //println(and1.compute)
    //println(and2.compute)
    //println(nor11.compute)
    //println(nor21.compute)
    //println(jkq.compute)
    //println(jknq.compute)
    //println("-")
    //println(and1.compute)
    //println(and2.compute)
    //println(nor11.compute)
    //println(nor21.compute)
    //println(jkq.compute)
    //println(jknq.compute)
    //println("-")
    //println(and1.compute)
    //println(and2.compute)
    //println(nor11.compute)
    //println(nor21.compute)
    //println(jkq.compute)
    //println(jknq.compute)
    //println("-")
    ////circ ! Stop
    //circ.die()
    stopDispatcher()
}
