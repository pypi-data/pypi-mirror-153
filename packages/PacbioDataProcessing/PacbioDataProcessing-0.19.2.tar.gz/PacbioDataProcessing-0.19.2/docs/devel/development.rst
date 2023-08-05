.. highlight:: python

*****************
Development notes
*****************

Getting ready
=============

This section will help you with the steps needed to start working on |project|.

1. Clone the repository:

   .. prompt:: bash
      :substitutions:

      git clone |repo_url|

2. CD into in:

   .. prompt:: bash

      cd pacbio-data-processing

3. (optional) Create a virtualenv/venv and activate it. See instructions in
   :ref:`installation`.
4. Install flit:

   .. prompt:: bash

      pip install flit

5. Install |project| with all the optional dependencies:

   .. prompt:: bash

      flit install --symlink --deps=develop

With this, you should be ready to start coding but... please, keep reading!


Testing
=======

The development of |project| follows the **double loop TDD** approach.
See `double loop TDD`_.


Writing code
------------

`double loop TDD`_ is a generalization of plain TDD.  A *second TDD loop* is added to
the procedure. This sencond loop is *behaviour driven*, meaning that the functionality
is guiding us in the development process.

In brief, the procedure to develop code with this technique is as follows:

1. Write a functional test case (aka acceptance test) for the functionality you
   want to implement. You do this from the point of view of the *user*. After this
   step you will have a failing FT for that feature.
2. Make your FT pass by implementing the needed features in your code following a
   normal TDD approach. Your point of view is now different from point 1: you
   look at the problem as a developer. Do not implement more features in your code
   than your FT requires to pass. In this phase we are just playing the usual TDD
   game with the goal of making the FT for the current feature pass.
   

.. _`double loop TDD`: http://coding-is-like-cooking.info/2013/04/outside-in-development-with-double-loop-tdd/


Running the tests
-----------------

* For the functional tests

  .. code-block:: console

     $ pytest tests/functional

* Unit tests (with coverage)

  .. code-block:: console

     $ pytest --cov=pacbio_data_processing tests/unit pacbio_data_processing


Writing tests
-------------

The FTs rely on ``pytest`` (with fixtures; without stdlib's unittest)

The UTs use ``unittest`` from the standard library.


GUI
---

In a first approximation, the GUI tests were a bit smoky. The tests
consisted in:

1. (FTs) Ensure that if ``sm-analysis-gui`` is launched, a process
   remains there for some time (as one would expect after launching
   a gui program).
2. (UTs) Mocky tests to check that Gooey has been employed.
   
One improvemnet would be using something like ``PyAutoGUI``.


GitLab pipelines
================

Pipelines are a helpful tool to ensure that the code is always working (CI/CD).
One important task of our pipelines is to run all the tests. Since the tests
*define* the behaviour of |project| and since particularly the functional tests
take a while to complete, it is very convenient to trigger the execution of the
tests whenever we push to the gitlab repository.

Now, |project| depends on `Gooey`_ that, in turn depends on `wxPython`_. Since
there are no official wxPython `Wheels`_ for Linux (see
`wxPython Downloads`_), the installation of |project| implies, in general,
the compilation of `wxPython`_ which is too expensive for the resources
provided by GitLab and leads to timeouts::

  ERROR: Job failed: execution took longer than 1h0m0s seconds

The provisional solution to be able to run the tests within the
GitLab pipelines is the following:

1. Create our own `Wheels`_ using the same *docker image* that is
   used by the pipelines. In the case of the ``python:3.9`` image, it is
   ``Debian 11``. Run the container:
   
   .. prompt:: bash

      docker run -ti --rm python:3.9 /bin/bash

   And now, inside the container, run all the steps in the pipeline
   *before* the installation of |project|:

   .. prompt:: bash root@2dbff77471c5:/#
		 
      apt-get update -qq -y
      apt-get install -qq -y build-essential gcc make apt-utils
      apt-get install -y software-properties-common xvfb libgtk2.0-0 libnotify4 freeglut3 libsdl1.2debian pkg-config
      add-apt-repository -y -r ppa:deadsnakes/ppa
      apt-get update -qq -y
      apt-get install -qq -y libbz2-dev zlib1g-dev libncurses5-dev libncursesw5-dev liblzma-dev libgtk-3-dev dpkg-dev libjpeg-dev libtiff-dev libsdl1.2-dev libnotify-dev freeglut3 freeglut3-dev libghc-gtk3-dev libwxgtk3.0-gtk3-dev libgtk-3-0 libwebkit2gtk-4.0 libwebkit2gtk-4.0-dev
      pip install pip --upgrade
      pip install flit

   Now, clone the repo:

   .. prompt:: bash root@2dbff77471c5:/#

      git clone https://gitlab.com/dvelazquez/pacbio-data-processing.git

   ``cd`` into the created directory:

   .. prompt:: bash root@2dbff77471c5:/#

      cd pacbio-data-processing

   And finally, install the project (it can take a while!):

   .. prompt:: bash root@2dbff77471c5:/pacbio-data-processing#
	       
      FLIT_ROOT_INSTALL=1 flit install --deps=all

   This last step will trigger the creation of a Wheel file for wxPython.

2. Find the Wheel created in the last step:
   
   .. prompt:: bash root@2dbff77471c5:/#
		 
      pip cache --format abspath wxPython

   which will return something like::

      /PATH/TO/WHEEL/wxPython-4.1.1-cp39-cp39-linux_x86_64.whl

3. Copy that file *from the host*. In another terminal run:
   
   .. prompt:: bash

      docker cp 2dbff77471c5:/PATH/TO/WHEEL/wxPython-4.1.1-cp39-cp39-linux_x86_64.whl .

   where ``2dbff77471c5`` is the id of the ``python:3.9`` container used in step ``1``.

4. Upload that file to a public URL, that can be passed to ``pip`` for the
   explicit installation of ``wxPython``.
5. Use that URL in the ``.gitlab-ci.yml`` file to install ``wxPython`` before
   installing |project|.


.. _`Gooey`: https://github.com/chriskiehl/Gooey
.. _`wxPython`: https://wxpython.org/
.. _`wxPython Downloads`: https://wxpython.org/pages/downloads/index.html
.. _`Wheels`: https://peps.python.org/pep-0427/
