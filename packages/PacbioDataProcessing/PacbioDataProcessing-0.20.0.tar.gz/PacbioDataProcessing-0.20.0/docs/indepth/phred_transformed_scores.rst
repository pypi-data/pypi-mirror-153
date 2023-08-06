.. _phred-transformed-scores:

Phred transformed scores
========================

:Author: David Palao
:Date: 17 August 2021
:Last updated: 17 August 2021
:Version: ---
:Tags: sm-analysis ipdSummary PacbioDataProcessing quality-value probability
       
:abstract:

   ``ipdSummary`` and ``blasr`` provide some *phred transformed quality values*.
   This document describes briefly what is meaning of this and how different
   *phred transformed quality values* could be combined in a sensible way.


Definitions
-----------

Base calling
  is the process of assigning a nucleobase (C, A, T or G) to the physical response
  of the device used to sequence a piece of DNA.


*Phred-transformed* scores or *phred quality scores*
  The probability of having an error in the identification process of one event
  is said to be *phred-transformed* if we write it as a quality value in the
  following way:

  .. math::

     Q\,=\,-10\,\log_{10}(P^{(\mathrm{e})})

  or, expressed in a more direct way:

  .. math::
     :label: QV-from-probability
	     
     Q\,=\,-10\,\log_{10}(1-P^{(\mathrm{ok})})

     

Combining quality values
------------------------

If some molecule has several events associated with it (e.g. several methylations)
each of them with a quality value, is it possible to combine those quality values
in a single global quality value?

For each quality value:

  .. math::

   Q_1, Q_2, \ldots, Q_n

we can compute the probability of having a wrong result:

  .. math::

   P^{(\mathrm{e})}_1, P^{(\mathrm{e})}_2, \ldots, P^{(\mathrm{e})}_n

and combine them to have the joint probability of having a correct result:

  .. math::

   P^{(\mathrm{ok})}\,=\,\prod_i\left(1-P^{(\mathrm{e})}_i\right)

then, a global quality value is computed straightforwardly from equation
:math:numref:`QV-from-probability`.

.. note::
   Using directly the product of probabilities of having an
   error would produce the wrong quality value, since the product of
   error probabilities is the joint probability of having
   *all measurements wrong*, and not the probability of having
   *any measurement wrong*, which is the desired quantity to compute
   the quality value. Therefore the mean value of qualities is not
   meaningful in this context, as a joint measure of quality.
