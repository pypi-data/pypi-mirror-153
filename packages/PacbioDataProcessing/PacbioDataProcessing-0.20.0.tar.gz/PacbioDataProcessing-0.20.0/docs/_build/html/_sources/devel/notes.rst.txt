.. _misc-notes:

Miscellaneous notes
===================

BAM files
---------

Modification of headers
^^^^^^^^^^^^^^^^^^^^^^^

When a a tool must modify a bam file, it seems to be agreed that
the header must contain some information about the process that
modified the file. This information is stored as a ``@PG`` record.
The following is an example::

  @PG	ID:4	PN:BLASR	VN:5.3.3	CL:blasr m54099_200714_225457.subreads.bam eco000913_3.fasta --bam --out blasr.m54099_200714_225457.subreads.bam 

The meaning of the fields is described in :ref:`samv1`.

With ``pysam`` it seems that an easy way to do it would be:

.. code-block:: python

   new_program = {
       "ID": "PacBioDataProcessing",
       "PN": "sm-analysis",
       "VN": "1.0.0",
       "CL": "sm-analysis my.bam my.fasta"
   }
   f = pysam.AlignmentFile(filename, "rb", check_sq=False)
   header = f.header.as_dict()
   programs = [new_program] + header["PG"]
   header["PG"] = programs
   # now we can write the header...
   


Easy installation
-----------------

In this section you can find some comments on different approaches to
create standalone executables. The aim is to make the installation process
easier for end users.

I have explored two possibilities:

1. `zipapp`_
2. `PyInstaller`_

None of them has convinced me at this point: either I do not have a clear
understanding of the problem or of the solutions provided by them. Or maybe
the answer is somewhere else. For example, as of today |project| depends
*implicitly* on :ref:`htslib` and that makes things complicated in this
regard since we cannot force the user to have that library in his/her
system. Despite the efforts in making easier the installation process
of |project|, at the end everything depends on whether the user has
:ref:`htslib` installed or not.

On the other hand, the two solutions listed above are *application centric*
which means AFAIK that they allow us to be in a situation where we have
a single huge file that provides only a fraction of |project|.

Finally, `wheels`_ provide an easy enough way of installing |project| that,
it is true, it suffers from the same dependency problem mentioned above, but
has a *zero-cost* to implement.


zipapp
^^^^^^

The procedure to create a self-contained app for ``sm-analysis-gui`` would be:

.. code-block:: console

   pip install PacbioDataProcessing[gui] --target sm-gui-app/
   python -m zipapp sm-gui-app -m "pacbio_data_processing.sm_analysis_gui:main_gui" -o sm-analysis-gui -p "/usr/bin/env python3.9"

The result would be a standalone executable for ``sm-analysis-gui``.


PyInstaller
^^^^^^^^^^^

WIP


Conclusion
^^^^^^^^^^

Before embarking in *easier methods* to install |project|, fix the hard dependency
problem first and probably other issues too.


.. _`zipapp`: https://docs.python.org/3/library/zipapp.html
.. _`PyInstaller`: https://www.pyinstaller.org/
