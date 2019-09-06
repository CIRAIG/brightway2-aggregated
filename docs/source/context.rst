.. _context:

Context
================================

Inventory data usually contains three types of exchanges:

  - Production exchanges, which represent the actual functional output of a given activity;
  - Technosphere exchanges, which represent the exchange of products between activities;
  - Elementary flows (called biosphere exchanges in Brightway2), which represent the exchanges between activities in the
    technosphere and the environment.

To calculate an impact score for a given functional unit, one needs to:

  1) scale all activities so that they supply exactly one functional unit (i.e. solve a system of linear equations),
     which is computation-intensive.
  2) Multiply the biosphere exchanges of each activity by the scaling factors obtained in the previous step, resulting in
     a life cycle inventory, normally containing hundreds or thousands of scaled biosphere exchanges.
  3) Multiply the scaled biosphere exchanges with characterization factors (impact per unit biosphere exchange).

Brightway2-aggregated does two things that simplifies these steps:

  1) It can store the solution to steps 1 and 2 for a given database, effectively eliminating the need to rescale the
     technosphere and biosphere exchanges each time one carries out an LCA. It does this by creating an
     "aggregated LCI database" (exactly like the "system" database supplied by ecoinvent).
  2) It can store the solution to steps 1, 2 and 3 for a given database, i.e. calculate cradle-to-gate impact scores for
     all possible outputs of a database.

These levels of simplification can be useful in some contexts:

  - Storing aggregated LCI data will slow down actual calculations in Brightway2 (because aggregated LCI are dense, and
    Brightway2 is optimised to work with sparse data). However, the LCI data can be associated with
    `presamples <https://presamples.readthedocs.io>`_, allowing the reuse of e.g. Monte Carlo results.
  - The real strength of Brightway2-aggregated is when databases store LCIA scores. This allows one to lightweight
    databases and calculations, useful when creating LCA tools. LCIA scores also play very well with presamples.

