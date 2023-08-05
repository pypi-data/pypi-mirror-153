.. _PacBio-tools:

============
PacBio tools
============

SMRT-link software server tool
------------------------------

The sequencing PacBio data is normally processed by a sofware-server
tool
`SMRT-link <https://www.pacb.com/products-and-services/analytical-software/smrt-analysis/>`__.
Which means that a Software to process the PacBio data should be
intalled in a server and then processed there using the standars
protocols of pacbio.

Here some additional information related to SMART-link:

-  `All SMRT software
   versions <https://www.pacb.com/support/software-downloads/>`__
-  `SMRT® Portal
   Help <http://files.pacb.com/software/smrtanalysis/2.2.0/doc/smrtportal/help/!SSL!/Webhelp/Portal_Main.htm>`__
-  `Installing SMRT_youtube
   videos <https://www.youtube.com/user/ZmjhsiehZ/videos>`__
-  `Evolution of sequencing
   era <https://www.pacb.com/blog/the-evolution-of-dna-sequencing-tools/>`__
-  `The white
   paper <https://www.pacb.com/wp-content/uploads/2015/09/WP_Detecting_DNA_Base_Modifications_Using_SMRT_Sequencing.pdf>`__
-  `SMRT link without
   control? <http://seqanswers.com/forums/showthread.php?s=f2bc6a3bb12677c9111e6608269733f3&t=93071>`__

PacBio-Bioconda
---------------

If you are familiar with command lines and programing the PacBio company
provide a collection of tools to manage the sequencing data. This can be
installed in a server or a personal computer using a virtual environment
called Bioconda, specifically Miniconda. The collection of tools are
called the `PacBio Bioconda
tools <https://github.com/PacificBiosciences/pbbioconda>`__.

Installing Miniconda
~~~~~~~~~~~~~~~~~~~~

It is possible to work with the PacBio data using differents tools
installed through Bioconda (virtual environment).

Follow the next steps to install Bioconda and its most useful tools.

1. **Download miniconda** Choose between miniconca 2 (for using python
   2) and miniconca 3 (for using python 3) in the `miniconda
   webpage <https://bioconda.github.io/user/install.html#install-conda>`__
   depending which version you need to work, choose the operative system
   you are using and donwload it.

To download miniconda 2 in MacOS, you can type the following line in
your terminal:

.. prompt:: bash

   curl -O https://repo.anaconda.com/miniconda/Miniconda2-latest-MacOSX-x86_64.sh

To download miniconda 3 in MacOS, you can type the following line in
your terminal:

.. prompt:: bash

   curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh

2. **Install miniconda** Using the terminal in the directory where
   miniconda was downloaded, the following line if you want to install
   miniconda 2 or 3 (just change the name). In this case miniconda 3 is
   going to be installed:

.. prompt:: bash

   sh Miniconda3-latest-MacOSX-x86_64.sh

a. Standard directory to install miniconda is in you home directory and
   a directory called miniconda3 will be created. Don’t forget the
   location of this folder because this is the route to call the virtual
   environment.

b. The installation process also ask you if you want to specify a
   directory. You can create a new one only typing a directory name
   after the ``>>>``\ prompt. This is optional and useful when you want
   to have more tha one virtual environment related to miniconda.

c. Another important question during the installation is if you wish the
   installer to initialize Miniconda3, wich means that every time you
   start the terminal, the virtual environment will be activated and the
   tools installed there. You only need to type ‘yes’ or ‘not’ after the
   ‘>>>’ prompt.

3. **Activate miniconda** If you type ‘not’ in the las step, then, when
   you open the terminal, go to your home directory where miniconda was
   installed and activate it as the following example (activation for
   miniconda3):

.. prompt:: bash

   source home_directory_route/miniconda3/bin/activate

4. **Configure miniconda** The first step is to have miniconda
   activated. Then, to configure miniconda installation, type the
   following lines in this order:

.. prompt:: bash

   conda config --add channels defaults
   conda config --add channels bioconda
   conda config --add channels conda-forge

5. **Installing tools** The more useful tools can be installed using the
   following line:

.. prompt:: bash

   conda install -c bioconda blasr pbcore numpy scipy pbbam samtools pbcommand

If you are interested in other tools, check the collections of tools you
can install in this link –> `PacBio-Bioconda
tools <https://github.com/PacificBiosciences/pbbioconda>`__ Is
recomendable to update the tools after installation. To do this type:

.. prompt:: bash

   conda update tool_name

for invidual tools or:

.. prompt:: bash

   conda update --all

to update all the tools.

6. **Deactivate miniconda** To deactivate the miniconda you don’t need
   to be in the home directory, just type this line and miniconda will
   be deactivate:

.. prompt:: bash

   conda deactivate

Some of the more useful tools to consider are:

+-----------------------------------+-----------------------------------+
| **Tool**                          | **Description**                   |
+===================================+===================================+
| bax2bam                           | Allows to transform files from    |
|                                   | old chemiestries and formats to   |
|                                   | the bam file format.              |
+-----------------------------------+-----------------------------------+
| blasr                             | The official PacBio aligner       |
|                                   | adapted for long sequencing       |
|                                   | reads. Although other aligners    |
|                                   | such as *BWA*, *Segemehl* and     |
|                                   | *pbalign* were compared, *blasr*  |
|                                   | had the best mapping along with   |
|                                   | pbaling, both aligners found in   |
|                                   | the pacbio bioconda tools. It was |
|                                   | decided to take *blasr* as the    |
|                                   | aligner to do the analyses        |
|                                   | because it is the only one whose  |
|                                   | result includes the ipd columns   |
|                                   | needed to be able to detect DNA   |
|                                   | modifications.                    |
+-----------------------------------+-----------------------------------+
| pbmm2                             | New aligner suggested to be a     |
|                                   | substitute for blasr. When        |
|                                   | evaluated, it turned out to be    |
|                                   | faster in the alignment process,  |
|                                   | however there is not a big        |
|                                   | difference in the total number of |
|                                   | aligned subreads. The output was  |
|                                   | not sorted by molecule and has    |
|                                   | therefore been discarded for the  |
|                                   | time being.                       |
+-----------------------------------+-----------------------------------+
| pbccs                             | This produce the Circular         |
|                                   | Consensus Sequencing from all the |
|                                   | subreads on each molecule         |
+-----------------------------------+-----------------------------------+
