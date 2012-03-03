import System.getProperty
import sbt._
import Keys._

object Build extends sbt.Build {
    val system = getProperty("os.name")
    val unmanagedListing = unmanagedJars in Compile += {
        if(system == "Linux") Attributed.blank(file("/usr/share/java/swt.jar")) else null
    }
    lazy val lgsis = Project("lgsis", file(".")).settings(unmanagedListing)
}
