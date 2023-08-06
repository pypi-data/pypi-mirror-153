import math
import os
import sys
import pytest
from dotenv import load_dotenv
from os import environ
import random
import string
import shutil
from faker.providers.person.en import Provider
import numpy as np
import pandas as pd
import time

GB = 1024. * 1024. * 1024.
MB = 1024. * 1024.


def pytest_addoption(parser):
    """
    adds the option to write --file=<your path to connector.py>
    """
    parser.addoption(
        "--source", action="store_true", default=False, help="run source tests"
    )
    parser.addoption(
        "--destination", action="store_true", default=False, help="run destination tests"
    )


@pytest.fixture(scope="session")
def root_dir():
    return os.path.dirname(os.path.abspath(".env.credentials"))


def add_root_dir_to_path(root_dir):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), root_dir))
    # print(path)
    if path not in sys.path:
        sys.path.insert(1, path)


@pytest.fixture(scope="session", autouse=True)
def copy_ini_to_root(root_dir):
    add_root_dir_to_path(root_dir)
    shutil.copy(os.path.join(os.path.dirname(__file__), "pytest.txt"),
                os.path.abspath("pytest.ini"))


@pytest.fixture(scope="session")
def module_name(pytestconfig):
    return pytestconfig.getoption("lib-path")


@pytest.fixture(scope="session",
                autouse=True)
def connector_class(root_dir):
    """ This takes in the connector file name and tries to import it """
    try:
        add_root_dir_to_path(root_dir)
        import src.connector as _conn
        return _conn
    except Exception:
        raise Exception("Error: cannot locate Connector class in session <session name>")


@pytest.fixture(scope="session")
def env_file(pytestconfig):
    return ".env.credentials"


def pytest_configure(config):
    config.addinivalue_line("markers", "source: mark test as a source function")


@pytest.fixture(scope="session")
def env(env_file):
    load_dotenv(env_file)
    return environ


@pytest.fixture(scope="session")
def good_object_id(env):
    return env["OBJECT_ID"]


@pytest.fixture(scope="session")
def bad_object_id(env):
    return env["OBJECT_ID"] + "_bad"


@pytest.fixture(scope="session")
def good_credentials(env):
    """ This takes the credentials in the env file and converts it to a dictionary """
    keys = list(env.keys())
    values = list(env.values())
    res = {keys[i].lower(): values[i] for i in range(len(keys))}
    if "USER_NAME" in env.keys():
        res["username"] = env["USER_NAME"]
    return res


@pytest.fixture(scope="session")
def bad_credentials(env):
    """ This has all the keys in the credentials object but those keys are mapped to random integers """
    keys = list(env.keys())
    res = {keys[i].lower(): str(i) for i in range(len(keys))}
    return res


@pytest.fixture(scope="session")
def filtered_column_nm(env):
    return env["FILTERED_COLUMN_NM"]


@pytest.fixture(scope="session")
def filtered_column_date_format(env):
    return env["FILTERED_COLUMN_DATE_FORMAT"]


@pytest.fixture(scope="session")
def earliest_date():
    return "0000-01-01"


@pytest.fixture(scope="session")
def custom_date_start_val():
    return "1941-03-26"


@pytest.fixture(scope="session")
def custom_date_end_val():
    return "2000-01-01"


@pytest.fixture(scope="session")
def connector(connector_class, good_credentials):
    connector = connector_class.Connector(good_credentials)
    return connector


@pytest.fixture(scope="session")
def good_authentication(connector):
    results = connector.authenticate()
    return results


@pytest.fixture(scope="session")
def get_good_objects(connector):
    connector.authenticate()
    objects = connector.get_objects()
    return objects


@pytest.fixture(scope="session")
def get_good_fields(good_object_id, connector):
    connector.authenticate()
    results = connector.get_fields(good_object_id)
    return results


@pytest.fixture(scope="session")
def get_all_good_field_ids(good_object_id, connector):
    connector.authenticate()
    results = connector.get_fields(good_object_id)
    return [result["field_id"] for result in results]


@pytest.fixture(scope="session")
def get_three_good_field_ids(good_object_id, connector):
    connector.authenticate()
    results = connector.get_fields(good_object_id)
    field_ids = [result["field_id"] for result in results]
    return field_ids[:3]


@pytest.fixture(scope="session")
def bad_field_ids(get_all_good_field_ids):
    FIELD_ID_LEN = 10

    # create a random 10-char string to add to get_good_field_ids
    letters = string.ascii_lowercase
    field_id = ''.join(random.choice(letters) for i in range(FIELD_ID_LEN))

    # if the random string happens to be a valid field id for this object, try again
    num_tries = 0
    while field_id in get_all_good_field_ids:
        num_tries += 1

        # if it tries 15 times and is still a valid field id, throw an exception
        if num_tries > 15:
            raise Exception
        field_id = ''.join(random.choice(letters) for i in range(FIELD_ID_LEN))

    # changing the last valid field id for the invalid one
    field_ids = get_all_good_field_ids
    field_ids[-1] = field_id
    return field_ids


@pytest.fixture(scope="session")
def bad_filters_data_type(env):
    # ? maybe have a field called "FILTERED_COLUMN_NM_WRONG_DATA_TYPE"?
    return {
        "filtered_column_nm": env["FILTERED_COLUMN_NM"],
        "start_selection_nm": env["FILTERED_SELECTION_NM"],
        "end_selection_nm": env["END_SELECTION_NM"],
        "start_value_txt": env["START_VALUE_TXT"],
        "end_value_txt": env["END_VALUE_TXT"],
        "timezone_offset_nbr": int(env["TIMEZONE_OFFSET_NBR"])
    }


@pytest.fixture(scope="session")
def get_good_data_small(connector, good_object_id, get_all_good_field_ids):
    connector.authenticate()
    # Since we are using a test account, we should have made some data for the selected object_id
    data = connector.get_data(object_id=good_object_id, field_ids=get_all_good_field_ids, n_rows=5)
    return data


@pytest.fixture(scope="session")
def get_good_meta_data(connector):
    connector.authenticate()
    meta = connector.get_metadata()
    return meta


@pytest.fixture(scope="session")
def batch_size():
    return 2.5 * MB


def random_names(name_type, size):
    """
    Generate n-length ndarray of person names.
    name_type: a string, either first_names or last_names
    """
    names = getattr(Provider, name_type)
    return np.random.choice(names, size=size)


def random_genders(size, p=None):
    """Generate n-length ndarray of genders."""
    if not p:
        # default probabilities
        p = (0.49, 0.49, 0.01, 0.01)
    gender = ("M", "F", "O", "")
    return np.random.choice(gender, size=size, p=p)


def random_dates(start, end, size):
    """
    Generate random dates within range between start and end.
    """
    # Unix timestamp is in nanoseconds by default, so divide it by
    # 24*60*60*10**9 to convert to days.
    divide_by = 24 * 60 * 60 * 10 ** 9
    start_u = start.value // divide_by
    end_u = end.value // divide_by
    return pd.to_datetime(np.random.randint(start_u, end_u, size), unit="D")


def random_numbers(start, end, size):
    """
    Generate random numbers within range between start and end.
    """
    return np.random.randint(start, end, size)


@pytest.fixture(scope="session")
def five_column_100_row_dataset():
    size = 100
    df = pd.DataFrame(columns=['First', 'Last', 'Gender', 'Birthdate'])
    df['First'] = random_names('first_names', size)
    df['Last'] = random_names('last_names', size)
    df['Gender'] = random_genders(size)
    df['BirthDate'] = random_dates(start=pd.to_datetime('1940-01-01'), end=pd.to_datetime('2022-01-01'), size=size)
    df['StartDate'] = random_dates(start=pd.to_datetime('1940-01-01'), end=pd.to_datetime('2022-01-01'), size=size)
    return to_dc_format(df)


@pytest.fixture(scope="session")
def batch_rows():
    return 200000


@pytest.fixture(scope="session")
def batch(batch_rows):
    size = batch_rows
    df = pd.DataFrame(columns=['First', 'Last', 'Gender', 'Birthdate'])
    df['First'] = random_names('first_names', size)
    df['Last'] = random_names('last_names', size)
    df['Gender'] = random_genders(size)
    df['BirthDate'] = random_dates(start=pd.to_datetime('1940-01-01'), end=pd.to_datetime('2022-01-01'), size=size)
    df['StartDate'] = random_dates(start=pd.to_datetime('1940-01-01'), end=pd.to_datetime('2022-01-01'), size=size)
    return to_dc_format(df)


@pytest.fixture(scope="session", params=[0.1, 0.25, 0.5, 1.0, 10.0, 100.0, 1000.0])
def num_gigs(request):
    return request.param


@pytest.fixture(scope="session")
def load_data(connector, batch, good_object_id, mapping_object, _replace, num_gigs, batch_size, batch_rows):
    print(f"\nNow loading {num_gigs} GB!")
    size = num_gigs
    batch_number = 1
    rows_loaded = 0
    generate_data_time = 0
    elapsed_time = 0
    total_batches = math.ceil((size * GB) / float(sys.getsizeof(batch)))

    start = time.time()
    connector.load_data(batch, good_object_id, mapping_object, _replace, batch_number, total_batches)
    end = time.time()
    elapsed_time += (end - start)

    while batch_number <= total_batches:
        rows_loaded += len(batch)
        print(f"Batch {batch_number}/{total_batches}: Loaded {rows_loaded} rows out of {total_batches * batch_rows} "
              f"in {elapsed_time} seconds.")
        batch_number += 1

        start = time.time()
        connector.load_data(batch, good_object_id, mapping_object, _replace, batch_number, total_batches)
        end = time.time()
        elapsed_time += (end - start)

    print(f"Loaded {rows_loaded} rows out of {total_batches * batch_rows}."
          f"\nTotal size uploaded: {size * GB} bytes, which is {size} GB.")
    with open("load_test_results.txt", "a") as f:
        f.write(f"LoadTest for {size} GB")
        f.write(f"Loaded {rows_loaded} rows out of {total_batches * batch_rows}."
                f"\nTotal size uploaded: {size * GB} bytes, which is {size} GB.")

        hours = math.floor(elapsed_time / (60. * 60.))
        minutes = math.floor((elapsed_time % (60. * 60.)) / 60.)
        seconds = (elapsed_time % (60. * 60.)) % 60.
        formatted_time = f"{hours} Hours {minutes} Minutes and {seconds} Seconds"

        print(f"Time elapsed to load {num_gigs} GB: {formatted_time}.")
        f.write(f"Time elapsed to load {num_gigs} GB: {formatted_time}.")
        assert elapsed_time < (10. * 60.)
        return True


@pytest.fixture(scope="session")
def mapping_object():
    # FIXME: these data types might be different for different connectors but its fine for right now
    return [
        {'source_field_id': "First", 'destination_field_id': "newfirst", 'datatype': "varchar(128)", 'size': None},
        {'source_field_id': "Last", 'destination_field_id': "newlast", 'datatype': "varchar(256)", 'size': None},
        {'source_field_id': "Gender", 'destination_field_id': "newgender", 'datatype': "varchar(128)", 'size': None},
        {'source_field_id': "BirthDate", 'destination_field_id': "newbirthdate", 'datatype': "date", 'size': None},
        {'source_field_id': "StartDate", 'destination_field_id': "newstartdate", 'datatype': "date", 'size': None}
    ]


def ten_column_dataset(num_rows):
    size = num_rows
    df = pd.DataFrame(columns=['First', 'Last', 'Gender', 'Birthdate'])
    df['First'] = random_names('first_names', size)
    df['Last'] = random_names('last_names', size)
    df['Gender'] = random_genders(size)
    df['BirthDate'] = random_dates(start=pd.to_datetime('1940-01-01'), end=pd.to_datetime('2022-01-01'), size=size)
    df['StartDate'] = random_dates(start=pd.to_datetime('1940-01-01'), end=pd.to_datetime('2022-01-01'), size=size)
    df['FavoriteNum'] = random_numbers(start=0, end=1000000, size=size)
    df['LeastFavoriteNum'] = random_numbers(start=0, end=1000000, size=size)
    df['NumberOfTimesSaidHello'] = random_numbers(start=0, end=1000000, size=size)
    df['SaddestAge'] = random_numbers(start=0, end=1000000, size=size)
    df['NumberOfPushupsDoneEver'] = random_numbers(start=0, end=1000000, size=size)
    return to_dc_format(df)


def to_dc_format(df):
    df = df.to_dict("records")
    return df


@pytest.fixture(scope="session")
def _append():
    return 0


@pytest.fixture(scope="session")
def _replace():
    return 1

