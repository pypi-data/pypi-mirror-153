from datetime import datetime, timedelta
from . import errors
import pytest


@pytest.mark.source
@pytest.mark.destination
@pytest.mark.general
class TestGeneral:
    def test_stores_credentials(self, connector, good_credentials):
        assert connector.credentials == good_credentials

    def test_env_has_object_id(self, good_credentials):
        assert "object_id" in good_credentials


@pytest.mark.source
@pytest.mark.destination
@pytest.mark.authenticate
class TestAuth:
    def test_returns_bool(self, good_authentication):
        results = good_authentication
        assert type(results) is bool

    def test_returns_true(self, good_authentication):
        results = good_authentication
        assert results

    def test_no_credentials_raises_authentication_error(self, connector_class):
        _connector = connector_class.Connector(None)
        with pytest.raises(errors.AuthenticationError):
            _connector.authenticate()


@pytest.mark.source
@pytest.mark.destination
@pytest.mark.get_objects
class TestGetObjects:
    def test_returns(self, get_good_objects):
        # Since we are using a test account, we should have made some objects when we made the account
        assert get_good_objects

    def test_returns_list(self, get_good_objects):
        assert type(get_good_objects) is list

    def test_returns_nonempty_list(self, get_good_objects):
        assert len(get_good_objects) > 0

    def test_returns_dicts_in_list(self, get_good_objects):
        objects = get_good_objects
        for obj in objects:
            assert type(obj) is dict

    def test_returns_nonempty_dicts_in_list(self, get_good_objects):
        objects = get_good_objects
        for obj in objects:
            assert len(obj) > 0

    def test_returns_object_id_in_dict(self, get_good_objects):
        objects = get_good_objects
        for obj in objects:
            assert "object_id" in obj

    def test_returns_object_name_in_dict(self, get_good_objects):
        objects = get_good_objects
        for obj in objects:
            assert "object_name" in obj

    def test_returns_object_label_in_dict(self, get_good_objects):
        objects = get_good_objects
        for obj in objects:
            assert "object_label" in obj

    def test_returns_object_group_in_dict(self, get_good_objects):
        objects = get_good_objects
        for obj in objects:
            assert "object_group" in obj


@pytest.mark.source
@pytest.mark.get_fields
class TestGetFields:
    def test_returns_list(self, get_good_fields):
        results = get_good_fields
        assert type(results) is list

    def test_returns_nonempty_list(self, get_good_fields):
        results = get_good_fields
        assert len(results) > 0

    def test_returns_dicts_in_list(self, get_good_fields):
        fields = get_good_fields
        for field in fields:
            assert type(field) is dict

    def test_returns_nonempty_dicts_in_list(self, get_good_fields):
        fields = get_good_fields
        for field in fields:
            assert len(field) > 0

    def test_returns_field_id_in_dict(self, get_good_fields):
        fields = get_good_fields
        for field in fields:
            assert "field_id" in field

    def test_returns_field_name_in_dict(self, get_good_fields):
        fields = get_good_fields
        for field in fields:
            assert "field_name" in field

    def test_returns_field_label_in_dict(self, get_good_fields):
        fields = get_good_fields
        for field in fields:
            assert "field_label" in field

    def test_returns_data_type_in_dict(self, get_good_fields):
        fields = get_good_fields
        for field in fields:
            assert "data_type" in field

    def test_returns_size_in_dict(self, get_good_fields):
        fields = get_good_fields
        for field in fields:
            assert "size" in field

    def test_bad_object_id_throws_error(self, bad_object_id, connector):
        with pytest.raises(errors.BadObjectIDError):
            connector.authenticate()
            connector.get_fields(bad_object_id)


@pytest.mark.source
@pytest.mark.get_data
class TestGetData:
    def test_returns(self, get_good_data_small):
        # Since we are using a test account, we should have made some data for the selected object_id
        data = get_good_data_small
        assert data

    def test_returns_dict(self, get_good_data_small):
        data = get_good_data_small
        assert type(data) is dict

    def test_returns_data_in_dict(self, get_good_data_small):
        data = get_good_data_small
        assert "data" in data

    def test_returns_data_as_list(self, get_good_data_small):
        data = get_good_data_small
        assert type(data["data"]) is list

    def test_returns_nonempty_list(self, get_good_data_small):
        data = get_good_data_small
        assert len(data["data"]) > 0

    def test_returns_dicts_in_list(self, get_good_data_small):
        data = get_good_data_small
        for obj in data["data"]:
            assert type(obj) is dict

    def test_filters_by_field_id(self, good_object_id, get_three_good_field_ids, connector):
        connector.authenticate()
        data = connector.get_data(good_object_id, get_three_good_field_ids, n_rows=5)
        assert len(data["data"][0].keys()) == len(get_three_good_field_ids)

    def test_bad_field_id_throws_error(self, good_object_id, bad_field_ids, connector):
        with pytest.raises(errors.BadFieldIDError):
            connector.authenticate()
            connector.get_data(good_object_id, bad_field_ids)

    def test_returns_nonempty_dicts_in_list(self, get_good_data_small):
        data = get_good_data_small
        for obj in data["data"]:
            assert len(obj) > 0

    def test_returns_next_page_flag(self, get_good_data_small):
        data = get_good_data_small
        assert "next_page" in data

    def test_filters_by_custom_date_returns(self, good_object_id, get_three_good_field_ids, connector,
                                            filtered_column_nm):
        connector.authenticate()
        data = connector.get_data(good_object_id,
                                  get_three_good_field_ids,
                                  filters={
                                      'filtered_column_nm': filtered_column_nm,
                                      'start_selection_nm': "Custom Date",
                                      'end_selection_nm': "Custom Date",
                                      'start_value_txt': "1941-03-26",
                                      'end_value_txt': "2000-01-01",
                                      'timezone_offset_nbr': "1"
                                  })
        assert data

    def test_filters_by_custom_date_works(self,
                                          good_object_id,
                                          get_three_good_field_ids,
                                          connector,
                                          filtered_column_nm,
                                          filtered_column_date_format,
                                          custom_date_start_val,
                                          custom_date_end_val):
        if filtered_column_nm not in get_three_good_field_ids:
            get_three_good_field_ids.append(filtered_column_nm)
        else:
            get_three_good_field_ids
        connector.authenticate()
        data = connector.get_data(good_object_id,
                                  get_three_good_field_ids,
                                  filters={
                                      'filtered_column_nm': filtered_column_nm,
                                      'start_selection_nm': "Custom Date",
                                      'end_selection_nm': "Custom Date",
                                      'start_value_txt': custom_date_start_val,
                                      'end_value_txt': custom_date_end_val,
                                      'timezone_offset_nbr': "1"
                                  },
                                  n_rows=5)
        start = datetime.strptime(custom_date_start_val, "%Y-%m-%d")
        end = datetime.strptime(custom_date_end_val, "%Y-%m-%d")
        for row in data["data"]:
            assert start < datetime.strptime(row[filtered_column_nm], filtered_column_date_format)
            assert datetime.strptime(row[filtered_column_nm], filtered_column_date_format) < end

    def test_filters_by_today_returns(self, good_object_id, get_three_good_field_ids, connector, filtered_column_nm):
        connector.authenticate()
        data = connector.get_data(good_object_id,
                                  get_three_good_field_ids,
                                  filters={
                                      'filtered_column_nm': filtered_column_nm,
                                      'start_selection_nm': "Custom Date",
                                      'end_selection_nm': "Today",
                                      'start_value_txt': "1941-03-26",
                                      'end_value_txt': "",
                                      'timezone_offset_nbr': "1"
                                  })
        assert data

    def test_filters_by_today_works(self,
                                    good_object_id,
                                    get_three_good_field_ids,
                                    connector,
                                    filtered_column_nm,
                                    filtered_column_date_format,
                                    custom_date_start_val,
                                    custom_date_end_val):
        if filtered_column_nm not in get_three_good_field_ids:
            get_three_good_field_ids.append(filtered_column_nm)
        else:
            get_three_good_field_ids
        connector.authenticate()
        data = connector.get_data(good_object_id,
                                  get_three_good_field_ids,
                                  filters={
                                      'filtered_column_nm': filtered_column_nm,
                                      'start_selection_nm': "Custom Date",
                                      'end_selection_nm': "Today",
                                      'start_value_txt': custom_date_start_val,
                                      'end_value_txt': custom_date_end_val,
                                      'timezone_offset_nbr': "1"
                                  },
                                  n_rows=5)
        start = datetime.strptime(custom_date_start_val, "%Y-%m-%d")
        end = datetime.utcnow() - timedelta(days=0, hours=int(1))
        for row in data["data"]:
            assert start < datetime.strptime(row[filtered_column_nm], filtered_column_date_format)
            assert datetime.strptime(row[filtered_column_nm], filtered_column_date_format) < end

    def test_filters_by_yesterday_returns(self, good_object_id, get_three_good_field_ids, connector,
                                          filtered_column_nm):
        connector.authenticate()
        data = connector.get_data(good_object_id,
                                  get_three_good_field_ids,
                                  filters={
                                      'filtered_column_nm': filtered_column_nm,
                                      'start_selection_nm': "Custom Date",
                                      'end_selection_nm': "Yesterday",
                                      'start_value_txt': "1941-03-26",
                                      'end_value_txt': "",
                                      'timezone_offset_nbr': "1"
                                  })
        assert data

    def test_filters_by_yesterday_works(self,
                                        good_object_id,
                                        get_three_good_field_ids,
                                        connector,
                                        filtered_column_nm,
                                        filtered_column_date_format,
                                        custom_date_start_val,
                                        custom_date_end_val):
        if filtered_column_nm not in get_three_good_field_ids:
            get_three_good_field_ids.append(filtered_column_nm)
        connector.authenticate()
        data = connector.get_data(good_object_id,
                                  get_three_good_field_ids,
                                  filters={
                                      'filtered_column_nm': filtered_column_nm,
                                      'start_selection_nm': "Custom Date",
                                      'end_selection_nm': "Yesterday",
                                      'start_value_txt': custom_date_start_val,
                                      'end_value_txt': custom_date_end_val,
                                      'timezone_offset_nbr': "1"
                                  },
                                  n_rows=5)
        start = datetime.strptime(custom_date_start_val, "%Y-%m-%d")
        end = datetime.utcnow() - timedelta(days=1, hours=int(1))
        for row in data["data"]:
            assert start < datetime.strptime(row[filtered_column_nm], filtered_column_date_format)
            assert datetime.strptime(row[filtered_column_nm], filtered_column_date_format) < end

    def test_filters_no_start_selection(self,
                                        good_object_id,
                                        get_three_good_field_ids,
                                        connector,
                                        filtered_column_nm,
                                        filtered_column_date_format,
                                        custom_date_end_val):
        if filtered_column_nm not in get_three_good_field_ids:
            get_three_good_field_ids.append(filtered_column_nm)
        connector.authenticate()
        data = connector.get_data(good_object_id,
                                  get_three_good_field_ids,
                                  filters={
                                      'filtered_column_nm': filtered_column_nm,
                                      'start_selection_nm': None,
                                      'end_selection_nm': "Yesterday",
                                      'start_value_txt': None,
                                      'end_value_txt': custom_date_end_val,
                                      'timezone_offset_nbr': "1"
                                  },
                                  n_rows=5)
        end = datetime.utcnow() - timedelta(days=1, hours=int(1))
        for row in data["data"]:
            assert datetime.strptime(row[filtered_column_nm], filtered_column_date_format) < end

    def test_filters_no_end_selection(self,
                                      good_object_id,
                                      get_three_good_field_ids,
                                      connector,
                                      filtered_column_nm,
                                      filtered_column_date_format,
                                      custom_date_start_val):
        if filtered_column_nm not in get_three_good_field_ids:
            get_three_good_field_ids.append(filtered_column_nm)
        connector.authenticate()
        data = connector.get_data(good_object_id,
                                  get_three_good_field_ids,
                                  filters={
                                      'filtered_column_nm': filtered_column_nm,
                                      'start_selection_nm': "Custom Date",
                                      'end_selection_nm': None,
                                      'start_value_txt': custom_date_start_val,
                                      'end_value_txt': None,
                                      'timezone_offset_nbr': "1"
                                  },
                                  n_rows=5)
        start = datetime.strptime(custom_date_start_val, "%Y-%m-%d")
        for row in data["data"]:
            assert start < datetime.strptime(row[filtered_column_nm], filtered_column_date_format)


@pytest.mark.destination
@pytest.mark.get_metadata
class TestGetMetaData:

    def test_returns_column_type_flg(self, get_good_meta_data):
        data = get_good_meta_data
        assert "column_type_flg" in data

    def test_returns_size_flg(self, get_good_meta_data):
        data = get_good_meta_data
        assert "size_flg" in data

    def test_returns_new_object_regex(self, get_good_meta_data):
        data = get_good_meta_data
        assert "new_object_regex" in data

    def test_returns_size_regex(self, get_good_meta_data):
        data = get_good_meta_data
        assert "size_regex" in data

    def test_returns_data_types(self, get_good_meta_data):
        data = get_good_meta_data
        assert "data_types" in data


@pytest.mark.destination
@pytest.mark.load_data
class TestLoadData:

    def test_load_data_append(self, connector, good_object_id, mapping_object, _append, five_column_100_row_dataset):
        try:
            connector.load_data(five_column_100_row_dataset,
                                good_object_id,
                                mapping_object,
                                _append,
                                batch_number=1,
                                total_batches=1)
        except Exception as e:
            assert False, f"Appending 100 rows of 5-column data raised an exception {e}"

    def test_load_data_replace(self, connector, good_object_id, mapping_object, _replace, five_column_100_row_dataset):
        try:
            connector.load_data(five_column_100_row_dataset,
                                good_object_id,
                                mapping_object,
                                _replace,
                                batch_number=1,
                                total_batches=1)
        except Exception as e:
            assert False, f"Replacing 100 rows of 5-column data raised an exception {e}"

    def test_load_data_create_new_table(self,
                                        connector,
                                        bad_object_id,
                                        mapping_object,
                                        _replace,
                                        five_column_100_row_dataset):
        # FIXME: a potential issue here is that i do not have object name validation for "_bad" on an object_id
        connector.load_data(five_column_100_row_dataset,
                            bad_object_id,
                            mapping_object,
                            _replace,
                            batch_number=1,
                            total_batches=1)
        connector.authenticate()
        objects = connector.get_objects()
        assert bad_object_id in [obj["object_id"] for obj in objects]

    @pytest.mark.load_test_slow
    def test_load_large_data(self,
                             load_data):
        assert load_data

