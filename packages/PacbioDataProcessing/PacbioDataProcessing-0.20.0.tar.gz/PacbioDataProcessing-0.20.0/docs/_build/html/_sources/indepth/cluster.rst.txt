.. _using-a-cluster:

============================
Using |project| on a cluster
============================

:Author: David Palao
:Date: 22 September 2021
:Last updated: 23 September 2021
:Version: ---
:Tags: sm-analysis bam-filter PacbioDataProcessing cluster goethe-HLR
       fuchs slurm
       
:abstract:

   This document describes the process of installing and using
   |project| on a *cluster* with a queueing system. It will
   be illustrated with the *goethe-HLR* cluster (at the University of
   Frankfurt) that employs *slurm* as a queueing system.


Introduction
============

A *computing cluster*, or *cluster*, is a system that provides
access to high computing power by joining multiple *nodes* and
coordinating their usage. A node is basically a single powerful
computer.

There are two obvious ways to give a *cluster* more
computing power:

* by adding more nodes. This strategy is sometimes referred to as
  *horizontal scaling*.
* by using more powerful nodes (with faster CPU, more *cores* or
  RAM, etc). Increasing the power of each node is sometimes called
  *vertical scaling*.

Processing large bam files with |project| can greatly benefit from
the resources provided by a cluster: you typically get access to
many powerful nodes, hence you can potentially increase the throughput
of your application both *horizontally* and *vertically*. Needless to say,
that comes with a price to pay in terms of complexity of usage.

The goal of this document is to lower the complexity barrier to use
a cluster to speed up the analysis of bam files with |project|. You will
find some explanations on how this can be done in practice. We will use as
example the *goethe-HLR* cluster managed by the CSC_ at the University
of Frankfurt.


Preparation
===========

Before anything you need a valid account on the cluster.

.. admonition:: For the goethe-HLR cluster

   To get an account on *goethe-HLR*, follow the instructions to submit
   a `CSC user application`_. At the time of writing this document
   access to the *FUCHS* (sub-)cluster is granted to academic institutions
   in the state of Hesse (Germany).


Installation
============

Once you have an account on a cluster you need to install |project| on the
system. Follow these instructions:

1. Login to the cluster. Typically after getting permission to use the
   cluster, you are provided by a user name and a password that will
   allow you to do login through *ssh*.

   .. admonition:: For the goethe-HLR cluster

      You will receive a username (in my case it is ``palao``, which I will use
      in the examples) and instructions to get the password.
      In order to access the cluster you need to *ssh* into the cluster.
      If you are using a terminal, type the following command (without the
      $, which is a symbol to indicate that you are expected to type what follows
      in a shell or terminal):

      .. prompt:: bash

	 ssh palao@goethe.hhlr-gu.de

      and type the password in, when requested.
      On success (i.e. you enter the correct password), that command will start
      a remote shell on the cluster which will be our main interface to it.
      If the *ssh* command is not in your system, one *ssh client*
      must be installed to be able to access *goethe-HLR*.

2. Install |project| on the cluster.  Follow the instructions found in
   the section about :ref:`installation` to install |project|.

   .. admonition:: For the goethe-HLR cluster

      In order to have the correct version of Python on the cluster
      you have several options:

      a. Install Python directly from sources, or
      b. Follow the `instructions to use spack at Goethe-HLR`_ and install
	 the needed version of Python with Spack.

      Installing Python from sources seems daunting but it ends up being
      easier than using Spack if you need a version that is not available
      in Spack. Of course it all depends on your experience.
      In case of doubts do not hesitate to contact the admins. They will
      hopefully give you a good advice in this regard.

3. |project| needs some external tools for the main pipeline ``sm-analysis``
   to work: :ref:`pbindex`, :ref:`blasr` and :ref:`ccs`. Follow the links to
   install them on the cluster.

   .. note::

      Since these are *external dependencies*, they can be installed anywhere
      as far as the tools are accesible to |project|. For instance, in my
      case I did the following:

      * ``ccs``. This tool's latest version is only provided as an executable
	(i.e., they closed the source). I downloaded it and stored it side by
	side with ``sm-analysis`` in the same ``venv``.
      * ``blasr``. I installed it with ``bioconda`` in a dedicated environment
	and passed the path to ``blasr`` directly to ``sm-analysis``:

	.. prompt:: bash

	   sm-analysis ... -b ~/miniconda/bin/blasr ...

	Notice that the ``...`` are symbolic.
      * ``pbindex``. I installed manually with ``meson`` the ``pbbam`` package
	and, again, pass the path to the executable in each call to
	``sm-analysis``:

	.. prompt:: bash

	   sm-analysis ... -p ~/src/pbbam/build/tools/pbindex ...


Once |project| is installed, you are almost ready to use it. But on a cluster
there is typically a queueing system that manages the resources. In the next
section we describe the usage of |project| through ``slurm``, a very common
queueing system.


Running
=======

A typical workflow to run software in a cluster managed by ``slurm`` (or any other
queueing system) is:

1. prepare a *batch* script, and
2. *submit* it and wait for the results.

The syntax and options of *batch* files are wide topics covered elsewhere. In
this section we focus in preparing minimally functional batch scripts to use
|project| with ``slurm``.

.. admonition:: For the goethe-HLR cluster

   In the webpage of `CSC`_ you can find plenty of information about the
   `Goethe-HLR Cluster Usage`_ and the `FUCHS Cluster Usage`_ including
   details about using ``slurm``, recommended storage locations and much more.


In the rest of the section we will provide some examples of *batch* scripts
and we will assume the following:

* |project| has been installed in a ``venv`` such that the activation step is:

  .. code-block:: bash

     source ~/.venvs/PacbioDataProcessing/bin/activate

* The working directory will be:

  .. code-block:: bash

     /scratch/darmstadt/palao/projects/pacbio/m45

* In that directory there is a bam file named ``m45.bam`` that we are interested
  in analyze on a per molecule basis with ``sm-analysis``. There is a reference
  too in the ``fasta`` format: ``reference.fasta`` and ``reference.fasta.fai``.


A simple ``slurm`` batch script for ``sm-analysis``
---------------------------------------------------

The following listing contains a batch script that:

* reserves ``1`` compute node from the partition named *fuchs* for ``2`` days and
  ``12`` hours
* starts ``10`` simultaneous instances of ``ipdSummary``, each spawning
  ``4`` worker processes

.. code-block:: bash

   #!/bin/bash
   #SBATCH --job-name=m45
   #SBATCH --partition=fuchs
   #SBATCH --nodes=1
   #SBATCH --time=2-12:00:00
   #SBATCH --mail-type=ALL

   source ~/.venvs/PacbioDataProcessing/bin/activate
   cd /scratch/darmstadt/palao/projects/pacbio/m45

   sm-analysis m45.bam reference.fasta -n 4 -N 10

A ``slurm`` batch script to run ``sm-analysis`` in parallel
-----------------------------------------------------------

For large bam files it could be beneficial to employ more than a single node to
speed up the analysis process.

The following listing contains a batch script that:

* reserves ``16`` compute nodes from the partition named *fuchs* for ``10`` days
* starts, *in each node*, ``10`` simultaneous instances of ``ipdSummary``, each
  in turn spawning ``4`` worker processes

.. code-block:: bash

   #!/bin/bash
   #SBATCH --job-name=m45
   #SBATCH --partition=fuchs
   #SBATCH --nodes=16
   #SBATCH --time=10-0:00:00
   #SBATCH --mail-type=ALL

   source ~/.venvs/PacbioDataProcessing/bin/activate
   cd /scratch/darmstadt/palao/projects/pacbio/m45

   for (( t=1;  t <= SLURM_NNODES; t++)); do
     srun --nodes=1 sm-analysis m45.bam reference.fasta -n 4 -N 10 -P ${t}:${SLURM_NNODES} &
     sleep 5
   done
   wait

Pay attention to the following points:

* we are splitting the processing in ``16`` *partitions*. Each node will produce the
  output corresponding to one 16-th of the original bam file in this example.
* ``sm-analysis`` is run with the help of ``srun`` to let ``slurm`` choose an empty
  node for each partition.
* at the end of the ``srun`` line there is a ``&`` and at the end of the script there is
  a ``wait`` command. It is very important not to forget these two *details*.


Submitting the job
------------------

Finally, once the batch script is ready, it is time to *submit a job*. A
job is what the queueing system creates when you tell it to run some program.
In order to tell the cluster to execute the task described in the script, save it
as, e.g. ``sm-analysis.slurm`` and run the following command in the cluster to
submit the job:

.. prompt:: bash

   sbatch sm-analysis.slurm

Since the mail notifications are all active, you should receive an email when the job
starts running and when it finishes.

However the ``squeue`` command could be handy to have immediate feedback on the status
of the job:

.. prompt:: bash

   squeue -u palao

the ``-u palao`` part means that we will get information only on jobs submitted
by user ``palao``. Other useful commands are available too. Please have a look
at `Goethe-HLR Cluster Usage`_ or at `FUCHS Cluster Usage`_ for more details.

Once the job successfully completes, you will find the results in the working
directory, ``/scratch/darmstadt/palao/projects/pacbio/m45`` in our case,
and a ``log`` file created by slurm with all the outputs generated by
the commands executed during the job. The name of the ``log`` file is, by
default something like ``slurm-??????.out``, where ``??????`` is the job number
assigned by ``slurm``.


.. _CSC: https://csc.uni-frankfurt.de/
.. _`CSC user application`: https://csc.uni-frankfurt.de/wiki/doku.php?id=public:access
.. _`instructions to use spack at Goethe-HLR`: https://csc.uni-frankfurt.de/wiki/doku.php?id=public:usage:spack
.. _`Goethe-HLR Cluster Usage`: https://csc.uni-frankfurt.de/wiki/doku.php?id=public:usage:goethe
.. _`FUCHS Cluster Usage`: https://csc.uni-frankfurt.de/wiki/doku.php?id=public:usage:fuchs
