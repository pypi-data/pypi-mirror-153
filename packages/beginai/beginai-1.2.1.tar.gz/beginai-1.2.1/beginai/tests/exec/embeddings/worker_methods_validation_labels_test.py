from .mock_service import BeginWorkerMock

APP_ID = 1
LICENSE_KEY = 10

def test_add_label_for_user():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = "user"
    object_id = 10
    label = 'test'

    bw.register_user(object_id)
    bw.add_label(object_name, object_id, label)

    results = bw.get_data().get('user')
    assert results == { 
        object_id: {
            "labels": [label]
        }
    }

def test_add_more_than_one_label_for_user():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = "user"
    object_id = 10
    label = 'test'
    label_2 = 'test_2'

    bw.register_user(object_id)
    bw.add_label(object_name, object_id, label)
    bw.add_label(object_name, object_id, label_2)

    results = bw.get_data().get('user')
    assert results == { 
        object_id: {
            "labels": [label, label_2]
        }
    }


def test_add_more_than_one_label_for_different_object():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = "book"
    object_id = 20
    label = 'test'
    label_2 = 'test_2'

    bw.register_user(10)
    bw.add_label("user", 10, label)
    bw.add_label("user", 10, label_2)

    bw.register_object(object_name, object_id)
    bw.add_label(object_name, object_id, 'object_label')

    results = bw.get_data()
    assert results == {'user': {10: {'labels': ['test', 'test_2']}}, 'interactions': {}, 'book': {20: {'labels': ['object_label']}}}

def test_add_label_validation_when_object_not_registered():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    try:
        bw.add_label(object_id=1, object_name='user', label='test')
    except ValueError:
        assert True

def test_add_label_validation_when_label_not_provided():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(1)
    try:
        bw.add_label(object_id=1, object_name='user', label='')
    except ValueError:
        assert True
