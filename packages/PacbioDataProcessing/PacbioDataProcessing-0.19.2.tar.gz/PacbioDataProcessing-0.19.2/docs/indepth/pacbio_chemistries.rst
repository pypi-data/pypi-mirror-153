The PacBio chemistries
----------------------

PacBio sequencing generate output formats that are different depending
on the chemistry used in the sequencing. The change in the chemistries
are because these undergo improvements to produce better results,
however this also have produced a data incompatibility when processing
or comparisons are made between different chemistries.

These are some of the chemistries used by PacBio and they are related to
the versions of the kits used to process the DNA.

Chemistry table
~~~~~~~~~~~~~~~

=========== ============= ================ =========
BindingKit  SequencingKit Chemistry        System
=========== ============= ================ =========
100-356-300 100-356-200   P6-C4            RS
100-356-300 100-356-200   P6-C4            RS
100-356-300 100-612-400   P6-C4            RS
100-356-300 100-612-400   P6-C4            RS
100-372-700 100-356-200   P6-C4            RS
100-372-700 100-356-200   P6-C4            RS
100-372-700 100-612-400   P6-C4            RS
100-372-700 100-612-400   P6-C4            RS
100-619-300 100-620-000   S/P1-C1/beta     RS?
100-619-300 100-620-000   S/P1-C1/beta     RS?
100-619-300 100-867-300   S/P1-C1.1        RS?
100-619-300 100-867-300   S/P1-C1.1        RS?
100-619-300 100-867-300   S/P1-C1.1        RS?
100-619-300 100-902-100   S/P1-C1.2        RS?
100-619-300 100-902-100   S/P1-C1.2        RS?
100-619-300 100-902-100   S/P1-C1.2        RS?
100-619-300 100-902-100   S/P1-C1.2        RS?
100-619-300 100-902-100   S/P1-C1.2        RS?
100-619-300 100-972-200   S/P1-C1.3        RS?
100-619-300 100-972-200   S/P1-C1.3        RS?
100-619-300 100-972-200   S/P1-C1.3        RS?
100-619-300 100-972-200   S/P1-C1.3        RS?
100-862-200 101-093-700   S/P2-C2/5.0      Sequel
100-862-200 100-861-800   S/P2-C2/5.0      Sequel
100-862-200 101-309-400   S/P2-C2/5.0      Sequel
100-862-200 101-309-500   S/P2-C2/5.0      Sequel
101-365-900 100-861-800   S/P2-C2/5.0      Sequel
101-365-900 101-093-700   S/P2-C2/5.0      Sequel
101-365-900 101-309-400   S/P2-C2/5.0      Sequel
101-365-900 101-309-500   S/P2-C2/5.0      Sequel
101-500-400 101-427-500   S/P3-C3/5.0      Sequel
101-500-400 101-427-800   S/P3-C3/5.0      Sequel
101-500-400 101-646-800   S/P3-C3/5.0      Sequel
101-490-800 101-490-900   S/P3-C1/5.0-8M   Sequel II
101-490-800 101-491-000   S/P3-C1/5.0-8M   Sequel II
101-490-800 101-644-500   S/P3-C1/5.0-8M   Sequel II
101-490-800 101-717-100   S/P3-C1/5.0-8M   Sequel II
101-717-300 101-644-500   S/P3-C1/5.0-8M   Sequel II
101-717-300 101-717-100   S/P3-C1/5.0-8M   Sequel II
101-717-400 101-644-500   S/P3-C1/5.0-8M   Sequel II
101-717-400 101-717-100   S/P3-C1/5.0-8M   Sequel II
101-789-500 101-789-300   S/P4-C2/5.0-8M   Sequel II
101-820-500 101-789-300   S/P4.1-C2/5.0-8M Sequel II
101-789-500 101-826-100   S/P4-C2/5.0-8M   Sequel II
101-789-500 101-820-300   S/P4-C2/5.0-8M   Sequel II
101-820-500 101-826-100   S/P4.1-C2/5.0-8M Sequel II
101-820-500 101-820-300   S/P4.1-C2/5.0-8M Sequel II
101-894-200 101-826-100   S/P5-C2/5.0-8M   Sequel II
101-894-200 101-789-300   S/P5-C2/5.0-8M   Sequel II
101-894-200 101-820-300   S/P5-C2/5.0-8M   Sequel II
=========== ============= ================ =========

Adapted from on: \* `Reference
1 <https://github.com/PacificBiosciences/pbbam/blob/develop/src/ChemistryTable.cpp>`__
\* `Reference
2 <http://seqanswers.com/forums/archive/index.php/t-89140.html>`__ \*
`Reference 3 <https://ccs.how/faq/chemistry.html>`__

Chemistries in our data
~~~~~~~~~~~~~~~~~~~~~~~

=============== =========== ============= ========= ========
Name            BindingKit  SequencingKit Chemistry Platform
=============== =========== ============= ========= ========
pMA683          100356300   100612400     P6-C4     RS
pMA684          100356300   100612400     P6-C4     RS
pMA685          100356300   100612400     P6-C4     RS
OriC_enrichment 100-862-200 100-861-800   P2-C2     SEQUEL
1_A07-50pM      101-500-400 101-427-800   P3-C3     SEQUEL
4_D05-10pM      101-500-400 101-427-800   P3-C3     SEQUEL
2_B07-20pM      101-500-400 101-427-800   P3-C3     SEQUEL
1_A09->100pM    101-500-400 101-427-800   P3-C3     SEQUEL
=============== =========== ============= ========= ========
