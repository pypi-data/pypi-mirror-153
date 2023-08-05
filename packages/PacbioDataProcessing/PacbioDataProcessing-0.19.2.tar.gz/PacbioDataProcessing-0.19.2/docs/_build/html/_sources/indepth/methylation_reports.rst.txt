.. _methylation-report-format:

==============================================
Description of data in the Methylation Reports
==============================================

:Author: David Palao
:Date: 6 May 2021
:Last updated: 13 September 2021
:Version: 3
:Tags: sm-analysis PacbioDataProcessing output methylation
       
:abstract:

   The ``sm-analysis`` pipeline produces a so-called
   *methylation report*. Its contents is described in this
   document.


Format
======

.. note::

   This section describes the most recent version of
   the methylation report's format.

The *methylation report* produced by ``sm-analysis`` is a csv file with ``;``
(semicolon) as separator and **21 columns** with the following header::

  molecule id;sequence;start of molecule;end of molecule;len(molecule);count(subreads+);count(subreads-);combined QUAL;mean(QUAL);sim ratio;count(GATC);positions of GATCs;count(methylation states);methylation states;combined score;mean(score);min(IPDRatio);mean(IPDRatio);combined idQV;mean(idQV);mean(coverage)

Each column can be itself separated (see e.g. columns 12 and 14). In that case
an *internal* separator, namely ``,``, is used.

The following table summarizes the meaning of each column.


+---------+-------------------+-------------------+----------------------------------+-------------+
| col num |   field name      |  possible values  | description                      | example     |
+=========+===================+===================+==================================+=============+
|   1     | ``molecule id``   |   positive int    | value provided by the sequencer  |  23480      |
+---------+-------------------+-------------------+----------------------------------+-------------+
|   2     | ``sequence``      |      [ACGT]*      | DNA sequence corresponding to    | AGACTTTC... |
|         |                   |                   | the molecule, as reported by CCS |             |
+---------+-------------------+-------------------+----------------------------------+-------------+
|   3     | ``start of``      |   positive int    | 1-based start position of the    |    312      |
|         | ``molecule``      |                   | molecule within the reference;   |             |
|         |                   |                   | the values are taken from the    |             |
|         |                   |                   | aligner; this value is the       |             |
|         |                   |                   | number of bases before the first |             |
|         |                   |                   | base of the sequence plus 1      |             |
|         |                   |                   | (the minimum position is 1)      |             |
+---------+-------------------+-------------------+----------------------------------+-------------+
|   4     | ``end of``        |   positive int    | 1-based end position of the      |   1509      |
|         | ``molecule``      |                   | molecule within the reference;   |             |
|         |                   |                   | the values are taken from the    |             |
|         |                   |                   | aligner. This value is the       |             |
|         |                   |                   | number of bases before the last  |             |
|         |                   |                   | base of the sequence plus 1      |             |
+---------+-------------------+-------------------+----------------------------------+-------------+
|   5     | ``len(molecule)`` |  positive int     | length of the DNA sequence       |  1198       |
|         |                   |                   | corresponding to the molecule,   |             |
|         |                   |                   | according to the aligned CCS     |             |
|         |                   |                   | file.                            |             |
+---------+-------------------+-------------------+----------------------------------+-------------+
|   6     | ``count(sub-``    |  int >= 0         | number of subreads in the +      |    51       |
|         | ``reads+)``       |                   | strand found in the input BAM    |             |
+---------+-------------------+-------------------+----------------------------------+-------------+
|   7     | ``count(sub-``    |  int >= 0         | number of subreads in the -      |    48       |
|         | ``reads-)``       |                   | strand found in the input BAM    |             |
+---------+-------------------+-------------------+----------------------------------+-------------+
|   8     | ``combined``      | positive float    | combined *QUAL* (asccii of base  |   95.2      |
|         | ``QUAL``          |                   | quality plus 33). Each QUAL      |             |
|         |                   |                   | is the Phred-transformed proba-  |             |
|         |                   |                   | bility value that the base is    |             |
|         |                   |                   | wrong.                           |             |
+---------+-------------------+-------------------+----------------------------------+-------------+
|   9     | ``mean(QUAL)``    | positive float    | mean *QUAL* (asccii of base      |   101.4     |
|         |                   |                   | quality plus 33). Each QUAL      |             |
|         |                   |                   | is the Phred-transformed proba-  |             |
|         |                   |                   | bility value that the base is    |             |
|         |                   |                   | wrong.                           |             |
+---------+-------------------+-------------------+----------------------------------+-------------+
|  10     | ``sim ratio``     |  float between 0  | ratio of similarity between the  |     1.0     |
|         |                   |  and 1            | molecule's sequence and the      |             |
|         |                   |                   | corresponding piece in the       |             |
|         |                   |                   | reference                        |             |
+---------+-------------------+-------------------+----------------------------------+-------------+
|  11     | ``count(GATC)``   |   positive int    | number of GATCs found in the DNA |      3      |
|         |                   |                   | sequence.                        |             |
+---------+-------------------+-------------------+----------------------------------+-------------+
|  12     | ``positions``     | comma separated   | 1-based absolute positions of    | 315,699,902 |
|         | ``of GATCs``      | sequence of int>0 | the Gs for all the GATCs present |             |
|         |                   |                   | in col 3 (ie, in the current     |             |
|         |                   |                   | molecule)                        |             |
+---------+-------------------+-------------------+----------------------------------+-------------+
|  13     | ``count(methy-``  |  positive int     | in how many positions the mole-  |   2         |
|         | ``lation``        |                   | cule was detected to have a      |             |
|         | ``states)``       |                   | methylation (``+``, ``-`` or     |             |
|         |                   |                   | ``f`` in column 7).              |             |
+---------+-------------------+-------------------+----------------------------------+-------------+
|  14     | ``methylation``   | comma separated   | each element corresponds to the  | f,-,0       |
|         | ``states``        | sequence of [0-+f]| methylation state of one GATC in |             |
|         |                   |                   | the sequence as returned by the  |             |
|         |                   |                   | ``ipdSummary`` program           |             |
+---------+-------------------+-------------------+----------------------------------+-------------+
|  15     | ``combined``      | positive float    | combined *score of the feature*  |  118        |
|         | ``score``         |                   | for each detection (each score   |             |
|         |                   |                   | is the Phred-transformed proba-  |             |
|         |                   |                   | bility value that a kinetic de-  |             |
|         |                   |                   | viation exists at a position)    |             |
+---------+-------------------+-------------------+----------------------------------+-------------+
|  16     | ``mean(score)``   | positive float    | mean *score of the feature*      |  150        |
|         |                   |                   | over all detections in the mole- |             |
|         |                   |                   | cule (each score is the Phred-   |             |
|         |                   |                   | transformed probability value    |             |
|         |                   |                   | that a kinetic deviation exists  |             |
|         |                   |                   | at a position)                   |             |
+---------+-------------------+-------------------+----------------------------------+-------------+
|  17     | ``min(IPDRatio)`` |  positive float   | min of tMean/modelPredictions    |  3.4        |
|         |                   |                   | (tMean is the capped mean of     |             |
|         |                   |                   | normalized IPDs observed at      |             |
|         |                   |                   | this position)                   |             |
+---------+-------------------+-------------------+----------------------------------+-------------+
|  18     | ``mean(IPDRatio)``|  positive float   | mean of tMean/modelPredictions   |  5.2        |
|         |                   |                   | (tMean is the capped mean of     |             |
|         |                   |                   | normalized IPDs observed at      |             |
|         |                   |                   | this position)                   |             |
+---------+-------------------+-------------------+----------------------------------+-------------+
|  19     | ``combined idQV`` |  positive float   | combined ``idQV`` value for all  |  19.6       |
|         |                   |                   | the detected modifications of    |             |
|         |                   |                   | the correct type in the given    |             |
|         |                   |                   | molecule                         |             |
+---------+-------------------+-------------------+----------------------------------+-------------+
|  20     | ``mean(idQV)``    |  positive float   | mean ``idQV`` value for all      |  30         |
|         |                   |                   | the detected modifications of    |             |
|         |                   |                   | the correct type in the given    |             |
|         |                   |                   | molecule                         |             |
+---------+-------------------+-------------------+----------------------------------+-------------+
|  21     | ``mean(coverage)``|  positive float   | mean value of the coverage       |  42         |
|         |                   |                   | levels used to assign the modif. |             |
|         |                   |                   | type label                       |             |
+---------+-------------------+-------------------+----------------------------------+-------------+

Some notes:

- the number of elements in columns 12 and 14 must be equal to the value in column 11
- ``idQV`` is the Phred-transformed QV of having a modification at a given position
- The meaning of the methylation state symbols:

  * ``0``:  not methylated
  * ``-``:  hemi-methylated. Negative strand
  * ``+``:  hemi-methylated. Positive strand
  * ``f``:  full methylated


Format (version 2)
==================

The *methylation report* produced by ``sm-analysis`` is a csv file with ``;``
(semicolon) as separator and **7 columns** with the following header::

  molecule id;count(GATC);sequence;start of molecule;end of molecule;positions of GATCs;methylation states

The following table summarizes the meaning of each column.


+---------+-----------------+-------------------+----------------------------------+--------------+
| col num |   field name    |  possible values  | description                      | example      |
+=========+=================+===================+==================================+==============+
|   1     | ``molecule id`` |   positive int    | value provided by the sequencer  |  23480       |
+---------+-----------------+-------------------+----------------------------------+--------------+
|   2     | ``count(GATC)`` |   positive int    | number of GATCs found in the DNA |      3       |
|         |                 |                   | sequence.                        |              |
+---------+-----------------+-------------------+----------------------------------+--------------+
|   3     | ``sequence``    |      [ACGT]*      | DNA sequence corresponding to    | AGACTTTC...  |
|         |                 |                   | the molecule, as reported by CCS |              |
+---------+-----------------+-------------------+----------------------------------+--------------+
|   4     | ``start of``    |   positive int    | 1-based start position of the    |    312       |
|         | ``molecule``    |                   | molecule within the reference;   |              |
|         |                 |                   | the values are taken from the    |              |
|         |                 |                   | aligner; this value is the       |              |
|         |                 |                   | number of bases before the first |              |
|         |                 |                   | base of the sequence plus 1      |              |
|         |                 |                   | (the minimum position is 1)      |              |
+---------+-----------------+-------------------+----------------------------------+--------------+
|   5     | ``end of``      |   positive int    | 1-based end position of the      |   1509       |
|         | ``molecule``    |                   | molecule within the reference;   |              |
|         |                 |                   | the values are taken from the    |              |
|         |                 |                   | aligner. This value is the       |              |
|         |                 |                   | number of bases before the last  |              |
|         |                 |                   | base of the sequence plus 1      |              |
+---------+-----------------+-------------------+----------------------------------+--------------+
|   6     | ``positions``   | comma separated   | 1-based absolute positions of    | 315,699,1002 |
|         | ``of GATCs``    | sequence of int>0 | the Gs for all the GATCs present |              |
|         |                 |                   | in col 3 (ie, in the current     |              |
|         |                 |                   | molecule)                        |              |
+---------+-----------------+-------------------+----------------------------------+--------------+
|   7     | ``methylation`` | comma separated   | each element corresponds to the  | f,-,0        |
|         | ``states``      | sequence of [0-+f]| methylation state of one GATC in |              |
|         |                 |                   | the sequence as returned by the  |              |
|         |                 |                   | ``ipdSummary`` program           |              |
+---------+-----------------+-------------------+----------------------------------+--------------+

Some notes:

- the number of elements in columns 6 and 7 must be equal to the value in column 2
- The meaning of the methylation state symbols:

  * ``0``:  not methylated
  * ``-``:  hemi-methylated. Negative strand
  * ``+``:  hemi-methylated. Positive strand
  * ``f``:  full methylated


Format (version 1)
==================

.. note::
   This version, v1, is an old format no longer used. It was decided to be 
   replaced by the version 2 (described above) in a work meeting (with DP,
   DV and TW) on 18 June 20201.


The *methylation report* produced by ``sm-analysis`` is a csv file with ``;``
(semicolon) as separator and **6 columns** with the following header::

  molecule id;count(GATC);sequence;start-end of molecule;
  positions of GATCs;methylation states

The following table summarizes the meaning of each column.


+---------+------------------------------+-------------------+----------------------------------+
| col num |   field name                 |  possible values  | description                      |
+=========+==============================+===================+==================================+
|   1     | ``molecule id``              |   positive int    | value provided by the sequencer  |
+---------+------------------------------+-------------------+----------------------------------+
|   2     | ``count(GATC)``              |   positive int    | number of GATCs found in the DNA |
|         |                              |                   | sequence.                        |
+---------+------------------------------+-------------------+----------------------------------+
|   3     | ``sequence``                 |      [ACGT]*      | DNA sequence corresponding to    |
|         |                              |                   | the molecule, as reported by CCS |
+---------+------------------------------+-------------------+----------------------------------+
|   4     | ``start-end of molecule``    |   [int>=,int>0]   | inclusive interval corresponding |
|         |                              |                   | to the start and end of the      |
|         |                              |                   | molecule within the reference;   |
|         |                              |                   | the values are taken from the    |
|         |                              |                   | aligner but shifted such that    |
|         |                              |                   | the minimum position is 0 (ie    |
|         |                              |                   | 0-index is used)                 |
+---------+------------------------------+-------------------+----------------------------------+
|   5     | ``positions of GATCs``       | space separated   | 0-index positions of the A in all|
|         |                              | sequence of int>0 | the GATCs present in col 3 and   |
|         |                              |                   | realtive to that sequence        |
+---------+------------------------------+-------------------+----------------------------------+
|   6     | ``methylation states``       | space separated   | each element corresponds to the  |
|         |                              | sequence of [0-+f]| methylation state of one GATC in |
|         |                              |                   | the sequence as returned by the  |
|         |                              |                   | ``ipdSummary`` program           |
+---------+------------------------------+-------------------+----------------------------------+

Some notes:

- the number of elements in columns 5 and 6 must be equal to the value in column 2
- The meaning of the methylation state symbols:

  * ``0``:  not methylated
  * ``-``:  hemi-methylated. Negative strand
  * ``+``:  hemi-methylated. Positive strand
  * ``f``:  full methylated
