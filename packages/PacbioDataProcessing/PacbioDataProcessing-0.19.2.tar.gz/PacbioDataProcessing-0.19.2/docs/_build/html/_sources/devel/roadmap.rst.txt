*******
Roadmap
*******

The roadmap is a summary of planned changes. It is splitted into two parts:

* :ref:`Future`
* :ref:`Past`

The difference between :ref:`Past` and the :ref:`CHANGELOG` is the point of view:
:ref:`CHANGELOG` is intended for *end users* whereas :ref:`Past` is mainly for
developers.


.. _Future:

Future
======

0.20.0
------

* [R14] Resume interrupted ``sm-analysis`` runs.

  * can provide the name of the temporary directory
  * can identify what molecules have been already processed and skips
    them (issue #17)


0.21.0
------

* [R24] Path to ``ccs`` can be provided as CLO.


0.22.0
------

* [R25] Documentation (II)

    * local distribution and installation of docs
    * launch local docs in browser
    * tutorial
    * structural refinaments
    * man page


1.0.0
-----

* [R16] Transparent usage of clusters. (?)
* [R08] Decouple from ipdSummary using kineticsTools as a package (?)
* [R26] BamFile implementation using pure python library ``pybam`` (or a
  python3 compliant fork of it)
* [R10] BAM files created contain info about source file and modifications
  introduced.
* Issues & bugs


1.1.0
-----

* [R23] New option that disables the standard filters before
  running the Single Molecule Analysis (``sm-analysis``)


1.2.0
-----

* [R18] Easy installation (after [R26])


.. _Past:

Past
====

0.19.0
------

* Issues: #14, #15, #58, #64, #67, #77


0.18.0
------

* [R22] Summary doc for humans (in HTML) with:

  * plots
  * basic statistics about subreads, molecules, methylations, etc.

* Issues: #59, #61, #62


0.17.0
------

* Issues: #43, #38, #54, #45


0.16.0
------

* [R17] GUI
* Issues: #44, #46, #47, #3


0.15.0
------

* [R02] ``samtools`` replaced by ``pysam``
* merge to master branch
* Issues #10, #27 and #36 fixed


0.14.0
------

* Issue #19
* [R20] Documentation.

  * Structure documentation
  * Add quick start and some more docs for end users
  * add docstrings as a starting point of docs for developers
  * integrate with sphinx


0.13.0
------

* [R21] Methylation report format V3
* pipelines (?)
* Issue #16, #28, #29, #5
* Code follows style guide (flake8)


0.12.0
------

* [R15] Various minor input options:

  * modification types
  * keep temporary directory
  * only produce methylation report
  * ccs file
  * aligned ccs file

* Issue #2


0.11.0
------

* [R03] Add option ``--partition`` to ``sm-analysis`` to select what fraction of an input
  file must be processed


0.10.0
------

* [R13] Number of processes used by external tools can be chosen.


0.9.0
-----

* [R19] Methylation state conforms to version 2 (see
  :ref:`methylation-report-format`).


0.8.0
-----

* [R12] Path to external tools can be provided:

  * ``blasr``
  * ``pbindex``
  * ``ipdSummary``


0.7.0
-----

* [R09] Automatically identify structure of BAM file:

  * where the molecule id is located (column)

* [R05] Option to select model in ``sm-analysis``


0.6.0
-----

Miscelaneous improvements:

  * protection against tracebacks (they should not be presented to end user)
  * version
  * debugging messages
  * More user friendly output of ``sm-analysis`` (with relevant key infos)


0.5.0
-----

* [R06] *legacy code* covered with tests: minimal ``sm-analysis`` functionality
* [R04] Implement new ``csv`` output with methilation state per molecule and circular
  consensus DNA sequence


0.4.0
-----

* [R01] ``bam-filter``: convert *legacy code* into *production* code

  * use the FTs to *define* what the code does, and
  * cover the existing code with UTs

