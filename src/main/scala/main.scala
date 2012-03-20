package main.scala

import System.getProperty
import com.coconut_palm_software.xscalawt.XScalaWT._ // just checking if we really have XS(cala)WT
import org.eclipse.swt.SWT // and SWT itself

object Placeholder {
    def main(args: Array[String]) : Unit = {
        println(getProperty("os.name"))
    }
}
