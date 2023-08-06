.. _quickstart9steps:

=======================
Quickstart on a cluster
=======================


This document describes briefly  how to install and use the |project|
software on a cluster. If you need more details, please consult the
references.

Starting with a PacBio sequencing file (bam file) and a
reference sequence (fasta file) you can generate a dataframe (csv file)
with columns containing properties for each molecule that overcame good
quality filters.

Additional to this, a summary report is generated containing information
related to the input and output files for each process.

1. Open a cluster access account (see :ref:`using-a-cluster`).

2. Open a terminal and login to access to the cluster
   (see :ref:`using-a-cluster`).

3. Install python 3.9 in the cluster (see the :ref:`installation` document).

4. Create a virtual environment (see the :ref:`installation` document).

5. Install the external dependences pbindex, blasr and ccs (see the
   :ref:`using-a-cluster` document).

6. Install PacBio Data Processing (see the :ref:`installation` document).

7. Transfer the input files to the cluster. Assuming you want to process
   a file called ``pbsequencing.bam`` and your reference is stored in
   a file called ``reference.fasta`` (with its companion index
   ``reference.fasta.fai``), run the following command in a terminal:

   .. code-block:: console

       scp pbsequencing.bam reference.fasta{,.fai} velazquez@goethe.hhlr-gu.de:/home/fuchs/darmstadt/velazquez

   the path will change depending on the name on your account, and the
   wanted destination directory.

8. Running a Job (see :ref:`using-a-cluster`).

9. Transfer the output files to your personal computer:

   .. code-block:: console

       scp velazquez@goethe.hhlr-gu.de:/home/fuchs/darmstadt/velazquez/[file to transfer] .

   where the trailing ``.`` (*dot*) can be replaced by any other *local path*,
   of course. The special case of ``.`` means *current working directory*.

   Or you can synchronize the remote location with your current working directory like:

   .. code-block:: console

       rsync -av velazquez@goethe.hhlr-gu.de:/home/fuchs/darmstadt/velazquez/ ./

