.. highlight:: shell

.. _blasr:

Blasr
=====

The ``sm-analysis`` program delegates the alignment of the input BAM
file to ``blasr``, which must be accessible at runtime. The ``blasr``
program will be called on demand: if an aligned file is found,
the alignment process will be skipped for that file.

By default, ``blasr`` is searched for in the ``PATH``. If it is
not found in the ``PATH``, you will receive a common runtime
error message::

  [CRITICAL] [Errno 2] No such file or directory: 'blasr'

and the program will terminate.

In that case, the instructions in the following sections can help you.


Installing Blasr
----------------

Probably the easiest way to install ``blasr`` is described in
`PacBio & Bioconda`_. The instructions are in summary:

1. Install ``conda`` (see `installing conda`_),
2. Setup the ``channels`` (as described in `bioconda channels`_), and
3. Install ``blasr``:

     .. prompt:: bash

	conda install -c bioconda blasr


Upon success, you will be able to pass the path to the ``blasr``
executable to ``sm-analysis`` if needed (see below for details).


Using blasr from `sm-analysis`
------------------------------

Let us assume that |project| was installed inside a virtual environment
located in::

  /home/david/.venvs/pdp

and let us assume that ``pbbioconda`` was installed in::

  /home/david/miniconda3

then, after activating the |project|'s virtual environment:

  .. prompt:: bash

     source /home/david/.venvs/pdp/bin/activate

you can tell ``sm-analysis`` about ``blasr`` by using a command
line option (``-b/--blasr-path``) as follows:

  .. prompt:: bash

     sm-analysis --blasr-path /home/david/miniconda3/bin/blasr


.. _`PacBio & Bioconda`: https://github.com/PacificBiosciences/pbbioconda
.. _`installing conda`: https://bioconda.github.io/user/install.html#install-conda
.. _`bioconda channels`: https://bioconda.github.io/user/install.html#set-up-channels
