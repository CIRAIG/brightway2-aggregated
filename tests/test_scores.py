from bw2agg.scores import add_all_unit_score_exchanges_and_cfs,\
    add_unit_score_exchange_and_cf
from brightway2 import projects, databases, methods, Database, Method, get_activity
import pytest


def test_add_unit_score_exchange_and_cf(data_for_testing):
    """ Augment methods and biosphere database for unit scores"""
    # Make sure project received with expected initial data (possibly delete
    # since this does not test the function, but rather the testing itself)
    projects.set_current(data_for_testing['project'])
    assert "biosphere" in databases
    method_name = data_for_testing['m1_name']
    assert method_name in methods

    assert len(Database('biosphere')) == 2
    loaded_biosphere_before = Database('biosphere').load()
    method = Method(method_name)
    loaded_method_before = method.load()
    assert len(loaded_method_before) == 2
    ef_code = method.get_abbreviation()
    assert ('biosphere', ef_code) not in loaded_biosphere_before

    # Augment method and biosphere database
    add_unit_score_exchange_and_cf(method=method_name, biosphere='biosphere')
    assert len(Database('biosphere')) == 3
    loaded_biosphere_after = Database('biosphere').load()
    assert ('biosphere', ef_code) in loaded_biosphere_after
    new_ef = get_activity(('biosphere', ef_code))
    assert new_ef['name'] == 'Unit impact for {}'.format(method_name)

    method = Method(method_name)
    loaded_method_after = method.load()
    assert len(loaded_method_after) == 3
    assert (('biosphere', ef_code), 1) in loaded_method_after

def test_add_unit_score_exchange_and_cf_no_such_method(data_for_testing):
    projects.set_current(data_for_testing['project'])
    assert "biosphere" in databases
    method_name = ('some', 'fake', 'method')
    with pytest.raises(ValueError) as exc_info:
        add_unit_score_exchange_and_cf(method_name, biosphere='biosphere')
    assert exc_info.value.args[0] == "Method ('some', 'fake', 'method') not in registered methods"

def test_add_unit_score_exchange_and_cf_no_such_biosphere(data_for_testing):
    projects.set_current(data_for_testing['project'])
    method_name = data_for_testing['m1_name']
    with pytest.raises(ValueError, match="Database biosphereXX not in registered databases"):
        add_unit_score_exchange_and_cf(method_name, biosphere='biosphereXX')

def test_add_unit_score_exchange_and_cf_act_exists(data_for_testing):
    projects.set_current(data_for_testing['project'])
    method_name = data_for_testing['m1_name']
    assert len(Database('biosphere')) == 2
    loaded_biosphere_before = Database('biosphere').load()
    method1_name = data_for_testing['m1_name']
    method1 = Method(method1_name)
    loaded_method1_before = method1.load()
    assert len(loaded_method1_before) == 2
    ef1_code = method1.get_abbreviation()
    assert ('biosphere', ef1_code) not in loaded_biosphere_before
    # Manually add ef to biosphere
    biosphere_data = Database('biosphere').load()
    biosphere_data[("biosphere", Method(method_name).get_abbreviation())] = {
            'name': 'Unit impact for {}'.format(method_name),
            'type': 'unit exchange',
            'unit': Method(method_name).metadata['unit']
        }
    Database('biosphere').write(biosphere_data)
    assert len(Database('biosphere')) == 3
    # run function, should not change the length of biosphere, but should add
    # cf to method
    add_unit_score_exchange_and_cf(method_name, biosphere='biosphere')
    loaded_method1_after = method1.load()
    assert len(loaded_method1_after) == 3
    assert len(Database('biosphere')) == 3


def test_add_all_unit_score_exchanges_and_cfs(data_for_testing):
    """ Augment methods and biosphere database for unit scores"""
    # Make sure project received with expected initial data (possibly delete
    # since this does not test the function, but rather the testing itself)
    projects.set_current(data_for_testing['project'])
    assert "biosphere" in databases
    assert len(methods) == 2
    assert len(Database('biosphere')) == 2

    loaded_biosphere_before = Database('biosphere').load()
    method1_name = data_for_testing['m1_name']
    method1 = Method(method1_name)
    loaded_method1_before = method1.load()
    assert len(loaded_method1_before) == 2
    ef1_code = method1.get_abbreviation()
    assert ('biosphere', ef1_code) not in loaded_biosphere_before
    method2_name = data_for_testing['m2_name']
    method2 = Method(method2_name)
    loaded_method2_before = method2.load()
    assert len(loaded_method2_before) == 2
    ef2_code = method2.get_abbreviation()
    assert ('biosphere', ef2_code) not in loaded_biosphere_before

    # Augment method and biosphere database
    add_all_unit_score_exchanges_and_cfs(biosphere='biosphere')

    assert len(Database('biosphere')) == 4

    loaded_biosphere_after = Database('biosphere').load()
    assert ('biosphere', ef1_code) in loaded_biosphere_after
    assert ('biosphere', ef2_code) in loaded_biosphere_after
    new_ef1 = get_activity(('biosphere', ef1_code))
    new_ef2 = get_activity(('biosphere', ef2_code))
    assert new_ef1['name'] == 'Unit impact for {}'.format(method1_name)
    assert new_ef2['name'] == 'Unit impact for {}'.format(method2_name)

    method1 = Method(method1_name)
    loaded_method1_after = method1.load()
    assert len(loaded_method1_after) == 3
    assert (('biosphere', ef1_code), 1) in loaded_method1_after

    method2 = Method(method2_name)
    loaded_method2_after = method2.load()
    assert len(loaded_method2_after) == 3
    assert (('biosphere', ef2_code), 1) in loaded_method2_after