.. _tech_ref:

Technical reference
===================
* :ref:`aggregating_tech`
* :ref:`scores_tech`


.. _aggregating_tech:

Generating aggregated databases
-------------------------------

.. _presamplepackagecreation:

.. autoclass:: bw2agg.aggregate.DatabaseAggregator

The only method you will use after instantiating the ``DatabaseAggregator`` object is ``generate``, see o	:ref:`quickstart <aggregating>`.

.. automethod:: bw2agg.aggregate.DatabaseAggregator.generate

.. _scores_tech:

Adding unit impacts exchanges to biosphere and unit impact characterization factors to methods
-----------------------------------------------------------------------------------------------

These steps are done automatically by the ``DatabaseAggregator``. THey can however be called directly:

.. autofunction:: bw2agg.scores.add_unit_score_exchange_and_cf

.. autofunction:: bw2agg.scores.add_all_unit_score_exchanges_and_cfs