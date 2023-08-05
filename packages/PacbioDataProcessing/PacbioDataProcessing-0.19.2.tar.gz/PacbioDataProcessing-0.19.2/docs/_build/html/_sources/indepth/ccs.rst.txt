.. highlight:: shell

.. _ccs:

CCS
===

The ``sm-analysis`` program uses the ``ccs`` program to obtain highly
accurate reads from the input BAM that are taken as the true sequences
and positions within the reference for each molecule. ``ccs`` must be
accessible at runtime and it is called on demand: if its output is
already there, it will not be computed again.

By default, ``ccs`` is searched for in the ``PATH``. If it is
not found in the ``PATH``, you will receive a common runtime
error message::

  [CRITICAL] [Errno 2] No such file or directory: 'ccs'

and the program will terminate.

In that case, the instructions in the following sections can help you.


Installing CCS
--------------

Probably the easiest way to install ``ccs`` is described in
`PacBio & Bioconda`_. The instructions are in summary:

1. Install ``conda`` (see `installing conda`_),
2. Setup the ``channels`` (as described in `bioconda channels`_), and
3. Install ``pbccs``:

     .. prompt:: bash

	conda install -c bioconda pbccs


Upon success, you will be able to pass the path to the ``ccs``
executable to ``sm-analysis`` if needed (see below for details).


Using ccs from `sm-analysis`
------------------------------

Let us assume that |project| was installed inside a virtual environment
located in::

  /home/david/.venvs/pdp

and let us assume that ``pbbioconda`` was installed in::

  /home/david/miniconda3

then, after activating the |project|'s virtual environment:

  .. prompt:: bash

     source /home/david/.venvs/pdp/bin/activate

you can tell ``sm-analysis`` about ``ccs`` by using a command
line option (``-c/--ccs-path``) as follows:

  .. prompt:: bash

     sm-analysis --ccs-path /home/david/miniconda3/bin/ccs


.. _`PacBio & Bioconda`: https://github.com/PacificBiosciences/pbbioconda
.. _`installing conda`: https://bioconda.github.io/user/install.html#install-conda
.. _`bioconda channels`: https://bioconda.github.io/user/install.html#set-up-channels


Issues
------

Multimapping
^^^^^^^^^^^^

In some cases an aligned CCS file presents multimapping. Two examples take from the
``st1A09`` file::

  m54099_200720_153206/4194505/ccs        0       U00096.3        392180  0       150=    *       0       0       ATCTGTACGTAAGTACGTGATGTCTCCTGCCCACTTCT...
  m54099_200720_153206/4194505/ccs        256     U00096.3        1094716 0       150=    *       0       0       ATCTGTACGTAAGTACGTGATGTCTCCTGCCCACTTCT...
  m54099_200720_153206/4194505/ccs        272     U00096.3        2170808 0       150=    *       0       0       GGACTGAGGGCAAAGGCCTCCCGGAAGTTCAGCCCGGT...
  m54099_200720_153206/4194505/ccs        272     U00096.3        567414  0       150=    *       0       0       GGACTGAGGGCAAAGGCCTCCCGGAAGTTCAGCCCGGT...
  m54099_200720_153206/4194505/ccs        272     U00096.3        315863  0       150=    *       0       0       GGACTGAGGGCAAAGGCCTCCCGGAAGTTCAGCCCGGT...
  ...
  m54099_200720_153206/4194627/ccs        0       U00096.3        274198  0       295=    *       0       0       CCCTTGTATCTGGCTTTCACGAAGCCGAACTGTCGCTT...
  m54099_200720_153206/4194627/ccs        256     U00096.3        574834  0       295=    *       0       0       CCCTTGTATCTGGCTTTCACGAAGCCGAACTGTCGCTT...
  m54099_200720_153206/4194627/ccs        256     U00096.3        688094  0       295=    *       0       0       CCCTTGTATCTGGCTTTCACGAAGCCGAACTGTCGCTT...
  m54099_200720_153206/4194627/ccs        272     U00096.3        3130803 0       295=    *       0       0       CGGCCAACGAGCATGACCTCAATCAGCTGGGTAATCTG...
  m54099_200720_153206/4194627/ccs        256     U00096.3        2101992 0       295=    *       0       0       CCCTTGTATCTGGCTTTCACGAAGCCGAACTGTCGCTT...
  m54099_200720_153206/4194627/ccs        256     U00096.3        2289162 0       295=    *       0       0       CCCTTGTATCTGGCTTTCACGAAGCCGAACTGTCGCTT...
  m54099_200720_153206/4194627/ccs        272     U00096.3        1396701 0       295=    *       0       0       CGGCCAACGAGCATGACCTCAATCAGCTGGGTAATCTG...
  m54099_200720_153206/4194627/ccs        272     U00096.3        1300156 0       295=    *       0       0       CGGCCAACGAGCATGACCTCAATCAGCTGGGTAATCTG...
  m54099_200720_153206/4194627/ccs        256     U00096.3        3365799 0       295=    *       0       0       CCCTTGTATCTGGCTTTCACGAAGCCGAACTGTCGCTT...
  m54099_200720_153206/4194627/ccs        256     U00096.3        3652279 0       295=    *       0       0       CCCTTGTATCTGGCTTTCACGAAGCCGAACTGTCGCTT...

How do we decide the position? In the current implementation, the first
subread of each molecule is taken (for details, see
``pacbio_data_processing.sm_analysis.map_molecules_with_highest_sim_ratio``),
because all the subreads are *perfect*. But notice that the positions (4th
column) differ.
