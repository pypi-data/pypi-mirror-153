.. _quickstart:

============================
Quickstart for the impatient
============================

If you know how to install python packages from PyPI and how to
use the command line, you can follow the instructions in this
section to get |project| up and running.

Alternatively, if you need a step-by-step guide to use |project| on a cluster,
follow the :ref:`quickstart9steps` guide.

Installation
============

To install **PacBio Data Processing**, open an interactive shell and run:

.. prompt:: bash

  pip install PacBioDataProcessing

or, alternatively:

.. prompt:: bash

  python -m pip install PacBioDataProcessing


.. note::

   More details as well as alternative installation methods are explained
   in :ref:`installation`.


.. warning::

   Although the installation of |project| is now complete, there are some
   *runtime* dependencies. That means that they *must be there* before
   *using* |project|. See :ref:`other-dependencies` and the links therein
   for the list of dependencies and suggestions on how to install them.


Using |project|
===============

To do a single molecule analysis of ``m6A`` methylations in DNA, you need:

* a BAM file with the result of the sequencing, and
* the reference file: a ``.fa/.fasta`` plus the companion
  ``.fa.fai/.fasta.fai`` file

and use the ``sm-analysis`` program, feeding it with those files.

For example, if the bam file's name is ``mysequence.bam`` and the reference
files are ``myreference.fasta`` and ``myreference.fasta.fai``, then the
``sm-analysis`` program will carry out a single molecule analysis of the
``m6A`` methylations found during sequencing with the following command:

  .. prompt:: bash

     sm-analysis mysequence.bam myreference.fasta

In the :ref:`usage` section you can find detailed information about
the output and the possible input options available in ``sm-analysis``
as well as a description of other tools provided by this package
(like ``bam-filter``).

