from .mock_service import BeginWorkerMock

APP_ID = 1
LICENSE_KEY = 10

def test_register_user_that_doesnt_exist_yet():
    user_id = 1231212
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(user_id)
    assert bw.get_data().get("user") == { user_id: {}}

def test_register_user_when_user_already_exists_do_nothing():
    user_id = 1231212
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)

    bw.register_user(user_id)
    bw.register_user(user_id)
    assert bw.get_data().get("user") == { user_id: {}}


def test_register_user_more_than_one_user():
    user_id_1 = 1231212
    user_id_2 = 8888888
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)

    bw.register_user(user_id_1)
    bw.register_user(user_id_2)
    assert bw.get_data().get("user") == { user_id_1: {}, user_id_2: {}}

def test_update_user_text_field():
    user_id = 12312125
    value = 'Hello'
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(user_id)
    bw.update_user_text_field(user_id, "text", value)

    expected = { user_id: { "text": value } }

    assert bw.get_data().get("user") == expected

def test_update_user_text_field_returns_error_when_value_provided_is_not_string():
    user_id = 12312125
    value = 123
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(user_id)

    try:
        bw.update_user_text_field(user_id, "text", value)
    except ValueError:
        assert True

def test_update_user_text_field_returns_error_when_fields_are_not_provided():
    user_id = 12312125
    value = 'Hello'
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(user_id)
    try:
        bw.update_user_text_field(None, "text", value)
    except ValueError:
        assert True

    try:
        bw.update_user_text_field(user_id, None, value)
    except ValueError:
        assert True

    try:
        bw.update_user_text_field(user_id, "text", None)
    except ValueError:
        assert True

def test_update_user_numerical_field():
    user_id = 12312125
    value = 10.0
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(user_id)
    bw.update_user_numerical_field(user_id, "number", value)

    expected = { user_id: { "number": value } }

    assert bw.get_data().get("user") == expected

def test_update_user_numerical_field_when_fields_are_not_provided():
    user_id = 12312125
    value = 10
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(user_id)
    try:
        bw.update_user_numerical_field(None, "number", value)
    except ValueError:
        assert True

    try:
        bw.update_user_numerical_field(user_id, None, value)
    except ValueError:
        assert True

    try:
        bw.update_user_numerical_field(user_id, "number", None)
    except ValueError:
        assert True

def test_update_user_numerical_field_returns_error_when_value_provided_is_not_number():
    user_id = 12312125
    value = "a"
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(user_id)

    try:
        bw.update_user_numerical_field(user_id, "number", value)
    except ValueError:
        assert True

def test_update_user_date_field():
    user_id = 12312125
    date = '16-05-1991'
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(user_id)
    bw.update_user_date_field(user_id, "userBirthDate", date)

    expected = { user_id: { "userbirthdate": date } }

    assert bw.get_data().get("user") == expected

def test_update_user_date_field_fails_when_the_user_is_not_registered():
    user_id = 12312125
    date = '16-05-1991'
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)

    try:
        bw.update_user_date_field(user_id, "userBirthDate", date)
    except ValueError:
        assert True

def test_update_user_date_field_fails_when_the_field_is_not_provided():
    user_id = 12312125
    date = '16-05-1991'
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(user_id)

    try:
        bw.update_user_date_field(user_id, '', date)
    except ValueError:
        assert True

def test_update_user_date_field_fails_when_the_date_is_not_provided():
    user_id = 12312125
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(user_id)

    try:
        bw.update_user_date_field(user_id, 'userBirthDate', None)
    except ValueError:
        assert True

def test_update_user_location_field():
    user_id = 1231212
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(user_id)
    latitude = 36.8507689
    longitude =  -76.2858726

    bw.update_user_location_field(user_id, "userLocation", latitude, longitude)

    expected = { user_id: { "userlocation": { "latitude": latitude, "longitude": longitude} } }

    assert bw.get_data().get("user") == expected

def test_update_user_location_field_fails_when_user_id_not_registered():
    user_id = 1231212
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    latitude = 36.8507689
    longitude =  -76.2858726

    try:
        bw.update_user_location_field(user_id, "userLocation", latitude, longitude)
    except ValueError:
        assert True

def test_update_user_location_field_fails_when_field_name_not_provided():
    user_id = 1231212
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    latitude = 36.8507689
    longitude =  -76.2858726
    bw.register_user(user_id)

    try:
        bw.update_user_location_field(user_id, '', latitude, longitude)
    except ValueError:
        assert True

def test_update_user_location_field_fails_when_lat_long_not_provided():
    user_id = 1231212
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    latitude = 36.8507689
    longitude =  -76.2858726
    bw.register_user(user_id)

    try:
        bw.update_user_location_field(user_id, 'location', None, longitude)
    except ValueError:
        assert True

    try:
        bw.update_user_location_field(user_id, 'location', latitude, None)
    except ValueError:
        assert True

def test_update_user_boolean_field():
    user_id = 12312125
    value = False
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(user_id)
    bw.update_user_boolean_field(user_id, "boolean", value)

    expected = { user_id: { "boolean": value } }

    assert bw.get_data().get("user") == expected

def test_update_user_boolean_field_returns_error_when_value_provided_is_not_boolean():
    user_id = 12312125
    value = 123
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(user_id)

    try:
        bw.update_user_boolean_field(user_id, "boolean", value)
    except ValueError:
        assert True

def test_update_user_boolean_field_returns_error_when_fields_are_not_provided():
    user_id = 12312125
    value = 'Hello'
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(user_id)
    try:
        bw.update_user_boolean_field(None, "boolean", value)
    except ValueError:
        assert True

    try:
        bw.update_user_boolean_field(user_id, None, value)
    except ValueError:
        assert True

    try:
        bw.update_user_boolean_field(user_id, "boolean", None)
    except ValueError:
        assert True