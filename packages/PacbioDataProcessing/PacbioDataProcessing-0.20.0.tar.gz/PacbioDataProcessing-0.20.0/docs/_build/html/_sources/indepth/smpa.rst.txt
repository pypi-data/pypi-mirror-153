.. _single-molecule-analysis:

========================
Single Molecule Analysis
========================

.. admonition:: WIP

   This section is Work In Progress. It is a central piece of
   documentation that must help the interested reader understand
   the fundamentals of this project.

**SMPA** (Single Molecule Position Analysis) is a tool that allows to
analyse PacBio sequencing data and generate tables with different
formats that allow us to explore the properties on each pacbio molecule
and on each methylated position. **SMPA** uses others important tools
like **blasr** to align our sequence with the reference sequence,
**pbccs** to generate circular consensus sequences, **ipdSummary** to
predict methylations on positions through an *in-silico* model (this
allows the user to use this tool without a control sample), and other
tools dedicated for instance to read and write files compatible with the
different pacbio tools. All of those tools are executed in a ordered
steps to produce different data frames.

   You can find more information about the pacbio tools :ref:`PacBio-tools`


   If you are interested in the *in-silico* model, click
   `here <https://github.com/PacificBiosciences/kineticsTools/blob/master/doc/manual.rst>`__

How it works
------------

The following figure is a flow chart of the ``sm-analysis`` pipeline.

.. figure:: flow_chart_sm_analysis.png
   :scale: 50 %
   :alt: sm-analysis

   Flow chart of the ``sm-analysis`` program.


Output
------

Different tables are produced:

The ``ipdSummary`` table
^^^^^^^^^^^^^^^^^^^^^^^^

It has 9 columns with the following description:

+--------------------------+---------------------+---------------------+
| **Column number**        | **Name**            | **Description**     |
+==========================+=====================+=====================+
| 1                        | molecule ID         | ID number for the   |
|                          |                     | analysed molecule   |
+--------------------------+---------------------+---------------------+
| 2                        | modification        | This is related to  |
|                          |                     | the type of         |
|                          |                     | modification chosen |
|                          |                     | to be detected      |
+--------------------------+---------------------+---------------------+
| 3                        | position            | Base position where |
|                          |                     | the methylation was |
|                          |                     | detected            |
+--------------------------+---------------------+---------------------+
| 4                        | score               | Phred-transformed   |
|                          |                     | pvalue that a       |
|                          |                     | kinetic deviation   |
|                          |                     | exists at this      |
|                          |                     | position            |
+--------------------------+---------------------+---------------------+
| 5                        | strand              | DNA strand (forward |
|                          |                     | or reverse)         |
+--------------------------+---------------------+---------------------+
| 6                        | coverage            | Valid IPDs at this  |
|                          |                     | position and        |
|                          |                     | probably related to |
|                          |                     | the numbers of      |
|                          |                     | subreads used for   |
|                          |                     | the detection       |
+--------------------------+---------------------+---------------------+
| 7                        | sequence            | Sequence context of |
|                          |                     | the detection, this |
|                          |                     | have 41 bases       |
|                          |                     | length and the      |
|                          |                     | modified base in    |
|                          |                     | the center          |
+--------------------------+---------------------+---------------------+
| 8                        | IPDratio            | This in the IPD     |
|                          |                     | ratio of the        |
|                          |                     | methylated base     |
|                          |                     | calculated using    |
|                          |                     | the *in-silico*     |
|                          |                     | model               |
+--------------------------+---------------------+---------------------+
| 9                        | idQV                | This is related     |
|                          |                     | with the quality    |
|                          |                     | value of the        |
|                          |                     | identification      |
+--------------------------+---------------------+---------------------+

For a more detailed description click
`here <https://github.com/PacificBiosciences/kineticsTools/blob/master/doc/manual.rst>`__


The molecule table
^^^^^^^^^^^^^^^^^^

It has 8 columns with the following description:

+--------------------------+---------------------+---------------------+
| **Column number**        | **Name**            | **Description**     |
+==========================+=====================+=====================+
| 1                        | **molecule_ID**     | ID number for the   |
|                          |                     | analysed molecule   |
+--------------------------+---------------------+---------------------+
| 2                        | **pos_u**           | List of sorted      |
|                          |                     | methylated          |
|                          |                     | positions in the    |
|                          |                     | molecule            |
+--------------------------+---------------------+---------------------+
| 3                        | **metypes_u**       | Methylated types    |
|                          |                     | related to the      |
|                          |                     | positions in        |
|                          |                     | *pos_u* column      |
+--------------------------+---------------------+---------------------+
| 4                        | **hemi_fwd**        | Number of           |
|                          |                     | detections only in  |
|                          |                     | the forward strand  |
|                          |                     | (hemi-methylation   |
|                          |                     | +)                  |
+--------------------------+---------------------+---------------------+
| 5                        | **hemi_rv**         | Number of           |
|                          |                     | detections only in  |
|                          |                     | the reverse strand  |
|                          |                     | (hemi-methylation   |
|                          |                     | -)                  |
+--------------------------+---------------------+---------------------+
| 6                        | **full**            | Number of full      |
|                          |                     | methylation         |
|                          |                     | detections          |
|                          |                     | (full-methylation)  |
+--------------------------+---------------------+---------------------+
| 7                        | **gatc_cov**        | Number of GATC      |
|                          |                     | positions in the    |
|                          |                     | molecule            |
+--------------------------+---------------------+---------------------+
| 8                        | **pos_diff**        | Difference in bases |
|                          |                     | between every       |
|                          |                     | position in the     |
|                          |                     | *pos_u* column      |
+--------------------------+---------------------+---------------------+


The position table
^^^^^^^^^^^^^^^^^^

It has 6 columns with the following description:

+--------------------------+---------------------+---------------------+
| **Column number**        | **Name**            | **Description**     |
+==========================+=====================+=====================+
| 1                        | **positions**       | Methylation         |
|                          |                     | position            |
+--------------------------+---------------------+---------------------+
| 2                        | **met_types**       | List of methylation |
|                          |                     | types detected for  |
|                          |                     | the position in     |
|                          |                     | different molecules |
+--------------------------+---------------------+---------------------+
| 3                        | **mol_cov**         | Number of molecules |
|                          |                     | on which the        |
|                          |                     | position appear     |
+--------------------------+---------------------+---------------------+
| 4                        | **hemi_fwd**        | Number of           |
|                          |                     | detections only in  |
|                          |                     | the forward strand  |
|                          |                     | (hemi-methylation   |
|                          |                     | +)                  |
+--------------------------+---------------------+---------------------+
| 5                        | **hemi_rv**         | Number of           |
|                          |                     | detections only in  |
|                          |                     | the reverse strand  |
|                          |                     | (hemi-methylation   |
|                          |                     | -)                  |
+--------------------------+---------------------+---------------------+
| 6                        | **full**            | Number of full      |
|                          |                     | methylation         |
|                          |                     | detections          |
|                          |                     | (full-methylation)  |
+--------------------------+---------------------+---------------------+


The Methylation report table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The methylation report table integrate the information from ipdSummary
together with CCS (Circular Consensus Sequence) and the reference. Each
line on this table contains information about each molecule. The
description of this format can be found in
:ref:`methylation-report-format`.
