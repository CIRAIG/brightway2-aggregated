"""Tools for creating and using aggregated data in brightway2
-------------------------------------------------------------

Contains two modules

bwagg.scores
------------
- Set ot functions that augment methods and biosphere databases to allow storing
  aggregated single scores
    * add_unit_score_exchange_and_cf
    * add_all_unit_score_exchanges_and_cfs
- Function that create copies of activities that have cradle to gate scores
  as biosphere exchanges
- Function that calculates LCIA arrays from an LCI array (e.g. resulting from Monte Carlo)

bw2agg.aggregate
----------------
- Contains DatabaseAggregator class that can generate aggregated databases, at
  the LCI or LCIA score level.
"""
__all__ = [
    'DatabaseAggregator',
    'add_unit_score_exchange_and_cf',
    'add_all_unit_score_exchanges_and_cfs',
    'add_impact_scores_to_act',
]

from .aggregate import DatabaseAggregator
from .scores import add_unit_score_exchange_and_cf, \
    add_all_unit_score_exchanges_and_cfs, add_impact_scores_to_act

