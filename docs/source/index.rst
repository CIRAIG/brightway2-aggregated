.. brightway2-aggregated documentation master file, created by
   sphinx-quickstart on Thu Sep  5 15:48:18 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Brightway2-aggregated
======================================

Brightway2-aggregated is an extension to the Brightway2 LCA framework to generate aggregated data.

It operates at two levels:

- aggregated LCI level (cradle-to-gate inventories), though this is not recommended because Brightway2 is
  optimized to work with sparse matrices, and the biosphere matrix of aggregated LCI databases are very dense)

- aggregated LCIA score (cradle-to-gate impact assessment score)

The ``DatabaseAggregator`` will calculate the LCI (and, optionally, the LCIA) for all activities in the database and
store the results in a new database. The activities in the resulting database will:

  - have a production exchange identical to the production exchange in the unit process database
  - have no further technosphere (i.e. there will be no off-diagonal elements in the **A** matrix)
  - Have either:

     * cradle-to-gate LCI results stored as biosphere exchanges (resulting in a dense biosphere matrix **B**), or
     * cradle-to-gate LCIA results stored as biosphere exchanges. The biosphere matrix (**B**) will therefore have as many
       rows as there are impact assessment methods of interest. This entails the creation of new "unit impact" biosphere
       exchanges, see :ref:`the section on preparing Brightway2 for use of cradle-to-gate scores <augmenting>`

While there are many reasons for using aggregated data, this module was specifically created to play well with
`presamples <https://presamples.readthedocs.io>`_, where aggregated data can be associated with presampled data
generated from e.g. Monte Carlo simulations.


.. toctree::
   :maxdepth: 2

   context
   quickstart
   tech_ref
   installing
   contributing
