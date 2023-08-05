.. highlight:: shell

.. _pbindex:

Pbindex
=======

The ``sm-analysis`` program delegates the indexing of one-molecule
BAM files to ``pbindex``, which must be accessible at runtime.
By default, ``pbindex`` is searched for in the ``PATH``. If it is
not found in the ``PATH``, you will receive an informative runtime
error message::

  [CRITICAL] [Errno 2] No such file or directory: 'pbindex'

and the program will stop.

In that case, the instructions in the following sections can help you.


Installing Pbindex
------------------

Probably the easiest way to install ``pbindex`` is described in
`PacBio & Bioconda`_. The instructions are basically:

1. Install ``conda`` (see `installing conda`_),
2. Setup the ``channels`` (as described in `bioconda channels`_), and
3. Install ``pbbam``:

     .. prompt:: bash

	conda install -c bioconda pbbam


Upon success, you will be able to pass the path to the ``pbindex``
executable to ``sm-analysis`` if needed (see below for details).


Using Pbindex from `sm-analysis`
--------------------------------

Let us assume that |project| was installed inside a virtual environment
located in::

  /home/david/.venvs/pdp

and let us assume that ``pbbioconda`` was installed in::

  /home/david/miniconda3

then, after activating the |project|'s virtual environment:

  .. prompt:: bash

     source /home/david/.venvs/pdp/bin/activate

you can tell ``sm-analysis`` about ``pbindex`` by using a command
line option (``-p/--pbindex-path``) as follows:

  .. prompt:: bash

     sm-analysis --pbindex-path /home/david/miniconda3/bin/pbindex


.. _`PacBio & Bioconda`: https://github.com/PacificBiosciences/pbbioconda
.. _`installing conda`: https://bioconda.github.io/user/install.html#install-conda
.. _`bioconda channels`: https://bioconda.github.io/user/install.html#set-up-channels
