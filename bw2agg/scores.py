import brightway2 as bw
import pyprind
import copy
import numpy as np
from .utils import copy_stripped_activity_to_other_db


def add_unit_score_exchange_and_cf(method, biosphere='biosphere3'):
    """ Add unit score biosphere exchanges and cfs to biosphere and methods.

    Allows the storing of LCIA results in the B matrix for LCI datasets. Makes
    changes inplace and does not return anything.

    Parameters
    ----------

    method: tuple
        Identification of the LCIA method, using Brightway2 tuple identifiers

    biosphere: str, default `biosphere3`
        Name of the biosphere database where biosphere exchanges are stored

    Note
    ----

    This function is invoked directly by the DatabaseAggregator

    """
    if method not in bw.methods:
        raise ValueError("Method {} not in registered methods".format(method))
    if biosphere not in bw.databases:
        raise ValueError("Database {} not in registered databases".format(biosphere))

    m = bw.Method(method)
    ef_code = m.get_abbreviation()
    ef_name = 'Unit impact for {}'.format(method)

    # Add to biosphere database, skip if already present
    try:
        ef = bw.get_activity((biosphere, ef_code))
        assert ef['name'] == ef_name
    except:
        ef = bw.Database(biosphere).new_activity(code=ef_code)
        ef['name'] = ef_name
        ef['unit'] = m.metadata['unit']
        ef['categories'] = ('undefined',)
        ef['exchanges']: []
        ef['type'] = 'unit impact exchange'
        ef.save()
        try:
            bw.mapping[(biosphere, ef_code)]
        except KeyError:
            print("Manually added {} to mapping".format(ef_code))
            bw.mapping.add((biosphere, ef_code))
    # Add to associated method, skip if already present
    loaded_method = m.load()
    try:
        existing_cf = [
            cf_tuple for cf_tuple in loaded_method
            if cf_tuple[0] == (biosphere, ef_code)
        ][0]
        assert existing_cf[1] == 1
    except:
        loaded_method.append(((biosphere, m.get_abbreviation()), 1))
        bw.Method(method).write(loaded_method)


def add_all_unit_score_exchanges_and_cfs(biosphere='biosphere3'):
    """Add unit scores and cfs for all methods in project.

    Makes changes inplace and does not return anything.

    Parameters
    ----------

    biosphere: str, default `biosphere3`
       Name of the biosphere database where biosphere exchanges are stored
    """
    print("Adding unit score biosphere exchanges and characterization factors "
          "to all {} methods in project".format(len(bw.methods))
          )
    for method in pyprind.prog_bar(bw.methods):
        add_unit_score_exchange_and_cf(method, biosphere=biosphere)


def add_impact_scores_to_act(act_code, agg_db, up_db, selected_methods,
                             overwrite=False, create_ef_on_the_fly=False,
                             biosphere='biosphere3',
                             create_agg_database_on_fly=False):
    """ Add unit impact scores to biosphere exchanges of activity in agg database

    The up_db is the unit process level database used for the calculations.
    The elementary flow code is Method(method).get_abbreviation()
    The elementary flow unit is Method(method).metadata['unit']
    The elementary flow name is 'Unit impact for {}'.format(method)
    """
    # Make sure unit process dataset exists
    assert (up_db, act_code) in bw.Database(up_db), "Activity missing from unit process database"
    up_act = bw.get_activity((up_db, act_code))
    # Create aggregated dataset if required
    if not (agg_db, act_code) in bw.Database(agg_db):
        agg_act = copy_stripped_activity_to_other_db(
            data=copy.deepcopy(up_act._data),
            target_db=agg_db,
            create_database_on_fly=create_agg_database_on_fly)
    else:
        agg_act = bw.get_activity((agg_db, act_code))

    existing_biosphere_in_agg = [exc.input.key for exc in agg_act.biosphere()]
    up_production_amount = up_act['production amount']

    lca = bw.LCA({up_act:up_production_amount})
    lca.lci()
    for method in selected_methods:
        m = bw.Method(method)
        ef_code = m.get_abbreviation()
        ef_name = 'Unit impact for {}'.format(method)
        result_already_in_act = (biosphere, ef_code) in existing_biosphere_in_agg
        if result_already_in_act:
            print("Results already exist for activity {}, category {}".format(agg_act, selected_methods))
            if not overwrite:
                print("Set overwrite=True to replace value")
            if overwrite:
                potential_exc = [exc for exc in agg_act.biosphere() if exc.input.key == (biosphere, ef_code)]
                if len(potential_exc) > 1:
                    raise ValueError(
                        "More than one corresponding exchange found. activity: {}, exchange:{}".format(
                            agg_act, method
                        )
                    )
                else:
                    exc = potential_exc[0]
        if not (biosphere, ef_code) in bw.Database(biosphere):
            if not create_ef_on_the_fly:
                raise ValueError('{} needs to be added to biosphere database'.format(ef_name))
            else:
                add_unit_score_exchange_and_cf(method, biosphere=biosphere)

        lca.switch_method(method)
        lca.lcia()
        if not result_already_in_act:
            exc = agg_act.new_exchange(
                input=(biosphere, ef_code),
                output=agg_act.key,
                amount=lca.score,
                unit=m.metadata['unit'],
            )
            exc['type'] = 'biosphere'
        else:
            exc['amount'] = lca.score
        exc.save()


# def calculate_LCIA_array_from_LCI_array(LCI_array, method, ref_bio_dict, result_precision='float32'):
#     """ Calculate a 1xn array of LCIA results from existing mxn LCI results array
#
#     The reference biosphere dictionary (ref_bio_dict) provides a mapping between
#     biosphere exchange keys and their corresponding rows in the LCI
#     array, i.e. its values are (bio_db_name, code): row_number_in_LCI_array
#     """
#     # Get a list of elementary flows that are characterized in the given method
#     loaded_method = bw.Method(method).load()
#     method_ordered_exchanges = [exc[0] for exc in loaded_method]
#
#     # Collectors for the LCI array indices and characterization factors that
#     # are relevant for the impact assessment (i.e. those that have
#     # characterization factors for the given method)
#     lca_specific_biosphere_indices = []
#     cfs = []
#     for exc in method_ordered_exchanges:  # For every exchange that has a cf
#         try:
#             # Check to see if it is in the bio_dict
#             # If it is, it is in the inventory, and its index is bio_dict[exc]
#             lca_specific_biosphere_indices.append(ref_bio_dict[exc])
#             # If it is in bio_dict, we need its characterization factor
#             cfs.append(dict(loaded_method)[exc])
#         except KeyError: # Exchange was not in bio_dict
#             pass
#
#     # Extract elements of the LCI array that are characterized,
#     # in the correct order
#     filtered_LCI_array = LCI_array[lca_specific_biosphere_indices][:]
#     # Convert CF list to CF array
#     cf_array = np.reshape(np.array(cfs), (-1, 1))
#     # LCIA score = sum of multiplication of inventory result and CF
#     LCIA_array = (np.array(filtered_LCI_array) * cf_array).sum(axis=0)
#     # Change result precision if needed
#     if LCIA_array.dtype != result_precision:
#         LCIA_array = LCIA_array.astype(result_precision, copy=False)
#     return LCIA_array
#
#
# class CharacterizedBiosphereDatabaseGenerator(object):
#     def __init__(self,
#                  up_db_name,
#                  score_db_name,
#                  method_list=list(bw.methods),
#                  biosphere='biosphere3',
#                  overwrite=False
#                  ):
#         """ Generate an LCI database where biosphere exchanges are replaced with gate-to-gate single scores
#
#         #TODO: Refactor to speedup: currently runs at unbearably slow speed
#         Instantiating the class will generate the data for the new database.
#         The `generate` method will write the database.
#
#         Parameters
#         ----------
#         up_db_name: str
#             Name of the unit process database from which results will be
#             calculated. Must be a registered database name.
#         score_db_name: str
#             Name of the new aggregated database.
#         method_list: list, default list(bw.methods)
#             List of method ids (tuples) for which to generate LCIA scores.
#             Default is all methods.
#         biosphere: str, default 'biosphere3'
#             Name of the biosphere database
#         overwrite: bool, default False
#             Determines whether an existing database with name `score_db_name`
#             will be overwritten.
#         """
#         print("WARNING: WIP. Runs at very slow speeds, needs to be refactored. We suggest halting unless you really need this.")
#         assert up_db_name in bw.databases, "Source database does not exist"
#         if score_db_name in bw.databases and not overwrite:
#             print("A database named {} already exists, set `overwrite` to True to overwrite").format(score_db_name)
#             return
#         self.source = bw.Database(up_db_name)
#         self.new_name = score_db_name
#         self.biosphere = biosphere
#         self.lca = bw.LCA({self.source.random(): 1})
#         self.lca.lci()
#         self.methods = method_list
#         self._get_impacts()
#
#     def check_methods(self):
#         for method in self.methods:
#             m = bw.Method(method)
#             ef_code = m.get_abbreviation()
#             if (self.biosphere, ef_code) not in bw.Database(self.biosphere):
#                 raise ValueError("Unit biosphere exchange for {} not in {} "
#                                  "database".format(method, self.biosphere)
#                 )
#             if (self.biosphere, ef_code) in [cf[0] for cf in m.load()]:
#                 raise ValueError("Unit impact characterization factor doesn't exist"
#                                  "for {} ".format(method)
#                 )
#
#     def __len__(self):
#         return len(self.source)
#
#     def __iter__(self):
#         # Data for this line:
#         # wrong_database = {key[0] for key in data}.difference({self.name})
#         yield ((self.new_name,))
#
#     def _get_techno_exchanges(self, act):
#         excs = []
#         for techno in act.technosphere():
#             data = techno.as_dict()
#             data['input'] = (self.new_name, data['input'][1])
#             data['output'] = (self.new_name, data['output'][1])
#             excs.append(data)
#         for prod in act.production():
#             data = prod.as_dict()
#             data['input'] = (self.new_name, data['input'][1])
#             data['output'] = (self.new_name, data['output'][1])
#             excs.append(data)
#         return excs
#
#     def _get_impacts(self):
#         self.impact_dict = {}
#         for method in self.methods:
#             self.lca.switch_method(method)
#             self.impact_dict[method] = (
#                     self.lca.characterization_matrix \
#                     * self.lca.biosphere_matrix.toarray()
#             ).sum(axis=0)
#
#     def _get_scores(self, act):
#         return [
#             {
#                 'input': (self.biosphere, bw.Method(method).get_abbreviation()),
#                 'output': (self.new_name, act['code']),
#                 'amount': self.impact_dict[method][self.lca.activity_dict[act.key]],
#                 'name': 'Unit impact for {}'.format(method),
#                 'unit': bw.Method(method).metadata['unit'],
#                 'comment': "Aggregated gate-to-gate impact for {}".format(method),
#                 'type': 'biosphere',
#                 'uncertainty type': 0,
#
#             } for method in self.methods
#         ]
#
#     def keys(self):
#         # Data for this line:
#         # mapping.add(data.keys())
#         for act in self.source:
#             yield (self.new_name, act['code'])
#
#     def values(self):
#         # Data for this line:
#         # geomapping.add({x["location"] for x in data.values() if x.get("location")})
#         for act in self.source:
#             yield act
#
#     def items(self):
#         # Actual data which is consumed by the function writing to the database
#         for i, act in enumerate(self.source):
#             self.lca.redo_lci({act: act['production amount']})
#             obj = copy.deepcopy(act._data)
#             obj['database'] = self.new_name
#             techno = self._get_techno_exchanges(act)
#             scores = self._get_scores(act)
#             print(i, act, len(techno), len(scores))
#
#             obj['exchanges'] = techno + scores
#             yield ((self.new_name, obj['code']), obj)
#
#     def generate(self):
#         bw.Database(self.new_name).write(self)