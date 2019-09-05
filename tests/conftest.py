import pytest
from bw2data.tests import bw2test
from brightway2 import Database, Method, methods, projects
from shutil import rmtree

@pytest.fixture
@bw2test
def data_for_testing():
    # Make sure we are starting off with an empty project
    assert not len(Database('techno_UP'))
    assert not len(Database('techno_LCI'))
    assert not len(Database('techno_LCIA'))
    assert not len(Database('biosphere'))
    assert not len(methods)

    biosphere = Database("biosphere")
    biosphere.register()
    biosphere.write({
        ("biosphere", "1"): {
            'categories': ['things'],
            'exchanges': [],
            'name': 'an emission',
            'type': 'emission',
            'unit': 'kg'
        },
        ("biosphere", "2"): {
            'categories': ['other things'],
            'exchanges': [],
            'name': 'another emission',
            'type': 'emission',
            'unit': 'kg'
        },
    })
    assert len(Database('biosphere')) == 2

    techno_UP = Database("techno_UP")
    techno_UP.register()
    techno_UP.write({
        ("techno_UP", "A"): {
            'exchanges': [
                {
                    'amount': 1.0,
                    'input': ('techno_UP', 'A'),
                    'type': 'production'
                },
                {
                    'amount': 10,
                    'input': ('techno_UP', 'B'),
                    'type': 'technosphere'
                },
                {
                    'amount': 100,
                    'input': ('biosphere', '1'),
                    'type': 'biosphere'
                },
                {
                    'amount': 1000,
                    'input': ('biosphere', '2'),
                    'type': 'biosphere'
                },
            ],
            'name': 'activity A',
            'unit': 'kg',
            'location': 'GLO',
            'reference product': 'A',
            'production amount': 1
        },
        ("techno_UP", "B"): {
            'exchanges': [
                {
                    'amount': 1.0,
                    'input': ('techno_UP', 'B'),
                    'type': 'production'
                },
                {
                    'amount': 25,
                    'input': ('biosphere', '1'),
                    'type': 'biosphere'
                },
                {
                    'amount': 50,
                    'input': ('biosphere', '2'),
                    'type': 'biosphere'
                },
            ],
            'name': 'activity B',
            'unit': 'kg',
            'location': 'GLO',
            'reference product': 'B',
            'production amount': 1
        },
    })
    m1_name = ('some', 'LCIA', 'method')
    m1 = Method(m1_name)
    m1.register()
    m1.metadata['unit'] = "Some impact unit"
    m1.write(
        [
            (("biosphere", "1"), 1),
            (("biosphere", "2"), 10),
        ]
    )

    m2_name = ('some other', 'LCIA', 'method')
    m2 = Method(m2_name)
    m2.register()
    m2.metadata['unit'] = "Some other impact unit"
    m2.write(
        [
            (("biosphere", "1"), 100),
            (("biosphere", "2"), 42),
        ]
    )
    print(projects.dir)
    yield {'project': projects.current, 'm1_name': m1_name, 'm2_name': m2_name}

    rmtree(projects.dir, ignore_errors=True)
