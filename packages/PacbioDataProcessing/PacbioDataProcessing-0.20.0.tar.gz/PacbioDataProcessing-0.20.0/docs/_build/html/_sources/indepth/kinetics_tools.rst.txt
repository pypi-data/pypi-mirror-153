.. highlight:: shell

.. _kineticsTools:

kineticsTools
=============

The ``sm-analysis`` program delegates the identification of
methylations to the ``ipdSummary`` program provided by the
`kineticsTools package`_.

By default, ``ipdSummary`` is searched for in the ``PATH``. If it is not
found in the ``PATH``, you will receive the usual runtime error message::

  [CRITICAL] [Errno 2] No such file or directory: 'ipdSummary'

and the program will terminate.

In that case, the instructions in the following sections can help you.


Installing kineticsTools
------------------------

The `kineticsTools package`_ is written in Python. Unfortunately, at the time
of this writing, there is no version of it in PyPI.

Therefore to use ``ipdSummary``, we need to install
``kineticsTools`` and its dependencies from their GitHub repositories.
This can be as follows. First activate the virtual environment where
you have installed (or will install) |project|. Let us assume that
|project| was installed inside a virtual environment located in::

  /home/david/.venvs/pdp

then, the activation must be done as usual with:

  .. prompt:: bash

     source /home/david/.venvs/pdp/bin/activate

and now install the required packages with:

  .. prompt:: bash

	pip install git+https://github.com/PacificBiosciences/pbcore.git
	pip install git+https://github.com/PacificBiosciences/pbcommand.git
	pip install git+https://github.com/PacificBiosciences/kineticsTools.git


After this you will be able to use the ``ipdSummary`` executable to
from ``sm-analysis`` automatically. If ``kineticsTools`` was installed in
a different virtual environment, have a look at the following section.

.. note::

   If, for some reason, the above mentioned repositories are not
   accesible, the installation can be carried out with the following
   lines that use alternative repositories:

   .. prompt:: bash

      pip install git+https://github.com/palao/pbcore.git
      pip install git+https://github.com/palao/pbcommand.git
      pip install git+https://github.com/palao/kineticsTools.git
      

Using ``ipdSummary`` installed in another virtual environment
-------------------------------------------------------------

Let us assume that |project| was installed inside a virtual environment
located in::

  /home/david/.venvs/pdp


but ``kineticsTools`` was installed in::

  /home/david/.venvs/another

then, after activating the |project|'s virtual environment:

  .. prompt:: bash

     source /home/david/.venvs/pdp/bin/activate

you can tell ``sm-analysis`` about ``ipdSummary`` by using a command
line option (``-i/--ipdsummary-path``) as follows:

  .. prompt:: bash

     sm-analysis --ipdsummary-path /home/david/.venvs/another/bin/ipdSummary


.. _`kineticsTools package`: https://github.com/PacificBiosciences/kineticsTools
