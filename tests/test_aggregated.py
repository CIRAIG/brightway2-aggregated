import pytest
from brightway2 import Database, Method, methods, LCA, projects, \
    databases, get_activity

from bw2agg.aggregate import add_unit_score_exchange_and_cf, DatabaseAggregator
from bw2agg.scores import add_all_unit_score_exchanges_and_cfs, add_impact_scores_to_act


def test_aggregated_LCIA_single_method_augment_on_fly(data_for_testing):
    projects.set_current(data_for_testing['project'])
    assert "techno_UP" in databases
    assert "biosphere" in databases
    assert "techno_agg_LCIA" not in databases
    assert data_for_testing['m1_name'] in methods

    DatabaseAggregator(
        up_db_name="techno_UP", agg_db_name="techno_agg_LCIA", database_type='LCIA',
        method_list=[data_for_testing['m1_name']], biosphere='biosphere', overwrite=False
    ).generate()

    assert "techno_agg_LCIA" in databases
    assert len(Database("techno_agg_LCIA"))==len(Database("techno_UP"))

    lca_unit_process = LCA({("techno_UP", "A"):1}, method=data_for_testing['m1_name'])
    lca_unit_process.lci()
    lca_unit_process.lcia()

    lca_LCIA = LCA({("techno_agg_LCIA", "A"):1}, method=data_for_testing['m1_name'])
    lca_LCIA.lci()
    lca_LCIA.lcia()
    assert lca_unit_process.score == lca_LCIA.score


def test_aggregated_LCIA_single_method_already_augmented(data_for_testing):
    projects.set_current(data_for_testing['project'])
    assert "techno_UP" in databases
    assert "biosphere" in databases
    assert "techno_agg_LCIA" not in databases
    assert data_for_testing['m1_name'] in methods

    add_unit_score_exchange_and_cf(method=data_for_testing['m1_name'], biosphere='biosphere')
    DatabaseAggregator(
        up_db_name="techno_UP", agg_db_name="techno_agg_LCIA", database_type='LCIA',
        method_list=[data_for_testing['m1_name']], biosphere='biosphere', overwrite=False
    ).generate()

    assert "techno_agg_LCIA" in databases
    assert len(Database("techno_agg_LCIA"))==len(Database("techno_UP"))

    lca_unit_process = LCA({("techno_UP", "A"):1}, method=data_for_testing['m1_name'])
    lca_unit_process.lci()
    lca_unit_process.lcia()

    lca_LCIA = LCA({("techno_agg_LCIA", "A"):1}, method=data_for_testing['m1_name'])
    lca_LCIA.lci()
    lca_LCIA.lcia()
    assert lca_unit_process.score == lca_LCIA.score


def test_aggregated_LCIA_multiple_methods_already_augmented(data_for_testing):
    projects.set_current(data_for_testing['project'])
    assert "techno_UP" in databases
    assert "biosphere" in databases
    assert "techno_agg_LCIA" not in databases
    assert data_for_testing['m1_name'] in methods
    assert data_for_testing['m2_name'] in methods
    assert len(methods)==2

    add_all_unit_score_exchanges_and_cfs(biosphere='biosphere')
    agg_db = DatabaseAggregator(
        up_db_name="techno_UP", agg_db_name="techno_agg_LCIA", database_type='LCIA',
        method_list=[data_for_testing['m1_name'], data_for_testing['m2_name']], biosphere='biosphere', overwrite=False
    ).generate()

    assert "techno_agg_LCIA" in databases
    assert len(Database("techno_agg_LCIA"))==len(Database("techno_UP"))

    lca_unit_process = LCA({("techno_UP", "A"):1}, method=data_for_testing['m1_name'])
    lca_unit_process.lci()
    lca_unit_process.lcia()

    lca_LCIA = LCA({("techno_agg_LCIA", "A"):1}, method=data_for_testing['m1_name'])
    lca_LCIA.lci()
    lca_LCIA.lcia()
    assert lca_unit_process.score == lca_LCIA.score
    score_in_B = lca_LCIA.biosphere_matrix[
        lca_LCIA.biosphere_dict[('biosphere', Method(data_for_testing['m1_name']).get_abbreviation())],
        lca_LCIA.activity_dict[("techno_agg_LCIA", "A")]
    ]
    assert score_in_B == lca_LCIA.score

    lca_unit_process = LCA({("techno_UP", "A"):1}, method=data_for_testing['m2_name'])
    lca_unit_process.lci()
    lca_unit_process.lcia()

    lca_LCIA = LCA({("techno_agg_LCIA", "A"):1}, method=data_for_testing['m2_name'])
    lca_LCIA.lci()
    lca_LCIA.lcia()
    assert lca_unit_process.score == lca_LCIA.score
    score_in_B = lca_LCIA.biosphere_matrix[
        lca_LCIA.biosphere_dict[('biosphere', Method(data_for_testing['m2_name']).get_abbreviation())],
        lca_LCIA.activity_dict[("techno_agg_LCIA", "A")]
    ]
    assert score_in_B == lca_LCIA.score


def test_aggregated_LCIA_multiple_methods_augment_on_fly(data_for_testing):
    projects.set_current(data_for_testing['project'])
    assert "techno_UP" in databases
    assert "biosphere" in databases
    assert "techno_agg_LCIA" not in databases
    assert data_for_testing['m1_name'] in methods
    assert data_for_testing['m2_name'] in methods
    assert len(methods)==2

    DatabaseAggregator(
        up_db_name="techno_UP", agg_db_name="techno_agg_LCIA", database_type='LCIA',
        method_list=[data_for_testing['m1_name'], data_for_testing['m2_name']], biosphere='biosphere', overwrite=False
    ).generate()

    assert "techno_agg_LCIA" in databases
    assert len(Database("techno_agg_LCIA"))==len(Database("techno_UP"))

    lca_unit_process = LCA({("techno_UP", "A"):1}, method=data_for_testing['m1_name'])
    lca_unit_process.lci()
    lca_unit_process.lcia()

    lca_LCIA = LCA({("techno_agg_LCIA", "A"):1}, method=data_for_testing['m1_name'])
    lca_LCIA.lci()
    lca_LCIA.lcia()
    assert lca_unit_process.score == lca_LCIA.score
    score_in_B = lca_LCIA.biosphere_matrix[
        lca_LCIA.biosphere_dict[('biosphere', Method(data_for_testing['m1_name']).get_abbreviation())],
        lca_LCIA.activity_dict[("techno_agg_LCIA", "A")]
    ]
    assert score_in_B == lca_LCIA.score

    lca_unit_process = LCA({("techno_UP", "A"):1}, method=data_for_testing['m2_name'])
    lca_unit_process.lci()
    lca_unit_process.lcia()

    lca_LCIA = LCA({("techno_agg_LCIA", "A"):1}, method=data_for_testing['m2_name'])
    lca_LCIA.lci()
    lca_LCIA.lcia()
    assert lca_unit_process.score == lca_LCIA.score
    score_in_B = lca_LCIA.biosphere_matrix[
        lca_LCIA.biosphere_dict[('biosphere', Method(data_for_testing['m2_name']).get_abbreviation())],
        lca_LCIA.activity_dict[("techno_agg_LCIA", "A")]
    ]
    assert score_in_B == lca_LCIA.score


def test_aggregated_LCI(data_for_testing):
    projects.set_current(data_for_testing['project'])
    assert "techno_UP" in databases
    assert "biosphere" in databases
    assert "techno_agg_LCI" not in databases
    assert data_for_testing['m1_name'] in methods

    agg_db = DatabaseAggregator(
        up_db_name="techno_UP", agg_db_name="techno_agg_LCI", database_type='LCI',
        method_list=[data_for_testing['m1_name']], biosphere='biosphere', overwrite=False
    ).generate()

    assert "techno_agg_LCI" in databases
    assert len(Database("techno_agg_LCI"))==len(Database("techno_UP"))

    lca_unit_process = LCA({("techno_UP", "A"):1}, method=data_for_testing['m1_name'])
    lca_unit_process.lci()
    lca_unit_process.lcia()

    lca_LCI = LCA({("techno_agg_LCI", "A"):1}, method=data_for_testing['m1_name'])
    lca_LCI.lci()
    lca_LCI.lcia()

    for act, col in lca_LCI.activity_dict.items():
        row = lca_LCI.product_dict[act]
        # Make sure production is 1
        assert lca_LCI.technosphere_matrix[row, col] == 1.0
        # Make sure other elements of the technosphere matrix are 0
        #assert lca_LCI.technosphere_matrix.sum(axis=0)[col]==1
    for ef, ef_row in lca_unit_process.biosphere_dict.items():
        up_lci = lca_unit_process.inventory.sum(axis=1)[ef_row]
        LCI_lci = lca_LCI.biosphere_matrix[
            lca_LCI.biosphere_dict[ef], 
            lca_LCI.activity_dict[("techno_agg_LCI", "A")]
        ]
        assert up_lci == LCI_lci
    assert lca_unit_process.score == lca_LCI.score

def test_add_impact_scores_to_act_non_existing_db(data_for_testing):
    """Test adding agg dataset to non-existing database"""
    assert 'agg' not in databases

    with pytest.raises(ValueError):
        add_impact_scores_to_act(
            act_code='A', agg_db='agg', up_db='techno_UP',
            selected_methods=[data_for_testing['m1_name'], data_for_testing['m2_name']], biosphere='biosphere',
            overwrite=False, create_ef_on_the_fly=True, create_agg_database_on_fly=False
        )

    add_impact_scores_to_act(
        act_code='A', agg_db='agg', up_db='techno_UP',
        selected_methods=[data_for_testing['m1_name'], data_for_testing['m2_name']], biosphere='biosphere',
        overwrite=False, create_ef_on_the_fly=True, create_agg_database_on_fly=True
    )
    assert 'agg' in databases
    assert len(Database('agg'))==1
    assert ('agg', 'A') in Database('agg')
    act = get_activity(('agg', 'A'))
    assert len([_ for _ in act.biosphere()]) == 2


def test_add_impact_scores_to_act_existing_db(data_for_testing):
    """Test adding agg dataset to existing database"""
    Database('agg').register()
    assert 'agg' in databases
    assert len(Database('agg')) == 0

    add_impact_scores_to_act(
        act_code='A', agg_db='agg', up_db='techno_UP',
        selected_methods=[data_for_testing['m1_name'], data_for_testing['m2_name']], biosphere='biosphere',
        overwrite=False, create_ef_on_the_fly=True, create_agg_database_on_fly=False
    )

    assert 'agg' in databases
    assert len(Database('agg'))==1
    assert ('agg', 'A') in Database('agg')
    act = get_activity(('agg', 'A'))
    act_bio_exc = {exc.input.key: exc['amount'] for exc in act.biosphere()}
    assert len(act_bio_exc) == 2

    lca = LCA({('techno_UP', 'A'):1}, method=data_for_testing['m1_name'])
    lca.lci()
    lca.lcia()
    assert lca.score == act_bio_exc[('biosphere', Method(data_for_testing['m1_name']).get_abbreviation())]
    lca.switch_method(method=data_for_testing['m2_name'])
    lca.lcia()
    assert lca.score == act_bio_exc[('biosphere', Method(data_for_testing['m2_name']).get_abbreviation())]
