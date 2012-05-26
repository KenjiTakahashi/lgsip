import System.getProperty
import sbt._
import Keys._

object Build extends sbt.Build {
    val system = getProperty("os.name")
    var lgsis = Project("lgsis", file("."))
    if(system == "Linux") {
        val unmanagedListing = unmanagedJars in Compile += {
            Attributed.blank(file("/usr/share/java/swt.jar"))
        }
        lgsis = lgsis.settings(unmanagedListing)
    }
}
