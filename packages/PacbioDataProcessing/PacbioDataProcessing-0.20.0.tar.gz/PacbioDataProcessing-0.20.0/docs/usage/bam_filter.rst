.. highlight:: shell

.. _bam-filter:

Filtering Bam files with ``bam-filter``
=======================================

This executable is useful to filter :ref:`aligned-PacBio-bam-file`'s
according to the values of some columns. It offers the following
options:

   .. prompt:: bash

   $ bam-filter -h
   usage: bam-filter [-h] [-l NUM] [-r NUM] [-q NUM] [-m MAPPING [MAPPING ...]] [-R NUM] [-v] [--version] BAM-FILE

   Program to filter BAM files after Pacbio sequencing. Different filters can be applied on demand (by default all the filters are disabled). The order in which the filters
   are applied is: 1) remove rows with len of DNA sequence under some threshold; 2) take only molecules with a minimum number of subreads; 3) choose molecules with
   sequencing quality above some threshold; and 4) choose mapping.

   positional arguments:
     BAM-FILE              input file in BAM format. The output will be another BAM-FILE with the same name but prefixed with 'parsed.'

     optional arguments:
       -h, --help            show this help message and exit
       -l NUM, --min-dna-seq-length NUM
   minimum length of DNA sequence to be kept (default: 0)
       -r NUM, --min-subreads-per-molecule NUM
                             minimum number of subreads per molecule to keep it (default: 1)
       -q NUM, --quality-threshold NUM
                             quality threshold of the sample. Between 0 (the lowest) and 255 (the highest) (default: 0)
       -m MAPPING [MAPPING ...], --mappings MAPPING [MAPPING ...]
                             keep only the requested (space separated) list of mappings (default: keep all)
       -R NUM, --min-relative-mapping-ratio NUM
                             minimum ratio (amount of found wanted mappings/all mappings present) in order to keep the data point (default: take all)
       -v, --verbose
       --version             show program's version number and exit
