.. _bam-file-format:

==========
BAM format
==========

The input/output sequencing files used by **PacBio Data Processing** are BAM
files (see `SAM/BAM format`_ for a description).

The bam file
============

The bam file is is a binary file. It is a compressed version
of a sam file ---that is a human readable format--- containing
all the sequencing information. To manipulate the bam file
format you can use packages like
`pysam <https://pysam.readthedocs.io/en/latest/installation.html>`__
compatible only with python 2 or
`pybam <https://github.com/JohnLonginotto/pybam>`__ for python2 and
`pybam <https://github.com/luidale/pybam>`__ for python 3. However, for
the PacBio bam file Pysam and Pybam are usefull to explore basic fiels
in the aligned PacBio bam file.

PacBio bam file
===============

Compared with the standard
`bam <https://samtools.github.io/hts-specs/SAMv1.pdf>`__ format, the
`PacBio.bam <https://github.com/PacificBiosciences/PacBioFileFormats/blob/3.0/BAM.rst>`__
have extra columns as those containing the Interpulse Duration (IPD)
value and Pulse Width (PW) that are important for the kinetic analysis.

The bam file of the main PacBio output (filename.subreads.bam) contains
26 columns which can be inspected using ``samtools``. For instance, the
following ``shell`` command tells us the number of columns in a bam file:

.. prompt:: bash

   samtools view filename.subreads.bam|awk -F'\t' '{print NF; exit}'

In the next table, the most important columns in a PacBio bam are
described:

+--------------------------+--------------------------+-----------------+
| Column number            | Tag or content           | Description     |
+==========================+==========================+=================+
| 1                        | Molecule identifier      | Molecule        |
|                          |                          | indentifier     |
|                          |                          | containing      |
|                          |                          | {movieName}/    |
|                          |                          | {holeNumber}/   |
|                          |                          | {qStart}_{qEnd} |
+--------------------------+--------------------------+-----------------+
| 10                       | …AGTAC…                  | Sequence        |
+--------------------------+--------------------------+-----------------+
| 11                       | …~~C!~…                  | QUAL            |
+--------------------------+--------------------------+-----------------+
| 12                       | RG                       | ReadGroup       |
+--------------------------+--------------------------+-----------------+
| 13                       | dq                       | DeletionQV      |
+--------------------------+--------------------------+-----------------+
| 14                       | dt                       | DeletionTag     |
+--------------------------+--------------------------+-----------------+
| 15                       | ip                       | Ipd: B,C or B,S |
|                          |                          | (raw frames or  |
|                          |                          | codec V1)       |
+--------------------------+--------------------------+-----------------+
| 16                       | iq                       | InsertionQv     |
+--------------------------+--------------------------+-----------------+
| 17                       | mq                       | MergeQv         |
+--------------------------+--------------------------+-----------------+
| 18                       | np                       | NumPasses       |
+--------------------------+--------------------------+-----------------+
| 19                       | pw                       | PulseWith: B,C  |
|                          |                          | or B,S (raw     |
|                          |                          | frames or codec |
|                          |                          | V1)             |
+--------------------------+--------------------------+-----------------+
| 20                       | qe                       | 0_based end     |
+--------------------------+--------------------------+-----------------+
| 21                       | qs                       | 0_based start   |
+--------------------------+--------------------------+-----------------+
| 22                       | rq                       | Float in [0,1]  |
|                          |                          | encoding        |
|                          |                          | expected        |
|                          |                          | accuracy        |
+--------------------------+--------------------------+-----------------+
| 23                       | sn                       | 4 floats for    |
|                          |                          | the average     |
|                          |                          | signal-to-noise |
|                          |                          | ratio of A,C,G, |
|                          |                          | and T (in that  |
|                          |                          | order) over the |
|                          |                          | HQ region       |
+--------------------------+--------------------------+-----------------+
| 24                       | sq                       | SubstitutionQV  |
+--------------------------+--------------------------+-----------------+
| 25                       | zm                       | ZNW hole number |
+--------------------------+--------------------------+-----------------+
| 26                       | cx                       | Subread local   |
|                          |                          | context flags   |
+--------------------------+--------------------------+-----------------+

If you want to check the differents length of the subreads using command
line, you can type:

.. prompt:: bash

   samtools view filename.subreads.bam|awk '{print length ($10)}'|sort -nur

For more information see the following link: `BAM format specification
for
PacBio <https://github.com/PacificBiosciences/PacBioFileFormats/blob/3.0/BAM.rst>`__

.. _aligned-PacBio-bam-file:

Aligned PacBio bam file
=======================

The aligned bam file of the main PacBio output (moviename.subreads.bam)
contains 28 columns. Again, the next ``shell`` one-liner counts the
columns in the bam:

.. prompt:: bash

   samtools view moviename.subreads.bam|awk -F'\t''{print NF; exit}'

It follows a brief description of the most important columns:

+--------------------------+--------------------------+-----------------+
| Column number            | Tag or content           | Description     |
+==========================+==========================+=================+
| 1                        | Molecule identifier      | Molecule        |
|                          |                          | indentifier     |
|                          |                          | containing      |
|                          |                          | {movieName}/    |
|                          |                          | {holeNumber}/   |
|                          |                          | {qStart}_{qEnd} |
+--------------------------+--------------------------+-----------------+
| 2                        | mapping flag             | Value related   |
|                          |                          | to the          |
|                          |                          | alignment type  |
|                          |                          | (forward strand |
|                          |                          | (0) and reverse |
|                          |                          | strand (16) are |
|                          |                          | the most        |
|                          |                          | important. More |
|                          |                          | details in the  |
|                          |                          | link ‘’Map      |
|                          |                          | Format          |
|                          |                          | Specification’’ |
|                          |                          | below)          |
+--------------------------+--------------------------+-----------------+
| 4                        | position                 | Position where  |
|                          |                          | the sequence    |
|                          |                          | was mapped      |
+--------------------------+--------------------------+-----------------+
| 5                        | mapping quality          | Quality of the  |
|                          |                          | mapping         |
+--------------------------+--------------------------+-----------------+
| 10                       | …AGTAC…                  | Sequence        |
+--------------------------+--------------------------+-----------------+
| 11                       | …~~C!~…                  | QUAL            |
+--------------------------+--------------------------+-----------------+
| 12                       | RG                       | ReadGroup       |
+--------------------------+--------------------------+-----------------+
| 13                       | dq                       | DeletionQV      |
+--------------------------+--------------------------+-----------------+
| 14                       | dt                       | DeletionTag     |
+--------------------------+--------------------------+-----------------+
| 15                       | ip                       | Ipd: B,C or B,S |
|                          |                          | (raw frames or  |
|                          |                          | codec V1)       |
+--------------------------+--------------------------+-----------------+
| 16                       | iq                       | InsertionQv     |
+--------------------------+--------------------------+-----------------+
| 17                       | mq                       | MergeQv         |
+--------------------------+--------------------------+-----------------+
| 18                       | np                       | NumPasses       |
+--------------------------+--------------------------+-----------------+
| 19                       | pw                       | PulseWith: B,C  |
|                          |                          | or B,S (raw     |
|                          |                          | frames or codec |
|                          |                          | V1)             |
+--------------------------+--------------------------+-----------------+
| 20                       | qe                       | 0_based end     |
+--------------------------+--------------------------+-----------------+
| 21                       | qs                       | 0_based start   |
+--------------------------+--------------------------+-----------------+
| 22                       | rq                       | Float in [0,1]  |
|                          |                          | encoding        |
|                          |                          | expected        |
|                          |                          | accuracy        |
+--------------------------+--------------------------+-----------------+
| 23                       | sn                       | 4 floats for    |
|                          |                          | the average     |
|                          |                          | signal-to-noise |
|                          |                          | ratio of A,C,G, |
|                          |                          | and T (in that  |
|                          |                          | order) over the |
|                          |                          | HQ region       |
+--------------------------+--------------------------+-----------------+
| 24                       | sq                       | SubstitutionQV  |
+--------------------------+--------------------------+-----------------+
| 25                       | zm                       | ZNW hole number |
+--------------------------+--------------------------+-----------------+
| 26                       | cx                       | Subread local   |
|                          |                          | context flags   |
+--------------------------+--------------------------+-----------------+
| 27                       | AS                       | Alignment score |
|                          |                          | generated by    |
|                          |                          | aligner         |
+--------------------------+--------------------------+-----------------+
| 28                       | NM                       | Number of       |
|                          |                          | differences     |
|                          |                          | (mismatches     |
|                          |                          | plus inserted   |
|                          |                          | and deleted     |
|                          |                          | bases) between  |
|                          |                          | the sequence    |
|                          |                          | and reference   |
+--------------------------+--------------------------+-----------------+

For more information:

* `Sequence Alignment/Map Format Specification <https://samtools.github.io/hts-specs/SAMv1.pdf>`__
* `Sequence Alignment/Map Optional Fields Specification <https://samtools.github.io/hts-specs/SAMtags.pdf>`__


Fields
======

In this section we give details on some particular fields (columns)
in a bam file.

Quailty of sequencing
---------------------

In the `SAM/BAM format`_ specification it is declared that the 11-th
column in the alignment section of BAM files is named ``QUAL``, and
it is described like follows:

  (brief description) ASCII of Phred-scaled base QUALity+33

  QUAL: ASCII of base QUALity plus 33 (same as the quality string in the
  Sanger FASTQ format). A base quality is the phred-scaled base error
  probability which equals -10 log10 Pr{base is wrong}. This field can
  be a ‘\*’ when quality is not stored. If not a ‘\*’, SEQ must not be a
  ‘\*’ and the length of the quality string ought to equal the length of SEQ.

And the `Wikipedia (FASTQ)`_ explains:

  The byte representing quality runs from ``0x21`` (lowest quality; ``!`` in
  ASCII) to ``0x7e`` (highest quality; ``~`` in ASCII). Here are the quality
  value characters in left-to-right increasing order of quality (ASCII)::

    !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~

For example, each base in a sequence like (in the 10-th column of a BAM
file)::

  AATGCTAGCTAGCTCCTTGGATCGATCCGAT

will have an ASCII symbol (between ``!`` and ``~``) associated with it
that will be the contents of the 11-th column in the BAM file. For
instance::

  ~~~~i~l~~~~_~~~~Z~~~~~~~~~~~~~~

Each symbol tells us the quality of sequencing *the corresponding base*.

Since the ASCII symbols ``!`` and ``~`` correspond to ``33`` and
``126`` in decimal (or ``0x21`` and ``0x7e`` in hexadecimal), and since
each quality value is shifted by ``33`` it means that the range
of allowed qualities, ``[0, 93]``, corresponds to a range of allowed
probabilities for each base being wrong of, roughly ``[1, 0.00005]``
(beware the scale).


.. _`SAM/BAM format`: https://github.com/samtools/hts-specs
.. _`Wikipedia (FASTQ)`: https://en.wikipedia.org/wiki/FASTQ_format
