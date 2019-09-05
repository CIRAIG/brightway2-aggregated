import brightway2 as bw
import pyprind
import hashlib
import copy
import numpy as np

def copy_stripped_activity_to_other_db(data, target_db, exist_ok=False,
                                       create_database_on_fly=False):
    """ Create an activity in `Database(target_db)` with only a production flow.

    Typical usage is the generation of an aggregated dataset: unit impacts would
    then be added to the activity as required, as biosphere exchanges.
    """
    # Check that the target database
    if not target_db in bw.databases:
        if not create_database_on_fly:
            raise ValueError("Database {} does not exist, set "
                             "`create_database_on_fly` to automatically create "
                             "database".format(target_db))
        else:
            bw.Database(target_db).register()

    # Check that all the required data is present
    required_fields = [
        'name',
        'reference product',
        'production amount',
        'location',
        'unit'
    ]
    missing_fields = [field for field in required_fields if field not in data]
    assert not missing_fields, "Fields missing: {}".format(missing_fields)

    if data.get('code'):
        new_code = data['code']
    else:
        s = "".join([data[field] for field in required_fields])
        new_code = str(hashlib.md5(s.encode('utf-8')).hexdigest())

    # Create or update target activity
    if (target_db, new_code) in bw.Database(target_db):
        if not exist_ok:
            raise ValueError("Activity already exists in target database")
        else:
            act = bw.get_activity((target_db, new_code))
            act['location'] = data['location']
            act['name'] = data['name']
            act['unit'] = data['unit']
    else:
        act = bw.Database(target_db).new_activity(
            code=new_code,
            name=data['name'],
            location=data['location'],
            unit=data['unit'],
        )

    act['reference product'] = data['reference product']
    act['production amount'] = data['production amount']
    act.save()

    # Create or update production exchange
    if single_production_exchange_exists((target_db, new_code)):
        exc = [p for p in act.production()][0]
        exc['name'] = data['reference product'],
        exc['location'] = data['location'],
        exc['input'] = act.key,
        exc['output'] = act.key,
        exc['amount'] = data['production amount'],
        exc['type'] = "production"
    else:
        exc = act.new_exchange(
            name=data['reference product'],
            location=data['location'],
            input=act.key,
            output=act.key,
            amount=data['production amount'],
            type="production"
        )
    exc.save()
    return act


def single_production_exchange_exists(act_key):
    """Return True if single production exchange exists

    Will throw error if more than one production exchange found
    """
    assert act_key in bw.Database(act_key[0])
    act = bw.get_activity(act_key)
    p = [exc for exc in act.production()]
    if len(p)>1:
        raise ValueError("Activity {} has {} production exchanges".format(act_key, len(p)))
    else:
        return True if p else False

