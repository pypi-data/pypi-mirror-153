.. highlight:: shell

.. _releases:

************************
HOW to release a version
************************

In this section I will describe the procedure to make a release (create
a new version of the code and publish it), and the management commands
that we use for that (``git``, ``flit``, etc).

Let us assume that we want to implement a new feature. Say that we are
going to create a replacement for the ``ccs`` program. The following is
an overview of the necessary steps to make the release:

1. Create a feature branch::

     git flow feature start own-ccs

2. (Hopefully not very) long cycles of double loop TDD to implement the
   feature (see :ref:`Testing`).
3. When the feature is ready, ensure that the tests pass::

     tox

4. Finish the branch::

     git flow feature finish own-ccs

   as a result you will land in the ``develop`` branch.

5. Merge the new feature into ``master``::

     git checkout master
     git merge develop

6. Fix whatever is needed in the documentation. At the very minimum,
   think at least about these docs:

   * ``CHANGELOG.rst``
   * ``docs/roadmap.rst``

7. Set the new version::

     bump2version "part"

   where ``part`` is one of: ``patch``, ``minor`` or ``major``. For instance::

     bum2version minor

   to increase the *minor* digit of the version. Versions are::

     major.minor.patch

   such that in, eg::

     1.0.2

   major is ``1``, minor is ``0`` and patch is ``2``.

8. Upload the changes to the repo::

     git push

   this will trigger the pipelines in gitlab and update the docs
   in readthedocs.

9. Publish the code in `PyPI`_::

     flit publish

10. Merge the changes into ``develop`` and keep working::

      git checkout develop
      git merge master


The above steps are only an minimal example. Probably a release is made
of many features.

.. _`PyPI`: https://pypi.org/
