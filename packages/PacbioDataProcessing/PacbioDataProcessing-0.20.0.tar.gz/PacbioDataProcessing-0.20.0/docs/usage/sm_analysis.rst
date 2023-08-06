.. highlight:: shell

.. _sm-analysis:

Single molecule analysis
========================

``sm-analysis``
---------------

``sm-analysis`` is the main program provided by |project|. It analyzes a
given input BAM file evaluating the methylation status of *each molecule*.

``sm-analysis`` expects a PacBio BAM file as input and the corresponding
``fasta`` file containing the reference. One of the first things that
the program will do is to ensure that this input BAM is aligned. Actually
two alignment processes will be carried out with the help of
:ref:`blasr` : a *straight* alignment and another alignment with a rotated
reference, the so-called *pi shifted* alignment, where the origin of the
reference is rotated by 180 degrees. The aim of this second alignment
process is to catch molecules that cross the origin with the help of those
two files.

Before running :ref:`blasr` the program will try to find the two aligned
versions of the input file, *if it is* unaligned.

On the other hand, if the input file is actually aligned, a *pi shifted*
version of it will be sought. And if found, it will be used.

If only a *straight* aligned file is at hand, the circular topology of the
reference will not be considered.

To find the aligned versions of the input BAM, the program tries to answer
three questions:

1. Is there a candidate with the expected filename?
2. Is the candidate aligned?
3. Are the molecules in it a subset of the molecules in the input BAM?

If the answer to the three questions is yes, the candidate is considered
a *plausible aligned version* of the input BAM, and it is as such used
within the rest of the analysis. If not, the alignment process is carried
out.

WIP: comments on CCS files...


Command line options
^^^^^^^^^^^^^^^^^^^^

The program has a `Command Line Interface (CLI)`_ with the
following options:

  .. prompt:: bash

  $ sm-analysis -h
  usage: sm-analysis [-h] [-M MODEL] [-b PATH] [-p PATH] [-i PATH] [-N NUM] [-n NUM] [--nprocs-blasr NUM] [-P PARTITION:NUMBER-OF-PARTITIONS] [-C BAM-FILE] [-c BAM-FILE]
  [--keep-temp-dir] [-m MOD-TYPE [MOD-TYPE ...]] [--only-produce-methylation-report] [-v] [--version]
  BAM-FILE ALIGNMENT-FILE

  Single Molecule Analysis. This program splits a BAM into 'molecules', aligns them individually with blasr (if wanted), generates indices and processes each molecule thru
  ipdSummary producing a joined gff file, a csv file with columns: molecule name, ?, ?, ?, ?, ...and a so-called methylation report. For this last part an aligned CCS BAM
  file is required. It can be passed in the command line or produced with the aligner from the CCS BAM file. If the CCS BAM file is not found --or not given--, it will be
  tried to be produced using 'ccs'.

  positional arguments:
  BAM-FILE              input file in BAM format
  ALIGNMENT-FILE        input file containing the alignment in FASTA format (typically a file ending in '.fa' or '.fasta'). A '.fai' file ('ALIGNMENT-FILE.fai') is also
  expected to be found side-by-side to ALIGNMENT-FILE.

  optional arguments:
  -h, --help            show this help message and exit
  -M MODEL, --ipd-model MODEL
                        model to be used by ipdSummary to identify the type of modification. MODEL must be either the model name or the path to the ipd model. First, the
  program will make an attempt to interprete MODEL as a path to a file defining a model; if that fails, MODEL will be understood to be the name of
  a model that must be accessible in the resources directory of kineticsTools (e.g. '-M SP3-C3' would trigger a search for a file called
  'SP3-C3.npz.gz' within the directory with models provided by kineticsTools). If this option is not given, the default model in ipdSummary is
  used.
  -b PATH, --blasr-path PATH
                        path to blasr program (default: 'blasr')
  -p PATH, --pbindex-path PATH
                        path to pbindex program (default: 'pbindex')
  -i PATH, --ipdsummary-path PATH
                        path to ipdSummary program (default: 'ipdSummary')
  -N NUM, --num-simultaneous-ipdsummarys NUM
                        number of simultaneous instances of ipdSummary that will cooperate to process the molecules (default: 1)
  -n NUM, --num-workers-per-ipdsummary NUM
                        number of worker processes that each instance of ipdSummary will spawn (default: 1)
  --nprocs-blasr NUM    number of worker processes that each instance of blasr will spawn (default: 1)
  -P PARTITION:NUMBER-OF-PARTITIONS, --partition PARTITION:NUMBER-OF-PARTITIONS
                        this option instructs the program to only analyze a fraction (partition) of the molecules present in the input bam file. The file is divided in
                        `NUMBER OF PARTITIONS` (almost) equal pieces but ONLY the PARTITION-th partition (fraction) is analyzed. For instance, `--partition 3:7` means
                        that the bam file is divided in seven pieces but only the third piece is analyzed (by default all the file is analyzed)
  -C BAM-FILE, --aligned-CCS-bam-file BAM-FILE
                        aligned CCS file in BAM format used to produce a report of methylation states. If provided, it is used in the production of the methylation
                        states report. If missing, one is generated from the CCS file using 'blasr'
  -c BAM-FILE, --CCS-bam-file BAM-FILE
                        CCS file in BAM format used to produce a report of methylation states. If provided, and the aligned version of it is not provided, it is aligned
                        and the result is used in the production of the methylation states report. If missing, one is generated from the original BAM file using the
                       'ccs' program
  --keep-temp-dir       should we make a copy of the temporary files generated? (default: False)
  -m MOD-TYPE [MOD-TYPE ...], --modification-types MOD-TYPE [MOD-TYPE ...]
                        focus only in the requested modification types (default: ['m6A'])
  --only-produce-methylation-report
                        use this flag to only produce the methylation report from the per detection csv file (default: False)
  -v, --verbose
  --version             show program's version number and exit


.. _`Command Line Interface (CLI)`: https://en.wikipedia.org/wiki/Command-line_interface


Graphical User Interface: ``sm-analysis-gui``
---------------------------------------------

Despite the power, beauty and *vintage* flavor of the command line, |project| offers
a `Graphical User Interface (GUI)`_ for its main executable ``sm-analysis``:
``sm-analysis-gui`` which, upon execution, will open a window that will allow
you to drive the single molecule analysis.


.. _`Graphical User Interface (GUI)`: https://en.wikipedia.org/wiki/Graphical_user_interface
