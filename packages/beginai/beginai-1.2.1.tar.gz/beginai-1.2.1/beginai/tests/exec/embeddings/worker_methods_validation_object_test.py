from .mock_service import BeginWorkerMock

APP_ID = 1
LICENSE_KEY = 10

def test_register_object_without_object_name():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    try:
        bw.register_object(object_name='', object_id=12)
    except ValueError:
        assert True

def test_register_object_without_object_id():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    try:
        bw.register_object(object_name='name', object_id=None)
    except ValueError:
        assert True

def test_register_object():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = 'Product'
    object_id = 10
    bw.register_object(object_name, object_id)

    expected = {
        object_name.lower() : { object_id: { }},
        "user": {},
        "interactions": {}
    }

    assert bw.get_data() == expected

def test_register_object_more_than_one():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = 'Product'
    object_id_1 = 10
    object_id_2 = 20
    bw.register_object(object_name, object_id_1)
    bw.register_object(object_name, object_id_2 )

    expected = {
        object_name.lower() : { object_id_1: { }, object_id_2: { } },
        "user": {},
        "interactions": {}
    }

    assert bw.get_data() == expected

def test_update_object_text_field_when_object_not_registered():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = 'Product'
    object_id = 10
    field = "bio"
    value = "test test"

    try:
        bw.update_object_text_field(object_name, object_id, field, value)
    except ValueError:
        assert True

def test_update_object_text_field_when_value_is_not_string():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = 'Product'
    object_id = 10
    field = "bio"
    value = 10
    bw.register_object(object_name, object_id)

    try:
        bw.update_object_text_field(object_name, object_id, field, value)
    except ValueError:
        assert True

def test_update_object_text_field_when_object_parameters_not_provided():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = 'Product'
    object_id = 10
    field = "bio"
    value = "test test"

    try:
        bw.update_object_text_field('', object_id, field, value)
    except ValueError:
        assert True

    bw.register_object(object_name, object_id)
    
    try:
        bw.update_object_text_field(object_name, None, field, value)
    except ValueError:
        assert True

    try:
        bw.update_object_text_field(object_name, object_id, None, value)
    except ValueError:
        assert True

    try:
        bw.update_object_text_field(object_name, object_id, field, None)
    except ValueError:
        assert True

def test_update_object_text_field_when_object_id_not_registered():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = 'Product'
    object_id_exists = 10
    object_id_doesnt_exist = 20
    field = "bio"
    value = "test test"

    bw.register_object(object_name, object_id_exists)

    try:
        bw.update_object_text_field(object_name, object_id_doesnt_exist, field, value)
    except ValueError:
        assert True

def test_update_object_numerical():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = 'Product'
    object_id = 10
    field = "bio"
    value = 10
    bw.register_object(object_name, object_id)

    bw.update_object_numerical_field(object_name, object_id, field, value)
    assert bw.get_data().get(object_name.lower()).get(object_id) == { field: value}

def test_update_object_numerical_field_when_value_is_not_valid():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = 'Product'
    object_id = 10
    field = "bio"
    value = "10"
    bw.register_object(object_name, object_id)

    try:
        bw.update_object_numerical_field(object_name, object_id, field, value)
    except ValueError:
        assert True

def test_update_object_text_field():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = 'Product'
    object_id = 10
    field = "bio"
    value = "test test"

    bw.register_object(object_name, object_id)

    bw.update_object_text_field(object_name, object_id, field, value)

    assert bw.get_data().get(object_name.lower()).get(object_id) == { field: value}

def test_update_object_date_field():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = 'Product'
    object_id = 10
    field = "date"
    value = "10-10-1991"

    bw.register_object(object_name, object_id)

    bw.update_object_date_field(object_name, object_id, field, value)

    assert bw.get_data().get(object_name.lower()).get(object_id) == { field: value}

def test_update_object_boolean_field():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = 'Product'
    object_id = 10
    field = "boolean"
    value = False

    bw.register_object(object_name, object_id)

    bw.update_object_boolean_field(object_name, object_id, field, value)

    assert bw.get_data().get(object_name.lower()).get(object_id) == { field: value}

def test_update_object_boolean_field_when_object_not_registered():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = 'Product'
    object_id = 10
    field = "bio"
    value = "test test"

    try:
        bw.update_object_boolean_field(object_name, object_id, field, value)
    except ValueError:
        assert True

def test_update_object_boolean_field_when_value_is_not_boolean():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = 'Product'
    object_id = 10
    field = "bio"
    value = 10
    bw.register_object(object_name, object_id)

    try:
        bw.update_object_boolean_field(object_name, object_id, field, value)
    except ValueError:
        assert True

def test_update_object_boolean_field_when_object_parameters_not_provided():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = 'Product'
    object_id = 10
    field = "bio"
    value = "test test"

    try:
        bw.update_object_boolean_field('', object_id, field, value)
    except ValueError:
        assert True

    bw.register_object(object_name, object_id)
    
    try:
        bw.update_object_boolean_field(object_name, None, field, value)
    except ValueError:
        assert True

    try:
        bw.update_object_boolean_field(object_name, object_id, None, value)
    except ValueError:
        assert True

    try:
        bw.update_object_boolean_field(object_name, object_id, field, None)
    except ValueError:
        assert True

def test_update_object_boolean_field_when_object_id_not_registered():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = 'Product'
    object_id_exists = 10
    object_id_doesnt_exist = 20
    field = "bio"
    value = "test test"

    bw.register_object(object_name, object_id_exists)

    try:
        bw.update_object_boolean_field(object_name, object_id_doesnt_exist, field, value)
    except ValueError:
        assert True