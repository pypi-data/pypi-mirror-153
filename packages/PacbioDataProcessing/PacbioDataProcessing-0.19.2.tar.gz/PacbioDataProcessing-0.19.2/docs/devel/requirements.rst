************
Requirements
************

A list of features to be added to the package. Requirements marked with a ``(*)``
are not yet assigned a version number.


[R01]
  ``bam-filter`` covered with tests

[R02]
  ``samtools`` replaced by ``pysam``

[R03]
  Add option ``--partition`` to ``sm-analysis`` to select what fraction of an input
  file must be processed

[R04]
  Implement new ``csv`` output with methilation state per molecule and circular
  consensus DNA sequence

[R05]
  Option to select model in ``sm-analysis`` (simply providing a string, eg ``P6-C4``).
  Instead of crashing if the expected model dows not agree with the chemistry, the
  program looks for different models in the directory and tests them in turn until
  a valid one is found.

[R06]
  *Legacy code* covered with tests: minimal ``sm-analysis`` functionality
  
[R07]
  Optimization: Reduce the number of temporary files that are created
  by ``sm-analysis``.

[R08]
  Decouple from ipdSummary using kineticsTools as a package

[R09]
  Automatically identify structure of BAM file:

  * where the molecule id is located (column)
    
[R10]
  BAM files created contain info about source file and modifications introduced.

[R11]
  Miscelaneous improvements:

  * protection against tracebacks (they should not be presented to end user)
  * version
  * debugging

[R12]
  Path to external tools can be provided:

  * ``blasr``
  * ``pbindex``
  * ``ipdSummary``

[R13]
  Number of processes used by external tools can be chosen.

[R14]
  Resume interrupted ``sm-analysis`` runs.

[R15]
  Various minor input options:

  * modification types
  * keep temporary directory?
  * only produce methylation report
  * ccs file
  * aligned ccs file

[R16]
  Transparent usage of clusters.

[R17]
  GUI

[R18]
  Easy installation

[R19]
  Methylation state conforms to version 2 (see :ref:`methylation-report-format`).

[R20]
  Documentation (I)

    * Structure documentation
    * Add quick start and some more docs for end users
    * add docstrings as a starting point for docs for developers
    * integrate with sphinx

[R21]
  Methylation report format V3

[R22]
  Summary doc for humans (html?, pdf?) with:

  * plots
  * basic statistics about subreads, molecules, methylations, etc.

[R23]
  New option that disables the standard filters before
  running the Single Molecule Analysis (``sm-analysis``)

[R24]
  Path to ``ccs`` can be provided as CLO.

[R25]
  Documentation (II)

    * local distribution and installation of docs
    * launch local docs in browser

[R26]
  BamFile implementation using pure python library ``pybam`` (or a
  python3 compliant fork of it)

[R27]
  Organization of files produced by ``sm-analysis``:

    * log files go to a dedicated ``log/`` directory (each molecule
      must have its onw log file)
    * auxiliary files (``ì-shifted...``, aligned BAMs, CCS, etc)
      must go into a dedicated directory (``aux/``?)

[R28]
  Browsable HTML document with information about status of individual
  GATCs and the neighbours.
