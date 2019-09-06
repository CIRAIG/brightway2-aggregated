.. _quickstart:

Quickstart
==========

This section provides a brief overview of the use of brightway2-aggregated.

* :ref:`aggregating`
* :ref:`augmenting`

.. note::
    The package was developed as an extension to the `Brightway2 LCA framework <https://brightwaylca.org/>`_.

.. _aggregating :

Generating aggregated databases
-------------------------------

To generate an aggregated version of an existing unit process database, you need:

  - to have brightway2 installed
  - a project with a unit process database you want to aggregate

If you want to aggregate all the way to cradle-to-gate scores (which you probably do), you also need a list of method ids.

.. warning::
    Aggregating at the LCI level generates very dense biosphere matrices. Because Brightway2 has been optimized to work
    with sparse matrices, this slows down calculations considerably.


.. code-block:: python

    >>> import brightway2 as bw
    >>> from bw2agg.aggregate import DatabaseAggregator
    >>> bw.projects.set_current('my project')

    # Create an aggregated database generator
    >>> agg_db = DatabaseAggregator(
    ...     up_db_name="Name of the unit process database",
    ...     agg_db_name="Name of the aggregated database",
    ...     database_type="LCIA", # or "LCI"
    ...     method_list=[('my', 'first', 'method'), ('my', 'second', 'method')], # Actual method ids
    ...     overwrite=False
    ... )

    # Generate and write aggregated database
    >>> agg_db.generate()
    Writing activities to SQLite3 database:
    0% [##############################] 100% | ETA: 00:00:00
    Total time elapsed: 00:03:37


More details on the function can be found :ref:`in the technical reference page <aggregating_tech>`.

.. _augmenting :

Preparing Brightway2 for use of cradle-to-gate scores
-----------------------------------------------------
In order to convert an LCI database to a cradle-to-gate LCIA scores database, and to use this aggregated database, two
things are needed:

  - New biosphere exchanges that represent the "unit impact scores". For example, say you want to have a database that
    contains precalculated cradle-to-gate climate change impact scores (i.e. carbon footprints), all the biosphere
    exchanges in the inventory need to be replaced with a single "unit score for climate change" biosphere exchange.
  - For this new biosphere exchange to be used in future LCIA, a new characterization factor, equal to 1, needs to be
    added for the "unit score for climate change" biosphere exchange.

These new exchanges and characterization factors are added automatically for the selected methods by the
``DatabaseAggregator``. However, it is possible to preemptively create these for a single method
``bw2agg.scores.add_unit_score_exchange_and_cf(method_id)``, or all methods
(``bw2agg.scores.add_all_unit_score_exchanges_and_cfs()``).
