.. _changelog:

Changelog
=========


Version 0.20.0
--------------

* Command line option to provide path to ``ccs`` program.
* Fasta index is created for the original reference if it is missing
  (issue #55)
* Removed runtime dependency on ``setuptools`` (issue #81).


Version 0.19.0
--------------

* ``sm-analysis`` filters out molecules with subreads in only one
  strand (issue #77).
* ``blasr`` and ``ccs`` operations protected by sentinel to prevent
  that parallel computations overwrite the aligned/ccs files (iss. #64).
* Bug fixed in plot with rolling average of coverage
* Issues: #58, #67
* Added Unique ID to each line of output (issue #14)
* Some improvements in the documentation.
* The result of calling external tools is taken into account in the
  pipeline: to inform about a possible error and to omit a faulty
  molecule.


Version 0.18.0
--------------

* Summary report for humans in HTML format with

  * plots, and
  * basic statistics about subreads, molecules, methylations, etc.

* Issues: #59
* Bugfixes: #61, #62, #65


Version 0.17.0
--------------

* The molecules in the methylation report are the ones found
  in the aligned CCS file that pass all the filters (issue #43)
* Circular alignment: it is assumed that the chromosome has a
  circular topology, which is taken into account in the analysis
  (issue #38)
* bugfixes in _BamFilePysam: it was writing spurious newlines
  after the header and between lines in the body.
* Other issues closed: #45, #54


Version 0.16.0
--------------

* GUI for ``sm-analysis``: ``sm-analysis-gui``
* Automatic alignment of unaligned input BAM (issue #44)
* Unpleasant error messages from Pysam suppressed (issue #46)
* Consistent behavior of CCS step in ``sm-analysis`` (
  issues #47 and #3)


Version 0.15.0
--------------

* Calls to external tool ``samtools`` replaced by usage of the ``pysam``
  library
* Issues closed:

  * #10 (methylation report's name shown on screen upon creation)
  * #27 (patitions taken into account in the methylation report)
  * #36 (a standard set of filters integrated into ``sm-analysis``)


Version 0.14.0
--------------

* Issues #32 and #19 fixed
* Added systematic documentation


Version 0.13.0
--------------

* Methylation report V3, with

  * quality columns
  * length of (DNA) molecule
  * column with number of methylations
  * columns with number of subreads per strand per molecule

* The list of molecules in a methylation report comes from
  the CCS file. Only molecules having the very same sequence
  in the reference and in the CCS are included.
* Some improvements on the developmnet side:

  * code follows style guide (``flake8`` tests pass)
  * pipelines ready

* some issues fixed


Version 0.12.0
--------------

* Added new command line options to ``sm-analysis``:

  * ``-C|--aligned-CCS-bam-file`` to pass an aligned ccs file (that file
    is used to produce the Methylation report)
  * ``-c|--CCS-bam-file`` to pass a ccs file (that file is used to produce
    the Methylation report, after being aligned, if the aligned version
    itself is not provided)
  * ``--keep-temp-dir`` to preserve a copy of the temporary directory
    with all the intermediate files used in the process.
  * ``-m|--modification-types`` to select the modification types (m6A,
    m4C, ...)
  * ``--only-produce-methylation-report`` to skip the analysis itself and
    only perform the last step: production of the methylation report.

* Issue #2 closed


Version 0.11.0
--------------

* Added option ``-P|--partition`` to ``sm-analysis`` to select what fraction
  of an input file must be processed. This change allows for an easy way to
  further parallelize the processing of input files within different nodes
  in a cluster.


Version 0.10.0
--------------

* Bugfix in methylation report
* New command line options for ``sm-analysis``:
  
  * ``-N|--num-simultaneous-ipdsummarys`` to launch multiple instances of
    ipdSummary
  * ``-n|--num-workers-per-ipdsummary`` to use multiple workers within each
    instance of ipdSummary
  * ``--nprocs-blasr`` to use multiple workers with blasr


Version 0.9.0
-------------

* Methylation reports (output by ``sm-analysis``) conform now to V2
  (see :ref:`methylation-report-format`).


Version 0.8.0
-------------

* New command line options for ``sm-analysis`` to choose the path to the

  * aligner (option ``-b|--blasr-path``)
  * indexer (option ``-b|--blasr-path``)
  * ipdSummary (option ``-i|--ipdsummary-path``)

* High level documentation about PacBio sequencing
    

Version 0.7.0
-------------

* ``sm-analysis`` and ``bam-filter`` automatically identify the
  structure of BAM file:

  * where the molecule id is located (column)

* ``sm-analysis`` has option to select the IPD model in ipdSummary
  (option ``-M|--ipd-model``).


Version 0.6.0
-------------

* added option ``--version`` to ``sm-analysis``
* verbosity is configurable (cl option: ``-v|--verbose``)
* no tracebacks should reach the end user, only error messages
* More user friendly output of ``sm-analysis`` (with relevant key infos)


Version 0.5.0
-------------

* *Legacy code* covered with tests: minimal ``sm-analysis`` functionality
* New ``csv`` output with methylation states per GATC


Version 0.4.0
-------------

* Switched to Double-loop TDD approach
* Code for ``bam-filter`` re-organized and covered with tests (most of it)
* some bugs fixed
* spike to parallelize (in node) ``sm-analysis``
  
