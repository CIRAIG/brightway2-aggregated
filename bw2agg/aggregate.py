import brightway2 as bw
from .scores import add_unit_score_exchange_and_cf
import copy

class DatabaseAggregator(object):
    def __init__(self,
                 up_db_name,
                 agg_db_name,
                 database_type='LCIA',
                 method_list=list(bw.methods),
                 biosphere='biosphere3',
                 overwrite=False
                 ):
        """ Generator to aggregate and write an LCI database

        Can be used to generate either:
            - an aggregated LCI database (i.e. a database with cradle-to-gate
              LCI stored in the biosphere matrix)
            - an aggregated LCIA database (i.e. a database with cradle-to-gate
              characterized inventories stored in the biosphere matrix as "unit
              impact" biosphere exchanges). This requires the creation of unit
              impact characterization factors and biosphere exchanges.

        Instantiating the class will generate the data for the new database.
        The `generate` method will write the database.

        Parameters
        ----------
        up_db_name: str
            Name of the unit process database from which results will be
            calculated. Must be a registered database name.
        agg_db_name: str
            Name of the new aggregated database.
        database_type: {'LCI', 'LCIA'}, default 'LCIA'
                Type of aggregated database to generate. 'LCIA' generates a
                database with cradle-to-gate inventories stored in the
                biosphere matrix as "unit impact" biosphere exchanges, while 'LCI'
                generates a database with cradle-to-gate LCI stored in the
                biosphere matrix.
                Note that performance of LCI aggregated databases is very poor
                due to Brightway2 assuming sparse matrices
            method_list: list, default list(bw.methods)
                List of method ids (tuples) for which to generate LCIA scores.
                Default is all methods.
            biosphere: str, default 'biosphere3'
                Name of the biosphere database
            overwrite: bool, default False
                Determines whether an existing database with name `agg_db_name`
                will be overwritten.
        """
        assert up_db_name in bw.databases, "Source database does not exist"
        if agg_db_name in bw.databases and not overwrite:
            print("A database named {} already exists, set `overwrite` to True to overwrite")
            return
        self.source = bw.Database(up_db_name)
        self.new_name = agg_db_name
        self.biosphere = biosphere
        self.lca = bw.LCA({self.source.random(): 1})
        self.lca.lci(factorize=True)
        self.database_type = database_type
        self.methods = method_list
        if self.database_type not in ['LCI', 'LCIA']:
            raise ValueError(
                '{} is not a valid database type, should be "LCI" or "LCIA"'.format(
                    self.database_type
                )
            )
        if self.database_type == "LCIA":
            assert self.methods
            for m in self.methods:
                add_unit_score_exchange_and_cf(m, biosphere)
            self.C_matrices = {}

    def __len__(self):
        return len(self.source)

    def __iter__(self):
        # Data for this line:
        # wrong_database = {key[0] for key in data}.difference({self.name})
        yield ((self.new_name,))

    def _get_exchanges(self):
        vector = self.lca.inventory.sum(axis=1)
        assert vector.shape == (len(self.lca.biosphere_dict), 1)
        return [{
            'input': flow,
            'amount': float(vector[index]),
            'type': 'biosphere',
        } for flow, index in self.lca.biosphere_dict.items()
            if abs(float(vector[index])) > 1e-17]

    def _create_C_matrices(self):
        self.C_matrices = {}
        for method in self.methods:
            self.lca.switch_method(method)
            self.C_matrices[method] = self.lca.characterization_matrix
        return self.C_matrices

    def _get_impacts(self, biosphere='biosphere3'):
        if len(self.C_matrices) == 0:
            self._create_C_matrices()
        return [{
            'input': (biosphere, bw.Method(method).get_abbreviation()),
            'amount': (C_matrix * self.lca.inventory).sum(),
            'type': 'biosphere',
            'name': 'Unit impact for {}'.format(method),
            'unit': bw.Method(method).metadata['unit']
        } \
            for method, C_matrix in self.C_matrices.items()]

    def keys(self):
        # Data for this line:
        # mapping.add(data.keys())
        for act in self.source:
            yield (self.new_name, act['code'])

    def values(self):
        # Data for this line:
        # geomapping.add({x["location"] for x in data.values() if x.get("location")})
        for act in self.source:
            yield act

    def items(self):
        # Actual data which is consumed by the function writing to the database
        for act in self.source:
            self.lca.redo_lci({act: act['production amount']})
            obj = copy.deepcopy(act._data)
            obj['database'] = self.new_name
            if self.database_type == "LCI":
                obj['exchanges'] = self._get_exchanges()
            elif self.database_type == "LCIA":
                obj['exchanges'] = self._get_impacts(biosphere=self.biosphere)
                assert len(obj['exchanges']) == len(self.methods)
            else:
                raise ValueError('Database type not understood, expected LCI or LCIA, got {}'.format(self.database_type))
            obj['exchanges'].append(
               {
                   'input': (self.new_name, act['code']),
                   'type': 'production',
                   'amount': act['production amount'],
               }
            )
            yield ((self.new_name, obj['code']), obj)

    def generate(self):
        bw.Database(self.new_name).write(self)
