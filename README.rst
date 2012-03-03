COMPILATION
===========
It uses SBT_ for compilation purposes.
On linux just "sbt compile" and/or "sbt run" and you should be set.
On Windows/OS X see `this page`_.

.. _SBT: https://github.com/harrah/xsbt
.. _this page: https://github.com/harrah/xsbt/wiki/Getting-Started-Setup

SWT
===
On Linux it will use global SWT from "/usr/share/java", for other systems you have to provide adequate swt.jar file (can be downloaded here_) and put it into lib/ directory before compilation.

.. _here: http://download.eclipse.org/eclipse/downloads/drops/R-3.7.2-201202080800/index.php#SWT
